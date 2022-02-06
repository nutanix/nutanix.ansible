# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Cluster(Prism):
    def __init__(self, module):
        resource_type = "/clusters"
        super(Cluster, self).__init__(module, resource_type=resource_type)


##### Helper functions #####


def get_cluster_uuid(config, module):
    if "name" in config["cluster"]:
        cluster = Cluster(module)
        name = config["cluster"]["name"]
        uuid = cluster.get_uuid(name)
        if not uuid:
            error = "Cluster {0} not found.".format(name)
            return None, error
    elif "uuid" in config["cluster"]:
        uuid = config["cluster"]["uuid"]
