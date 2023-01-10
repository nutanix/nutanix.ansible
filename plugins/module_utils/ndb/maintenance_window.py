# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type


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

    def _get_default_spec(self):
        return deepcopy({"name": "", "description": "", "timezone": "", "schedule": {}})

    def get_update_spec(self, override_spec=None):
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
