#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_image_placement_policies_info
short_description: image placement policies info module
version_added: 1.0.0
description: 'Get image placement policy info'
options:
    kind:
      description:
        - The kind name
      type: str
      default: image_placement_policy
    policy_uud:
        description:
            - policy UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
  - name: List image placement policies using name filter criteria
    ntnx_image_placement_policies_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        - name: test_policy
    register: result

  - name: List image placement policies using length, offset
    ntnx_image_placement_policies_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 2
      offset: 1
    register: result
"""
RETURN = r"""
"""


from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.image_placement_policy import ImagePlacementPolicy  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        policy_uuid=dict(type="str"),
        kind=dict(type="str", default="image_placement_policy"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_policy(module, result):
    policy_obj = ImagePlacementPolicy(module)
    uuid = module.params.get("policy_uuid")
    resp = policy_obj.read(uuid)
    result["response"] = resp


def get_particular_policies(module, result):
    policy_obj = ImagePlacementPolicy(module)
    spec, err = policy_obj.get_info_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Image Placement Policies info Spec", **result)
    resp = policy_obj.list(spec)
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
        mutually_exclusive=[
            ("policy_uuid", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("policy_uuid"):
        get_policy(module, result)
    else:
        get_particular_policies(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
