#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_users_info
short_description: users info module
version_added: 1.4.0
description: 'Get users info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: user
    user_uuid:
        description:
            - user UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List users using name filter criteria
    ntnx_users_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        username: "{{ name }}"
    register: result

  - name: List users using length, offset, sort order and sort attribute
    ntnx_users_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 2
      offset: 1
      sort_order: "DESCENDING"
      sort_attribute: "username"
    register: result

  - name: test getting particular user using uuid
    ntnx_users_info:
        nutanix_host: "{{ ip }}"
        nutanix_username: "{{ username }}"
        nutanix_password: "{{ password }}"
        validate_certs: False
        user_uuid: '{{ uuid  }}'
    register: result
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for users list output
  returned: always
  type: dict
  sample: {
                "filter": "username=={{name}}",
                "kind": "user",
                "length": 1,
                "offset": 0,
                "total_matches": 1
            }
entities:
  description: users intent response
  returned: always
  type: list
  sample:  [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "kind": "user",
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "000000-0000-0000-0000-0000000"
                    },
                    "spec": {
                        "resources": {
                            "directory_service_user": {
                                "directory_service_reference": {
                                    "kind": "directory_service",
                                    "uuid": "000000-0000-0000-0000-0000000"
                                },
                                "user_principal_name": "user1@xx.com"
                            }
                        }
                    },
                    "status": {
                        "name": "user1@xx.com",
                        "resources": {
                            "access_control_policy_reference_list": [
                                {
                                    "kind": "access_control_policy",
                                    "name": "nuCalmAcp-db48cbac-eac8-c384-84f6-3c8376d70db6",
                                    "uuid": "000000-0000-0000-0000-0000000"
                                }
                            ],
                            "directory_service_user": {
                                "default_user_principal_name": "user1@xx.com",
                                "directory_service_reference": {
                                    "kind": "directory_service",
                                    "name": "ds",
                                    "uuid": "000000-0000-0000-0000-0000000"
                                },
                                "user_principal_name": "user1@xx.com"
                            },
                            "display_name": null,
                            "projects_reference_list": [
                                {
                                    "kind": "project",
                                    "name": "p1",
                                    "uuid": "000000-0000-0000-0000-0000000"
                                },
                                {
                                    "kind": "project",
                                    "name": "p2",
                                    "uuid": "000000-0000-0000-0000-0000000"
                                }
                            ],
                            "resource_usage_summary": {
                                "resource_domain": {
                                    "resources": []
                                }
                            },
                            "user_type": "DIRECTORY_SERVICE"
                        },
                        "state": "COMPLETE"
                    }
                }
            ]
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.users import Users  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        user_uuid=dict(type="str"),
        kind=dict(type="str", default="user"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_user(module, result):
    users = Users(module)
    uuid = module.params.get("user_uuid")
    resp = users.read(uuid)
    result["response"] = resp


def get_users(module, result):
    users = Users(module)
    spec, err = users.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating User info Spec", **result)
    resp = users.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("user_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("user_uuid"):
        get_user(module, result)
    else:
        get_users(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
