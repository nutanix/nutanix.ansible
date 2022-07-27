#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_roles_info
short_description: role info module
version_added: 1.4.0
description: 'Get roles info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: role
    role_uuid:
        description:
            - role UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: List all roles
  ntnx_roles_info:
    nutanix_host: <host_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: List role using uuid criteria
  ntnx_roles_info:
    nutanix_host: <host_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    role_uuid: "{{ test_role_uuid }}"
  register: result

- name: List roles using filter criteria
  ntnx_roles_info:
    nutanix_host: <host_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    filter:
      name: "{{ test_role_name }}"
"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description:
    - Metadata for role list output
    - Below struct is only obtained when we use filters or list roles using length, etc.
  returned: always
  type: dict
  sample:  {
                "kind": "role",
                "length": 1,
                "offset": 0,
                "total_matches": 14
            }
entities:
  description:
    - entities intent response
    - Below struct is only obtained when we use filters or list roles using length, etc.
  returned: always
  type: list
  sample: [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-07-26T08:25:00Z",
                        "entity_version": "",
                        "kind": "role",
                        "last_update_time": "2022-07-26T08:25:01Z",
                        "owner_reference": {
                            "kind": "user",
                            "name": "admin",
                            "uuid": "00000000-0000-0000-0000-000000000000"
                        },
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "ansnjs74-d825-4cfd-879c-ec7a86a82cfd"
                    },
                    "spec": {
                        "description": "check123-updated",
                        "name": "test-ansible-1-updated-1-2-3",
                        "resources": {
                            "permission_reference_list": [
                                {
                                    "kind": "permission",
                                    "uuid": "nsjd51de-26f1-4caf-760d-df81c3ca8a88"
                                },
                                {
                                    "kind": "permission",
                                    "uuid": "sheusjdf-2253-44a9-7ddd-e10c53a4ad04"
                                }
                            ]
                        }
                    },
                    "status": {
                        "description": "check123-updated",
                        "execution_context": {
                            "task_uuid": [
                                "29s6heyd-3e01-42e3-9276-d75571273f89"
                            ]
                        },
                        "is_system_defined": false,
                        "name": "test-ansible-1-updated-1-2-3",
                        "resources": {
                            "permission_reference_list": [
                                {
                                    "kind": "permission",
                                    "name": "perm1",
                                    "uuid": "nsjd51de-26f1-4caf-760d-df81c3ca8a88"
                                },
                                {
                                    "kind": "permission",
                                    "name": "perm2",
                                    "uuid": "sheusjdf-2253-44a9-7ddd-e10c53a4ad04"
                                }
                            ]
                        },
                        "state": "COMPLETE"
                    }
                }
        ]
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.roles import Roles  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        role_uuid=dict(type="str"),
        kind=dict(type="str", default="role"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_role(module, result):
    roles = Roles(module)
    uuid = module.params.get("role_uuid")
    resp = roles.read(uuid)
    result["response"] = resp


def get_roles(module, result):
    roles = Roles(module)
    spec, err = roles.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Roles info Spec", **result)
    resp = roles.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("role_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("role_uuid"):
        get_role(module, result)
    else:
        get_roles(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
