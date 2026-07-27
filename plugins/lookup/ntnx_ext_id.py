# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    name: ntnx_ext_id
    author:
        - George Ghawali (@george-ghawali)
    short_description: Resolve a Nutanix entity name to its external ID (ext_id) using V4 APIs.
    version_added: "2.6.0"
    description:
        - Resolve human readable names of Nutanix Prism Central entities to their external IDs (UUIDs).
        - This lets playbooks pass names instead of hard coding UUIDs when calling the C(*_v2) modules,
          which require C(ext_id) values for resource references.
        - Each search term is resolved by listing the entity using a server side OData C($filter) and
          returning the matching C(ext_id).
        - Works for any top level entity that exposes a list API supporting a server side
          OData C($filter) and an C(ext_id), across clusters management, networking, virtual
          machine management, volumes, IAM, flow microsegmentation, data protection,
          data policies and objects.
        - This plugin uses PC v4 APIs based SDKs.
    options:
        _terms:
            description:
                - One or more names (or values of O(filter_attribute)) to resolve to external IDs.
                - Terms are flattened one level, so a list variable can be passed as a single
                  argument instead of spelling out every name.
                - Ignored when O(filter) is set, in which case the raw filter is used directly.
            type: list
            elements: str
        resource:
            description:
                - The type of entity to resolve.
            type: str
            required: true
            choices:
                - cluster
                - cluster_profile
                - storage_container
                - subnet
                - vpc
                - virtual_switch
                - floating_ip
                - network_function
                - routing_policy
                - vm
                - image
                - image_placement_policy
                - template
                - ova
                - volume_group
                - iscsi_client
                - category
                - user
                - user_group
                - role
                - operation
                - authorization_policy
                - directory_service
                - saml_identity_provider
                - service_group
                - address_group
                - network_security_policy
                - entity_group
                - recovery_point
                - protection_policy
                - storage_policy
                - object_store
        filter_attribute:
            description:
                - The entity attribute that each search term is matched against using OData C(eq).
                - This is the server side OData property name (camelCase), for example C(name),
                  C(displayName), C(username) or C(key).
                - If not provided, a sensible default is used per resource
                  (C(name) for most resources, C(key) for C(category), C(username) for C(user),
                  C(displayName) for C(role), C(operation) and C(authorization_policy),
                  C(templateName) for C(template) and C(clusterReference) for C(iscsi_client)).
                - Only attributes the V4 list API accepts in a C($filter) can be used. Requesting
                  any other attribute makes the API answer with an OData validation error.
            type: str
        filter:
            description:
                - A raw OData C($filter) expression used as is, instead of building one from the search terms.
                - Use this when names are not unique and you need to add qualifiers,
                  for example C("name eq 'vlan-100' and virtualSwitchReference eq '<uuid>'").
                - When set, O(_terms) is ignored and a single lookup is performed.
            type: str
        fail_on_missing:
            description:
                - If V(true), raise an error when a search term resolves to no entity.
                - If V(false), V(None) is returned for that term instead.
                - Prefer C(query) over C(lookup) when this is V(false), because a V(None) entry
                  cannot be joined into a string. See the notes for details.
            type: bool
            default: true
        fail_on_multiple:
            description:
                - If V(true), raise an error when a search term resolves to more than one entity.
                - If V(false), all matching external IDs are returned.
            type: bool
            default: true
        nutanix_host:
            description:
                - Prism Central hostname or IP address.
            type: str
            required: true
            env:
                - name: NUTANIX_HOSTNAME
                - name: NUTANIX_HOST
        nutanix_username:
            description:
                - Prism Central username.
                - Required unless O(nutanix_api_key) is provided.
            type: str
            env:
                - name: NUTANIX_USERNAME
        nutanix_password:
            description:
                - Prism Central password.
                - Required unless O(nutanix_api_key) is provided.
            type: str
            no_log: true
            env:
                - name: NUTANIX_PASSWORD
        nutanix_api_key:
            description:
                - Prism Central API key, used instead of username and password.
            type: str
            no_log: true
            env:
                - name: NUTANIX_API_KEY
        nutanix_port:
            description:
                - Prism Central port.
            type: str
            default: "9440"
            env:
                - name: NUTANIX_PORT
        validate_certs:
            description:
                - Set to V(false) to skip TLS certificate validation. Not recommended for production.
            type: bool
            default: true
            env:
                - name: VALIDATE_CERTS
                - name: NUTANIX_VALIDATE_CERTS
        nutanix_debug:
            description:
                - Enable verbose API logging to a log file.
            type: bool
            default: false
            env:
                - name: NUTANIX_DEBUG
        read_timeout:
            description:
                - Read timeout in milliseconds for API calls.
                - Raise this when Prism Central is slow to answer list calls.
            type: int
            default: 30000
    extends_documentation_fragment:
        - nutanix.ncp.ntnx_proxy_v2
    requirements:
        - "ntnx_clustermgmt_py_client (for resource=cluster, cluster_profile or storage_container)"
        - "ntnx_networking_py_client (for resource=subnet, vpc, virtual_switch, floating_ip,
          network_function or routing_policy)"
        - "ntnx_vmm_py_client (for resource=vm, image, image_placement_policy, template or ova)"
        - "ntnx_volumes_py_client (for resource=volume_group or iscsi_client)"
        - "ntnx_prism_py_client (for resource=category)"
        - "ntnx_iam_py_client (for resource=user, user_group, role, operation,
          authorization_policy, directory_service or saml_identity_provider)"
        - "ntnx_microseg_py_client (for resource=service_group, address_group,
          network_security_policy or entity_group)"
        - "ntnx_dataprotection_py_client (for resource=recovery_point)"
        - "ntnx_datapolicies_py_client (for resource=protection_policy or storage_policy)"
        - "ntnx_objects_py_client (for resource=object_store)"
    notes:
        - Names are not guaranteed to be unique in Prism Central. When a name can match more than one
          entity, either set O(fail_on_multiple=false) or provide a more specific O(filter).
        - This lookup runs on the Ansible controller and performs at least one API call per
          search term. When a filter matches more than 100 entities, the results are paginated
          and one additional API call is made per extra page.
        - O(resource=iscsi_client) is the one resource that is not resolved by a name. Its V4 list
          API only accepts C(clusterReference) and C(extId) in a C($filter), so a search term is
          the external ID of a cluster and the lookup returns the external IDs of every iSCSI
          client on it. Set O(fail_on_multiple=false) unless the cluster has a single client.
        - For O(resource=storage_container) the V4 API leaves C(extId) empty and returns the
          identifier in C(containerExtId) instead. The lookup falls back to C(containerExtId) for
          that resource, so the returned value is still the UUID that references the container.
        - This plugin always returns a list, but C(lookup) joins that list into a comma separated
          string. Use C(query), or C(lookup) with C(wantlist=true), whenever more than one external
          ID can come back, that is with several search terms or with O(fail_on_multiple=false).
          C(wantlist) is handled by Ansible itself and is available for every lookup plugin, so it
          is not listed among the options above.
        - With O(fail_on_missing=false) the returned list holds V(None) for terms that matched
          nothing, and Ansible cannot join V(None) into a string. C(lookup) then falls back to
          returning the bare V(None) for a single term, or the raw list for several terms. Use
          C(query) to always get a list.
"""

EXAMPLES = r"""
- name: Resolve a cluster name to its ext_id
  ansible.builtin.set_fact:
    cluster_ext_id: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', 'my-cluster', resource='cluster',
                nutanix_host=pc_ip, nutanix_username=user, nutanix_password=pass,
                validate_certs=false) }}

- name: Use the lookup inline when creating a subnet (credentials from environment)
  nutanix.ncp.ntnx_subnets_v2:
    state: present
    name: vlan-100
    subnet_type: VLAN
    network_id: 100
    cluster_reference: "{{ lookup('nutanix.ncp.ntnx_ext_id', 'my-cluster', resource='cluster') }}"
    virtual_switch_reference: "{{ lookup('nutanix.ncp.ntnx_ext_id', 'vs0', resource='virtual_switch') }}"

- name: Resolve multiple VM names at once with query()
  ansible.builtin.debug:
    msg: "{{ query('nutanix.ncp.ntnx_ext_id', 'vm1', 'vm2', 'vm3', resource='vm') }}"

- name: Resolve a list variable of VM names
  ansible.builtin.set_fact:
    vm_ext_ids: "{{ query('nutanix.ncp.ntnx_ext_id', vm_names, resource='vm') }}"
  vars:
    vm_names:
      - vm1
      - vm2

# lookup() would join these into "uuid1,uuid2,uuid3"; wantlist=true keeps them as a list
# and is equivalent to using query().
- name: Same thing with lookup() and wantlist
  ansible.builtin.debug:
    msg: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', 'vm1', 'vm2', 'vm3',
                resource='vm', wantlist=true) }}

- name: Tolerate missing names and keep a list with a None placeholder per missing term
  ansible.builtin.set_fact:
    vm_ext_ids: >-
      {{ query('nutanix.ncp.ntnx_ext_id', 'vm1', 'does-not-exist',
               resource='vm', fail_on_missing=false) }}

- name: Resolve a subnet using a precise filter
  ansible.builtin.set_fact:
    subnet_ext_id: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', resource='subnet',
                filter="name eq 'vlan-100' and virtualSwitchReference eq '" ~ vs_ext_id ~ "'") }}

- name: Resolve a category by its key (returns all matching ext_ids)
  ansible.builtin.set_fact:
    category_ext_ids: >-
      {{ query('nutanix.ncp.ntnx_ext_id', 'Environment', resource='category',
               fail_on_multiple=false) }}

- name: Resolve a role by its display name (default filter_attribute is displayName)
  ansible.builtin.set_fact:
    role_ext_id: "{{ lookup('nutanix.ncp.ntnx_ext_id', 'Super Admin', resource='role') }}"

# The default filter_attribute for a user is username, so matching on the email
# address instead needs the emailId OData property.
- name: Resolve a user by email instead of the default username
  ansible.builtin.set_fact:
    user_ext_id: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', 'alice@example.com',
                resource='user', filter_attribute='emailId') }}

- name: Raw filter mode with no positional terms (when filter is set, terms are ignored)
  ansible.builtin.set_fact:
    vm_ext_id_from_raw_filter: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', resource='vm',
                filter="name eq 'vm1'") }}

- name: List the iSCSI clients of a cluster (terms are cluster ext_ids, not client names)
  ansible.builtin.set_fact:
    iscsi_client_ext_ids: >-
      {{ query('nutanix.ncp.ntnx_ext_id', cluster_ext_id,
               resource='iscsi_client', fail_on_multiple=false) }}

- name: Resolve a protection policy name to its ext_id
  ansible.builtin.set_fact:
    protection_policy_ext_id: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', 'pp-gold', resource='protection_policy') }}

- name: Reach Prism Central through an HTTPS proxy
  ansible.builtin.set_fact:
    vm_ext_id: >-
      {{ lookup('nutanix.ncp.ntnx_ext_id', 'vm1', resource='vm',
                https_proxy='http://proxy.example.com:3128',
                proxy_username=proxy_user, proxy_password=proxy_pass) }}
"""

RETURN = r"""
_raw:
    description:
        - A flat list of external IDs (UUIDs) matching the search terms or filter, in input order.
          This is what C(query), or C(lookup) with C(wantlist=true), returns. Plain C(lookup) joins
          the list into a comma separated string.
        - When O(fail_on_missing=false) and a search term matches no entity, the entry for that term
          is V(None) rather than a string, so the list can hold a mix of strings and V(None) values.
        - When O(fail_on_multiple=false) and a search term matches several entities, every matching
          external ID is added to the list.
        - Nothing is returned when the lookup fails, an error is raised instead. This happens when
          O(fail_on_missing=true) and a term matches no entity, when O(fail_on_multiple=true) and a
          term matches more than one entity, when O(resource) is not one of the supported values,
          when neither a search term nor O(filter) is given, when O(nutanix_host) is not set, and
          when the underlying V4 list API call raises an exception.
    type: list
    elements: str
"""

import json  # noqa: E402
import tempfile  # noqa: E402

from ansible.errors import AnsibleError  # noqa: E402
from ansible.module_utils._text import to_native  # noqa: E402
from ansible.plugins.lookup import LookupBase  # noqa: E402

from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..plugin_utils.ext_id_resources import PROXY_OPTIONS, RESOURCE_MAP  # noqa: E402

# The V4 list APIs cap ``_limit`` at 100, so bigger result sets are walked page by page.
PAGE_SIZE = 100


class _LookupModuleAdapter:
    """Minimal stand-in for AnsibleModule.

    The shared ``get_*_api_instance`` helpers only ever read ``module.params``
    (via ``.get``) and call ``module.fail_json``, so a lightweight object with
    those two members is enough to reuse them from a lookup plugin.
    """

    def __init__(self, params):
        self.params = params
        self.tmpdir = tempfile.gettempdir()

    def jsonify(self, data):
        return json.dumps(data, default=to_native)

    def fail_json(self, msg, **kwargs):
        error = to_native(msg)
        if kwargs:
            error = "{0}: {1}".format(error, self.jsonify(kwargs))
        raise AnsibleError(error)


class LookupModule(LookupBase):

    @staticmethod
    def _escape(value):
        """Escape a value for use inside an OData single quoted string literal."""
        return to_native(value).replace("'", "''")

    def _build_params(self):
        nutanix_host = self.get_option("nutanix_host")
        if not nutanix_host:
            raise AnsibleError(
                "nutanix_host must be provided either as a lookup argument or via the "
                "NUTANIX_HOSTNAME/NUTANIX_HOST environment variable"
            )
        params = {
            "nutanix_host": nutanix_host,
            "nutanix_port": self.get_option("nutanix_port"),
            "nutanix_username": self.get_option("nutanix_username"),
            "nutanix_password": self.get_option("nutanix_password"),
            "nutanix_api_key": self.get_option("nutanix_api_key"),
            "validate_certs": self.get_option("validate_certs"),
            "nutanix_debug": self.get_option("nutanix_debug"),
            "nutanix_log_file": None,
            "read_timeout": self.get_option("read_timeout"),
        }
        # Proxy options come from the ntnx_proxy_v2 doc fragment. They are passed
        # through as is, so the shared client falls back to the HTTPS_PROXY,
        # HTTP_PROXY, ALL_PROXY, NO_PROXY, PROXY_USERNAME and PROXY_PASSWORD
        # environment variables when an option is unset, exactly as it does for modules.
        for option in PROXY_OPTIONS:
            params[option] = self.get_option(option)
        return params

    @staticmethod
    def _extract_ext_ids(resource, data):
        if resource == "storage_container":
            return [
                item.get("ext_id") or item.get("container_ext_id")
                for item in data
                if item.get("ext_id") or item.get("container_ext_id")
            ]
        return [item.get("ext_id") for item in data if item.get("ext_id")]

    def _list_ext_ids(self, list_method, resource, odata_filter):
        ext_ids = []
        fetched = 0
        current_page = 0

        while True:
            try:
                resp = list_method(
                    _filter=odata_filter, _page=current_page, _limit=PAGE_SIZE
                )
            except Exception as e:
                raise AnsibleError(
                    "API exception raised while listing {0} with filter '{1}': {2}".format(
                        resource, odata_filter, to_native(e)
                    )
                )

            data = strip_internal_attributes(resp.to_dict()).get("data") or []
            if not data:
                break

            ext_ids.extend(self._extract_ext_ids(resource, data))
            fetched += len(data)

            metadata = getattr(resp, "metadata", None)
            total_available = getattr(metadata, "total_available_results", 0) or 0
            if fetched >= total_available:
                break

            current_page += 1

        return ext_ids

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        # Ansible does not flatten lookup arguments, so a list variable passed as a
        # single argument arrives as one nested list instead of several terms.
        terms = self._flatten(terms)

        resource = self.get_option("resource")
        if resource not in RESOURCE_MAP:
            raise AnsibleError(
                "Unsupported resource '{0}'. Supported resources: {1}".format(
                    resource, ", ".join(sorted(RESOURCE_MAP))
                )
            )
        spec = RESOURCE_MAP[resource]

        raw_filter = self.get_option("filter")
        if not terms and not raw_filter:
            raise AnsibleError(
                "At least one search term or a 'filter' must be provided"
            )

        attribute = self.get_option("filter_attribute") or spec["filter_attribute"]
        fail_on_missing = self.get_option("fail_on_missing")
        fail_on_multiple = self.get_option("fail_on_multiple")

        module = _LookupModuleAdapter(self._build_params())
        api_instance = spec["get_api_instance"](module)
        list_method = getattr(api_instance, spec["list_method"])

        if raw_filter:
            searches = [raw_filter]
        else:
            searches = [
                "{0} eq '{1}'".format(attribute, self._escape(term)) for term in terms
            ]

        ret = []
        for odata_filter in searches:
            ext_ids = self._list_ext_ids(list_method, resource, odata_filter)

            if not ext_ids:
                if fail_on_missing:
                    raise AnsibleError(
                        "No {0} found matching filter: {1}".format(
                            resource, odata_filter
                        )
                    )
                ret.append(None)
                continue

            if len(ext_ids) > 1 and fail_on_multiple:
                raise AnsibleError(
                    "Found {0} {1} matching filter '{2}'. Refine the search "
                    "(use a more specific 'filter') or set fail_on_multiple=false.".format(
                        len(ext_ids), resource, odata_filter
                    )
                )

            ret.extend(ext_ids)

        return ret
