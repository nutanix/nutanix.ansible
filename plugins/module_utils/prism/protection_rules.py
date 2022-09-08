# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from ..utils import convert_to_secs
from .prism import Prism

__metaclass__ = type


class ProtectionRule(Prism):
    def __init__(self, module):
        resource_type = "/protection_rules"
        super(ProtectionRule, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "start_time": self._build_spec_start_time,
            "protected_categories": self._build_spec_protected_categories,
            "schedules": self._build_spec_schedules,
        }

    def get_affected_entities(self, rule_uuid):
        return self.read(uuid=rule_uuid, endpoint="query_entities")

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "protection_rule"},
                "spec": {
                    "resources": {
                        "availability_zone_connectivity_list": [],
                        "ordered_availability_zone_list": [],
                        "category_filter": {
                            "params": {},
                            "type": "CATEGORIES_MATCH_ANY",
                        },
                        "primary_location_list": [],
                    },
                    "name": None,
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None

    def _build_spec_start_time(self, payload, start_time):
        payload["spec"]["resources"]["start_time"] = start_time
        return payload, None

    def _build_spec_protected_categories(self, payload, categories):
        payload["spec"]["resources"]["category_filter"]["params"] = categories
        return payload, None

    def _build_spec_schedules(self, payload, schedules):
        ordered_az_list = []
        az_connectivity_list = []

        if self.module.params.get("primary_site"):
            ordered_az_list.append(self.module.params["primary_site"])
        elif len(payload["spec"]["resources"]["primary_location_list"]) == 0:
            return None, "Please provide primary_site spec"

        # create ordered_availability_zone_list
        for schedule in schedules:
            if schedule.get("source") and schedule["source"] not in ordered_az_list:
                ordered_az_list.append(schedule["source"])
            if (
                schedule.get("destination")
                and schedule["destination"] not in ordered_az_list
            ):
                ordered_az_list.append(schedule["destination"])
        payload["spec"]["resources"]["ordered_availability_zone_list"] = ordered_az_list

        if self.module.params.get("primary_site"):
            payload["spec"]["resources"]["primary_location_list"] = [
                ordered_az_list.index(self.module.params["primary_site"])
            ]

        # create availability_zone_connectivity_list from schedules
        for schedule in schedules:
            az_connection_spec = {}
            spec = {}
            if schedule.get("source"):
                az_connection_spec[
                    "source_availability_zone_index"
                ] = ordered_az_list.index(schedule["source"])
            if schedule.get("destination"):
                az_connection_spec[
                    "destination_availability_zone_index"
                ] = ordered_az_list.index(schedule["destination"])

            if schedule["protection_type"] == "ASYNC":
                if (
                    not (schedule.get("rpo") and schedule.get("rpo_unit"))
                    and schedule.get("snapshot_type")
                    and (
                        schedule.get("local_retention_policy")
                        or schedule.get("remote_retention_policy")
                    )
                ):
                    return (
                        None,
                        "rpo, rpo_unit, snapshot_type and atleast one policy are required fields for aysynchronous snapshot schedule",
                    )

                spec["recovery_point_objective_secs"], err = convert_to_secs(
                    schedule["rpo"], schedule["rpo_unit"]
                )
                if err:
                    return None, err

                spec["snapshot_type"] = schedule["snapshot_type"]
                if schedule.get("local_retention_policy"):
                    spec["local_snapshot_retention_policy"] = schedule[
                        "local_retention_policy"
                    ]
                if schedule.get("remote_retention_policy"):
                    spec["remote_snapshot_retention_policy"] = schedule[
                        "remote_retention_policy"
                    ]
            else:
                if schedule.get("auto_suspend_timeout"):
                    spec["auto_suspend_timeout_secs"] = schedule["auto_suspend_timeout"]
                spec["recovery_point_objective_secs"] = 0
            az_connection_spec["snapshot_schedule_list"] = [spec]
            az_connectivity_list.append(az_connection_spec)

        payload["spec"]["resources"][
            "availability_zone_connectivity_list"
        ] = az_connectivity_list
        return payload, None
