#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_registries_info
short_description: registry  info module
version_added: 1.6.0
description: 'Get registry info'
options:
      registry_name:
        description:
            - registry name
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List registries
  ntnx_karbon_registries_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Get registries using name
  ntnx_registries_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    registry_name: "registry-name"
  register: result
"""
RETURN = r"""
name:
    description: K8s registry name.
    returned: always
    type: str
    sample: "test-module21"
status:
    description: K8s registry status.
    returned: always
    type: str
    sample: "kActive"
uuid:
    description: The universally unique identifier (UUID) of the k8s registry.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
endpoint:
    description: "Endpoint of the private registry in format url:port. Example: prod-user-registry:5000"
    returned: always
    type: str
    sample: "xxx.xxx.xxx.xxx:5000"
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.karbon.registries import Registry  # noqa: E402


def get_module_spec():

    module_args = dict(
        registry_name=dict(type="str"),
    )

    return module_args


def get_registry(module, result):
    registry = Registry(module)
    registry_name = module.params.get("registry_name")

    resp = registry.read(registry_name)

    result["response"] = resp


def get_registries(module, result):
    registry = Registry(module)

    # If there is no registries,
    # response will be empty list causing error in entity class
    # so do status code checks here incase of other failures.
    # During failures response is of type dict else its list
    resp = registry.read(raise_error=False)
    if isinstance(resp, dict) and resp.get("code") >= 300:
        result["error"] = resp.get("message")
        result["changed"] = False
        result["response"] = None
        module.fail_json(msg="Failed getting registries info", **result)

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("registry_name"):
        get_registry(module, result)
    else:
        get_registries(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
