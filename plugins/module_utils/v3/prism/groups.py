# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from .prism import Prism


class Groups(Prism):
    def __init__(self, module):
        resource_type = "/groups"
        super(Groups, self).__init__(module, resource_type=resource_type)

    def get_uuid(
        self,
        value="",
        key="name",
        data=None,
        entity_type="",
        raise_error=True,
        no_response=False,
    ):
        if not data:
            data = {
                "entity_type": entity_type,
                "filter_criteria": "{0}=={1}".format(key, value),
            }

        resp = self.list(
            data, use_base_url=True, raise_error=raise_error, no_response=no_response
        )
        if resp.get("group_results"):
            return resp["group_results"][0]["entity_results"][0]["entity_id"]
        return None


def get_entity_uuid(config, module, key, entity_type):
    if "name" in config:
        groups = Groups(module)
        name = config["name"]
        uuid = groups.get_uuid(value=name, key=key, entity_type=entity_type)
        if not uuid:
            entity_type = entity_type.replace("_", " ")
            error = "{0} {1} not found.".format(entity_type.capitalize(), name)
            return None, error
    elif "uuid" in config:
        uuid = config["uuid"]

    return uuid, None
