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
    manual_mode_node_spec = dict(
        node_uuid=dict(type="str", required=True),
        node_position=dict(type="str", required=True, choices=["A", "B", "C", "D"]),
        hypervisor_hostname=dict(type="str", required=True),
        hypervisor_ip=dict(type="str", required=True),
        cvm_ip=dict(type="str", required=True),
        ipmi_ip=dict(type="str", required=True),
        ipmi_password=dict(type="str", required=False, no_log=True),
        ipmi_user=dict(type="str", required=False),
        image_now=dict(type=bool, required=True),
        node_serial=dict(type=str, required=False),
        hypervisor=dict(type="str", required=True, choice=hypervisor_options),
    )
    discovery_override = dict(
        hypervisor_hostname=dict(type="str", required=False),
        hypervisor_ip=dict(type="str", required=False),
        cvm_ip=dict(type="str", required=False),
        ipmi_ip=dict(type="str", required=False),
        hypervisor=dict(type="str", required=False, choice=hypervisor_options),
    )
    discovery_mode_node_spec = dict(
        node_serial=dict(type="str", required=True),
        image_now=dict(type="bool", required=True),
        discovery_override=dict(
            type="dict", required=False, options=discovery_override
        ),
        ipmi_password=dict(type="str", required=False, no_log=True),
        ipmi_user=dict(type="str", required=False),
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
        redundancy_factor=dict(type="int", required=True, choices=[2, 3]),
        timezone=dict(type="str", required=True),
        cvm_vip=dict(type="str", required=False),
        cvm_ntp_servers=dict(type="list", elements="str", required=False),
        cvm_dns_servers=dict(type="list", elements="str", required=False),
        cluster_init_now=dict(type="bool", default=True),
    )

    hypervisor_iso_spec_dict = dict(
        filename=dict(type="str", required=True),
        checksum=dict(type="str", required=False),
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

    module_args = dict(
        cvm_gateway=dict(type="str", required=True),
        cvm_netmask=dict(type="str", required=True),
        hypervisor_gateway=dict(type="str", required=True),
        hypervisor_nameserver=dict(type="str", required=True),
        hypervisor_netmask=dict(type="str", required=True),
        nos_package=dict(type="str", required=True),
        blocks=dict(type="list", required=True, options=block_spec, elements="dict"),
        cluster=dict(type="dict", required=False, options=cluster_spec),
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

    resp, status = image_nodes.create(spec)
    if status["error"]:
        result["error"] = status["error"]
        result["response"] = resp
        module.fail_json(msg="Failed to image nodes", **result)

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
    resp, status = progress.wait_for_completion(session_id)
    result["response"] = resp
    if status["error"]:
        result["error"] = status["error"]
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
