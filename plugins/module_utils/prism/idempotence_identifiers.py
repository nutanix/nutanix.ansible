# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

__metaclass__ = type

from .prism import Prism
import uuid

class IdempotenceIdenitifiers(Prism):
    def __init__(self, module):
        resource_type = "/idempotence_identifiers"
        super(IdempotenceIdenitifiers, self).__init__(module, resource_type=resource_type)

    def get_idempotent_uuids(self, count):
        if count < 1:
            return []
        spec = {
            "client_identifier" : uuid.uuid4(),
            "count": count
        }
        resp = self.create(spec)
        return resp["uuid_list"]