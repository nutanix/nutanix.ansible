#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_nics_v2
short_description: Manage NICs of Nutanix VMs
description:
    - This module allows you to create, update, and delete NICs of Nutanix VMs.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    state:
        description:
            - Specify state
            - If C(state) is set to present then module will create NIC.
            - If C(state) is set to present and nic ext_id is given then module will update given NIC.
            - if C(state) is set to absent then module will delete NIC of that VM.
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
        required: false
    vm_ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    backing_info:
        description:
            - The backing information for the NIC.
            - Deprecated, use C(nic_backing_info) instead.
        type: dict
        suboptions:
            model:
                description:
                    - The model of the NIC.
                type: str
                choices:
                    - VIRTIO
                    - E1000
                required: false
            mac_address:
                description:
                    - The MAC address of the NIC.
                type: str
                required: false
            is_connected:
                description:
                    - Whether the NIC needs to be connected or not.
                type: bool
                required: false
            num_queues:
                description:
                    - The number of queues for the NIC.
                type: int
                required: false
    nic_backing_info:
        description:
            - Backing Information about how NIC is associated with a VM.
        type: dict
        suboptions:
            virtual_ethernet_nic:
                description:
                    - The virtual ethernet NIC information.
                type: dict
                suboptions:
                    model:
                        description:
                            - The model of the NIC.
                        type: str
                        choices:
                            - VIRTIO
                            - E1000
                        required: false
                    mac_address:
                        description:
                            - The MAC address of the NIC.
                        type: str
                        required: false
                    is_connected:
                        description:
                            - Whether the NIC needs to be connected or not.
                        type: bool
                        required: false
                    num_queues:
                        description:
                            - The number of queues for the NIC.
                        type: int
                        required: false
    network_info:
        description:
            - The network configuration for the NIC.
            - Deprecated, use C(nic_network_info) instead.
        type: dict
        suboptions:
            nic_type:
                description:
                    - The type of the NIC.
                type: str
                choices:
                    - NORMAL_NIC
                    - DIRECT_NIC
                    - NETWORK_FUNCTION_NIC
                    - SPAN_DESTINATION_NIC
                required: false
            network_function_chain:
                description:
                    - The network function chain for the NIC.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - The external ID of the network function chain.
                        type: str
                        required: true
                required: false
            network_function_nic_type:
                description:
                    - The type of the network function NIC.
                type: str
                choices:
                    - INGRESS
                    - EGRESS
                    - TAP
                required: false
            subnet:
                description:
                    - The subnet for the NIC.
                type: dict
                suboptions:
                    ext_id:
                        description:
                            - The external ID of the subnet.
                        type: str
                        required: true
                required: false
            vlan_mode:
                description:
                    - The VLAN mode for the NIC.
                type: str
                choices:
                    - ACCESS
                    - TRUNK
                required: false
            trunked_vlans:
                description:
                    - The trunked VLANs for the NIC.
                type: list
                elements: int
                required: false
            should_allow_unknown_macs:
                description:
                    - Whether to allow unknown MAC addresses or not.
                type: bool
                required: false
            ipv4_config:
                description:
                    - The IPv4 configuration for the NIC.
                type: dict
                suboptions:
                    should_assign_ip:
                        description:
                            - Whether to assign an IP address or not.
                        type: bool
                        required: false
                    ip_address:
                        description:
                            - The IP address for the NIC.
                        type: dict
                        suboptions:
                            value:
                                description:
                                    - The IP address value.
                                type: str
                                required: True
                            prefix_length:
                                description:
                                    - The prefix length for the IP address.
                                    - Can be skipped, default it will be 32.
                                type: int
                                required: false
                    secondary_ip_address_list:
                        description:
                            - The list of secondary IP addresses for the NIC.
                        type: list
                        elements: dict
                        suboptions:
                            value:
                                description:
                                    - The IP address value.
                                type: str
                                required: true
                            prefix_length:
                                description:
                                    - The prefix length for the IP address.
                                    - Can be skipped, default it will be 32.
                                type: int
                                required: false
                required: false
    nic_network_info:
        description:
            - Network configuration for the NIC.
        type: dict
        suboptions:
            virtual_ethernet_nic_network_info:
                description:
                    - The network configuration for the virtual ethernet NIC.
                type: dict
                suboptions:
                    nic_type:
                        description:
                            - The type of the NIC.
                        type: str
                        choices:
                            - NORMAL_NIC
                            - DIRECT_NIC
                            - NETWORK_FUNCTION_NIC
                            - SPAN_DESTINATION_NIC
                        required: false
                    network_function_chain:
                        description:
                            - The network function chain for the NIC.
                        type: dict
                        suboptions:
                            ext_id:
                                description:
                                    - The external ID of the network function chain.
                                type: str
                                required: true
                        required: false
                    network_function_nic_type:
                        description:
                            - The type of the network function NIC.
                        type: str
                        choices:
                            - INGRESS
                            - EGRESS
                            - TAP
                        required: false
                    subnet:
                        description:
                            - The subnet for the NIC.
                        type: dict
                        suboptions:
                            ext_id:
                                description:
                                    - The external ID of the subnet.
                                type: str
                                required: true
                        required: false
                    vlan_mode:
                        description:
                            - The VLAN mode for the NIC.
                        type: str
                        choices:
                            - ACCESS
                            - TRUNK
                        required: false
                    trunked_vlans:
                        description:
                            - The trunked VLANs for the NIC.
                        type: list
                        elements: int
                        required: false
                    should_allow_unknown_macs:
                        description:
                            - Whether to allow unknown MAC addresses or not.
                        type: bool
                        required: false
                    ipv4_config:
                        description:
                            - The IPv4 configuration for the NIC.
                        type: dict
                        suboptions:
                            should_assign_ip:
                                description:
                                    - Whether to assign an IP address or not.
                                type: bool
                                required: false
                            ip_address:
                                description:
                                    - The IP address for the NIC.
                                type: dict
                                suboptions:
                                    value:
                                        description:
                                            - The IP address value.
                                        type: str
                                        required: True
                                    prefix_length:
                                        description:
                                            - The prefix length for the IP address.
                                            - Can be skipped, default it will be 32.
                                        type: int
                                        required: false
                            secondary_ip_address_list:
                                description:
                                    - The list of secondary IP addresses for the NIC.
                                type: list
                                elements: dict
                                suboptions:
                                    value:
                                        description:
                                            - The IP address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - The prefix length for the IP address.
                                            - Can be skipped, default it will be 32.
                                        type: int
                                        required: false
                        required: false
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger_v2
"""

EXAMPLES = r"""
- name: Create nic with assigning IP as true
  nutanix.ncp.ntnx_vms_nics_v2:
      nutanix_host: "<pc-ip>"
      nutanix_username: "<username>"
      nutanix_password: "<password>"
      validate_certs: false
      vm_ext_id: "97634446-ac09-41c8-8298-71608c6d5ac9"
      backing_info:
          is_connected: true
      network_info:
          nic_type: "NORMAL_NIC"
          subnet:
              ext_id: "18f0ed6e-30c8-48be-9c8f-e7cb4153416a"
          vlan_mode: "ACCESS"
          ipv4_config:
              should_assign_ip: true
  register: result

- name: Create nic with assigning private IP
  nutanix.ncp.ntnx_vms_nics_v2:
      nutanix_host: "<pc-ip>"
      nutanix_username: "<username>"
      nutanix_password: "<password>"
      validate_certs: false
      vm_ext_id: "97634446-ac09-41c8-8298-71608c6d5ac9"
      backing_info:
          is_connected: true
      network_info:
          nic_type: "NORMAL_NIC"
          subnet:
              ext_id: "18f0ed6e-30c8-48be-9c8f-e7cb4153416a"
          vlan_mode: "ACCESS"
          ipv4_config:
              should_assign_ip: true
              ip_address:
                  value: "10.44.44.44"
  register: result

- name: Update VLAN nic type
  nutanix.ncp.ntnx_vms_nics_v2:
      nutanix_host: "<pc-ip>"
      nutanix_username: "<username>"
      nutanix_password: "<password>"
      validate_certs: false
      vm_ext_id: "97634446-ac09-41c8-8298-71608c6d5ac9"
      ext_id: "40a5ac91-83f6-5d35-8ae0-d8f013779377"
      network_info:
          nic_type: "DIRECT_NIC"
  register: result

- name: Delete NIC
  nutanix.ncp.ntnx_vms_nics_v2:
      nutanix_host: "<pc-ip>"
      nutanix_username: "<username>"
      nutanix_password: "<password>"
      validate_certs: false
      state: "absent"
      vm_ext_id: "97634446-ac09-41c8-8298-71608c6d5ac9"
      ext_id: "40a5ac91-83f6-5d35-8ae0-d8f013779377"
  register: result
"""

RETURNS = r"""
response:
    description:
        - Currently for create operation it will return the task details.
        - For update it will return the final state of VM NIC if wait is set to true. Else it will return task details.
        - For delete it will return the task details.
    type: dict
    returned: always
    sample: {
            "cluster_ext_ids": [
                "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-04-23T09:10:10.037257+00:00",
            "completion_details": null,
            "created_time": "2024-04-23T09:10:06.890679+00:00",
            "entities_affected": [
                {
                    "ext_id": "97634446-ac09-41c8-8298-71608c6d5ac9",
                    "rel": "vmm:ahv:vm"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:40a5ac91-83f6-5d35-8ae0-d8f013779377",
            "is_cancelable": false,
            "last_updated_time": "2024-04-23T09:10:10.037257+00:00",
            "legacy_error_message": null,
            "operation": "CreateNic",
            "operation_description": null,
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-04-23T09:10:06.901247+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:9b097142-fc32-5675-8ebb-e35206c1080f",
                    "href": "https://10.44.76.42:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:9b097142-fc32-5675-8ebb-e35206c1080f",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
task_ext_id:
    description: The external ID of the task associated with the operation.
    type: str
changed:
    description: Indicates whether the module changed the state of the VM.
    type: bool
error:
    description: The error message, if any, encountered.
    type: str
ext_id:
    description:
        - NIC external ID
        - Only returned when NIC is updated.
        - Due to known issue, external ID wont be present during create operation.
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
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    wait_for_completion,
    wait_for_entity_ext_id_in_task,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_nic, get_vm  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
        vm_ext_id=dict(type="str", required=True),
    )
    module_args.update(vm_specs.get_nic_spec())
    return module_args


def create_nic(module, result):
    vms = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.AhvConfigNic()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vm nic Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of vm current state
    vm = get_vm(module, vms, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.create_nic(vmExtId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating vm nic",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id, err = wait_for_entity_ext_id_in_task(
            module, task_ext_id, rel=TASK_CONSTANTS.RelEntityType.VM_NIC
        )
        if err:
            result["error"] = err
            module.fail_json(msg="Failed to get NIC external ID from task", **result)
        if ext_id:
            resp = get_nic(module, api_instance=vms, ext_id=ext_id, vm_ext_id=vm_ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def update_new_fields_in_spec(update_spec, params):
    """
    Update the spec according to the parameters provided in the module.
    This is a workaround to ensure that the new fields are included in the update spec.
    """
    if hasattr(update_spec, "backing_info") and hasattr(
        update_spec, "nic_backing_info"
    ):
        if params.get("nic_backing_info"):
            update_spec.backing_info.model = update_spec.nic_backing_info.model
            update_spec.backing_info.is_connected = (
                update_spec.nic_backing_info.is_connected
            )
            update_spec.backing_info.mac_address = (
                update_spec.nic_backing_info.mac_address
            )
            update_spec.backing_info.num_queues = (
                update_spec.nic_backing_info.num_queues
            )

        elif params.get("backing_info"):
            update_spec.nic_backing_info.model = update_spec.backing_info.model
            update_spec.nic_backing_info.is_connected = (
                update_spec.backing_info.is_connected
            )
            update_spec.nic_backing_info.mac_address = (
                update_spec.backing_info.mac_address
            )
            update_spec.nic_backing_info.num_queues = (
                update_spec.backing_info.num_queues
            )

    if hasattr(update_spec, "network_info") and hasattr(
        update_spec, "nic_network_info"
    ):
        if params.get("nic_network_info"):
            update_spec.network_info.nic_type = update_spec.nic_network_info.nic_type
            update_spec.network_info.network_function_chain = (
                update_spec.nic_network_info.network_function_chain
            )
            update_spec.network_info.network_function_nic_type = (
                update_spec.nic_network_info.network_function_nic_type
            )
            update_spec.network_info.subnet = update_spec.nic_network_info.subnet
            update_spec.network_info.vlan_mode = update_spec.nic_network_info.vlan_mode
            update_spec.network_info.trunked_vlans = (
                update_spec.nic_network_info.trunked_vlans
            )
            update_spec.network_info.should_allow_unknown_macs = (
                update_spec.nic_network_info.should_allow_unknown_macs
            )
            update_spec.network_info.ipv4_config = (
                update_spec.nic_network_info.ipv4_config
            )

        elif params.get("network_info"):
            update_spec.nic_network_info.nic_type = update_spec.network_info.nic_type
            update_spec.nic_network_info.network_function_chain = (
                update_spec.network_info.network_function_chain
            )
            update_spec.nic_network_info.network_function_nic_type = (
                update_spec.network_info.network_function_nic_type
            )
            update_spec.nic_network_info.subnet = update_spec.network_info.subnet
            update_spec.nic_network_info.vlan_mode = update_spec.network_info.vlan_mode
            update_spec.nic_network_info.trunked_vlans = (
                update_spec.network_info.trunked_vlans
            )
            update_spec.nic_network_info.should_allow_unknown_macs = (
                update_spec.network_info.should_allow_unknown_macs
            )
            update_spec.nic_network_info.ipv4_config = (
                update_spec.network_info.ipv4_config
            )


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_nic(module, result):
    vms = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    current_spec = get_nic(module, api_instance=vms, ext_id=ext_id, vm_ext_id=vm_ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    update_new_fields_in_spec(update_spec, module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm nic update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = vms.update_nic_by_id(vmExtId=vm_ext_id, extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating vm nic",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    # poll for the last unfinished task
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_nic(module, api_instance=vms, ext_id=ext_id, vm_ext_id=vm_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_nic(module, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "NIC with ext_id:{0} will be deleted.".format(ext_id)
        return

    vms = get_vm_api_instance(module)
    nic = get_nic(module, api_instance=vms, ext_id=ext_id, vm_ext_id=vm_ext_id)
    etag = get_etag(nic)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vms.delete_nic_by_id(vmExtId=vm_ext_id, extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting vm nic",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            (
                "state",
                "present",
                (
                    "ext_id",
                    "backing_info",
                    "nic_backing_info",
                    "network_info",
                    "nic_network_info",
                ),
                True,
            ),
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
        if module.params.get("ext_id"):
            update_nic(module, result)
        else:
            create_nic(module, result)
    else:
        delete_nic(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
