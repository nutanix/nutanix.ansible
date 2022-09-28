#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_era_clones_info
short_description: clone  info module
version_added: 1.7.0
description: 'Get clone info'
options:
      clone_name:
        description:
            - clone name
        type: str
      clone_id:
        description:
            - clone id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List clones
    ntnx_era_clones_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
    register: result

  - name: Get clone using name
    ntnx_clones_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      clone_name: "clone-name"
    register: result

  - name: Get clone using id
    ntnx_clones_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      clone_id: "clone-id"
    register: result

"""
RETURN = r"""
"""

from ..module_utils.era.base_info_module import BaseEraInfoModule  # noqa: E402
from ..module_utils.era.clones import Clone  # noqa: E402


def get_module_spec():

    module_args = dict(
        clone_name=dict(type="str"),
        clone_id=dict(type="str"),
    )

    return module_args


def get_clone(module, result):
    clone = Clone(module, resource_type="/v0.8/clones")
    if module.params.get("clone_name"):
        clone_name = module.params["clone_name"]
        clone_option = "{0}/{1}".format("name", clone_name)
    else:
        clone_option = "{0}".format(module.params["clone_id"])

    resp = clone.read(clone_option)

    result["response"] = resp


def get_clones(module, result):
    clone = Clone(module)

    resp = clone.read()

    result["response"] = resp


def run_module():
    module = BaseEraInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[("clone_name", "clone_id")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("clone_name") or module.params.get("clone_id"):
        get_clone(module, result)
    else:
        get_clones(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
