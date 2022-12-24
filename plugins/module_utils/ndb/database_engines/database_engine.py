from copy import deepcopy

from ..database_engines.postgres import (
    PostgresHAInstance,
    PostgresSingleInstance,
)




class DatabaseEngine:
    _engine_type = ""

    def __init__(self, module):
        self.module = module

    def build_spec_db_instance_provision_action_arguments(self, payload, config):
        return (
            None,
            "Build spec method for Database instance action arguments is not implemented",
        )

    def build_spec_db_params_profile_properties(self, params, curr_properties=None):
        return (
            None,
            "Build spec method for Database Parameter profile's properties is not implemented",
        )

    def get_db_engine_type(self):
        return self._engine_type


def get_database_engine_object(module, db_type):
    engines = {
        "posgres_single_instance": PostgresSingleInstance,
        "postgres_ha_instance": PostgresHAInstance,
    }

    if db_type in engines:
        return engines[db_type].__new__(engines[db_type], module=module), None

    else:
        return None, "Invalid database engine type: {0}".format(db_type)
