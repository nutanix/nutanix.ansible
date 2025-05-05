# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ..constants import NDB
from .database_engines.db_engine_factory import create_db_engine, get_engine_type
from .db_server_vm import DBServerVM
from .nutanix_database import NutanixDatabase
from .profiles.profile_types import DatabaseParameterProfile
from .time_machines import TimeMachine


class DatabaseInstance(NutanixDatabase):
    resource_type = "/databases"

    def __init__(self, module):

        super(DatabaseInstance, self).__init__(module, self.resource_type)
        self.build_spec_methods = {
            "auto_tune_staging_drive": self._build_spec_auto_tune_staging_drive,
        }

    def provision(self, data):
        endpoint = "provision"
        return self.create(data, endpoint, timeout=60)

    def register(self, data):
        endpoint = "register"
        return self.create(data, endpoint)

    def scale(self, uuid, data):
        endpoint = "update/extend-storage"
        return self.update(data=data, uuid=uuid, endpoint=endpoint, method="POST")

    def restore(self, uuid, data):
        endpoint = "restore"
        return self.update(data=data, uuid=uuid, endpoint=endpoint, method="POST")

    def add_databases(self, instance_uuid, data):
        endpoint = "linked-databases"
        return self.update(
            data=data, uuid=instance_uuid, endpoint=endpoint, method="POST"
        )

    def remove_linked_database(self, linked_database_uuid, database_instance_uuid):
        spec = {"delete": True, "forced": True}
        endpoint = "linked-databases/{0}".format(linked_database_uuid)
        return self.delete(uuid=database_instance_uuid, endpoint=endpoint, data=spec)

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

    @staticmethod
    def format_response(response):
        """This method formats the response.  It removes attributes as per requirement."""
        attrs = [
            "lcmConfig",
            "accessLevel",
            "category",
            "placeholder",
            "internal",
            "databaseGroupStateInfo",
            "databaseClusterType",
            "parentTimeMachineId",
            "parentSourceDatabaseId",
            "ownerId",
            "databaseStatus",
            "groupInfo",
        ]
        for attr in attrs:
            if attr in response:
                response.pop(attr)

        if response.get("metadata") is not None:
            response["provisionOperationId"] = response.get("metadata", {}).get(
                "provisionOperationId"
            )
        response.pop("metadata")

        # format database node's responses
        for node in response.get("databaseNodes", []):
            DBServerVM.format_response(node)
            node.pop("dbserver")

        # format time machine's response
        if response.get("timeMachine"):
            TimeMachine.format_response(response.get("timeMachine"))

        return response

    def _get_action_argument_spec(self, name, value):
        return deepcopy({"name": name, "value": value})

    def get_default_provision_spec(self):
        return deepcopy(
            {
                "databaseType": None,
                "name": None,
                "dbParameterProfileId": None,
                "actionArguments": [],
                "clustered": False,
                "autoTuneStagingDrive": True,
                "tags": [],
            }
        )

    def get_default_registration_spec(self):
        return deepcopy(
            {
                "databaseType": "",
                "databaseName": "",
                "workingDirectory": "",
                "actionArguments": [],
                "autoTuneStagingDrive": True,
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

    def _get_default_scaling_spec(self):
        return deepcopy(
            {
                "actionArguments": [
                    {"name": "working_dir", "value": "/tmp"},
                ],
                "applicationType": None,
            }
        )

    def get_default_restore_spec(self):
        return deepcopy(
            {
                "snapshotId": None,
                "latestSnapshot": None,
                "userPitrTimestamp": None,
                "timeZone": None,
                "actionArguments": [{"name": "sameLocation", "value": True}],
            }
        )

    def get_database(self, name=None, uuid=None, query=None):
        if uuid:
            resp = self.read(uuid=uuid, query=query, raise_error=False)
        elif name:
            query_params = {"value-type": "name", "value": name}
            if query:
                query.update(query_params)
            else:
                query = query_params
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

    def get_spec(self, old_spec=None, params=None, **kwargs):
        # handle registration and provisioning from this factory itself

        if kwargs.get("update"):
            return self.get_update_spec(old_spec=old_spec, params=params, **kwargs)
        elif kwargs.get("provision"):
            return self.get_spec_for_provision(
                old_spec=old_spec, params=params, **kwargs
            )
        elif kwargs.get("register"):
            return self.get_spec_for_registration(
                old_spec=old_spec, params=params, **kwargs
            )

        return None, "Please provide supported arguments"

    def get_update_spec(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "name": self.build_spec_name,
            "desc": self.build_spec_desc,
        }
        return super().get_spec(old_spec=old_spec, params=params, **kwargs)

    def get_spec_for_provision(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "name": self.build_spec_name,
            "db_params_profile": self.build_spec_db_params_profile,
            "desc": self._build_spec_database_desc,
        }
        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)

        if self.module.params.get("auto_tune_staging_drive") is not None:
            payload["autoTuneStagingDrive"] = self.module.params.get(
                "auto_tune_staging_drive"
            )

        return payload, err

    def get_spec_for_registration(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "working_directory": self._build_spec_register_working_dir,
            "name": self._build_spec_register_name,
            "desc": self.build_spec_desc,
        }

        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)

        if self.module.params.get("auto_tune_staging_drive") is not None:
            payload["autoTuneStagingDrive"] = self.module.params.get(
                "auto_tune_staging_drive"
            )

        return payload, err

    def get_engine_type(self):
        engine_types = NDB.DatabaseTypes.ALL

        for type in engine_types:
            if type in self.module.params:
                return type, None

        return (
            None,
            "Input doesn't conatains config for allowed engine types of databases",
        )

    def get_db_engine_spec(self, payload, params=None, **kwargs):

        db_engine_type, err = get_engine_type(self.module)
        if err:
            return None, err

        config = self.module.params.get(db_engine_type) or params

        if not config:
            return None, "input for database engine is missing, {0}".format(
                db_engine_type
            )

        db_architecture = config.get("type")

        db_engine, err = create_db_engine(
            self.module, engine_type=db_engine_type, db_architecture=db_architecture
        )
        if err:
            return None, err

        if kwargs.get("provision"):

            payload, err = db_engine.build_spec_db_instance_provision_action_arguments(
                payload, config
            )
            if err:
                return None, err

        elif kwargs.get("register"):
            payload, err = db_engine.build_spec_db_instance_register_action_arguments(
                payload, config
            )
            if err:
                return None, err

        payload["databaseType"] = db_engine_type + "_database"
        return payload, err

    def get_delete_spec(self):
        spec = {
            "delete": False,
            "remove": False,
            "softRemove": False,
            "deleteTimeMachine": False,
            "deleteLogicalCluster": False,
        }

        if self.module.params.get("soft_delete"):
            spec["softRemove"] = True
        elif self.module.params.get("delete_db_from_vm"):
            spec["delete"] = True
        else:
            spec["remove"] = True

        if self.module.params.get("delete_time_machine"):
            spec["deleteTimeMachine"] = True

        return spec

    def get_scaling_spec(self, scale_config, database_type):
        config = deepcopy(scale_config)
        spec = self._get_default_scaling_spec()

        spec["applicationType"] = database_type

        spec["actionArguments"].append(
            self._get_action_argument_spec(
                "data_storage_size", int(config.get("storage_gb"))
            )
        )
        spec["actionArguments"].append(
            self._get_action_argument_spec(
                "pre_script_cmd", config.get("pre_update_cmd")
            )
        )
        spec["actionArguments"].append(
            self._get_action_argument_spec(
                "post_script_cmd", config.get("post_update_cmd")
            )
        )

        return spec

    def get_restore_spec(self, restore_config):
        spec = self.get_default_restore_spec()
        if restore_config.get("snapshot_uuid"):
            spec["snapshotId"] = restore_config["snapshot_uuid"]
        elif restore_config.get("pitr_timestamp"):
            spec["userPitrTimestamp"] = restore_config["pitr_timestamp"]
            spec["timeZone"] = restore_config.get("timezone")
        else:
            spec["latestSnapshot"] = True

        return spec

    def get_add_database_spec(self, database_names):
        spec = {"databases": []}

        for name in database_names:
            spec["databases"].append({"databaseName": name})

        return spec

    def build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def build_spec_db_params_profile(self, payload, db_params_profile):
        db_params = DatabaseParameterProfile(self.module)
        uuid, err = db_params.get_profile_uuid(db_params_profile)
        if err:
            return None, err

        payload["dbParameterProfileId"] = uuid
        return payload, None

    def _build_spec_database_desc(self, payload, desc):
        payload["databaseDescription"] = desc
        return payload, None

    def _build_spec_register_name(self, payload, name):
        payload["databaseName"] = name
        return payload, None

    def _build_spec_register_working_dir(self, payload, working_dir):
        payload["workingDirectory"] = working_dir
        return payload, None

    def _build_spec_auto_tune_staging_drive(self, payload, value):
        payload["autoTuneStagingDrive"] = value
        return payload, None
