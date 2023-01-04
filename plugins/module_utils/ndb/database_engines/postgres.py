# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type



from copy import deepcopy

from .database_engine import DatabaseEngine
from ...constants import NDB
from ..db_servers import DBServerVM



class Postgres(DatabaseEngine):
    def __init__(self, module):
        self._type = NDB.DatabaseTypes.POSTGRES
        super(Postgres, self).__init__(module)

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
            "autovacuum_vacuum_cost_delay": "ms",
        }

        # update current properties with input config
        if properties:

            for prop in properties:
                # if input given
                if prop["name"] in input_properties:

                    # get property value from input and add unit suffix if required
                    val = str(input_properties[prop["name"]]) + property_units.get(
                        prop["name"], ""
                    )

                    # update the property value
                    prop["value"] = val

        else:

            for name, val in default_properties:

                # check if property value is given in input
                if name in input_properties:
                    val = str(val)

                val = val + property_units.get(name, "")

                spec = {"name": name, "value": val}
                properties.append(spec)

        return properties, None


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
            "backup_policy",
        ]

        # create action arguments
        for arg in args:
            if arg in config:
                spec = {"name": arg, "value": config[arg]}
                action_arguments.append(spec)

        action_arguments.append({
            "name": "postgres_software_home",
            "value": config["software_path"]
        })

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
            "backup_policy": "",
            "failover_mode": "",
            "archive_wal_expire_days": "",
            "enable_synchronous_mode": False,
            "enable_peer_auth": False,
            "node_type": "database",
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

    def build_spec_db_instance_additional_vms(self, payload, config):
        ha_proxy = config.get("ha_proxy")

        # validations
        if not ha_proxy.get("cluster"):
            return None, "cluster info is required for ha proxy"

        if not ha_proxy.get("name"):
            return None, "name is required for ha proxy"

        ha_proxy["node_type"] = "haproxy"
        db_server_vm = DBServerVM(self.module)
        payload, err = db_server_vm.build_spec_vms(payload, [ha_proxy])
        if err:
            return None, err
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
