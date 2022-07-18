#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_groups_info
short_description: user groups info module
version_added: 1.4.0
description: 'Get user groups info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: user_group
    user_group_uuid:
        description:
            - user group UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List user_groups using user_group uuid criteria
  ntnx_user_groups_info:
    user_group_uuid: "{{ test_user_group_uuid }}"
  register: result
  ignore_errors: True

- name: List all user groups
  ntnx_user_groups_info:
  register: user_groups

- name: List user_groups using filter criteria
  ntnx_user_groups_info:
    filter:
      group_name: "{{ test_user_group_name }}"
  register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: 
    - Metadata for user group list output
    - Below response struct is for user groups info using filters
  returned: Only when listed using filter
  type: dict
  sample: {
                "filter": "user_group==xx@xx.com",
                "kind": "user_group",
                "length": 1,
                "offset": 0,
                "total_matches": 1
            }
entities:
  description: 
    - user groups intent response
    - Below response struct is for user groups info using filters
  returned: Only when all user groups are listed or using filter
  type: list
  sample: [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "kind": "user_group",
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "f7f476ca-e971-42d3-b56b-578b729d6673"
                    },
                    "spec": {},
                    "status": {
                        "resources": {
                            "access_control_policy_reference_list": [],
                            "directory_service_user_group": {
                                "directory_service_reference": {
                                    "kind": "directory_service",
                                    "name": "xx",
                                    "uuid": "ca6c1ed6-33cb-441d-92fe-64cb0229751f"
                                },
                                "distinguished_name": "xx,xx,xx,xx"
                            },
                            "display_name": "xxx",
                            "projects_reference_list": [
                                {
                                    "kind": "project",
                                    "name": "test-project",
                                    "uuid": "s675ede4-0b59-43b4-8e94-bb001d4acad8"
                                }
                            ],
                            "user_group_type": "DIRECTORY_SERVICE"
                        },
                        "state": "COMPLETE"
                    }
                }
            ]
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.user_groups import UserGroups  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        user_group_uuid=dict(type="str"),
        kind=dict(type="str", default="user_group"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_user_group(module, result):
    user_groups = UserGroups(module)
    uuid = module.params.get("user_group_uuid")
    resp = user_groups.read(uuid)
    result["response"] = resp


def get_user_groups(module, result):
    user_groups = UserGroups(module)
    spec, err = user_groups.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating User group info Spec", **result)
    resp = user_groups.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("user_group_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("user_group_uuid"):
        get_user_group(module, result)
    else:
        get_user_groups(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
