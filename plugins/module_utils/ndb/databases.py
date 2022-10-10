# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .clusters import get_cluster_uuid
from .db_servers import get_db_server_uuid
from .slas import get_sla_uuid
from .tags import Tag
from .nutanix_database import NutanixDatabase
from .profiles import Profile, get_profile_uuid
from ..constants import NDB as NDB_CONSTANTS

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
            "time_machine": self._build_spec_time_machine,
            "postgress": self._build_spec_postgress,
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
        query = {
            "value-type": key,
            "value": value
        }
        resp = self.read(query=query, raise_error=False)

        if not resp:
            return None, "Database instance with name {0} not found.".format(value)
        elif resp.get("errorCode"):
            self.module.fail_json(
                msg="Failed fetching Database instance",
                error=resp.get("message"),
                response=resp,
            )

        uuid = resp[0]["id"]
        return uuid, None

    def create(self, data=None, endpoint=None, query=None, method="POST", raise_error=True, no_response=False, timeout=30):
        endpoint = "provision"
        return super().create(data, endpoint, query, method, raise_error, no_response, timeout)
    
    def update(self, data=None, uuid=None, endpoint=None, query=None, raise_error=True, no_response=False, timeout=30, method="PATCH"):
        return super().update(data, uuid, endpoint, query, raise_error, no_response, timeout, method)

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
                "tags": []
            }
        )
    
    def get_update_spec(self):
        return deepcopy(
            {
                "name": None,
                "description": None,
                "tags": [],
                "resetTags": True,
                "resetName": True,
                "resetDescription": True
            }
        )
    
    def get_delete_spec(self):
        return deepcopy(
            {
                "delete": False,
                "remove": False,
                "deleteTimeMachine": False, 
                "deleteLogicalCluster": True
            }
        )

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_auto_tune_staging_drive(self, payload, value):
        payload["autoTuneStagingDrive"] = payload["auto_tune_staging_drive"]
        return payload, None

    def _build_spec_db_params_profile(self, payload, db_params_profile):
        uuid, err = get_profile_uuid(
            self.module, "Database_Parameter", db_params_profile
        )
        if err:
            return None, err

        payload["dbParameterProfileId"] = uuid
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
            uuid, err = get_profile_uuid(
                self.module, "Software", vm_config["compute_profile"]
            )
            if err:
                return None, err

            profiles = Profile(self.module)
            software_profile = profiles.read(uuid)
            payload["softwareProfileId"] = uuid
            payload["softwareProfileVersionId"] = software_profile["latestVersionId"]

            # set network prfile
            uuid, err = get_profile_uuid(
                self.module, "Network", vm_config["compute_profile"]
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

            # set cluster config
            uuid, err = get_cluster_uuid(self.module, vm_config["cluster"])
            if err:
                return None, err
            payload["nxClusterId"] = uuid

            # set other params
            payload["sshPublicKey"] = vm_config["pub_ssh_key"]
            payload["vmPassword"] = vm_config["password"]
            return payload, None

    def _build_spec_time_machine(self, payload, time_machine):

        # set sla uuid
        uuid, err = get_sla_uuid(self.module, time_machine["sla"])
        if err:
            return None, err
        payload["time_machine"]["slaId"] = uuid

        schedule = time_machine.get("schedule")
        schedule_spec = {}
        if schedule.get("daily"):

            time = schedule["daily"].split(":")
            if len(time) != 3:
                return None, "Dail snapshot schedule not in HH:MM:SS format."

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

            # set quaterly and yearly as they are dependent on quaterly and yearly
            if schedule.get("quaterly"):
                schedule_spec["quartelySchedule"] = {
                    "enabled": True,
                    "startMonth": schedule["quaterly"],
                    "dayOfMonth": schedule.get("monthly"),
                }

            if schedule.get("yearly"):
                schedule_spec["quartelySchedule"] = {
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

        payload["time_machine"]["schedule"] = schedule_spec
        payload["time_machine"]["name"] = time_machine["name"]
        payload["time_machine"]["description"] = time_machine.get("desc", "")
        payload["time_machine"]["autoTuneLogDrive"] = time_machine.get(
            "auto_tune_log_drive"
        )
        return payload, None

    def _build_spec_postgress(self, payload, postgress):
        action_arguments = []
        fields = [
            "listener_port",
            "auto_tune_staging_drive",
            "allocate_pg_hugepage",
            "cluster_database",
            "auth_method",
            "db_password",
            "pre_create_script",
            "post_create_script",
        ]
        for field in fields:
            spec = {"name": field, "value": postgress.get(field)}
            action_arguments.append(spec)

        # handle scenariors where display names are diff
        action_arguments.append(
            {"name": "database_names", "value": postgress.get("db_name")}
        )
        action_arguments.append(
            {"name": "database_size", "value": postgress.get("db_size")}
        )

        payload["actionArguments"] = action_arguments
        payload["database_type"] = NDB_CONSTANTS.DatabaseTypes.POSTGRESS
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
