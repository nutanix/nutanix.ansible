# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .slas import get_sla_uuid

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class TimeMachine(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/tms"
        super(TimeMachine, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "sla": self._build_spec_sla,
            "schedule": self._build_spec_schedule,
            "auto_tune_log_drive": self._build_spec_auto_tune_log_drive,
        }

    def get_time_machine(self, uuid=None, name=None):
        if uuid:
            resp = self.read(uuid=uuid)
        elif name:
            endpoint = "{0}/{1}".format("name", name)
            resp = self.read(endpoint=endpoint)
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

                    # fetch all details using uuid
                    if resp.get("id"):
                        resp = self.read(uuid=resp["id"])
        else:
            return (
                None,
                "Please provide either uuid or name for fetching time machine details",
            )
        return resp, None

    def get_default_spec_for_single_instance(self):
        return deepcopy(
            {
                "name": "",
                "description": "",
                "slaId": "",
                "schedule": {},
                "autoTuneLogDrive": True,
            }
        )

    def get_spec(self, old_spec, params=None):
        tm_payload = self.get_default_spec_for_single_instance()
        if not params:
            if self.module.params.get("time_machine"):
                params = self.module.params.get("time_machine")
            else:
                return None, "'time_machine' is required for creating time machine spec"

        time_machine_spec, err = super().get_spec(old_spec=tm_payload, params=params)
        if err:
            return None, err
        old_spec["timeMachineInfo"] = time_machine_spec
        return old_spec, None

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_auto_tune_log_drive(self, payload, auto_tune):
        payload["autoTuneLogDrive"] = auto_tune
        return payload, None

    def _build_spec_sla(self, payload, sla):
        uuid, err = get_sla_uuid(self.module, sla)
        if err:
            return None, err
        payload["slaId"] = uuid
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
