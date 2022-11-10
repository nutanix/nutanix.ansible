# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy


__metaclass__ = type


from .nutanix_database import NutanixDatabase
from ..constants import NDB
from .clusters import Cluster, get_cluster_uuid



class Profile(NutanixDatabase):
    types = ["Database_Parameter", "Compute", "Network", "Software"]

    def __init__(self, module):
        resource_type = "/profiles"
        super(Profile, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "compute": self._build_spec_compute,
            "db_params": self._build_spec_db_params,
            "network": self._build_spec_network,
            "software": self._build_spec_software,
            "database_type": self._build_spec_database_type
        }

    def get_profile_uuid(self, type, name):
        if type not in self.types:
            return None, "{0} is not a valid type. Allowed types are {1}".format(
                type, self.types
            )
        query = {"type": type, "name": name}
        resp = self.read(query=query)
        uuid = resp.get("id")
        return uuid

    def read(
        self,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        if uuid:
            if not query:
                query = {}
            query["id"] = uuid
        return super().read(
            uuid=None,
            endpoint=endpoint,
            query=query,
            raise_error=raise_error,
            no_response=no_response,
            timeout=timeout,
        )

    def get_profile_by_version(self, uuid, version_id="latest"):
        endpoint = "{0}/versions/{1}".format(uuid, version_id)
        resp = self.read(endpoint=endpoint)
        return resp

    def get_profiles(self, uuid=None, name=None, type=None):
        if name or uuid:
            query = {}
            if name:
                query["name"] = name
            else:
                query["id"] = uuid

            if type:
                query["type"] = type

            resp = self.read(query=query)
        elif type:
            query = {"type": type}
            resp = self.read(query=query)
            if not resp:
                return None, "Profiles with type {0} not found".format(type)
        else:
            return (
                None,
                "Please provide uuid, name or profile type for fetching profile details",
            )

        return resp, None

    def get_all_name_uuid_map(self, type=None):
        if type:
            query = {"type": type}

        name_uuid_map = {}
        resp = self.read(query=query)
        if not isinstance(resp, list):
            return None, "Invalid response type obtained from NDB server"

        for entity in resp:
            name_uuid_map[entity["name"]] = entity["id"]

        return name_uuid_map, None
    def _get_default_spec(self):
        return deepcopy(
            {
                "type": "",
                "engineType": "",
                "systemProfile": False,
                "properties": [],
                "name": "",
                "description": "",
            }
        )
    
    def _get_property_spec(self, name, value):
        return deepcopy({
            "name": name,
            "value": value
        })

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None
    
    def _build_spec_database_type(self, payload, type):
        if not self.module.params.get("compute"):
            payload["engineType"] = type + "_database"
        return payload, None

    def _build_spec_compute(self, payload, compute):
        properties = deepcopy(payload["properties"])

        # create properties key value map w.r.t to api spec arguments
        props_key_value_map = {}
        if compute.get("vcpus"):
            props_key_value_map["CPUS"] = compute["vcpus"]

        if compute.get("cores_per_cpu"):
            props_key_value_map["CORE_PER_CPU"] = str(compute["cores_per_cpu"])

        if compute.get("memory"):
            props_key_value_map["MEMORY_SIZE"] = str(compute["memory"])

        # update existing properties with new values
        for prop in properties:
            if props_key_value_map.get(prop["name"]):
                prop["value"] = props_key_value_map[prop["name"]]

                # remove property from map
                props_key_value_map.pop(prop["name"])

        # add new properties if required
        for key, val in props_key_value_map.items():
            spec = {"name": key, "value": val}
            properties.append(spec)

        payload["properties"] = properties
        payload["type"] = NDB.ProfileTypes.COMPUTE

        return payload, None

    def _build_spec_software(self, payload, software):
        return payload, None

    def _build_spec_db_params(self, payload, db_params):
        return payload, None

    def _build_spec_network(self, payload, network):
        vlans = network.get("vlans", [])
        payload["properties"] = payload.get("properties", [])
        if network.get("topology") == "cluster" or len(vlans)>1:
            payload, err = self._build_spec_multicluster_network_profile(payload, vlans)
            payload["properties"].append({
                "name": "NUM_CLUSTERS",
                "value": len(vlans)
            })
        else:
            payload, err = self._build_spec_single_cluster_network_profile(payload, vlans[0])
        
        if err:
            return None, err

        enable_ip_address_selection = network.get("enable_ip_address_selection", False)
        payload["properties"].append({
            "name": "ENABLE_IP_ADDRESS_SELECTION",
            "value": enable_ip_address_selection
        })

        topology = network.get("topology")
        if topology == "all":
            topology = "ALL"
        
        payload["topology"] = topology
        payload["type"] = NDB.ProfileTypes.NETWORK


        return payload, None

    def _build_spec_multicluster_network_profile(self, payload, vlans):
        _clusters = Cluster(self.module)
        clusters_uuid_name_map = _clusters.get_all_clusters_uuid_name_map()

        for i in range(len(vlans)):
            cluster_uuid, err = get_cluster_uuid(self.module, vlans[i].get("cluster"))
            if err:
                return err
            payload["properties"].append(self._get_property_spec("VLAN_NAME_"+str(i), vlans[i].get("vlan_name")))
            payload["properties"].append(self._get_property_spec("CLUSTER_NAME_"+str(i), clusters_uuid_name_map[cluster_uuid]))
            payload["properties"].append(self._get_property_spec("CLUSTER_ID_"+str(i), cluster_uuid))

        return payload, None

    def _build_spec_single_cluster_network_profile(self, payload, vlan):
        cluster = vlan.get("cluster")
        cluster_uuid, err = get_cluster_uuid(self.module, cluster)
        if err:
            return None, err
        payload["properties"] = [self._get_property_spec("VLAN_NAME", vlan.get("vlan_name"))]

        payload["versionClusterAssociation"] = [
            {
                "nxClusterId": cluster_uuid
            }
        ]

        return payload, None

# helper functions


def get_profile_uuid(module, type, config):
    uuid = ""
    if config.get("name"):
        profiles = Profile(module)
        uuid = profiles.get_profile_uuid(type, config["name"])
    elif config.get("uuid"):
        uuid = config["uuid"]
    else:
        error = "Profile config {0} doesn't have name or uuid key".format(config)
        return error, None
    return uuid, None
