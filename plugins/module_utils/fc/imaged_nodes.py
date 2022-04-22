#from __future__ import absolute_import, division, print_function

from copy import deepcopy
from email.policy import default
from .fc import FoundationCentral

__metaclass__ = type


class ImagedNodes(FoundationCentral):
    def __init__(self, module):
        resource_type = "/imaged_nodes"
        super(ImagedNodes, self).__init__(
                module, resource_type=resource_type
            )
        self.build_spec_methods = {
            "length": self._build_spec_length,
            "offset": self._build_spec_offset,
            "filters": self._build_spec_filters 
        }

    def _build_spec_length(self, payload, value):
        payload["length"] = value
        return payload,None

    def _build_spec_offset(self, payload, value):
        payload["offset"] = value
        return payload,None

    def _build_spec_filters(self, payload, value):
        payload["filters"] = value
        return payload, None 

    def _get_default_spec(self):
        return deepcopy({
            "length": 10,
            "offset":0,
            "filters":{
                "node_state": ""
            }
        })




