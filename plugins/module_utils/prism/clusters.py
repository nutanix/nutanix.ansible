# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism
from copy import deepcopy


class Cluster(Prism):
    def __init__(self, module):
        resource_type = "/clusters"
        super(Cluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            # "cluster": self._build_spec_cluster_name,
            "authorized_public_key_list": self._build_spec_public_keys,
        }

    def _get_default_spec(self):
        return deepcopy(
            {
                "api_version": "3.1.0",
                "metadata": {"kind": "cluster", "spec_version": 2},
                "spec": {
                    "name": None,
                    "resources": {
                        "config": {
                            "authorized_public_key_list": []
                        }
                    }
                }
            }
        )

    def _build_spec_public_keys(self, payload, public_keys):
        # public keys is a list of dict values with name, key
        public_key_list = []
        for key_detail in public_keys:
            key_entry = {"name": key_detail.get('name'), "key": key_detail.get('key')}
            public_key_list.append(key_entry)
        payload["spec"]["resources"]["config"]["authorized_public_key_list"] = public_key_list
        return payload, None

    def _build_spec_cluster_name(self, payload, param):
        if "name" in param:
            cluster = Cluster(self.module)
            name = param["name"]
            uuid = cluster.get_uuid(name)
            if not uuid:

                error = "Cluster {0} not found.".format(name)
                return None, error

        elif "uuid" in param:
            uuid = param["uuid"]

        payload["metadata"]["uuid"] = uuid
        return payload, None

    def get_current_spec(self):
        config = self.module.params.get('cluster')
        if "name" in config:
            name = config["name"]
            uuid = self.get_uuid(name)
            if not uuid:
                error = "Cluster {0} not found.".format(name)
                return None, error
        elif "uuid" in config:
            uuid = config["uuid"]
        else:
            error = "Config {0} doesn't have name or uuid key".format(config)
            return None, error
        cluster_info = self.read(uuid)
        old_spec = {}
        old_spec['spec'] = cluster_info['spec']
        old_spec['api_version'] = cluster_info['api_version']
        old_spec['metadata'] = cluster_info['metadata']

        return deepcopy(old_spec)


# Helper functions


def get_cluster_uuid(config, module):
    if "name" in config:
        cluster = Cluster(module)
        name = config["name"]
        uuid = cluster.get_uuid(name)
        if not uuid:
            error = "Cluster {0} not found.".format(name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
