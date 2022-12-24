from copy import deepcopy
from nutanix_database import NutanixDatabase
from database_engines.database_engine import DatabaseEngine
from profiles import get_profile_uuid


class DatabaseInstance(NutanixDatabase):
    resource_type = "/database"
    db_engine: DatabaseEngine = None

    def __init__(self, module, db_engine: DatabaseEngine):

        # assign database engine handler
        self.db_engine = db_engine

        super(SingleInstance, SingleInstance).__init__(module, self.resource_type)

    def provision(self, data):
        pass

    def register(self, data):
        pass

    def build_spec_provision(self, payload, config):

        build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "db_params_profile": self._build_spec_db_params_profile,
            "database_type": self._build_spec_database_type,
            "auto_tune_staging_drive": self._build_spec_auto_tune_staging_drive,
        }

        for field, method in build_spec_methods.items():
            if field in config:
                payload, err = method(payload, config[field])
                if err:
                    return None, err

        # build action arguments related to database engine
        db_engine_config = config.get(self.db_engine.get_db_engine_type())
        payload, err = self.db_engine.build_spec_db_instance_provision_action_arguments(
            payload, db_engine_config
        )
        return payload, err

    def build_spec_register(self, payliad, config):
        pass

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["databaseDescription"] = desc
        return payload, None

    def _build_spec_db_params_profile(self, payload, db_params_profile):
        uuid, err = get_profile_uuid(
            self.module, "Database_Parameter", db_params_profile
        )
        if err:
            return None, err

        payload["dbParameterProfileId"] = uuid
        return payload, None

    def _build_spec_database_type(self, payload):
        payload["databaseType"] = self.db_engine.get_type()
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
