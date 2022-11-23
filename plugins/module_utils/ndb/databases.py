# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ..constants import NDB as NDB_CONSTANTS
from .clusters import get_cluster_uuid, Cluster
from .db_servers import get_db_server_uuid
from .nutanix_database import NutanixDatabase
from .profiles import Profile, get_profile_uuid
from .slas import get_sla_uuid
from .tags import Tag

__metaclass__ = type


class Database(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/databases"
        super(Database, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "auto_tune_staging_drive": self._build_spec_auto_tune_staging_drive,
            "db_params_profile": self._build_spec_db_params_profile,
            "db_vm": self._build_spec_db_vm,
            "db_server_cluster": self._build_spec_db_server_cluster,
            "time_machine": self._build_spec_time_machine,
            "postgres": self._build_spec_postgres,
            "tags": self._build_spec_tags,
        }

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        query = {"value-type": key, "value": value}
        resp = self.read(query=query)

        if not resp:
            return None, "Database instance with name {0} not found.".format(value)

        uuid = resp[0].get("id")
        return uuid, None

    def create(
        self,
        data=None,
        endpoint=None,
        query=None,
        method="POST",
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        endpoint = "provision"
        return super().create(
            data, endpoint, query, method, raise_error, no_response, timeout
        )

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

    def get_database(self, name=None, uuid=None):
        default_query = {"detailed": True}
        if uuid:
            resp = self.read(uuid=uuid, query=default_query)
        elif name:
            query = {"value-type": "name", "value": name}
            query.update(deepcopy(default_query))
            resp = self.read(query=query)
            if not resp:
                return None, "Database with name {0} not found".format(name)
            if isinstance(resp, list):
                resp = resp[0]
                return resp, None
        else:
            return (
                None,
                "Please provide either uuid or name for fetching database details",
            )

        return resp, None

    def _get_default_spec(self):
        return deepcopy(
            {
                "databaseType": None,
                "name": None,
                "dbParameterProfileId": None,
                "timeMachineInfo": {
                    "name": None,
                    "slaId": None,
                    "schedule": {},
                    "autoTuneLogDrive": True,
                },
                "actionArguments": [],
                "nodes": [],
                "nodeCount": 1,
                "clustered": False,
                "autoTuneStagingDrive": True,
                "tags": [],
            }
        )

    def get_default_update_spec(self, override_spec=None):
        spec = deepcopy(
            {
                "name": None,
                "description": None,
                "tags": [],
                "resetTags": True,
                "resetName": True,
                "resetDescription": True,
            }
        )
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def get_default_delete_spec(self):
        return deepcopy(
            {
                "delete": False,
                "remove": False,
                "deleteTimeMachine": False,
                "deleteLogicalCluster": True,
            }
        )
    
    def _get_properties_spec(self, name, value):
        spec = {
            "name": name,
            "value": value
        }
        return spec

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["databaseDescription"] = desc
        return payload, None

    def _build_spec_auto_tune_staging_drive(self, payload, value):
        payload["autoTuneStagingDrive"] = value
        return payload, None

    def _build_spec_db_params_profile(self, payload, db_params_profile):
        uuid, err = get_profile_uuid(
            self.module, "Database_Parameter", db_params_profile
        )
        if err:
            return None, err

        payload["dbParameterProfileId"] = uuid
        return payload, None

    def _build_spec_software_profile(self, payload, software_profile):
        uuid, err = get_profile_uuid(
                self.module, "Software", software_profile
        )
        if err:
            return None, err

        payload["softwareProfileId"] = uuid
        if software_profile.get("version_id"):
            payload["softwareProfileVersionId"] = software_profile["software_profile"][
                "version_id"
            ]
        else:
            profiles = Profile(self.module)
            profile = profiles.read(uuid)
            payload["softwareProfileId"] = uuid
            payload["softwareProfileVersionId"] = profile[
                "latestVersionId"
            ]
        
        return payload, None

    def _build_spec_db_vm(self, payload, db_vm):
        if db_vm.get("use_registered_server"):

            uuid, err = get_db_server_uuid(self.module, db_vm["use_registered_server"])
            if err:
                return None, err

            payload["createDbserver"] = False
            payload["dbserverId"] = uuid
            payload["nodes"] = [{"properties": [], "dbserverId": uuid}]

        else:
            vm_config = db_vm["create_new_server"]

            # set compute profile
            uuid, err = get_profile_uuid(
                self.module, "Compute", vm_config["compute_profile"]
            )
            if err:
                return None, err
            payload["computeProfileId"] = uuid

            # set software profile
            payload, err = self._build_spec_software_profile(payload, vm_config["software_profile"])
            if err:
                return None, err

            # set network prfile
            uuid, err = get_profile_uuid(
                self.module, "Network", vm_config["network_profile"]
            )
            if err:
                return None, err

            payload["nodes"] = [
                {
                    "properties": [],
                    "vmName": vm_config["name"],
                    "networkProfileId": uuid,
                }
            ]
            payload["networkProfileId"] = uuid

            # set cluster config
            uuid, err = get_cluster_uuid(self.module, vm_config["cluster"])
            if err:
                return None, err
            payload["nxClusterId"] = uuid

            # set other params
            payload["sshPublicKey"] = vm_config["pub_ssh_key"]
            payload["vmPassword"] = vm_config["password"]
            payload["createDbserver"] = True

        return payload, None

    def _build_spec_db_server_cluster(self, payload, db_server_cluster):
        if db_server_cluster.get("new_cluster"):
            
            # basic validations
            if not db_server_cluster.get("new_cluster").get("name"):
                return None, "'name' is required for new db servers cluster"

            server_cluster_config = db_server_cluster["new_cluster"]
            vms = server_cluster_config.get("vms", [])
            if len(vms)<1:
                return None, "Atleast one vm is required for creating cluster of database servers"

            # get compute profile
            compute_profile_uuid, err = get_profile_uuid(
                self.module, "Compute", server_cluster_config["compute_profile"]
            )
            if err:
                return None, err
            
            # get network prfile
            network_profile_uuid, err = get_profile_uuid(
                self.module, "Network", server_cluster_config["network_profile"]
            )
            if err:
                return None, err
            
            # get archive log destination link
            archive_log_destination = server_cluster_config.get("archive_log_destination", "")


            # get cluster uuid map to assign cluster uuid for each node vm
            clusters = Cluster(self.module)
            clusters_name_uuid_map = clusters.get_all_clusters_name_uuid_map()

            nodes = payload.get("nodes", [])
            for vm in vms:
                spec = {
                    "properties": []
                }

                # set vm properties
                if vm.get("role", False):
                    spec["properties"].append(self._get_properties_spec("role", vm["role"]))

                if vm.get("failover_mode"):
                    spec["properties"].append(self._get_properties_spec("failover_mode", vm["failover_mode"]))
                
                if vm.get("node_type"):
                    spec["properties"].append(self._get_properties_spec("node_type", vm["node_type"]))

                spec["properties"].append(self._get_properties_spec("remote_archive_destination", archive_log_destination))
                
                # set profiles
                spec["networkProfileId"] = network_profile_uuid
                spec["computeProfileId"] = compute_profile_uuid

                # set cluster uuid using clusters_name_uuid_map
                if server_cluster_config.get("cluster"):
                    
                    uuid = ""
                    if server_cluster_config["cluster"].get("name"):
                        if clusters_name_uuid_map.get(server_cluster_config["cluster"]["name"]):
                            uuid = clusters_name_uuid_map[server_cluster_config["cluster"]["name"]]
                        else:
                            return None, "NDB cluster with name '{0}' not found".format(server_cluster_config["cluster"]["name"])

                    elif server_cluster_config["cluster"].get("uuid"):
                        uuid = server_cluster_config["cluster"]["uuid"]
                    
                    spec["nxClusterId"] = uuid
                    
                else:
                    return None, "Cluster details is required for every db server vm node"
                
                nodes.append(spec)
                
            payload["nodes"] = nodes
            payload["nodeCount"] = len(payload["nodes"])
            payload["createDbserver"] = True
            payload["clustered"] = True

            # set software profile
            payload, err = self._build_spec_software_profile(payload, server_cluster_config["software_profile"])
            if err:
                return None, err
            
            # set ssh key and vm password
            if server_cluster_config.get("pub_ssh_key"):
                payload["sshPublicKey"] = server_cluster_config["pub_ssh_key"]
            
            if server_cluster_config.get("ndb_user_password"):
                payload["vmPassword"] = server_cluster_config["ndb_user_password"]

            # set required action arguments
            action_arguments = payload.get("actionArguments", [])
            action_arguments.append(self._get_properties_spec("cluster_name", server_cluster_config.get("name")))
            action_arguments.append(self._get_properties_spec("cluster_description", server_cluster_config.get("desc")))
        
        return payload, None

    def _build_spec_time_machine(self, payload, time_machine):

        # set sla uuid
        sla_uuid, err = get_sla_uuid(self.module, time_machine["sla"])
        if err:
            return None, err

        time_machine_spec = {}

        if self.module.params.get("ha_instance", False):
            clusters = []
            for cluster in time_machine.get("clusters", []):
                uuid, err = get_cluster_uuid(self.module, cluster)
                if err:
                    return None, err
                clusters.append(uuid)
            
            time_machine_spec["slaDetails"] = {
                "primarySla": {
                    "slaId": sla_uuid,
                    "nxClusterIds": clusters
                }
            }

        else:
            time_machine_spec["slaId"] = sla_uuid

        schedule = time_machine.get("schedule")
        schedule_spec = {}
        if schedule.get("daily"):

            time = schedule["daily"].split(":")
            if len(time) != 3:
                return None, "Daily snapshot schedule not in HH:MM:SS format."

            schedule_spec["snapshotTimeOfDay"] = {
                "hours": int(time[0]),
                "minutes": int(time[1]),
                "seconds": int(time[2]),
            }

        if schedule.get("weekly"):
            schedule_spec["weeklySchedule"] = {
                "enabled": True,
                "dayOfWeek": schedule["weekly"],
            }

        if schedule.get("monthly"):
            schedule_spec["monthlySchedule"] = {
                "enabled": True,
                "dayOfMonth": schedule["monthly"],
            }

            # set quaterly and yearly as they are dependent on monthly
            if schedule.get("quaterly"):
                schedule_spec["quartelySchedule"] = {
                    "enabled": True,
                    "startMonth": schedule["quaterly"],
                    "dayOfMonth": schedule.get("monthly"),
                }

            if schedule.get("yearly"):
                schedule_spec["yearlySchedule"] = {
                    "enabled": True,
                    "month": schedule["yearly"],
                    "dayOfMonth": schedule.get("monthly"),
                }

        if schedule.get("log_catchup") or schedule.get("snapshots_per_day"):
            schedule_spec["continuousSchedule"] = {
                "enabled": True,
                "logBackupInterval": schedule.get("log_catchup"),
                "snapshotsPerDay": schedule.get("snapshots_per_day"),
            }

        time_machine_spec["schedule"] = schedule_spec
        time_machine_spec["name"] = time_machine["name"]
        time_machine_spec["description"] = time_machine.get("desc", "")
        time_machine_spec["autoTuneLogDrive"] = time_machine.get("auto_tune_log_drive")
        payload["timeMachineInfo"] = time_machine_spec
        return payload, None

    def _build_spec_ha_proxy(self, payload, ha_proxy):

        # validations
        if not ha_proxy.get("cluster"):
            return None, "cluster details is required for ha proxy"
        
        if not ha_proxy.get("name"):
            return None, "'name' is required for ha proxy"

        # add action arguments
        action_arguments = payload.get("actionArguments", [])
        
        action_arguments.append({
            "name": "provision_virtual_ip",
            "value": ha_proxy.get("provision_virtual_ip", False)
        })

        if ha_proxy.get("write_port"):
            action_arguments.append({
                "name": "proxy_write_port",
                "value": ha_proxy["write_port"]
            })
        
        if ha_proxy.get("read_port"):
            action_arguments.append({
                "name": "proxy_read_port",
                "value": ha_proxy["read_port"]
            })
        
        action_arguments.append({
            "name": "deploy_haproxy",
            "value": True
        })

        payload["actionArguments"] = action_arguments

        # add HA proxy vm details
        nodes = payload.get("nodes", [])
        node_spec = {
            "properties": {
                "name": "node_type",
                "value": "haproxy"
            }
        }

        uuid, err = get_cluster_uuid(self.module, ha_proxy.get("cluster"))
        if err:
            return None, err

        node_spec["nxClusterId"] = uuid
        node_spec["vmName"] = ha_proxy["name"]
        nodes.append(node_spec)

        payload["nodes"] = nodes
        payload["nodeCount"] = len(payload["nodes"])
        return payload, None
        
        
    def _build_spec_postgres(self, payload, postgres):
        action_arguments = payload.get("actionArguments", [])

        # map of action arguments fields to their default value
        # these are common action arguments for both HA and single instance database
        # 'args' map is used for creating action arguments spec further
        args = {
            "listener_port": "",
            "allocate_pg_hugepage": False,
            "cluster_database": False,
            "db_password": "",
            "pre_create_script": "",
            "post_create_script": "",
        }

        ha_instance = self.module.params.get("ha_instance", False)

        # Add HA or single instance related specific arguments to args for including them
        # in action arguments spec
        if ha_instance:
            args.update(
                {
                    "patroni_cluster_name": "",
                    "backup_policy": "",
                    "failover_mode": "",
                    "archive_wal_expire_days": "",
                    "enable_synchronous_mode": False
                }
            )
        else:
            args.update(
                {
                    "auto_tune_staging_drive": False,
                    "auth_method": ""
                }
            )


        # create action arguments
        for key, value in args.items():
            spec = {"name": key, "value": postgres.get(key, value)}
            action_arguments.append(spec)

        # handle scenariors where display names are different
        action_arguments.append(
            {"name": "database_names", "value": postgres.get("db_name")}
        )
        action_arguments.append(
            {"name": "database_size", "value": str(postgres.get("db_size"))}
        )

        # for HA instance, add HA proxy related action arguments and vm details if required
        if ha_instance and postgres.get("ha_proxy"):
            payload, err = self._build_spec_ha_proxy(payload, postgres.get("ha_proxy"))
            if err:
                return None, err

        payload["actionArguments"] = action_arguments
        payload["databaseType"] = NDB_CONSTANTS.DatabaseTypes.POSTGRES
        return payload, None

    def _build_spec_tags(self, payload, tags):
        _tags = Tag(self.module)
        name_uuid_map = _tags.get_all_name_uuid_map()
        specs = []
        for name, val in tags.items():
            if name not in name_uuid_map:
                return None, "Tag with name {0} not found".format(name)
            spec = {"tagId": name_uuid_map[name], "tagName": name, "value": val}
            specs.append(spec)
        payload["tags"] = specs
        return payload, None
