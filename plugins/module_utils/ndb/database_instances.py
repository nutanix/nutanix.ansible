from copy import deepcopy
from .nutanix_database import NutanixDatabase
from .database_engines.database_engine import DatabaseEngine
from .database_engines.db_engine_factory import create_db_engine
from .profiles import get_profile_uuid


class DatabaseInstance(NutanixDatabase):
    resource_type = "/databases"

    def __init__(self, module):

        super(DatabaseInstance, self).__init__(module, self.resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "db_params_profile": self._build_spec_db_params_profile,
            "auto_tune_staging_drive": self._build_spec_auto_tune_staging_drive,
        }

    def provision(self, data):
        endpoint = "provision"
        return self.create(data, endpoint)

    def register(self, data):
        endpoint = "register"
        return self.create(data, endpoint)

    def update(
        self,
        data=None,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
        method="PUT",
    ):
        return super().update(
            data,
            uuid,
            endpoint,
            query,
            raise_error,
            no_response,
            timeout,
            method="PATCH",
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

    def get_default_spec(self):
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
        spec = {
            "delete": False,
            "remove": False,
            "deleteTimeMachine": False,
            "deleteLogicalCluster": True,
        }

        if self.module.params.get("soft_delete"):
            spec["remove"] = True
            spec["delete"] = False
        else:
            spec["delete"] = True
            spec["remove"] = False

        if self.module.params.get("delete_time_machine"):
            spec["deleteTimeMachine"] = True

        return spec

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

    def get_spec(self, old_spec=None, params=None, **kwargs):
        # handle registration and provisioning from this factory itself

        if kwargs.get("update"):
            return self.get_update_spec(payload=old_spec)
        else:
            if kwargs.get("provision"):
                return self.get_spec_for_provision(payload=old_spec)
            else:
                return self.get_spec_for_registration(payload=old_spec)

    def get_update_spec(self, payload):
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc_update,
        }
        return super().get_spec(old_spec=payload)

    def get_db_engine_spec(self, payload):

        db_engine, err = create_db_engine(self.module)
        if err:
            return None, err

        db_type = db_engine.get_type()

        config = self.module.params[db_type]

        payload, err = db_engine.build_spec_db_instance_provision_action_arguments(
            payload, config
        )

        payload["databaseType"] = db_type + "_database"
        return payload, err

    def get_spec_for_provision(self, payload):
        return super().get_spec(old_spec=payload)

    def get_spec_for_registration(self, payload):
        return super().get_spec(old_spec=payload)

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["databaseDescription"] = desc
        return payload, None

    def _build_spec_desc_update(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_db_params_profile(self, payload, db_params_profile):
        uuid, err = get_profile_uuid(
            self.module, "Database_Parameter", db_params_profile
        )
        if err:
            return None, err

        payload["dbParameterProfileId"] = uuid
        return payload, None

    def _build_spec_auto_tune_staging_drive(self, payload, value):
        payload["autoTuneStagingDrive"] = value
        return payload, None


class SingleInstance(DatabaseInstance):
    def __init__(self, module, db_engine: DatabaseEngine):
        super(SingleInstance, SingleInstance).__init__(module, db_engine)


class HAInstance(DatabaseInstance):
    def __init__(self, module, db_engine: DatabaseEngine):
        super(HAInstance, SingleInstance).__init__(module, db_engine)
