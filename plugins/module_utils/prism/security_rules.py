# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class SecurityRules(Prism):
    def __init__(self, module):
        resource_type = "/network_security_rules"
        super(SecurityRules, self).__init__(module, resource_type=resource_type)
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
                "metadata": {},
                "spec": {
                    "name": None,
                    "resources": {
                        "allow_ipv6_traffic": True,
                        "is_policy_hitlog_enabled": True,
                        "ad_rule": {},
                        "app_rule": {},
                        "isolation_rule": {},
                        "quarantine_rule": {}
                    }
                }
            }
        )
