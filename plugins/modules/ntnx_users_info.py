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
        name: "{{ name }}"
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
                "filter": "name=={{name}}",
                "kind": "user",
                "length": 2,
                "offset": 0,
                "total_matches": 2
            }
entities:
  description: users intent response
  returned: always
  type: list
  sample: [
    #TODO
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
    user = Users(module)
    uuid = module.params.get("user_uuid")
    resp = user.read(uuid)
    result["response"] = resp


def get_users(module, result):
    user = Users(module)
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
