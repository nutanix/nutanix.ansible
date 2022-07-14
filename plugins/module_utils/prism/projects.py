# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .user_groups import get_user_group_reference_spec
from .subnets import get_subnet_reference_spec, get_subnet_uuid
from .users import get_user_reference_spec
from .spec.categories_mapping import CategoriesMapping

__metaclass__ = type

from .prism import Prism


class Projects(Prism):
    def __init__(self, module):
        resource_type = "/projects"
        super(Projects, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "remove_categories": CategoriesMapping.build_remove_all_categories_spec,
            "categories": CategoriesMapping.build_categories_mapping_spec,
            "resource_limits": self._build_spec_resource_limits,
            "default_subnet_reference": self._build_spec_default_subnet_reference,
            "subnet_reference_list": self._build_spec_subnet_reference_list,
            "user_uuid_list": self._build_spec_user_reference_list,
            "external_user_group_uuid_list": self._build_spec_external_user_group_reference_list
        }

    def validate_project_name_exists(self, name):
        uuid = self.get_uuid(name)
        if uuid:
            return True
        return False

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "project"},
                "spec": {
                    "name": None,
                    "resources": {},
                },
            }
        )

    def _build_spec_name(self, payload, name):
        payload["spec"]["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["spec"]["description"] = desc
        return payload, None
    
    def _build_spec_resource_limits(self, payload, resource_limits):
        payload["spec"]["resources"]["resource_domain"] = {}
        payload["spec"]["resources"]["resource_domain"]["resources"] = resource_limits
        return payload, None
    
    def _build_spec_default_subnet_reference(self, payload, subnet_ref):
        uuid, err = get_subnet_uuid(subnet_ref, self.module)
        if err:
            return None, err
    
        payload["spec"]["resources"]["default_subnet_reference"] = get_subnet_reference_spec(uuid)
        return payload, None
    
    def _build_spec_subnet_reference_list(self, payload, subnet_ref_list):
        subnet_reference_specs = []
        for ref in subnet_ref_list:
            uuid, err = get_subnet_uuid(ref, self.module)
            if err:
                return None, err
            subnet_reference_specs.append(get_subnet_reference_spec(uuid))
        payload["spec"]["resources"]["subnet_reference_list"] = subnet_reference_specs
        return payload, None
        
    def _build_spec_user_reference_list(self, payload, user_uuid_list):
        user_reference_specs = []
        for uuid in user_uuid_list:
            user_reference_specs.append(get_user_reference_spec(uuid))
        payload["spec"]["resources"]["user_reference_list"] = user_reference_specs
        return payload, None
    
    def _build_spec_external_user_group_reference_list(self, payload, ext_user_uuid_list):
        user_groups_reference_specs = []
        for uuid in ext_user_uuid_list:
            user_groups_reference_specs.append(get_user_group_reference_spec(uuid))
        payload["spec"]["resources"]["external_user_group_reference_list"] = user_groups_reference_specs
        return payload, None
    