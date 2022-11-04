# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class TimeMachine(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/tms"
        super(TimeMachine, self).__init__(module, resource_type=resource_type)

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
