# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
from copy import deepcopy

from .clusters import Cluster, get_cluster_uuid
from .profiles import Profile, get_profile_uuid

__metaclass__ = type


from .nutanix_database import NutanixDatabase


class DBServerVM(NutanixDatabase):
    def __init__(self, module):

        resource_type = "/dbservers"
        super(DBServerVM, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "compute_profile": self.build_spec_compute_profile,
            "software_profile": self.build_spec_software_profile,
            "network_profile": self.build_spec_network_profile,
            "cluster": self.build_spec_cluster,
            "pub_ssh_key": self.build_spec_pub_ssh_key,
            "vm_password": self.build_spec_vm_password,
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

    def get_default_payload_for_provision(self):
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
    
    def get_default_payload_for_registration(self):
        return deepcopy({
            "nxClusterId": "",
            "vmIp": "",
            "vmUsername": "",
            "vmPassword": "",
            "vmSshkey": "",
            "vmDescription": "",
            "resetDescriptionInNxCluster": False
        })


    def get_spec(self, old_spec=None, params=None, **kwargs):

        # if db server vm is required for db instance
        if kwargs.get("db_instance_provision"):
            if self.module.params.get("db_vm", {}).get("create_new_server"):
                payload, err = self.get_spec_provision_for_db_instance(payload=old_spec)
                return payload, err
            elif self.module.params.get("db_vm", {}).get("use_registered_server"):
                payload, err = self.get_spec_registered_server_for_db_instance_provision(
                    payload=old_spec
                )
                return payload, err
        
        # if db server vm is required for registering db instance
        elif kwargs.get("db_instance_register"):
            if self.module.params.get("db_vm", {}).get("registered"):
                payload, err = self.get_spec_registered_vm_for_db_instance_registration(payload=old_spec)
                return payload, err
            elif self.module.params.get("db_vm", {}).get("unregistered"):
                payload, err = self.get_spec_register(payload=old_spec)
                return payload, err
        
        # if only db server vm provision or register is required
        elif kwargs.get("db_vm"):
            if kwargs.get("provision"):
                payload, err = self.get_spec_provision(payload=old_spec)
                return payload, err
            elif kwargs.get("register"):
                payload, err = self.get_spec_register(payload=old_spec)
                return payload, err
        
        return None, "Please provide supported arguments"

    # this routine populates spec for provisioning db vm for database instance creation
    def get_spec_provision_for_db_instance(self, payload):

        payload.update(self.get_default_payload_for_provision())
        db_vm_config = self.module.params.get("db_vm", {}).get("create_new_server", {})
        if not db_vm_config:
            return (
                None,
                "'db_vm.create_new_server' is required for creating spec for new db server vm",
            )

        payload, err = super().get_spec(old_spec=payload, params=db_vm_config)
        if err:
            return None, err

        # configure vm related spec
        kwargs = {
            "network_profile_uuid": payload["networkProfileId"]
        }

        payload, err = self.build_spec_vms(payload, [db_vm_config])
        if err:
            return None, err

        payload["clustered"] = False
        payload["createDbserver"] = True
        return payload, err

    # this routine populates spec for registered db vm to host new database instance
    def get_spec_registered_server_for_db_instance_provision(self, payload):
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

    # this routine creates spec for provisioning of db server vm
    def get_spec_provision(self, payload={}):
        payload.update(self.get_default_payload_for_provision())
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

    # this routine creates spec for registration of db server vm, also can be used during db instance registration
    def get_spec_register(self, payload={}):
        self.build_spec_methods = {
            "ip": self._build_spec_register_vm_ip,
            "username": self._build_spec_register_vm_username,
            "password": self._build_spec_register_vm_password,
            "private_ssh_key": self._build_spec_register_vm_private_ssh_key,
            "desc": self._build_spec_register_vm_desc,
            "reset_desc_in_ntnx_cluster": self._build_spec_register_vm_reset_desc,
            "cluster": self.build_spec_cluster
        }

        payload.update(self.get_default_payload_for_registration())

        config = self.module.params.get("db_vm", {}).get(
            "unregistered", {}
        )
        if not config:
            return (
                None,
                "'db_vm.unregistered' is required for creating spec for registering db server vm",
            )
        payload, err = super().get_spec(old_spec=payload, params=config)
        if err:
            return None, err
        
        return payload, err

    # this routine creates spec for registered vm to register db instance from it
    def get_spec_registered_vm_for_db_instance_registration(self, payload):

        config = self.module.params.get("db_vm", {}).get(
            "registered", {}
        )
        if not config:
            return (
                None,
                "'db_vm.registered' is required for creating spec for registered db server vm",
            )

        # fetch vm ip using name or uuid
        if config.get("name") or config.get("uuid"):

            vm_info, err = self.get_db_server(
                name=config.get("name"), uuid=config.get("uuid")
            )
            if err:
                return None, err

            if not vm_info.get("ipAddresses", []):
                return None, "No IP address found for given db server vm"

            # picking first IP of db server vm for registraion
            payload["vmIp"] = vm_info["ipAddresses"][0]

        elif config.get("ip"):
            payload["vmIp"] = config["ip"]

        else:
            return None, "name, uuid or ip is required for registered vm configuration"

        return payload, None

    # builder methods for vm creation
    def _build_spec_name(self, payload, name):
        if not payload.get("nodes"):
            payload["nodes"] = [{}]

        payload["nodes"][0]["vmName"] = name
        return payload, None
    
    def _build_spec_database_type(self, payload, db_type):
        payload["database_type"] = db_type
        return payload, None

    def build_spec_compute_profile(self, payload, profile):
        # set compute profile
        uuid, err = get_profile_uuid(self.module, "Compute", profile)
        if err:
            return None, err
        payload["computeProfileId"] = uuid
        return payload, None

    def build_spec_software_profile(self, payload, profile):
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

    def build_spec_network_profile(self, payload, profile):
        # set network prfile
        uuid, err = get_profile_uuid(self.module, "Network", profile)
        if err:
            return None, err

        payload["networkProfileId"] = uuid
        return payload, None

    def build_spec_cluster(self, payload, cluster):
        # set cluster config
        uuid, err = get_cluster_uuid(self.module, cluster)
        if err:
            return None, err
        payload["nxClusterId"] = uuid
        return payload, None

    def build_spec_pub_ssh_key(self, payload, pub_ssh_key):
        payload["sshPublicKey"] = pub_ssh_key
        return payload, None
    
    def _build_spec_ip(self, payload, ip):
        payload["ipInfos"] = [
            {
                "ipType": "VM_IP",
                "ipAddresses": [
                    ip
                ]
            }
        ],
        return payload, None

    def build_spec_vm_password(self, payload, password):
        payload["vmPassword"] = password
        return payload, None
    
    def build_spec_vms(self, payload, vms, **kwargs):
        nodes = payload.get("nodes", [])

        # get cluster uuid map to assign cluster uuid for each node vm
        cluster = Cluster(self.module)
        clusters = cluster.get_all_clusters_name_uuid_map()

        # spec with default vlaues
        spec = {
            "properties": [],
            "vmName": "",
            "networkProfileId": kwargs.get("network_profile_uuid", ""),
            "computeProfileId": kwargs.get("compute_profile_uuid", ""),
            "nxClusterId": kwargs.get("cluster_uuid", "")
        }

        profile = Profile(self.module)

        # get all network profile name uuid map
        network_profiles, err = profile.get_all_name_uuid_map(type="Network")
        if err:
            return None, err

        # get all compute profile name uuid map
        compute_profiles, err = profile.get_all_name_uuid_map(type="Compute")
        if err:
            return None, err

        for vm in vms:

            node = deepcopy(spec)
            node["vmName"] = vm.get("name")

            properties = ["role", "node_type"]

            for prop in properties:
                if prop in vm:
                    node["properties"].append({
                        "name":prop,
                        "value": vm[prop]
                    })
            
            if vm.get("archive_log_destination"):
                node["properties"].append({
                        "name": "remote_archive_destination",
                        "value": vm.get("archive_log_destination")
                })
        
            # add network profile for a vm if required
            if vm.get("network_profile"):
                uuid = ""
                if vm["network_profile"].get("name"):
                    if network_profiles.get(vm["network_profile"]["name"]):
                        uuid = network_profiles[vm["network_profile"]["name"]]
                    else:
                        return None, "Network profile with name '{0}' not found".format(
                            vm["network_profile"]["name"]
                        )

                elif vm["network_profile"].get("uuid"):
                    uuid = vm["network_profile"]["uuid"]

                node["networkProfileId"] =  uuid
            
             # add network profile for a vm if required
            if vm.get("compute_profile"):
                uuid = ""
                if vm["compute_profile"].get("name"):
                    if compute_profiles.get(vm["compute_profile"]["name"]):
                        uuid = compute_profiles[vm["compute_profile"]["name"]]
                    else:
                        return None, "Compute profile with name '{0}' not found".format(
                            vm["compute_profile"]["name"]
                        )

                elif vm["compute_profile"].get("uuid"):
                    uuid = vm["compute_profile"]["uuid"]

                node["computeProfileId"] =  uuid
            
            # add cluster spec for a vm
            if vm.get("cluster"):
                cluster_uuid = ""
                if vm["cluster"].get("name"):
                    if clusters.get(vm["cluster"]["name"]):
                        cluster_uuid = clusters[vm["cluster"]["name"]]
                    else:
                        return None, "NDB cluster with name '{0}' not found".format(
                            vm["cluster"]["name"]
                        )

                elif vm["cluster"].get("uuid"):
                    cluster_uuid = vm["cluster"]["uuid"]

                node["nxClusterId"] =  cluster_uuid

            if vm.get("ip"):
                payload, err = self._build_spec_ip(payload, vm.get("ip"))
                if err:
                    return None, err

            nodes.append(node)
        
        payload["nodes"] = nodes
        payload["nodeCount"] = len(payload["nodes"])
        return payload, None

    def _build_spec_register_vm_ip(self, payload, ip):
        payload["vmIp"] = ip
        action_arguments = payload.get("actionArguments", [])
        action_arguments.append({
            "name": "vmIp",
            "value": ip
        })
        payload["actionArguments"] = action_arguments
        return payload, None
    
    def _build_spec_register_vm_username(self, payload, username):
        payload["vmUsername"] = username
        return payload, None
    
    def _build_spec_register_vm_password(self, payload, password):
        payload["vmPassword"] = password
        return payload, None
    
    def _build_spec_register_vm_private_ssh_key(self, payload, private_ssh_key):
        payload["vmSshkey"] = private_ssh_key
        return payload, None
    
    def _build_spec_register_vm_desc(self, payload, desc):
        payload["vmDescription"] = desc
        return payload, None
    
    def _build_spec_register_vm_reset_desc(self, payload, reset_desc):
        payload["resetDescriptionInNxCluster"] = reset_desc
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
