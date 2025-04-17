#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_backup_target_info_v2
short_description: Get PC backup targets info
version_added: 2.1.0
description:
    - Fetch specific backup target info using external ID
    - Fetch list of multiple backup targets info if external ID is not provided with optional filters
options:
    ext_id:
        description: External ID to fetch specific backup target info
        type: str
    domain_manager_ext_id:
        description:
            - Domain manager means the PC
            - External ID of the domain manager (PC)
            - Domain manager external ID can be fetched using this module ntnx_pc_config_info_v2
            - Using ntnx_clusters_info_v2, you can list all clusters and get the one with clusterFunctionType as 'PRISM_CENTRAL'
        type: str
        required: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all backup targets
  nutanix.ncp.ntnx_pc_backup_target_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    domain_manager_ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
  register: backup_result

- name: Get backup target info
  nutanix.ncp.ntnx_pc_backup_target_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    domain_manager_ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
    ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: backup_result
"""

RETURN = r"""
response:
    description:
        - Response for fetching backup targets info
        - Backup target info if external ID is provided
        - List of multiple backup targets info if external ID is not provided
    type: dict
    returned: always
    sample:
        {
            "backup_pause_reason": null,
            "ext_id": "00062c47-ac15-ee40-185b-ac1f6b6f97e2",
            "is_backup_paused": false,
            "last_sync_time": null,
            "links": null,
            "location": {
                "config": {
                    "ext_id": "00062c47-ac15-ee40-185b-ac1f6b6f97e2",
                    "name": "auto_cluster_prod_e98628bb1f50"
                }
            },
            "tenant_id": null
        }

ext_id:
    description: External ID of the backup target
    returned: always
    type: str
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_backup_target  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        domain_manager_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_backup_target_with_ext_id(module, domain_manager_backups_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_backup_target(module, domain_manager_backups_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_backup_targets(module, domain_manager_backups_api, result):
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating backup targets info Spec", **result)
    try:
        resp = domain_manager_backups_api.list_backup_targets(
            domainManagerExtId=domain_manager_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching backup targets info",
        )

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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    domain_manager_backups_api = get_domain_manager_backup_api_instance(module)
    if module.params.get("ext_id"):
        get_backup_target_with_ext_id(module, domain_manager_backups_api, result)
    else:
        get_backup_targets(module, domain_manager_backups_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
