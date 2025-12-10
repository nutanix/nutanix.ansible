# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    name: ntnx_prism_vm_inventory_v2
    short_description: Get a list of Nutanix VMs for ansible dynamic inventory using V4 APIs.
    description:
        - Get a list of Nutanix VMs for ansible dynamic inventory using V4 APIs and SDKs.
    version_added: "2.4.0"
    author:
        - George Ghawali (@george-ghawali)
    requirements:
        - "ntnx_vmm_py_client"
        - "ntnx_clustermgmt_py_client"
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['ntnx_prism_vm_inventory_v2', 'nutanix.ncp.ntnx_prism_vm_inventory_v2']
        nutanix_host:
            description:
                - Prism central hostname or IP address
                - If not provided, values will be taken from environment variables NUTANIX_HOSTNAME or NUTANIX_HOST
                - If both are set, NUTANIX_HOSTNAME is preferred over NUTANIX_HOST
            required: false
            type: str
            env:
                - name: NUTANIX_HOSTNAME
                - name: NUTANIX_HOST
        nutanix_username:
            description:
                - Prism central username
                - If not provided, values will be taken from environment variable NUTANIX_USERNAME
            required: false
            type: str
            env:
                - name: NUTANIX_USERNAME
        nutanix_password:
            description:
                - Prism central password
                - If not provided, values will be taken from environment variable NUTANIX_PASSWORD
            required: false
            type: str
            env:
                - name: NUTANIX_PASSWORD
        nutanix_port:
            description:
                - Prism central port
                - If not provided, values will be taken from environment variable NUTANIX_PORT
                - By default, this is set to 9440
            required: false
            default: "9440"
            type: str
            env:
                - name: NUTANIX_PORT
        fetch_all_vms:
            description:
                - Set to C(True) to fetch all VMs
                - Set to C(False) to fetch specified number of VMs based on page and limit
                - If set to C(True), page and limit will be ignored
                - By default, this is set to C(False)
            default: false
            type: bool
        page:
            description:
                - Page number for pagination (starts from 0)
                - This is ignored if fetch_all_vms is set to True
            default: 0
            type: int
        limit:
            description:
                - Number of records to retrieve per page
                - Must be between 1 and 100
                - This is ignored if fetch_all_vms is set to True
            default: 50
            type: int
        filter:
            description:
                - OData filter expression to filter VMs
                - For example C(name eq 'my-vm') or C(startswith(name, 'prod'))
                - Used in List VMs API call to filter VMs
            type: str
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
                        - "cluster_name (Cluster Name)"
                        - "cluster_ext_id (Cluster External ID)"
                        - "vm_ext_id (VM External ID)"
                        - "vm_description (VM Description)"
                        - "Suppose we have a VM with name VM_123 and cluster name Cluster_456"
                        - >
                          "Then the expression {vm_name}.nutanix1.{cluster_name}.nutanix2.com will be resolved to
                          VM_123.nutanix1.Cluster_456.nutanix2.com as ansible_host"
                    type: str
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
                - Used locally to filter VMs after they are fetched from the API.
            default: []
            elements: str
            type: list
    extends_documentation_fragment:
        - constructed
        - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
# Minimal inventory file (nutanix.yml)
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false

# Fetch all VMs
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  fetch_all_vms: true

# Fetch VMs with pagination
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  page: 0
  limit: 80

# Use OData filter
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  filter: "startswith(name, 'test_vm')"

# using compose for defining new host variables
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  compose:
    ansible_user: "'ansible_user'"
    memory_gb: memory_size_bytes / 1073741824 if memory_size_bytes else 0

# using groups for grouping the VMs
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  groups:
    # Create a group for powered on VMs.
    powered_on: power_state == 'ON'
    # Create a group for powered off VMs.
    powered_off: power_state == 'OFF'

# using keyed groups for grouping the VMs
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  keyed_groups:
    - key: machine_type
      prefix: machine
      separator: "_"
    - key: power_state
      prefix: power
      separator: "_"

# using custom ansible host for defining the ansible_host for the VMs
- plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  custom_ansible_host:
    expr: "{vm_name}.nutanix1.{vm_ext_id}.nutanix2.{cluster_name}.nutanix3.{cluster_ext_id}.nutanix4.{vm_description}.com"
"""

import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import tempfile  # noqa: E402

from ansible.errors import AnsibleError  # noqa: E402
from ansible.module_utils.basic import env_fallback  # noqa: E402
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable  # noqa: E402

from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402


class Mock_Module:

    def __init__(
        self,
        hostname,
        port,
        username,
        password,
        validate_certs=False,
        fetch_all_vms=False,
        custom_ansible_host=None,
        nutanix_debug=False,
        nutanix_log_file=None,
    ):
        self.tmpdir = tempfile.gettempdir()
        self.params = {
            "nutanix_host": hostname,
            "nutanix_port": port,
            "nutanix_username": username,
            "nutanix_password": password,
            "validate_certs": validate_certs,
            "fetch_all_vms": fetch_all_vms,
            "custom_ansible_host": custom_ansible_host,
            "load_params_without_defaults": False,
            "nutanix_debug": nutanix_debug,
            "nutanix_log_file": nutanix_log_file,
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
    """Nutanix VM dynamic inventory module for ansible using V4 APIs"""

    NAME = "nutanix.ncp.ntnx_prism_vm_inventory_v2"

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

    def _fetch_vms(self, vmm, fetch_all_vms=False, page=0, limit=50, filter=None):
        """
        Fetch VMs from Nutanix using V4 SDK.
        Handles pagination if fetch_all_vms is True.
        """
        vms = []

        if fetch_all_vms:
            # Fetch all VMs using pagination
            current_page = 0
            while True:
                try:
                    kwargs = {"_page": current_page, "_limit": 100}
                    if filter:
                        kwargs["_filter"] = filter

                    resp = vmm.list_vms(**kwargs)
                except Exception as e:
                    raise AnsibleError(
                        "Failed to fetch VMs from PC: {0}".format(str(e))
                    )

                if resp and hasattr(resp, "data") and resp.data:
                    # Convert response objects to dictionaries
                    for item in resp.data:
                        vms.append(strip_internal_attributes(item.to_dict()))

                # Check if all VMs have been fetched successfully
                total_available = getattr(resp.metadata, "total_available_results", 0)
                if len(vms) >= total_available:
                    break

                current_page += 1
        else:
            # Fetch specific number of VMs based on page and limit
            try:
                kwargs = {"_page": page, "_limit": limit}
                if filter:
                    kwargs["_filter"] = filter

                resp = vmm.list_vms(**kwargs)
            except Exception as e:
                raise AnsibleError("Failed to fetch VMs from PC: {0}".format(str(e)))

            if resp and hasattr(resp, "data") and resp.data:
                for item in resp.data:
                    vms.append(strip_internal_attributes(item.to_dict()))

        return vms

    def _extract_vm_ip(self, vm):
        """
        Extract IP address from VM NICs.
        Returns the first learned/DHCP IP address found.
        """
        nics = vm.get("nics") or []
        for nic in nics:
            network_info = nic.get("nic_network_info", {})
            if network_info.get("nic_type") != "NORMAL_NIC":
                continue
            if not network_info:
                continue
            ipv4_info = network_info.get("ipv4_info")
            ipv4_config = network_info.get("ipv4_config")
            if ipv4_info:
                learned_ips = ipv4_info.get("learned_ip_addresses", [])
                if learned_ips and len(learned_ips) > 0:
                    first_ip = learned_ips[0]
                    if first_ip and first_ip.get("value"):
                        return first_ip.get("value")
            elif ipv4_config:
                ip_address = ipv4_config.get("ip_address")
                if ip_address:
                    value = ip_address.get("value")
                    if value:
                        return value
            else:
                ipv6_info = network_info.get("ipv6_info")
                if ipv6_info:
                    learned_ips = ipv6_info.get("learned_ipv6_addresses", [])
                    if learned_ips and len(learned_ips) > 0:
                        first_ip = learned_ips[0]
                        if first_ip and first_ip.get("value"):
                            return first_ip.get("value")

        return None

    def _resolve_custom_ansible_host(self, vm, cluster_ext_id_name_map, expr, strict):
        """Resolve ansible_host expression with placeholders if defined."""

        lookup = {
            "cluster_name": cluster_ext_id_name_map.get(
                vm.get("cluster", {}).get("ext_id")
            ),
            "cluster_ext_id": vm.get("cluster", {}).get("ext_id"),
            "vm_name": vm.get("name"),
            "vm_description": vm.get("description"),
            "vm_ext_id": vm.get("ext_id"),
        }

        try:
            vm_ip = re.sub(r"\{([^}]+)\}", self.get_replacement_function(lookup), expr)
            return vm_ip
        except Exception as e:
            if strict:
                raise AnsibleError(
                    f"Error formatting ansible_host expression for VM {lookup.get('vm_name')} "
                    f"with ext_id {lookup.get('vm_ext_id')}: {e}"
                )
        return None

    def _remove_unwanted_keys(self, host_vars):
        """Remove unnecessary keys from host_vars."""
        unwanted_keys = {
            "boot_config",
            "cd_roms",
            "cluster",
            "create_time",
            "disks",
            "host",
            "nics",
            "ownership_info",
            "project",
            "update_time",
            "tenant_id",
            "links",
            "source",
            "availability_zone",
            "guest_customization",
            "guest_tools",
            "apc_config",
            "storage_config",
            "gpus",
            "serial_port",
            "protection_type",
            "pcie_devices",
            "name",
            "description",
            "ext_id",
        }
        for key in unwanted_keys:
            host_vars.pop(key, None)

    def _build_host_vars(self, vm, cluster_ext_id_name_map, strict=False):
        """
        Build a dictionary of host variables from the V4 VM response.
        Returns all VM attributes, excluding null/empty values.
        """
        # Validate VM data
        if not vm or not isinstance(vm, dict):
            raise ValueError("Invalid VM data: expected dict, got {0}".format(type(vm)))

        # Extract IP address from NICs for ansible_host
        vm_ip = None

        # Start with all VM attributes
        host_vars = {}

        # Add all attributes from VM, excluding null/empty values
        for key, value in vm.items():
            if value is None:
                continue
            if isinstance(value, (list, dict, str)) and not value:
                continue

            host_vars[key] = value

        # Add ansible_host for SSH connectivity
        vm_ip = self._extract_vm_ip(vm)
        host_vars["ansible_host"] = vm_ip

        # Convert categories to list of extId if present
        if vm.get("categories"):
            category_ext_ids = []
            for category in vm.get("categories") or []:
                if isinstance(category, dict):
                    category_ext_id = category.get("ext_id")
                    if category_ext_id:
                        category_ext_ids.append(category_ext_id)
            if category_ext_ids:
                host_vars["categories"] = category_ext_ids

        # Handle custom ansible_host
        if getattr(self, "custom_ansible_host", None) and self.custom_ansible_host.get(
            "expr"
        ):
            expr = self.custom_ansible_host.get("expr")
            vm_ip = self._resolve_custom_ansible_host(
                vm, cluster_ext_id_name_map, expr, strict
            )
            host_vars["ansible_host"] = vm_ip

        # Remove unwanted keys
        self._remove_unwanted_keys(host_vars)

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
                        "Could not evaluate filter '{0}' - {1}".format(
                            host_filter, str(e)
                        )
                    )
                return False
        return True

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)

        # Get configuration options from inventory file or environment variables
        self.nutanix_host = (
            self.get_option("nutanix_host")
            or env_fallback("NUTANIX_HOSTNAME")
            or env_fallback("NUTANIX_HOST")
        )
        self.nutanix_username = self.get_option("nutanix_username") or env_fallback(
            "NUTANIX_USERNAME"
        )
        self.nutanix_password = self.get_option("nutanix_password") or env_fallback(
            "NUTANIX_PASSWORD"
        )
        self.nutanix_port = self.get_option("nutanix_port") or env_fallback(
            "NUTANIX_PORT", "9440"
        )

        # Validate required parameters
        if not self.nutanix_host:
            raise AnsibleError(
                "nutanix_host must be provided either in inventory file or as NUTANIX_HOSTNAME environment variable or NUTANIX_HOST environment variable"
            )
        if not self.nutanix_username:
            raise AnsibleError(
                "nutanix_username must be provided either in inventory file or as NUTANIX_USERNAME environment variable"
            )
        if not self.nutanix_password:
            raise AnsibleError(
                "nutanix_password must be provided either in inventory file or as NUTANIX_PASSWORD environment variable"
            )

        self.validate_certs = self.get_option("validate_certs")
        self.fetch_all_vms = self.get_option("fetch_all_vms")
        self.page = self.get_option("page")
        self.limit = self.get_option("limit")
        self.filter = self.get_option("filter")
        self.custom_ansible_host = self.get_option("custom_ansible_host")
        self.nutanix_debug = (
            self.get_option("nutanix_debug")
            or os.environ.get("NUTANIX_DEBUG", "false").lower() == "true"
        )
        self.nutanix_log_file = self.get_option("nutanix_log_file") or os.environ.get(
            "NUTANIX_LOG_FILE"
        )

        # Determines if composed variables or groups using nonexistent variables is an error
        strict = self.get_option("strict")
        host_filters = self.get_option("filters")

        # Create mock module for SDK
        module = Mock_Module(
            self.nutanix_host,
            self.nutanix_port,
            self.nutanix_username,
            self.nutanix_password,
            self.validate_certs,
            self.fetch_all_vms,
            self.custom_ansible_host,
            self.nutanix_debug,
            self.nutanix_log_file,
        )

        # Get VM API instance
        vmm = get_vm_api_instance(module)
        clusters = get_clusters_api_instance(module)
        list_clusters = clusters.list_clusters()
        cluster_ext_id_name_map = {}
        for cluster in list_clusters.data:
            if cluster:
                cluster_dict = cluster.to_dict()
                ext_id = cluster_dict.get("ext_id")
                name = cluster_dict.get("name")
                cluster_ext_id_name_map[ext_id] = name

        # Fetch VMs
        vms = self._fetch_vms(
            vmm,
            fetch_all_vms=self.fetch_all_vms,
            page=self.page,
            limit=self.limit,
            filter=self.filter,
        )

        # Process each VM
        for vm in vms:
            if not vm:
                continue

            # Get cluster information for this VM
            cluster_ext_id = vm.get("cluster", {}).get("ext_id")
            cluster_name = cluster_ext_id_name_map.get(cluster_ext_id)
            try:
                host_vars = self._build_host_vars(vm, cluster_ext_id_name_map, strict)
            except Exception as e:
                raise AnsibleError(
                    f"Failed to build host vars for VM {vm.get('name')} with ext_id {vm.get('ext_id')}: {str(e)}"
                )

            if not self._should_add_host(host_vars, host_filters, strict):
                continue

            # Add variables to host variables
            vm_name = vm.get("name")
            vm_ext_id = vm.get("ext_id")
            owner_ext_id = vm.get("ownership_info", {}).get("owner", {}).get("ext_id")
            project_ext_id = vm.get("project", {}).get("ext_id")
            vm_description = vm.get("description")

            # Add additional info to host_vars
            host_vars["vm_name"] = vm_name
            host_vars["vm_ext_id"] = vm_ext_id
            host_vars["cluster_name"] = cluster_name
            host_vars["cluster_ext_id"] = cluster_ext_id
            if owner_ext_id is not None:
                host_vars["owner_ext_id"] = owner_ext_id
            if project_ext_id is not None:
                host_vars["project_ext_id"] = project_ext_id
            if vm_description is not None:
                host_vars["vm_description"] = vm_description

            # Create group based on cluster
            if cluster_ext_id:
                group_name = "cluster_{0}".format(cluster_ext_id.replace("-", "_"))
                self.inventory.add_group(group_name)
                self.inventory.add_child("all", group_name)
            else:
                group_name = "all"

            if vm_name:
                self.inventory.add_host(vm_name, group=group_name)
                # Set all host_vars as variables
                for key, value in host_vars.items():
                    self.inventory.set_variable(vm_name, key, value)

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

    def get_replacement_function(self, lookup):

        def repl(match):
            val_key = match.group(1).strip()
            val = lookup.get(val_key, "")
            if val_key not in lookup:
                allowed_vars = ", ".join(f"'{k}'" for k in lookup.keys())
                raise Exception(
                    "Variable '{val_key}' not found when formatting ansible_host expression. ".format(
                        val_key=val_key
                    )
                    + "Please use one of the following allowed variables: {allowed_vars}.".format(
                        allowed_vars=allowed_vars
                    )
                )
            elif val is None or val == "":
                raise Exception(
                    "Variable '{val_key}' is not defined or empty".format(
                        val_key=val_key
                    )
                )
            return val

        return repl
