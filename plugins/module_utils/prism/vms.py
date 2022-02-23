# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import os
from copy import deepcopy

from .clusters import Cluster
from .groups import Groups
from .images import Image
from .prism import Prism
from .projects import Project
from .subnets import Subnet


class VM(Prism):
    def __init__(self, module):
        resource_type = "/vms"
        super(VM, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "project": self._build_spec_project,
            "cluster": self._build_spec_cluster,
            "vcpus": self._build_spec_vcpus,
            "cores_per_vcpu": self._build_spec_cores,
            "memory_gb": self._build_spec_mem,
            "networks": self._build_spec_networks,
            "disks": self._build_spec_disks,
            "boot_config": self._build_spec_boot_config,
            "guest_customization": self._build_spec_gc,
            "timezone": self._build_spec_timezone,
            "categories": self._build_spec_categories,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "vm"},
                "spec": {
                    "cluster_reference": {"kind": "cluster", "uuid": None},
                    "name": None,
                    "resources": {
                        "num_sockets": 1,
                        "num_vcpus_per_socket": 1,
                        "memory_size_mib": 4096,
                        "power_state": "ON",
                        "disk_list": [],
                        "nic_list": [],
                        "gpu_list": [],
                        "boot_config": {
                            "boot_type": "LEGACY",
                            "boot_device_order_list": ["CDROM", "DISK", "NETWORK"],
                        },
                        "hardware_clock_timezone": "UTC",
                    },
                },
            }
        )

    def _get_default_network_spec(self):
        return deepcopy(
            {
                "ip_endpoint_list": [],
                "subnet_reference": {"kind": "subnet", "uuid": None},
                "is_connected": True,
            }
        )

    def _get_default_disk_spec(self):
        return deepcopy(
            {
                "device_properties": {
                    "device_type": "DISK",
                    "disk_address": {"adapter_type": None, "device_index": None},
                },
                "storage_config": {
                    "storage_container_reference": {
                        "kind": "storage_container",
                        "uuid": None,
                    }
                },
                "data_source_reference": {"kind": "image", "uuid": None},
            }
        )

    def _build_spec_name(self, payload, value):
        payload["spec"]["name"] = value
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["spec"]["description"] = value
        return payload, None

    def _build_spec_project(self, payload, param):
        if "name" in param:
            project = Project(self.module)
            name = param["name"]
            uuid = project.get_uuid(name)
            if not uuid:

                error = "Project {0} not found.".format(name)
                return None, error

        elif "uuid" in param:
            uuid = param["uuid"]

        payload["metadata"].update(
            {"project_reference": {"uuid": uuid, "kind": "project"}}
        )
        return payload, None

    def _build_spec_cluster(self, payload, param):
        if "name" in param:
            cluster = Cluster(self.module)
            name = param["name"]
            uuid = cluster.get_uuid(name)
            if not uuid:

                error = "Cluster {0} not found.".format(name)
                return None, error

        elif "uuid" in param:
            uuid = param["uuid"]

        payload["spec"]["cluster_reference"]["uuid"] = uuid
        return payload, None

    def _build_spec_vcpus(self, payload, value):
        payload["spec"]["resources"]["num_sockets"] = value
        return payload, None

    def _build_spec_cores(self, payload, value):
        payload["spec"]["resources"]["num_vcpus_per_socket"] = value
        return payload, None

    def _build_spec_mem(self, payload, value):
        payload["spec"]["resources"]["memory_size_mib"] = value * 1024
        return payload, None

    def _build_spec_networks(self, payload, networks):
        nics = []
        for network in networks:
            nic = self._get_default_network_spec()
            if network.get("private_ip"):
                nic["ip_endpoint_list"].append({"ip": network["private_ip"]})

            nic["is_connected"] = network["is_connected"]

            if network.get("subnet", {}).get("name"):
                subnet = Subnet(self.module)
                name = network["subnet"]["name"]
                uuid = subnet.get_uuid(name)
                if not uuid:
                    error = "Subnet {0} not found.".format(name)
                    return None, error

            elif network.get("subnet", {}).get("uuid"):
                uuid = network["subnet"]["uuid"]

            nic["subnet_reference"]["uuid"] = uuid

            nics.append(nic)

        payload["spec"]["resources"]["nic_list"] = nics
        return payload, None

    def _build_spec_disks(self, payload, vdisks):
        disks = []
        device_indexes = {}

        for vdisk in vdisks:
            disk = self._get_default_disk_spec()

            if vdisk.get("type"):
                disk["device_properties"]["device_type"] = vdisk["type"]

            if vdisk.get("bus"):
                if vdisk["bus"] in device_indexes:
                    device_indexes[vdisk["bus"]] += 1
                else:
                    device_indexes[vdisk["bus"]] = 0

                disk["device_properties"]["disk_address"]["adapter_type"] = vdisk["bus"]
                disk["device_properties"]["disk_address"][
                    "device_index"
                ] = device_indexes[vdisk["bus"]]

            if vdisk.get("empty_cdrom"):
                disk.pop("data_source_reference")
                disk.pop("storage_config")

            else:
                if vdisk.get("size_gb"):
                    disk["disk_size_bytes"] = vdisk["size_gb"] * 1024 * 1024 * 1024

                if vdisk.get("storage_container"):
                    disk.pop("data_source_reference")
                    if vdisk["storage_container"].get("name"):
                        groups = Groups(self.module)
                        name = vdisk["storage_container"]["name"]
                        uuid = groups.get_uuid(
                            value=name,
                            key="container_name",
                            entity_type="storage_container",
                        )
                        if not uuid:
                            error = "Storage container {0} not found.".format(name)
                            return None, error

                    elif vdisk["storage_container"].get("uuid"):
                        uuid = vdisk["storage_container"]["uuid"]

                    disk["storage_config"]["storage_container_reference"]["uuid"] = uuid

                elif vdisk.get("clone_image"):
                    if "name" in vdisk["clone_image"]:
                        image = Image(self.module)
                        name = vdisk["clone_image"]["name"]
                        uuid = image.get_uuid(name)
                        if not uuid:
                            error = "Image {0} not found.".format(name)
                            return None, error

                    elif "uuid" in vdisk["clone_image"]:
                        uuid = vdisk["clone_image"]["uuid"]

                    disk["data_source_reference"]["uuid"] = uuid

            if (
                not disk.get("storage_config", {})
                .get("storage_container_reference", {})
                .get("uuid")
            ):
                disk.pop("storage_config", None)

            if not disk.get("data_source_reference", {}).get("uuid"):
                disk.pop("data_source_reference", None)

            disks.append(disk)

        payload["spec"]["resources"]["disk_list"] = disks
        return payload, None

    def _build_spec_boot_config(self, payload, param):
        boot_config = payload["spec"]["resources"]["boot_config"]
        if "LEGACY" == param["boot_type"] and "boot_order" in param:
            boot_config["boot_device_order_list"] = param["boot_order"]

        elif "UEFI" == param["boot_type"]:
            boot_config.pop("boot_device_order_list")
            boot_config["boot_type"] = "UEFI"

        elif "SECURE_BOOT" == param["boot_type"]:
            boot_config.pop("boot_device_order_list")
            boot_config["boot_type"] = "SECURE_BOOT"
            payload["spec"]["resources"]["machine_type"] = "Q35"
        return payload, None

    def _build_spec_gc(self, payload, param):
        fpath = param["script_path"]

        if not os.path.exists(fpath):
            error = "File not found: {0}".format(fpath)
            return None, error

        with open(fpath, "rb") as f:
            content = base64.b64encode(f.read())
        gc_spec = {"guest_customization": {}}

        if "sysprep" in param["type"]:
            gc_spec["guest_customization"] = {
                "sysprep": {"install_type": "PREPARED", "unattend_xml": content}
            }

        elif "cloud_init" in param["type"]:
            gc_spec["guest_customization"] = {"cloud_init": {"user_data": content}}

        if "is_overridable" in param:
            gc_spec["guest_customization"]["is_overridable"] = param["is_overridable"]
        payload["spec"]["resources"].update(gc_spec)
        return payload, None

    def _build_spec_timezone(self, payload, value):
        payload["spec"]["resources"]["hardware_clock_timezone"] = value
        return payload, None

    def _build_spec_categories(self, payload, value):
        payload["metadata"]["categories_mapping"] = value
        payload["metadata"]["use_categories_mapping"] = True
        return payload, None


# Helper functions


def get_vm_uuid(config, module):
    if "name" in config:
        vm = VM(module)
        name = config.get("name")
        uuid = vm.get_uuid(name, "vm_name")
        if not uuid:
            error = "VM {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config.get("uuid")

    return uuid, None
