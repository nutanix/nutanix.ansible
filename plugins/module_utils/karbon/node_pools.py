# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ..prism.clusters import get_cluster_uuid
from ..prism.subnets import get_subnet_uuid
from .clusters import Cluster


class NodePool(Cluster):
    kind = "cluster"

    def __init__(self, module, resource_type="/v1-alpha.1/k8s/clusters"):
        super(NodePool, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
        }

    def _get_default_pool_spec(self):
        return deepcopy(
            {"name": "",
             "num_instances": 0,
             "ahv_config": {
                 "cpu": 0,
                 "disk_mib": 0,
                 "memory_mib": 0,
                 "network_uuid": "",
                 "iscsi_network_uuid": ""
             }
             }

        )

    def _build_pool_spec(self, payload, config):
        payload["name"] = config["node_pool_name"]
        payload["num_instances"] = config["pool_config"]["num_instances"]
        payload["ahv_config"]["cpu"] = config["pool_config"]["cpu"]
        payload["ahv_config"]["memory_mib"] = config["pool_config"]["memory_gb"] * 1024
        payload["ahv_config"]["disk_mib"] = config["pool_config"]["disk_gb"] * 1024
        payload["ahv_config"]["network_uuid"] = config["node_subnet"]["uuid"]
        if config.get("node_iscsi_subnet"):
            payload["ahv_config"]["iscsi_network_uuid"] = config["node_iscsi_subnet"].get("uuid")

        return payload, None

    def get_pool_spec(self):
        default_pool_spec = self._get_default_pool_spec()
        spec, error = self._build_pool_spec(default_pool_spec, self.module.params)
        if error:
            return spec, error
        return spec, None

    def add_node_pool(self, cluster_name, data=None):

        endpoint = "add-node-pool"
        resp = self.update(
            data=data,
            uuid=cluster_name,
            method="POST",
            endpoint=endpoint,
        )
        return resp

    def get_nodes_count(self, cluster_name, node_name):
        nodes_count = 0
        node_pools = self.read_node_pools(cluster_name)
        for pool in node_pools:
            if pool.get("name") == node_name:
                nodes_count = len(pool.get("nodes"))
                break
        return nodes_count

    def remove_nodes_of_pool(self, cluster_name, node_name):
        nodes_count = self.get_nodes_count(cluster_name, node_name)
        resp = {}
        if nodes_count:
            spec = {"count": nodes_count}
            endpoint = "node-pools/{0}/remove-nodes".format(node_name)
            resp = self.update(
                data=spec,
                uuid=cluster_name,
                endpoint=endpoint,
                method="POST"
            )
        return resp

    def remove_node_pool(self, cluster_name, node_name):

        endpoint = "node-pools/{0}".format(node_name)
        resp = self.delete(
            uuid=cluster_name,
            endpoint=endpoint,
        )
        return resp

    def read_node_pools(self, cluster_name):

        endpoint = "node-pools"
        resp = self.read(
            uuid=cluster_name,
            endpoint=endpoint,
        )
        return resp

    def add_node(self, cluster_name, node_name, data=None):

        endpoint = "node-pools/{0}/add-nodes".format(node_name)
        resp = self.update(
            data=data,
            uuid=cluster_name,
            endpoint=endpoint,
        )
        return resp

    def remove_node(self, cluster_name, node_name, data=None):

        endpoint = "node-pools/{0}/remove-nodes".format(node_name)
        resp = self.update(
            data=data,
            uuid=cluster_name,
            endpoint=endpoint,
        )
        return resp

    def update_labels(self, cluster_name, node_name, data=None):

        endpoint = "node-pools/{0}/update-labels".format(node_name)
        resp = self.update(
            data=data,
            uuid=cluster_name,
            endpoint=endpoint,
        )
        return resp
