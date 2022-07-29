#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_permissions_info
short_description: permissions info module
version_added: 1.4.0
description: 'Get permissions info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: permission
    permission_uuid:
        description:
            - permission UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: List all permissions
  ntnx_permissions_info:
    nutanix_host: <host_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: List permission using uuid criteria
  ntnx_permissions_info:
    permission_uuid: "{{ test_permission_uuid }}"
    nutanix_host: <host_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: List permissions using filter criteria
  ntnx_permissions_info:
    nutanix_host: <host_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    filter:
      name: "{{ test_permission_name }}"
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
    - Metadata for permission list output
    - Below struct is only obtained when we use filters or list permissions using length, etc.
  returned: always
  type: dict
  sample:   {
                "kind": "permission",
                "length": 20,
                "offset": 0,
                "total_matches": 1
            }
entities:
  description:
    - permission intent response
    - Below struct is only obtained when we use filters or list permissions using length, etc.
  returned: always
  type: list
  sample: [
                {
                    "metadata": {
                        "categories": {},
                        "categories_mapping": {},
                        "creation_time": "2022-07-05T18:28:26Z",
                        "kind": "permission",
                        "last_update_time": "2022-07-05T18:28:26Z",
                        "spec_hash": "00000000000000000000000000000000000000000000000000",
                        "spec_version": 0,
                        "uuid": "asdas3a77f4-73d4-4875-a8b9-3d2c068b8042"
                    },
                    "spec": {
                        "description": "Allows to xyz",
                        "name": "permission_xyz",
                        "resources": {
                            "fields": {
                                "field_mode": "DISALLOWED",
                                "field_name_list": []
                            },
                            "kind": "<kind>",
                            "operation": "update"
                        }
                    },
                    "status": {
                        "description": "Allows to xyz",
                        "name": "permission_xyz",
                        "resources": {
                            "fields": {
                                "field_mode": "DISALLOWED",
                                "field_name_list": []
                            },
                            "kind": "<kind>",
                            "operation": "update"
                        },
                        "state": "COMPLETE"
                    }
                }
            ]
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.permissions import Permission  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        permission_uuid=dict(type="str"),
        kind=dict(type="str", default="permission"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_permission(module, result):
    permissions = Permission(module)
    uuid = module.params.get("permission_uuid")
    resp = permissions.read(uuid)
    result["response"] = resp


def get_permissions(module, result):
    permissions = Permission(module)
    spec, err = permissions.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Permissions info Spec", **result)
    resp = permissions.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("permission_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("permission_uuid"):
        get_permission(module, result)
    else:
        get_permissions(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
