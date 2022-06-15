# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism
from .projects import Project


class SecurityRule(Prism):
    def __init__(self, module):
        resource_type = "/network_security_rules"
        super(SecurityRule, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "project": self._build_spec_project,
            "allow_ipv6_traffic": self._build_allow_ipv6_traffic,
            "is_policy_hitlog_enabled": self._build_is_policy_hitlog_enabled,
            "ad_rule": self._build_ad_rule,
            "app_rule": self._build_app_rule,
            "isolation_rule": self._build_isolation_rule,
            "quarantine_rule": self._build_quarantine_rule,
            "categories": self._build_spec_categories,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "network_security_rule"},
                "spec": {
                    "name": None,
                    "resources": {
                        # "allow_ipv6_traffic": False,
                        "is_policy_hitlog_enabled": False,
                        # "ad_rule": {},
                        # "app_rule": {},
                        # "isolation_rule": {},
                        # "quarantine_rule": {}
                    },
                },
            }
        )

    def _build_spec_name(self, payload, value):
        payload["spec"]["name"] = value
        return payload, None

    def _build_spec_desc(self, payload, value):
        payload["spec"]["description"] = value
        return payload, None

    def _build_spec_project(self, payload, param):
        if "name" in param:
            project = Project(self.module)
            name = param["name"]
            uuid = project.get_uuid(name)
            if not uuid:
                error = "Project {0} not found.".format(name)
                return None, error

        elif "uuid" in param:
            uuid = param["uuid"]

        payload["metadata"].update(
            {"project_reference": {"uuid": uuid, "kind": "project"}}
        )
        return payload, None

    def _build_allow_ipv6_traffic(self, payload, value):
        payload["spec"]["resources"]["allow_ipv6_traffic"] = value
        return payload, None

    def _build_is_policy_hitlog_enabled(self, payload, value):
        payload["spec"]["resources"]["is_policy_hitlog_enabled"] = value
        return payload, None

    def _build_ad_rule(self, payload, value):
        if payload["spec"]["resources"].get("ad_rule"):
            self._build_spec_rule(payload["spec"]["resources"]["ad_rule"], value)
        else:
            payload["spec"]["resources"]["ad_rule"] = value
        return payload, None

    def _build_app_rule(self, payload, value):
        if payload["spec"]["resources"].get("app_rule"):
            self._build_spec_rule(payload["spec"]["resources"]["app_rule"], value)
        else:
            payload["spec"]["resources"]["app_rule"] = value
        return payload, None

    def _build_isolation_rule(self, payload, value):
        if payload["spec"]["resources"].get("isolation_rule"):
            isolation_rule = payload["spec"]["resources"]["isolation_rule"]
            if value.get("first_entity_filter"):
                self._generate_filter_spec(isolation_rule["first_entity_filter"], value["first_entity_filter"])
            if value.get("second_entity_filter"):
                self._generate_filter_spec(isolation_rule["second_entity_filter"], value["second_entity_filter"])
            if value.get("action"):
                isolation_rule["action"] = value["action"]
        else:
            payload["spec"]["resources"]["isolation_rule"] = value
        return payload, None

    def _build_quarantine_rule(self, payload, value):
        if payload["spec"]["resources"].get("quarantine_rule"):
            self._build_spec_rule(payload["spec"]["resources"]["quarantine_rule"], value)
        return payload, None

    def _build_spec_categories(self, payload, value):
        payload["metadata"]["categories_mapping"] = value
        payload["metadata"]["use_categories_mapping"] = True
        return payload, None

    def _build_spec_rule(self, payload, value):
        rule = payload
        if value.get("target_group"):
            rule["target_group"] = value["target_group"]
        if value.get("inbound_allow_list"):
            self._generate_bound_spec(rule["inbound_allow_list"], value["inbound_allow_list"])
        if value.get("outbound_allow_list"):
            self._generate_bound_spec(rule["outbound_allow_list"], value["outbound_allow_list"])
        if value.get("action"):
            rule["action"] = value["action"]

        return payload, None

    def _generate_bound_spec(self, payload, list_of_rules):
        for rule in list_of_rules:
            if rule.get("rule_id"):
                rule_spec = self._filter_by_uuid(rule["rule_id"], payload)
            else:
                rule_spec = {}
            for key, value in rule.items():
                if key == "filter":
                    self._generate_filter_spec(rule_spec[key], value)
                else:
                    rule_spec[key] = value
            if not rule_spec.get("rule_id"):
                payload.append(rule_spec)

    def _generate_filter_spec(self, payload, value):
        if value.get("type"):
            payload["type"] = value["type"]
        if value.get("kind_list"):
            payload["kind_list"] = value["kind_list"]
        if value.get("params"):
            payload["params"] = value["params"]

    def _filter_by_uuid(self, uuid, items_list):
        try:
            return next(filter(lambda d: d.get("rule_id") == uuid, items_list))
        except BaseException:
            self.module.fail_json(
                msg="Failed generating VM Spec",
                error="Entity {0} not found.".format(uuid),
            )
