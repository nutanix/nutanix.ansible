# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy

from .database_engines.db_engine_factory import create_db_engine
from .nutanix_database import NutanixDatabase
from .profiles.profile_types import DatabaseParameterProfile
from .time_machines import TimeMachine


class DatabaseClone(NutanixDatabase):
    resource_type = "/clones"

    def __init__(self, module):

        super(DatabaseClone, self).__init__(module, self.resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "db_params_profile": self._build_spec_db_params_profile,
            "time_machine": self._build_spec_time_machine,
            "removal_schedule": self._build_spec_removal_schedule,
            "refresh_schedule": self._build_spec_refresh_schedule,
        }

    def create(self, time_machine_uuid, data):
        time_machine = TimeMachine(self.module)
        endpoint = "{0}/clones".format(time_machine_uuid)
        return time_machine.create(data=data, endpoint=endpoint)

    def refresh(self, uuid, data):
        endpoint = "refresh"
        return self.update(data=data, uuid=uuid, endpoint=endpoint, method="POST")

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
            data,
            uuid,
            endpoint,
            query,
            raise_error,
            no_response,
            timeout,
            method=method,
        )

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "description": "",
                "clustered": False,
                "nxClusterId": "",
                "sshPublicKey": "",
                "timeMachineId": "",
                "snapshotId": None,
                "userPitrTimestamp": None,
                "timeZone": "",
                "latestSnapshot": False,
                "actionArguments": [],
                "lcmConfig": {"databaseLCMConfig": {}},
                "databaseParameterProfileId": "",
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
                "lcmConfig": {},
                "resetLcmConfig": False,
            }
        )
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def get_default_delete_spec(self):
        return deepcopy({"remove": False, "delete": False, "softRemove": False})

    def get_clone(self, uuid=None, name=None):
        if uuid:
            resp = self.read(uuid=uuid)
        elif name:
            query = {"value-type": "name", "value": name}
            resp = self.read(query=query)
            if not resp:
                return None, "Clone with name {0} not found".format(name)
            resp = resp[0]
        else:
            return None, "Please provide either uuid or name for fetching clone details"

        return resp, None

    def get_db_engine_spec(self, payload, params=None, **kwargs):

        db_engine, err = create_db_engine(self.module, db_architecture="single")
        if err:
            return None, err

        db_type = db_engine.get_type()

        config = self.module.params.get(db_type) or params

        payload, err = db_engine.build_spec_db_clone_action_arguments(payload, config)
        if err:
            return None, err

        return payload, err

    def get_update_spec(self, payload):
        self.build_spec_methods = {
            "removal_schedule": self._build_spec_removal_schedule_update,
            "refresh_schedule": self._build_spec_refresh_schedule_update,
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
        }

        return super().get_spec(old_spec=payload)

    def get_delete_spec(self, payload):
        if self.module.params.get("delete_from_vm"):
            payload["delete"] = True
        elif self.module.params.get("soft_remove"):
            payload["softRemove"] = True
        else:
            payload["remove"] = True

        return payload, None

    def get_clone_refresh_spec(self):
        payload = {}
        if self.module.params.get("snapshot_uuid"):
            payload["snapshotId"] = self.module.params.get("snapshot_uuid")
        elif self.module.params.get("pitr_timestamp"):
            payload["userPitrTimestamp"] = self.module.params.get("pitr_timestamp")
        else:
            return (
                None,
                "snapshot_uuid or pitr_timestamp is required for database clone refresh",
            )

        payload["timeZone"] = self.module.params.get("timezone")
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_db_params_profile(self, payload, db_params_profile):
        db_params = DatabaseParameterProfile(self.module)
        uuid, err = db_params.get_profile_uuid(
            db_params_profile
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
            payload["snapshotId"] = time_machine.get("snapshot_uuid")
        elif time_machine.get("pitr_timestamp"):
            payload["userPitrTimestamp"] = time_machine.get("pitr_timestamp")
        else:
            return (
                None,
                "Required snapshot_uuid or pitr_timestamp for source of db clone",
            )

        payload["timeZone"] = time_machine.get("timezone")
        return payload, None

    def _build_spec_removal_schedule(self, payload, removal_schedule):
        expiry_details = payload.get("lcmConfig", {}).get("expiryDetails", {})
        if not expiry_details:
            expiry_details = {}

        # map of display name to api field names
        args = {
            "days": "expireInDays",
            "timezone": "expiryDateTimezone",
            "delete_database": "deleteDatabase",
            "timestamp": "expiryTimestamp",
            "remind_before_in_days": "remindBeforeInDays",
        }
        for key, val in args.items():
            if removal_schedule.get(key) is not None:
                expiry_details[val] = removal_schedule.get(key)
        
        if not payload["lcmConfig"].get("databaseLCMConfig"):
            payload["lcmConfig"]["databaseLCMConfig"] = {
                "expiryDetails": expiry_details
            }
        else:
            payload["lcmConfig"]["databaseLCMConfig"]["expiryDetails"] = expiry_details

        return payload, None

    def _build_spec_refresh_schedule(self, payload, refresh_schedule):
        refresh_details = payload.get("lcmConfig", {}).get("refreshDetails", {})
        if not refresh_details:
            refresh_details = {}

        # map of display name to api field names
        args = {
            "days": "refreshInDays",
            "timezone": "refreshDateTimezone",
            "time": "refreshTime",
        }

        for key, val in args.items():
            if refresh_schedule.get(key):
                refresh_details[val] = refresh_schedule.get(key)
        
        if not payload["lcmConfig"].get("databaseLCMConfig"):
            payload["lcmConfig"]["databaseLCMConfig"] = {
                "refreshDetails": refresh_details
            }
        else:
            payload["lcmConfig"]["databaseLCMConfig"]["refreshDetails"] = refresh_details        
        
        return payload, None

    def _build_spec_removal_schedule_update(self, payload, removal_schedule):
        if removal_schedule.get("state", "present") == "absent":
            payload["removeExpiryConfig"] = True
        else:
            
            payload, err = self._build_spec_removal_schedule(payload, removal_schedule)
            if err:
                return None, err
            payload["lcmConfig"]["expiryDetails"] = payload["lcmConfig"]["databaseLCMConfig"]["expiryDetails"]
            payload["lcmConfig"].pop("databaseLCMConfig")
            
            # some changes for expiry timestamp
            if removal_schedule.get("timestamp"):
                payload["lcmConfig"]["expiryDetails"]["expireInDays"] = 0
            payload["resetLcmConfig"] = True
        return payload, None

    def _build_spec_refresh_schedule_update(self, payload, refresh_schedule):
        if refresh_schedule.get("state", "present") == "absent":
            payload["removeRefreshConfig"] = True
        else:
            payload, err = self._build_spec_refresh_schedule(payload, refresh_schedule)
            if err:
                return None, err
            
            payload["lcmConfig"]["refreshDetails"] = payload["lcmConfig"]["databaseLCMConfig"]["refreshDetails"]
            payload["lcmConfig"].pop("databaseLCMConfig")
            payload["resetLcmConfig"] = True
        return payload, None
