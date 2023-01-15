# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy
from .database_engines.db_engine_factory import create_db_engine
from .time_machines import TimeMachine
from .database_instances import DatabaseInstance
from .profiles import get_profile_uuid


class DatabaseClone(DatabaseInstance):
    resource_type="/clones"
    def __init__(self, module):

        super(DatabaseClone, self).__init__(module, self.resource_type)
        self.build_spec_methods = {
            "name": self.build_spec_name,
            "desc": self.build_spec_desc,
            "db_params_profile": self._build_spec_db_params_profile,
            "time_machine": self._build_spec_time_machine,
            "removal_schedule": self._build_spec_removal_schedule,
            "refresh_schedule": self._build_spec_refresh_schedule,
        }

    def clone(self, data, time_machine_uuid):
        time_machine = TimeMachine(self.module)
        endpoint = "{}/clones".format(time_machine_uuid)
        return time_machine.create(data=data, endpoint=endpoint)
    
    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "description": "",
                "clustered": False,
                "nxClusterId": "",
                "sshPublicKey": "",
                "timeMachineId": "",
                "snapshotId": "",
                "userPitrTimestamp": None,
                "timeZone": "",
                "latestSnapshot": False,
                "actionArguments": [],
                "lcmConfig": {
                    "databaseLCMConfig":{}
                },
                "databaseParameterProfileId": ""
            }
        )

    def get_db_engine_spec(self, payload, params=None, **kwargs):

        db_engine, err = create_db_engine(self.module, "single")
        if err:
            return None, err

        db_type = db_engine.get_type()

        config = self.module.params.get(db_type) or params

        payload, err = db_engine.build_spec_db_clone_action_arguments(
                payload, config
            )
        if err:
            return None, err

        return payload, err

    def _build_spec_db_params_profile(self, payload, db_params_profile):
        uuid, err = get_profile_uuid(
            self.module, "Database_Parameter", db_params_profile
        )
        if err:
            return None, err

        payload["databaseParameterProfileId"] = uuid
        return payload, None

    def _build_spec_time_machine(self, payload, time_machine):
        _time_machine = TimeMachine(self.module)
        uuid, err = _time_machine.get_time_machine_uuid(time_machine)
        if err:
            return None, err
        payload["timeMachineId"] = uuid
        
        if time_machine.get("snapshot_uuid"):
            payload["snapshotId"] =  time_machine.get("snapshot_uuid")
        elif time_machine.get("pitr_timestamp"):
            payload["userPitrTimestamp"] =  time_machine.get("userPitrTimestamp")
        else:
            return None, "Required snapshot_uuid or pitr_timestamp for source of db clone"
        
        payload["timeZone"] = time_machine.get("timezone")
        return payload, None

    def _build_spec_removal_schedule(self, payload, removal_schedule):
        payload["lcmConfig"]["databaseLCMConfig"]["expiryDetails"] = {
            "expireInDays": removal_schedule.get("days"),
            "expiryDateTimezone": removal_schedule.get("timezone"),
            "deleteDatabase": removal_schedule.get("delete_database")
        }
        return payload, None

    def _build_spec_refresh_schedule(self, payload, refresh_schedule):
        payload["lcmConfig"]["databaseLCMConfig"]["refreshDetails"] = {
            "refreshInDays": str(refresh_schedule.get("days")),
            "refreshTime": refresh_schedule.get("time"),
            "refreshDateTimezone": refresh_schedule.get("timezone"),
        }
        return payload, None 