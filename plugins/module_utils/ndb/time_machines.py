# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .clusters import Cluster, get_cluster_uuid
from .nutanix_database import NutanixDatabase
from .slas import get_sla_uuid

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

    def log_catchup(self, time_machine_uuid, data):
        endpoint = "{0}/{1}".format(time_machine_uuid, "log-catchups")
        return self.create(data=data, endpoint=endpoint)

    def get_time_machine(self, uuid=None, name=None, query=None):
        """
        Fetch time machine info based on uuid or name.
        Args:
            uuid(str): uuid of time machine
            name(str): name of time machine
            query(str): query params
        """
        if uuid:
            resp = self.read(uuid=uuid, query=query)
        elif name:
            endpoint = "{0}/{1}".format("name", name)
            resp = self.read(endpoint=endpoint, query=query)
            if isinstance(resp, list):
                if not resp:
                    return None, "Time machine with name {0} not found".format(name)
                else:
                    tm = None
                    for entity in resp:
                        if entity["name"] == name:
                            tm = entity
                            break
                    if not tm:
                        return None, "Time machine with name {0} not found".format(name)
                    resp = tm
        return resp, None

    def authorize_db_server_vms(self, uuid, data):
        endpoint = "dbservers"
        return self.update(data=data, uuid=uuid, endpoint=endpoint, method="POST")

    def deauthorize_db_server_vms(self, uuid, data):
        endpoint = "dbservers"
        return self.delete(data=data, uuid=uuid, endpoint=endpoint)

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
        if config.get("uuid"):
            uuid = config["uuid"]
        elif config.get("name"):
            name = config["name"]
            tm, err = self.get_time_machine(name=name)
            if err:
                return None, err
            uuid = tm.get("id")
        else:
            error = "time machine config {0} doesn't have name or uuid key".format(
                config
            )
            return None, error

        return uuid, None

    @staticmethod
    def format_response(response):
        """This method formats time machine based responses.  It removes attributes as per requirement."""
        attrs = ["metadata", "ownerId", "accessLevel", "category"]
        for attr in attrs:
            if attr in response:
                response.pop(attr)
        return response

    def get_log_catchup_spec(self, for_restore=False):
        return deepcopy(
            {
                "forRestore": for_restore,
                "actionArguments": [
                    {"name": "preRestoreLogCatchup", "value": for_restore},
                    {"name": "switch_log", "value": True},
                ],
            }
        )

    def get_authorized_db_server_vm_uuid(self, time_machine_uuid, config):
        uuid = ""
        if config.get("name"):
            resp = self.get_authorized_db_server_vms(
                uuid=time_machine_uuid, query={"usable": True}
            )
            for vm in resp:
                if vm.get("name") == config.get("name"):
                    uuid = vm.get("id")

            if not uuid:
                return None, "Authorized db server vm with name {0} not found".format(
                    config.get("name")
                )

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

    def get_default_data_access_management_spec(self, override_spec=None):
        spec = deepcopy({"nxClusterId": "", "type": "OTHER", "slaId": ""})
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def get_data_access_management_spec(self, old_spec=None):
        self.build_spec_methods = {
            "cluster": self._build_spec_cluster,
            "type": self._build_spec_type,
            "sla": self._build_spec_sla,
        }
        spec = old_spec or self.get_default_data_access_management_spec()
        return super().get_spec(old_spec=spec)

    def _build_spec_cluster(self, payload, param):
        uuid, err = get_cluster_uuid(self.module, param)
        if err:
            return None, err
        payload["nxClusterId"] = uuid
        return payload, None

    def _build_spec_type(self, payload, type):
        payload["type"] = type
        return payload, None

    def _build_spec_sla(self, payload, param):
        uuid, err = get_sla_uuid(self.module, param)
        if err:
            return None, err
        if payload.get("slaId"):
            payload["resetSlaId"] = True
        payload["slaId"] = uuid
        return payload, None

    def check_if_cluster_exists(self, time_machine_uuid, cluster_uuid):
        """
        This method checks if cluster is associated with time machine
        """
        query = {
            "load-associated-clusters": True,
        }
        resp = self.read(uuid=time_machine_uuid, query=query)

        for cluster in resp.get("associatedClusters", []):
            if cluster.get("nxClusterId") == cluster_uuid:
                return True

        return False

    def read_data_access_instance(self, time_machine_uuid, cluster_uuid):
        endpoint = "clusters/{0}".format(cluster_uuid)
        query = {"detailed": True}
        return self.read(uuid=time_machine_uuid, endpoint=endpoint, query=query)

    def create_data_access_instance(self, uuid=None, data=None):
        return self.update(uuid=uuid, data=data, endpoint="clusters", method="POST")

    def update_data_access_instance(self, tm_uuid=None, cluster_uuid=None, data=None):
        endpoint = "clusters/{0}".format(cluster_uuid)
        return self.update(uuid=tm_uuid, data=data, endpoint=endpoint, method="PATCH")

    def delete_data_access_instance(self, tm_uuid=None, cluster_uuid=None):
        endpoint = "clusters/{0}".format(cluster_uuid)
        data = {
            "deleteReplicatedSnapshots": True,
            "deleteReplicatedProtectionDomains": True,
        }
        return self.delete(uuid=tm_uuid, data=data, endpoint=endpoint)
