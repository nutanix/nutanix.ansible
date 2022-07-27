# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Permissions(Prism):
    kind = "permission"

    def __init__(self, module):
        resource_type = "/permissions"
        super(Permissions, self).__init__(module, resource_type=resource_type)

    def get_uuid(self, value, key="name", raise_error=True, no_response=False):
        filter_spec = {
            "filter": "{0}=={1}".format(key, value),
            "length": self.entities_limitation,
            "offset": 0,
            "kind": self.kind,
        }
        resp = self.list(
            data=filter_spec, raise_error=raise_error, no_response=no_response
        )
        for entity in resp["entities"]:
            if entity["spec"]["name"] == value:
                return entity["metadata"]["uuid"]

        # Incase there are more entities to check
        while resp["total_matches"] > resp["length"] + resp["offset"]:
            filter_spec["length"] = self.entities_limitation
            filter_spec["offset"] = filter_spec["offset"] + self.entities_limitation
            resp = self.list(
                data=filter_spec, raise_error=raise_error, no_response=no_response
            )
            for entity in resp["entities"]:
                if entity["spec"]["name"] == value:
                    return entity["metadata"]["uuid"]
        return None

    @classmethod
    def build_permission_reference_spec(cls, uuid=None):
        spec = {"kind": cls.kind, "uuid": uuid}
        return spec


def get_permission_uuid(config, module):
    if "name" in config:
        users = Permissions(module)
        name = config["name"]
        uuid = users.get_uuid(name)
        if not uuid:

            error = "Permission {0} not found.".format(name)
            return None, error

    elif "uuid" in config:
        uuid = config["uuid"]

    return uuid, None
