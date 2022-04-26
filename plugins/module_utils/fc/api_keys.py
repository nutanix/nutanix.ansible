#from __future__ import absolute_import, division, print_function

from copy import deepcopy
from .fc import FoundationCentral

__metaclass__ = type


class ApiKey(FoundationCentral):
    entity_type="api_keys"
    def __init__(self, module):
        resource_type = "/api_keys"
        super(ApiKey, self).__init__(
                module, resource_type=resource_type
            )
        self.build_spec_methods = {
            "alias": self._build_spec_alias
        }

    def _get_default_spec(self):
        return deepcopy({ "alias": None })

    def _build_spec_alias(self, payload, alias):
        payload["alias"] = alias
        return payload, None

