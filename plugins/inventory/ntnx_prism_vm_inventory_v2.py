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
        - This plugin uses the V4 API SDK (ntnx_vmm_py_client) instead of direct API calls.
    version_added: "2.4.0"
    notes:
        - User needs to have API View access for resources for this inventory module to work.
        - Requires ntnx_vmm_py_client SDK to be installed.
    author:
        - "Nutanix Ansible Team"
    requirements:
        - "ntnx_vmm_py_client"
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['ntnx_prism_vm_inventory_v2', 'nutanix.ncp.ntnx_prism_vm_inventory_v2']
        nutanix_host:
            description: Prism central hostname or IP address
            required: false
            type: str
            env:
                - name: NUTANIX_HOST
        nutanix_username:
            description: Prism central username
            required: false
            type: str
            env:
                - name: NUTANIX_USERNAME
        nutanix_password:
            description: Prism central password
            required: false
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
                - Conforms to OData V4.01 URL conventions
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
            default: []
            elements: str
            type: list
    extends_documentation_fragment:
        - constructed
"""

EXAMPLES = r"""
# Minimal inventory file (nutanix.yml)
plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false

# Fetch all VMs
plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false
fetch_all_vms: true

# Fetch VMs with pagination
plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false
page: 0
limit: 100

# Use OData filter
plugin: nutanix.ncp.ntnx_prism_vm_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false
filter: "startswith(name, 'test_vm')"

"""

import os  # noqa: E402

from ansible.errors import AnsibleError  # noqa: E402
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable  # noqa: E402
from ..module_utils.v4.vmm.api_client import get_vm_api_instance  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


class Mock_Module:
    """Mock module to interface with V4 SDK helper functions"""

    def __init__(self, host, port, username, password, validate_certs=False):
        self.params = {
            "nutanix_host": host,
            "nutanix_port": port,
            "nutanix_username": username,
            "nutanix_password": password,
            "validate_certs": validate_certs,
        }

    def fail_json(self, msg, **kwargs):
        """Fail with a message"""
        kwargs["failed"] = True
        kwargs["msg"] = msg
        raise AnsibleError(msg)


class InventoryModule(BaseInventoryPlugin, Constructable):
    """Nutanix VM dynamic inventory module using V4 APIs"""

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
                else:
                    break

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

    def _build_host_vars(self, vm):
        """
        Build a dictionary of host variables from the V4 VM response.
        Returns all VM attributes, excluding null/empty values.
        """
        # Validate VM data
        if not vm or not isinstance(vm, dict):
            raise ValueError("Invalid VM data: expected dict, got {0}".format(type(vm)))

        # Extract IP address from NICs for ansible_host
        vm_ip = None
        nics = vm.get("nics", [])
        if nics:
            for nic in nics:
                network_info = nic.get("network_info", {})
                if not network_info:
                    continue

                # Fallback to ipv4_info (learned/DHCP IP)
                ipv4_info = network_info.get("ipv4_info")
                if ipv4_info:
                    learned_ips = ipv4_info.get("learned_ip_addresses", [])
                    if learned_ips and len(learned_ips) > 0:
                        first_ip = learned_ips[0]
                        if first_ip and first_ip.get("value"):
                            vm_ip = first_ip.get("value")
                            break

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
        host_vars["ansible_host"] = vm_ip

        # Add convenience fields
        cluster = vm.get("cluster")
        if cluster and isinstance(cluster, dict):
            host_vars["cluster_ext_id"] = cluster.get("ext_id")

        # Convert categories to list of extId if present
        if vm.get("categories"):
            category_ext_ids = []
            for category in vm.get("categories", []):
                if isinstance(category, dict):
                    category_ext_id = category.get("ext_id")
                    if category_ext_id:
                        category_ext_ids.append(category_ext_id)
            if category_ext_ids:
                host_vars["categories"] = category_ext_ids

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
        self.nutanix_host = self.get_option("nutanix_host") or os.environ.get(
            "NUTANIX_HOST"
        )
        self.nutanix_username = self.get_option("nutanix_username") or os.environ.get(
            "NUTANIX_USERNAME"
        )
        self.nutanix_password = self.get_option("nutanix_password") or os.environ.get(
            "NUTANIX_PASSWORD"
        )
        self.nutanix_port = self.get_option("nutanix_port") or os.environ.get(
            "NUTANIX_PORT", "9440"
        )

        # Validate required parameters
        if not self.nutanix_host:
            raise AnsibleError(
                "nutanix_host must be provided either in inventory file or as NUTANIX_HOST environment variable"
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
        )

        # Get VM API instance
        vmm = get_vm_api_instance(module)

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

            try:
                host_vars = self._build_host_vars(vm)
            except Exception as e:
                raise AnsibleError(
                    "Failed to build host vars for VM: {0}. VM data: {1}".format(
                        str(e), vm
                    )
                )

            if not self._should_add_host(host_vars, host_filters, strict):
                continue

            # Add host to inventory
            vm_name = host_vars.get("name")
            cluster_ext_id = host_vars.get("cluster_ext_id")

            # Create group based on cluster if available
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
