from copy import deepcopy


class DatabaseEngine:
    _type=""

    def build_spec_db_instance_action_arguments(self, payload, action_arguments):
        return None, "Build spec method for Database instance action arguments is not implemented"

    def build_spec_db_params_profile_properties(self, params, cur_properties=None):
        return None, "Build spec method for Database Parameter profile's properties is not implemented"
    
    def get_database_type(self):
        return self._type

class Postgres(DatabaseEngine):

    def __init__(self):
        self._type = "postgres"        

    def build_spec_db_params_profile_properties(self, params, cur_properties=None):
        input_properties = deepcopy(params)
        properties = []

        # for update
        if cur_properties:
            properties = deepcopy(properties)

        # map of properties with defaults
        default_properties = {
            "max_connections": 100,
            "max_replication_slots": 10,
            "effective_io_concurrency": 1,
            "timezone": "UTC",
            "max_prepared_transactions": 0,
            "max_locks_per_transaction": 64,
            "max_wal_senders": 10,
            "max_worker_processes": 8,
            "checkpoint_completion_target": 0.5,
            "autovacuum": "on",
            "autovacuum_freeze_max_age": 200000000,
            "autovacuum_vacuum_threshold": 50,
            "autovacuum_vacuum_scale_factor": 0.2,
            "autovacuum_work_mem": -1,
            "autovacuum_max_workers": 3,
            "wal_buffers": -1,
            "synchronous_commit": "on",
            "random_page_cost": 4,
            "wal_keep_segments": 700,
            "min_wal_size": 80,
            "max_wal_size": 1,
            "checkpoint_timeout": 5,
            "autovacuum_vacuum_cost_delay": 2,
        }

        # map of certain properties with their units
        property_units = {
            "min_wal_size": "MB",
            "max_wal_size": "GB",
            "checkpoint_timeout": "min",
            "autovacuum_vacuum_cost_delay": "ms"
        }

        # update current properties with input config
        if properties:

            for prop in properties:
                # if input given
                if prop["name"] in input_properties:

                    # get property value from input and add unit suffix if required
                    val = str(input_properties[prop["name"]]) + property_units.get(prop["name"], "")
                    
                    # update the property value
                    prop["value"] = val

        else:

            for name, val in default_properties:

                # check if property value is given in input
                if name in input_properties:
                    val = str(val)

                val = val + property_units.get(name, "")
                
                spec = {
                    "name": name,
                    "value": val
                }
                properties.append(spec)

        return properties, None
    
class SingleInstance(Postgres):
    
    def build_spec_db_instance_action_arguments(self, action_arguments):
        action_arguments = []

        # fields to their defaults maps
        args = {
            "listener_port": "",
            "auto_tune_staging_drive": False,
            "allocate_pg_hugepage": False,
            "cluster_database": False,
            "auth_method": "",
            "db_password": "",
            "pre_create_script": "",
            "post_create_script": "",
        }

        # create action arguments
        for key, value in args.items():
            spec = {"name": key, "value": action_arguments.get(key, value)}
            action_arguments.append(spec)

        # handle scenariors where display names are diff
        action_arguments.append(
            {"name": "database_names", "value": action_arguments.get("db_name")}
        )
        action_arguments.append(
            {"name": "database_size", "value": str(action_arguments.get("db_size"))}
        )

        return action_arguments

class HAInstance(Postgres):

    def build_spec_db_instance_action_arguments(self, payload, action_arguments):
        # implement DatabaseEngine.build_spec_db_instance_action_arguments()
        pass

