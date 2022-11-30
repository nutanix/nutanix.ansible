# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class Snapshots(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/snapshots"
        super(Snapshots, self).__init__(module, resource_type=resource_type)

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        endpoint = "{0}/{1}".format(key, value)
        resp = self.read(uuid=None, endpoint=endpoint)
        return resp.get("id")

    def get_snapshot_files(self, uuid):
        endpoint = "/files"
        resp = self.read(uuid=uuid, endpoint=endpoint)
        return resp
