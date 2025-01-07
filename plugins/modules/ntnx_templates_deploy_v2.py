#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_templates_deploy_v2
short_description: Deploy Nutanix templates
description:
    - This module allows you to deploy Nutanix templates.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
    ext_id:
        description:
            - The external ID of the template to deploy.
        required: true
        type: str
    version_id:
        description:
            - The identifier of a Template Version.
        type: str
    number_of_vms:
        description:
            - Number of VMs to be deployed.
        type: int
    override_vms_config:
        description:
            - A list specifying the VM configuration overrides for each of the VMs to be created.
              Each element in the list corresponds to a VM and includes the override configurations
              such as VM Name, Configuration, and Guest Customization. The position of the element
              in the list defines the index of the VM to which the override configuration will be applied.
        type: list
        elements: dict
        suboptions:
                name:
                    description: Name of the virtual machine
                    type: str
                num_sockets:
                    description: Number of vCPU sockets.
                    type: int
                num_cores_per_socket:
                    description: Number of cores per socket.
                    type: int
                num_threads_per_core:
                    description: Number of threads per core.
                    type: int
                memory_size_bytes:
                    description: Memory size in bytes.
                    type: int
                nics:
                    description: NICs attached to the VM.
                    type: list
                    elements: dict
                    suboptions:
                            backing_info:
                                description: Defines a NIC emulated by the hypervisor
                                type: dict
                                suboptions:
                                    model:
                                        description: Model of the NIC
                                        type: str
                                        choices: ["VIRTIO", "E1000"]
                                    mac_address:
                                        description: MAC address of the emulated NIC.
                                        type: str
                                    is_connected:
                                        description: Indicates whether the NIC is connected or not. Default is True.
                                        type: bool
                                    num_queues:
                                        description: The number of Tx/Rx queue pairs for this NIC.
                                        type: int
                            network_info:
                                description: Network information for a NIC.
                                type: dict
                                suboptions:
                                    nic_type:
                                        description: Type of the NIC
                                        type: str
                                        choices: ["NORMAL_NIC", "DIRECT_NIC", "NETWORK_FUNCTION_NIC", "SPAN_DESTINATION_NIC"]
                                    network_function_chain:
                                        description: The network function chain associates with the NIC. Only valid if nic_type is NORMAL_NIC.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description: The globally unique identifier of a network function chain. It should be of type UUID.
                                                required: true
                                                type: str
                                    network_function_nic_type:
                                        description: The type of this Network function NIC. Defaults to INGRESS.
                                        type: str
                                        choices: ["INGRESS", "EGRESS", "TAP"]
                                    subnet:
                                        description: Network identifier for this adapter. Only valid if nic_type is NORMAL_NIC or DIRECT_NIC.
                                        type: dict
                                        suboptions:
                                            ext_id:
                                                description: The globally unique identifier of a subnet. It should be of type UUID.
                                                required: true
                                                type: str
                                    vlan_mode:
                                        description:
                                            - By default, all the virtual NICs are created in ACCESS mode, which permits only one VLAN per virtual network.
                                              TRUNKED mode allows multiple VLANs on a single VM NIC for network-aware user VMs.
                                        type: str
                                        choices: ["ACCESS", "TRUNK"]
                                    trunked_vlans:
                                        description:
                                            - List of networks to trunk if VLAN mode is marked as TRUNKED.
                                              If empty and VLAN mode is set to TRUNKED, all the VLANs are trunked.
                                        type: list
                                        elements: int
                                    should_allow_unknown_macs:
                                        description:
                                            - Indicates whether an unknown unicast traffic is forwarded to this NIC or not.
                                              This is applicable only for the NICs on the overlay subnets.
                                        type: bool
                                    ipv4_config:
                                        description: The IP address configurations.
                                        type: dict
                                        suboptions:
                                            should_assign_ip:
                                                description:
                                                    - If set to true (default value), an IP address must be assigned to the VM NIC
                                                      either the one explicitly specified by the user or allocated automatically by
                                                      the IPAM service by not specifying the IP address.
                                                      If false, then no IP assignment is required for this VM NIC.
                                                type: bool
                                            ip_address:
                                                description: Primary IP address configuration
                                                type: dict
                                                suboptions:
                                                    value:
                                                        description: IP address
                                                        type: str
                                                        required: True
                                                    prefix_length:
                                                        description: Prefix length of the IP address
                                                        type: int
                                            secondary_ip_address_list:
                                                description: List of secondary IP addresses
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    value:
                                                        description: IP address
                                                        type: str
                                                        required: True
                                                    prefix_length:
                                                        description: Prefix length of the IP address
                                                        type: int

                guest_customization:
                    description:
                        - Stage a Sysprep or cloud-init configuration file to be used by the guest for the next boot.
                          Note that the Sysprep command must be used to generalize the Windows VMs before triggering this API call.
                    type: dict
                    suboptions:
                        config:
                            type: dict
                            description: The Nutanix Guest Tools customization settings.
                            suboptions:
                                sysprep:
                                    description: Sysprep configuration for Windows guests
                                    type: dict
                                    suboptions:
                                            install_type:
                                                description:
                                                    - Indicates whether the guest will be freshly installed using this unattend configuration,
                                                      or this unattend configuration will be applied to a pre-prepared image. Default is 'PREPARED'.
                                                type: str
                                                choices: ["FRESH", "PREPARED"]
                                            sysprep_script:
                                                description: Parameters for the sysprep script
                                                type: dict
                                                suboptions:
                                                        unattendxml:
                                                            description: unattend.xml settings
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: XML content for unattend.xml
                                                                    type: str
                                                        custom_key_values:
                                                            description: Custom key-value pairs
                                                            type: dict
                                                            suboptions:
                                                                key_value_pairs:
                                                                    description: The list of the individual KeyValuePair elements.
                                                                    type: list
                                                                    elements: dict
                                                                    suboptions:
                                                                        name:
                                                                            description: The key of this key-value pair
                                                                            type: str
                                                                        value:
                                                                            description: The value associated with the key for this key-value pair
                                                                            type: raw

                                cloudinit:
                                    description: Cloud-init configuration for Linux guests
                                    type: dict
                                    suboptions:
                                            datasource_type:
                                                description: Type of cloud-init datasource
                                                type: str
                                                choices: ["CONFIG_DRIVE_V2"]
                                            metadata:
                                                description:
                                                    - The contents of the meta_data configuration for cloud-init.
                                                      This can be formatted as YAML or JSON. The value must be base64 encoded.
                                                type: str
                                            cloud_init_script:
                                                description: The script to use for cloud-init.
                                                type: dict
                                                suboptions:
                                                        user_data:
                                                            description: User data script
                                                            type: dict
                                                            suboptions:
                                                                value:
                                                                    description: The actual user data script content
                                                                    type: str
                                                                    required: True
                                                        custom_key_values:
                                                            description: Custom key-value pairs
                                                            type: dict
                                                            suboptions:
                                                                key_value_pairs:
                                                                    description: The list of the individual KeyValuePair elements.
                                                                    type: list
                                                                    elements: dict
                                                                    suboptions:
                                                                        name:
                                                                            description: The key of this key-value pair
                                                                            type: str
                                                                        value:
                                                                            description: The value associated with the key for this key-value pair
                                                                            type: raw
    cluster_reference:
        description:
            - The identifier of the Cluster where the VM(s) will be created using a Template.
        type: str
    wait:
        description:
            - Whether to wait for the template deployment to complete.
        type: bool
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Deploy VM
  nutanix.ncp.ntnx_templates_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ template_ext_id }}"
    version_id: "{{version_ext_id}}"
    cluster_reference: "{{cluster.uuid}}"

- name: Deploy vm and override config
  nutanix.ncp.ntnx_templates_deploy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ template_ext_id }}"
    version_id: "{{version_ext_id}}"
    cluster_reference: "{{cluster.uuid}}"
    override_vms_config:
      - name: vm_template_override
        num_sockets: 4
        num_cores_per_socket: 4
        num_threads_per_core: 2
        memory_size_bytes: 4294967296
"""

RETURN = r"""
ext_id:
    description: The external ID of the deployed template.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
task_ext_id:
    description: The external ID of the deployment task.
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
response:
    description: The response from the template deployment API which always includes the task details.
    type: dict
    returned: always
    sample:
        {
                "cluster_ext_ids": null,
                "completed_time": "2024-05-20T08:13:07.945618+00:00",
                "completion_details": null,
                "created_time": "2024-05-20T08:12:59.209878+00:00",
                "entities_affected": [
                    {
                        "ext_id": "fa236286-b965-4125-8367-672e6597a2f8",
                        "rel": "vmm:content:templates"
                    }
                ],
                "error_messages": null,
                "ext_id": "ZXJnb24=:f27e2a60-a171-48e5-a7ab-8872c8560984",
                "is_cancelable": false,
                "last_updated_time": "2024-05-20T08:13:07.945617+00:00",
                "legacy_error_message": null,
                "operation": "kVmTemplateDeploy",
                "operation_description": null,
                "owned_by": {
                    "ext_id": "00000000-0000-0000-0000-000000000000",
                    "name": "admin"
                },
                "parent_task": null,
                "progress_percentage": 100,
                "started_time": "2024-05-20T08:12:59.226669+00:00",
                "status": "SUCCEEDED",
                "sub_steps": null,
                "sub_tasks": [
                    {
                        "ext_id": "ZXJnb24=:1089a445-8d35-47ce-b059-2fad04432017",
                        "href": "https://000.000.000.000:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:1089a445-8d35-47ce-b059-2fad04432017",
                        "rel": "subtask"
                    },
                    {
                        "ext_id": "ZXJnb24=:e5f36bac-751d-4e69-b72c-aebb32b6cfea",
                        "href": "https://000.000.000.000:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:e5f36bac-751d-4e69-b72c-aebb32b6cfea",
                        "rel": "subtask"
                    },
                    {
                        "ext_id": "ZXJnb24=:a2bca528-3455-4115-9da0-79ed7c0ace96",
                        "href": "https://000.000.000.000:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:a2bca528-3455-4115-9da0-79ed7c0ace96",
                        "rel": "subtask"
                    }
                ],
                "warnings": null
            }
changed:
    description: Indicates whether the template deployment changed the system.
    type: bool
    returned: always
    sample: true
error:
    description: The error message if the template deployment failed.
    type: str
    returned: when error occurs
    sample: "Failed to deploy template"
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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_templates_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_template  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_override_vm_config_schema():
    override_config_schema = dict(
        name=dict(type="str"),
        num_sockets=dict(type="int"),
        num_cores_per_socket=dict(type="int"),
        num_threads_per_core=dict(type="int"),
        memory_size_bytes=dict(type="int"),
        nics=dict(
            type="list",
            elements="dict",
            options=vm_specs.get_nic_spec(),
            obj=vmm_sdk.AhvConfigNic,
        ),
        guest_customization=dict(
            type="dict",
            options=vm_specs.get_gc_spec(),
            obj=vmm_sdk.GuestCustomizationParams,
        ),
    )
    return override_config_schema


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        version_id=dict(type="str"),
        number_of_vms=dict(type="int"),
        override_vms_config=dict(
            type="list", elements="dict", options=get_override_vm_config_schema()
        ),
        cluster_reference=dict(type="str"),
    )

    return module_args


def deploy_template(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id=ext_id)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.TemplateDeployment()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create templates deploy spec", **result)

    # Generate override vm config map for each VM
    override_vms_config = module.params.get("override_vms_config", [])
    if override_vms_config:
        override_vm_config_map = {}
        vm_index = 0
        override_vms_config_schema = get_override_vm_config_schema()
        kwargs = {"module_args": override_vms_config_schema}
        for vm_config in override_vms_config:
            s = vmm_sdk.VmConfigOverride()
            s, err = sg.generate_spec(obj=s, attr=vm_config, **kwargs)
            if err:
                result["error"] = err
                module.fail_json(
                    msg="Failed generating vm config override spec", **result
                )
            override_vm_config_map[str(vm_index)] = s
            vm_index += 1

        spec.override_vm_config_map = override_vm_config_map

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create deploy template spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        version_ext_id = module.params.get("version_id")
        result[
            "msg"
        ] = "Template ({0}) with given version ({1}) will be deployed.".format(ext_id, version_ext_id)
        return

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for deploying template", **result)

    kwargs = {"if_match": etag}

    try:
        resp = templates.deploy_template(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deploying template",
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
    }
    deploy_template(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
