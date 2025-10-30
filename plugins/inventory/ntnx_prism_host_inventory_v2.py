# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
name: ntnx_prism_host_inventory_v2
short_description: Get a list of Nutanix hosts for ansible dynamic inventory using V4 APIs.
description:
    - Get a list of Nutanix hosts for ansible dynamic inventory using V4 APIs and SDKs.
    - This plugin uses the V4 API SDK (ntnx_clustermgmt_py_client) instead of direct API calls.
version_added: "2.4.0"
notes:
    - User needs to have API View access for resources for this inventory module to work.
    - Requires ntnx_clustermgmt_py_client SDK to be installed.
author:
    - George Ghawali (@george-ghawali)
requirements:
    - "ntnx_clustermgmt_py_client"
options:
    plugin:
        description: Name of the plugin
        required: true
        choices: ['ntnx_prism_host_inventory_v2', 'nutanix.ncp.ntnx_prism_host_inventory_v2']
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
    fetch_all_hosts:
        description:
            - Set to C(True) to fetch all hosts
            - Set to C(False) to fetch specified number of hosts based on page and limit
            - If set to C(True), page and limit will be ignored
            - By default, this is set to C(False)
        default: false
        type: bool
    page:
        description:
            - Page number for pagination (starts from 0)
            - This is ignored if fetch_all_hosts is set to True
        default: 0
        type: int
    limit:
        description:
            - Number of records to retrieve per page
            - Must be between 1 and 100
            - This is ignored if fetch_all_hosts is set to True
        default: 50
        type: int
    filter:
        description:
            - OData filter expression to filter hosts
            - For example C(hostName eq 'my-host') or C(startswith(hostName, 'prod'))
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
plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false

# Fetch all hosts
plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false
fetch_all_hosts: true

# Fetch hosts with pagination
plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false
page: 0
limit: 100

# Use OData filter
plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
nutanix_host: 10.x.x.x
nutanix_username: admin
nutanix_password: password
validate_certs: false
filter: "startswith(hostName, 'prod')"

"""

import os  # noqa: E402

from ansible.errors import AnsibleError  # noqa: E402
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (
    get_clusters_api_instance,
)  # noqa: E402
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
    """Nutanix Host dynamic inventory module using V4 APIs"""

    NAME = "nutanix.ncp.ntnx_prism_host_inventory_v2"

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

    def _fetch_hosts(
        self, host_client, fetch_all_hosts=False, page=0, limit=50, filter=None
    ):
        """
        Fetch hosts from Nutanix using V4 SDK.
        Handles pagination if fetch_all_hosts is True.
        """
        hosts = []

        if fetch_all_hosts:
            # Fetch all hosts using pagination
            current_page = 0
            while True:
                try:
                    kwargs = {"_page": current_page, "_limit": 100}
                    if filter:
                        kwargs["_filter"] = filter

                    resp = host_client.list_hosts(**kwargs)
                except Exception as e:
                    raise AnsibleError(
                        "Failed to fetch hosts from PC: {0}".format(str(e))
                    )

                if resp and hasattr(resp, "data") and resp.data:
                    # Convert response objects to dictionaries
                    for item in resp.data:
                        hosts.append(strip_internal_attributes(item.to_dict()))
                else:
                    break

                # Check if all hosts have been fetched successfully
                total_available = getattr(resp.metadata, "total_available_results", 0)
                if len(hosts) >= total_available:
                    break

                current_page += 1
        else:
            # Fetch specific number of hosts based on page and limit
            try:
                kwargs = {"_page": page, "_limit": limit}
                if filter:
                    kwargs["_filter"] = filter

                resp = host_client.list_hosts(**kwargs)
            except Exception as e:
                raise AnsibleError("Failed to fetch hosts from PC: {0}".format(str(e)))

            if resp and hasattr(resp, "data") and resp.data:
                for item in resp.data:
                    hosts.append(strip_internal_attributes(item.to_dict()))

        return hosts

    def _build_host_vars(self, host):
        """
        Build a dictionary of host variables from the V4 host response.
        Returns all host attributes, excluding null/empty values.
        """
        # Validate host data
        if not host or not isinstance(host, dict):
            raise ValueError(
                "Invalid host data: expected dict, got {0}".format(type(host))
            )

        # Extract IP address for ansible_host
        host_ip = None

        # Try to get IP from hypervisor external address first
        hypervisor = host.get("hypervisor")
        if hypervisor and isinstance(hypervisor, dict):
            external_addr = hypervisor.get("external_address")
            if external_addr and isinstance(external_addr, dict):
                ipv4 = external_addr.get("ipv4")
                if ipv4 and isinstance(ipv4, dict):
                    host_ip = ipv4.get("value")

        # Fallback to controller VM addresses if hypervisor IP not found
        if not host_ip:
            controller_vm = host.get("controller_vm")
            if controller_vm and isinstance(controller_vm, dict):
                external_addr = controller_vm.get("external_address")
                if external_addr and isinstance(external_addr, dict):
                    ipv4 = external_addr.get("ipv4")
                    if ipv4 and isinstance(ipv4, dict):
                        host_ip = ipv4.get("value")

        # Start with all host attributes
        host_vars = {}

        # Add all attributes from host, excluding null/empty values
        for key, value in host.items():
            if value is None:
                continue
            if isinstance(value, (list, dict, str)) and not value:
                continue
            host_vars[key] = value

        if "host_name" in host_vars:
            host_vars["name"] = host_vars["host_name"]

        host_vars["ansible_host"] = host_ip

        cluster = host.get("cluster")
        if cluster and isinstance(cluster, dict):
            host_vars["cluster_ext_id"] = cluster.get("uuid")

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
        self.fetch_all_hosts = self.get_option("fetch_all_hosts")
        self.page = self.get_option("page")
        self.limit = self.get_option("limit")
        self.filter = self.get_option("filter")

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

        # Get Host API instance
        host_client = get_clusters_api_instance(module)

        # Fetch Hosts
        hosts = self._fetch_hosts(
            host_client,
            fetch_all_hosts=self.fetch_all_hosts,
            page=self.page,
            limit=self.limit,
            filter=self.filter,
        )

        # Process each host
        for host in hosts:
            # Skip if host data is None or empty
            if not host:
                continue

            try:
                host_vars = self._build_host_vars(host)
            except Exception as e:
                raise AnsibleError(
                    "Failed to build host vars for Host: {0}. Host data: {1}".format(
                        str(e), host
                    )
                )

            if not self._should_add_host(host_vars, host_filters, strict):
                continue

            # Add host to inventory
            host_name = host_vars.get("name")
            cluster_ext_id = host_vars.get("cluster_ext_id")

            # Create group based on cluster if available
            if cluster_ext_id:
                group_name = "cluster_{0}".format(cluster_ext_id.replace("-", "_"))
                self.inventory.add_group(group_name)
                self.inventory.add_child("all", group_name)
            else:
                group_name = "all"

            if host_name:
                self.inventory.add_host(host_name, group=group_name)
                # Set all host_vars as variables
                for key, value in host_vars.items():
                    self.inventory.set_variable(host_name, key, value)

                # Add variables created by the user's Jinja2 expressions to the host
                self._set_composite_vars(
                    self.get_option("compose"),
                    host_vars,
                    host_name,
                    strict=strict,
                )
                self._add_host_to_composed_groups(
                    self.get_option("groups"),
                    host_vars,
                    host_name,
                    strict=strict,
                )
                self._add_host_to_keyed_groups(
                    self.get_option("keyed_groups"),
                    host_vars,
                    host_name,
                    strict=strict,
                )
