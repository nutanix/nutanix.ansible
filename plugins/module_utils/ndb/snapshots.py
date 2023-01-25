# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

__metaclass__ = type


from .clusters import Cluster
from .nutanix_database import NutanixDatabase
from .time_machines import TimeMachine


class Snapshot(NutanixDatabase):
    def __init__(self, module):
        resource_type = "/snapshots"
        super(Snapshot, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "expiry_days": self._build_spec_expiry,
            "clusters": self._build_spec_clusters,
        }

    def create_snapshot(self, time_machine_uuid, data):
        endpoint = "{0}/{1}".format(time_machine_uuid, "snapshots")
        time_machine = TimeMachine(self.module)
        return time_machine.create(data=data, endpoint=endpoint)

    def rename_snapshot(self, uuid, data):
        endpoint = "i/{0}".format(uuid)
        return self.update(data=data, endpoint=endpoint, method="PATCH")

    def update_expiry(self, uuid, data):
        query = {"set-lcm-config": True}
        endpoint = "i/{0}".format(uuid)
        return self.update(data=data, endpoint=endpoint, query=query)

    def remove_expiry(self, uuid, data):
        endpoint = "i/{0}".format(uuid)
        query = {"unset-lcm-config": True}
        return self.update(data=data, endpoint=endpoint, query=query)

    def replicate(self, uuid, time_machine_uuid, data):
        endpoint = "{0}/{1}/{2}".format("snapshots", uuid, "replicate")
        time_machine = TimeMachine(self.module)
        return time_machine.update(
            data=data, uuid=time_machine_uuid, endpoint=endpoint, method="POST"
        )

    def get_snapshot(self, time_machine_uuid, name):
        snapshot_uuid, err = self.get_snapshot_uuid(time_machine_uuid, name)
        if err:
            return None, err
        return (
            self.read(snapshot_uuid, query={"load-replicated-child-snapshots": True}),
            None,
        )

    def get_snapshot_uuid(self, time_machine_uuid, name):
        query = {
            "value-type": time_machine_uuid,
            "detailed": False,
            "load-database": False,
            "load-clones": False,
            "time-zone": "UTC",
        }

        snapshots = self.read(query=query)
        uuid = ""
        if isinstance(snapshots, list):

            # multiple snapshots can have same name
            # check for latest snapshot with given name using latest timestamp
            latest_timestamp = 0
            for snapshot in snapshots:
                if (
                    snapshot.get("name") == name
                    and snapshot.get("snapshotTimeStampDate") > latest_timestamp
                ):
                    uuid = snapshot.get("id")
                    latest_timestamp = snapshot.get("snapshotTimeStampDate")

            if not uuid:
                return None, "Snapshot with name {0} not found".format(name)

        return uuid, None

    def _get_default_spec(self):
        return deepcopy({"name": "", "replicateToClusterIds": []})

    def _get_default_snapshot_replication_spec(self):
        return deepcopy({"nxClusterIds": []})

    def get_expiry_update_spec(self, config):
        expiry = config.get("expiry_days")
        timezone = config.get("timezone")
        spec = {
            "lcmConfig": {
                "expiryDetails": {
                    "expiryDateTimezone": timezone,
                    "expireInDays": expiry,
                }
            }
        }
        return spec

    def get_rename_snapshot_spec(self, name):
        spec = self._get_default_spec()
        spec["name"] = name
        spec["resetName"] = True
        return spec

    def get_remove_expiry_spec(self, uuid, name):
        spec = {"id": uuid, "name": name}
        return spec

    def get_replicate_snapshot_spec(self):
        payload = self._get_default_snapshot_replication_spec()
        self.build_spec_methods = {
            "clusters": self._build_spec_clusters,
            "expiry_days": self._build_spec_expiry,
        }
        payload, err = self.get_spec(old_spec=payload)
        if err:
            return None, err
        payload["nxClusterIds"] = payload.pop("replicateToClusterIds")
        return payload, None

    def _build_spec_name(self, payload, name):
        payload["name"] = name
        return payload, None

    def _build_spec_expiry(self, payload, expiry):
        if not self.module.params.get("timezone"):
            return None, "timezone is required field for snapshot removal schedule"
        payload["lcmConfig"] = {
            "snapshotLCMConfig": {
                "expiryDetails": {
                    "expiryDateTimezone": self.module.params.get("timezone"),
                    "expireInDays": int(expiry),
                }
            }
        }
        return payload, None

    def _build_spec_clusters(self, payload, clusters):
        cluster_uuids, err = self.resolve_cluster_uuids(clusters)
        if err:
            return None, err
        payload["replicateToClusterIds"] = cluster_uuids
        return payload, None

    def resolve_cluster_uuids(self, clusters):
        _clusters = Cluster(self.module)
        specs = []

        # if there are more then one clusters then fetch all to resolve uuids
        clusters_name_uuid_map = {}
        if len(clusters) > 1:
            clusters_name_uuid_map = _clusters.get_all_clusters_name_uuid_map()

        for cluster in clusters:
            uuid = ""
            if cluster.get("name"):

                uuid = ""
                if clusters_name_uuid_map:
                    uuid = clusters_name_uuid_map.get(cluster.get("name"))
                else:
                    uuid = _clusters.get_uuid(value=cluster.get("name"))

                if not uuid:
                    return None, "Cluster with name {0} not found".format(
                        cluster["name"]
                    )
            else:
                uuid = cluster.get("uuid")

            specs.append(uuid)

        return specs, None
