#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_clones_info
short_description: info module for database clones
version_added: 1.8.0-beta.1
description: 'Get clone info'
options:
      name:
        description:
            - clone name
        type: str
      uuid:
        description:
            - clone id
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List all era db clones
  ntnx_ndb_clones_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: clones

- name: get era clones using it's name
  ntnx_ndb_clones_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_clone"
  register: result

- name: List clones use id
  ntnx_ndb_clones_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of clone>"
  register: result

"""
RETURN = r"""
response:
  description: response for listing all clones
  returned: always
  type: list
  sample:
   [
            {
                "accessLevel": null,
                "category": "DB_GROUP_IMPLICIT",
                "clone": true,
                "clustered": false,
                "databaseClusterType": null,
                "databaseGroupStateInfo": null,
                "databaseName": "root",
                "databaseNodes": [
                    {
                        "accessLevel": null,
                        "databaseId": "3bf23402-67f0-yd87-967d-3a80b1d336f9",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 17:10:46",
                        "dateModified": "2022-10-17 17:10:46",
                        "dbserver": null,
                        "dbserverId": "eafakzef-5e63-4e93-bfa5-bb79967e3f3c",
                        "description": "",
                        "id": "e45a4eb7-c32a-4895-a32d-8450fe0b6be3",
                        "info": {
                            "info": null,
                            "secureInfo": null
                        },
                        "metadata": null,
                        "name": "PRAD_POSTGRESS_2022_Oct_17_22_35_49",
                        "ownerId": "eac70dbf-22fb-462b-9498-965796ca1f73",
                        "primary": false,
                        "properties": [],
                        "protectionDomain": null,
                        "protectionDomainId": "3e62f008-7739-47a5-b26c-fd6971a110d8",
                        "softwareInstallationId": "2ac645c8-988b-4cbf-9dc6-b37d19b4464f",
                        "status": "READY",
                        "tags": []
                    }
                ],
                "databaseStatus": "UNKNOWN",
                "databases": null,
                "dateCreated": "2022-10-17 17:06:12",
                "dateModified": "2022-10-19 11:07:11",
                "dbserverLogicalClusterId": null,
                "dbserverlogicalCluster": null,
                "description": "",
                "eraCreated": true,
                "groupInfo": null,
                "id": "3bfe2902-67f0-4d87-967d-3a80b1d361f9",
                "info": null,
                "internal": false,
                "lcmConfig": null,
                "linkedDatabases": [
                    {
                        "databaseName": "postgres",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 17:10:00",
                        "dateModified": "2022-10-17 17:10:00",
                        "description": null,
                        "id": "255e2610-d78a-42f5-8878-80ca01048651",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "postgres",
                        "ownerId": "eac70dbf-22fb-462b-9218-949796ca1f73",
                        "parentDatabaseId": "3bfe2902-74f0-4d87-967d-3a80b1d336f9",
                        "parentLinkedDatabaseId": "7453a712-c770-456a-b217-0a1c74bf0a50",
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "root",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 17:10:00",
                        "dateModified": "2022-10-17 17:10:00",
                        "description": null,
                        "id": "b93c2c70-fc6b-4148-8871-9c2912cea041",
                        "info": {
                            "info": {
                                "created_by": "user"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "root",
                        "ownerId": "eac70dbf-22fb-462b-9148-949796ca1f73",
                        "parentDatabaseId": "3bfe2907-47f0-4d87-967d-3a80b1d336f9",
                        "parentLinkedDatabaseId": "4195a159-0186-4741-8076-bd815269753f",
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "template1",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 17:10:00",
                        "dateModified": "2022-10-17 17:10:00",
                        "description": null,
                        "id": "50b6fd43-c5ee-4e85-b1f3-241ce3b16377",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "template1",
                        "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "3bfe2902-78f0-4d87-967d-3a80b1d336f9",
                        "parentLinkedDatabaseId": "4115126e-2913-48a2-b7a6-0a94fbefe16b",
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "template0",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 17:10:00",
                        "dateModified": "2022-10-17 17:10:00",
                        "description": null,
                        "id": "eb3b9d14-91bb-4735-9479-2366a45b592b",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "template0",
                        "ownerId": "eac70dbf-22fb-462b-9298-949796ca1f73",
                        "parentDatabaseId": "3bfe2902-67f0-4d87-9682d-3a80b1d336f9",
                        "parentLinkedDatabaseId": "56e97fff-4ae2-12d9-9c89-3fe50b3903d3",
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    }
                ],
                "metadata": {
                    "baseSizeComputed": true,
                    "capabilityResetTime": null,
                    "createdDbservers": null,
                    "deregisterInfo": null,
                    "deregisteredWithDeleteTimeMachine": false,
                    "info": null,
                    "lastLogCatchUpForRestoreOperationId": null,
                    "lastRefreshTimestamp": "2022-10-17 13:17:48",
                    "lastRequestedRefreshTimestamp": null,
                    "logCatchUpForRestoreDispatched": false,
                    "originalDatabaseName": null,
                    "pitrBased": false,
                    "provisionOperationId": null,
                    "refreshBlockerInfo": null,
                    "registeredDbservers": null,
                    "sanitised": false,
                    "secureInfo": null,
                    "sourceSnapshotId": "7657037a-c39d-dsada-99cd-d90217b40a9d",
                    "stateBeforeRefresh": null,
                    "stateBeforeRestore": null,
                    "stateBeforeScaling": null,
                    "tmActivateOperationId": null
                },
                "metric": null,
                "name": "PRAD_POSTGRESS_2022_Oct_17_22_35_49",
                "ownerId": "eac70dbf-22fb-462b-9498-9497dasca1f73",
                "parentDatabaseId": null,
                "parentSourceDatabaseId": null,
                "parentTimeMachine": null,
                "parentTimeMachineId": "b051e542-1b96-40ba-dsef-52e9feb77003",
                "placeholder": false,
                "properties": [
                    {
                        "description": null,
                        "name": "version",
                        "ref_id": "3bfe2902-67f0-4d87-967d-3asdb1d336f9",
                        "secure": false,
                        "value": "10.4"
                    },
                    {
                        "description": null,
                        "name": "vm_ip",
                        "ref_id": "3bfe2902-67f0-4d87-967d-3asdb1d336f9",
                        "secure": false,
                        "value": "000.000.000.000"
                    },
                    {
                        "description": null,
                        "name": "postgres_software_home",
                        "ref_id": "3bfe2902-67f0-4d87-967d-3asdb1d336f9",
                        "secure": false,
                        "value": "%2Fusr%2Fpgsql-10.4"
                    },
                    {
                        "description": null,
                        "name": "listener_port",
                        "ref_id": "3sde2902-67f0-4d87-967d-3a80b1d336f9",
                        "secure": false,
                        "value": "5432"
                    },
                    {
                        "description": null,
                        "name": "db_parameter_profile_id",
                        "ref_id": "3sae2902-67f0-4d87-967d-3a80b1d336f9",
                        "secure": false,
                        "value": "a8auc1fb-8787-4442-8f38-eeb2417a8cbb"
                    },
                    {
                        "description": null,
                        "name": "BASE_SIZE",
                        "ref_id": "3gfe2902-67f0-4d87-967d-3a80b1d336f9",
                        "secure": false,
                        "value": "{\"clusterStorage\":
                         {\"d7881b99-5a9d-4da7-8e7d-c938499214de\":
                         {\"41f39cb1-a5fd-4bc8-bb78-d3fe81a76539\":
                         {\"size\": 26416896, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                          \"dcd08c14-20dd-4b27-893c-c65a4c2e1d3b\":
                          {\"size\": 23134208, \"allocatedSize\": 0,
                          \"usedSize\": 0, \"unit\": \"B\"}, \"7c695994-a1ff-459c-9174-c93f75b470a4\":
                           {\"size\": 9189376, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"},
                           \"c35e56bd-f1b8-4349-b9aa-a86273c473c3\": {\"size\": 5496832, \"allocatedSize\": 0, \"usedSize\": 0, \"unit\": \"B\"}}}}"
                    }
                ],
                "status": "READY",
                "tags": [],
                "timeMachine": null,
                "timeMachineId": "f5gf5d90-835c-4d37-a922-3a936aaa21da",
                "timeZone": "UTC",
                "type": "postgres_database"
            }
        ]

"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.clones import Clone  # noqa: E402


def get_module_spec():

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
    )

    return module_args


def get_clone(module, result):
    clone = Clone(module)
    if module.params.get("name"):
        name = module.params["name"]
        resp, err = clone.get_clone(name=name)
    else:
        uuid = module.params["uuid"]
        resp, err = clone.get_clone(uuid=uuid)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching clone info", **result)

    result["response"] = resp


def get_clones(module, result):
    clone = Clone(module)

    resp = clone.read()

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_clone(module, result)
    else:
        get_clones(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
