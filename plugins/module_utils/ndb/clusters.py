# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class Cluster(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/clusters"
        super(Cluster, self).__init__(module, resource_type=resource_type)

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
        resp = self.read(uuid=None, endpoint=endpoint)
        return resp["id"]


# helper functions


def get_cluster_uuid(module, config):
    uuid = ""
    if config.get("name"):
        clusters = Cluster(module)
        uuid = clusters.get_uuid(config["name"])
    elif config.get("uuid"):
        uuid = config["uuid"]
    else:
        error = "cluster config {0} doesn't have name or uuid key".format(config)
        return error, None
    return uuid, None
