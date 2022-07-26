#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_groups_info
short_description: User Groups info module
version_added: 1.4.0
description: 'Get User Groups info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: user_group
    usergroup_uuid:
        description:
            - user group UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List user groups using name filter criteria
    ntnx_user_groups_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        group_name: "{{ name }}"
    register: result

  - name: List user groups using length, offset, sort order and sort attribute
    ntnx_user_groups_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 2
      offset: 1
      sort_order: "DESCENDING"
      sort_attribute: "group_name"
    register: result

  - name: test getting particular user group using uuid
    ntnx_user_groups_info:
        nutanix_host: "{{ ip }}"
        nutanix_username: "{{ username }}"
        nutanix_password: "{{ password }}"
        validate_certs: False
        usergroup_uuid: '{{ uuid  }}'
    register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for user groups list output
  returned: always
  type: dict
  sample: {
                "filter": "group_name=={{name}}",
                "kind": "user",
                "length": 2,
                "offset": 0,
                "total_matches": 2
            }
entities:
  description: user groups intent response
  returned: always
  type: list
  sample: [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "kind": "user_group",
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec": {
                        "resources": {
                            "directory_service_user_group": {
                                "distinguished_name": "CN=test_custom_{_group_},CN=Users,DC=ad,DC=ds,DC=io"
                            }
                        }
                    },
                    "status": {
                        "execution_context": {
                            "task_uuid": [
                               "00000000-0000-0000-0000-000000000000"
                            ]
                        },
                        "resources": {
                            "access_control_policy_reference_list": [],
                            "directory_service_user_group": {
                                "directory_service_reference": {
                                    "kind": "directory_service",
                                    "name": "ds",
                                    "uuid": "00000000-0000-0000-0000-000000000000"
                                },
                                "distinguished_name": "cn=test_custom_{_group_},cn=users,dc=ad,dc=ds,dc=io"
                            },
                            "display_name": "test_custom_{_group_}",
                            "projects_reference_list": [],
                            "user_group_type": "DIRECTORY_SERVICE"
                        },
                        "state": "COMPLETE"
                    }
                },
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "kind": "user_group",
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 1,
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec": {
                        "resources": {
                            "directory_service_user_group": {
                                "distinguished_name": "<distinguished-name>"
                            }
                        }
                    },
                    "status": {
                        "execution_context": {
                            "task_uuid": [
                               "00000000-0000-0000-0000-000000000000"
                            ]
                        },
                        "resources": {
                            "access_control_policy_reference_list": [],
                            "directory_service_user_group": {
                                "directory_service_reference": {
                                    "kind": "directory_service",
                                    "name": "qanucalm",
                                    "uuid": "00000000-0000-0000-0000-000000000000"
                                },
                                "distinguished_name": "<distinugished-name>"
                            },
                            "display_name": "name1",
                            "projects_reference_list": [],
                            "user_group_type": "DIRECTORY_SERVICE"
                        },
                        "state": "PENDING"
                    }
                }
            ]
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.user_groups import UserGroups  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        usergroup_uuid=dict(type="str"),
        kind=dict(type="str", default="user_group"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_user(module, result):
    user = UserGroups(module)
    uuid = module.params.get("usergroup_uuid")
    resp = user.read(uuid)
    result["response"] = resp


def get_users(module, result):
    user = UserGroups(module)
    spec, err = user.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating user info Spec", **result)
    resp = user.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("usergroup_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("usergroup_uuid"):
        get_user(module, result)
    else:
        get_users(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
