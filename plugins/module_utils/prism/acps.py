# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism


class ACP(Prism):
    def __init__(self, module):
        resource_type = "/access_control_policies"
        super(ACP, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "role": self._build_spec_role,
            "user": self._build_spec_user,
            "user_group": self._build_spec_user_group,
            "filters": self._build_spec_filters,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {
                    "kind": "access_control_policy",
                },
                "spec": {
                    "name": None,
                    "resources": {
                    },
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None

    def _build_spec_role(self, payload, config):
        if config.get("uuid"):
            payload["spec"]["resources"]["role_reference"] = {
                "kind": "role",
                "uuid": config["uuid"]
            }
        return payload, None

    def _build_spec_user(self, payload, config):
        if config.get("uuid"):
            payload["spec"]["resources"]["user_reference_list"] = [{
                "kind": "user",
                "uuid": config["uuid"]
            }]
        return payload, None

    def _build_spec_user_group(self, payload, config):
        user_group_reference_list = []
        for item in config:
            if item.get("uuid"):
                user_group_reference_list.append({
                    "kind": "user_group",
                    "uuid": item["uuid"]
                })
        payload["spec"]["resources"]["user_group_reference_list"] = user_group_reference_list
        return payload, None

    def _build_spec_filters(self, payload, config):
        filter_list = []
        for item in config:
            filter = {}
            if item.get("scope_filter"):
                scope_filter = {}
                if item["scope_filter"].get("lhs"):
                    scope_filter["left_hand_side"] = item["scope_filter"]["lhs"]
                if item["scope_filter"].get("operator"):
                    scope_filter["operator"] = item["scope_filter"]["operator"]
                if item["scope_filter"].get("rhs"):
                    scope_filter["right_hand_side"] = item["scope_filter"]["rhs"]

                if scope_filter:
                    filter["scope_filter_expression_list"] = scope_filter

            if item.get("entity_filter"):
                entity_filter = {}
                if item["entity_filter"].get("lhs"):
                    entity_filter["left_hand_side"] = {"entity_type": item["entity_filter"]["lhs"]}
                if item["entity_filter"].get("operator"):
                    entity_filter["operator"] = item["entity_filter"]["operator"]
                if item["entity_filter"].get("rhs"):
                    entity_filter["right_hand_side"] = item["entity_filter"]["rhs"]

                if entity_filter:
                    filter["entity_filter_expression_list"] = entity_filter
            if filter:
                filter_list.append(filter)
        payload["spec"]["resources"]["filter_list"] = {"context_list": filter_list}
        return payload, None
