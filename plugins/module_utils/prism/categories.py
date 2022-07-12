# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .prism import Prism

__metaclass__ = type


class Categories(Prism):
    def __init__(self, module):

        resource_type = "/categories"
        super(Categories, self).__init__(
            module, resource_type=resource_type
        )

class CategoryKey(Categories):
    def __init__(self, module):
        super(CategoryKey, self).__init__(
            module
        )
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc
        }
    
    def list(self, name):
        data = {
            "kind": "category"
        }
        endpoint = "{0}/list".format(name)
        return super().list(data=data, use_base_url=True, endpoint=endpoint)
    
    def create(self, name, data):
        return super().create(data=data, endpoint=name, method="PUT")
    
    def get_spec(self, old_spec=None):
        if old_spec:
            key_spec = self._strip_extra_attributes_from_key_spec(old_spec)
            return super().get_spec(old_spec=key_spec)
        return super().get_spec()

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "name": None,
            }
        )

    def _strip_extra_attributes_from_key_spec(self, key_spec):
        spec = {}
        default_spec = {
            "api_version": "3.1.0",
            "name": None,
            "description": None
        }
        for k in default_spec:
            v = key_spec.get(k)
            if v:
                spec[k] = v

        return spec

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None


class CategoryValue(Categories):
    def __init__(self, module):
        super(CategoryValue, self).__init__(
            module
        )
    
    def create(self, name, data):
        endpoint = "{0}/{1}".format(name, data["value"])
        return super().create(data=data, endpoint=endpoint, method="PUT")
    
    def delete(self, name, value):
        endpoint = "{0}/{1}".format(name, value)
        return super().delete(endpoint=endpoint, no_response=True)

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "value": None
            }
        )
    
    def get_spec(self, value):
        spec = self._get_default_spec()
        spec["value"] = value
        return spec