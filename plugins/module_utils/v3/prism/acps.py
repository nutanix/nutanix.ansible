# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ..constants import ACP as CONSTANTS
from .prism import Prism
from .roles import Role, get_role_uuid


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

    def _get_cluster_access_spec(self, clusters):
        cluster_access_spec = {
            "operator": "IN",
            "left_hand_side": {"entity_type": "cluster"},
            "right_hand_side": {"uuid_list": clusters},
        }
        return cluster_access_spec

    def _get_project_access_spec(self, project_uuids, scope_level=False):
        project_access_spec = {
            "operator": "IN",
            "right_hand_side": {"uuid_list": project_uuids},
            "left_hand_side": {"entity_type": "project"},
        }
        if scope_level:
            project_access_spec["left_hand_side"] = "PROJECT"
        return project_access_spec

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
                        entity_filter["left_hand_side"] = {"entity_type": item["lhs"]}
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

    def build_role_permissions_based_context(self, role_uuid):

        # get assigned permission name for given role
        role = Role(self.module)
        role_info = role.read(role_uuid)
        role_permissions = (role_info["status"]["resources"]).get(
            "permission_reference_list", []
        )
        role_permissions_names = []
        for permission in role_permissions:
            if permission.get("name"):
                role_permissions_names.append(permission["name"])

        # Get predefined premissions to entity access expressions from constants
        expressions_dict = CONSTANTS.EntityFilterExpressionList.PERMISSION_TO_ACCESS_MAP
        permission_names = expressions_dict.keys()

        # Add entity access expressions based on permissions assigned to role
        entity_expressions = []
        for permission in permission_names:
            if permission in role_permissions_names:
                entity_expressions.append(deepcopy(expressions_dict[permission]))

        context = {"entity_filter_expression_list": entity_expressions}
        return context

    def build_role_based_filter_list(
        self, role, project_uuids, cluster_uuids=None, collab=False
    ):
        if not role.get("name") and not role.get("uuid"):
            return None, "Provide role name or uuid for creating custom acp filter list"

        role_uuid, err = get_role_uuid(role, self.module)
        if err:
            return None, err

        role_name = role.get("name")
        if not role_name:
            _role = Role(self.module)
            resp = _role.read(uuid=role_uuid)
            role_name = resp["status"]["name"]

        project_scope_level_access_config = self._get_project_access_spec(
            project_uuids, scope_level=True
        )

        # ACP context list consists of:
        # 1. Collaboration based project access
        # 2. Role permissions based access
        # 3. Default access to all roles

        # collaboration ON or OFF based context
        collab_access = ""
        if collab:
            collab_access = "ALL"
        else:
            collab_access = "SELF_OWNED"
        collab_context = {
            "scope_filter_expression_list": [
                deepcopy(project_scope_level_access_config)
            ],
            "entity_filter_expression_list": [
                {
                    "operator": "IN",
                    "left_hand_side": {"entity_type": collab_access},
                    "right_hand_side": {"collection": collab_access},
                }
            ],
        }

        # default context containing entity access expressions in give project scope needs to be added for all roles
        default_context = {
            "scope_filter_expression_list": [
                deepcopy(project_scope_level_access_config)
            ],
            "entity_filter_expression_list": deepcopy(
                CONSTANTS.EntityFilterExpressionList.DEFAULT
            ),
        }

        # role based entity access expressions context based on the permissions it have
        role_based_context = {}
        if role_name == "Project Admin":

            role_based_context = {
                "entity_filter_expression_list": deepcopy(
                    CONSTANTS.EntityFilterExpressionList.PROJECT_ADMIN
                )
            }
            role_based_context["entity_filter_expression_list"].append(
                self._get_project_access_spec(project_uuids)
            )

        elif role_name == "Developer":
            role_based_context = {
                "entity_filter_expression_list": deepcopy(
                    CONSTANTS.EntityFilterExpressionList.DEVELOPER
                )
            }

        elif role_name == "Consumer":
            role_based_context = {
                "entity_filter_expression_list": deepcopy(
                    CONSTANTS.EntityFilterExpressionList.CONSUMER
                )
            }

        elif role_name == "Operator":
            role_based_context = {
                "entity_filter_expression_list": deepcopy(
                    CONSTANTS.EntityFilterExpressionList.OPERATOR
                )
            }

        else:
            role_based_context = self.build_role_permissions_based_context(role_uuid)

        # scope is global for role based entity access
        role_based_context["scope_filter_expression_list"] = []

        # give access to project based whitelisted clusters
        if cluster_uuids:
            role_based_context["entity_filter_expression_list"].append(
                self._get_cluster_access_spec(cluster_uuids)
            )

        filter_list = {
            "context_list": [collab_context, role_based_context, default_context]
        }
        return filter_list, None
