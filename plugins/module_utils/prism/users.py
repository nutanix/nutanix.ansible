# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism
from .projects import Project
from .spec.categories_mapping import CategoriesMapping


class Users(Prism):
    kind = "user"

    def __init__(self, module):
        resource_type = "/users"
        super(Users, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "project": self._build_spec_project,
            "principal_name": self._build_spec_principal_name,
            "directory_service_uuid": self._build_spec_directory_service,
            "username": self._build_spec_username,
            "identity_provider_uuid": self._build_spec_identity_provider,
            "categories": CategoriesMapping.build_categories_mapping_spec,
            "remove_categories": CategoriesMapping.build_remove_all_categories_spec,
        }
    
    def _get_default_spec(self):
        return deepcopy(
            {
                "metadata": {"kind": "user"},
                "spec": {
                    "resources": {
                        "directory_service_user": {},
                        "identity_provider_user": {},
                    }
                },
            }
        )

    def _build_spec_project(self, payload, config):
        if "name" in config:
            project = Project(self.module)
            name = config["name"]
            uuid = project.get_uuid(name)
            if not uuid:
                error = "Project {0} not found.".format(name)
                return None, error

        elif "uuid" in config:
            uuid = config["uuid"]

        payload["metadata"].update(
            {"project_reference": {"uuid": uuid, "kind": "project"}}
        )
        return payload, None

    def _build_spec_principal_name(self, payload, config):
        payload["spec"]["resources"]["directory_service_user"].update({
            "user_principal_name": config,
        })
        return payload, None

    def _build_spec_directory_service(self, payload, config):
        payload["spec"]["resources"]["directory_service_user"].update({
            "directory_service_reference":
                {
                    "kind": "directory_service",
                    "uuid": config,
                }
        })
        payload["spec"]["resources"].pop("identity_provider_user")
        return payload, None

    def _build_spec_username(self, payload, config):
        payload["spec"]["resources"]["identity_provider_user"].update({"username": config})
        return payload, None

    def _build_spec_identity_provider(self, payload, config):
        payload["spec"]["resources"]["identity_provider_user"].update({
            "identity_provider_reference": {
                "kind": "identity_provider",
                "uuid": config,
            }
        })
        payload["spec"]["resources"].pop("directory_service_user")
        return payload, None
    
    @classmethod
    def build_user_reference_spec(cls, uuid):
        spec = {"kind": cls.kind, "uuid": uuid}
        return spec
