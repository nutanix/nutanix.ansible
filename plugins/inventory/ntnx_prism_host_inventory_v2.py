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
    version_added: "2.4.0"
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
                - Used in List Hosts API call to filter hosts
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
                - Used locally to filter hosts after they are fetched from the API.
            default: []
            elements: str
            type: list
    extends_documentation_fragment:
        - constructed
        - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
# Minimal inventory file (nutanix.yml)
- plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false

# Fetch all hosts
- plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  fetch_all_hosts: true

# Fetch hosts with pagination
- plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  page: 0
  limit: 80

# Use OData filter
- plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  filter: "startswith(hostName, 'prod')"

# using compose for defining new host variables
- plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  compose:
    ansible_user: "'ansible_user'"
    memory_gb: memory_size_bytes / 1073741824 if memory_size_bytes else 0
    cpu_frequency_ghz: cpu_frequency_hz / 1000000000 if cpu_frequency_hz else 0

# using groups for defining new host groups
- plugin: nutanix.ncp.ntnx_prism_host_inventory_v2
  nutanix_host: 10.x.x.x
  nutanix_username: admin
  nutanix_password: password
  validate_certs: false
  groups:
    high_memory: (memory_size_bytes / 1073741824) > 100 # > 100GB
    low_memory: (memory_size_bytes / 1073741824) <= 100 # <= 100GB
"""

import json  # noqa: E402
import os  # noqa: E402
import tempfile  # noqa: E402

from ansible.errors import AnsibleError  # noqa: E402
from ansible.module_utils.basic import env_fallback  # noqa: E402
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable  # noqa: E402

from ..module_utils.constants import DEFAULT_LOG_FILE  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


class Mock_Module:

    def __init__(
        self,
        hostname,
        port,
        username,
        password,
        validate_certs=False,
        fetch_all_hosts=False,
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
            "fetch_all_hosts": fetch_all_hosts,
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

    def _remove_unwanted_keys(self, host_vars):
        """Remove unnecessary keys from host_vars."""
        unwanted_keys = {
            "boot_time_usecs",
            "cluster",
            "controller_vm",
            "disk",
            "ext_id",
            "gpu_list",
            "hypervisor",
            "tenant_id",
            "links",
            "key_management_device_to_cert_status",
        }
        for key in unwanted_keys:
            host_vars.pop(key, None)

    def extract_ip_address_from_external(self, external_addr):
        if not external_addr or not isinstance(external_addr, dict):
            return None
        ipv4 = external_addr.get("ipv4", {})
        if ipv4 and isinstance(ipv4, dict) and ipv4.get("value"):
            return ipv4.get("value")
        ipv6 = external_addr.get("ipv6", {})
        if ipv6 and isinstance(ipv6, dict) and ipv6.get("value"):
            return ipv6.get("value")
        return None

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
        host_vars = {}

        # Try to get IP from hypervisor external address first
        hypervisor = host.get("hypervisor", {})
        external_addr = hypervisor.get("external_address", {})
        hypervisor_ip = self.extract_ip_address_from_external(external_addr)
        if hypervisor_ip:
            host_vars["hypervisor_ip"] = hypervisor_ip

        # Set controller VM IP address
        controller_vm = host.get("controller_vm", {})
        external_addr = controller_vm.get("external_address", {})
        controller_vm_ip = self.extract_ip_address_from_external(external_addr)
        if controller_vm_ip:
            host_vars["controller_vm_ip"] = controller_vm_ip

        # Set ipmi ip address
        ipmi = host.get("ipmi")
        if ipmi and isinstance(ipmi, dict):
            ip_address = ipmi.get("ip")
            if ip_address and isinstance(ip_address, dict):
                ipv4 = ip_address.get("ipv4")
                if ipv4 and isinstance(ipv4, dict):
                    host_vars["ipmi_ip"] = ipv4.get("value")

        # Start with all host attributes

        # Add all attributes from host, excluding null/empty values
        for key, value in host.items():
            if value is None:
                continue
            if isinstance(value, (list, dict, str)) and not value:
                continue
            host_vars[key] = value

        # Add ansible_host for SSH connectivity
        host_vars["ansible_host"] = host_vars.get("hypervisor_ip")

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
        self.fetch_all_hosts = self.get_option("fetch_all_hosts")
        self.page = self.get_option("page")
        self.limit = self.get_option("limit")
        self.filter = self.get_option("filter")
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
            self.nutanix_debug,
            self.nutanix_log_file,
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
                    f"Failed to build host vars for Host {host.get('host_name')} with ext_id {host.get('ext_id')}: {str(e)}"
                )

            if not self._should_add_host(host_vars, host_filters, strict):
                continue

            # Add variables to host variables
            host_name = host.get("host_name")
            host_ext_id = host.get("ext_id")
            cluster_ext_id = host.get("cluster", {}).get("uuid")
            cluster_name = host.get("cluster", {}).get("name")

            # Add additional info to host_vars
            host_vars["host_name"] = host_name
            host_vars["host_ext_id"] = host_ext_id
            host_vars["cluster_name"] = cluster_name
            host_vars["cluster_ext_id"] = cluster_ext_id

            # Create group based on cluster
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
