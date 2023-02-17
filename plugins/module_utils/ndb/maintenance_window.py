# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

__metaclass__ = type


from .db_server_cluster import DBServerCluster
from .db_server_vm import DBServerVM
from .nutanix_database import NutanixDatabase


class MaintenanceWindow(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/maintenance"
        super(MaintenanceWindow, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "schedule": self._build_spec_schedule,
        }

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
            data, uuid, endpoint, query, raise_error, no_response, timeout, method
        )

    def update_tasks(self, data):
        endpoint = "tasks"
        return super().create(data=data, endpoint=endpoint)

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        resp = self.read()
        for entity in resp:
            if entity.get(key) == value:
                return entity.get("id"), None

        return None, "Maintenance window with name {0} not found.".format(value)

    def get_maintenance_window_uuid(self, config):
        if "name" in config:
            name = config["name"]
            uuid, err = self.get_uuid(value=name)
            if err:
                return None, err
        elif "uuid" in config:
            uuid = config["uuid"]
        else:
            error = "Config {0} doesn't have name or uuid key".format(config)
            return None, error

        return uuid, None

    def get_spec(self, old_spec=None, params=None, **kwargs):
        if kwargs.get("configure_automated_patching"):
            return self.get_spec_for_automated_patching(
                old_spec=old_spec, params=params, **kwargs
            )

        else:
            return super().get_spec(old_spec=old_spec, params=params, **kwargs)

    def _get_default_spec(self):
        return deepcopy({"name": "", "description": "", "timezone": "", "schedule": {}})

    def get_default_update_spec(self, override_spec=None):
        spec = {
            "name": "",
            "description": "",
            "timezone": "",
            "schedule": {},
            "resetSchedule": True,
            "resetDescription": True,
            "resetName": True,
        }
        if override_spec:
            for key in spec:
                if key in override_spec:
                    spec[key] = override_spec[key]

        return spec

    def get_default_automated_patching_spec(self):
        return deepcopy({"maintenanceWindowId": "", "tasks": []})

    def get_spec_for_automated_patching(self, old_spec=None, params=None, **kwargs):
        config = params or self.module.params.get("automated_patching", {})

        payload = old_spec
        if not payload:
            payload = self.get_default_automated_patching_spec()

        self.build_spec_methods = {
            "maintenance_window": self._build_spec_maintenance_window,
            "tasks": self._build_spec_tasks,
            "db_server_vms": self._build_spec_db_server_vms,
            "db_server_clusters": self._build_spec_db_server_clusters,
        }
        return super().get_spec(old_spec=payload, params=config, **kwargs)

    def _build_spec_name(self, payload, name):

        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):

        payload["description"] = desc
        return payload, None

    def _build_spec_schedule(self, payload, schedule):
        spec = payload.get("schedule", {})

        if schedule.get("recurrence"):
            spec["recurrence"] = schedule.get("recurrence").upper()

        if schedule.get("day_of_week"):
            spec["dayOfWeek"] = schedule.get("day_of_week").upper()

        if schedule.get("day_of_week"):
            spec["weekOfMonth"] = schedule.get("week_of_month")

        if schedule.get("duration"):
            spec["duration"] = schedule.get("duration")

        if schedule.get("start_time"):
            spec["startTime"] = schedule.get("start_time")

        payload["schedule"] = spec

        payload["timezone"] = schedule.get("timezone")
        return payload, None

    # builders for configuring automated patching
    def _build_spec_maintenance_window(self, payload, mw):
        uuid, err = self.get_maintenance_window_uuid(config=mw)
        if err:
            return None, err
        payload["maintenanceWindowId"] = uuid
        return payload, err

    def _build_spec_tasks(self, payload, tasks):
        specs = payload.get("tasks", [])
        for task in tasks:
            spec = {}

            if task.get("type"):
                spec["taskType"] = task.get("type")
            else:
                return (
                    None,
                    "'type' is required for setting task type in automated patching",
                )

            # set pre post commands
            spec["payload"] = {"prePostCommand": {}}
            if task.get("pre_task_cmd"):
                spec["payload"]["prePostCommand"]["preCommand"] = task.get(
                    "pre_task_cmd"
                )
            if task.get("post_task_cmd"):
                spec["payload"]["prePostCommand"]["postCommand"] = task.get(
                    "post_task_cmd"
                )

            specs.append(spec)

        payload["tasks"] = specs
        return payload, None

    def _build_spec_db_server_vms(self, payload, vms):
        db_server_vms = DBServerVM(self.module)
        uuids, err = db_server_vms.resolve_uuids_from_entity_specs(vms=vms)
        if err:
            return None, err

        if not payload.get("entities"):
            payload["entities"] = {}
        payload["entities"]["ERA_DBSERVER"] = uuids
        return payload, None

    def _build_spec_db_server_clusters(self, payload, clusters):
        db_server_clusters = DBServerCluster(self.module)
        cluster_name_uuid_map = db_server_clusters.get_all_clusters_name_uuid_map()

        uuids = []
        for cluster in clusters:

            if cluster.get("name"):
                if cluster_name_uuid_map.get(cluster["name"]):
                    uuid = cluster_name_uuid_map[cluster["name"]]
                else:
                    return None, "DB server cluster with name '{0}' not found".format(
                        cluster["name"]
                    )

            elif cluster.get("uuid"):
                uuid = cluster["uuid"]
            else:
                return (
                    None,
                    "uuid or name is required for setting db server cluster uuid",
                )

            uuids.append(uuid)

        if not payload.get("entities"):
            payload["entities"] = {}
        payload["entities"]["ERA_DBSERVER_CLUSTER"] = uuids
        return payload, None


class AutomatedPatchingSpec:
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    task = dict(
        type=dict(type="str", choices=["OS_PATCHING", "DB_PATCHING"], required=False),
        pre_task_cmd=dict(type="str", required=False),
        post_task_cmd=dict(type="str", required=False),
    )

    automated_patching_argument_spec = dict(
        maintenance_window=dict(
            type="dict",
            options=entity_by_spec,
            mutuallu_exclusive=mutually_exclusive,
            required=False,
        ),
        tasks=dict(type="list", elements="dict", options=task, required=False),
    )
