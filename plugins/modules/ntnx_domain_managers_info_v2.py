#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_domain_managers_info_v2
short_description: Fetch domain manager (Prism Central) and related info
version_added: 2.7.0
description:
    - Fetch domain manager (Prism Central) and related info using the Prism v4 APIs.
    - This single info module dispatches to one of four list operations depending
      on the parameters supplied -
      1. If I(ext_id) is provided alone, the specific domain manager (Prism Central)
      is fetched by external identifier.
      2. If none of the id-scoping parameters are supplied, all domain managers
      (Prism Central) are listed.
      3. If I(domain_manager_ext_id) is supplied, backup targets configured
      for that domain manager are listed.
      4. If I(restore_source_ext_id) is supplied, restorable domain managers for
      that restore source are listed.
      5. If both I(restore_source_ext_id) and I(restorable_domain_manager_ext_id)
      are supplied, restore points for that restorable domain manager are listed.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get / List domain manager (Prism Central) configuration) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin, Domain Manager Viewer,
      Internal Super Admin, NCM Connector, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List backup targets / restorable domain managers / restore points) -
      Required Roles: Domain Manager Admin, Domain Manager Viewer, Prism Admin, Prism Viewer, Super Admin
    - The target host for this module is the domain manager (Prism Central), i.e.
      pass the PC endpoint in C(nutanix_host). The restorable-domain-manager and
      restore-point list APIs are also exposed on Prism Element (FCVM) for
      recovery scenarios, but this module uses the Prism Central endpoint.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    ext_id:
        description:
            - External identifier of the domain manager (Prism Central).
            - When supplied, the module fetches a single domain manager by its ext_id.
            - Mutually exclusive with I(filter) and the scope parameters
              (I(domain_manager_ext_id), I(restore_source_ext_id),
              I(restorable_domain_manager_ext_id)).
        type: str
    domain_manager_ext_id:
        description:
            - External identifier of the domain manager (Prism Central) whose
              backup targets should be listed.
        type: str
    restore_source_ext_id:
        description:
            - External identifier of the restore source whose restorable domain
              managers (or restore points, when combined with
              I(restorable_domain_manager_ext_id)) should be listed.
        type: str
    restorable_domain_manager_ext_id:
        description:
            - External identifier of the restorable domain manager whose restore
              points should be listed.
            - Must be used together with I(restore_source_ext_id).
        type: str
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
- name: List all domain managers (Prism Central) on the cluster
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: all_domain_managers

- name: Fetch a specific domain manager (Prism Central) by ext_id
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: one_domain_manager

- name: List all backup targets configured on a domain manager (Prism Central)
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: all_backup_targets

- name: List all restorable domain managers for a given restore source
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
  register: all_restorable_domain_managers

- name: List all restore points for a given restore source and restorable domain manager
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
    restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
  register: all_restore_points

- name: List restore points with a filter and limit
  nutanix.ncp.ntnx_domain_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
    restorable_domain_manager_ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    filter: "extId eq '8545bc57-7719-3273-a837-5aeb5f2c64b5'"
    limit: 1
  register: filtered_restore_points
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix domain manager info v4 API.
        - The host targeted by this module is the domain manager (Prism Central);
          the restorable-domain-manager / restore-point APIs are also exposed on
          Prism Element (FCVM) but this module uses the Prism Central endpoint.
        - It can be a single domain manager if I(ext_id) is provided.
        - List of multiple domain managers if I(ext_id) is not provided with optional filter or limit.
        - List of backup targets when I(domain_manager_ext_id) is provided.
        - List of restorable domain managers when I(restore_source_ext_id) is provided.
        - List of restore points when both I(restore_source_ext_id) and
          I(restorable_domain_manager_ext_id) are provided.
    returned: always
    type: dict
    sample:
        {
            "config": {
                "bootstrap_config": {
                    "cloud_init_config": null,
                    "environment_info": {
                        "provider_type": "NTNX",
                        "provisioning_type": "NTNX",
                        "type": "ONPREM"
                    }
                },
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
                }
            },
            "node_ext_ids": [
                "e5cc110f-3a4a-4a88-8c89-71aa101adb03"
            ],
            "should_enable_high_availability": false,
            "tenant_id": null
        }

changed:
    description: Always False for info modules.
    returned: always
    type: bool
    sample: false

ext_id:
    description: External identifier of the fetched domain manager (Prism Central).
    returned: when I(ext_id) is provided
    type: str
    sample: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"

total_available_results:
    description:
        - Total number of entities available on the backend for the dispatched list operation.
    returned: when the module lists entities (no I(ext_id))
    type: int
    sample: 1

msg:
    description: Status / error message surfaced to the user.
    returned: When applicable
    type: str
    sample: "Api Exception raised while fetching domain managers info"

error:
    description: Error details when the task fails.
    returned: when an error occurs
    type: str
    sample: null

failed:
    description: Indicates whether the task failed.
    returned: when the task fails
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
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


def get_module_spec():
    """
    Return the Ansible argument spec for the domain managers info module.

    The spec enumerates the id-scoping parameters used to dispatch between the
    four backing SDK list operations (``ListDomainManagers``,
    ``ListBackupTargets``, ``ListRestorableDomainManagers``, ``ListRestorePoints``)
    plus the single ``ext_id`` used for the ``GetDomainManagerById`` fast path.
    """
    module_args = dict(
        ext_id=dict(type="str"),
        domain_manager_ext_id=dict(type="str"),
        restore_source_ext_id=dict(type="str"),
        restorable_domain_manager_ext_id=dict(type="str"),
    )
    return module_args


def _generate_info_kwargs(module, result, context):
    """
    Build the OData kwargs dict used for a list_* SDK call.

    Args:
        module: Ansible module instance.
        result: Running result dict (populated with the generated error, if any).
        context: Short human-readable context string used in the fail message.

    Returns:
        The kwargs dict ready to be forwarded to the SDK list operation, or
        ``None`` if spec generation failed (``module.fail_json`` is called
        inside this helper on failure).
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating {0} info Spec".format(context), **result
        )
    return kwargs


def get_domain_manager_with_ext_id(module, api_instance, result):
    """
    Fetch a single domain manager (Prism Central) by its external identifier.
    """
    ext_id = module.params.get("ext_id")
    resp = get_pc_config(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_domain_managers(module, api_instance, result):
    """
    List all domain managers (Prism Central) configured on the cluster.
    """
    kwargs = _generate_info_kwargs(module, result, "domain managers")
    try:
        resp = list_entities(
            api_instance.list_domain_managers,
            kwargs=kwargs,
        )
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


def get_backup_targets(module, backups_api, result):
    """
    List backup targets configured for a given domain manager (Prism Central).
    """
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    kwargs = _generate_info_kwargs(module, result, "backup targets")
    try:
        resp = list_entities(
            backups_api.list_backup_targets,
            kwargs=kwargs,
            domainManagerExtId=domain_manager_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching backup targets info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_restorable_domain_managers(module, backups_api, result):
    """
    List restorable domain managers backed up at the given restore source.
    """
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    kwargs = _generate_info_kwargs(module, result, "restorable domain managers")
    try:
        resp = list_entities(
            backups_api.list_restorable_domain_managers,
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


def get_restore_points(module, backups_api, result):
    """
    List restore points for a given restore source and restorable domain manager.
    """
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    kwargs = _generate_info_kwargs(module, result, "restore points")
    try:
        resp = list_entities(
            backups_api.list_restore_points,
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


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "domain_manager_ext_id"),
            ("ext_id", "restore_source_ext_id"),
            ("ext_id", "restorable_domain_manager_ext_id"),
            ("domain_manager_ext_id", "restore_source_ext_id"),
            ("domain_manager_ext_id", "restorable_domain_manager_ext_id"),
        ],
        required_by={
            "restorable_domain_manager_ext_id": "restore_source_ext_id",
        },
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}

    restore_source_ext_id = module.params.get("restore_source_ext_id")
    restorable_domain_manager_ext_id = module.params.get(
        "restorable_domain_manager_ext_id"
    )
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")

    if restorable_domain_manager_ext_id and restore_source_ext_id:
        backups_api = get_domain_manager_backup_api_instance(module)
        get_restore_points(module, backups_api, result)
    elif restore_source_ext_id:
        backups_api = get_domain_manager_backup_api_instance(module)
        get_restorable_domain_managers(module, backups_api, result)
    elif domain_manager_ext_id:
        backups_api = get_domain_manager_backup_api_instance(module)
        get_backup_targets(module, backups_api, result)
    elif module.params.get("ext_id"):
        api_instance = get_domain_manager_api_instance(module)
        get_domain_manager_with_ext_id(module, api_instance, result)
    else:
        api_instance = get_domain_manager_api_instance(module)
        get_domain_managers(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
