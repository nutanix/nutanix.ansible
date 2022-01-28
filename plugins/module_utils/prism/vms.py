# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from re import search


__metaclass__ = type
from copy import deepcopy

import base64
import os

from .clusters import Cluster
from .prism import Prism
from .projects import Project
from .subnets import Subnet
from .groups import Groups
from .images import Image


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

    def get_spec(self):
        spec = self._get_default_spec()
        for ansible_param, ansible_value in self.module.params.items():
            build_spec_method = self.build_spec_methods.get(ansible_param)
            if build_spec_method and ansible_value:
                _, error = build_spec_method(spec, ansible_value)
        return spec, None

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
                "disk_size_bytes": None,
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
                error = "Failed to get UUID for project name: {0}".format(name)
                return None, error

        elif "uuid" in param:
            uuid = param["uuid"]

        payload["metadata"]["project_reference"]["uuid"] = uuid
        return payload, None

    def _build_spec_cluster(self, payload, param):
        if "name" in param:
            cluster = Cluster(self.module)
            name = param["name"]
            uuid = cluster.get_uuid(name)
            if not uuid:
                error = "Failed to get UUID for cluster name: {0}".format(name)
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

            if "private_ip" in network:
                nic["ip_endpoint_list"]["ip"] = network["private_ip"]

            if "is_connected" in network:
                nic["is_connected"] = network["is_connected"]

            if network.get("subnet") and "name" in network["subnet"]:
                subnet = Subnet(self.module)
                name = network["subnet"]["name"]
                uuid = subnet.get_uuid(name)
                if not uuid:
                    error = "Failed to get UUID for subnet name: {0}".format(name)
                    return None, error

            elif "uuid" in network["subnet"]:
                uuid = network["subnet"]["uuid"]

            nic["subnet_reference"]["uuid"] = uuid

            nics.append(nic)

        payload["spec"]["resources"]["nic_list"] = nics
        return payload, None

    def _build_spec_disks(self, payload, vdisks):
        disks = []
        scsi_index = sata_index = pci_index = ide_index = 0

        for vdisk in vdisks:
            disk = self._get_default_disk_spec()

            if "type" in vdisk:
                disk["device_properties"]["device_type"] = vdisk["type"]

            if "bus" in vdisk:
                if vdisk["bus"] == "SCSI":
                    device_index = scsi_index
                    scsi_index += 1
                elif vdisk["bus"] == "SATA":
                    device_index = sata_index
                    sata_index += 1
                elif vdisk["bus"] == "PCI":
                    device_index = pci_index
                    pci_index += 1
                elif vdisk["bus"] == "IDE":
                    device_index = ide_index
                    ide_index += 1

                disk["device_properties"]["disk_address"]["adapter_type"] = vdisk["bus"]
                disk["device_properties"]["disk_address"]["device_index"] = device_index

            if "empty_cdrom" in vdisk:
                disk.pop("disk_size_bytes")
                disk.pop("data_source_reference")
                disk.pop("storage_config")

            else:
                disk["disk_size_bytes"] = vdisk["size_gb"] * 1024 * 1024 * 1024

                if "storage_container" in vdisk:
                    disk.pop("data_source_reference")
                    if "name" in vdisk["storage_container"]:
                        groups = Groups(self.module)
                        name = vdisk["storage_container"]["name"]
                        uuid = groups.get_uuid(
                            entity_type="storage_container",
                            filter="container_name=={0}".format(name),
                        )
                        if not uuid:
                            error = "Failed to get UUID for storgae container: {0}".format(
                                name
                            )
                            return None, error

                    elif "uuid" in vdisk["storage_container"]:
                        uuid = vdisk["storage_container"]["uuid"]

                    disk["storage_config"]["storage_container_reference"]["uuid"] = uuid

                elif "clone_image" in vdisk:
                    if "name" in vdisk["clone_image"]:
                        image = Image(self.module)
                        name = vdisk["clone_image"]["name"]
                        uuid = image.get_uuid(name)
                        if not uuid:
                            error = "Failed to get UUID for image: {0}".format(name)
                            return None, error

                    elif "uuid" in vdisk["clone_image"]:
                        uuid = vdisk["clone_image"]["uuid"]

                    disk["data_source_reference"]["uuid"] = uuid
            if not disk["storage_config"]["storage_container_reference"]["uuid"]:
                disk.pop("storage_config")
            if not disk["data_source_reference"]["uuid"]:
                disk.pop("data_source_reference")

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
