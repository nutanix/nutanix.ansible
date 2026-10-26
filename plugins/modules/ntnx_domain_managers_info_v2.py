#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_domain_managers_info_v2
short_description: Fetch Domain Manager (Prism Central) related info using PC v4 APIs
version_added: 2.7.0
description:
    - Multi-purpose info module that fetches Domain Manager (Prism Central)
      related information using the PC v4 APIs.
    - Four distinct read operations are exposed through a single module and
      selected by the C(method) parameter.
    - "C(domain_managers): List or get domain manager (Prism Central)
      configuration details — SDK method
      C(DomainManagerApi.list_domain_managers) /
      C(DomainManagerApi.get_domain_manager_by_id). This is the default and
      runs against the PC itself."
    - "C(backup_targets): List or get backup targets for a given Prism
      Central — SDK method
      C(DomainManagerBackupsApi.list_backup_targets) /
      C(DomainManagerBackupsApi.get_backup_target_by_id). This also runs
      against the PC itself."
    - "C(restorable_domain_managers): List the domain managers backed up
      at a given restore source — SDK method
      C(DomainManagerBackupsApi.list_restorable_domain_managers). This
      runs against the Prism Element (hosting cluster) that holds the
      restore source."
    - "C(restore_points): List or get restore points for a given
      restorable domain manager — SDK method
      C(DomainManagerBackupsApi.list_restore_points) /
      C(DomainManagerBackupsApi.get_restore_point_by_id). This also runs
      against the Prism Element that holds the restore source."
    - If C(ext_id) is provided (for operations that support it), a single
      entity is returned. Otherwise a list of entities is returned, with
      optional C(filter), C(limit), C(page), C(orderby) and C(select)
      pagination controls as supported by the underlying API.
    - This module uses PC v4 APIs based SDKs.
notes:
    - The C(domain_managers) and C(backup_targets) methods must be pointed
      at the Prism Central endpoint.
    - The C(restorable_domain_managers) and C(restore_points) methods must
      be pointed at the Prism Element (hosting cluster) endpoint — the host
      that keeps the restore source for the backed up PC. These two methods
      require C(nutanix_username) / C(nutanix_password) (API key auth is
      not supported for PE).
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(List domain managers / Get domain manager by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin,
      Domain Manager Viewer, Internal Super Admin, NCM Connector,
      Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List backup targets / Get backup target by ext_id) -
      Required Roles: Domain Manager Admin, Domain Manager Viewer,
      Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List restorable domain managers) -
      Required Roles: Domain Manager Admin, Domain Manager Viewer,
      Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List restore points / Get restore point by ext_id) -
      Required Roles: Domain Manager Admin, Domain Manager Viewer,
      Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    method:
        description:
            - Selects which Domain Manager info API to invoke.
            - C(domain_managers) targets C(ListDomainManagers) /
              C(GetDomainManagerById).
            - C(backup_targets) targets C(ListBackupTargets).
            - C(restorable_domain_managers) targets
              C(ListRestorableDomainManagers).
            - C(restore_points) targets C(ListRestorePoints).
        type: str
        required: false
        default: domain_managers
        choices:
            - domain_managers
            - backup_targets
            - restorable_domain_managers
            - restore_points
    ext_id:
        description:
            - External ID of the entity to fetch when C(method) is
              C(domain_managers), C(backup_targets) or C(restore_points).
            - When omitted, the list variant of the selected API is called.
            - Not applicable to C(method=restorable_domain_managers), which
              only supports listing.
        type: str
        required: false
    domain_manager_ext_id:
        description:
            - External ID of the domain manager (Prism Central) that owns the
              requested backup target.
            - Required when C(method) is C(backup_targets).
        type: str
        required: false
    restore_source_ext_id:
        description:
            - External ID of the restore source. Obtained from the
              C(ntnx_pc_restore_source_v2) module.
            - Required when C(method) is C(restorable_domain_managers) or
              C(restore_points).
        type: str
        required: false
    restorable_domain_manager_ext_id:
        description:
            - External ID of the restorable domain manager returned by
              C(ListRestorableDomainManagers).
            - Required when C(method) is C(restore_points).
        type: str
        required: false
    nutanix_host:
        description:
            - The Nutanix endpoint to talk to.
            - When C(method) is C(domain_managers) or C(backup_targets),
              provide the Prism Central IP / FQDN.
            - When C(method) is C(restorable_domain_managers) or
              C(restore_points), provide the Prism Element (hosting cluster)
              IP / FQDN that keeps the restore source.
        type: str
        required: true
    nutanix_username:
        description:
            - The username to authenticate with the Nutanix endpoint.
            - Required because the restore source / restore point APIs run
              against a Prism Element and do not support API-key auth.
        type: str
        required: true
    nutanix_password:
        description:
            - The password to authenticate with the Nutanix endpoint.
            - Required because the restore source / restore point APIs run
              against a Prism Element and do not support API-key auth.
        type: str
        required: true
    nutanix_api_key:
        description:
            - Not supported for the restore source / restore point methods,
              which run against a Prism Element.
            - Only effective when calling the C(domain_managers) or
              C(backup_targets) methods against a Prism Central.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all Prism Centrals (domain managers) known to this PC
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: domain_managers
  register: all_pcs

- name: Get a specific Prism Central by ext_id
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: domain_managers
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: single_pc

- name: List all backup targets for a given Prism Central
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: backup_targets
    domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: backup_targets

- name: Get a specific backup target by ext_id
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: backup_targets
    domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    ext_id: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"
  register: one_backup_target

- name: List all restorable domain managers backed up at a restore source (run against PE)
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ pe_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: restorable_domain_managers
    restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
  register: restorable_pcs

- name: List all restore points for a given restorable domain manager (run against PE)
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ pe_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: restore_points
    restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
    restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: restore_points

- name: Fetch all domain managers across all pages
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    method: domain_managers
    fetch_all: true
  register: all_pcs_paged
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix domain manager info v4 API.
        - The host may be Prism Central (for C(domain_managers) and
          C(backup_targets)) or the hosting Prism Element (for
          C(restorable_domain_managers) and C(restore_points)).
        - A single entity dict is returned when an C(ext_id) is provided.
        - A list of entity dicts is returned when C(ext_id) is not provided
          (optionally filtered / paginated).
    type: dict
    returned: always
    sample:
        {
            "config": {
                "bootstrap_config": null,
                "build_info": {
                    "version": "pc.2024.3"
                },
                "credentials": null,
                "name": "PC_10.44.76.25",
                "resource_config": {
                    "container_ext_ids": [
                        "6171a26e-7d08-4f10-b6fa-9304b333f6b6"
                    ],
                    "data_disk_size_bytes": 536870912000,
                    "memory_size_bytes": 37580963840,
                    "num_vcpus": 10
                },
                "should_enable_lockdown_mode": null,
                "size": "SMALL"
            },
            "ext_id": "cfddac63-ffdb-4d9c-9a8c-54abf89ce234",
            "hosting_cluster_ext_id": "00062cd6-e034-fd28-185b-ac1f6b6f97e2",
            "is_registered_with_hosting_cluster": true,
            "links": null,
            "network": {
                "external_address": {
                    "ipv4": {
                        "prefix_length": null,
                        "value": "10.44.76.25"
                    },
                    "ipv6": null
                },
                "fqdn": null,
                "name_servers": [
                    {
                        "fqdn": null,
                        "ipv4": {
                            "prefix_length": null,
                            "value": "10.40.64.15"
                        },
                        "ipv6": null
                    }
                ],
                "ntp_servers": [
                    {
                        "fqdn": {
                            "value": "0.example.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    }
                ]
            },
            "node_ext_ids": [
                "e5cc110f-3a4a-4a88-8c89-71aa101adb03"
            ],
            "should_enable_high_availability": false,
            "tenant_id": null
        }

ext_id:
    description: External ID of the fetched entity (only populated for
        C(ext_id) based get operations).
    type: str
    returned: when a single entity is fetched
    sample: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"

changed:
    description: Always C(false) — this is an info module.
    returned: always
    type: bool
    sample: false

msg:
    description: Status / error message surfaced by the module.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching domain managers info"

error:
    description: Error details when the module fails.
    returned: when an error occurs
    type: str

failed:
    description: Whether the module execution failed.
    returned: when something fails
    type: bool
    sample: false

total_available_results:
    description:
        - Total number of entities available on the server for the selected
          list operation (only populated when a list variant is called).
    type: int
    returned: when a list variant is called
    sample: 1
"""

import warnings  # noqa: E402

from ansible.module_utils.basic import env_fallback  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import (  # noqa: E402
    get_backup_target,
    get_pc_config,
    get_restore_point,
)
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


METHOD_DOMAIN_MANAGERS = "domain_managers"
METHOD_BACKUP_TARGETS = "backup_targets"
METHOD_RESTORABLE_DOMAIN_MANAGERS = "restorable_domain_managers"
METHOD_RESTORE_POINTS = "restore_points"


def get_module_spec():
    module_args = dict(
        nutanix_username=dict(
            type="str", fallback=(env_fallback, ["NUTANIX_USERNAME"]), required=True
        ),
        nutanix_password=dict(
            type="str",
            no_log=True,
            fallback=(env_fallback, ["NUTANIX_PASSWORD"]),
            required=True,
        ),
        method=dict(
            type="str",
            required=False,
            default=METHOD_DOMAIN_MANAGERS,
            choices=[
                METHOD_DOMAIN_MANAGERS,
                METHOD_BACKUP_TARGETS,
                METHOD_RESTORABLE_DOMAIN_MANAGERS,
                METHOD_RESTORE_POINTS,
            ],
        ),
        ext_id=dict(type="str", required=False),
        domain_manager_ext_id=dict(type="str", required=False),
        restore_source_ext_id=dict(type="str", required=False),
        restorable_domain_manager_ext_id=dict(type="str", required=False),
    )
    return module_args


def _require(module, params):
    """Fail the module when any of the required parameters is missing.

    Args:
        module: AnsibleModule instance.
        params: Iterable of parameter names that must be set.
    """
    missing = [p for p in params if not module.params.get(p)]
    if missing:
        module.fail_json(
            msg="Missing required parameter(s) for method '{0}': {1}".format(
                module.params.get("method"), ", ".join(missing)
            )
        )


def get_single_domain_manager(module, api_instance, result):
    """Fetch a single domain manager (PC) by external ID."""
    ext_id = module.params.get("ext_id")
    resp = get_pc_config(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_domain_managers(module, api_instance, result):
    """List all domain managers visible from this endpoint."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating domain managers info spec", **result)

    try:
        resp = list_entities(api_instance.list_domain_managers, kwargs=kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching domain managers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_single_backup_target(module, api_instance, result):
    """Fetch a single backup target by external ID."""
    ext_id = module.params.get("ext_id")
    resp = get_backup_target(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_backup_targets(module, api_instance, result):
    """List backup targets configured on a given domain manager (PC)."""
    _require(module, ["domain_manager_ext_id"])
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating backup targets info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_backup_targets,
            kwargs=kwargs,
            domainManagerExtId=domain_manager_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching backup targets info",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
    if total_available_results is not None:
        result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_restorable_domain_managers(module, api_instance, result):
    """List the domain managers (PCs) backed up at a given restore source."""
    _require(module, ["restore_source_ext_id"])
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating restorable domain managers info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_restorable_domain_managers,
            kwargs=kwargs,
            restoreSourceExtId=restore_source_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restorable domain managers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_single_restore_point(module, api_instance, result):
    """Fetch a single restore point by external ID."""
    _require(
        module,
        ["restore_source_ext_id", "restorable_domain_manager_ext_id"],
    )
    ext_id = module.params.get("ext_id")
    resp = get_restore_point(
        module,
        api_instance,
        ext_id,
        module.params.get("restore_source_ext_id"),
        module.params.get("restorable_domain_manager_ext_id"),
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_restore_points(module, api_instance, result):
    """List restore points for a given restorable domain manager."""
    _require(
        module,
        ["restore_source_ext_id", "restorable_domain_manager_ext_id"],
    )
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating restore points info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_restore_points,
            kwargs=kwargs,
            restoreSourceExtId=restore_source_ext_id,
            restorableDomainManagerExtId=restorable_domain_manager_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restore points info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def dispatch(module, result):
    """Pick the correct SDK call for the requested C(method)."""
    method = module.params.get("method")
    ext_id = module.params.get("ext_id")

    if method == METHOD_DOMAIN_MANAGERS:
        api_instance = get_domain_manager_api_instance(module)
        if ext_id:
            get_single_domain_manager(module, api_instance, result)
        else:
            get_domain_managers(module, api_instance, result)
        return

    if method == METHOD_BACKUP_TARGETS:
        api_instance = get_domain_manager_backup_api_instance(module)
        if ext_id:
            _require(module, ["domain_manager_ext_id"])
            get_single_backup_target(module, api_instance, result)
        else:
            get_backup_targets(module, api_instance, result)
        return

    if method == METHOD_RESTORABLE_DOMAIN_MANAGERS:
        api_instance = get_domain_manager_backup_api_instance(module)
        get_restorable_domain_managers(module, api_instance, result)
        return

    if method == METHOD_RESTORE_POINTS:
        api_instance = get_domain_manager_backup_api_instance(module)
        if ext_id:
            get_single_restore_point(module, api_instance, result)
        else:
            get_restore_points(module, api_instance, result)
        return

    module.fail_json(msg="Unsupported method: {0}".format(method))


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    dispatch(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
