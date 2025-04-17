# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import uuid

from .prism import Prism


class IdempotenceIdentifiers(Prism):
    def __init__(self, module):
        resource_type = "/idempotence_identifiers"
        super(IdempotenceIdentifiers, self).__init__(
            module, resource_type=resource_type
        )

    def get_idempotent_uuids(self, count=1):
        if count < 1:
            return []
        spec = {"client_identifier": str(uuid.uuid4()), "count": count}
        resp = self.create(spec)
        return resp["uuid_list"]

    # this func requests for UUID5 algo uuids used mainly for pc users
    def get_salted_uuids(self, name_list):
        spec = {"name_list": name_list}
        resp = self.create(spec, endpoint="salted")
        return resp["name_uuid_list"]
