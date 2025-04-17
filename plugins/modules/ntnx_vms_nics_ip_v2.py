#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_nics_ip_v2
short_description: Assign/Release IP to/from Nutanix VM NICs.
description:
    - This module allows you to assign or release IP from Nutanix VM NICs.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
    - Pradeepsingh Bhati (@bhati-pradeep)
notes:
    - Module will will skip releasing IP from NIC, if no IP is assigned to NIC.
    - Module will skip if the install/uninstall is not required as per above check.
options:
    state:
        description:
            - Specify state
            - If C(state) is set to present then module will assign IP to NIC.
            - if C(state) is set to absent then module will release IP from.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The external ID of the NIC.
        type: str
        required: true
    vm_ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    ip_address:
        description:
            - The IP address for the NIC to be assigned.
        type: dict
        suboptions:
            value:
                description:
                    - The IP address value.
                type: str
                required: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Assign IP
  nutanix.ncp.ntnx_vms_nics_ip_v2:
      nutanix_host: "<pc-ip>"
      nutanix_username: "<username>"
      nutanix_password: "<password>"
      validate_certs: false
      ext_id: 7147b563-7b80-4be5-96b5-d8ff63187a5c
      vm_ext_id: "521ab899-2398-4a23-62cb-8cd5e46ee5d2"
      ip_address:
          value: "10.51.144.137"
  register: result

- name: Release IP
  nutanix.ncp.ntnx_vms_nics_ip_v2:
      nutanix_host: "<pc-ip>"
      nutanix_username: "<username>"
      nutanix_password: "<password>"
      validate_certs: false
      state: absent
      ext_id: 7147b563-7b80-4be5-96b5-d8ff63187a5c
      vm_ext_id: "521ab899-2398-4a23-62cb-8cd5e46ee5d2"
      register: result
"""

RETURNS = r"""
response:
    description:
        - For C(wait)=false, it will return task details
        - Else it will return NIC info
    type: dict
    returned: always
    sample: {
            "backing_info": {
                "is_connected": true,
                "mac_address": "50:6b:8d:f9:de:e7",
                "model": null,
                "num_queues": 1
            },
            "ext_id": "7147b563-7b80-4be5-96b5-d8ff63187a5c",
            "links": null,
            "network_info": {
                "ipv4_config": {
                    "ip_address": {
                        "prefix_length": 32,
                        "value": "10.51.144.137"
                    },
                    "secondary_ip_address_list": null,
                    "should_assign_ip": null
                },
                "ipv4_info": null,
                "network_function_chain": null,
                "network_function_nic_type": null,
                "nic_type": "NORMAL_NIC",
                "should_allow_unknown_macs": null,
                "subnet": {
                    "ext_id": "18f0ed6e-30c8-48be-9c8f-e7cb4153416a"
                },
                "trunked_vlans": null,
                "vlan_mode": "ACCESS"
            },
            "tenant_id": null
        }
task_ext_id:
    description: The external ID of the task associated with the operation.
    type: str
changed:
    description: Indicates whether the module changed the state of the VM NIC.
    type: bool
error:
    description: The error message, if any, encountered.
    type: str
ext_id:
    description:
        - NIC external ID
    type: str
vm_ext_id:
    description: VM external ID
    type: str
skipped:
    description: Indicates whether the operation was skipped due to no state changes (Idempotency).
    type: bool
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_nic  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ip_address = dict(
        value=dict(type="str", required=True),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        vm_ext_id=dict(type="str", required=True),
        ip_address=dict(
            type="dict", options=ip_address, obj=vmm_sdk.IPv4Address, required=False
        ),
    )
    return module_args


def assign_ip(module, result):
    vms = get_vm_api_instance(module)
    nic_ext_id = module.params.get("ext_id")
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = nic_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AssignIpParams()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating assign IP to VM Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of nic current state
    vm = get_nic(module, api_instance=vms, ext_id=nic_ext_id, vm_ext_id=vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.assign_ip_by_id(
            vmExtId=vm_ext_id, extId=nic_ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while assign IP to VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        nic = get_nic(module, api_instance=vms, ext_id=nic_ext_id, vm_ext_id=vm_ext_id)
        result["response"] = strip_internal_attributes(nic.to_dict())
    result["changed"] = True


def release_ip(module, result):
    vms = get_vm_api_instance(module)
    nic_ext_id = module.params.get("ext_id")
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = nic_ext_id

    if module.check_mode:
        result["response"] = "Release IP address from NIC with external ID: {}".format(
            nic_ext_id
        )
        return

    # get etag of nic current state
    nic = get_nic(module, api_instance=vms, ext_id=nic_ext_id, vm_ext_id=vm_ext_id)

    # check if IP is not assigned then no need for releasing it
    ip_info = nic.network_info
    if hasattr(ip_info, "ipv4_config") and getattr(ip_info, "ipv4_config") is None:
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. NIC doesn't have IP assigned", **result
        )

    etag = get_etag(nic)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.release_ip_by_id(vmExtId=vm_ext_id, extId=nic_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while releasing IP from VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        nic = get_nic(module, api_instance=vms, ext_id=nic_ext_id, vm_ext_id=vm_ext_id)
        result["response"] = strip_internal_attributes(nic.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("ip_address",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "vm_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        assign_ip(module, result)
    else:
        release_ip(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
