# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .prism import Prism
from .permissions import Permissions, get_permission_uuid

__metaclass__ = type


class Roles(Prism):
    def __init__(self, module):
        resource_type = "/roles"
        super(Roles, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "permissions": self._build_spec_permissions,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "metadata": {"kind": "role"},
                "spec": {"resources": {"permission_reference_list": []}, "name": None},
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None

    def _build_spec_permissions(self, payload, permissions):
        permission_ref_specs = []
        for permission in permissions:
            uuid, err = get_permission_uuid(permission, self.module)
            if err:
                return None, err
            permission_ref_specs.append(
                Permissions.build_permission_reference_spec(uuid)
            )
        payload["spec"]["resources"]["permission_reference_list"] = permission_ref_specs
        return payload, None


def get_role_uuid(config, module):
    if "name" in config:
        roles = Roles(module)
        name = config["name"]
        uuid = roles.get_uuid(name)
        if not uuid:

            error = "Role {0} not found.".format(name)
            return None, error

    elif "uuid" in config:
        uuid = config["uuid"]

    return uuid, None
