#from __future__ import absolute_import, division, print_function

from ..module_utils.fc.api_keys import ApiKeys
from ..module_utils.base_module import BaseModule

from ..module_utils.utils import remove_param_with_none_value


DOCUMENTATION = r"""
---
module: ntnx_foundation_central_api_keys
short_description: Nutanix module which creates api key for foundation central
version_added: 1.1.0
description: 'Create a new api key which will be used by nodes to authenticate with Foundation Central .'
options:
  nutanix_host:
    description:
      - Foundation VM hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 8000
    required: false
  alias:
    description: name which will used to generate key
    type: str
    required: true
    default: None

author:
 - Abhishek Chaudhary (@abhimutant)
"""

EXAMPLES = r"""
  - name: Create API key
    ntnx_foundation_central_api_keys_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      alias: "test"
"""

RETURN = r"""
API_key:
  description: newly created api key
  returned: true
  type: list
  api_key": [
            {
                "alias": "test,
                "api_key": "{{ api_key}}",
                "created_timestamp": "2022-04-18T00:41:45.000-07:00",
                "current_time": "2022-04-18T04:45:35.000-07:00",
                "key_uuid": "{{ uuid }}"
            }
        ],
"""

def get_module_spec():
    module_args = dict(
        alias = dict(type=str)
    )
    return module_args


def create(module, result):
    key = ApiKeys(module)
    spec, error = key.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating api_key Spec", **result)

    resp = key.create(spec)
    result["api_key"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {}
    create(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
