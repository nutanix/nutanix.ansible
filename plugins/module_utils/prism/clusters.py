# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism
from copy import deepcopy


class Cluster(Prism):
    def __init__(self, module):
        resource_type = "/clusters"
        super(Cluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "authorized_public_key_list": self._build_spec_public_keys,
            "timezone": self._build_spec_timezone,
            "supported_information_verbosity": self._build_spec_supported_information_verbosity,
            "redundancy_factor": self._build_spec_redundancy_factor,
            "network": self._build_spec_network,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "cluster", "spec_version": 2},
                "spec": {
                    "name": None,
                    "resources": {
                        "config": {
                            "authorized_public_key_list": []
                        }
                    }
                }
            }
        )

    def _build_spec_redundancy_factor(self, payload, redundancy_factor):
        if redundancy_factor is not None:
            payload["spec"]["resources"]["config"]["redundancy_factor"] = redundancy_factor
        return payload, None

    def _build_spec_supported_information_verbosity(self, payload, verbosity):
        if verbosity is not None:
            payload["spec"]["resources"]["config"]["supported_information_verbosity"] = verbosity
        return payload, None

    def _build_spec_timezone(self, payload, timezone):
        if timezone is not None:
            payload["spec"]["resources"]["config"]["timezone"] = timezone
        return payload, None

    def _build_spec_public_keys(self, payload, public_keys):
        if public_keys is not None:
            payload["spec"]["resources"]["config"]["authorized_public_key_list"] = public_keys
        return payload, None

    def _build_spec_network(self, payload, network):
        single_entries = ["external_ip", "fully_qualified_domain_name", "external_data_services",
                          "external_subnet", "internal_subnet", "masquerading_ip", "masquerading_port", "domain_server",
                          "nfs_subnet_whitelist", "name_server_ip_list", "ntp_server_ip_list",
                          "http_proxy_list", "http_proxy_whitelist", "default_vswitch_config", "smtp_server"]

        for single_entry in single_entries:
            if single_entry in network:
                payload["spec"]["resources"]["network"][single_entry] = network[single_entry]

        return payload, None

    def get_current_spec(self):
        config = self.module.params.get('cluster')
        if "name" in config:
            name = config["name"]
            uuid = self.get_uuid(name)
            if not uuid:
                error = "Cluster {0} not found.".format(name)
                return None, error
        elif "uuid" in config:
            uuid = config["uuid"]
        else:
            error = "Config {0} doesn't have name or uuid key".format(config)
            return None, error
        cluster_info = self.read(uuid)
        old_spec = {}
        old_spec['spec'] = cluster_info['spec']
        old_spec['api_version'] = cluster_info['api_version']
        old_spec['metadata'] = cluster_info['metadata']

        return deepcopy(old_spec)

# Helper functions


def get_cluster_uuid(config, module):
    if "name" in config:
        cluster = Cluster(module)
        name = config["name"]
        uuid = cluster.get_uuid(name)
        if not uuid:
            error = "Cluster {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
