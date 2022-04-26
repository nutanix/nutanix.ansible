from __future__ import absolute_import, division, print_function

from .fc import FoundationCentral
from copy import deepcopy

__metaclass__ = type


class ImagedNode(FoundationCentral):
    entity_type = "imaged_nodes"

    def __init__(self, module):
        resource_type = "/imaged_nodes"
        super(ImagedNode, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {"filters": self._build_spec_filters}

    def _build_spec_filters(self, payload, value):
        payload["filters"] = value
        return payload, None

    def _get_default_spec(self):
        return deepcopy({"filters": {"node_state": ""}})

    # Helper function
    def node_details_by_node_serial(self, node_serial):
        spec = self._get_default_spec()
        resp = self.list(spec)
        for node in resp["imaged_nodes"]:
            if node["node_serial"] == node_serial:
                return (self.read(node["imaged_node_uuid"]), None)
        return (
            None,
            "Node serial: {0} is not matching with any of nodes registered to Foundation Central.".format(
                node_serial
            ),
        )
