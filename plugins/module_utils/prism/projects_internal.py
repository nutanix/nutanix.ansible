# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

import uuid as _uuid
from copy import deepcopy

from .acps import ACP
from .clusters import Cluster
from .idempotence_identifiers import IdempotenceIdenitifiers
from .prism import Prism
from .roles import get_role_uuid
from .subnets import Subnet, get_subnet_uuid
from .user_groups import UserGroup
from .users import User

__metaclass__ = type


class ProjectsInternal(Prism):

    project_uuid = ""

    def __init__(self, module, uuid=""):

        # project uuid is required when we create acps
        if uuid:
            self.project_uuid = uuid

        resource_type = "/projects_internal"
        super(ProjectsInternal, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "resource_limits": self._build_spec_resource_limits,
            "clusters": self._build_spec_cluster_reference_list,
            "default_subnet": self._build_spec_default_subnet,
            "subnets": self._build_spec_subnets,
            "role_mappings": self._build_spec_role_mappings,
        }

    def create(
        self,
        data=None,
        endpoint=None,
        query=None,
        method="POST",
        raise_error=True,
        no_response=False,
        timeout=30,
    ):
        if not data["metadata"].get("uuid"):
            data["metadata"]["uuid"] = self.project_uuid

        if not self.project_uuid:
            self.module.fail_json(
                error="Error creating project. Project UUID is not set"
            )

        return super().create(
            data, endpoint, query, method, raise_error, no_response, timeout
        )

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "project", "uuid": None},
                "spec": {
                    "project_detail": {
                        "name": None,
                        "resources": {},
                    },
                    "user_list": [],
                    "user_group_list": [],
                    "access_control_policy_list": [],
                },
            }
        )

    def _get_project_new_acp_spec(self):
        return deepcopy(
            {
                "operation": "ADD",
                "metadata": {
                    "kind": "access_control_policy",
                },
                "acp": {
                    "name": None,
                    "resources": {
                        "role_reference": {
                            "kind": "role",
                            "uuid": None,
                        },
                        "user_reference_list": [],
                        "filter_list": {},
                        "user_group_reference_list": [],
                    },
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["project_detail"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["project_detail"]["description"] = desc
        return payload, None

    def _build_spec_resource_limits(self, payload, resource_limits):
        payload["spec"]["project_detail"]["resources"]["resource_domain"] = {}
        payload["spec"]["project_detail"]["resources"]["resource_domain"][
            "resources"
        ] = resource_limits
        return payload, None

    def _build_spec_cluster_reference_list(self, payload, cluster_ref_list):
        cluster_reference_specs = []
        for uuid in cluster_ref_list:
            cluster_reference_specs.append(Cluster.build_cluster_reference_spec(uuid))
        payload["spec"]["project_detail"]["resources"][
            "cluster_reference_list"
        ] = cluster_reference_specs
        return payload, None

    def _build_spec_default_subnet(self, payload, subnet_ref):
        uuid, err = get_subnet_uuid(subnet_ref, self.module)
        if err:
            return None, err

        payload["spec"]["project_detail"]["resources"][
            "default_subnet_reference"
        ] = Subnet.build_subnet_reference_spec(uuid)
        return payload, None

    def _build_spec_subnets(self, payload, subnet_ref_list):
        subnet_reference_specs = []
        for ref in subnet_ref_list:
            uuid, err = get_subnet_uuid(ref, self.module)
            if err:
                return None, err
            subnet_reference_specs.append(Subnet.build_subnet_reference_spec(uuid))
        payload["spec"]["project_detail"]["resources"][
            "subnet_reference_list"
        ] = subnet_reference_specs
        return payload, None

    # Build user and user groups create config to add them to PC
    def _build_spec_user_and_user_groups_list(self, payload, role_mappings):

        # This spec is only configured when new users and user groups are needed to create in pc
        new_uuids_required = 0
        for role_mapping in role_mappings:
            if role_mapping.get("user") and not role_mapping["user"].get("uuid"):
                new_uuids_required += 1
            if role_mapping.get("user_group") and not role_mapping["user_group"].get(
                "uuid"
            ):
                new_uuids_required += 1

        ii = IdempotenceIdenitifiers(self.module)
        new_uuid_list = ii.get_idempotent_uuids(new_uuids_required)
        if len(new_uuid_list) < new_uuids_required:
            return None, "Required count of new uuids: {0}, got {1}".format(
                new_uuids_required, len(new_uuid_list)
            )

        _user = User(self.module)
        _user_group = UserGroup(self.module)
        users = []
        user_groups = []
        name_uuid_map = {}
        for role_mapping in role_mappings:
            if role_mapping.get("user") and not role_mapping["user"].get("uuid"):
                user, err = _user.get_spec(params=role_mapping["user"])
                if err:
                    return None, err
                user["user"] = user.pop("spec")
                user["metadata"]["uuid"] = new_uuid_list.pop()
                user["operation"] = "ADD"
                users.append(user)
                name = role_mapping["user"].get("username") or role_mapping["user"].get(
                    "principal_name"
                )
                name_uuid_map[name] = user["metadata"]["uuid"]

            if role_mapping.get("user_group") and not role_mapping["user_group"].get(
                "uuid"
            ):
                user_group, err = _user_group.get_spec(
                    params=role_mapping["user_group"]
                )
                if err:
                    return None, err
                user_group["user_group"] = user_group.pop("spec")
                user_group["metadata"]["uuid"] = new_uuid_list.pop()
                user_group["operation"] = "ADD"
                user_groups.append(user_group)
                name = role_mapping.get("distinguished_name") or role_mapping.get(
                    "idp", {}
                ).get("group_name")
                name_uuid_map[name] = user_group["metadata"]["uuid"]

        payload["spec"]["user_list"] = users
        payload["spec"]["user_group_list"] = user_groups
        return name_uuid_map, None

    def _build_spec_role_mappings(self, payload, role_mappings):

        if not self.project_uuid:
            return (
                None,
                "Set ProjectsInternal.project_uuid for generating role mapping spec in project",
            )

        payload["spec"]["project_detail"]["resources"]["user_reference_list"] = []
        payload["spec"]["project_detail"]["resources"][
            "external_user_group_reference_list"
        ] = []

        # Create new user and user groups config if required
        # new_users_groups_name_uuid_map will help in acp creation
        (
            new_users_groups_name_uuid_map,
            err,
        ) = self._build_spec_user_and_user_groups_list(payload, role_mappings)
        if err:
            return None, err

        collab = self.module.params["collaboration"]
        cluster_uuids = self.module.params["clusters"]

        # One ACP is required for each role and associated user/user groups
        # If there is an exiting ACP for a role in project, UPDATE  or DELETE it as per given role_mapping
        # If there is no ACP for a given role in projects, create a new ACP for that role

        # Create role_user_groups_map for role_uuid -> users and user_groups references
        # Maintain role_name_uuid_map to store uuid of role and save get uuid api calls
        role_name_uuid_map = {}
        role_user_groups_map = {}
        for role_mapping in role_mappings:
            role_uuid = ""

            if role_mapping["role"].get("name"):

                # If role name given, check for uuid from role_name_uuid_map else get from pc
                if not role_name_uuid_map.get(role_mapping["role"]["name"]):
                    role_uuid, err = get_role_uuid(role_mapping["role"], self.module)
                    if err:
                        return None, err
                    role_name_uuid_map[role_mapping["role"]["name"]] = role_uuid
                else:
                    role_uuid = role_name_uuid_map[role_mapping["role"]["name"]]
            else:
                role_uuid = role_mapping["role"]["uuid"]

            # create structure if new role entry is required
            if not role_user_groups_map.get(role_uuid):
                role_user_groups_map[role_uuid] = {"users": [], "user_groups": []}

            # Add user/user_group references to particular role
            if role_mapping.get("user"):
                user_ref = {"uuid": "", "kind": "user"}
                if role_mapping["user"].get("uuid"):
                    uuid = role_mapping["user"]["uuid"]
                    user_ref["uuid"] = uuid
                    payload["spec"]["project_detail"]["resources"][
                        "user_reference_list"
                    ].append(user_ref)

                else:
                    name = role_mapping["user"].get("username") or role_mapping[
                        "user"
                    ].get("principal_name")
                    uuid = new_users_groups_name_uuid_map[name]
                    user_ref["uuid"] = uuid
                role_user_groups_map[role_uuid]["users"].append(user_ref)
            else:
                user_group_ref = {"uuid": "", "kind": "user_group"}
                if role_mapping["user_group"].get("uuid"):
                    uuid = role_mapping["user_group"]["uuid"]
                    user_group_ref["uuid"] = uuid
                    payload["spec"]["project_detail"]["resources"][
                        "external_user_group_reference_list"
                    ].append(user_group_ref)

                else:
                    name = role_mapping.get("distinguished_name") or role_mapping.get(
                        "idp", {}
                    ).get("group_name")
                    uuid = new_users_groups_name_uuid_map[name]
                    user_group_ref["uuid"] = uuid

                role_user_groups_map[role_uuid]["user_groups"].append(user_group_ref)

        _acp = ACP(self.module)

        # first check existing acps of project if UPDATE/DELETE of acp is required
        for acp in payload["spec"]["access_control_policy_list"]:

            # if acp for role is required then UPDATE(users, user groups and context) else DELETE acp
            if (
                acp["acp"]["resources"]["role_reference"]["uuid"]
                not in role_user_groups_map
            ):
                acp["operation"] = "DELETE"
                acp["acp"]["resources"]["user_reference_list"] = []
                acp["acp"]["resources"]["user_group_reference_list"] = []
            else:
                acp["operation"] = "UPDATE"
                (
                    acp["acp"]["resources"]["filter_list"],
                    err,
                ) = _acp.build_role_based_filter_list(
                    acp["acp"]["resources"]["role_reference"],
                    [self.project_uuid],
                    cluster_uuids,
                    collab,
                )
                if err:
                    return None, err
                acp["acp"]["resources"]["user_reference_list"] = role_user_groups_map[
                    acp["acp"]["resources"]["role_reference"]["uuid"]
                ]["users"]
                acp["acp"]["resources"][
                    "user_group_reference_list"
                ] = role_user_groups_map[
                    acp["acp"]["resources"]["role_reference"]["uuid"]
                ][
                    "user_groups"
                ]

                # pop the role uuid entry once used for acp update
                role_user_groups_map.pop(
                    acp["acp"]["resources"]["role_reference"]["uuid"]
                )

        # iterate for remaining role uuids in role_user_groups_map to create new acps for them
        for role_uuid, val in role_user_groups_map.items():
            acp = self._get_project_new_acp_spec()
            acp["acp"]["name"] = "ansible-{0}".format(str(_uuid.uuid4()))
            acp["acp"]["resources"]["role_reference"] = {
                "kind": "role",
                "uuid": role_uuid,
            }
            acp["acp"]["resources"]["user_reference_list"] = val["users"]
            acp["acp"]["resources"]["user_group_reference_list"] = val["user_groups"]
            (
                acp["acp"]["resources"]["filter_list"],
                err,
            ) = _acp.build_role_based_filter_list(
                acp["acp"]["resources"]["role_reference"],
                [self.project_uuid],
                cluster_uuids,
                collab,
            )
            if err:
                return None, err
            payload["spec"]["access_control_policy_list"].append(acp)

        return payload, None


def get_project_uuid(module, config):
    if "name" in config:
        project = ProjectsInternal(module)
        name = config["name"]
        uuid = project.get_uuid(name)
        if not uuid:
            error = "Project {0} not found.".format(name)
            return None, error

    elif "uuid" in config:
        uuid = config["uuid"]

    return uuid, None
