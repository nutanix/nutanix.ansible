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

    def _build_query_params(self, query_params):
        query = {}
        if query_params.get("all"):
            query.update({"all": query_params["all"]})
        if query_params.get("database_ids"):
            db_ids = ",".join(query_params["database_ids"])
            query.update({"database-ids": db_ids})
        if query_params.get("value"):
            query.update({"value": query_params["value"]})
        if query_params.get("value_type"):
            query.update({"value-type": query_params["value_type"]})
        if query_params.get("time_zone"):
            query.update({"time-zone": query_params["time_zone"]})

        return query

    def get_snapshots(self):
        query_params = self.module.params.get("queries")
        if query_params:
            queries = self._build_query_params(query_params)
            resp = self.read(query=queries)
        else:
            resp = self.read()

        return resp

    def get_snapshot_files(self, uuid):
        endpoint = "files"
        resp = self.read(uuid=uuid, endpoint=endpoint)
        return resp
