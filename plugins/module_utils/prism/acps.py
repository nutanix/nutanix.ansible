# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism
from .roles import get_role_uuid


class ACP(Prism):
    def __init__(self, module):
        resource_type = "/access_control_policies"
        super(ACP, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "role": self._build_spec_role,
            "user_uuids": self._build_spec_user,
            "user_group_uuids": self._build_spec_user_group,
            "filters": self._build_spec_filters,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "access_control_policy"},
                "spec": {"name": None, "resources": {}},
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None

    def _build_spec_role(self, payload, config):
        uuid, error = get_role_uuid(config, self.module)
        if error:
             return None, error
        payload["spec"]["resources"]["role_reference"] = {"kind": "role", "uuid": uuid}
        return payload, None

    def _build_spec_user(self, payload, config):
        user_reference_list = []
        for item in config:
            user_reference_list.append({"kind": "user", "uuid": item})
        payload["spec"]["resources"]["user_reference_list"] = user_reference_list
        return payload, None

    def _build_spec_user_group(self, payload, config):
        user_group_reference_list = []
        for item in config:
            user_group_reference_list.append({"kind": "user_group", "uuid": item})
        payload["spec"]["resources"][
            "user_group_reference_list"
        ] = user_group_reference_list
        return payload, None

    def _build_spec_filters(self, payload, config):
        filter_list = []
        for filter in config:
            filter_spec = {}
            if filter.get("scope_filter"):
                scope_filters = []
                for item in filter["scope_filter"]:
                    scope_filter = {}
                    if item.get("lhs"):
                        scope_filter["left_hand_side"] = item["lhs"]
                    if item.get("operator"):
                        scope_filter["operator"] = item["operator"]
                    if item.get("rhs"):
                        scope_filter["right_hand_side"] = item["rhs"]

                    if scope_filter:
                        scope_filters.append(scope_filter)
                if scope_filters:
                    filter_spec["scope_filter_expression_list"] = scope_filters

            if filter.get("entity_filter"):
                entity_filters = []
                for item in filter["entity_filter"]:
                    entity_filter = {}
                    if item.get("lhs"):
                        entity_filter["left_hand_side"] = {
                            "entity_type": item["lhs"]
                        }
                    if item.get("operator"):
                        entity_filter["operator"] = item["operator"]
                    if item.get("rhs"):
                        entity_filter["right_hand_side"] = item["rhs"]

                    if entity_filter:
                        entity_filters.append(entity_filter)
                if entity_filters:
                    filter_spec["entity_filter_expression_list"] = entity_filters
            if filter_spec:
                filter_list.append(filter_spec)
        payload["spec"]["resources"]["filter_list"] = {"context_list": filter_list}
        return payload, None
