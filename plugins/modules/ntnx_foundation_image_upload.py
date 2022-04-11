#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.foundation.base_module import FoundationBaseModule
from ..module_utils.foundation.image_upload import Image
from ..module_utils.utils import remove_param_with_none_value

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_image_upload
short_description: Nutanix module which uploads hypervisor or AOS image to foundation vm.
version_added: 1.1.0
description: Uploads hypervisor or AOS image to foundation vm.
options:
  nutanix_host:
    description:
      - Foundation VM hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - Foundation VM port
    type: str
    default: 8000
    required: false
  source:
    description:
      - local full path of installer file where the ansible playbook runs
      - mandatory incase of upload i.e. state=present
    type: str
    required: false
    description:
  file_name:
    description:
      - Name of installer file that will be uploaded to foundation vm
    type: str
    required: true
  installer_type:
    description:
      - One of "kvm", "esx", "hyperv", "xen", or "nos"
    type: str
    choices: [kvm, esx, hyperv, xen, nos]
    required: true
author:
 - Prem Karat (@premkarat)
"""

EXAMPLES = r"""

"""

RETURN = r"""

"""


def get_module_spec():
    module_args = dict(
        filename=dict(type="str", required=True),
        installer_type=dict(
            type="str", required=True, choices=["kvm", "esx", "hyperv", "xen", "nos"]
        ),
        source=dict(type="str", required=False),
    )

    return module_args


def upload_image(module, result):
    image = Image(module)
    fname = module.params["filename"]
    itype = module.params["installer_type"]
    source = module.params["source"]
    timeout = module.params["timeout"]
    resp = image.upload_image(fname, itype, source, timeout=timeout)
    result["changed"] = True
    result["response"] = resp


def delete_image(module, result):
    image = Image(module, delete_image=True)
    fname = module.params["filename"]
    itype = module.params["installer_type"]
    resp = image.delete_image(fname, itype)

    result["changed"] = True
    result["response"] = resp


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_if=[
            ("state", "present", ("source",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    state = module.params["state"]
    if state == "present":
        upload_image(module, result)
    elif state == "absent":
        delete_image(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
