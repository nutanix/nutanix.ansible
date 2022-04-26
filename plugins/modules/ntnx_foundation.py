#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ..module_utils.foundation.base_module import FoundationBaseModule
from ..module_utils.foundation.image_nodes import ImageNodes
from ..module_utils.foundation.progress import Progress
from ..module_utils.utils import remove_param_with_none_value

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_image_nodes
short_description: Nutanix module to image nodes and optionally create clusters
version_added: 1.1.0
description: 'Nutanix module to image nodes and optionally create clusters'
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
    cvm_gateway:
        description:
        - default CVM gateway
        type: str
        required: true
    cvm_netmask:
        description:
        - default CVM netmask
        type: str
        required: true
    hypervisor_gateway:
        description:
        - default hypervisor gateway
        type: str
        required: true
    hypervisor_netmask:
        description:
        - default hypervisor netmask
        type: str
        required: true
    nos_package:
        description:
        - NOS package to be installed
        type: str
        required: true
    blocks:
        description:
        - Block level parameters
        type: list
        elements: dict
        required: True
        suboptions:
            block_id:
                description:
                - Block ID
                type: str
                required: false
            nodes:
                description:
                - Block level parameters
                type: list
                elements: dict
                required: true
                suboptions:
                    manual_mode:
                        description:
                        - manually add nodes
                        - mutually exclusive with discovery_modes
                        type: dict
                        required: false
                        suboptions:
                            node_uuid:
                                description:
                                - uuid of node
                                type: str
                                required: false
                            node_serial:
                                description:
                                - serial of node
                                type: str
                                required: false
                            node_position:
                                description:
                                - set node position
                                type: str
                                required: true
                            hypervisor_hostname:
                                description:
                                - host name for hypervisor
                                type: str
                                required: true
                            hypervisor_ip:
                                description:
                                - set hypervisor ip
                                type: str
                                required: true
                            hypervisor:
                                description:
                                - hypervisor type
                                type: str
                                choices:
                                    - kvm
                                    - hyperv
                                    - xen
                                    - esx
                                    - ahv
                                required: true
                            cvm_ip:
                                description:
                                - set ip for cvm
                                type: str
                                required: true
                            cvm_gb_ram:
                                description:
                                - cvm ram in gb
                                type: int
                                required: false
                            cvm_num_vcpus:
                                description:
                                - vcpus for cvm
                                type: int
                                required: false
                            current_cvm_vlan_tag:
                                description:
                                - current cvm vlan tag
                                type: int
                                required: false
                            image_now:
                                description:
                                - image now or later
                                type: str
                                required: false
                                default: true
                            image_delay:
                                description:
                                - Imaging delay
                                type: int
                                required: false
                            ipmi_ip:
                                description:
                                - ipmi ip
                                type: str
                                required: true
                            ipmi_password:
                                description:
                                - ipmi password, override default_ipmi_password
                                - mandatory incase of ipmi based imaging and bare metal nodes
                                type: str
                                required: false
                            ipmi_user:
                                description:
                                - ipmi user, override default_ipmi_user
                                - mandatory incase of ipmi based imaging and bare metal nodes
                                type: str
                                required: false
                            ipmi_netmask:
                                description:
                                - ipmi netmask, mandatory for bare metal nodes
                                type: str
                                required: false
                            ipmi_gateway:
                                description:
                                - ipmi gateway, mandatory for bare metal nodes
                                type: str
                                required: false
                            ipmi_mac:
                                description:
                                - ipmi mac address
                                type: str
                                required: false
                            ipmi_configure_now:
                                description:
                                - set to configure ipmi before imaging
                                type: bool
                                required: false
                            ipmi_mac:
                                description:
                                - ipmi mac address
                                type: str
                                required: false
                            ipv6_address:
                                description:
                                - ipv6 address, required incase of using cvm for imaging
                                type: str
                                required: false
                            device_hint:
                                description:
                                - use "vm_installer" to enable CVM imaging from standalone
                                type: str
                                required: false
                            ipv6_interface:
                                description:
                                - ipv6 interface
                                type: str
                                required: false
                            current_network_interface:
                                description:
                                - current network interface, required incase of using cvm for imaging
                                type: str
                                required: false
                            ipv6_interface:
                                description:
                                - ipv6 interface
                                type: str
                                required: false
                            rdma_passthrough:
                                description:
                                - passthru RDMA nic to CVM if possible, default to false
                                type: bool
                                required: false
                            bond_mode:
                                description:
                                - bonde mode, "dynamic" if using LACP, "static" for LAG
                                type: str
                                choices:
                                    - dynamic
                                    - static
                                required: false
                            bond_lacp_rate:
                                description:
                                - slow or fast if lacp if being used at the switch
                                type: str
                                choices:
                                    - slow
                                    - fast
                                required: false
                            bond_uplinks:
                                description:
                                - MAC Addresses of NICs in a team/bond
                                type: list
                                elements: str
                                required: false
                            cluster_id:
                                description:
                                    - ID of cluster
                                type: str
                                required: false
                            ucsm_node_serial:
                                description:
                                    - UCSM node serial
                                type: str
                                required: false
                            ucsm_managed_mode:
                                description:
                                    - UCSM Managed mode
                                type: str
                                required: false
                            image_successful:
                                description:
                                    - UCSM node serial
                                type: bool
                                required: false
                            exlude_boot_serial:
                                description:
                                    - serial of boot device to be excluded, used by NX G6 platforms
                                type: bool
                                required: false
                            mitigate_low_boot_space:
                                description:
                                    - relocate bootbank files to make space for phoenix files
                                type: bool
                                required: false
                            vswitches:
                                description:
                                - vswitch configuration. Foundation will auto-calculate this in most cases. Provide it only if you want to override foundation's defaults.
                                type: list
                                elements: dict
                                required: false
                                suboptions:
                                    lacp:
                                        description:
                                        - Status of LACP
                                        type: str
                                        required: false
                                    bond_mode:
                                        description:
                                        - bond_mode such as balance-tcp, active-backup, etc
                                        type: str
                                        required: false
                                    name:
                                        description:
                                        - Name of the vswitch
                                        type: str
                                        required: false
                                    uplinks:
                                        description:
                                        - MAC Addresses of NICs in a team/bond
                                        type: str
                                        required: false
                                    mtu:
                                        description:
                                        - MTU of the vswitch. Applicable only for AHV
                                        type: list
                                        elements: int
                                        required: false
                                    other_conifg:
                                        description:
                                        - Auxillary lacp configurations. Applicable only for AHV
                                        type: list
                                        elements: str
                                        required: false
                            ucsm_params:
                                description:
                                - UCSM parameters
                                type: dict
                                required: false
                                suboptions:
                                    native_vlan:
                                        description:
                                        - if the vlan is native.
                                        type: bool
                                        required: false
                                    keep_ucsm_settings:
                                        description:
                                        - Whether UCSM settings should be kept
                                        type: bool
                                        required: false
                                    mac_pool:
                                        description:
                                        - Mac address pool
                                        type: str
                                        required: false
                                    vlan_name:
                                        description:
                                        - Name of vlan
                                        type: str
                                        required: false
                    discovery_mode:
                        description:
                        - discover and use existing network informatio pulled from internal info apis
                        - mutually exclusive with manual_mode
                        - can override certain fields, which are pulled during discovery
                        type: dict
                        required: false
                        suboptions:
                            node_serial:
                                description:
                                - serial of node
                                type: str
                                required: false
                            image_now:
                                description:
                                - image now or later
                                type: str
                                required: false
                                default: true
                            discovery_override:
                                description:
                                    - can override certain fields, which are pulled during discovery
                                type: dict
                                required: false
                                suboptions:
                                    node_uuid:
                                        description:
                                        - uuid of node
                                        type: str
                                        required: false
                                    node_position:
                                        description:
                                        - set node position
                                        type: str
                                        required: false
                                    hypervisor_hostname:
                                        description:
                                        - host name for hypervisor
                                        - required for dos based nodes
                                        type: str
                                        required: false
                                    hypervisor_ip:
                                        description:
                                        - set hypervisor ip
                                        - required for dos based nodes
                                        type: str
                                        required: false
                                    hypervisor:
                                        description:
                                        - hypervisor type
                                        - required for dos based nodes
                                        type: str
                                        choices:
                                            - kvm
                                            - hyperv
                                            - xen
                                            - esx
                                            - ahv
                                        required: false
                                    cvm_ip:
                                        description:
                                        - set ip for cvm
                                        type: str
                                        required: false
                                    current_cvm_vlan_tag:
                                        description:
                                        - current cvm vlan tag
                                        - required for certain case like dos based nodes
                                        type: int
                                        required: false
                                    ipmi_ip:
                                        description:
                                        - ipmi ip
                                        type: str
                                        required: true
                                    ipmi_netmask:
                                        description:
                                        - ipmi netmask, mandatory for bare metal nodes
                                        type: str
                                        required: false
                                    ipmi_gateway:
                                        description:
                                        - ipmi gateway, mandatory for bare metal nodes
                                        type: str
                                        required: false
                                    ipv6_address:
                                        description:
                                        - ipv6 address, required incase of using cvm for imaging
                                        type: str
                                        required: false
                                    current_network_interface:
                                        description:
                                        - current network interface, required incase of using cvm for imaging
                                        type: str
                                        required: false
                                    cluster_id:
                                        description:
                                            - ID of cluster
                                        type: str
                                        required: false
                            ipmi_password:
                                description:
                                - ipmi password, override default_ipmi_password
                                - mandatory incase of ipmi based imaging and bare metal nodes
                                type: str
                                required: false
                            ipmi_user:
                                description:
                                - ipmi user, override default_ipmi_user
                                - mandatory incase of ipmi based imaging and bare metal nodes
                                type: str
                                required: false
                            device_hint:
                                description:
                                - use "vm_installer" to enable CVM imaging from standalone
                                type: str
                                required: false
                            ipv6_interface:
                                description:
                                - ipv6 interface
                                type: str
                                required: false
                            rdma_passthrough:
                                description:
                                - passthru RDMA nic to CVM if possible, default to false
                                type: bool
                                required: false
                            bond_mode:
                                description:
                                - bonde mode, "dynamic" if using LACP, "static" for LAG
                                type: str
                                choices:
                                    - dynamic
                                    - static
                                required: false
                            bond_lacp_rate:
                                description:
                                - slow or fast if lacp if being used at the switch
                                type: str
                                choices:
                                    - slow
                                    - fast
                                required: false
                            bond_uplinks:
                                description:
                                - MAC Addresses of NICs in a team/bond
                                type: list
                                elements: str
                                required: false
                            ucsm_node_serial:
                                description:
                                    - UCSM node serial
                                type: str
                                required: false
                            ucsm_managed_mode:
                                description:
                                    - UCSM Managed mode
                                type: str
                                required: false
                            exlude_boot_serial:
                                description:
                                    - serial of boot device to be excluded, used by NX G6 platforms
                                type: bool
                                required: false
                            mitigate_low_boot_space:
                                description:
                                    - relocate bootbank files to make space for phoenix files
                                type: bool
                                required: false
                            vswitches:
                                description:
                                - vswitch configuration. Foundation will auto-calculate this in most cases. Provide it only if you want to override foundation's defaults.
                                type: list
                                elements: dict
                                required: false
                                suboptions:
                                    lacp:
                                        description:
                                        - Status of LACP
                                        type: str
                                        required: false
                                    bond_mode:
                                        description:
                                        - bond_mode such as balance-tcp, active-backup, etc
                                        type: str
                                        required: false
                                    name:
                                        description:
                                        - Name of the vswitch
                                        type: str
                                        required: false
                                    uplinks:
                                        description:
                                        - MAC Addresses of NICs in a team/bond
                                        type: str
                                        required: false
                                    mtu:
                                        description:
                                        - MTU of the vswitch. Applicable only for AHV
                                        type: list
                                        elements: int
                                        required: false
                                    other_conifg:
                                        description:
                                        - Auxillary lacp configurations. Applicable only for AHV
                                        type: list
                                        elements: str
                                        required: false
                            ucsm_params:
                                description:
                                - UCSM parameters
                                type: dict
                                required: false
                                suboptions:
                                    native_vlan:
                                        description:
                                        - if the vlan is native.
                                        type: bool
                                        required: false
                                    keep_ucsm_settings:
                                        description:
                                        - Whether UCSM settings should be kept
                                        type: bool
                                        required: false
                                    mac_pool:
                                        description:
                                        - Mac address pool
                                        type: str
                                        required: false
                                    vlan_name:
                                        description:
                                        - Name of vlan
                                        type: str
                                        required: false
    clusters:
        description:
        - Cluster parameters
        type: list
        elements: dict
        required: false
        suboptions:
            enable_ns:
                description:
                - If network segmentation should be enabled.
                type: bool
                required: false
            name:
                description:
                - name of cluster
                type: str
                required: true
            redundancy_factor:
                description:
                - redundancy factor
                type: int
                required: true
            timezone:
                description:
                - timezone to be set
                type: str
                required: false
            hypervisor_ntp_servers:
                description:
                - list of NTP servers of hypervisor
                type: list
                elements: str
                required: false
            cvm_ntp_servers:
                description:
                - list of NTP servers of CVM
                type: list
                elements: str
                required: false
            cvm_dns_servers:
                description:
                - list of dns servers of CVM
                type: list
                elements: str
                required: false
            cluster_members:
                description:
                - list of cluster member cvm ips
                type: list
                elements: str
                required: true
            cvm_vip:
                description:
                - cluster external ip
                type: str
                required: false
            cluster_init_now:
                description:
                - whether to create cluster now
                type: bool
                required: false
                default: true
            backplane_subnet:
                description:
                - Backplane subnet address
                type: str
                required: false
            backplane_netmask:
                description:
                - Backplane netmask
                type: str
                required: false
            backplane_vlan:
                description:
                - Backplane vlan
                type: str
                required: false
    hypervisor_iso:
        description:
        - Hypervisor ISO.
        type: dict
        required: false
        suboptions:
            kvm:
                description: kvm hypervisor details
                type: dict
                required: false
                suboptions:
                    filename:
                        description: filename of the hypervisor file in foundation vm
                        type: str
                        required: true
                    checksum:
                        description: checksum of the hypervisor file
                        type: str
                        required: true
            esx:
                description: esx hypervisor details
                type: dict
                required: false
                suboptions:
                    filename:
                        description: filename of the hypervisor file in foundation vm
                        type: str
                        required: true
                    checksum:
                        description: checksum of the hypervisor file
                        type: str
                        required: true
            hyperv:
                description: hyperv hypervisor details
                type: dict
                required: false
                suboptions:
                    filename:
                        description: filename of the hypervisor file in foundation vm
                        type: str
                        required: true
                    checksum:
                        description: checksum of the hypervisor file
                        type: str
                        required: true
            xen:
                description: xen hypervisor details
                type: dict
                required: false
                suboptions:
                    filename:
                        description: filename of the hypervisor file in foundation vm
                        type: str
                        required: true
                    checksum:
                        description: checksum of the hypervisor file
                        type: str
                        required: true
            ahv:
                description: ahv hypervisor details
                type: dict
                required: false
                suboptions:
                    filename:
                        description: filename of the hypervisor file in foundation vm
                        type: str
                        required: true
                    checksum:
                        description: checksum of the hypervisor file
                        type: str
                        required: true

    foundation_central:
        description:
        - Foundation Central specific settings
        type: dict
        required: false
        suboptions:
            fc_ip:
                description:
                    - IP address of foundation central
                type: str
                required: true
            api_key:
                description:
                    - api_key which the node uses to register itself with foundation central
                type: str
                required: true
    tests:
        description:
            - Types of tests to be performed
        type: dict
        required: false
        suboptions:
            run_ncc:
                description:
                    - Whether NCC checks should run
                type: str
                required: false
                default: false
            run_syscheck:
                description:
                    - Whether system checks should run
                type: str
                required: false
                default: false
    eos_metadata:
        description:
            - Contains user data from Eos portal
        type: dict
        required: false
        suboptions:
            config_id:
                description:
                    - Id of the Eos config uploaded in foundation GUI
                type: str
                required: false
            account_name:
                description:
                    - list of account names
                type: list
                elements: str
                required: false
            email:
                description:
                    - Email address of the user who downloaded Eos config
                type: str
                required: false

    ipmi_gateway:
        description:
        - default IPMI gateway
        type: str
        required: false
    ipmi_gateway:
        description:
        - default IPMI gateway
        type: str
        required: false
    default_ipmi_user:
        description:
        - default ipmi username, required either at node leve or here incase of ipmi based imaging
        type: str
        required: false
    default_ipmi_password:
        description:
        - default ipmi password, required either at node leve or here incase of ipmi based imaging
        type: str
        required: false
    skip_hypervisor:
        description:
        - If hypervisor installation should be skipped.
        type: bool
        default: False
        required: false
    rdma_passthrough:
        description:
        - passthru RDMA nic to CVM if possible, default to false
        type: bool
        default: false
        required: false
    bond_mode:
        description:
        - default bond_mode. "dynamic" if using LACP, "static" for LAG
        type: str
        choices:
            - dynamic
            - static
        required: false
    bond_lacp_rate:
        description:
        - slow or fast if lacp if being used at the switch
        type: str
        choices:
            - slow
            - fast
        required: false
    current_cvm_vlan_tag:
        description:
        - Current CVM vlan tag of all nodes
        type: str
        required: false
    hypervisor_password:
        description:
            - Hypervisor password
        type: str
        required: false
    xen_master_label:
        description:
            - xen server master label
        type: str
        required: false
    xen_master_password:
         description:
            - xen server master password
        type: str
        required: false
    xen_master_ip:
         description:
            - xen server master ip
        type: str
        required: false
    xen_master_username:
         description:
            - xen server master username
        type: str
        required: false
    xen_config_type:
         description:
            - xen config types
        type: str
        required: false
    hyperv_external_vnic:
        description:
            - Hyperv External virtual network adapter name
        type: str
        required: false
    hyperv_external_vswitch:
        description:
            - Hyperv External vswitch name
        type: str
        required: false
    hyperv_sku:
        description:
            - Hyperv SKU
        type: str
        required: false
    hyperv_product_key:
        description:
            - hyperv product key
        type: str
        required: false
    ucsm_ip:
        description:
            - UCSM ip address
        type: str
        required: false
    ucsm_user:
        description:
            - UCSM username
        type: str
        required: false
    ucsm_password:
        description:
            - UCSM password
        type: str
        required: false
    unc_path:
        description:
            - UNC Path
        type: str
        required: false
    unc_username:
        description:
            - UNC username
        type: str
        required: false
    unc_password:
        description:
            - UNC password
        type: str
        required: false
    svm_rescue_args:
        description:
            - Arguments to be passed to svm_rescue for AOS installation. Ensure that the arguments provided are supported by the AOS version used for imaging.
        type: list
        elements: string
        required: false
    install_script:
        description:
            - install script
        type: str
        required: false
    timeout:
        description:
            - timeout for polling imaging nodes & cluster creation process in seconds
        type: int
        required: false
        default: 3600

author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""

EXAMPLES = r"""
// in this example, we will image three nodes with new aos package and create cluster
- name: Image nodes
  hosts: localhost
  gather_facts: false
  collections:
    - nutanix.ncp
  tasks:
  - name: Image nodes
    ntnx_foundation:
      timeout : 3660
      nutanix_host: "10.xx.xx.xx"
      cvm_gateway: "10.xx.xx.xx"
      cvm_netmask: "xx.xx.xx.xx"
      hypervisor_gateway: "10.xx.xx.xx"
      hypervisor_netmask: "xx.xx.xx.xx"
      default_ipmi_user: "username"
      nos_package: "nutanix_aos_installer.tar.gz"
      blocks:
        - block_id: "<block_id>"
          nodes:
            // manually added node / baremetal
            - manual_mode :
                current_cvm_vlan_tag: xx
                cvm_gb_ram: 50
                ipmi_password: "password"
                ipmi_ip: "10.xx.xx.xx"
                cvm_ip: "10.xx.xx.xx"
                hypervisor: "kvm"
                hypervisor_ip: "10.xx.xx.xx"
                hypervisor_hostname: "superman-1"
                node_position: "D"
            // dos based node
            - discovery_mode:
                cvm_gb_ram: 50
                ipmi_password : "password"
                node_serial : "node_serial"
                discovery_override:
                  hypervisor_hostname: "superman-2"
                  hypervisor_ip: "10.xx.xx.xx"
                  cvm_ip: "10.xx.xx.xx"
                  hypervisor: "kvm"
            // aos based node
            - discovery_mode:
                cvm_gb_ram: 50
                ipmi_password : "password"
                node_serial : "node_serial"
                discovery_override:
                  hypervisor_hostname: "superman-3"
                  cvm_ip : "10.xx.xx.xx"

      clusters:
        - name : "superman"
          redundancy_factor: 2
          cluster_members:
            - "10.xx.xx.xx"
            - "10.xx.xx.xx"
            - "10.xx.xx.xx"

"""

RETURN = r"""

"""


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
        name=dict(type="str", required=True),
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
        current_cvm_vlan_tag=dict(type="str", required=False),
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
