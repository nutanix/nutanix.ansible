#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_db_servers_info
short_description: info module for ndb db server vms info
version_added: 1.8.0-beta.1
description: 'Get database server info'
options:
      name:
        description:
            - server name
        type: str
      uuid:
        description:
            - server id
        type: str
      server_ip:
        description:
            - db server vm ip
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List era db_servers
  ntnx_ndb_db_servers_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: db_servers

- name: get era db_servers using it's name
  ntnx_ndb_db_servers_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result

- name: get era db_servers using it's id
  ntnx_ndb_db_servers_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of db_server>"
  register: result

- name: get era db_servers using ip
  ntnx_ndb_db_servers_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    server_ip: "<ip of db_server>"
  register: result
"""
RETURN = r"""
response:
  description: listing all db servers
  returned: always
  type: list
  sample: [
            {
                "accessKey": null,
                "accessKeyId": "883dasd5bb-8122-473e-91d5-434asd785426",
                "accessLevel": null,
                "associatedTimeMachineIds": null,
                "associated_time_machine_id": null,
                "clientId": "d7adas12e-8042-48e1-95c1-2362dasdd653",
                "clones": null,
                "clustered": false,
                "databaseType": "postgres_database",
                "databases": null,
                "dateCreated": "2022-10-14 12:22:36",
                "dateModified": "2022-10-19 12:44:10",
                "dbserverClusterId": null,
                "dbserverInValidEaState": true,
                "description": "DBServer for pnkwlheh",
                "eraCreated": true,
                "eraDrive": null,
                "eraDriveId": "c225dsafcb-8f16-4d86-8eac-56ad85c1789f",
                "eraVersion": "2.4.1",
                "fqdns": null,
                "id": "eaf72bef-das63-4e93-bfa5-bb799das3f3c",
                "info": null,
                "internal": false,
                "ipAddresses": [
                    "000.000.000.000"
                ],
                "is_server_driven": false,
                "lcmConfig": null,
                "macAddresses": [
                    "xx:xx:xx:xx:xx"
                ],
                "metadata": {
                    "associatedTimeMachines": [
                        "b05das42-1b96-40ba-89ef-52e9fdas003"
                    ],
                    "clustered": false,
                    "databaseType": "postgres_database",
                    "deregisterInfo": null,
                    "eraDriveInitialised": true,
                    "info": null,
                    "lastClockSyncAlertTime": null,
                    "leaderMetadata": null,
                    "markedForDeletion": false,
                    "physicalEraDrive": true,
                    "pinnedHostId": null,
                    "protectionDomainMigrationStatus": null,
                    "provisionOperationId": "8d9das7b-eeb1-48df-b277-be27927e19e3",
                    "secureInfo": null,
                    "singleInstance": true,
                    "softwareSnaphotInterval": 0
                },
                "metric": null,
                "name": "wuuoyqzj",
                "nxClusterId": "d78das99-5a9d-4da7-8e7d-c9dsa499214de",
                "ownerId": "eac70dbf-22fb-462b-9498-94979dsaa1f73",
                "placeholder": false,
                "properties": [
                    {
                        "description": null,
                        "name": "software_profile_version_id",
                        "ref_id": "eafsadef-5e63-4e93-bfa5-bb79dsa3f3c",
                        "secure": false,
                        "value": "1c34dase-0f44-43d6-b886-af10fdsa9783"
                    },
                    {
                        "description": null,
                        "name": "vm_core_count",
                        "ref_id": "eafdsaf-5e63-4e93-bfa5-bdsa67e3f3c",
                        "secure": false,
                        "value": "1"
                    },
                    {
                        "description": null,
                        "name": "compute_profile_id",
                        "ref_id": "eadasbef-5e63-4e93-bfa5-bbdas7e3f3c",
                        "secure": false,
                        "value": "75a0dsab-d67b-4474-86e6-af6dasaeb71"
                    },
                    {
                        "description": null,
                        "name": "network_profile_id",
                        "ref_id": "eadasef-5e63-4e93-bfa5-bb79dase3f3c",
                        "secure": false,
                        "value": "6dsac92-450f-4b7b-aa62-eebdase2d91d"
                    },
                    {
                        "description": null,
                        "name": "software_profile_id",
                        "ref_id": "eaf7ewf-5e63-4e93-bfa5-bda7e3f3c",
                        "secure": false,
                        "value": "b00bewa-41f1-4f01-8201-e0cddasd7dbc6"
                    },
                    {
                        "description": null,
                        "name": "access_key_id",
                        "ref_id": "eadsad2bef-5e63-4e93-bfa5-bbczxc7e3f3c",
                        "secure": false,
                        "value": "883dasb-8122-473e-91d5-43vsdv6785426"
                    },
                    {
                        "description": null,
                        "name": "era_user",
                        "ref_id": "eafdasef-5e63-4e93-bfa5-bbsa67e3f3c",
                        "secure": false,
                        "value": "era"
                    },
                    {
                        "description": null,
                        "name": "era_base",
                        "ref_id": "eadasbef-5e63-4e93-bfa5-bb799sad3c",
                        "secure": false,
                        "value": "/opt/era_base"
                    },
                    {
                        "description": null,
                        "name": "current_op_id",
                        "ref_id": "eafdaef-5e63-4e93-bfa5-bb7da7e3f3c",
                        "secure": false,
                        "value": "8d9dsab-eeb1-48df-b277-bedasd19e3"
                    },
                    {
                        "description": null,
                        "name": "isEraCreated",
                        "ref_id": "edsaef-5e63-4e93-bfa5-bb7dasdf3c",
                        "secure": false,
                        "value": "true"
                    },
                    {
                        "description": null,
                        "name": "software_home",
                        "ref_id": "das2bef-5e63-4e93-bfa5-bb7dsade3f3c",
                        "secure": false,
                        "value": "/usr/pgsql-10.4"
                    },
                    {
                        "description": null,
                        "name": "vm_ip_address_list",
                        "ref_id": "edasdef-5e63-4e93-bfa5-bbdasd7e3f3c",
                        "secure": false,
                        "value": "000.000.000.000"
                    },
                    {
                        "description": null,
                        "name": "working_dir",
                        "ref_id": "eaf7dasdf-5e63-4e93-bfa5-bb79asda3f3c",
                        "secure": false,
                        "value": "/tmp"
                    },
                    {
                        "description": null,
                        "name": "os_type",
                        "ref_id": "eafdasdf-5e63-4e93-bfa5-bb79dasd3f3c",
                        "secure": false,
                        "value": "linux"
                    },
                    {
                        "description": null,
                        "name": "application_type",
                        "ref_id": "eadsadef-5e63-4e93-bfa5-bbdasd7e3f3c",
                        "secure": false,
                        "value": "postgres_database"
                    },
                    {
                        "description": null,
                        "name": "application_version",
                        "ref_id": "edadbef-5e63-4e93-bfa5-bdasd967e3f3c",
                        "secure": false,
                        "value": "10.4"
                    },
                    {
                        "description": null,
                        "name": "os_info",
                        "ref_id": "eafdasf-5e63-4e93-bfa5-dasd9967e3f3c",
                        "secure": false,
                        "value": "Linux wuuoyqzj 5.10.0-1.el7.elrepo.x86_64 #1 SMP Sun Dec 13 18:34:48 EST 2020 x86_64 x86_64 x86_64 GNU/Linux\n"
                    },
                    {
                        "description": null,
                        "name": "node_type",
                        "ref_id": "eadasef-5e63-4e93-bfa5-bdas67e3f3c",
                        "secure": false,
                        "value": "database"
                    },
                    {
                        "description": null,
                        "name": "vm_cpu_count",
                        "ref_id": "eadasdbef-5e63-4e93-bfa5-bb799dsad3f3c",
                        "secure": false,
                        "value": "2"
                    },
                    {
                        "description": null,
                        "name": "listener_port",
                        "ref_id": "eadasdef-5e63-4e93-bfa5-bb79dasde3f3c",
                        "secure": false,
                        "value": "5432"
                    }
                ],
                "protectionDomain": null,
                "protectionDomainId": "7a16dasd-8596-4e19-9aed-b776adsa736a",
                "queryCount": 0,
                "requestedVersion": null,
                "softwareInstallations": null,
                "status": "UP",
                "tags": [],
                "time_machine_info": null,
                "type": "DBSERVER",
                "validDiagnosticBundleState": true,
                "vmClusterName": "wuuosyqzj",
                "vmClusterUuid": "417das8-c8e0-4718-b91f-cb40dasbd95",
                "vmInfo": {
                    "deregisterInfo": null,
                    "distribution": null,
                    "info": null,
                    "networkInfo": [
                        {
                            "accessInfo": [
                                {
                                    "accessType": "PRISM",
                                    "destinationSubnet": ""
                                },
                                {
                                    "accessType": "DSIP",
                                    "destinationSubnet": "000.000.000.000/23"
                                },
                                {
                                    "accessType": "ERA_SERVER",
                                    "destinationSubnet": "000.000.000.000/24"
                                },
                                {
                                    "accessType": "PUBLIC",
                                    "destinationSubnet": null
                                }
                            ],
                            "defaultGatewayDevice": true,
                            "deviceName": "eth0",
                            "eraConfigured": true,
                            "flags": "4163<UP,BROADCAST,RUNNING,MULTICAST> ",
                            "gateway": "000.000.000.000",
                            "hostname": null,
                            "ipAddresses": [
                                "000.000.000.000"
                            ],
                            "macAddress": "00000-0000-00000-0000000",
                            "mtu": "1500",
                            "subnetMask": "000.000.000.000",
                            "vlanName": "vlan.x",
                            "vlanType": "Static",
                            "vlanUuid": "00000-0000-00000-0000000"
                        }
                    ],
                    "osType": null,
                    "osVersion": null,
                    "secureInfo": null
                },
                "vmTimeZone": "UTC",
                "windowsDBServer": false,
                "workingDirectory": "/tmp"
            }
        ]
"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.db_servers import DBServers  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        server_ip=dict(type="str"),
    )

    return module_args


def get_db_server(module, result):
    db_server = DBServers(module)
    if module.params.get("uuid"):
        resp, err = db_server.get_db_server(uuid=module.params["uuid"])
    elif module.params.get("name"):
        resp, err = db_server.get_db_server(name=module.params["name"])
    else:
        resp, err = db_server.get_db_server(ip=module.params["server_ip"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching database server info", **result)

    result["response"] = resp


def get_db_servers(module, result):
    db_server = DBServers(module)

    resp = db_server.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid", "server_ip")],
    )
    result = {"changed": False, "error": None, "response": None}
    if (
        module.params.get("name")
        or module.params.get("uuid")
        or module.params.get("server_ip")
    ):
        get_db_server(module, result)
    else:
        get_db_servers(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
