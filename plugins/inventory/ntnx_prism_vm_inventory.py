# -*- coding: utf-8 -*-

# Copyright: (c) 2021 [Balu George, Prem Karat]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    name: ntnx_prism_vm_inventory
    plugin_type: inventory
    short_description: Get a list of Nutanix VMs for ansible dynamic inventory.
    description:
        - Get a list of Nutanix VMs for ansible dynamic inventory.
    version_added: "1.0.0"
    author:
        - "Balu George (@balugeorge)"
        - "Prem Karat (@premkarat)"
    inventory: ntnx_prism_vm_inventory
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['ntnx_prism_vm_inventory', 'nutanix.ncp.ntnx_prism_vm_inventory']
        nutanix_hostname:
            description: Prism central hostname or IP address
            required: true
            type: str
            env:
                - name: NUTANIX_HOSTNAME
        nutanix_username:
            description: Prism central username
            required: true
            type: str
            env:
                - name: NUTANIX_USERNAME
        nutanix_password:
            description: Prism central password
            required: true
            type: str
            env:
                - name: NUTANIX_PASSWORD
        nutanix_port:
            description: Prism central port
            default: 9440
            type: str
            env:
                - name: NUTANIX_PORT
        data:
            description:
                - Pagination support for listing VMs
                - Default length(number of records to retrieve) has been set to 500
            default: {"offset": 0, "length": 500}
            type: dict
        validate_certs:
            description:
                - Set value to C(False) to skip validation for self signed certificates
                - This is not recommended for production setup
            default: True
            type: boolean
            env:
                - name: VALIDATE_CERTS
    notes: "null"
    requirements: "null"
"""

import json  # noqa: E402
import tempfile  # noqa: E402

from ansible.plugins.inventory import BaseInventoryPlugin  # noqa: E402

from ..module_utils.prism import vms  # noqa: E402


class Mock_Module:
    def __init__(self, host, port, username, password, validate_certs=False):
        self.tmpdir = tempfile.gettempdir()
        self.params = {
            "nutanix_host": host,
            "nutanix_port": port,
            "nutanix_username": username,
            "nutanix_password": password,
            "validate_certs": validate_certs,
        }

    def jsonify(self, data):
        return json.dumps(data)


class InventoryModule(BaseInventoryPlugin):
    """Nutanix VM dynamic invetory module for ansible"""

    NAME = "nutanix.ncp.ntnx_prism_vm_inventory"

    def verify_file(self, path):
        """Verify inventory configuration file"""
        if not super().verify_file(path):
            return False

        inventory_file_fmts = (
            "nutanix.yaml",
            "nutanix.yml",
            "nutanix_host_inventory.yaml",
            "nutanix_host_inventory.yml",
        )
        return path.endswith(inventory_file_fmts)

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)

        self.nutanix_hostname = self.get_option("nutanix_hostname")
        self.nutanix_username = self.get_option("nutanix_username")
        self.nutanix_password = self.get_option("nutanix_password")
        self.nutanix_port = self.get_option("nutanix_port")
        self.data = self.get_option("data")
        self.validate_certs = self.get_option("validate_certs")

        module = Mock_Module(
            self.nutanix_hostname,
            self.nutanix_port,
            self.nutanix_username,
            self.nutanix_password,
            self.validate_certs,
        )
        vm = vms.VM(module)
        resp = vm.list(self.data)
        keys_to_strip_from_resp = [
            "disk_list",
            "vnuma_config",
            "nic_list",
            "power_state_mechanism",
            "host_reference",
            "serial_port_list",
            "gpu_list",
            "storage_config",
            "boot_config",
            "guest_customization",
        ]

        for entity in resp["entities"]:
            cluster = entity["status"]["cluster_reference"]["name"]
            vm_name = entity["status"]["name"]
            vm_uuid = entity["metadata"]["uuid"]
            vm_ip = None

            # Get VM IP
            nic_count = 0
            for nics in entity["status"]["resources"]["nic_list"]:
                if nics["nic_type"] == "NORMAL_NIC" and nic_count == 0:
                    for endpoint in nics["ip_endpoint_list"]:
                        if endpoint["type"] == "ASSIGNED":
                            vm_ip = endpoint["ip"]
                            nic_count += 1
                            continue

            # Add inventory groups and hosts to inventory groups
            self.inventory.add_group(cluster)
            self.inventory.add_child("all", cluster)
            self.inventory.add_host(vm_name, group=cluster)
            self.inventory.set_variable(vm_name, "ansible_host", vm_ip)
            self.inventory.set_variable(vm_name, "uuid", vm_uuid)

            # Add hostvars
            for key in keys_to_strip_from_resp:
                try:
                    del entity["status"]["resources"][key]
                except KeyError:
                    pass

            for key, value in entity["status"]["resources"].items():
                self.inventory.set_variable(vm_name, key, value)
