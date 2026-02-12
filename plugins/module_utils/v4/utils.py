# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import json

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

    ip_config = obj.to_dict().get("ip_config", [])
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
            msg=f"Missing required parameter(s): {', '.join(missing_params)}"
        )

    return missing_params
