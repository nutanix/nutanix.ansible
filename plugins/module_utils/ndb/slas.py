# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class SLA(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/slas"
        super(SLA, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "frequency": self._build_spec_frequency,
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
        endpoint = "{0}/{1}".format(key, value)
        resp = self.read(uuid=None, endpoint=endpoint, raise_error=raise_error)
        return resp.get("id")

    def get_sla(self, uuid=None, name=None):
        if uuid:
            resp = self.read(uuid=uuid)
        elif name:
            endpoint = "{0}/{1}".format("name", name)
            resp = self.read(endpoint=endpoint)

        else:
            return None, "Please provide either uuid or name for fetching sla details"
        return resp, None

    def _get_default_spec(self):
        return deepcopy(
            {
                "name": None,
                "continuousRetention": 0,
                "dailyRetention": 0,
                "weeklyRetention": 0,
                "monthlyRetention": 0,
                "quarterlyRetention": 0,
            }
        )

    def get_default_update_spec(self):
        spec = self._get_default_spec()
        spec["description"] = None
        return spec

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_frequency(self, payload, frequency):

        if frequency.get("logs_retention"):
            payload["continuousRetention"] = frequency.get("logs_retention")

        if frequency.get("snapshots_retention"):

            # map of module attributes to api attributes
            snapshots_retention_attr_map = {
                "daily": "dailyRetention",
                "weekly": "weeklyRetention",
                "monthly": "monthlyRetention",
                "quarterly": "quarterlyRetention",
            }

            snapshots_retention = frequency["snapshots_retention"]

            # if input given in module then add in api payload
            for attr, api_attr in snapshots_retention_attr_map.items():
                if snapshots_retention.get(attr) is not None:
                    payload[api_attr] = snapshots_retention[attr]

        return payload, None


# helper functions


def get_sla_uuid(module, config):
    uuid = ""
    if config.get("name"):
        slas = SLA(module)
        uuid = slas.get_uuid(config["name"])
    elif config.get("uuid"):
        uuid = config["uuid"]
    else:
        error = "sla config {0} doesn't have name or uuid key".format(config)
        return None, error
    return uuid, None
