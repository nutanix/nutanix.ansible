# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class Tag(NutanixDatabase):
    types = ["Database_Parameter"]

    def __init__(self, module):
        resource_type = "/tags"
        super(Tag, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
            "entity_type": self._build_spec_entity_type,
            "tag_value_required": self._build_spec_tag_vlaue_required,
            "status": self._build_spec_status
        }

    def read(self, uuid=None, endpoint=None, query=None, raise_error=True, no_response=False, timeout=30):
        
        if uuid:
            if not query:
                query = {}
            query["id"] = uuid

        return super().read(uuid=None, query=query, endpoint=endpoint, raise_error=raise_error, no_response=no_response, timeout=timeout)


    def get_tag_uuid(self, name, entity_type):
        # use name + entity_type combination to get tag details
        query = {}
        if entity_type:
            query["entityType"] = entity_type

        resp = self.read(query=query)

        uuid = None
        if isinstance(resp, list):
            for tag in resp:
                if tag.get("name") == name and tag.get("status") == "ENABLED":
                    uuid =  tag.get("id")

        else:
            return None, "Invalid API response"

        if not uuid:
            return None, "Tag with name {0} not found".format(name)

        return uuid, None

    def get_all_name_uuid_map(self):
        resp = self.read()
        name_uuid_map = {}
        for tag in resp:
            name_uuid_map[tag["name"]] = tag["id"]
        return name_uuid_map

    def get_default_update_spec(self):
        return deepcopy({
            "id": "",
            "name": "",
            "description": "",
            "owner": "",
            "required": False,
            "status": "",
            "entityType": ""
        })

    def _get_default_spec(self):
        return deepcopy(
            {
                "entityType": "",
                "name": "",
                "required": False,
                "description": ""
            }
        )
    
    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_desc(self, payload, desc):
        payload["description"] = desc
        return payload, None
    
    def _build_spec_entity_type(self, payload, entity_type):
        payload["entityType"] = entity_type
        return payload, None
    
    def _build_spec_tag_vlaue_required(self, payload, tag_value_required):
        payload["required"] = tag_value_required
        return payload, None
    
    def _build_spec_status(self, payload, status):
        payload["status"] = status
        return payload, None