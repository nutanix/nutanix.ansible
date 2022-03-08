# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.foundation import (
    Foundation,
)
from ansible_collections.nutanix.ncp.plugins.module_utils.foundation.node_discovery import (
    NodeDiscovery,
)
from this import d

__metaclass__ = type

import base64
import os
from copy import deepcopy


class ImageNodes(Foundation):
    def __init__(self, module):
        resource_type = "/image_nodes"
        super(ImageNodes, self).__init__(module, resource_type=resource_type)
        self.node_discovery = NodeDiscovery(module)
        self.build_spec_methods = {
            "nos_package": self._build_spec_nos_package,
            "blocks": self._build_spec_blocks,
            "cluster": self._build_spec_cluster,
            "hypervisor_iso": self._build_spec_hypervisor_iso,
            "cvm_gateway": self._build_spec_cvm_gateway ,
            "cvm_netmask": self._build_spec_cvm_netmask ,
            "hypervisor_gateway": self._build_spec_hypervisor_gateway ,
            "hypervisor_nameserver": self._build_spec_hypervisor_nameserver ,
            "hypervisor_netmask": self._build_spec_hypervisor_netmask ,
            "ipmi_gateway": self._build_spec_ipmi_gateway ,
            "ipmi_netmask": self._build_spec_ipmi_netmask ,
            "default_ipmi_user": self._build_spec_default_ipmi_user ,
            "default_ipmi_password": self._build_spec_default_ipmi_password ,
            "skip_hypervisor": self._build_spec_skip_hypervisor ,
            "rdma_passthrough": self._build_spec_rdma_passthrough,
            "bond_mode": self._build_spec_bond_mode,
            "bond_lacp_rate": self._build_spec_bond_lacp_rate,
            "current_cvm_vlan_tag": self._build_spec_current_cvm_vlan_tag,
            "foundation_central": self._build_spec_foundation_central,
            "xen_master_label":self._build_spec_xen_master_label,
            "xen_master_password":self._build_spec_xen_master_password,
            "xen_master_ip":self._build_spec_xen_master_ip ,
            "xen_master_username":self._build_spec_xen_master_username ,
            "hyperv_external_vnic":self._build_spec_hyperv_external_vnic ,
            "hyperv_external_vswitch":self._build_spec_hyperv_external_vswitch ,
            "hyperv_sku":self._build_spec_hyperv_sku ,
            "hyperv_product_key":self._build_spec_hyperv_product_key ,
            "xen_config_type":self._build_spec_xen_config_type ,
            "ucsm_ip":self._build_spec_ucsm_ip ,
            "ucsm_user":self._build_spec_ucsm_user ,
            "ucsm_password":self._build_spec_ucsm_password ,
            "unc_path":self._build_spec_unc_path ,
            "unc_username":self._build_spec_unc_username ,
            "unc_password":self._build_spec_unc_password ,
            "svm_rescue_args":self._build_spec_svm_rescue_args ,
            "install_script": self._build_spec_install_script,
            "hypervisor_password": self._build_spec_hypervisor_password,
        }
    def _get_default_spec(self):
        return {
            "hypervisor_iso": {}
        }

    def _get_default_node_spec(self):
        return {
                "node_uuid": "",
                "node_position": "",
                "hypervisor_hostname": "",
                "hypervisor_ip": "",
                "cvm_ip": "",
                "ipmi_ip": "",
                "ipmi_password": "",
                "ipmi_user": "",
                "node_serial": "",
                "hypervisor":"",
        }

    

    def _get_fc_spec(self, fc_ip, api_key):
        return {
                "foundation_central": True,
                "fc_metadata": {
                    "fc_ip": fc_ip,
                    "api_key": api_key,
                }
        }


    def _build_spec_nodes(self,payload, param):
        nodes = []
        for n in param["nodes"]:
            node = {}
            if n.get("manual_mode"):
                node,status = self._build_spec_node_manual_mode(n.get("manual_mode"))
            if n.get("discovery_mode"):
                node,status = self._build_spec_node_discovery_mode(n.get("discovery_mode"))
            if status and status.get("error"):
                return status.get("error")
            nodes.append(node)
        payload["nodes"] = nodes
        return None


    def _build_spec_node_discovery_mode(self, n):
        resp, status = self.node_discovery.discover(include_network_details=True)
        if status and status.get("error"):
            return resp, status
        node_serial = n.get("node_serial")
        node_info = self._find_node_by_serial(node_serial, resp)
        if not node_info:
            return None, {"error": "Unable to discover node with serial {}".format(node_serial)}
        node = self._create_spec_based_on_node_template(node_info)
        discovery_override = n.get("discovery_override",{})
        node.update(discovery_override)
        node["hypervisor"] = self._ahv_hypervisor_conversion(node.get("hypervisor"))
        node["image_now"] = n.get("image_now")
        node["ipmi_password"] = n.get("ipmi_password")
        node["ipmi_user"] = n.get("ipmi_user")
        return node,status

    def _build_spec_node_manual_mode(self,n):
        node = self._create_spec_based_on_node_template(n)
        node["image_now"] = n.get("image_now")
        return node, None

    def _build_spec_foundation_central(self,payload, param):
        api_key = param.get("api_key")
        fc_ip = param.get("fc_ip")
        payload["fc_settings"]=self._get_fc_spec(fc_ip,api_key)
        return payload, None


    def _build_spec_blocks(self,payload,param):
        blocks = []
        for b in param:
            block = {}
            block["block_id"] = b.get("block_id")
            status = self._build_spec_nodes(block, b)
            if status:
                return payload, status
            blocks.append(block)
        payload["blocks"] = blocks
        return payload, None

    def _build_spec_cluster(self,payload,param):
        cluster={}
        cluster["cluster_name"]=param.get("name")
        cluster["redundancy_factor"]= param.get("redundancy_factor")
        cluster["timezone"]= param.get("timezone")
        cluster["cluster_external_ip"]= param.get("cvm_vip")
        cluster["cluster_init_now"]=param.get("cluster_init_now")
        cluster["cvm_ntp_servers"]= self._flatten_server_list(param.get("cvm_ntp_servers"))
        cluster["cvm_dns_servers"]= self._flatten_server_list(param.get("cvm_dns_servers"))
        cluster["cluster_members"] = self._get_cluster_members(payload["blocks"])
        payload["clusters"]= [cluster]
        return payload, None

    def _build_spec_hypervisor_iso(self,payload,value):
        hypervisor_iso = {}
        for hi in value:
            hi_name = hi 
            hi_val = value[hi]
            hi_name = self._ahv_hypervisor_conversion(hi_name)
            hypervisor_iso[hi_name] = {}
            if "checksum" in hi_val:
                hypervisor_iso[hi_name]["checksum"]= hi_val.get("checksum")
            if "filename" in hi_val:        
                hypervisor_iso[hi_name]["filename"]= hi_val.get("filename")
        payload["hypervisor_iso"] = hypervisor_iso
        return payload, None


    def _build_spec_nos_package(self,payload,value):
        payload["nos_package"] = value
        return payload, None

    def _build_spec_cvm_gateway(self,payload,value):
        payload["cvm_gateway"] = value
        return payload, None

    def _build_spec_cvm_netmask(self,payload,value):
        payload["cvm_netmask"] = value
        return payload, None

    def _build_spec_hypervisor_gateway(self,payload,value):
        payload["hypervisor_gateway"] = value
        return payload, None

    def _build_spec_hypervisor_nameserver(self,payload,value):
        payload["hypervisor_nameserver"] = value
        return payload, None

    def _build_spec_hypervisor_netmask(self,payload,value):
        payload["hypervisor_netmask"] = value
        return payload, None

    def _build_spec_ipmi_gateway(self,payload,value):
        payload["ipmi_gateway"] = value
        return payload, None

    def _build_spec_ipmi_netmask(self,payload,value):
        payload["ipmi_netmask"] = value
        return payload, None

    def _build_spec_default_ipmi_user(self,payload,value):
        payload["ipmi_user"] = value
        return payload, None

    def _build_spec_default_ipmi_password(self,payload,value):
        payload["ipmi_password"] = value
        return payload, None

    def _build_spec_skip_hypervisor(self,payload,value):
        payload["skip_hypervisor"] = value
        return payload, None

    def _build_spec_rdma_passthrough(self,payload,value):
        payload["rdma_passthrough"] = value
        return payload, None

    def _build_spec_bond_mode(self,payload,value):
        payload["bond_mode"] = value
        return payload, None

    def _build_spec_bond_lacp_rate(self,payload,value):
        payload["bond_lacp_rate"] = value
        return payload, None

    def _build_spec_current_cvm_vlan_tag(self,payload,value):
        payload["current_cvm_vlan_tag"] = value
        return payload, None

    def _build_spec_xen_master_label(self, payload,value):
        payload["xs_master_label"] = value 
        return payload, None 

    def _build_spec_xen_master_password(self, payload,value):
        payload["xs_master_password"] = value 
        return payload, None 

    def _build_spec_xen_master_ip(self, payload,value):
        payload["xs_master_ip"] = value 
        return payload, None 

    def _build_spec_xen_master_username(self, payload,value):
        payload["xs_master_username"] = value 
        return payload, None

    def _build_spec_hyperv_external_vnic(self, payload,value):
        payload["hyperv_external_vnic"] = value 
        return payload, None

    def _build_spec_hyperv_external_vswitch(self, payload,value):
        payload["hyperv_external_vswitch"] = value 
        return payload, None

    def _build_spec_hyperv_sku(self, payload,value):
        payload["hyperv_sku"] = value 
        return payload, None 

    def _build_spec_hyperv_product_key(self, payload,value):
        payload["hyperv_product_key"] = value 
        return payload, None 

    def _build_spec_xen_config_type(self, payload,value):
        payload["xs_config_type"] = value 
        return payload, None 

    def _build_spec_ucsm_ip(self, payload,value):
        payload["ucsm_ip"] = value 
        return payload, None 

    def _build_spec_ucsm_user(self, payload,value):
        payload["ucsm_user"] = value 
        return payload, None 

    def _build_spec_ucsm_password(self, payload,value):
        payload["ucsm_password"] = value 
        return payload, None 

    def _build_spec_unc_path(self, payload,value):
        payload["unc_path"] = value 
        return payload, None 

    def _build_spec_unc_username(self, payload,value):
        payload["unc_username"] = value 
        return payload, None 

    def _build_spec_unc_password(self, payload,value):
        payload["unc_password"] = value 
        return payload, None 

    def _build_spec_svm_rescue_args(self, payload,value):
        payload["svm_rescue_args"] = value 
        return payload, None 

    def _build_spec_install_script(self, payload, value):
        payload["install_script"] = value 
        return payload, None         

    def _build_spec_hypervisor_password(self, payload, value):
        payload["hypervisor_password"] = value 
        return payload, None      


# Helper functions
    def _flatten_server_list(self,server_list):
        return ",".join(server_list)

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

    def _find_node_by_serial(self, node_serial, blocks):
        for b in blocks.get("blocks"):
            nodes = b.get("nodes",[])
            for n in nodes:
                n_serial = n.get("node_serial")
                if node_serial == n_serial:
                    return n 
        return None


    def _create_spec_based_on_node_template(self,n):
        node = {}
        node_template = self._get_default_node_spec()
        for node_attr in node_template:
            n_val = n.get(node_attr)
            if n_val:
                if node_attr== "hypervisor":
                    n_val = self._ahv_hypervisor_conversion(n_val)
                node[node_attr] = n_val
        return node

    def _ahv_hypervisor_conversion(self, hypervisor):
        if hypervisor == "ahv":
            return "kvm"
        return hypervisor
