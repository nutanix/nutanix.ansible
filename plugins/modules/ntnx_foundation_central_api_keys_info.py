#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_api_keys_info
short_description: Nutanix module which returns the api key
version_added: 1.1.0
description: 'List all the api keys created in Foundation Central.'
options:
  key_uuid:
    description:
      - Return the API Key given it's uuid
    type: str
    required: false
  alias:
    description: Return the API Key given it's alias
    type: str
  custom_filter:
    description: Return the API Key given it's alias
    type: dict
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Abhishek Chaudhary (@abhimutant)
"""

EXAMPLES = r"""
- name: Get API key with alias filter
  ntnx_foundation_central_api_keys_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    alias: "test"

- name: Get API key with key_uuid filter
  ntnx_foundation_central_api_keys_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    key_uuid: "{{ uuid of key }}"

- name: List all the API key within FC
  ntnx_foundation_central_api_keys_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""

RETURN = r"""
API_key:
  description: returned API with alias as a filter
  returned: if correct alias is given
  type: list
  sample: [
            {
                "alias": "test",
                "api_key": "{{ api_key}}",
                "created_timestamp": "2022-04-18T00:41:45.000-07:00",
                "current_time": "2022-04-18T04:45:35.000-07:00",
                "key_uuid": "{{ uuid }}"
            },
        ]
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.fc.api_keys import ApiKey  # noqa: E402


def get_module_spec():
    module_args = dict(
        key_uuid=dict(type="str", no_log=True),
        alias=dict(type="str"),
        custom_filter=dict(type="dict"),
    )
    return module_args


def list_api_keys(module, result):
    key_uuid = module.params.get("key_uuid")
    alias = module.params.get("alias")
    api_keys = ApiKey(module)
    if key_uuid:
        result["response"] = api_keys.read(key_uuid)
    else:
        spec, error = api_keys.get_spec()
        if error:
            result["error"] = error
            module.fail_json(msg="Failed generating API keys Spec", **result)

        if module.check_mode:
            result["response"] = spec
            return

        resp = api_keys.list(spec)
        if alias:
            result["response"] = [x for x in resp["api_keys"] if x["alias"] == alias]
        else:
            result["response"] = resp

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    list_api_keys(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
