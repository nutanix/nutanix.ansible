# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class Tag(NutanixDatabase):
    types = ["Database_Parameter"]

    def __init__(self, module):
        resource_type = "/tags"
        super(Tag, self).__init__(module, resource_type=resource_type)

    def get_all_name_uuid_map(self):
        resp = self.read()
        name_uuid_map = {}
        for tag in resp:
            name_uuid_map[tag["name"]] = tag["id"]
        return name_uuid_map
