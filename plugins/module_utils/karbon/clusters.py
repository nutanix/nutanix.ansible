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

    def __init__(self, module, resource_type="/v1/k8s/clusters"):
        super(Cluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "k8s_version": self._build_spec_k8s_version,
            "cni": self._build_spec_cni,
            "custom_node_configs": self._build_spec_node_configs,
            "storage_class": self._build_spec_storage_class,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "metadata": {"api_version": "v1.0.0"},
                "version": "",
                "cni_config": {},
                "etcd_config": {},
                "masters_config": {"single_master_config": {}},
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
        }
        provider = config.get("network_provider")
        if provider == "Calico":
            cni["calico_config"] = {
                "ip_pool_configs": [{"cidr": config["pod_ipv4_cidr"]}]
            }
        elif provider == "Flannel":
            cni["flannel_config"] = {}
        payload["cni_config"] = cni
        return payload, None

    def _build_spec_node_configs(self, payload, config):
        self.type_is_dev = self.module.params.get("cluster_type") != "PROD"
        control_plane_virtual_ip = self.module.params.get(
            "control_plane_virtual_ip", None
        )
        for key, value in config.items():

            spec_key = "{0}_config".format(key)
            node_pool, err = self._generate_resource_spec(
                value, key if key[-1] != "s" else key[:-1:]
            )
            if err:
                return None, err

            payload[spec_key]["node_pools"] = [node_pool]
            if spec_key == "masters_config":
                if node_pool["num_instances"] > 1:

                    if not control_plane_virtual_ip:
                        err = "control_plane_virtual_ip is required if the number of master nodes is 2 or cluster_type is 'PROD'."
                        return None, err

                    payload[spec_key].pop("single_master_config")
                    payload[spec_key]["active_passive_config"] = {
                        "external_ipv4_address": control_plane_virtual_ip
                    }

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
                "username": config["nutanix_cluster_username"],
                "password": config["nutanix_cluster_password"],
                "storage_container": config["storage_container"],
                "file_system": config.get("file_system"),
                "flash_mode": config.get("flash_mode"),
            },
        }
        payload["storage_class_config"] = storage_class
        return payload, None

    def _generate_resource_spec(self, config, resource_type):

        config, err = self.validate_resources(config, resource_type)
        if err:
            return None, err

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

        node = {
            "name": "{0}_{1}_pool".format(
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
        }
        num_instances = config.get(
            "num_instances",
            1 if self.type_is_dev else 3 if resource_type != "master" else 2,
        )
        node["num_instances"] = num_instances

        return node, None

    @staticmethod
    def validate_resources(resources, resource_type):
        min_cpu = 4
        min_memory = 8
        min_disk_size = 120
        err = "{0} cannot be less then {1}"
        if (
            resource_type == "master"
            and resources.get("num_instances")
            and resources["num_instances"] not in [1, 2]
        ):
            return None, "value of masters.num_instances must be 1 or 2"
        elif (
            resource_type == "etcd"
            and resources.get("num_instances")
            and resources["num_instances"] not in [1, 3, 5]
        ):
            return None, "value of etcd.num_instances must be 1, 3 or 5"
        if resources["cpu"] < min_cpu:
            return None, err.format("cpu", min_cpu)
        if resources["memory_gb"] < min_memory:
            return None, err.format("memory_gb", min_memory)
        if resources["disk_gb"] < min_disk_size:
            return None, err.format("disk_gb", min_disk_size)
        return resources, None
