# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

__metaclass__ = type


from .clusters import get_cluster_uuid
from .nutanix_database import NutanixDatabase
from .slas import get_sla_uuid


class TimeMachine(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/tms"
        super(TimeMachine, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "cluster": self._build_spec_cluster,
            "type": self._build_spec_type,
            "sla": self._build_spec_sla,
        }

    def log_catchup(self, time_machine_uuid, data):
        endpoint = "{0}/{1}".format(time_machine_uuid, "log-catchups")
        return self.create(data=data, endpoint=endpoint)

    def get_time_machine(self, uuid=None, name=None):
        """
        Fetch time machine info based on uuid or name.
        Args:
            uuid(str): uuid of time machine
            name(str): name of time machine
        """
        if uuid:
            resp = self.read(uuid=uuid)
        elif name:
            endpoint = "{0}/{1}".format("name", name)
            resp = self.read(endpoint=endpoint)
            if isinstance(resp, list):
                if not resp:
                    return None, "Time machine with name {0} not found".format(name)
                else:
                    tm = None
                    for entity in resp:
                        if entity["name"] == name:
                            tm = entity
                            break
                    if not tm:
                        return None, "Time machine with name {0} not found".format(name)
                    resp = tm

                    # fetch all details using uuid
                    if resp.get("id"):
                        resp = self.read(uuid=resp["id"])
        else:
            return (
                None,
                "Please provide either uuid or name for fetching time machine details",
            )
        return resp, None

    def get_time_machine_uuid(self, config):
        uuid = ""
        if config.get("uuid"):
            uuid = config["uuid"]
        elif config.get("name"):
            name = config["name"]
            tm, err = self.get_time_machine(name=name)
            if err:
                return None, err
            uuid = tm.get("id")
        else:
            error = "time machine config {0} doesn't have name or uuid key".format(
                config
            )
            return None, error

        return uuid, None

    def get_log_catchup_spec(self, for_restore=False):
        return deepcopy(
            {
                "forRestore": for_restore,
                "actionArguments": [
                    {"name": "preRestoreLogCatchup", "value": for_restore},
                    {"name": "switch_log", "value": True},
                ],
            }
        )

    def get_default_data_access_spec(self, override_spec=None):
        spec = deepcopy({"nxClusterId": "", "type": "OTHER", "slaId": ""})
        if override_spec:
            for key in spec.keys():
                if override_spec.get(key):
                    spec[key] = deepcopy(override_spec[key])

        return spec

    def get_data_access_spec(self, old_spec=None):
        spec = old_spec or self.get_default_data_access_spec()
        return super().get_spec(old_spec=spec)

    def _build_spec_cluster(self, payload, param):
        uuid, err = get_cluster_uuid(self.module, param)
        if err:
            return None, err
        payload["nxClusterId"] = uuid
        return payload, None

    def _build_spec_type(self, payload, type):
        payload["type"] = type
        return payload, None

    def _build_spec_sla(self, payload, param):
        uuid, err = get_sla_uuid(self.module, param)
        if err:
            return None, err
        if payload.get("slaId"):
            payload["resetSlaId"] = True
        payload["slaId"] = uuid
        return payload, None

    def read_data_access_instance(
        self, tm_uuid=None, cluster_uuid=None, raise_error=False
    ):
        endpoint = "clusters/{0}".format(cluster_uuid)
        return super().read(uuid=tm_uuid, endpoint=endpoint, raise_error=raise_error)

    def create_data_access_instance(self, uuid=None, data=None):
        return super().update(uuid=uuid, data=data, endpoint="clusters", method="POST")

    def update_data_access_instance(self, tm_uuid=None, cluster_uuid=None, data=None):
        endpoint = "clusters/{0}".format(cluster_uuid)
        return super().update(
            uuid=tm_uuid, data=data, endpoint=endpoint, method="PATCH"
        )

    def delete_data_access_instance(self, tm_uuid=None, cluster_uuid=None):
        endpoint = "clusters/{0}".format(cluster_uuid)
        data = {
            "deleteReplicatedSnapshots": True,
            "deleteReplicatedProtectionDomains": True,
        }
        return super().delete(uuid=tm_uuid, data=data, endpoint=endpoint)
