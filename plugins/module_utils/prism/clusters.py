# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Cluster(Prism):
    kind = "cluster"

    def __init__(self, module):
        resource_type = "/clusters"
        super(Cluster, self).__init__(module, resource_type=resource_type)

    def get_all_clusters_name_uuid_map(
        self,
    ):
        name_uuid_map = {}
        max_length = 500
        data = {"offset": 0}
        while True:
            data["length"] = max_length
            resp = self.list(data=data)
            for cluster in resp.get("entities", []):
                name = ""
                if cluster.get("spec", {}).get("name"):
                    name = cluster["spec"]["name"]
                elif cluster.get("status", {}).get("name"):
                    name = cluster["status"]["name"]
                else:
                    continue

                name_uuid_map[name] = cluster["metadata"]["uuid"]

            data["offset"] = data["offset"] + max_length
            if data["offset"] > resp["metadata"]["total_matches"]:
                break
        return name_uuid_map

    @classmethod
    def build_cluster_reference_spec(cls, uuid):
        spec = {"kind": cls.kind, "uuid": uuid}
        return spec


# Helper functions


def get_cluster_uuid(config, module):
    if "name" in config:
        cluster = Cluster(module)
        name = config["name"]
        clusters_name_uuid_map = cluster.get_all_clusters_name_uuid_map()
        if clusters_name_uuid_map.get(name):
            return clusters_name_uuid_map.get(name), None
        else:
            error = "Cluster {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
        return uuid, None
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error
