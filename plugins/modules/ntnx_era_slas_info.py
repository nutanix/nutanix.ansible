#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_era_slas_info
short_description: sla  info module
version_added: 1.7.0
description: 'Get sla info'
options:
      sla_name:
        description:
            - sla name
        type: str
      sla_id:
        description:
            - sla id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List slas
    ntnx_era_slas_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
    register: result

  - name: Get slas using name
    ntnx_era_slas_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      sla_name: "sla-name"
    register: result

  - name: Get slas using id
    ntnx_era_slas_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      sla_id: "sla-id"
    register: result

"""
RETURN = r"""
"""

from ..module_utils.era.base_info_module import BaseEraInfoModule  # noqa: E402
from ..module_utils.era.slas import SLA  # noqa: E402


def get_module_spec():

    module_args = dict(
        sla_name=dict(type="str"),
        sla_id=dict(type="str"),
    )

    return module_args


def get_sla(module, result):
    sla = SLA(module)
    if module.params.get("sla_name"):
        sla_name = module.params["sla_name"]
        sla_option = "{0}/{1}".format("name", sla_name)
    else:
        sla_option = "{0}".format(module.params["sla_id"])

    resp = sla.read(sla_option)

    result["response"] = resp


def get_slas(module, result):
    sla = SLA(module)

    resp = sla.read()

    result["response"] = resp


def run_module():
    module = BaseEraInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
        mutually_exclusive=[("sla_name", "sla_id")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("sla_name") or module.params.get("sla_id"):
        get_sla(module, result)
    else:
        get_slas(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
