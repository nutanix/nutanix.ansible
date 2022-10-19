# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class Clone(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/clones"
        super(Clone, self).__init__(module, resource_type=resource_type)

    def get_clone(self, uuid=None, name=None):
        if uuid:
            resp = self.read(uuid=uuid)
        elif name:
            query = {"value-type": "name", "value": name}
            resp = self.read(query=query)
            if not resp:
                return None, "Clone with name {0} not found".format(name)
            resp = resp[0]
        else:
            return None, "Please provide either uuid or name for fetching clone details"

        return resp, None
