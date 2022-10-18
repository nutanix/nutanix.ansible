# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class SLA(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/slas"
        super(SLA, self).__init__(module, resource_type=resource_type)

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
        resp = self.read(uuid=None, endpoint=endpoint, raise_error=False)
        if resp.get("errorCode"):
            self.module.fail_json(
                msg="Failed fetching sla info",
                error=resp.get("message"),
                response=resp,
            )
        return resp.get("id")

    def get_sla(self, uuid=None, name=None):
        if uuid:
            resp = self.read(uuid=uuid, raise_error=False)
        elif name:
            endpoint = "{0}/{1}".format("name", name)
            resp = self.read(endpoint=endpoint, raise_error=False)

        else:
            return None, "Please provide either uuid or name for fetching sla details"

        if isinstance(resp, dict) and resp.get("errorCode"):
            self.module.fail_json(
                msg="Failed fetching sla info",
                error=resp.get("message"),
                response=resp,
            )
        return resp, None


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
        return error, None
    return uuid, None
