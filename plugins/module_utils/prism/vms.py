# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import os
from copy import deepcopy

from ansible.module_utils.basic import _load_params

from .clusters import Cluster, get_cluster_uuid
from .groups import get_entity_uuid
from .images import get_image_uuid
from .prism import Prism
from .projects import Project
from .spec.categories_mapping import CategoriesMapping
from .subnets import get_subnet_uuid


class VM(Prism):
    def __init__(self, module):
        resource_type = "/vms"
        super(VM, self).__init__(module, resource_type=resource_type)
        if self.module.params.get("load_params_without_defaults", True):
            self.params_without_defaults = _load_params()
        else:
            self.params_without_defaults = self.module.params
        self.require_vm_restart = False
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
            "categories": CategoriesMapping.build_categories_mapping_spec,
            "remove_categories": CategoriesMapping.build_remove_all_categories_spec,
        }

    @staticmethod
    def is_on(payload):
        return True if payload["spec"]["resources"]["power_state"] == "ON" else False

    def get_clone_spec(self):
        spec, error = self.get_spec({"spec": {"resources": {}}})
        if error:
            return spec, error
        spec["spec"].update(spec["spec"].pop("resources", {}))
        spec["spec"].pop("hardware_clock_timezone", None)
        spec = {"override_spec": spec["spec"]}
        return spec, None

    def clone(self, spec):
        endpoint = "{0}/clone".format(self.module.params["src_vm_uuid"])
        resp = self.create(spec, endpoint)
        return resp

    def get_ova_image_spec(self):
        return deepcopy(
            {
                "name": self.module.params["name"],
                "disk_file_format": self.module.params["file_format"],
            }
        )

    def create_ova_image(self, spec):
        endpoint = "{0}/{1}".format(self.module.params["src_vm_uuid"], "export")
        resp = self.create(spec, endpoint)
        return resp

    def power_on(self, payload, raise_error=True):
        uuid = payload["metadata"]["uuid"]
        payload["spec"]["resources"]["power_state"] = "ON"
        resp = self.update(payload, uuid, raise_error=raise_error)
        return resp

    def soft_shutdown(self, payload, raise_error=True):
        uuid = payload["metadata"]["uuid"]
        payload["spec"]["resources"]["power_state"] = "OFF"
        payload["spec"]["resources"]["power_state_mechanism"]["mechanism"] = "ACPI"
        resp = self.update(payload, uuid, raise_error=raise_error)
        return resp

    def hard_power_off(self, payload, raise_error=True):
        uuid = payload["metadata"]["uuid"]
        payload["spec"]["resources"]["power_state"] = "OFF"
        payload["spec"]["resources"]["power_state_mechanism"]["mechanism"] = "HARD"
        resp = self.update(payload, uuid, raise_error=raise_error)
        return resp

    def is_restart_required(self):

        if self.require_vm_restart:
            return True

        return False

    @staticmethod
    def set_power_state(spec, power_state):
        spec["spec"]["resources"]["power_state"] = power_state

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

    def _build_spec_vcpus(self, payload, vcpus):
        current_vcpus = payload["spec"]["resources"].get("num_sockets", 0)
        self._check_and_set_require_vm_restart(current_vcpus, vcpus)
        payload["spec"]["resources"]["num_sockets"] = vcpus
        return payload, None

    def _build_spec_cores(self, payload, cores):
        self.require_vm_restart = True
        payload["spec"]["resources"]["num_vcpus_per_socket"] = cores
        return payload, None

    def _build_spec_mem(self, payload, mem_gb):
        mem_mib = mem_gb * 1024
        current_mem_mib = payload["spec"]["resources"].get("memory_size_mib", 0)
        self._check_and_set_require_vm_restart(current_mem_mib, mem_mib)
        payload["spec"]["resources"]["memory_size_mib"] = mem_mib
        return payload, None

    def _build_spec_networks(self, payload, networks):
        nics = []
        for network in networks:
            if network.get("uuid"):
                nic = self._filter_by_uuid(
                    network["uuid"], payload["spec"]["resources"]["nic_list"]
                )

                payload["spec"]["resources"]["nic_list"].remove(nic)

                if network.get("state") == "absent":
                    continue

                network = self._filter_by_uuid(
                    network["uuid"], self.params_without_defaults.get("networks", [])
                )

            else:
                nic = self._get_default_network_spec()
            if network.get("private_ip"):
                nic["ip_endpoint_list"] = [{"ip": network["private_ip"]}]

            nic["is_connected"] = network["is_connected"]
            if network.get("subnet"):

                if network.get("subnet", {}).get("uuid"):
                    uuid = network["subnet"]["uuid"]

                elif network.get("subnet", {}).get("name"):
                    name = network["subnet"]["name"]

                    # consider cluster as well to get subnet from given cluster only
                    cluster_ref = None
                    if self.module.params.get("cluster"):
                        cluster_ref = self.module.params["cluster"]
                    else:
                        cluster_ref = payload["spec"]["cluster_reference"]

                    cluster_uuid, err = get_cluster_uuid(cluster_ref, self.module)
                    if err:
                        return None, err

                    config = {
                        "name": name,
                        "cluster_uuid": cluster_uuid
                    }
                    uuid, err = get_subnet_uuid(config, self.module)
                    if err:
                        return None, err

                nic["subnet_reference"]["uuid"] = uuid

            nics.append(nic)
        if payload["spec"]["resources"].get("nic_list"):
            payload["spec"]["resources"]["nic_list"] += nics
        else:
            payload["spec"]["resources"]["nic_list"] = nics

        return payload, None

    def _build_spec_disks(self, payload, vdisks):
        device_indexes = {}
        existing_devise_indexes = list(
            map(
                lambda d: d["device_properties"]["disk_address"],
                payload["spec"]["resources"]["disk_list"],
            )
        )

        for vdisk in vdisks:

            if vdisk.get("uuid"):
                if vdisk.get("state") == "absent":
                    self._remove_disk(vdisk, payload, existing_devise_indexes)
                else:
                    self._update_disk(vdisk, payload)
            else:
                disk = self._add_disk(vdisk, device_indexes, existing_devise_indexes)
                payload["spec"]["resources"]["disk_list"].append(disk)

        return payload, None

    def _build_spec_boot_config(self, payload, param):
        boot_config = payload["spec"]["resources"]["boot_config"]
        if "LEGACY" == param["boot_type"] and "boot_order" in param:
            boot_config["boot_device_order_list"] = param["boot_order"]

        elif "UEFI" == param["boot_type"]:
            boot_config.pop("boot_device_order_list", None)
            boot_config["boot_type"] = "UEFI"

        elif "SECURE_BOOT" == param["boot_type"]:
            boot_config.pop("boot_device_order_list", None)
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

    def _check_and_set_require_vm_restart(self, current_value, new_value):
        if new_value < current_value:
            self.require_vm_restart = True

    def _filter_by_uuid(self, uuid, items_list):
        try:
            return next(filter(lambda d: d.get("uuid") == uuid, items_list))
        except BaseException:
            self.module.fail_json(
                msg="Failed generating VM Spec",
                error="Entity {0} not found.".format(uuid),
            )

    def _generate_disk_spec(
        self, vdisk, disk, device_indexes=None, existing_devise_indexes=None
    ):
        if vdisk.get("type"):
            disk["device_properties"]["device_type"] = vdisk["type"]

        bus = vdisk.get("bus")
        if bus:
            if bus in ["IDE", "SATA"]:
                self.require_vm_restart = True
            disk["device_properties"]["disk_address"]["adapter_type"] = bus
            index = device_indexes.get(bus, -1) + 1
            while True:
                if not existing_devise_indexes.count(
                    {"adapter_type": bus, "device_index": index}
                ):
                    device_indexes[bus] = index
                    break
                index += 1

            disk["device_properties"]["disk_address"]["device_index"] = device_indexes[
                bus
            ]

        if vdisk.get("empty_cdrom", None):
            disk.pop("data_source_reference", None)
            disk.pop("storage_config", None)

        else:
            if vdisk.get("size_gb"):
                disk_size_bytes = vdisk["size_gb"] * 1024 * 1024 * 1024
                if not vdisk.get("uuid") or (
                    "disk_size_bytes" in disk
                    and disk_size_bytes >= disk.get("disk_size_bytes", 0)
                ):
                    if disk.get("bus") in ["IDE", "SATA"]:
                        self.require_vm_restart = True
                    disk["disk_size_bytes"] = vdisk["size_gb"] * 1024 * 1024 * 1024
                else:
                    if disk.get("device_properties", {}).get("device_type") == "CDROM":
                        self.module.fail_json(
                            msg="Unsupported operation: Cannot resize empty cdrom.",
                            disk=disk,
                        )
                    self.module.fail_json(
                        msg="Unsupported operation: Unable to decrease disk size.",
                        disk=disk,
                    )

            if vdisk.get("storage_container"):
                disk.pop("data_source_reference", None)
                uuid, error = get_entity_uuid(
                    vdisk["storage_container"],
                    self.module,
                    key="container_name",
                    entity_type="storage_container",
                )
                if error:
                    return None, error

                disk["storage_config"]["storage_container_reference"]["uuid"] = uuid

            elif vdisk.get("clone_image"):
                uuid, error = get_image_uuid(vdisk["clone_image"], self.module)
                if error:
                    return None, error

                disk["data_source_reference"]["uuid"] = uuid

        if (
            not disk.get("storage_config", {})
            .get("storage_container_reference", {})
            .get("uuid")
        ):
            disk.pop("storage_config", None)

        if not disk.get("data_source_reference", {}).get("uuid"):
            disk.pop("data_source_reference", None)
        return disk

    def _add_disk(self, vdisk, device_indexes, existing_devise_indexes):
        disk = self._get_default_disk_spec()

        disk = self._generate_disk_spec(
            vdisk, disk, device_indexes, existing_devise_indexes
        )
        return disk

    def _update_disk(self, vdisk, payload):
        disk = self._filter_by_uuid(
            vdisk["uuid"], payload["spec"]["resources"]["disk_list"]
        )

        disk.pop("disk_size_mib", None)

        vdisk = self._filter_by_uuid(
            vdisk["uuid"], self.params_without_defaults.get("disks", [])
        )
        self._generate_disk_spec(vdisk, disk)

    def _remove_disk(self, vdisk, payload, existing_devise_indexes):
        disk = self._filter_by_uuid(
            vdisk["uuid"], payload["spec"]["resources"]["disk_list"]
        )
        existing_devise_indexes.remove(disk["device_properties"]["disk_address"])

        if disk["device_properties"]["disk_address"]["adapter_type"] != "SCSI":
            self.require_vm_restart = True

        payload["spec"]["resources"]["disk_list"].remove(disk)


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


def get_vm_reference_spec(config, module):
    uuid = config.get("uuid", "")
    name = config.get("name", "")
    if ("name" not in config) and ("uuid" not in config):
        return None, "Provide name or uuid for building vm reference spec"
    elif "name" not in config:
        vm = VM(module)
        resp = vm.read(config["uuid"])
        name = resp["status"]["name"]
    elif "uuid" not in config:
        uuid, err = get_vm_uuid(config, module)
        if err:
            return None, err

    vm_ref_spec = {"kind": "vm", "name": name, "uuid": uuid}
    return vm_ref_spec, None
