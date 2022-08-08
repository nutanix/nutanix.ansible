# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ..prism.clusters import get_cluster_uuid
from ..prism.subnets import get_subnet_uuid
from .karbon import Karbon


class Cluster(Karbon):
    kind = "cluster"

    def __init__(self, module):
        resource_type = "/clusters"
        super(Cluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "k8s_version": self._build_spec_k8s_version,
            "cni": self._build_spec_cni,
            "etcd": self._build_spec_etcd,
            "masters": self._build_spec_masters,
            "storage_class": self._build_spec_storage_class,
            "workers": self._build_spec_workers,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "metadata": {"api_version": "v1.0.0"},
                "version": "",
                "cni_config": {},
                "etcd_config": {},
                "masters_config": {
                    "single_master_config": {},
                },
                "storage_class_config": {},
                "workers_config": {},
            }
        )

    def _build_spec_name(self, payload, value):
        payload["name"] = value
        return payload, None

    def _build_spec_k8s_version(self, payload, value):
        payload["version"] = value
        return payload, None

    def _build_spec_cni(self, payload, config):
        cni = {
            "node_cidr_mask_size": config["node_cidr_mask_size"],
            "service_ipv4_cidr": config["service_ipv4_cidr"],
            "pod_ipv4_cidr": config["pod_ipv4_cidr"],
            "flannel_config": config.get("flannel_config", {}),
        }
        payload["cni_config"] = cni
        return payload, None

    def _build_spec_etcd(self, payload, config):
        node_pool, err = self._generate_resource_spec(config, "etcd")
        if err:
            return None, err
        payload["etcd_config"] = {"node_pools": [node_pool]}
        return payload, None

    def _build_spec_masters(self, payload, config):
        node_pool, err = self._generate_resource_spec(config, "master")
        if err:
            return None, err
        payload["masters_config"]["node_pools"] = [node_pool]
        return payload, None

    def _build_spec_storage_class(self, payload, config):

        if not hasattr(self, "cluster_uuid") and self.module.params.get("cluster"):
            cluster_ref = self.module.params.get("cluster")
            self.cluster_uuid, error = get_cluster_uuid(cluster_ref, self.module)
            if error:
                return None, error

        storage_class = {
            "default_storage_class": config.get("default_storage_class"),
            "name": config["name"],
            "reclaim_policy": config.get("reclaim_policy"),
            "volumes_config": {
                "prism_element_cluster_uuid": self.cluster_uuid,
                "username": self.module.params.get("nutanix_username"),
                "password": self.module.params.get("nutanix_password"),
                "storage_container": config["storage_container"],
                "file_system": config.get("file_system"),
                "flash_mode": config.get("flash_mode"),
            },
        }
        payload["storage_class_config"] = storage_class
        return payload, None

    def _build_spec_workers(self, payload, config):
        node_pool, err = self._generate_resource_spec(config, "worker")
        if err:
            return None, err
        payload["workers_config"] = {"node_pools": [node_pool]}
        return payload, None

    def _generate_resource_spec(self, config, resource_type):

        if not hasattr(self, "subnet_uuid") and self.module.params.get("node_subnet"):
            subnet_ref = self.module.params.get("node_subnet")
            self.subnet_uuid, err = get_subnet_uuid(subnet_ref, self.module)
            if err:
                return None, err

        if not hasattr(self, "cluster_uuid") and self.module.params.get("cluster"):
            cluster_ref = self.module.params.get("cluster")
            self.cluster_uuid, error = get_cluster_uuid(cluster_ref, self.module)
            if error:
                return None, error

        return {
            "num_instances": config.get("num_instances"),
            "name": "{0}962424e56137{1}_pool".format(
                self.module.params.get("name"), resource_type
            ),
            "node_os_version": self.module.params.get("host_os"),
            "ahv_config": {
                "cpu": config.get("cpu"),
                "memory_mib": config.get("memory_gb") * 1024,
                "disk_mib": config.get("disk_gb") * 1024,
                "network_uuid": self.subnet_uuid,
                "prism_element_cluster_uuid": self.cluster_uuid,
            },
        }, None
