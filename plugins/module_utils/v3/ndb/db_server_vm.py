# This file is part of Ansible
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from copy import deepcopy

__metaclass__ = type


from .clusters import Cluster, get_cluster_uuid
from .database_engines.db_engine_factory import create_db_engine
from .nutanix_database import NutanixDatabase
from .profiles.profile_types import ComputeProfile, NetworkProfile, SoftwareProfile
from .time_machines import TimeMachine


class DBServerVM(NutanixDatabase):
    def __init__(self, module):

        resource_type = "/dbservers"
        super(DBServerVM, self).__init__(module, resource_type=resource_type)
        self.build_spec_methods = {
            "compute_profile": self.build_spec_compute_profile,
            "software_profile": self.build_spec_software_profile,
            "network_profile": self.build_spec_network_profile,
            "cluster": self.build_spec_cluster,
            "password": self.build_spec_password,
        }

    def provision(self, data):
        endpoint = "provision"
        return self.create(data, endpoint)

    def register(self, data):
        endpoint = "register"
        return self.create(data, endpoint)

    def update(
        self,
        data=None,
        uuid=None,
        endpoint=None,
        query=None,
        raise_error=True,
        no_response=False,
        timeout=30,
        method="PATCH",
    ):
        return super().update(
            data, uuid, endpoint, query, raise_error, no_response, timeout, method
        )

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

    def get_all_db_servers_name_uuid_map(self):
        resp = self.read()
        name_uuid_map = {}
        for vm in resp:
            if vm.get("name") and vm.get("id"):
                name_uuid_map[vm.get("name")] = vm.get("id")

        return name_uuid_map

    def get_db_server(self, name=None, uuid=None, ip=None, query=None):
        resp = None
        if uuid:
            resp = self.read(uuid=uuid, query=query)
        elif name or ip:
            key = "name" if name else "ip"
            val = name if name else ip
            query_params = {"value-type": key, "value": val}
            if query:
                query.update(query_params)
            else:
                query = query_params
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

    def get_db_server_uuid(self, config):
        if "name" in config:
            name = config["name"]
            uuid, err = self.get_uuid(name)
            if err:
                return None, err
        elif "uuid" in config:
            uuid = config["uuid"]
        else:
            error = "Config {0} doesn't have name or uuid key".format(config)
            return None, error

        return uuid, None

    @staticmethod
    def format_response(response):
        """This method formats response of db server vm.  It removes attributes as per requirement."""
        attrs = [
            "accessKeyId",
            "lcmConfig",
            "category",
            "placeholder",
            "accessKey",
            "accessLevel",
            "ownerId",
            "softwareInstallationId",
        ]
        for attr in attrs:
            if attr in response:
                response.pop(attr)

        if response.get("metadata") is not None:
            response["provisionOperationId"] = response.get("metadata", {}).get(
                "provisionOperationId"
            )

        response.pop("metadata")

        return response

    def get_default_spec_for_provision(self):
        return deepcopy(
            {
                "actionArguments": [],
                "nxClusterId": "",
                "databaseType": "",
                "latestSnapshot": False,
                "networkProfileId": "",
                "softwareProfileId": "",
                "softwareProfileVersionId": "",
                "computeProfileId": "",
                "vmPassword": None,
            }
        )

    def get_default_spec_for_registration(self):
        return deepcopy(
            {
                "nxClusterId": "",
                "vmIp": "",
                "resetDescriptionInNxCluster": False,
                "forcedInstall": True,
            }
        )

    def get_default_spec_for_update(self, override=None):
        spec = {
            "name": "",
            "description": "",
            "resetNameInNxCluster": False,
            "resetDescriptionInNxCluster": False,
            "resetCredential": False,
            "credentials": [],
            "resetTags": False,
            "resetName": False,
            "resetDescription": False,
        }

        # populate spec with values from old_spec
        if override:
            for key in spec:
                if key in override:
                    spec[key] = override[key]

        return spec

    def get_default_delete_spec(self, **kwargs):
        delete = kwargs.get("delete", False)
        return deepcopy(
            {
                "softRemove": False,
                "remove": not delete,
                "delete": delete,
                "deleteVgs": False,
                "deleteVmSnapshots": False,
            }
        )

    def get_spec(self, old_spec=None, params=None, **kwargs):
        # if db server vm is required for db instance
        if kwargs.get("db_instance_provision"):
            if kwargs.get("provision_new_server"):
                return self.get_spec_provision_for_db_instance(
                    old_spec=old_spec, params=params, **kwargs
                )
            elif kwargs.get("use_registered_server"):
                return self.get_spec_registered_server_for_db_instance_provision(
                    old_spec=old_spec, params=params, **kwargs
                )

        # if db server vm is required for registering db instance
        elif kwargs.get("db_instance_register"):
            if kwargs.get("use_registered_server"):
                return self.get_spec_registered_vm_for_db_instance_registration(
                    old_spec=old_spec, params=params, **kwargs
                )
            elif kwargs.get("register_server"):
                return self.get_spec_register_for_db_instance_registration(
                    old_spec=old_spec, params=params, **kwargs
                )

        elif kwargs.get("db_clone"):
            if kwargs.get("provision_new_server"):
                return self.get_spec_provision_for_db_instance(
                    old_spec=old_spec, params=params, **kwargs
                )
            elif kwargs.get("use_authorized_server"):
                return self.get_spec_authorized_vm(
                    old_spec=old_spec, params=params, **kwargs
                )

        # if only db server vm provision or register is required
        else:
            if kwargs.get("provision_new_server"):
                return self.get_spec_provision(
                    old_spec=old_spec, params=params, **kwargs
                )
            elif kwargs.get("register_server"):
                return self.get_spec_register(
                    old_spec=old_spec, params=params, **kwargs
                )
            elif kwargs.get("update"):
                return self.get_spec_update_vm(
                    old_spec=old_spec, params=params, **kwargs
                )
            elif kwargs.get("delete"):
                return self.get_spec_delete_vm(
                    old_spec=old_spec, params=params, **kwargs
                )
        return None, "Please provide supported arguments"

    def get_db_engine_spec(self, payload, params=None, **kwargs):

        db_engine, err = create_db_engine(self.module, db_architecture="single")
        if err:
            return None, err

        db_type = db_engine.get_type()

        config = self.module.params.get(db_type) or params

        if kwargs.get("register"):
            payload, err = db_engine.build_spec_db_server_vm_register_action_arguments(
                payload, config
            )
            if err:
                return None, err
            payload["databaseType"] = db_type + "_database"

        elif kwargs.get("provision"):
            # add db engine specific spec for provisioning vm
            pass

        return payload, err

    # this routine populates spec for provisioning db vm for database instance creation
    def get_spec_provision_for_db_instance(self, old_spec=None, params=None, **kwargs):

        self.build_spec_methods.update({"pub_ssh_key": self.build_spec_pub_ssh_key})

        if not params:
            params = self.module.params.get("db_vm", {}).get("create_new_server", {})

        if not params:
            return (
                None,
                "db server vm input is required for creating spec for new db server vm",
            )

        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)
        if err:
            return None, err

        # configure vm related spec
        kwargs = {"network_profile_uuid": payload["networkProfileId"]}

        payload, err = self.build_spec_vms(payload, [params], **kwargs)
        if err:
            return None, err

        # add description
        payload["actionArguments"].append(
            {"name": "dbserver_description", "value": params.get("desc")}
        )

        payload["clustered"] = False
        payload["createDbserver"] = True
        return payload, err

    # this routine populates spec for registered db vm to host new database instance
    def get_spec_registered_server_for_db_instance_provision(
        self, old_spec=None, params=None, **kwargs
    ):
        payload = deepcopy(old_spec)
        if not params:
            params = self.module.params.get("db_vm", {}).get(
                "use_registered_server", {}
            )

        if not params:
            return (
                None,
                "db server vm input is required for creating spec for registered db server vm",
            )

        uuid, err = self.get_db_server_uuid(params)
        if err:
            return None, err

        payload["createDbserver"] = False
        payload["dbserverId"] = uuid
        payload["nodes"] = [{"properties": [], "dbserverId": uuid}]
        return payload, None

    # this routine creates spec for provisioning of db server vm
    def get_spec_provision(self, old_spec=None, params=None, **kwargs):

        self.build_spec_methods.update(
            {
                "database_type": self._build_spec_database_type,
                "time_machine": self._build_spec_time_machine,
                "software_profile": self.build_spec_software_profile,
                "time_zone": self._build_spec_time_zone,
                "desc": self._build_spec_description,
            }
        )

        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)
        if err:
            return None, err

        # add vm name
        if not payload.get("actionArguments"):
            payload["actionArguments"] = []

        payload["actionArguments"].append(
            {"name": "vm_name", "value": self.module.params.get("name")}
        )

        # add client public key
        payload["actionArguments"].append(
            {
                "name": "client_public_key",
                "value": self.module.params.get("pub_ssh_key"),
            }
        )

        return payload, err

    # this routine creates spec for registration of db server vm
    def get_spec_register(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "ip": self._build_spec_register_vm_ip,
            "username": self._build_spec_register_username,
            "password": self._build_spec_register_password,
            "private_ssh_key": self._build_spec_register_private_ssh_key,
            "reset_desc_in_ntnx_cluster": self._build_spec_reset_description,
            "cluster": self.build_spec_cluster,
            "desc": self._build_spec_description,
            "working_directory": self._build_spec_register_working_dir,
        }

        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)
        if err:
            return None, err

        # field name changes as per api requirements
        payload["nxClusterUuid"] = payload.pop("nxClusterId")

        return payload, err

    # this routine creates spec for registration of db server vm for db instance registration
    def get_spec_register_for_db_instance_registration(
        self, old_spec=None, params=None, **kwargs
    ):

        self.build_spec_methods = {
            "ip": self._build_spec_register_vm_ip,
            "username": self._build_spec_register_vm_username,
            "password": self._build_spec_register_vm_password,
            "private_ssh_key": self._build_spec_register_vm_private_ssh_key,
            "desc": self._build_spec_register_vm_desc,
            "reset_desc_in_ntnx_cluster": self._build_spec_reset_description,
            "cluster": self.build_spec_cluster,
        }

        if not params:
            params = self.module.params.get("db_vm", {}).get("unregistered", {})

        if not params:
            return (
                None,
                "db server vm input is required for creating spec for registering db server vm",
            )
        payload, err = super().get_spec(old_spec=old_spec, params=params, **kwargs)
        if err:
            return None, err

        action_arguments = payload.get("actionArguments", [])
        action_arguments.append({"name": "vmIp", "value": payload.get("vmIp")})
        payload["actionArguments"] = action_arguments

        return payload, err

    # this routine creates spec for registered vm to register db instance from it
    def get_spec_registered_vm_for_db_instance_registration(
        self, old_spec=None, params=None, **kwargs
    ):
        payload = deepcopy(old_spec)
        if not params:
            params = self.module.params.get("db_vm", {}).get("registered", {})

        if not params:
            return (
                None,
                "Registered db server vm input is required for creating spec for db server vm",
            )

        # fetch vm ip using name or uuid
        if params.get("name") or params.get("uuid"):

            vm_info, err = self.get_db_server(
                name=params.get("name"), uuid=params.get("uuid")
            )
            if err:
                return None, err

            if not vm_info.get("ipAddresses", []):
                return None, "No IP address found for given db server vm"

            # picking first IP of db server vm for registraion
            payload["vmIp"] = vm_info["ipAddresses"][0]

        elif params.get("ip"):
            payload["vmIp"] = params["ip"]

        else:
            return None, "name, uuid or ip is required for registered vm configuration"

        return payload, None

    def get_spec_authorized_vm(self, old_spec=None, params=None, **kwargs):
        payload = deepcopy(old_spec)
        if not params:
            params = self.module.params.get("db_vm", {}).get(
                "use_authorized_server", {}
            )

        if not params:
            return (
                None,
                "Authorized db server vm input is required for creating spec for authorized db server vm",
            )

        time_machine_uuid = kwargs.get("time_machine_uuid") or payload.get(
            "timeMachineId"
        )
        if not time_machine_uuid:
            return (
                None,
                "Time machine uuid is required for creating authorized db server vm spec",
            )

        # get db server vm uuid associated with given time machine
        time_machine = TimeMachine(self.module)
        db_server_vm_uuid, err = time_machine.get_authorized_db_server_vm_uuid(
            time_machine_uuid=time_machine_uuid, config=params
        )
        if err:
            return None, err

        db_server_vm = self.read(uuid=db_server_vm_uuid)

        payload["createDbserver"] = False
        payload["dbserverId"] = db_server_vm_uuid
        payload["nxClusterId"] = db_server_vm.get("nxClusterId")
        payload["nodes"] = [
            {
                "vmName": db_server_vm.get("name"),
                "properties": [],
                "nxClusterId": db_server_vm.get("nxClusterId"),
                "dbserverId": db_server_vm_uuid,
            }
        ]

        return payload, None

    def get_spec_update_vm(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "name": self._build_spec_update_name,
            "desc": self._build_spec_update_desc,
            "reset_name_in_ntnx_cluster": self._build_spec_update_reset_name_in_ntnx_cluster,
            "reset_desc_in_ntnx_cluster": self._build_spec_reset_description,
            "update_credentials": self._build_spec_update_credentials,
        }

        return super().get_spec(old_spec=old_spec, params=params, **kwargs)

    def get_spec_delete_vm(self, old_spec=None, params=None, **kwargs):
        self.build_spec_methods = {
            "delete_from_cluster": self._build_spec_delete_from_cluster,
            "delete_vm_snapshots": self._build_spec_delete_vm_snapshots,
            "delete_vgs": self._build_spec_delete_volume_groups,
            "soft_remove": self._build_spec_soft_remove,
        }

        return super().get_spec(old_spec=old_spec, params=params, **kwargs)

    # builder methods for vm provisioning
    def _build_spec_name(self, payload, name):
        if not payload.get("nodes"):
            payload["nodes"] = [{}]

        payload["nodes"][0]["vmName"] = name
        return payload, None

    def _build_spec_description(self, payload, desc):
        payload["description"] = desc
        return payload, None

    def _build_spec_database_type(self, payload, db_type):
        payload["databaseType"] = db_type
        return payload, None

    def build_spec_compute_profile(self, payload, profile):
        # set compute profile
        compute_profile = ComputeProfile(self.module)
        uuid, err = compute_profile.get_profile_uuid(profile)
        if err:
            return None, err
        payload["computeProfileId"] = uuid
        return payload, None

    def build_spec_software_profile(self, payload, profile):
        # set software profile
        software_profile = SoftwareProfile(self.module)
        uuid, err = software_profile.get_profile_uuid(profile)
        if err:
            return None, err

        payload["softwareProfileId"] = uuid
        if profile.get("version_uuid"):
            payload["softwareProfileVersionId"] = profile["version_uuid"]
        else:
            software_profile = software_profile.read(uuid)
            payload["softwareProfileId"] = uuid
            payload["softwareProfileVersionId"] = software_profile["latestVersionId"]

        return payload, None

    def build_spec_network_profile(self, payload, profile):
        # set network prfile
        network_profile = NetworkProfile(self.module)
        uuid, err = network_profile.get_profile_uuid(profile)
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

    def _build_spec_time_machine(self, payload, time_machine):
        _time_machine = TimeMachine(self.module)
        uuid, err = _time_machine.get_time_machine_uuid(time_machine)
        if err:
            return None, err

        payload["timeMachineId"] = uuid
        if time_machine.get("snapshot_uuid"):
            payload["snapshotId"] = time_machine.get("snapshot_uuid")
            payload["latestSnapshot"] = False
        else:
            payload["latestSnapshot"] = True

        return payload, None

    def _build_spec_time_zone(self, payload, time_zone):
        payload["timeZone"] = time_zone
        return payload, None

    def _build_spec_ip(self, payload, ip):
        payload["ipInfos"] = [{"ipType": "VM_IP", "ipAddresses": [ip]}]
        return payload, None

    def build_spec_password(self, payload, password):
        payload["vmPassword"] = password
        return payload, None

    def build_spec_vms(self, payload, vms, **kwargs):  # noqa: C901
        """
        This method takes list of vm input and create specs for each.
        Pass acceptable defaults in kwargs.
        """
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
            "nxClusterId": kwargs.get("cluster_uuid", ""),
        }

        # get all network profile name uuid map
        network_profile = NetworkProfile(self.module)
        network_profiles, err = network_profile.get_all_name_uuid_map()
        if err:
            return None, err

        # get all compute profile name uuid map
        compute_profile = ComputeProfile(self.module)
        compute_profiles, err = compute_profile.get_all_name_uuid_map()
        if err:
            return None, err

        for vm in vms:

            node = deepcopy(spec)
            node["vmName"] = vm.get("name")

            properties = ["role", "node_type"]

            for prop in properties:
                if prop in vm:
                    node["properties"].append({"name": prop, "value": vm[prop]})

            if vm.get("archive_log_destination"):
                node["properties"].append(
                    {
                        "name": "remote_archive_destination",
                        "value": vm.get("archive_log_destination"),
                    }
                )

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

                node["networkProfileId"] = uuid

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

                node["computeProfileId"] = uuid

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

                node["nxClusterId"] = cluster_uuid

            if vm.get("ip"):
                node, err = self._build_spec_ip(node, vm.get("ip"))
                if err:
                    return None, err

            nodes.append(node)

        payload["nodes"] = nodes
        payload["nodeCount"] = len(payload["nodes"])
        return payload, None

    # builders for registration
    def _build_spec_register_vm_ip(self, payload, ip):
        payload["vmIp"] = ip
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

    def _build_spec_register_username(self, payload, username):
        payload["username"] = username
        return payload, None

    def _build_spec_register_password(self, payload, password):
        payload["password"] = password
        return payload, None

    def _build_spec_register_private_ssh_key(self, payload, private_ssh_key):
        payload["sshPrivateKey"] = private_ssh_key
        return payload, None

    def _build_spec_reset_description(self, payload, reset_desc):
        payload["resetDescriptionInNxCluster"] = reset_desc
        return payload, None

    def _build_spec_register_working_dir(self, payload, working_dir):
        payload["workingDirectory"] = working_dir
        return payload, None

    def _build_spec_update_reset_name_in_ntnx_cluster(self, payload, reset):
        payload["resetNameInNxCluster"] = reset
        return payload, None

    def _build_spec_update_name(self, payload, name):
        if name != payload.get("name", ""):
            payload["name"] = name
            payload["resetName"] = True
        return payload, None

    def _build_spec_update_desc(self, payload, desc):
        if desc != payload.get("desc", ""):
            payload["description"] = desc
            payload["resetDescription"] = True
        return payload, None

    def _build_spec_update_credentials(self, payload, credentials):
        payload["credentials"] = credentials
        payload["resetCredential"] = True
        return payload, None

    # builders for deleting vm spec
    def _build_spec_delete_from_cluster(self, payload, delete_from_cluster):
        payload["delete"] = delete_from_cluster
        return payload, None

    def _build_spec_delete_volume_groups(self, payload, delete_volume_groups):
        payload["deleteVgs"] = delete_volume_groups
        return payload, None

    def _build_spec_soft_remove(self, payload, soft_remove):
        payload["softRemove"] = soft_remove
        payload["remove"] = False
        return payload, None

    def _build_spec_delete_vm_snapshots(self, payload, delete_vm_snapshots):
        payload["deleteVmSnapshots"] = delete_vm_snapshots
        return payload, None

    def resolve_uuids_from_entity_specs(self, vms):
        """
        This helper creates list of uuids from list of db server vms config (containing either name or uuid)
        """
        vms_name_uuid_map = self.get_all_db_servers_name_uuid_map()

        uuids = []
        for vm in vms:

            if vm.get("name"):
                if vms_name_uuid_map.get(vm["name"]):
                    uuid = vms_name_uuid_map[vm["name"]]
                else:
                    return None, "DB server vm with name '{0}' not found".format(
                        vm["name"]
                    )

            elif vm.get("uuid"):
                uuid = vm["uuid"]
            else:
                return None, "uuid or name is required for setting db server vm"

            uuids.append(uuid)

        return uuids, None
