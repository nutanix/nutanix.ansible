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
                    }
                }
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
        payload["spec"]["resources"]["ad_rule"] = value
        return payload, None

    def _build_app_rule(self, payload, value):
        payload["spec"]["resources"]["app_rule"] = value
        return payload, None

    def _build_isolation_rule(self, payload, value):
        payload["spec"]["resources"]["isolation_rule"] = value
        return payload, None

    def _build_quarantine_rule(self, payload, value):
        payload["spec"]["resources"]["quarantine_rule"] = value
        return payload, None

    def _build_spec_categories(self, payload, value):
        payload["metadata"]["categories_mapping"] = value
        payload["metadata"]["use_categories_mapping"] = True
        return payload, None