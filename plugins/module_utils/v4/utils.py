# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import json
import os

try:
    # Python 3
    from urllib.parse import unquote, urlparse
except ImportError:
    # Python 2.7
    from urllib import unquote

    from urlparse import urlparse

__metaclass__ = type


def strip_internal_attributes(data, exclude_attributes=None):
    """
    This method will remove v4 api internal fields like _reserved, _object_type and _unknown_fields
    from given data.
    Args:
        data (dict): v4 api data
        exclude_attributes (list): list of attributes that need to exclude
    """
    internal_attributes = [
        "_object_type",
        "_reserved",
        "_unknown_fields",
        "$dataItemDiscriminator",
    ]
    if exclude_attributes is None:
        exclude_attributes = []
    if isinstance(data, dict):
        for attr in internal_attributes:
            if attr in data and attr not in exclude_attributes:
                data.pop(attr)

        for key, val in data.items():
            if isinstance(val, dict):
                strip_internal_attributes(val, exclude_attributes)
            elif isinstance(val, list) and val and isinstance(val[0], dict):
                for item in val:
                    strip_internal_attributes(item, exclude_attributes)
    elif isinstance(data, list):
        for item in data:
            strip_internal_attributes(item, exclude_attributes)

    return data


def _get_nested_value(obj, dotted_path):
    """
    Get a nested value from a dict using a dotted path.

    Example:
        _get_nested_value({"address": {"ipv4": {"value": "1.2.3.4"}}}, "address.ipv4.value")
        -> "1.2.3.4"
    """
    if obj is None or dotted_path is None:
        return None
    current_val = obj
    for part in str(dotted_path).split("."):
        if not isinstance(current_val, dict) or part not in current_val:
            return None
        current_val = current_val[part]
    return current_val


def filter_entities_by_attribute_get_ext_id(
    entities,
    attribute_path,
    expected_value,
    ext_id_key="ext_id",
):
    """
    Filter a list of entity dicts by a (possibly nested) attribute and return the matching ext_id.

    Args:
        entities (list[dict]|None): entities to search (e.g. config['users'] or config['traps'])
        attribute_path (str): attribute name or dotted path (e.g. 'username' or 'address.ipv4.value')
        expected_value: value to match with == (after extraction)
        ext_id_key (str): field name that contains the external id (default: 'ext_id')

    Returns:
        str|None: the first matched entity's ext_id, or None if no match.
    """
    if not entities:
        return None
    for item in entities:
        if not isinstance(item, dict):
            continue
        actual = _get_nested_value(item, attribute_path)
        if actual == expected_value:
            return item.get(ext_id_key)
    return None


def raise_api_exception(module, exception, msg=None):
    """
    This routine raise module failure as per exception
    Args:
        module (AnsibleModule): certain ansible module
        exception(ApiException): api exception object
        msg (str): error message
    """
    kwargs = {
        "msg": msg,
        "status": getattr(exception, "status", ""),
        "error": getattr(exception, "reason", ""),
    }
    if getattr(exception, "body", None):
        kwargs["response"] = json.loads(exception.body)
    else:
        kwargs["response"] = str(exception)
    module.fail_json(**kwargs)


def strip_antivirus_extra_attributes(obj):
    """
    This method will remove antivirus object's extra fields from given object.
    Args:
        obj (object): antivirus object
    Returns:
        object: antivirus object with stripped extra fields
    """

    extra_fields = ["connection_status", "partner"]

    for field in extra_fields:
        setattr(obj, field, None)

    return obj


def strip_users_empty_attributes(obj):
    """
    This method will remove empty attributes from given user object.
    Args:
        obj (object): user object
    Returns:
        object: user object with stripped empty attributes
    """
    exclude = ["password"]

    for key, value in obj.to_dict().items():
        if value == "" and key not in exclude:
            setattr(obj, key, None)


def remove_empty_ip_config(obj):
    """
    This method will remove empty ip_config from given object.
    Args:
        obj (object): object
    Returns:
        object: object with stripped empty ip_config
    """
    internal_attributes = [
        "_object_type",
        "_reserved",
        "_unknown_fields",
        "$dataItemDiscriminator",
    ]

    ip_config = obj.to_dict().get("ip_config") or []
    empty_ipv4 = False
    empty_ipv6 = False
    for item in ip_config.copy():
        if not item.get("ipv4") or all(
            value is None
            for key, value in item["ipv4"].items()
            if key not in internal_attributes
        ):
            empty_ipv4 = True
        if not item.get("ipv6") or all(
            value is None
            for key, value in item["ipv6"].items()
            if key not in internal_attributes
        ):
            empty_ipv6 = True

        if empty_ipv6 and empty_ipv4:
            ip_config.remove(item)
    setattr(obj, "ip_config", ip_config)


def remove_fields_from_spec(obj, fields_to_remove, deep=False):
    """
    Removes specified fields from a given object (dict or list).
    If deep=True, it removes the fields recursively.
    Modifies the object in-place.

    Args:
        obj (dict | list): The object to strip fields from.
        fields_to_remove (set): Field names to remove.
        deep (bool): Whether to remove fields recursively.
    """
    if isinstance(obj, dict):
        # First, remove the unwanted keys at current level
        for field in fields_to_remove:
            if field in obj:
                del obj[field]

        # If deep, recurse into values
        if deep:
            for key in list(obj.keys()):
                value = obj[key]
                remove_fields_from_spec(value, fields_to_remove, deep=True)

    elif isinstance(obj, list):
        # Recurse into each item if deep
        if deep:
            for item in obj:
                remove_fields_from_spec(item, fields_to_remove, deep=True)


def validate_required_params(module, required_params):
    """
    This routine checks if all required parameters are present in module.params
    and fails if any are missing.

    Args:
        module: AnsibleModule object
        required_params: List of required parameter names
                        Example: ['name', 'type', 'cluster_uuid']

    Returns:
        list: List of missing parameter names (empty if all present)
    """
    missing_params = []

    for param in required_params:
        if param not in module.params or module.params[param] is None:
            missing_params.append(param)

    if missing_params:
        module.fail_json(
            msg="Missing required parameter(s): {0}".format(", ".join(missing_params))
        )

    return missing_params


def _get_proxy_url(module=None):
    """
    Get proxy URL from module parameters (preferred) or environment variables.

    Precedence (highest to lowest):
        https_proxy -> http_proxy -> all_proxy  (module params, lowercase)
        HTTPS_PROXY -> HTTP_PROXY -> ALL_PROXY  (environment variables, uppercase)
    """
    proxy_names = [
        "https_proxy",
        "http_proxy",
        "all_proxy",
    ]
    # Check module params first (lowercase)
    for name in proxy_names:
        if name in module.params:
            proxy_url = module.params.get(name)
            if proxy_url:
                return proxy_url
    # Fall back to environment variables (uppercase)
    for name in proxy_names:
        proxy_url = os.environ.get(name.upper())
        if proxy_url:
            return proxy_url
    return None


def _detect_no_proxy(host, module=None):
    """
    Detect if the 'no_proxy' environment variable is set and honor those locations.
    """
    env_no_proxy = module.params.get("no_proxy") or os.environ.get("NO_PROXY")
    if env_no_proxy:
        env_no_proxy = env_no_proxy.split(",")
        netloc = host or ""

        for no_proxy_host in env_no_proxy:
            if netloc.endswith(no_proxy_host) or netloc.split(":")[0].endswith(
                no_proxy_host
            ):
                # Our requested host matches something in no_proxy, so don't
                # use the proxy for this
                return False
    return True


def _apply_proxy_from_env(config, module=None):
    """
    Apply proxy configuration from environment variables.

    Supports credentials either embedded in URL or via separate environment variables:
    - Embedded: http://username:password@proxy:port
    - Separate: PROXY_USERNAME and PROXY_PASSWORD environment variables
    """
    if not _detect_no_proxy(config.host, module):
        return

    proxy_url = _get_proxy_url(module)
    if not proxy_url:
        return

    parsed = urlparse(proxy_url)
    if not parsed.hostname or parsed.scheme == "":
        return

    config.proxy_scheme = parsed.scheme
    config.proxy_host = parsed.hostname
    config.proxy_port = parsed.port or 443

    # Get credentials from URL first, then fall back to separate environment variables
    if parsed.username:
        config.proxy_username = unquote(parsed.username)
    else:
        config.proxy_username = module.params.get("proxy_username") or os.environ.get(
            "PROXY_USERNAME"
        )

    if parsed.password:
        config.proxy_password = unquote(parsed.password)
    else:
        config.proxy_password = module.params.get("proxy_password") or os.environ.get(
            "PROXY_PASSWORD"
        )


def get_task_ext_id_from_response(resp):
    """Return the task ext_id from an async share/unshare API response.

    Only a genuine ``TaskReference`` payload is treated as awaitable. Responses
    that completed synchronously (e.g. IAM's ``DirectoryServiceShareResponse``)
    or that carry an empty list/map return ``None`` so the caller skips waiting.

    Args:
        resp: The SDK response object returned by a share/unshare call.

    Returns:
        str | None: The task external ID, or None when there is no task.
    """
    data = getattr(resp, "data", None)
    if data is None:
        return None
    if type(data).__name__ != "TaskReference":
        return None
    return getattr(data, "ext_id", None)


def reconcile_sharing(
    module,
    api_instance,
    ext_id,
    read_fn,
    share_fn,
    unshare_fn,
    shared_with_projects=None,
    share_all_fn=None,
    unshare_all_fn=None,
    is_shared_with_all=None,
    resource_label="resource",
):
    """Drive a resource's project sharing to the desired state.

    Reads the current sharing state once, then walks the difference against the
    desired state and performs each share/unshare one at a time. Every
    ``share_fn``/``unshare_fn`` call is expected to block until its change is
    applied (task-based APIs wait on their task via ``wait_for_completion``;
    the synchronous IAM endpoints return only once applied), so a single pass
    reaches the desired state. If nothing differs, no call is made and the
    resource is already in the desired state (idempotent no-op).

    Args:
        module: Ansible module object.
        api_instance: SDK API instance, passed through to the callables.
        ext_id (str): External ID of the resource.
        read_fn (callable): ``read_fn(module, ext_id)`` returning the current
            SDK spec of the resource.
        share_fn/unshare_fn (callable): Per-project share/unshare functions
            (signature ``fn(module, api_instance, ext_id, project_ext_id)``).
        shared_with_projects (list | None): Desired list of project ext_ids.
            ``None`` leaves per-project sharing untouched. Ignored when the
            resource ends up shared with all projects, whether because
            ``is_shared_with_all`` was set truthy in this call or the resource
            was already shared with every project, since per-project sharing is
            then redundant.
        share_all_fn/unshare_all_fn (callable | None): Optional all-projects
            share/unshare functions (signature ``fn(module, api_instance, ext_id)``).
        is_shared_with_all (bool | None): Desired shared-with-all-projects state.
            ``None`` leaves it untouched.
        resource_label (str): Human-readable resource name used in the warning
            emitted when ``shared_with_projects`` is ignored because the resource
            is already shared with all projects.

    Returns:
        bool: True if any share/unshare was performed.
    """
    current = read_fn(module, ext_id)
    changed = False

    current_shared_all = bool(
        getattr(current, "is_shared_with_all_projects", None)
        or getattr(current, "shared_with_all_projects", None)
    )

    if is_shared_with_all is not None and share_all_fn and unshare_all_fn:
        if is_shared_with_all and not current_shared_all:
            share_all_fn(module, api_instance, ext_id)
            changed = True
            current_shared_all = True
        elif not is_shared_with_all:
            unshare_all_fn(module, api_instance, ext_id)
            changed = True
            current_shared_all = False

    if shared_with_projects is not None and current_shared_all:
        module.warn(
            "shared_with_projects was ignored because the {0} is shared with all "
            "projects, which already grants access to every project. To manage "
            "per-project sharing, first set is_shared_with_all_projects to false, "
            "then specify shared_with_projects.".format(resource_label)
        )

    if shared_with_projects is not None and not current_shared_all:
        current_projects = set(getattr(current, "shared_with_projects", None) or [])
        desired_projects = set(shared_with_projects)

        for project_ext_id in desired_projects - current_projects:
            share_fn(module, api_instance, ext_id, project_ext_id)
            changed = True

        for project_ext_id in current_projects - desired_projects:
            unshare_fn(module, api_instance, ext_id, project_ext_id)
            changed = True

    return changed


def raise_unsupported_update_fields(module, current_spec, update_spec, fields):
    """
    Fail the module if the user attempts to update fields that the API does
    not allow to be changed.

    Compares the values of each field in ``fields`` between ``current_spec``
    and ``update_spec``.  If any value differs, the module is failed with a
    message listing the offending fields.

    Dot-notation is supported for nested fields.  For example,
    ``"a.b"`` will traverse into key/attribute ``a`` and then compare ``b``.

    Both specs may be SDK model objects (with attributes) or plain dicts;
    the look-up strategy adapts automatically at each nesting level.

    Args:
        module: AnsibleModule instance.
        current_spec: The existing resource spec fetched from the API.
        update_spec: The spec generated from the user-provided parameters.
        fields (list[str]): Field names (dot-notation for nested) for which
            update is not supported.
    """
    if not fields:
        return

    _sentinel = object()

    def _get(obj, name):
        if isinstance(obj, dict):
            return obj.get(name, _sentinel)
        return getattr(obj, name, _sentinel)

    def _resolve(obj, path):
        for part in path.split("."):
            if obj is _sentinel or obj is None:
                return _sentinel
            obj = _get(obj, part)
        return obj

    changed = []
    for field in fields:
        current_val = _resolve(current_spec, field)
        update_val = _resolve(update_spec, field)
        if current_val != update_val and update_val is not None:
            changed.append(field)

    if changed:
        module.fail_json(
            msg="Update is not supported for the following field(s): {0}".format(
                ", ".join(changed)
            )
        )


def strip_read_only_fields(spec, fields=None):
    """
    Remove server-populated read-only fields from a v4 SDK spec object before
    sending it back as an update body. Modules whose entity has read-only
    fields (e.g. counters populated by the platform) can pass them via
    ``fields``.

    The spec is mutated in place; it is also returned so callers can chain.

    Args:
        spec (object): SDK model object to mutate.
        fields (Iterable[str] | None): Attribute names to remove.

    Returns:
        object: The same ``spec``, with the listed attributes removed.
    """
    if not fields:
        return spec

    for field in fields:
        if hasattr(spec, field):
            delattr(spec, field)
    return spec


def normalize_oneof_marker_values(params, marker_keys):
    """Normalize one-of marker variants from ``null`` to ``{}``.

    Some one-of (discriminated union) variants map to SDK classes with no
    user-facing fields; the variant is selected purely by *which* key is
    present. Users may write either ``some_marker: {}`` or simply
    ``some_marker:`` (null) in their playbook. The latter form would otherwise
    be stripped by ``remove_param_with_none_value`` before the spec generator
    could dispatch it, so we promote ``null`` to ``{}`` for the given marker
    keys here.

    The structure is mutated in place.

    Args:
        params (dict | list): module params (or a nested fragment) to normalize.
        marker_keys (Iterable[str]): keys whose ``null`` value should become ``{}``.
    """
    if isinstance(params, dict):
        for key, value in params.items():
            if key in marker_keys and value is None:
                params[key] = {}
            elif isinstance(value, dict):
                normalize_oneof_marker_values(value, marker_keys)
            elif isinstance(value, list):
                for item in value:
                    normalize_oneof_marker_values(item, marker_keys)
