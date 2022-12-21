# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ..entity import Entity


class Cluster(Entity):
    __BASEURL__ = "/era"

    def __init__(self, module, api_version="v0.9"):
        resource_type = "{0}/{1}/clusters".format(self.__BASEURL__, api_version)

        super(Cluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "name_prefix": self._build_spec_name_prefix,
            "cluster_ip": self._build_spec_cluster_ip,
            "cluster_credentials": self._build_spec_cluster_credentials,
            "agent_network": self._build_spec_agent_network,
            "vlan_access": self._build_spec_vlan_access,
            "storage_container": self._build_spec_storage_container,
        }

    def update(
        self,
        data=None,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
        method="PATCH",
    ):
        return super().update(
            data, uuid, endpoint, query, raise_error, no_response, timeout, method
        )

    def get_cluster_by_ip(self):
        cluster_ip = self.module.params["cluster_ip"]
        clusters = self.read()
        for cluster in clusters:
            if cluster_ip in cluster["ipAddresses"]:
                return cluster
        return None

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        endpoint = "{0}/{1}".format(key, value)
        resp = self.read(uuid=None, endpoint=endpoint)
        return resp.get("id")

    def get_cluster(self, uuid=None, name=None):
        if uuid:
            resp = self.read(uuid=uuid)
        elif name:
            endpoint = "{0}/{1}".format("name", name)
            resp = self.read(endpoint=endpoint)

            # we fetch cluster using ID again to get complete info.
            # if resp and resp.get("id"):
            #     resp = self.read(uuid=resp["id"])

        else:
            return (
                None,
                "Please provide either uuid or name for fetching cluster details",
            )

        return resp, None

    def _get_default_spec(self):
        return deepcopy(
            {
                "clusterName": "",
                "clusterIP": "",
                "storageContainer": "",
                "agentVMPrefix": "",
                "port": 9440,
                "protocol": "https",
                "clusterType": "NTNX",
                "version": "v2",
                "credentialsInfo": [],
                "agentNetworkInfo": [],
                "networksInfo": [],
            }
        )

    def get_default_update_spec(self, override_spec=None):
        spec = deepcopy(
            {
                # "username": "",
                # "password": "",
                "name": "",
                "description": "",
                "ipAddresses": [],
            }
        )
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def _build_spec_name(self, payload, name):
        if self.module.params.get("uuid"):
            payload["name"] = name
        else:
            payload["clusterName"] = name
        return payload, None

    def _build_spec_name_prefix(self, payload, prefix):
        payload["agentVMPrefix"] = prefix
        return payload, None

    def _build_spec_desc(self, payload, desc):
        if self.module.params.get("uuid"):
            payload["description"] = desc
        else:
            payload["clusterDescription"] = desc
        return payload, None

    def _build_spec_cluster_ip(self, payload, cluster_ip):
        if self.module.params.get("uuid"):
            payload["ipAddresses"] = [cluster_ip]
        else:
            payload["clusterIP"] = cluster_ip
        return payload, None

    def _build_spec_cluster_credentials(self, payload, credentials):
        if self.module.params.get("uuid"):
            payload["username"] = credentials["username"]
            payload["password"] = credentials["password"]
        else:
            payload["credentialsInfo"] = [
                {"name": "username", "value": credentials["username"]},
                {"name": "password", "value": credentials["password"]},
            ]
        return payload, None

    def _build_spec_agent_network(self, payload, agent_network):
        payload["agentNetworkInfo"] = [
            {"name": "dns", "value": ",".join(agent_network["dns_servers"])},
            {"name": "ntp", "value": ",".join(agent_network["ntp_servers"])},
        ]
        return payload, None

    def _build_spec_vlan_access(self, payload, vlans_config):
        networks_info = []
        prism_vlan = {
            "type": vlans_config["prism_vlan"]["vlan_type"],
            "networkInfo": [
                {"name": "vlanName", "value": vlans_config["prism_vlan"]["vlan_name"]},
                {"name": "staticIP", "value": vlans_config["prism_vlan"]["static_ip"]},
                {"name": "gateway", "value": vlans_config["prism_vlan"]["gateway"]},
                {
                    "name": "subnetMask",
                    "value": vlans_config["prism_vlan"]["subnet_mask"],
                },
            ],
            "accessType": ["PRISM"],
        }
        if vlans_config.get("dsip_vlan"):
            dsip_vlan = {
                "type": vlans_config["dsip_vlan"]["vlan_type"],
                "networkInfo": [
                    {
                        "name": "vlanName",
                        "value": vlans_config["dsip_vlan"]["vlan_name"],
                    },
                    {
                        "name": "staticIP",
                        "value": vlans_config["dsip_vlan"]["static_ip"],
                    },
                    {"name": "gateway", "value": vlans_config["dsip_vlan"]["gateway"]},
                    {
                        "name": "subnetMask",
                        "value": vlans_config["dsip_vlan"]["subnet_mask"],
                    },
                ],
                "accessType": ["DSIP"],
            }
            networks_info.append(dsip_vlan)
        else:
            prism_vlan["accessType"].append("DSIP")
        if vlans_config.get("dbserver_vlan"):
            dbserver_vlan = {
                "type": vlans_config["dbserver_vlan"]["vlan_type"],
                "networkInfo": [
                    {
                        "name": "vlanName",
                        "value": vlans_config["dbserver_vlan"]["vlan_name"],
                    },
                    {
                        "name": "staticIP",
                        "value": vlans_config["dbserver_vlan"]["static_ip"],
                    },
                    {
                        "name": "gateway",
                        "value": vlans_config["dbserver_vlan"]["gateway"],
                    },
                    {
                        "name": "subnetMask",
                        "value": vlans_config["dbserver_vlan"]["subnet_mask"],
                    },
                ],
                "accessType": ["DBSERVER"],
            }
            networks_info.append(dbserver_vlan)
        else:
            prism_vlan["accessType"].append("DBSERVER")
        networks_info.append(prism_vlan)

        payload["networksInfo"] = networks_info
        return payload, None

    def _build_spec_storage_container(self, payload, storage_container):
        payload["storageContainer"] = storage_container
        return payload, None


# helper functions


def get_cluster_uuid(module, config):
    uuid = ""
    if config.get("name"):
        clusters = Cluster(module)
        uuid = clusters.get_uuid(config["name"])
    elif config.get("uuid"):
        uuid = config["uuid"]
    else:
        error = "cluster config {0} doesn't have name or uuid key".format(config)
        return error, None
    return uuid, None
