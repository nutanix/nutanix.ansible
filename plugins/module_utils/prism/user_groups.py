# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from .prism import Prism
from .projects import Project
from .spec.categories_mapping import CategoriesMapping


class UserGroups(Prism):
    def __init__(self, module):
        resource_type = "/user_groups"
        super(UserGroups, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "project": self._build_spec_project,
            "distinguished_name": self._build_spec_user_distinguished_name,
            "idp": self._build_spec_saml_user_group,
            "categories": CategoriesMapping.build_categories_mapping_spec,
            "remove_categories": CategoriesMapping.build_remove_all_categories_spec,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "metadata": {"kind": "user_group"},
                "spec": {"resources": {}},
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

    def _build_spec_user_distinguished_name(self, payload, config):
        if "ou=" in config:
            payload["spec"]["resources"]["directory_service_ou"] = {
                "distinguished_name": config
            }
        else:
            payload["spec"]["resources"]["directory_service_user_group"] = {
                "distinguished_name": config
            }

        return payload, None

    def _build_spec_saml_user_group(self, payload, config):
        payload["spec"]["resources"]["saml_user_group"] = {
            "name": config["group_name"],
            "idpUuid": config["idp_uuid"],
        }
        return payload, None
