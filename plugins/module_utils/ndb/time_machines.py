# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class TimeMachine(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/tms"
        super(TimeMachine, self).__init__(module, resource_type=resource_type)

    def get_time_machine(self, uuid=None, name=None):
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
