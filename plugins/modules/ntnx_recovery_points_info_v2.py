#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_points_info_v2
short_description: Get recovery points info
version_added: 2.0.0
description:
    - Fetch specific recovery point info using external ID
    - Fetch list of multiple recovery points info if external ID is not provided with optional filters
options:
    ext_id:
        description:
            - External ID to fetch specific recovery point info
        type: str
extends_documentation_fragment:
        - nutanix.ncp.ntnx_credentials
        - nutanix.ncp.ntnx_info_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
    - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: Fetch recovery point using external id
  ntnx_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
  register: result

- name: List all recovery points
  ntnx_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
  register: result

- name: Fetch details for a Recovery Point using Filters
  ntnx_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    filter: extId eq '840c6c3f-2b01-47d5-81fb-b285e45e89ba'
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for fetching recovery points info
        - One recovery point info if External ID is provided
        - List of multiple recovery points info if External ID is not provided
    returned: always
    type: dict
    sample:
        {
            "creation_time": "2024-08-22T03:23:36.701254+00:00",
            "expiration_time": "2092-09-09T06:37:42+00:00",
            "ext_id": "840c6c3f-2b01-47d5-81fb-b285e45e89ba",
            "links": null,
            "location_agnostic_id": "e5e1a71b-4911-480d-a4d4-3a175797c401",
            "location_references": [
                {
                    "location_ext_id": "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
                }
            ],
            "name": "test_abhi_RP_8:53:16 am, Aug 22",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "recovery_point_type": "CRASH_CONSISTENT",
            "status": "COMPLETE",
            "tenant_id": null,
            "vm_recovery_points": [
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
            ],
            "volume_group_recovery_points": null
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs
    sample: null

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the recovery point
    type: str
    returned: when external ID of top level recovery point is provided
    sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import get_recovery_point  # noqa: E402
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
    )

    return module_args


def get_recovery_point_using_ext_id(module, recovery_points, result):
    ext_id = module.params.get("ext_id")
    resp = get_recovery_point(module, recovery_points, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_recovery_points(module, recovery_points, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating recovery points info Spec", **result)

    try:
        resp = recovery_points.list_recovery_points(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery points info",
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
    result = {"changed": False, "error": None, "response": None}
    recovery_points = get_recovery_point_api_instance(module)
    if module.params.get("ext_id"):
        get_recovery_point_using_ext_id(module, recovery_points, result)
    else:
        get_recovery_points(module, recovery_points, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
