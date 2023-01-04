# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .db_servers import DBServerVM
from .nutanix_database import NutanixDatabase

__metaclass__ = type


class DBServerCluster(NutanixDatabase):

    def __init__(self, module):
        resource_type = "/dpcs"
        super(DBServerCluster, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "name": self._build_spec_name,
            "desc": self._build_spec_desc,
        }

    def get_spec(self, old_spec=None, params=None, **kwargs):

        # if db server vm cluster is required for db instance
        if kwargs.get("db_instance"):
            if self.module.params.get("db_server_cluster", {}).get("new_cluster"):
                payload, err = self.get_spec_provision_for_db_instance(payload=old_spec)
                return payload, err
            else:
                return None, "Spec builder for DB server cluster registration for HA instance is not implemented"

        elif kwargs.get("db_server_cluster"):
            return None, "Spec builder for DB server cluster provision or register is not implemented"
        
        return None, "Please provide supported arguments"

    def get_default_spec_for_db_instance(self):
        return deepcopy(
            {
                "nodes": [{"properties": [], "vmName": "", "networkProfileId": ""}],
                "nxClusterId": "",
            }
        )

    # this routine populates spec for provisioning db server VM cluster for database instance
    def get_spec_provision_for_db_instance(self, payload):

        db_server_vm = DBServerVM(self.module)

        self.build_spec_methods.update(
            {
                "compute_profile": db_server_vm.build_spec_compute_profile,
                "software_profile": db_server_vm.build_spec_software_profile,
                "network_profile": db_server_vm.build_spec_network_profile,
                "password": db_server_vm.build_spec_vm_password,
                "ndb_cluster": db_server_vm.build_spec_cluster,
                "pub_ssh_key": db_server_vm.build_spec_pub_ssh_key,
            }
        )

        config = self.module.params.get("db_server_cluster", {}).get("new_cluster", {})
        if not config:
            return (
                None,
                "'db_server_cluster.new_cluster' is required for creating spec for new db server vm cluster",
            )

        payload, err = super().get_spec(old_spec=payload, params=config)
        if err:
            return None, err

        # apply defaults to all vms
        network_profile_uuid = payload["networkProfileId"]
        compute_profile_uuid = payload["computeProfileId"]
        archive_log_destination = config.get("archive_log_destination")
        for vm in config["vms"]:
            vm["network_profile_uuid"] = network_profile_uuid
            vm["compute_profile_uuid"] = compute_profile_uuid
            vm["archive_log_destination"] = archive_log_destination

        # configure spec for group of vms for cluster
        payload, err = db_server_vm.build_spec_vms(payload, config["vms"])
        if err:
            return None, err

        payload["clustered"] = True
        payload["createDbserver"] = True
        return payload, err


    # builder methods for vm
    def _build_spec_name(self, payload, name):
        action_arguments = payload.get("actionArguments", [])
        action_arguments.append({
            "name": "cluster_name",
            "value": name
        })
        payload["actionArguments"] = action_arguments
        return payload, None

    def _build_spec_desc(self, payload, desc):
        action_arguments = payload.get("actionArguments", [])
        action_arguments.append({
            "name": "cluster_description",
            "value": desc
        })
        payload["actionArguments"] = action_arguments

        return payload, None
