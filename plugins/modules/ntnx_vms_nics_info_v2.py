#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_nics_info_v2
short_description: Fetch information about Nutanix VM's NICs
description:
  - This module fetches information about Nutanix VM's NICs.
  - The module can fetch information about all NICs or a specific NICs.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
    ext_id:
        description:
        - The external ID of the nic.
        type: str
        required: false
    vm_ext_id:
        description:
        - The external ID of the vm.
        type: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Fetch information about all nics of a vm
  nutanix.ncp.ntnx_vms_nics_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec16e

- name: Fetch information about a specific nic
  nutanix.ncp.ntnx_vms_nics_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec16e
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VMM Nics v4 API.
    - it can be single nic or list of nics as per spec.
  type: dict
  returned: always
  sample: {
            "backing_info": {
                "is_connected": true,
                "mac_address": "50:6b:8d:a2:37:00",
                "model": null,
                "num_queues": 1
            },
            "ext_id": "4a67ce54-dd9c-4c71-9d91-2a19d512dc7d",
            "links": null,
            "network_info": {
                "ipv4_config": null,
                "ipv4_info": null,
                "network_function_chain": null,
                "network_function_nic_type": null,
                "nic_type": "NORMAL_NIC",
                "should_allow_unknown_macs": null,
                "subnet": {
                    "ext_id": "34c596ab-37fe-4739-a961-5e5cad79bb99"
                },
                "trunked_vlans": null,
                "vlan_mode": "ACCESS"
            },
            "tenant_id": null
        }
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
vm_ext_id:
    description: The external ID of the vm.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
ext_id:
    description:
        - The external ID of the nic when specific nic is fetched.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
total_available_results:
    description:
        - The total number of available NICs when all NICs are fetched.
    type: int
    returned: when all nics are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_nic(module, result):
    vms = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")

    try:
        resp = vms.get_nic_by_id(vmExtId=vm_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm nic info",
        )

    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_nics(module, result):
    vms = get_vm_api_instance(module)
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm nics info Spec", **result)

    try:
        resp = vms.list_nics_by_vm_id(vmExtId=vm_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm nics info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_nic(module, result)
    else:
        get_nics(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
