# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy
from .nutanix_files import NutanixFiles
from ..prism.subnets import get_subnet_uuid
from ..prism.clusters import get_cluster_uuid


class FileServer(NutanixFiles):
    resource_type = "/config/file-servers"

    def __init__(self, module):

        super(FileServer, self).__init__(module, self.resource_type)

    def read(self, uuid=None, endpoint=None, query=None, raise_error=True, no_response=False, timeout=30, **kwargs):
        if not query:
            query = {}

        # For getting response without reserved objects info
        query["$mode"] = "pretty"
        return super().read(uuid, endpoint, query, raise_error, no_response, timeout, **kwargs)

    def update(self, data=None, uuid=None, endpoint=None, query=None, raise_error=True, no_response=False, timeout=30, method="PUT", **kwargs):
        etag = kwargs.get("etag")
        if not etag:
            return "'etag' is mandatory for update operations"

        kwargs.update({
            "additional_headers" : {
                "If-Match": etag
            }
        })
        return super().update(data, uuid, endpoint, query, raise_error, no_response, timeout, method, **kwargs)
    
    def get_file_servers_by_name(self, name):
        query = {
            "filter": "name%20eq%20'{0}'".format(name)
        }
        return self.read(query=query)

    def get_file_server_uuid(self, name, cluster_uuid):
        file_servers = self.get_file_servers_by_name(name=name)
        for file_server in file_servers.get("data", []):
            if file_server.get("clusterExtId") == cluster_uuid:
                return file_server.get("extId")
        return None

    def _get_default_spec(self):
        return deepcopy({
            "dnsDomainName": None,
            "dnsServers": [],
            "externalNetworks":[],
            "internalNetworks":[],
            "memoryGib": None,
            "name": None,
            "ntpServers": [],
            "nvmsCount": None,
            "sizeInGib": None,
            "vcpus": None,
            "version": None,
        })
    
    def get_spec(self, old_spec=None, params=None, **kwargs):
        if kwargs.get("create"):
            return self.get_create_spec(old_spec, params, **kwargs)
        elif kwargs.get("update"):
            return self.get_update_spec(old_spec, params, **kwargs)
        return super().get_spec(old_spec, params, **kwargs)

    # spec builders
    def get_create_spec(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "version": self._build_spec_version,
            "cluster": self._build_spec_cluster,
            "size_gb": self._build_spec_size_gb,
            "vms_config": self._build_spec_vms_config,
            "dns_domain_name": self._build_spec_dns_domain_name,
            "dns_servers": self._build_spec_dns_servers,
            "ntp_servers": self._build_spec_ntp_servers,
            "file_blocking_extensions": self._build_spec_file_blocking_extensions,
            "external_networks": self._build_spec_external_networks,
            "internal_networks": self._build_spec_internal_networks
        }
        return super().get_spec(old_spec, params, **kwargs)
    
    def get_update_spec(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "size_gb": self._build_spec_size_gb,
            "vms_config": self._build_spec_vms_config,
            "dns_domain_name": self._build_spec_dns_domain_name,
            "dns_servers": self._build_spec_dns_servers,
            "ntp_servers": self._build_spec_ntp_servers,
            "file_blocking_extensions": self._build_spec_file_blocking_extensions,
        }
        return super().get_spec(old_spec, params, **kwargs)

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_dns_domain_name(self, payload, dns_domain_name):
        payload["dnsDomainName"] = dns_domain_name
        return payload, None
    
    def _build_spec_version(self, payload, version):
        payload["version"] = version
        return payload, None
    
    def _build_spec_vms_config(self, payload, vm):
        payload["vcpus"] = vm.get("vcpus")
        payload["memoryGib"] = vm.get("memory_gb")
        payload["nvmsCount"] = vm.get("vms_count")
        return payload, None
    
    def _build_spec_cluster(self, payload, cluster):
        cluster_uuid, err = get_cluster_uuid(cluster, self.module)
        if err:
            return None, err
        payload["clusterExtId"] = cluster_uuid
        return payload, None

    def _build_spec_size_gb(self, payload, size):
        payload["sizeInGib"] = size
        return payload, None

    def _build_spec_dns_servers(self, payload, dns_servers):
        dns_server_specs = []
        for dns_server in dns_servers:
            dns_server_specs.append(self._get_ip_spec(dns_server))
        payload["dnsServers"] = dns_server_specs
        return payload, None

    def _build_spec_ntp_servers(self, payload, ntp_servers):
        ntp_server_specs = []
        for ntp in ntp_servers:
            spec = {}
            if ntp.get("fqdn"):
                spec["fqdn"] = {
                    "value": ntp.get("fqdn")
                }
            elif ntp.get("ip"):
                spec["ipv4"] = {
                    "value": ntp.get("ipv4")
                }
            ntp_server_specs.append(spec)
        payload["ntpServers"] = ntp_server_specs
        return payload, None

    def _build_spec_file_blocking_extensions(self, payload, file_blocking_extensions):
        payload["fileBlockingExtensions"] = file_blocking_extensions
        return payload, None

    def _build_spec_external_networks(self, payload, external_networks):
        specs = []
        cluster_config = self.module.params.get("cluster")
        if not cluster_config:
            return None, "cluster config is required for setting network"
        for network in external_networks:
            spec, err = self._build_spec_network(network, cluster=cluster_config)
            if err:
                return None, err
            specs.append(spec)
        payload["externalNetworks"] = specs
        return payload, None

    def _build_spec_internal_networks(self, payload, internal_networks):
        specs = []
        cluster_config = self.module.params.get("cluster")
        if not cluster_config:
            return None, "cluster config is required for setting network"
        
        for network in internal_networks:
            spec, err = self._build_spec_network(network, cluster=cluster_config)
            if err:
                return None, err
            specs.append(spec)
        payload["internalNetworks"] = specs
        return payload, None

    def _build_spec_network(self, network_config, cluster):
        spec = {}
        spec["isManaged"] = network_config.get("is_managed", False)

        # fetch subnet uuid
        cluster_uuid, err = get_cluster_uuid(cluster, self.module)
        if err:
            return None, err

        subnet = deepcopy(network_config.get("subnet"))
        subnet["cluster_uuid"] = cluster_uuid
        subnet_uuid, err = get_subnet_uuid(subnet, self.module)
        if err:
            return None, err
        
        spec["networkExtId"] = subnet_uuid

        # add details for unmanaged subnet
        if not spec["isManaged"]:
            protocol = network_config.get("protocol")
            if not protocol:
                return None, "Please provide protocol for network configuration"
            
            if network_config.get("virtual_ip"):
                spec["virtualIpAddress"] = self._get_protocol_based_ip_spec(network_config.get("virtual_ip"), protocol)
            
            spec["defaultGateway"] = self._get_protocol_based_ip_spec(network_config.get("default_gateway"), protocol)
            
            ip_addresses = []
            for ip_address in network_config.get("ip_addresses", []):
                ip_addresses.append(self._get_protocol_based_ip_spec(ip_address, protocol))
            spec["ipAddresses"] = ip_addresses
            
            if protocol == "ipv4":
                spec["subnetMask"] = self._get_protocol_based_ip_spec(network_config.get("netmask"), protocol)
            else:
                spec["ipv6PrefixLength"] = network_config.get("prefix_length")
        

        return spec, None

    def _get_protocol_based_ip_spec(self, ip, protocol):
        """
        This method creates spec for defining IP and protocol for v4 spec
        """
        return deepcopy({
            protocol: self._get_ip_spec(ip)
        })
    
    def _get_ip_spec(self, ip):
        """
        This method creates spec for defining IP for v4 spec
        """
        return deepcopy({
            "value": ip
        })
        
        


