# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .clusters import Cluster
from .slas import get_sla_uuid
from .nutanix_database import NutanixDatabase

__metaclass__ = type


class TimeMachine(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/tms"
        super(TimeMachine, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "schedule": self._build_spec_schedule,
            "auto_tune_log_drive": self._build_spec_auto_tune_log_drive,
        }

    def authorize_db_server_vms(self, uuid, data):
        endpoint = "dbservers"
        return self.update(data=data, uuid=uuid, endpoint=endpoint, method="POST")

    def get_authorized_db_server_vms(self, uuid, query=None):
        endpoint = "candidate-dbservers"
        return self.read(uuid=uuid, endpoint=endpoint, query=query)

    def get_time_machines(self, value=None, key="uuid", endpoint=None, query=None):

        if value:
            endpoint = value
            if not query:
                query = {}

            query["value-type"] = key

        return self.read(endpoint=endpoint, query=query)

    def get_time_machine_uuid(self, config):
        uuid = ""
        if config.get("name"):
            resp = self.get_time_machines(value=config["name"], key="name")
            uuid = resp.get("id")
        elif config.get("uuid"):
            uuid = config["uuid"]
        else:
            error = "time machine config {0} doesn't have name or uuid key".format(
                config
            )
            return error, None
        return uuid, None

    def get_authorized_db_server_vm_uuid(self, time_machine_uuid, config):
        uuid = ""
        if config.get("name"):
            resp = self.get_authorized_db_server_vms(uuid=time_machine_uuid, query={"usable": True})
            for vm in resp:
                if vm.get("name") == config.get("name"):
                    uuid = vm.get("id")
            
            if not uuid:
                return None, "Authorized db server vm with name {0} not found".format(config.get("name"))

        elif config.get("uuid"):
            uuid = config["uuid"]

        else:
            error = "Authorized db server vm config {0} doesn't have name or uuid key".format(
                config
            )
            return error, None

        return uuid, None

    
    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "description": "",
                "schedule": {},
                "autoTuneLogDrive": True,
            }
        )

    def get_spec(self, old_spec, params=None, **kwargs):

        if not params:
            if self.module.params.get("time_machine"):
                params = self.module.params.get("time_machine")
            else:
                return None, "'time_machine' is required for creating time machine spec"

        time_machine_spec, err = super().get_spec(params=params)
        if err:
            return None, err

        # set sla spec
        sla_uuid, err = get_sla_uuid(self.module, params["sla"])
        if err:
            return None, err

        # set destination clusters incase of HA instance
        if params.get("clusters"):
            cluster_uuids = []

            # fetch all clusters name uuid map
            _cluster = Cluster(self.module)
            clusters_name_uuid_map = _cluster.get_all_clusters_name_uuid_map()

            for cluster in params.get("clusters"):
                cluster_uuid = ""
                if cluster.get("name"):
                    if clusters_name_uuid_map.get(cluster["name"]):
                        cluster_uuid = clusters_name_uuid_map[cluster["name"]]
                    else:
                        return None, "NDB cluster with name '{0}' not found".format(
                            cluster["name"]
                        )

                elif cluster.get("uuid"):
                    cluster_uuid = cluster["uuid"]

                cluster_uuids.append(cluster_uuid)

            time_machine_spec["slaDetails"] = {
                "primarySla": {"slaId": sla_uuid, "nxClusterIds": cluster_uuids}
            }
        else:
            time_machine_spec["slaId"] = sla_uuid

        old_spec["timeMachineInfo"] = time_machine_spec
        return old_spec, None

    def get_authorize_db_server_vms_spec(self):
        # avoiding circuler imports
        from .db_server_vm import DBServerVM
        _db_server_vms = DBServerVM(self.module)
        db_server_vms = self.module.params.get("db_server_vms")

        uuids, err = _db_server_vms.resolve_uuids_from_entity_specs(vms=db_server_vms)
        payload = uuids
        return payload, err

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_auto_tune_log_drive(self, payload, auto_tune):
        payload["autoTuneLogDrive"] = auto_tune
        return payload, None

    def _build_spec_schedule(self, payload, schedule):
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

        payload["schedule"] = schedule_spec
        return payload, None
