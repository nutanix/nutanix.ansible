#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_image_nodes
short_description: Nutanix module to foundation nodes
version_added: 1.1.0
description: 'Foundation nodes'
options:
  nutanix_host:
    description:
      - Foundation VM hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 8000
    required: false

author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""


"""

RETURN = r"""

"""

from ..module_utils.foundation.base_module import FoundationBaseModule
from ..module_utils.foundation.image_nodes import ImageNodes
from ..module_utils.foundation.progress import Progress
from ..module_utils.utils import remove_param_with_none_value


def get_module_spec():
    hypervisor_options = ["kvm", "hyperv", "xen", "esx", "ahv"]

    ucsm_params = dict(
        native_vlan=dict(type="bool", required=False),
        keep_ucsm_settings=dict(type="bool", required=False),
        mac_pool=dict(type="str", required=False),
        vlan_name=dict(type="str", required=False),
    )

    vswitches = dict(
        lacp=dict(type="str", required=False),
        bond_mode=dict(type="str", required=False),
        name=dict(type="str", required=False),
        uplinks=dict(type="str", required=False),
        mtu=dict(type="int", required=False),
        other_config=dict(type="list", elements="str", required=False),
    )

    manual_mode_node_spec = dict(
        node_uuid=dict(type="str", required=False),
        node_serial=dict(type=str, required=False),
        node_position=dict(type="str", required=True),
        hypervisor_hostname=dict(type="str", required=True),
        hypervisor_ip=dict(type="str", required=True),
        hypervisor=dict(type="str", required=True, choice=hypervisor_options),
        cvm_ip=dict(type="str", required=True),
        cvm_gb_ram=dict(type="int", required=False),
        cvm_num_vcpus=dict(type="int", required=False),
        current_cvm_vlan_tag=dict(type="int", required=False),
        image_now=dict(type=bool, required=False, default=True),
        image_delay=dict(type="int", required=False),
        ipmi_ip=dict(type="str", required=True),
        ipmi_password=dict(type="str", required=False, no_log=True),
        ipmi_user=dict(type="str", required=False),
        ipmi_netmask=dict(type="str", required=False),
        ipmi_gateway=dict(type="str", required=False),
        ipmi_mac=dict(type="str", required=False),
        ipmi_configure_now=dict(type="bool", required=False),
        ipv6_address=dict(type="str", required=False),
        device_hint=dict(type="str", required=False, choices=["vm_installer"]),
        ipv6_interface=dict(type="str", required=False),
        current_network_interface=dict(type="str", required=False),
        bond_mode=dict(type="str", required=False),
        bond_lacp_rate=dict(type="str", required=False),
        rdma_passthrough=dict(type="bool", required=False),
        bond_uplinks=dict(type="list", elements="str", required=False),
        cluster_id=dict(type="str", required=False),
        ucsm_node_serial=dict(type="str", required=False),
        image_successful=dict(type="bool", required=False),
        ucsm_managed_mode=dict(type="str", required=False),
        exlude_boot_serial=dict(type="bool", required=False),
        mitigate_low_boot_space=dict(type="bool", required=False),
        vswitches=dict(type="list", elements="dict", options=vswitches, required=False),
        ucsm_params=dict(type="dict", options=ucsm_params, required=False),
    )

    discovery_override = dict(
        hypervisor_hostname=dict(type="str", required=False),
        hypervisor_ip=dict(type="str", required=False),
        cvm_ip=dict(type="str", required=False),
        ipmi_ip=dict(type="str", required=False),
        hypervisor=dict(type="str", required=False, choice=hypervisor_options),
        node_position=dict(type="str", required=False),
        node_uuid=dict(type="str", required=False),
        ipmi_netmask=dict(type="str", required=False),
        ipmi_gateway=dict(type="str", required=False),
        ipv6_address=dict(type="str", required=False),
        current_network_interface=dict(type="str", required=False),
        current_cvm_vlan_tag=dict(type="int", required=False),
        cluster_id=dict(type="str", required=False),
    )

    discovery_mode_node_spec = dict(
        node_serial=dict(type="str", required=True),
        image_now=dict(type="bool", required=False, default=True),
        discovery_override=dict(
            type="dict", required=False, options=discovery_override
        ),
        ipmi_password=dict(type="str", required=False, no_log=True),
        ipmi_user=dict(type="str", required=False),
        image_delay=dict(type="int", required=False),
        device_hint=dict(type="str", required=False, choices=["vm_installer"]),
        cvm_gb_ram=dict(type="int", required=False),
        cvm_num_vcpus=dict(type="int", required=False),
        ipv6_interface=dict(type="str", required=False),
        bond_mode=dict(type="str", required=False),
        bond_lacp_rate=dict(type="str", required=False),
        rdma_passthrough=dict(type="bool", required=False),
        ucsm_node_serial=dict(type="str", required=False),
        ucsm_managed_mode=dict(type="str", required=False),
        exlude_boot_serial=dict(type="bool", required=False),
        mitigate_low_boot_space=dict(type="bool", required=False),
        bond_uplinks=dict(type="list", elements="str", required=False),
        vswitches=dict(type="list", elements="dict", options=vswitches, required=False),
        ucsm_params=dict(type="dict", options=ucsm_params, required=False),
    )

    node_mode_constraints = [("manual_mode", "discovery_mode")]

    node_modes = dict(
        manual_mode=dict(type="dict", options=manual_mode_node_spec),
        discovery_mode=dict(type="dict", options=discovery_mode_node_spec),
    )

    block_spec = dict(
        block_id=dict(type="str", required=True),
        nodes=dict(
            type="list",
            required=True,
            elements="dict",
            options=node_modes,
            mutually_exclusive=node_mode_constraints,
            required_one_of=node_mode_constraints,
        ),
    )
    cluster_spec = dict(
        name=dict(type="str", required=False),
        redundancy_factor=dict(type="int", required=True),
        timezone=dict(type="str", required=False),
        hypervisor_ntp_servers=dict(type="list", required=False, elements="str"),
        cluster_members=dict(type="list", required=True, elements="str"),
        cvm_vip=dict(type="str", required=False),
        cvm_ntp_servers=dict(type="list", elements="str", required=False),
        cvm_dns_servers=dict(type="list", elements="str", required=False),
        cluster_init_now=dict(type="bool", default=True),
        enable_ns=dict(type="bool", required=False),
        backplane_subnet=dict(type="str", required=False),
        backplane_netmask=dict(type="str", required=False),
        backplane_vlan=dict(type="str", required=False),
    )

    hypervisor_iso_spec_dict = dict(
        filename=dict(type="str", required=True),
        checksum=dict(type="str", required=True),
    )
    hypervisor_iso_spec = dict(
        kvm=dict(type="dict", required=False, options=hypervisor_iso_spec_dict),
        esx=dict(type="dict", required=False, options=hypervisor_iso_spec_dict),
        hyperv=dict(type="dict", required=False, options=hypervisor_iso_spec_dict),
        xen=dict(type="dict", required=False, options=hypervisor_iso_spec_dict),
        ahv=dict(type="dict", required=False, options=hypervisor_iso_spec_dict),
    )

    foundation_central = dict(
        fc_ip=dict(type="str", required=True),
        api_key=dict(type="str", required=True),
    )

    tests = dict(
        run_ncc=dict(type="bool", required=False, default=False),
        run_syscheck=dict(type="bool", required=False, default=False),
    )

    eos_metadata = dict(
        config_id=dict(type="str", required=False),
        account_name=dict(type="list", elements="str", required=False),
        email=dict(type="str", required=False),
    )

    module_args = dict(
        cvm_gateway=dict(type="str", required=True),
        cvm_netmask=dict(type="str", required=True),
        hypervisor_gateway=dict(type="str", required=True),
        hypervisor_nameserver=dict(type="str", required=False),
        hypervisor_netmask=dict(type="str", required=True),
        nos_package=dict(type="str", required=True),
        blocks=dict(type="list", required=True, options=block_spec, elements="dict"),
        clusters=dict(
            type="list", elements="dict", required=False, options=cluster_spec
        ),
        hypervisor_iso=dict(
            type="dict",
            required=False,
            options=hypervisor_iso_spec,
            mutually_exclusive=[("ahv", "kvm")],
        ),
        ipmi_gateway=dict(type="str", required=False),
        ipmi_netmask=dict(type="str", required=False),
        default_ipmi_user=dict(type="str", required=False),
        default_ipmi_password=dict(type="str", required=False, no_log=True),
        skip_hypervisor=dict(type="bool", required=False, default=False),
        rdma_passthrough=dict(type="bool", required=False, default=False),
        bond_mode=dict(type="str", required=False, choice=["static", "dynamic"]),
        bond_lacp_rate=dict(type="str", required=False, choice=["fast", "slow"]),
        current_cvm_vlan_tag=dict(type="str", required=False, default="0"),
        foundation_central=dict(
            type="dict", required=False, options=foundation_central
        ),
        tests=dict(type="dict", required=False, options=tests),
        eos_metadata=dict(type="dict", required=False, options=eos_metadata),
        hypervisor_password=dict(type="str", required=False, no_log=True),
        xen_master_label=dict(type="str", required=False),
        xen_master_password=dict(type="str", required=False, no_log=True),
        xen_master_ip=dict(type="str", required=False),
        xen_master_username=dict(type="str", required=False),
        xen_config_type=dict(type="str", required=False),
        hyperv_external_vnic=dict(type="str", required=False),
        hyperv_external_vswitch=dict(type="str", required=False),
        hyperv_sku=dict(type="str", required=False),
        hyperv_product_key=dict(type="str", required=False, no_log=True),
        ucsm_ip=dict(type="str", required=False),
        ucsm_user=dict(type="str", required=False),
        ucsm_password=dict(type="str", required=False, no_log=True),
        unc_path=dict(type="str", required=False),
        unc_username=dict(type="str", required=False),
        unc_password=dict(type="str", required=False, no_log=True),
        svm_rescue_args=dict(type="list", elements="str", required=False),
        install_script=dict(type="str", required=False),
        timeout=dict(type="int", required=False, default=3600),
    )

    return module_args


def image_nodes(module, result):
    image_nodes = ImageNodes(module)
    spec, error = image_nodes.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Image Nodes Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = image_nodes.create(spec)

    session_id = resp.get("session_id")
    if not session_id:
        module.fail_json(msg="Failed to fetch session_id during node imaging")

    result["changed"] = True
    result["response"] = resp
    result["session_id"] = session_id

    if module.params.get("wait"):
        wait_image_completion(module, result)


def wait_image_completion(module, result):
    progress = Progress(module)
    session_id = result["session_id"]
    resp, err = progress.wait_for_completion(session_id)
    result["response"] = resp
    if err:
        result["error"] = err
        result["response"] = resp
        module.fail_json(msg="Failed to image nodes", **result)


def run_module():
    module = FoundationBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("bond_mode", "dynamic", ("bond_lacp_rate",))],
    )
    remove_param_with_none_value(module.params)
    result = {}
    image_nodes(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
