# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

from .clusters import get_cluster_uuid
from .nutanix_database import NutanixDatabase

__metaclass__ = type


class VLAN(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/resources/networks"
        super(VLAN, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "vlan_type": self._build_spec_type,
        }

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        query = {key: value}
        resp = self.read(query=query, raise_error=False)
        if resp is None:
            return None, "vlan instance with name {0} not found.".format(value)
        uuid = resp.get("id")
        return uuid, None

    def get_vlan(self, name=None, uuid=None):
        default_query = {"detailed": True}
        if uuid:
            resp = self.read(uuid=uuid, query=default_query)
        elif name:
            query = {"value-type": "name", "value": name}
            query.update(deepcopy(default_query))
            resp = self.read(query=query)
            if not resp:
                return None, "vlan with name {0} not found".format(name)
            if isinstance(resp, list):
                resp = resp[0]
                return resp, None
        else:
            return (
                None,
                "Please provide either uuid or name for fetching vlan details",
            )

        return resp, None

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": "",
                "type": "",
                "properties": [],
                "ipPools": [],
                "clusterId": "1c42ca25-32f4-42d9-a2bd-6a21f925b725"
            }
        )

    def get_default_update_spec(self, override_spec=None):
        spec = deepcopy(
            {
                "name": None,
                "description": None,
                "tags": [],
                "resetTags": True,
                "resetName": True,
                "resetDescription": True,
            }
        )
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def get_default_delete_spec(self):
        return deepcopy(
            {
                "delete": False,
                "remove": False,
                "deleteTimeMachine": False,
                "deleteLogicalCluster": True,
            }
        )

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_type(self, payload, vlan_type):
        payload["type"] = vlan_type
        return payload, None

    def _build_spec_cluster(self, payload, param):
        uuid, err = get_cluster_uuid(param, self.module)
        if err:
            return None, err
        payload["clusterId"] = uuid
        return payload, None

    def _build_spec_ip_pools(self, payload, params):
        pools = []
        for ip_pool in params["ip_pools"]:
            range = {"range": ip_pool["start_ip"] + " " + ip_pool["end_ip"]}
            pools.append(range)
        payload["ipPools"] = pools
        return payload, None
