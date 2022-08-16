# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

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
            "ordered_availability_zones": self._build_spec_ordered_availability_zones,
            "availability_zone_connections": self._build_spec_availability_zone_connections,
            "protected_categories": self._build_spec_protected_categories
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
                        "category_filter":{
                            "params": {},
                            "type": "CATEGORIES_MATCH_ANY"
                        },
                        "primary_location_list":[0]
                    }, 
                    "name": None
                },
            }
        )

    def _convert_to_secs(self, value, unit):
        """
        This routin converts given value to time interval into seconds as per unit
        """
        conversion_multiplier = {
            "MINUTE": 60,
            "HOUR": 3600,
            "DAY": 86400,
            "WEEK": 604800
        }
        if unit not in conversion_multiplier:
            return None, "Invalid unit given for interval conversion to seconds"
        
        return value * conversion_multiplier[unit], None

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

    def _build_spec_ordered_availability_zones(self, payload, availability_zones):
        payload["spec"]["resources"]["ordered_availability_zone_list"] = availability_zones
        return payload, None
    
    def _build_spec_availability_zone_connections(self, payload, az_connections):
        availability_zone_connectivity_list = []
        for connection in az_connections:
            spec = {}

            spec["source_availability_zone_index"] = connection["source_index"]
            if connection.get("destination_index"):
                spec["destination_availability_zone_index"] = connection["destination_index"]

            snapshot_schedules = []
            for schedule in connection["snapshot_schedules"]:
                schedule_spec = {}

                if schedule["protection_type"] == "ASYNC":
                    rpo, err = self._convert_to_secs(schedule["rpo"], schedule["rpo_unit"])
                    if err:
                        return None, err
                    schedule_spec["recovery_point_objective_secs"] = rpo
                    
                    schedule_spec["snapshot_type"] = schedule["snapshot_type"]
                    
                    if schedule.get("local_retention_policy"):
                        schedule_spec["local_snapshot_retention_policy"] = schedule.get["local_retention_policy"]
                    if schedule.get("remote_retention_policy"):
                        schedule_spec["remote_snapshot_retention_policy"] = schedule.get["remote_retention_policy"]
                
                elif schedule["protection_type"] == "SYNC":
                    schedule_spec["recovery_point_objective_secs"] = 0
                    if connection.get("auto_suspend_timeout"):
                        spec["auto_suspend_timeout_secs"] = connection["auto_suspend_timeout"]

                snapshot_schedules.append(schedule_spec)
            
            spec["snapshot_schedule_list"] = snapshot_schedules
            availability_zone_connectivity_list.append(spec)
        
        payload["availability_zone_connectivity_list"] = availability_zone_connectivity_list
        return payload, None
