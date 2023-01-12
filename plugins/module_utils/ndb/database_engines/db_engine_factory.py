# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ..database_engines.postgres import (
    PostgresHAInstance,
    PostgresSingleInstance,
)
from ...constants import NDB


def get_engine_type(module):
    engine_types = NDB.DatabaseTypes.ALL

    for type in engine_types:
        if type in module.params:
            return type, None

    return None, "Input doesn't conatains config for allowed engine types of databases"


def create_db_engine(module, db_architecture=None):
    engines = {"postgres": {"single": PostgresSingleInstance, "ha": PostgresHAInstance}}

    engine_type, err = get_engine_type(module)
    if err:
        return None, err

    if not db_architecture:       
        db_architecture = module.params[engine_type].get("type")

    if not db_architecture:
        return None, "db architecture is required for creating db engine object"

    if engine_type in engines:
        if (
            db_architecture
            and isinstance(engines[engine_type], dict)
            and db_architecture in engines[engine_type]
        ):
            return engines[engine_type][db_architecture](module), None
        else:
            return (
                None,
                "Invalid database engine architecture: {0} given for {1}".format(
                    db_architecture, engine_type
                ),
            )
    else:
        return None, "Invalid database engine type: {0}".format(engine_type)
