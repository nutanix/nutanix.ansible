# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from ...constants import NDB
from .database_engine import DatabaseEngine


class Postgres(DatabaseEngine):
    def __init__(self, module):
        self._type = NDB.DatabaseTypes.POSTGRES
        super(Postgres, self).__init__(module)

    def build_spec_create_db_params_profile_properties(self, payload, db_params):
        properties = payload.get("properties", [])

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
            "autovacuum_vacuum_cost_delay": "ms",
        }

        # create new properties spec
        for name, val in default_properties.items():

            # check if property value is given in input
            if name in db_params:
                val = str(db_params.get(name))

            val = str(val) + property_units.get(name, "")

            spec = {"name": name, "value": val}
            properties.append(spec)

        payload["properties"] = properties
        return payload, None

    def build_spec_update_db_params_profile_version(self, payload, db_params):

        # map of certain properties with their units
        property_units = {
            "min_wal_size": "MB",
            "max_wal_size": "GB",
            "checkpoint_timeout": "min",
            "autovacuum_vacuum_cost_delay": "ms",
        }

        properties = payload.get("properties", [])

        # update properties
        for prop in properties:

            # check if property value is given in input
            if prop["name"] in db_params:
                val = str(db_params.get(prop["name"]))
                val = val + property_units.get(prop["name"], "")
                prop["value"] = val

        payload["properties"] = properties
        return payload, None


class PostgresSingleInstance(Postgres):
    def __init__(self, module):
        super(PostgresSingleInstance, self).__init__(module)

    def build_spec_db_instance_provision_action_arguments(self, payload, config):

        action_arguments = payload.get("actionArguments", [])
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
            spec = {"name": key, "value": config.get(key, value)}
            action_arguments.append(spec)

        # handle scenariors where display names are diff
        action_arguments.append(
            {"name": "database_names", "value": config.get("db_name")}
        )
        action_arguments.append(
            {"name": "database_size", "value": str(config.get("db_size"))}
        )

        payload["actionArguments"] = action_arguments
        return payload, None

    def build_spec_db_instance_register_action_arguments(self, payload, config):
        action_arguments = payload.get("actionArguments", [])

        # List of action arguments for postgres registration
        args = [
            "listener_port",
            "db_name",
            "db_user",
            "db_password",
        ]

        # create action arguments
        for arg in args:
            if arg in config:
                spec = {"name": arg, "value": config[arg]}
                action_arguments.append(spec)

        action_arguments.append(
            {"name": "postgres_software_home", "value": config["software_path"]}
        )

        payload["actionArguments"] = action_arguments
        return payload, None

    def build_spec_db_server_vm_register_action_arguments(self, payload, config):
        action_arguments = payload.get("actionArguments", [])

        action_arguments.append(
            {"name": "postgres_software_home", "value": config.get("software_path", "")}
        )

        action_arguments.append(
            {"name": "listener_port", "value": config.get("listener_port", "")}
        )

        payload["actionArguments"] = action_arguments
        return payload, None

    def build_spec_db_clone_action_arguments(self, payload, config):
        action_arguments = payload.get("actionArguments", [])
        # fields to their defaults maps
        args = {
            "db_password": "",
            "pre_clone_cmd": "",
            "post_clone_cmd": "",
        }

        # create action arguments
        for key, value in args.items():
            spec = {"name": key, "value": config.get(key, value)}
            action_arguments.append(spec)

        payload["actionArguments"] = action_arguments
        return payload, None


class PostgresHAInstance(Postgres):
    def __init__(self, module):
        super(PostgresHAInstance, self).__init__(module)

    def build_spec_db_instance_provision_action_arguments(self, payload, config):

        action_arguments = payload.get("actionArguments", [])
        # Below is a map of common action arguments fields to their default value
        args = {
            "listener_port": "",
            "allocate_pg_hugepage": False,
            "cluster_database": False,
            "db_password": "",
            "pre_create_script": "",
            "post_create_script": "",
            "patroni_cluster_name": "",
            "archive_wal_expire_days": "",
            "enable_synchronous_mode": False,
            "enable_peer_auth": False,
            "node_type": "database",
            "backup_policy": "primary_only",
            "failover_mode": "Automatic",
        }

        # create action arguments
        for key, default in args.items():
            spec = {"name": key, "value": config.get(key, default)}
            action_arguments.append(spec)

        # handle scenariors where display names are different
        action_arguments.append(
            {"name": "database_names", "value": config.get("db_name")}
        )
        action_arguments.append(
            {"name": "database_size", "value": str(config.get("db_size"))}
        )

        # for HA instance, add HA proxy related action arguments and vm details if required
        ha_proxy = config.get("ha_proxy")
        if ha_proxy:
            action_arguments, err = self._build_spec_ha_proxy_action_arguments(
                ha_proxy, action_arguments=action_arguments
            )
            if err:
                return None, err

        payload["actionArguments"] = action_arguments
        return payload, None

    def _build_spec_ha_proxy_action_arguments(self, ha_proxy, action_arguments=None):

        if not action_arguments:
            action_arguments = []

        action_arguments.append(
            {
                "name": "provision_virtual_ip",
                "value": ha_proxy.get("provision_virtual_ip", False),
            }
        )

        if ha_proxy.get("write_port"):
            action_arguments.append(
                {"name": "proxy_write_port", "value": ha_proxy["write_port"]}
            )

        if ha_proxy.get("read_port"):
            action_arguments.append(
                {"name": "proxy_read_port", "value": ha_proxy["read_port"]}
            )

        action_arguments.append({"name": "deploy_haproxy", "value": True})
        return action_arguments, None
