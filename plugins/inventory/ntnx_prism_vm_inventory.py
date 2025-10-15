# -*- coding: utf-8 -*-

# Copyright: (c) 2021 [Balu George, Prem Karat]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    name: ntnx_prism_vm_inventory
    short_description: Get a list of Nutanix VMs for ansible dynamic inventory.
    description:
        - Get a list of Nutanix VMs for ansible dynamic inventory.
    version_added: "1.0.0"
    notes:
        - User needs to have API View access for resources for this inventory module to work.
    author:
        - "Balu George (@balugeorge)"
        - "Prem Karat (@premkarat)"
    requirements:
        - "json"
        - "tempfile"
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
            default: "9440"
            type: str
            env:
                - name: NUTANIX_PORT
        fetch_all_vms:
            description:
                - Set to C(True) to fetch all VMs
                - Set to C(False) to fetch specified number of VMs based on offset and length
                - If set to C(True), offset and length will be ignored
                - By default, this is set to C(False)
        custom_ansible_host:
            description:
                - Optional expression to construct the ansible_host for a VM instead of VM IP.
                - If provided, it will override ansible_host value with resolved value of the expression.
                - If not provided, ansible_host value will be set to VM IP as default.
            required: false
            type: dict
            suboptions:
                expr:
                    description:
                        - "Expression to construct the ansible_host for a VM."
                        - "The expression can use the following variables:"
                        - "vm_name (VM Name)"
                        - "cluster (Cluster Name)"
                        - "cluster_uuid (Cluster UUID)"
                        - "vm_uuid (VM UUID)"
                        - "vm_description (VM Description)"
                    type: str
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
        filters:
            description:
                - A list of Jinja2 expressions used to filter the inventory
                - All expressions are combined using an AND operation—each item must match every filter to be included.
            default: []
            elements: str
            type: list
    extends_documentation_fragment:
        - constructed
"""
Examples = r"""
Example 1: sample inventory file without using custom_ansible_host
if nutanix_hostname, nutanix_username, nutanix_password are not set, values will be taken from environment variables:
inventory file starts from here:
plugin: nutanix.ncp.ntnx_prism_vm_inventory
validate_certs: false
data: { offset: 0, length: 20 }
fetch_all_vms: false
groups:
  group_1: "'integration' in name"
  group_2: "'auto' in name"
  group_3: "'integration' not in name and 'auto' not in name"
keyed_groups:
  - prefix: host
    separator: "_"
    key: ansible_host

Example 2: sample inventory file with using custom_ansible_host
if nutanix_hostname, nutanix_username, nutanix_password are not set, values will be taken from environment variables:
plugin: nutanix.ncp.ntnx_prism_vm_inventory
validate_certs: false
data: { offset: 0, length: 20 }
fetch_all_vms: false
groups:
  group_1: "'integration' in name"
  group_2: "'auto' in name"
  group_3: "'integration' not in name and 'auto' not in name"
keyed_groups:
  - prefix: host
    separator: "_"
    key: ansible_host
custom_ansible_host:
  expr: "{vm_name}.nutanix1.{cluster}.nutanix2.{cluster_uuid}.nutanix3.{vm_uuid}.nutanix4.com"
"""

import json  # noqa: E402
import re  # noqa: E402
import tempfile  # noqa: E402

from ansible.errors import AnsibleError  # noqa: E402
from ansible.module_utils.basic import env_fallback  # noqa: E402
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable  # noqa: E402

from ..module_utils.v3.prism import vms  # noqa: E402


class Mock_Module:
    def __init__(
        self,
        host,
        port,
        username,
        password,
        validate_certs=False,
        fetch_all_vms=False,
        custom_ansible_host=None,
    ):
        self.tmpdir = tempfile.gettempdir()
        self.params = {
            "nutanix_host": host,
            "nutanix_port": port,
            "nutanix_username": username,
            "nutanix_password": password,
            "validate_certs": validate_certs,
            "fetch_all_vms": fetch_all_vms,
            "custom_ansible_host": custom_ansible_host,
            "load_params_without_defaults": False,
        }

    def jsonify(self, data):
        return json.dumps(data)

    def fail_json(self, msg, **kwargs):
        """Fail with a message"""
        kwargs["failed"] = True
        kwargs["msg"] = msg
        print("\n%s" % self.jsonify(kwargs))
        raise AnsibleError(self.jsonify(kwargs))


class InventoryModule(BaseInventoryPlugin, Constructable):
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

    def _build_host_vars(self, entity):
        """
        Build a dictionary of host variables from the raw entity.
        """
        cluster = entity.get("status", {}).get("cluster_reference", {}).get("name")
        cluster_uuid = entity.get("status", {}).get("cluster_reference", {}).get("uuid")
        vm_name = entity.get("status", {}).get("name")
        vm_description = entity.get("status", {}).get("description")
        vm_uuid = entity.get("metadata", {}).get("uuid")
        vm_ip = None

        vm_resources = entity.get("status", {}).get("resources", {}).copy()
        for nics in vm_resources.get("nic_list", []):
            if nics.get("nic_type") == "NORMAL_NIC":
                for endpoint in nics.get("ip_endpoint_list", []):
                    if endpoint.get("type") in ["ASSIGNED", "LEARNED"]:
                        vm_ip = endpoint.get("ip")
                        break
                if vm_ip:
                    break

        if getattr(self, "custom_ansible_host", None) and self.custom_ansible_host.get(
            "expr"
        ):
            lookup = {
                "cluster": cluster,
                "cluster_uuid": cluster_uuid,
                "vm_name": vm_name,
                "vm_description": vm_description,
                "vm_uuid": vm_uuid,
            }

            def repl(match):
                val_key = match.group(1).strip()
                val = lookup.get(val_key, "")
                if val_key not in lookup:
                    allowed_vars = ", ".join(f"'{k}'" for k in lookup.keys())
                    raise AnsibleError(
                        "Variable '{val_key}' not found when formatting ansible_host expression. ".format(val_key=val_key) +
                        "Please use one of the following allowed variables: {allowed_vars}.".format(allowed_vars=allowed_vars)
                    )
                elif val is None or val == "":
                    raise AnsibleError(
                        "Variable '{val_key}' is not defined or empty when formatting ansible_host expression for VM {vm_name}. with uuid {vm_uuid}.".format(val_key=val_key, vm_name=vm_name, vm_uuid=vm_uuid)
                    )
                return val

            vm_ip = re.sub(r"\{([^}]+)\}", repl, self.custom_ansible_host.get("expr"))

        # Remove unwanted keys.
        for key in [
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
        ]:
            vm_resources.pop(key, None)

        host_vars = {
            "ansible_host": vm_ip,
            "uuid": vm_uuid,
            "name": vm_name,
            "cluster": cluster,
            "cluster_uuid": cluster_uuid,
            "description": vm_description,
        }
        host_vars.update(vm_resources)

        # Incorporate ntnx_categories if available.
        if "metadata" in entity and "categories" in entity["metadata"]:
            host_vars["ntnx_categories"] = entity["metadata"]["categories"]

        return host_vars

    def _should_add_host(self, host_vars, host_filters, strict):
        """
        Evaluate filter expressions against host_vars.
        Returns True if the host should be added, False otherwise.
        """
        if not host_filters:
            return True

        for host_filter in host_filters:
            try:
                if not self._compose(host_filter, host_vars):
                    return False
            except Exception as e:
                if strict:
                    raise AnsibleError(
                        "Could not evaluate filter '%s' - %s" % (host_filter, str(e))
                    )
                return False
        return True

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)

        self.nutanix_hostname = self.get_option("nutanix_hostname") or env_fallback(
            "NUTANIX_HOSTNAME"
        )
        self.nutanix_username = self.get_option("nutanix_username") or env_fallback(
            "NUTANIX_USERNAME"
        )
        self.nutanix_password = self.get_option("nutanix_password") or env_fallback(
            "NUTANIX_PASSWORD"
        )
        self.nutanix_port = self.get_option("nutanix_port") or env_fallback(
            "NUTANIX_PORT"
        )
        self.data = self.get_option("data")
        self.validate_certs = self.get_option("validate_certs")
        self.fetch_all_vms = self.get_option("fetch_all_vms")
        self.custom_ansible_host = self.get_option("custom_ansible_host")
        # Determines if composed variables or groups using nonexistent variables is an error
        strict = self.get_option("strict")
        host_filters = self.get_option("filters")

        module = Mock_Module(
            self.nutanix_hostname,
            self.nutanix_port,
            self.nutanix_username,
            self.nutanix_password,
            self.validate_certs,
            self.fetch_all_vms,
            self.custom_ansible_host,
        )
        vm = vms.VM(module)
        self.data["offset"] = self.data.get("offset", 0)
        resp = vm.list(data=self.data, fetch_all_vms=self.fetch_all_vms)
        for entity in resp.get("entities", []):
            try:
                host_vars = self._build_host_vars(entity)

                if not self._should_add_host(host_vars, host_filters, strict):
                    continue

                # Add host to inventory.
                vm_name = host_vars.get("name")
                cluster = host_vars.get("cluster")
                vm_ip = host_vars.get("ansible_host")
                vm_uuid = host_vars.get("uuid")

                if cluster:
                    self.inventory.add_group(cluster)
                    self.inventory.add_child("all", cluster)
                if vm_name:
                    self.inventory.add_host(vm_name, group=cluster)
                    self.inventory.set_variable(vm_name, "ansible_host", vm_ip)
                    self.inventory.set_variable(vm_name, "uuid", vm_uuid)
                    self.inventory.set_variable(vm_name, "name", vm_name)
                    # Set all host_vars as variables.
                    for key, value in host_vars.items():
                        self.inventory.set_variable(vm_name, key, value)

                self.inventory.set_variable(
                    vm_name,
                    "project_reference",
                    entity.get("metadata", {}).get("project_reference", {}),
                )

                # Add variables created by the user's Jinja2 expressions to the host
                self._set_composite_vars(
                    self.get_option("compose"),
                    host_vars,
                    vm_name,
                    strict=strict,
                )
                self._add_host_to_composed_groups(
                    self.get_option("groups"),
                    host_vars,
                    vm_name,
                    strict=strict,
                )
                self._add_host_to_keyed_groups(
                    self.get_option("keyed_groups"),
                    host_vars,
                    vm_name,
                    strict=strict,
                )

            except (AnsibleError, Exception) as e:
                self.display.error(str(e))
