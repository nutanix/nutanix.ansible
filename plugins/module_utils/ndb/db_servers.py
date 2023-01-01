# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .clusters import get_cluster_uuid
from .profiles import Profile, get_profile_uuid

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class DBServerVM(NutanixDatabase):
    def __init__(self, module):

        resource_type = "/dbservers"
        super(DBServerVM, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "compute_profile": self._build_spec_compute_profile,
            "software_profile": self._build_spec_software_profile,
            "network_profile": self._build_spec_network_profile,
            "cluster": self._build_spec_cluster,
            "pub_ssh_key": self._build_spec_pub_ssh_key,
            "vm_password": self._build_spec_vm_password,
        }

    def get_uuid(
        self,
        value,
        key="name",
        data=None,
        entity_type=None,
        raise_error=True,
        no_response=False,
    ):
        query = {"value-type": key, "value": value}
        resp = self.read(query=query)

        if not resp:
            return None, "DB server vm with name {0} not found.".format(value)

        uuid = resp[0].get("id")
        return uuid, None

    def get_db_server(self, name=None, uuid=None, ip=None):
        resp = None
        if uuid:
            resp = self.read(uuid=uuid)
        elif name or ip:
            key = "name" if name else "ip"
            val = name if name else ip
            query = {"value-type": key, "value": val}
            resp = self.read(query=query)
            if not resp:
                return None, "Database server with {0} {1} not found".format(key, val)
            resp = resp[0]
        else:
            return (
                None,
                "Please provide uuid, name or server IP for fetching database server details",
            )

        return resp, None

    def provision(self, data):
        pass

    def register(self, data):
        pass

    def get_default_payload(self):
        return deepcopy(
            {
                "actionArguments": [],
                "nxClusterId": "",
                "databaseType": "",
                "latestSnapshot": True,
                "networkProfileId": "",
                "softwareProfileId": "",
                "softwareProfileVersionId": "",
                "computeProfileId": "",
                "vmPassword": None,
            }
        )

    def get_spec(self, old_spec=None, params=None, **kwargs):
        if kwargs.get("db_instance"):
            if self.module.params.get("db_vm", {}).get("create_new_server"):
                payload, err = self.get_spec_provision_for_db_instance(payload=old_spec)
                return payload, err
            else:
                payload, err = self.get_spec_for_db_instance_on_registered_server(
                    payload=old_spec
                )
                return payload, err
        elif kwargs.get("db_vm"):
            if kwargs.get("provision"):
                payload, err = self.get_spec_provision(payload=old_spec)
                return payload, err
            else:
                payload, err = self.get_spec_register(payload=old_spec)
                return payload, err

    def get_default_spec_for_db_instance(self):
        return deepcopy(
            {
                "nodes": [{"properties": [], "vmName": "", "networkProfileId": ""}],
                "nxClusterId": "",
            }
        )

    # this routine populates spec for provisioning db vm for database instance creation
    def get_spec_provision_for_db_instance(self, payload):

        payload.update(self.get_default_spec_for_db_instance())

        self.build_spec_methods.update(
            {
                "name": self._build_spec_name,
            }
        )

        db_vm_config = self.module.params.get("db_vm", {}).get("create_new_server", {})
        if not db_vm_config:
            return (
                None,
                "'db_vm.create_new_server' is required for creating spec for new db server vm",
            )

        payload, err = super().get_spec(old_spec=payload, params=db_vm_config)
        if err:
            return None, err

        payload["nodeCount"] = 1
        payload["clustered"] = False
        payload["createDbserver"] = True
        return payload, err

    def get_spec_for_db_instance_on_registered_server(self, payload):
        db_vm_config = self.module.params.get("db_vm", {}).get(
            "use_registered_server", {}
        )
        if not db_vm_config:
            return (
                None,
                "'db_vm.use_registered_server' is required for creating spec for registered db server vm",
            )

        uuid, err = get_db_server_uuid(self.module, db_vm_config)
        if err:
            return None, err

        payload["createDbserver"] = False
        payload["dbserverId"] = uuid
        payload["nodes"] = [{"properties": [], "dbserverId": uuid}]
        return payload, None

    def get_spec_provision(self, payload):
        self.build_spec_methods.update(
            {
                "database_type": self._build_spec_database_type,
            }
        )

        payload, err = super().get_spec(old_spec=payload)

        if not payload.get("actionArguments"):
            payload["actionArguments"] = []

        payload["actionArguments"].append(
            {"name": "vm_name", "value": self.module.params.get("name")}
        )

        payload["actionArguments"].append(
            {
                "name": "client_public_key",
                "value": self.module.params.get("pub_ssh_key"),
            }
        )

        return payload, err

    def get_spec_register(self, payload):
        pass

    # builder methods for vm
    def _build_spec_name(self, payload, name):
        if not payload.get("nodes"):
            payload["nodes"] = [{}]

        payload["nodes"][0]["vmName"] = name
        return payload, None

    def _build_spec_compute_profile(self, payload, profile):
        # set compute profile
        uuid, err = get_profile_uuid(self.module, "Compute", profile)
        if err:
            return None, err
        payload["computeProfileId"] = uuid
        return payload, None

    def _build_spec_software_profile(self, payload, profile):
        # set software profile
        uuid, err = get_profile_uuid(self.module, "Software", profile)
        if err:
            return None, err

        payload["softwareProfileId"] = uuid
        if profile.get("version_id"):
            payload["softwareProfileVersionId"] = profile["version_id"]
        else:
            profiles = Profile(self.module)
            software_profile = profiles.read(uuid)
            payload["softwareProfileId"] = uuid
            payload["softwareProfileVersionId"] = software_profile["latestVersionId"]

        return payload, None

    def _build_spec_network_profile(self, payload, profile):
        # set network prfile
        uuid, err = get_profile_uuid(self.module, "Network", profile)
        if err:
            return None, err

        payload["networkProfileId"] = uuid
        return payload, None

    def _build_spec_cluster(self, payload, cluster):
        # set cluster config
        uuid, err = get_cluster_uuid(self.module, cluster)
        if err:
            return None, err
        payload["nxClusterId"] = uuid
        return payload, None

    def _build_spec_pub_ssh_key(self, payload, pub_ssh_key):
        payload["sshPublicKey"] = pub_ssh_key
        return payload, None

    def _build_spec_vm_password(self, payload, password):
        payload["vmPassword"] = password
        return payload, None

    def _build_spec_database_type(self, payload, db_type):
        payload["database_type"] = db_type
        return payload, None


def get_db_server_uuid(module, config):
    if "name" in config:
        db_servers = DBServerVM(module)
        name = config["name"]
        uuid, err = db_servers.get_uuid(name)
        if err:
            return None, err
    elif "uuid" in config:
        uuid = config["uuid"]
    else:
        error = "Config {0} doesn't have name or uuid key".format(config)
        return None, error

    return uuid, None
