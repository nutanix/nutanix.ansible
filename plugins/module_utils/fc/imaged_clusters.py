from __future__ import absolute_import, division, print_function
from copy import deepcopy
from .fc import FoundationCentral
from .imaged_nodes import ImagedNode

__metaclass__ = type


class ImagedCluster(FoundationCentral):
    entity_type = "imaged_clusters"

    def __init__(self, module):
        resource_type = "/imaged_clusters"
        self.ImgNodes = ImagedNode(module)
        super(ImagedCluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "cluster_external_ip": self._build_spec_cluster_exip,
            "common_network_settings": self._build_spec_common_network_settings,
            "hypervisor_iso_details": self._build_spec_hypervisor_iso_details,
            "storage_node_count": self._build_spec_storage_node_count,
            "redundancy_factor": self._build_spec_redundancy_factor,
            "cluster_name": self._build_spec_cluster_name,
            "aos_package_url": self._build_spec_aos_package_url,
            "cluster_size": self._build_spec_cluster_size,
            "aos_package_sha256sum": self._build_spec_aos_package_sha256sum,
            "timezone": self._build_spec_timezone,
            "nodes_list": self._build_spec_nodes_list,
            "skip_cluster_creation": self._build_spec_skip_cluster_creation,
            "filters": self._build_spec_filters,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "cluster_external_ip": "",
                "common_network_settings": {},
                "redundancy_factor": 2,
                "cluster_name": "",
                "aos_package_url": None,
                "nodes_list": [],
            }
        )

    def _build_spec_cluster_exip(self, payload, value):
        payload["cluster_external_ip"] = value

        return payload, None

    def _build_spec_storage_node_count(self, payload, value):
        payload["storage_node_count"] = value
        return payload, None

    def _build_spec_redundancy_factor(self, payload, value):
        payload["redundancy_factor"] = value
        return payload, None

    def _build_spec_cluster_name(self, payload, value):
        payload["cluster_name"] = value
        return payload, None

    def _build_spec_aos_package_url(self, payload, value):
        payload["aos_package_url"] = value
        return payload, None

    def _build_spec_cluster_size(self, payload, value):
        payload["cluster_size"] = value
        return payload, None

    def _build_spec_aos_package_sha256sum(self, payload, value):
        payload["aos_package_sha256sum"] = value
        return payload, None

    def _build_spec_timezone(self, payload, value):
        payload["timezone"] = value
        return payload, None

    def _build_spec_skip_cluster_creation(self, payload, value):
        payload["skip_cluster_creation"] = value
        return payload, None

    def _build_spec_common_network_settings(self, payload, nsettings):
        net = self._get_default_network_settings(nsettings)
        payload["common_network_settings"] = net
        return payload, None

    def _build_spec_hypervisor_iso_details(self, payload, value):
        hiso = self._get_default_hypervisor_iso_details(value)
        payload["hypervisor_iso_details"] = hiso
        return payload, None

    def _build_spec_nodes_list(self, payload, nodes):
        nodes_list = []

        for node in nodes:
            if node.get("manual_mode"):
                _node = node.get("manual_mode")
                spec = self._get_default_nodes_spec(_node)

            elif node.get("discovery_mode"):
                _node = node.get("discovery_mode")
                node_serial = _node.get("node_serial")
                node_details, error = self.ImgNodes.node_details_by_node_serial(
                    node_serial
                )
                if not node_details:
                    return None, error
                discovery_override = _node.get("discovery_override", {})
                if discovery_override:
                    node_details.update(discovery_override)
                spec = self._get_default_nodes_spec(node_details)

            nodes_list.append(spec)
        payload["nodes_list"] = nodes_list

        return payload, None

    def _build_spec_filters(self, payload, value):
        payload["filters"] = value
        return payload, None

    def _get_default_hypervisor_iso_details(self, isodetails):
        spec = {}
        default_spec = {
            "hyperv_sku": None,
            "url": None,
            "hyperv_product_key": None,
            "sha256sum": None,
        }
        for k in default_spec:
            v = isodetails.get(k)
            if v:
                spec[k] = v
        return spec

    def _get_default_network_settings(self, cnsettings):
        spec = {}
        default_spec = {
            "cvm_dns_servers": [],
            "hypervisor_dns_servers": [],
            "cvm_ntp_servers": [],
            "hypervisor_ntp_servers": [],
        }

        for k in default_spec:
            v = cnsettings.get(k)
            if v:
                spec[k] = v
        return spec

    def _get_default_nodes_spec(self, node):
        spec = {}
        default_spec = {
            "cvm_gateway": None,
            "ipmi_netmask": None,
            "rdma_passthrough": False,
            "imaged_node_uuid": None,
            "cvm_vlan_id": None,
            "hypervisor_type": None,
            "image_now": True,
            "hypervisor_hostname": None,
            "hypervisor_netmask": None,
            "cvm_netmask": None,
            "ipmi_ip": None,
            "hypervisor_gateway": None,
            "hardware_attributes_override": {},
            "cvm_ram_gb": None,
            "cvm_ip": None,
            "hypervisor_ip": None,
            "use_existing_network_settings": False,
            "ipmi_gateway": None,
        }

        for k in default_spec:
            if k in node:
                v = node.get(k)
                if v:
                    spec[k] = v
        return spec
