#from __future__ import absolute_import, division, print_function

from copy import deepcopy
from .fc import FoundationCentral

__metaclass__ = type


class ApiKeys(FoundationCentral):
    def __init__(self, module):
        resource_type = "/api_keys"
        super(ApiKeys, self).__init__(
                module, resource_type=resource_type
            )
        self.build_spec_methods = {
            "alias": self._build_spec_alias,
            "length": self._build_spec_length,
            "offset": self._build_spec_offset
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "alias": None,
                "length":10,
                "offset":0
            }
        )

    def _build_spec_alias(self, payload, alias):
        payload["alias"] = alias
        return payload, None

    def _build_spec_length(self, payload, length):
        payload["length"] = length
        return payload, None

    def _build_spec_offset(Self, payload, offset):
        payload["offset"] = offset
        return payload, None

