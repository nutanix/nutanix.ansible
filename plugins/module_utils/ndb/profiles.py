# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy


__metaclass__ = type


from .nutanix_database import NutanixDatabase
from ..constants import NDB
from .clusters import Cluster, get_cluster_uuid
from .db_servers import get_db_server_uuid

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
            "database_type": self._build_spec_database_type,
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
    
    def create_version(self, uuid, data):
        endpoint = "versions"
        resp = self.update(uuid=uuid, endpoint=endpoint, data=data, method="POST")
        return resp
    
    def delete_version(self, profile_uuid, version_uuid):
        endpoint = "versions/{0}".format(version_uuid)
        resp = self.delete(uuid=profile_uuid, endpoint=endpoint, data={})
        return resp
    
    def update_version(self, profile_uuid, version_uuid, data):
        endpoint = "versions/{0}".format(version_uuid)
        resp = self.update(uuid=profile_uuid, endpoint=endpoint, data=data)
        return resp

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

    def get_update_profile_spec(self, old_spec=None):
        payload = {}
        payload["name"] = self.module.params.get("name", old_spec.get("name"))
        payload["description"] = self.module.params.get("desc", old_spec.get("description"))
        return payload

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
        return deepcopy({"name": name, "value": value})

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

        version_config = software.get("version")
        properties, err = self._build_software_version_create_properties(version_config, base_version=True)        
        if err:
            return None, err
        
        payload["properties"] = properties
        
        cluster_uuids = []
        for cluster in software.get("clusters", []):
            uuid, err = get_cluster_uuid(self.module, cluster)
            if err:
                return err
            cluster_uuids.append(uuid)
        
        payload["availableClusterIds"] = cluster_uuids

        payload["type"] = NDB.ProfileTypes.SOFTWARE
        topology = software.get("topology")
        if topology == "all":
            topology = "ALL"

        payload["topology"] = topology
        return payload, None

    def _build_spec_db_params(self, payload, db_params):
        database_type = self.module.params.get("database_type")
        if not database_type:
            return None, "'database_type' is required for creating db params spec"

        properties_spec_builder, err = self._db_params_properties_spec_build_methods(
            database_type
        )
        if err:
            return None, err

        config = db_params.get(database_type)
        if not config:
            return (
                None,
                "Database parameters config not found for database type '{0}'".format(
                    database_type
                ),
            )

        payload["properties"] = properties_spec_builder(config)
        payload["type"] = NDB.ProfileTypes.DB_PARAMS
        return payload, None

    def _build_spec_network(self, payload, network):
        vlans = network.get("vlans", [])
        payload["properties"] = payload.get("properties", [])
        if network.get("topology") == "cluster" or len(vlans) > 1:
            payload, err = self._build_spec_multicluster_network_profile(payload, vlans)
            payload["properties"].append({"name": "NUM_CLUSTERS", "value": len(vlans)})
        else:
            payload, err = self._build_spec_single_cluster_network_profile(
                payload, vlans[0]
            )

        if err:
            return None, err

        enable_ip_address_selection = network.get("enable_ip_address_selection", False)
        payload["properties"].append(
            {
                "name": "ENABLE_IP_ADDRESS_SELECTION",
                "value": enable_ip_address_selection,
            }
        )

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
            payload["properties"].append(
                self._get_property_spec(
                    "VLAN_NAME_" + str(i), vlans[i].get("vlan_name")
                )
            )
            payload["properties"].append(
                self._get_property_spec(
                    "CLUSTER_NAME_" + str(i), clusters_uuid_name_map[cluster_uuid]
                )
            )
            payload["properties"].append(
                self._get_property_spec("CLUSTER_ID_" + str(i), cluster_uuid)
            )

        return payload, None

    def _build_spec_single_cluster_network_profile(self, payload, vlan):
        cluster = vlan.get("cluster")
        cluster_uuid, err = get_cluster_uuid(self.module, cluster)
        if err:
            return None, err
        payload["properties"] = [
            self._get_property_spec("VLAN_NAME", vlan.get("vlan_name"))
        ]

        payload["versionClusterAssociation"] = [{"nxClusterId": cluster_uuid}]

        return payload, None

    def _db_params_properties_spec_build_methods(self, database_type):
        """
        This routine returns properties spec builder method for database parameter profile
        creation as per database type
        """
        methods = {
            "postgres": self._build_spec_postgres_db_params_properties,
        }
        if methods.get(database_type):
            return methods[database_type], None
        else:
            return (
                None,
                "Properties spec build method for database type '{0}' not found".format(
                    database_type
                ),
            )

    def _build_spec_postgres_db_params_properties(self, config):

        # map of property key with defaults
        props = {
            "max_connections": 100,
            "max_replication_slots": 10,
            "effective_io_concurrency": 1,
            "timezone": "UTC",
            "max_prepared_transactions": 0,
            "max_locks_per_transaction": 64,
            "max_wal_senders": 10,
            "max_worker_processes": 8,
            "checkpoint_completion_target": 0.5,
            "autovacuum": "on",
            "autovacuum_freeze_max_age": 200000000,
            "autovacuum_vacuum_threshold": 50,
            "autovacuum_vacuum_scale_factor": 0.2,
            "autovacuum_work_mem": -1,
            "autovacuum_max_workers": 3,
            "wal_buffers": -1,
            "synchronous_commit": "on",
            "random_page_cost": 4,
            "wal_keep_segments": 700,
        }

        # map of property key with defaults and units
        props_with_units = {
            "min_wal_size": {"default": 80, "unit": "MB"},
            "max_wal_size": {"default": 1, "unit": "GB"},
            "checkpoint_timeout": {"default": 5, "unit": "min"},
            "autovacuum_vacuum_cost_delay": {"default": 2, "unit": "ms"},
        }

        properties = []

        # add specs for normal properties
        for prop, default in props.items():
            properties.append(self._get_property_spec(prop, config.get(prop, default)))

        # add specs for properties with units
        for prop, val in props_with_units.items():
            prop_value = str(config.get(prop, val.get(default))) + val.get("unit", "")
            properties.append(self._get_property_spec(prop, prop_value))

        return properties

    def _build_software_version_create_properties(self, version, base_version=False):
        properties = []
        if base_version:
            if version.get("name"):
                properties.append(self._get_property_spec("BASE_PROFILE_VERSION_NAME", version["name"]))
            if version.get("desc"):
                properties.append(self._get_property_spec("BASE_PROFILE_VERSION_DESCRIPTION", version["desc"]))

        if version.get("notes", {}).get("os"):
            properties.append(self._get_property_spec("OS_NOTES", version["notes"]["os"]))

        if version.get("notes", {}).get("db_software"):
            properties.append(self._get_property_spec("DB_SOFTWARE_NOTES", version["notes"]["db_software"]))

        if version.get("db_server"):
            uuid, err = get_db_server_uuid(self.module, version["db_server"])
            if err:
                return None, err
            properties.append(self._get_property_spec("SOURCE_DBSERVER_ID", uuid))

        return properties, None

    def build_software_version_create_spec(self, version):
        payload = self._get_default_spec()
        
        if not version.get("db_server") or not version.get("name"):
            return None, "'db_server' and 'name' are required fields for creating new software profile version."
        
        payload["name"] = version["name"]
        if version.get("desc"):
            payload["description"] = version["desc"]

        properties, err = self._build_software_version_create_properties(version, base_version=False)
        if err:
            return None, err 
        payload["properties"] = properties

        payload["type"] = NDB.ProfileTypes.SOFTWARE

        payload, err = self._build_spec_database_type(payload, self.module.params.get("database_type"))
        if err:
            return err
        
        topology = self.module.params["software"].get("topology")
        if topology == "all":
            topology = "ALL"

        payload["topology"] = topology
        return payload, None

    def build_software_version_update_spec(self, version, old_spec):
        payload = {}
        payload["name"] = version.get("name", old_spec.get("name"))
        payload["description"] = version.get("desc", old_spec.get("description", ""))
        payload["published"] = self.module.params.get("publish", old_spec.get("published"))
        payload["deprecated"] = version.get("deprecate", old_spec.get("deprecated"))

        # when publishing deprecated field needs to be reset
        if self.module.params.get("publish"):
            payload["deprecated"] = False

        return payload
        


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
