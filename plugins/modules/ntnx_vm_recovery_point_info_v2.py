#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_point_info_v2
short_description: Get VM recovery point info
version_added: 2.0.0
description:
    - Fetch specific VM recovery point info which is part of top level recovery point
options:
    recovery_point_ext_id:
        description:
            - Top level Recovery point external ID
        type: str
        required: true
    vm_recovery_point_ext_id:
        description:
            - VM recovery point external ID
        type: str
        required: true
extends_documentation_fragment:
        - nutanix.ncp.ntnx_credentials
        - nutanix.ncp.ntnx_info_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
    - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: Fetch specific VM recovery point info which is part of top level recovery point
  ntnx_vm_recovery_point_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
  register: result
"""
RETURN = r"""
response:
    description:
        - Response for fetching VM recovery point info
    returned: always
    type: dict
    sample:
        {
            "application_consistent_properties": null,
            "consistency_group_ext_id": null,
            "disk_recovery_points": [
                {
                    "disk_ext_id": "839feff9-bac0-4a70-9523-82ea9e431517",
                    "disk_recovery_point_ext_id": "21d467f0-ccef-4733-91cc-f04db58a92eb"
                },
                {
                    "disk_ext_id": null,
                    "disk_recovery_point_ext_id": "91aedb3c-39c9-4750-b553-6e8360d7c1ff"
                }
            ],
            "ext_id": "b387359d-fa5c-4d58-9eb2-3af1a4976319",
            "links": null,
            "location_agnostic_id": "51264897-07a8-4292-831b-ae28a37135e5",
            "tenant_id": null,
            "vm_categories": null,
            "vm_ext_id": "2e572ceb-d955-4ed7-956f-1c90acf5b5ad"
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: always
    sample: null

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_vm_recovery_point,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        recovery_point_ext_id=dict(type="str", required=True),
        vm_recovery_point_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_vm_recovery_point_using_vm_rp_ext_id(module, recovery_points, result):
    recovery_point_ext_id = module.params.get("recovery_point_ext_id")
    vm_recovery_point_ext_id = module.params.get("vm_recovery_point_ext_id")
    resp = get_vm_recovery_point(
        module, recovery_points, recovery_point_ext_id, vm_recovery_point_ext_id
    )
    result["ext_id"] = vm_recovery_point_ext_id
    result["recovery_point_ext_id"] = recovery_point_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    recovery_points = get_recovery_point_api_instance(module)
    get_vm_recovery_point_using_vm_rp_ext_id(module, recovery_points, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
