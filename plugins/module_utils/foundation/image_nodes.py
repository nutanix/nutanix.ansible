# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from .foundation import Foundation
from .node_discovery import NodeDiscovery

__metaclass__ = type

from copy import deepcopy


class ImageNodes(Foundation):
    def __init__(self, module):
        resource_type = "/image_nodes"
        super(ImageNodes, self).__init__(module, resource_type=resource_type)
        self.node_discovery = NodeDiscovery(module)
        self._ahv_hypervisor_conversion(module)
        self.build_spec_methods = {
            "blocks": self._build_spec_blocks,
            "cluster": self._build_spec_cluster,
            "nos_package": self._build_spec_nos_package,
            "cvm_gateway": self._build_spec_cvm_gateway,
            "cvm_netmask": self._build_spec_cvm_netmask,
            "current_cvm_vlan_tag": self._build_spec_current_cvm_vlan_tag,
            "hypervisor_iso": self._build_spec_hypervisor_iso,
            "hypervisor_gateway": self._build_spec_hypervisor_gateway,
            "hypervisor_nameserver": self._build_spec_hypervisor_nameserver,
            "hypervisor_netmask": self._build_spec_hypervisor_netmask,
            "hypervisor_password": self._build_spec_hypervisor_password,
            "skip_hypervisor": self._build_spec_skip_hypervisor,
            "ipmi_gateway": self._build_spec_ipmi_gateway,
            "ipmi_netmask": self._build_spec_ipmi_netmask,
            "default_ipmi_user": self._build_spec_default_ipmi_user,
            "default_ipmi_password": self._build_spec_default_ipmi_password,
            "rdma_passthrough": self._build_spec_rdma_passthrough,
            "bond_mode": self._build_spec_bond_mode,
            "bond_lacp_rate": self._build_spec_bond_lacp_rate,
            "foundation_central": self._build_spec_foundation_central,
            "xen_master_label": self._build_spec_xen_master_label,
            "xen_master_password": self._build_spec_xen_master_password,
            "xen_master_ip": self._build_spec_xen_master_ip,
            "xen_master_username": self._build_spec_xen_master_username,
            "xen_config_type": self._build_spec_xen_config_type,
            "hyperv_external_vnic": self._build_spec_hyperv_external_vnic,
            "hyperv_external_vswitch": self._build_spec_hyperv_external_vswitch,
            "hyperv_sku": self._build_spec_hyperv_sku,
            "hyperv_product_key": self._build_spec_hyperv_product_key,
            "ucsm_ip": self._build_spec_ucsm_ip,
            "ucsm_user": self._build_spec_ucsm_user,
            "ucsm_password": self._build_spec_ucsm_password,
            "unc_path": self._build_spec_unc_path,
            "unc_username": self._build_spec_unc_username,
            "unc_password": self._build_spec_unc_password,
            "svm_rescue_args": self._build_spec_svm_rescue_args,
            "install_script": self._build_spec_install_script,
            "tests": self._build_spec_tests,
            "eos_metadata": self._build_spec_eos_meta_data,
        }

    def _get_default_spec(self):
        return deepcopy({"hypervisor_iso": {}})

    def _get_fc_spec(self, fc_ip, api_key):
        return deepcopy(
            {
                "foundation_central": True,
                "fc_metadata": {
                    "fc_ip": fc_ip,
                    "api_key": api_key,
                },
            }
        )

    def _get_default_cluster_spec(self, cluster):
        
        default_spec = {
            "redundancy_factor" : "",
            "cluster_init_now" : "",
            "enable_ns" : "",
            "backplane_subnet" : "",
            "backplane_netmask" : "",
            "backplane_vlan" : "",
        }
        return self.get_intersection_of_spec(default_spec, cluster)

    def _build_spec_foundation_central(self, payload, param):
        api_key = param.get("api_key")
        fc_ip = param.get("fc_ip")
        payload["fc_settings"] = self._get_fc_spec(fc_ip, api_key)
        return payload, None

    def _build_spec_tests(self, payload, param):
        payload["tests"] = param
        return payload, None

    def _build_spec_eos_meta_data(self, payload, param):
        payload["eos_metadata"] = param
        return payload, None
    
    def _build_spec_blocks(self, payload, blocks):
        _blocks = []
        for block in blocks:
            nodes, error = self._get_nodes(block["nodes"])
            if not nodes:
                return None, error
            _block = {}
            _block["block_id"] = block.get("block_id")
            _block["nodes"] = nodes
            _blocks.append(_block)

        payload["blocks"] = _blocks
        return payload, None

    def _build_spec_cluster(self, payload, param):
        clusters = []
        for cluster in param:   
            cluster_spec = self._get_default_cluster_spec(cluster)
            cluster_spec["cluster_name"] = param.get("name")
            cluster_spec["cluster_external_ip"] = param.get("cvm_vip")
            cluster_spec["cvm_ntp_servers"] = self._list2str(param.get("cvm_ntp_servers"))
            cluster_spec["cvm_dns_servers"] = self._list2str(param.get("cvm_dns_servers"))
            cluster_spec["cluster_members"] = param.get("cluster_members")

            if len(cluster_spec["cluster_members"])==1 :
                cluster_spec["single_node_cluster"] = True

            clusters.append(cluster_spec)
        payload["clusters"] = clusters
        return payload, None

    def _build_spec_hypervisor_iso(self, payload, value):
        hypervisor_iso = {}
        for hi in value:
            hi_name = hi
            hi_val = value[hi]
            hi_name = self._ahv2kvm(hi_name)
            hypervisor_iso[hi_name] = {}
            if "checksum" not in hi_val or "filename" not in hi_val:
                return None, "checksum and filename are required parameter for hypervisor iso" 
           
            hypervisor_iso[hi_name]["checksum"] = hi_val.get("checksum")
            hypervisor_iso[hi_name]["filename"] = hi_val.get("filename")
        payload["hypervisor_iso"] = hypervisor_iso
        return payload, None

    def _build_spec_nos_package(self, payload, value):
        payload["nos_package"] = value
        return payload, None

    def _build_spec_cvm_gateway(self, payload, value):
        payload["cvm_gateway"] = value
        return payload, None

    def _build_spec_cvm_netmask(self, payload, value):
        payload["cvm_netmask"] = value
        return payload, None

    def _build_spec_hypervisor_gateway(self, payload, value):
        payload["hypervisor_gateway"] = value
        return payload, None

    def _build_spec_hypervisor_nameserver(self, payload, value):
        payload["hypervisor_nameserver"] = value
        return payload, None

    def _build_spec_hypervisor_netmask(self, payload, value):
        payload["hypervisor_netmask"] = value
        return payload, None

    def _build_spec_ipmi_gateway(self, payload, value):
        payload["ipmi_gateway"] = value
        return payload, None

    def _build_spec_ipmi_netmask(self, payload, value):
        payload["ipmi_netmask"] = value
        return payload, None

    def _build_spec_default_ipmi_user(self, payload, value):
        payload["ipmi_user"] = value
        return payload, None

    def _build_spec_default_ipmi_password(self, payload, value):
        payload["ipmi_password"] = value
        return payload, None

    def _build_spec_skip_hypervisor(self, payload, value):
        payload["skip_hypervisor"] = value
        return payload, None

    def _build_spec_rdma_passthrough(self, payload, value):
        payload["rdma_passthrough"] = value
        return payload, None

    def _build_spec_bond_mode(self, payload, value):
        payload["bond_mode"] = value
        return payload, None

    def _build_spec_bond_lacp_rate(self, payload, value):
        payload["bond_lacp_rate"] = value
        return payload, None

    def _build_spec_current_cvm_vlan_tag(self, payload, value):
        payload["current_cvm_vlan_tag"] = value
        return payload, None

    def _build_spec_xen_master_label(self, payload, value):
        payload["xs_master_label"] = value
        return payload, None

    def _build_spec_xen_master_password(self, payload, value):
        payload["xs_master_password"] = value
        return payload, None

    def _build_spec_xen_master_ip(self, payload, value):
        payload["xs_master_ip"] = value
        return payload, None

    def _build_spec_xen_master_username(self, payload, value):
        payload["xs_master_username"] = value
        return payload, None

    def _build_spec_hyperv_external_vnic(self, payload, value):
        payload["hyperv_external_vnic"] = value
        return payload, None

    def _build_spec_hyperv_external_vswitch(self, payload, value):
        payload["hyperv_external_vswitch"] = value
        return payload, None

    def _build_spec_hyperv_sku(self, payload, value):
        payload["hyperv_sku"] = value
        return payload, None

    def _build_spec_hyperv_product_key(self, payload, value):
        payload["hyperv_product_key"] = value
        return payload, None

    def _build_spec_xen_config_type(self, payload, value):
        payload["xs_config_type"] = value
        return payload, None

    def _build_spec_ucsm_ip(self, payload, value):
        payload["ucsm_ip"] = value
        return payload, None

    def _build_spec_ucsm_user(self, payload, value):
        payload["ucsm_user"] = value
        return payload, None

    def _build_spec_ucsm_password(self, payload, value):
        payload["ucsm_password"] = value
        return payload, None

    def _build_spec_unc_path(self, payload, value):
        payload["unc_path"] = value
        return payload, None

    def _build_spec_unc_username(self, payload, value):
        payload["unc_username"] = value
        return payload, None

    def _build_spec_unc_password(self, payload, value):
        payload["unc_password"] = value
        return payload, None

    def _build_spec_svm_rescue_args(self, payload, value):
        payload["svm_rescue_args"] = value
        return payload, None

    def _build_spec_install_script(self, payload, value):
        payload["install_script"] = value
        return payload, None

    def _build_spec_hypervisor_password(self, payload, value):
        payload["hypervisor_password"] = value
        return payload, None

    def _list2str(self, lst):
        return ",".join(lst)

    def _get_cluster_members(self, blocks):
        cluster_members = []
        for b in blocks:
            nodes = b.get("nodes")
            block_members = list(map(lambda e: self._get_cvm_ip(e), nodes))
            cluster_members = cluster_members + block_members
        return cluster_members

    def _get_cvm_ip(self, node):
        cvm_ip = node.get("cvm_ip", node.get("svm_ip"))
        if not cvm_ip:
            raise Exception("unable to extract CVM IP from node {}", node)
        return cvm_ip

    def _get_nodes(self, nodes):
        _nodes = []
        for node in nodes:
            if node.get("manual_mode"):
                _node = node.get("manual_mode")
                spec = self._get_default_node_spec(_node)

            elif node.get("discovery_mode"):
                _node = node.get("discovery_mode")
                discovery_override = _node.get("discovery_override", {})
                blocks, error = self.node_discovery.discover(
                    include_network_details=True
                )
                if not blocks:
                    return None, error

                node_serial = _node.get("node_serial")
                _node = self._find_node_by_serial(node_serial, blocks["blocks"])
                if not _node:
                    error = "Failed to discover node with serial {}".format(node_serial)
                    return None, error

                spec = self._get_default_node_spec(_node)
                if discovery_override:
                    spec.update(discovery_override)

                spec["image_now"] = _node["image_now"]
                if _node.get["ipmi_user"]:
                    spec["ipmi_user"] = _node["ipmi_user"]
                if _node.get["ipmi_password"]:
                    spec["ipmi_password"] = _node["ipmi_password"]

            _nodes.append(spec)

        return _nodes, None

    def _get_default_node_spec(self, node):
        spec = {}
        default_spec = {
            "node_uuid" : "",
            "node_position" : "",
            "hypervisor_hostname" : "",
            "hypervisor_ip" : "",
            "cvm_ip" : "",
            "image_now" : True, 
            "ipmi_ip" : "",
            "ipmi_password" : "",
            "ipmi_user" : "",
            "ipmi_netmask" : "",
            "ipmi_gateway" : "",
            "ipmi_mac" : "",          
            "ipmi_configure_now" : False,
            "node_serial" : "",
            "hypervisor" : "",
            "ipv6_address" : "",
            "image_delay" : None,
            "device_hint" : "",
            "cvm_gb_ram" : None,
            "bond_mode" : "",
            "rdma_passthrough" : False,
            "cluster_id" : "",
            "ucsm_node_serial" : "",
            "ipv6_interface" : "",
            "cvm_num_vcpus" : None,
            "current_network_interface" : "",
            "bond_lacp_rate" : "",
            "ucsm_managed_mode" : "",
            "current_cvm_vlan_tag" : None,
            "exlude_boot_serial" : False,
            "mitigate_low_boot_space" : False,
            "bond_uplinks" : [],
            "vswitches" : [],
            "ucsm_params" : None,
        }
        for k in default_spec:
            v = node.get(k)
            if v:
                if k == "hypervisor":
                    v = self._ahv2kvm(v)
                spec[k] = v
        return spec

    def _ahv2kvm(self, hypervisor):
        if hypervisor == "ahv":
            return "kvm"
        return hypervisor

    def _find_node_by_serial(self, nserial, blocks):
        for block in blocks:
            nodes = block.get("nodes", [])
            for node in nodes:
                if node.get("node_serial") == nserial:
                    return node
        return None
