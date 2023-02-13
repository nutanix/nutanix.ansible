# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

__metaclass__ = type


from ...constants import NDB
from ..clusters import Cluster, get_cluster_uuid
from ..database_engines.db_engine_factory import create_db_engine
from .profiles import Profile


class ComputeProfile(Profile):
    def __init__(self, module):
        super(ComputeProfile, self).__init__(module)
        self._type = NDB.ProfileTypes.COMPUTE

    def get_create_profile_spec(self, old_spec=None, params=None, **kwargs):

        payload, err = super().get_create_profile_spec(
            old_spec=old_spec, params=params, **kwargs
        )
        if err:
            return None, err

        compute = self.module.params.get("compute", {})
        return self._build_spec_create_profile(payload, compute)

    def get_update_version_spec(self, old_spec=None, params=None, **kwargs):
        payload = deepcopy(old_spec)

        if not params:
            params = self.module.params.get("compute")

        if params:
            payload, err = self._build_spec_update_profile(payload, params)
            if err:
                return None, err

        # remove not required fields
        if payload.get("type") is not None:
            payload.pop("type")
        if payload.get("topology") is not None:
            payload.pop("topology")
        if payload.get("versionClusterAssociation") is not None:
            payload.pop("versionClusterAssociation")

        return self.build_spec_status(payload)

    def _build_spec_create_profile(self, payload, compute=None):
        properties = payload.get("properties", [])

        property_map = {
            "vcpus": {"name": "CPUS", "default": "1"},
            "cores_per_cpu": {"name": "CORE_PER_CPU", "default": "2"},
            "memory": {"name": "MEMORY_SIZE", "default": "16"},
        }

        for key, config in property_map.items():
            name = config.get("name")
            default = config.get("default")

            # fetch value from input or use default
            val = str(compute.get(key, default))
            properties.append(self.get_property_spec(name, val))

        payload["properties"] = properties
        return payload, None

    def _build_spec_update_profile(self, payload, compute):

        properties_map = deepcopy(payload["propertiesMap"])
        if compute.get("vcpus"):
            properties_map["CPUS"] = str(compute["vcpus"])

        if compute.get("cores_per_cpu"):
            properties_map["CORE_PER_CPU"] = str(compute["cores_per_cpu"])

        if compute.get("memory"):
            properties_map["MEMORY_SIZE"] = str(compute["memory"])

        properties = payload.get("properties", [])

        # update existing properties with new values
        for prop in properties:
            prop["value"] = properties_map.get(prop["name"])

        return payload, None


class NetworkProfile(Profile):
    def __init__(self, module):
        super(NetworkProfile, self).__init__(module)
        self._type = NDB.ProfileTypes.NETWORK

    def get_create_profile_spec(self, old_spec=None, params=None, **kwargs):

        self.build_spec_methods.update({"network": self._build_spec_profile})
        return super().get_create_profile_spec(
            old_spec=old_spec, params=params, **kwargs
        )

    def get_update_version_spec(self, old_spec=None, params=None, **kwargs):
        payload = deepcopy(old_spec)

        if not params:
            params = self.module.params.get("network")

        if params:
            payload, err = self._build_spec_profile(payload, params)
            if err:
                return None, err

        # remove not required fields
        if payload.get("type") is not None:
            payload.pop("type")
        if payload.get("topology") is not None:
            payload.pop("topology")
        if payload.get("versionClusterAssociation") is not None:
            payload.pop("versionClusterAssociation")

        return self.build_spec_status(payload)

    def _build_spec_profile(self, payload, profile):
        vlans = profile.get("vlans", [])
        payload["properties"] = []
        if profile.get("topology") == "cluster" or len(vlans) > 1:
            payload, err = self._build_spec_multicluster_network_profile(payload, vlans)
            payload["properties"].append({"name": "NUM_CLUSTERS", "value": len(vlans)})
        else:
            payload, err = self._build_spec_single_cluster_network_profile(
                payload, vlans[0]
            )

        if err:
            return None, err

        enable_ip_address_selection = profile.get("enable_ip_address_selection", False)
        payload["properties"].append(
            {
                "name": "ENABLE_IP_ADDRESS_SELECTION",
                "value": str(enable_ip_address_selection).lower(),
            }
        )

        topology = profile.get("topology")
        if topology == "all":
            topology = "ALL"

        payload["topology"] = topology

        return payload, None

    def _build_spec_multicluster_network_profile(self, payload, vlans):
        _clusters = Cluster(self.module)
        clusters_uuid_name_map = _clusters.get_all_clusters_uuid_name_map()

        for i in range(len(vlans)):
            cluster_uuid, err = get_cluster_uuid(self.module, vlans[i].get("cluster"))
            if err:
                return err
            payload["properties"].append(
                self.get_property_spec("VLAN_NAME_" + str(i), vlans[i].get("vlan_name"))
            )
            payload["properties"].append(
                self.get_property_spec(
                    "CLUSTER_NAME_" + str(i), clusters_uuid_name_map[cluster_uuid]
                )
            )
            payload["properties"].append(
                self.get_property_spec("CLUSTER_ID_" + str(i), cluster_uuid)
            )

        return payload, None

    def _build_spec_single_cluster_network_profile(self, payload, vlan):
        cluster = vlan.get("cluster")
        cluster_uuid, err = get_cluster_uuid(self.module, cluster)
        if err:
            return None, err

        payload["properties"] = [
            self.get_property_spec("VLAN_NAME", vlan.get("vlan_name"))
        ]

        payload["versionClusterAssociation"] = [{"nxClusterId": cluster_uuid}]

        return payload, None


class SoftwareProfile(Profile):
    def __init__(self, module):
        super(SoftwareProfile, self).__init__(module)
        self._type = NDB.ProfileTypes.SOFTWARE

    def get_create_profile_spec(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods.update({"software": self._build_spec_profile})
        payload, err = super().get_create_profile_spec(
            old_spec=old_spec, params=params, **kwargs
        )
        if err:
            return None, err

        if payload.get("updateClusterAvailability"):
            payload.pop("updateClusterAvailability")

        return payload, None

    def get_update_profile_spec(self, old_spec=None, params=None, **kwargs):
        payload, err = super().get_update_profile_spec(old_spec, params, **kwargs)
        if err:
            return None, err

        clusters = self.module.params.get("software", {}).get("clusters", [])
        if clusters:
            payload, err = self._build_spec_clusters_availibilty(payload, clusters)
            if err:
                return None, err

        return payload, None

    def get_create_version_spec(self, old_spec=None, params=None, **kwargs):
        if not params:
            params = self.module.params.get("software")

        if not params:
            return None, "Please provide version config for creating new version"

        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)
        if err:
            return None, err

        payload["type"] = self._type

        # add new base version related properties
        payload, err = self._build_spec_version_create_properties(payload, params)
        if err:
            return None, err

        topology = self.module.params["software"].get("topology")
        if topology == "all":
            topology = "ALL"

        payload["topology"] = topology

        return payload, None

    def get_update_version_spec(self, old_spec=None, params=None, **kwargs):

        if not params:
            params = self.module.params.get("software")

        payload, err = super().get_spec(old_spec=old_spec, params=params, *kwargs)
        if err:
            return None, err

        # update version status and return
        return self.build_spec_status(payload)

    def _build_spec_profile(self, payload, profile):

        payload, err = self._build_spec_version_create_properties(
            payload, profile, base_version=True
        )
        if err:
            return None, err

        # add cluster uuids
        clusters = profile.get("clusters", [])
        if clusters:
            payload, err = self._build_spec_clusters_availibilty(payload, clusters)
            if err:
                return None, err

        topology = profile.get("topology")
        if topology == "all":
            topology = "ALL"

        payload["topology"] = topology
        return payload, None

    def _build_spec_version_create_properties(
        self, payload, version, base_version=False
    ):
        properties = payload.get("properties", [])
        if base_version:
            if version.get("name"):
                properties.append(
                    self.get_property_spec("BASE_PROFILE_VERSION_NAME", version["name"])
                )
            if version.get("desc"):
                properties.append(
                    self.get_property_spec(
                        "BASE_PROFILE_VERSION_DESCRIPTION", version["desc"]
                    )
                )

        if version.get("notes", {}).get("os"):
            properties.append(
                self.get_property_spec("OS_NOTES", version["notes"]["os"])
            )

        if version.get("notes", {}).get("db_software"):
            properties.append(
                self.get_property_spec(
                    "DB_SOFTWARE_NOTES", version["notes"]["db_software"]
                )
            )

        if version.get("db_server"):
            # importing here to avoid frozen import
            from ..db_server_vm import DBServerVM

            db_server_vm = DBServerVM(self.module)
            uuid, err = db_server_vm.get_db_server_uuid(version["db_server"])
            if err:
                return None, err
            properties.append(self.get_property_spec("SOURCE_DBSERVER_ID", uuid))

        payload["properties"] = properties
        return payload, None

    def _build_spec_clusters_availibilty(self, payload, clusters):
        _clusters = Cluster(self.module)
        spec = []
        clusters_name_uuid_map = _clusters.get_all_clusters_name_uuid_map()
        for cluster in clusters:
            uuid = ""
            if cluster.get("name"):
                uuid = clusters_name_uuid_map.get(cluster["name"])
                if not uuid:
                    return None, "Cluster with name {0} not found".format(
                        cluster["name"]
                    )
            else:
                uuid = cluster["uuid"]

            spec.append(uuid)
        payload["availableClusterIds"] = spec
        payload["updateClusterAvailability"] = True
        return payload, None

    def build_spec_status(self, payload):
        if self.module.params.get("publish"):
            payload["published"] = self.module.params.get("publish")
            payload["deprecated"] = False

        elif self.module.params.get("deprecate"):
            payload["deprecated"] = self.module.params.get("deprecate")

        return payload, None


class DatabaseParameterProfile(Profile):
    def __init__(self, module):
        self._type = NDB.ProfileTypes.DB_PARAMS
        super(DatabaseParameterProfile, self).__init__(module)

    def get_db_engine_spec(self, payload=None, params=None, **kwargs):
        engine_type = kwargs.get("engine_type")
        if not engine_type:
            engine_type = self.module.params.get("database_type")

        db_engine, err = create_db_engine(self.module, engine_type=engine_type)
        if err:
            return None, err

        engine_type = db_engine.get_type()

        config = {}
        if params:
            config = params.get(engine_type, {})

        if not payload:
            payload = {}

        if kwargs.get("create_profile"):
            payload, err = db_engine.build_spec_create_db_params_profile_properties(
                payload, config
            )
            if err:
                return None, err
        elif kwargs.get("update_version"):
            payload, err = db_engine.build_spec_update_db_params_profile_version(
                payload, config
            )
            if err:
                return None, err

        return payload, err

    def get_create_profile_spec(self, old_spec=None, params=None, **kwargs):
        payload, err = super().get_create_profile_spec(old_spec, params, **kwargs)
        if err:
            return None, err

        if not params:
            params = self.module.params.get("database_parameter", {})
        return self.get_db_engine_spec(
            payload=payload, params=params, create_profile=True
        )

    def get_update_version_spec(self, old_spec=None, params=None, **kwargs):
        payload = deepcopy(old_spec)

        if not params:
            params = self.module.params.get("database_parameter")
        
        kwargs["update_version"] = True
        payload, err = self.get_db_engine_spec(
            payload=payload, params=params, **kwargs
        )
        if err:
            return None, err

        if payload.get("type") is not None:
            payload.pop("type")
        if payload.get("topology") is not None:
            payload.pop("topology")
        if payload.get("versionClusterAssociation") is not None:
            payload.pop("versionClusterAssociation")
        return self.build_spec_status(payload)


# Helper methods for getting profile type objects


def get_profile_type(module):
    profile_types = NDB.ProfileTypes.ALL

    for type in profile_types:
        if type in module.params:
            return type, None

    return None, "Input doesn't conatains config for allowed profile types of databases"


def get_profile_type_obj(module, profile_type=None):  # -> tuple[Profile, str]:
    profiles = {
        "software": SoftwareProfile,
        "network": NetworkProfile,
        "compute": ComputeProfile,
        "database_parameter": DatabaseParameterProfile,
    }

    if not profile_type:
        profile_type, err = get_profile_type(module)
        if err:
            return None, err

    if profile_type in profiles:
        return profiles[profile_type](module), None
    else:
        return None, "Profile type {0} is not supported".format(profile_type)
