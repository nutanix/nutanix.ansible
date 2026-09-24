#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_info_v2
short_description: Fetch information about Nutanix AHV based PC VMs
description:
  - This module fetches information about Nutanix AHV based PC VMs
  - The module can fetch information about all VMs or a specific AHV based PC VMs
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get VM by ext_id) -
      Required Roles: Account Owner, Administrator, Backup Admin, Consumer, Developer, Disaster Recovery Admin, Disaster Recovery Viewer,
      Flow Admin, Flow Policy Author, Flow Viewer, NCM Connector, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
      Project Manager, Storage Admin, Super Admin, User, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin,
      Self-Service Admin (deprecated)
    - >-
      B(List VMs) -
      Required Roles: Account Owner, Administrator, Backup Admin, Consumer, Developer, Flow Admin, Flow Policy Author,
      Flow Viewer, NCM Connector, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Project Manager,
      Storage Admin, Super Admin, User, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin,
      Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
        - The external ID of the VM.
        type: str
        required: false
    ip_address:
        description:
        - IP address to search for. Returns VMs where any NIC reports this IP.
        - Matches learned IPv4 addresses, configured/static IPv4 address, secondary IPv4 addresses, and learned IPv6 addresses.
        - Exact match only. No substring or CIDR matching.
        - This filtering is performed client-side on the VMs returned by the existing list_vms call. Only VMs in the returned page are searched. Pagination (page/limit) is not automatically adjusted.
        type: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Fetch information about all vms
  nutanix.ncp.ntnx_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Fetch information about a specific vm
  nutanix.ncp.ntnx_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653

- name: Search VMs by IP address (client-side filtering)
  nutanix.ncp.ntnx_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ip_address: "10.0.0.1"

- name: Search VMs by IP with additional OData filter
  nutanix.ncp.ntnx_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my-vm'"
    ip_address: "10.0.0.1"
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC vms v4 API.
    - it can be single vm or list of vms as per spec.
  type: dict
  returned: always
  sample: {
            "apc_config": {
                "cpu_model": null,
                "is_apc_enabled": false
            },
            "availability_zone": null,
            "bios_uuid": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
            "boot_config": {
                "boot_device": null,
                "boot_order": [
                    "CDROM",
                    "DISK",
                    "NETWORK"
                ]
            },
            "categories": null,
            "cd_roms": null,
            "cluster": {
                "ext_id": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
            },
            "create_time": "2024-06-24T08:01:46.269181+00:00",
            "description": "ansible test",
            "disks": null,
            "enabled_cpu_features": null,
            "ext_id": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
            "generation_uuid": "8bd335e2-f616-4806-87b3-53120c1f2acb",
            "gpus": null,
            "guest_customization": null,
            "guest_tools": null,
            "hardware_clock_timezone": "UTC",
            "host": null,
            "is_agent_vm": false,
            "is_branding_enabled": true,
            "is_cpu_passthrough_enabled": false,
            "is_cross_cluster_migration_in_progress": false,
            "is_gpu_console_enabled": false,
            "is_live_migrate_capable": null,
            "is_memory_overcommit_enabled": false,
            "is_vcpu_hard_pinning_enabled": false,
            "is_vga_console_enabled": true,
            "links": null,
            "machine_type": "PC",
            "memory_size_bytes": 1073741824,
            "name": "GFGLBElSNEGBansible-agvm",
            "nics": null,
            "num_cores_per_socket": 1,
            "num_numa_nodes": 0,
            "num_sockets": 1,
            "num_threads_per_core": 1,
            "ownership_info": {
                "owner": {
                    "ext_id": "00000000-0000-0000-0000-000000000000"
                }
            },
            "power_state": "OFF",
            "protection_policy_state": null,
            "protection_type": "UNPROTECTED",
            "serial_ports": null,
            "source": null,
            "storage_config": null,
            "tenant_id": null,
            "update_time": "2024-06-24T08:01:46.806598+00:00",
            "vtpm_config": {
                "is_vtpm_enabled": false,
                "version": null
            }
        }
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching vms info"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
ext_id:
    description:
        - The external ID of the vm when specific vm is fetched.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
total_available_results:
    description:
        - The total number of available VMs in PC.
    type: int
    returned: when all vms are fetched
    sample: 125
"""
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        ip_address=dict(type="str"),
    )
    return module_args


def _extract_vm_ips(vm):
    """
    Collect IP addresses reported for the VM's NICs.
    Mirrors inventory plugin ntnx_prism_vm_inventory_v2._extract_vm_ips logic
    to ensure consistent matching for learned, configured and secondary addresses.
    Returns list of string IPs, handles missing/null safely.
    """
    ips = []

    def add(value):
        if value and value not in ips:
            ips.append(value)

    for nic in vm.get("nics") or []:
        network_info = nic.get("nic_network_info") or {}

        # inventory skips non-NORMAL_NIC; keep same for consistency
        # but if nic_type missing, still evaluate IPs (handle legacy)
        nic_type = network_info.get("nic_type")
        if nic_type is not None and nic_type != "NORMAL_NIC":
            continue

        ipv4_info = network_info.get("ipv4_info") or {}
        for address in ipv4_info.get("learned_ip_addresses") or []:
            add((address or {}).get("value"))

        ipv4_config = network_info.get("ipv4_config") or {}
        add((ipv4_config.get("ip_address") or {}).get("value"))
        for address in ipv4_config.get("secondary_ip_address_list") or []:
            add((address or {}).get("value"))

        ipv6_info = network_info.get("ipv6_info") or {}
        for address in ipv6_info.get("learned_ipv6_addresses") or []:
            add((address or {}).get("value"))

    return ips


def get_vm(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = vmm.get_vm_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vm info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vms(module, result):
    vmm = get_vm_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vms info Spec", **result)

    try:
        resp = vmm.list_vms(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vms info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    if resp is None or getattr(resp, "data", None) is None:
        result["response"] = []
    else:
        data = strip_internal_attributes(resp.to_dict()).get("data") or []
        # Client-side filtering by ip_address: only VMs returned by the API in
        # the current page are searched. Pagination is not adjusted.
        requested_ip = module.params.get("ip_address")
        if requested_ip:
            filtered = []
            for vm in data:
                if requested_ip in _extract_vm_ips(vm):
                    filtered.append(vm)
            data = filtered
        result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "ip_address"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_vm(module, result)
    else:
        get_vms(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
