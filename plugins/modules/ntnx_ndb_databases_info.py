#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_databases_info
short_description: info module for ndb database instances
version_added: 1.8.0
description: 'Get database instance info'
options:
      name:
        description:
            - database name
        type: str
      uuid:
        description:
            - database id
        type: str
      filters:
        description:
            - write
        type: dict
        suboptions:
            detailed:
                description:
                    - write
                type: bool
            load_dbserver_cluster:
                description:
                    - write
                type: bool
            order_by_dbserver_cluster:
                description:
                    - write
                type: bool
            order_by_dbserver_logical_cluster:
                description:
                    - write
                type: bool
            value:
                description:
                    - write
                type: str
            value_type:
                description:
                    - write
                type: str
                choices: ["ip","name","database-name"]
            time_zone:
                description:
                    - write
                type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_ndb_base_module
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""


- name: List era databases
  ntnx_ndb_databases_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: databases

- name: Get era databases using its name
  ntnx_ndb_databases_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_name"
  register: result

- name: Get era databases using its uuid
  ntnx_ndb_databases_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of database>"
  register: result

"""
RETURN = r"""
response:
  description: response for listing all databases
  returned: always
  type: list
  sample: [
            {
                "accessLevel": null,
                "category": "DB_GROUP_IMPLICIT",
                "clone": false,
                "clustered": false,
                "databaseClusterType": null,
                "databaseGroupStateInfo": null,
                "databaseName": "PRAD_POSTGRESS",
                "databaseNodes": [
                    {
                        "accessLevel": null,
                        "databaseId": "e4a3cdaf-d643-43c5-8e11-83cbdabf16fa",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 13:13:36",
                        "dateModified": "2022-10-17 13:14:57",
                        "dbserver": null,
                        "dbserverId": "70d53dsaf-8022-44ba-9996-d0b6b351e8d5",
                        "description": "postgres_database PRAD_POSTGRESS on host 10.51.144.207",
                        "id": "fc6f3159-8a45-sadc-98a3-c503d62e2d71",
                        "info": {
                            "info": {},
                            "secureInfo": null
                        },
                        "metadata": null,
                        "name": "PRAD_POSTGRESS",
                        "ownerId": "eac70asa-22fb-462b-9498-949796ca1f73",
                        "primary": false,
                        "properties": [],
                        "protectionDomain": null,
                        "protectionDomainId": "dfdbbcac-ce90-46e6-fgdg-19ba74f1f569",
                        "softwareInstallationId": "0819dd55-4grf0-4a95-9ece-306edsfc404b4a",
                        "status": "READY",
                        "tags": []
                    }
                ],
                "databaseStatus": "UNKNOWN",
                "databases": null,
                "dateCreated": "2022-10-17 12:50:50",
                "dateModified": "2022-10-19 11:50:04",
                "dbserverLogicalClusterId": null,
                "dbserverlogicalCluster": null,
                "description": "new description",
                "eraCreated": true,
                "groupInfo": null,
                "id": "e4a3c27f-d643-43c5-8e11-83sdfabf16fa",
                "info": {
                    "info": {
                        "bpg_configs": {
                            "bpg_db_param": {
                                "effective_cache_size": "3GB",
                                "maintenance_work_mem": "512MB",
                                "max_parallel_workers_per_gather": "2",
                                "max_worker_processes": "8",
                                "shared_buffers": "1024MB",
                                "work_mem": "32MB"
                            },
                            "storage": {
                                "archive_storage": {
                                    "size": 600.0
                                },
                                "data_disks": {
                                    "count": 4.0
                                },
                                "log_disks": {
                                    "count": 4.0,
                                    "size": 100.0
                                }
                            },
                            "vm_properties": {
                                "dirty_background_ratio": 5.0,
                                "dirty_expire_centisecs": 500.0,
                                "dirty_ratio": 15.0,
                                "dirty_writeback_centisecs": 100.0,
                                "nr_hugepages": 118.0,
                                "overcommit_memory": 1.0,
                                "swappiness": 0.0
                            }
                        }
                    },
                    "secureInfo": {}
                },
                "internal": false,
                "lcmConfig": null,
                "linkedDatabases": [
                    {
                        "databaseName": "template0",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 13:12:52",
                        "dateModified": "2022-10-17 13:12:52",
                        "description": null,
                        "id": "56e97fff-4ae2-45d9-sfds9-3fe50b3903d3",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "template0",
                        "ownerId": "eac70dbf-22fb-46sfd-9498-94sfd96ca1f73",
                        "parentDatabaseId": "e4a3c27f-d643-4fd5-8e11-83cbdsdf16fa",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "postgres",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 13:12:52",
                        "dateModified": "2022-10-17 13:12:52",
                        "description": null,
                        "id": "3153a712-c770-456a-b217-0a1c7fsd0a50",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "postgres",
                        "ownerId": "eac70dbf-22fb-462b-9fsd8-94fsd6ca1f73",
                        "parentDatabaseId": "e4a3c27f-d643-43c5-8e11-8sfdabf16fa",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "template1",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 13:12:52",
                        "dateModified": "2022-10-17 13:12:52",
                        "description": null,
                        "id": "41sdfs26e-2913-48a2-b7a6-0a94fbesf16b",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "template1",
                        "ownerId": "easdfdbf-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "e4asds7f-d643-43c5-8e11-83cbdabf16fa",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "root",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-17 13:12:52",
                        "dateModified": "2022-10-17 13:12:52",
                        "description": null,
                        "id": "3d9sfd59-0186-4741-8076-bdsdf269753f",
                        "info": {
                            "info": {
                                "created_by": "user"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "root",
                        "ownerId": "esdfdbf-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "e4asdff-d643-43c5-8e11-83cbdabf16fa",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    }
                ],
                "metadata": {
                    "baseSizeComputed": false,
                    "capabilityResetTime": null,
                    "createdDbservers": null,
                    "deregisterInfo": null,
                    "deregisteredWithDeleteTimeMachine": false,
                    "info": null,
                    "lastLogCatchUpForRestoreOperationId": null,
                    "lastRefreshTimestamp": null,
                    "lastRequestedRefreshTimestamp": null,
                    "logCatchUpForRestoreDispatched": false,
                    "originalDatabaseName": null,
                    "pitrBased": false,
                    "provisionOperationId": "ff5fsdf-6f95-4b58-abf3-e4fbcd6b27fc",
                    "refreshBlockerInfo": null,
                    "registeredDbservers": null,
                    "sanitised": false,
                    "secureInfo": null,
                    "sourceSnapshotId": null,
                    "stateBeforeRefresh": null,
                    "stateBeforeRestore": null,
                    "stateBeforeScaling": null,
                    "tmActivateOperationId": null
                },
                "metric": null,
                "name": "PRAD_POSTGRESS",
                "ownerId": "eaasddf-22fb-462b-9498-94979dsa1f73",
                "parentDatabaseId": null,
                "parentSourceDatabaseId": null,
                "parentTimeMachineId": null,
                "placeholder": false,
                "properties": [
                    {
                        "description": null,
                        "name": "vm_ip",
                        "ref_id": "e4a3asdf-d643-43c5-8e11-83adsabf16fa",
                        "secure": false,
                        "value": "000.000.000.000"
                    },
                    {
                        "description": null,
                        "name": "USAGE_SIZE",
                        "ref_id": "e4aasddf-d643-43c5-8e11-83cadsbf16fa",
                        "secure": false,
                        "value": "0"
                    },
                    {
                        "description": null,
                        "name": "db_parameter_profile_id",
                        "ref_id": "e4a3ads-d643-43c5-8e11-83cbdaadsafa",
                        "secure": false,
                        "value": "a80aasda-8787-4442-8f38-eeb2adsd8cbb"
                    },
                    {
                        "description": null,
                        "name": "auth",
                        "ref_id": "easda27f-d643-43c5-8e11-83adsabf16fa",
                        "secure": false,
                        "value": "md5"
                    },
                    {
                        "description": null,
                        "name": "version",
                        "ref_id": "e4aasdaf-d643-43c5-8e11-83asdbf16fa",
                        "secure": false,
                        "value": "10.4"
                    },
                    {
                        "description": null,
                        "name": "provisioning_spec",
                        "ref_id": "e4das7f-d643-43c5-8e11-83cbasd6fa",
                        "secure": false,
                        "value": ""
                    },
                    {
                        "description": null,
                        "name": "postgres_software_home",
                        "ref_id": "easda27f-d643-43c5-8e11-83cbdabf16fa",
                        "secure": false,
                        "value": "%2Fasdr%2Fpgsql-10.4"
                    },
                    {
                        "description": null,
                        "name": "listener_port",
                        "ref_id": "edasdc27f-d643-43c5-8e11-83cbdabf16fa",
                        "secure": false,
                        "value": "5432"
                    },
                    {
                        "description": null,
                        "name": "SIZE",
                        "ref_id": "edas27f-d643-43c5-8e11-83cbdabf16fa",
                        "secure": false,
                        "value": "295"
                    },
                    {
                        "description": null,
                        "name": "SIZE_UNIT",
                        "ref_id": "easda27f-d643-43c5-8e11-83cbdabf16fa",
                        "secure": false,
                        "value": "GB"
                    },
                    {
                        "description": null,
                        "name": "AUTO_EXTEND_DB_STAGE",
                        "ref_id": "edasdc27f-d643-43c5-8e11-83cbdabf16fa",
                        "secure": false,
                        "value": "true"
                    },
                    {
                        "description": null,
                        "name": "last_backed_up_txn_log",
                        "ref_id": "edasd3c27f-d643-43c5-8e11-83cbdabf16fa",
                        "secure": false,
                        "value": "000000010000000000000001"
                    }
                ],
                "status": "READY",
                "tags": [
                    {
                        "entityId": "easda7f-d643-43c5-8e11-83cbdabf16fa",
                        "entityType": "DATABASE",
                        "tagId": "93asdbe-5b8c-4ba2-a98b-0086272e187d",
                        "tagName": "test",
                        "value": "check1"
                    }
                ],
                "timeMachine": null,
                "timeMachineId": "basd42-1b96-40ba-89ef-52e9feb77003",
                "timeZone": "UTC",
                "type": "postgres_database"
            },
            {
                "accessLevel": null,
                "category": "DB_GROUP_IMPLICIT",
                "clone": false,
                "clustered": false,
                "databaseClusterType": null,
                "databaseGroupStateInfo": null,
                "databaseName": "ujbcfnhq",
                "databaseNodes": [
                    {
                        "accessLevel": null,
                        "databaseId": "2c8asd5-16c7-4cb7-9341-670bd36b684c",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-19 12:02:24",
                        "dateModified": "2022-10-19 12:04:30",
                        "dbserver": null,
                        "dbserverId": "3bdasdcb-f392-4873-9460-960308e043a9",
                        "description": "postgres_database ujbcfnhq on host 10.51.144.214",
                        "id": "cbdasd8-a4db-4f14-b757-32459df965aa",
                        "info": {
                            "info": {},
                            "secureInfo": null
                        },
                        "metadata": null,
                        "name": "ujbcfnhq",
                        "ownerId": "eadasdbf-22fb-462b-9498-949796ca1f73",
                        "primary": false,
                        "properties": [],
                        "protectionDomain": null,
                        "protectionDomainId": "c0asd9-0672-43d4-83df-8167176d4d2a",
                        "softwareInstallationId": "20asd662-8fdb-44b3-9bf4-9f58ff2ca51b",
                        "status": "READY",
                        "tags": []
                    }
                ],
                "databaseStatus": "UNKNOWN",
                "databases": null,
                "dateCreated": "2022-10-19 11:39:20",
                "dateModified": "2022-10-19 12:04:23",
                "dbserverLogicalClusterId": null,
                "dbserverlogicalCluster": null,
                "description": "ansible-created",
                "eraCreated": true,
                "groupInfo": null,
                "id": "2c8asd15-16c7-4cb7-9341-670bd36b684c",
                "info": {
                    "info": {
                        "bpg_configs": {
                            "bpg_db_param": {
                                "effective_cache_size": "3GB",
                                "maintenance_work_mem": "512MB",
                                "max_parallel_workers_per_gather": "2",
                                "max_worker_processes": "8",
                                "shared_buffers": "1024MB",
                                "work_mem": "32MB"
                            },
                            "storage": {
                                "archive_storage": {
                                    "size": 600.0
                                },
                                "data_disks": {
                                    "count": 4.0
                                },
                                "log_disks": {
                                    "count": 4.0,
                                    "size": 100.0
                                }
                            },
                            "vm_properties": {
                                "dirty_background_ratio": 5.0,
                                "dirty_expire_centisecs": 500.0,
                                "dirty_ratio": 15.0,
                                "dirty_writeback_centisecs": 100.0,
                                "nr_hugepages": 118.0,
                                "overcommit_memory": 1.0,
                                "swappiness": 0.0
                            }
                        }
                    },
                    "secureInfo": {}
                },
                "internal": false,
                "lcmConfig": null,
                "linkedDatabases": [
                    {
                        "databaseName": "postgres",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-19 12:01:36",
                        "dateModified": "2022-10-19 12:01:36",
                        "description": null,
                        "id": "94asdad0-172b-4723-bc81-49a15b9bbfc8",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "postgres",
                        "ownerId": "eaasdabf-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "dasd6a15-16c7-4cb7-9341-670dasd684c",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "ansible_test",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-19 12:01:36",
                        "dateModified": "2022-10-19 12:01:36",
                        "description": null,
                        "id": "e1das7bb-8be3-49e0-a42b-8f8ce59c8d7c",
                        "info": {
                            "info": {
                                "created_by": "user"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "ansible_test",
                        "ownerId": "eadasddbf-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "2casdaa15-16c7-4cb7-9341-670bd36b684c",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "template0",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-19 12:01:36",
                        "dateModified": "2022-10-19 12:01:36",
                        "description": null,
                        "id": "7f12dase-22b5-4b47-a6b2-d3729aa8d97a",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "template0",
                        "ownerId": "eac7dasf-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "2cdasda15-16c7-4cb7-9341-670bd36b684c",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    },
                    {
                        "databaseName": "template1",
                        "databaseStatus": "READY",
                        "dateCreated": "2022-10-19 12:01:36",
                        "dateModified": "2022-10-19 12:01:36",
                        "description": null,
                        "id": "61e5das2-8018-4e85-9794-5fe61fc8e4de",
                        "info": {
                            "info": {
                                "created_by": "system"
                            },
                            "secureInfo": null
                        },
                        "metadata": null,
                        "metric": null,
                        "name": "template1",
                        "ownerId": "eac7asd-22fb-462b-9498-949796ca1f73",
                        "parentDatabaseId": "2c836a15-16c7-4cb7-9341-670dasd6b684c",
                        "parentLinkedDatabaseId": null,
                        "snapshotId": null,
                        "status": "READY",
                        "timeZone": null
                    }
                ],
                "metadata": {
                    "baseSizeComputed": false,
                    "capabilityResetTime": null,
                    "createdDbservers": null,
                    "deregisterInfo": null,
                    "deregisteredWithDeleteTimeMachine": false,
                    "info": null,
                    "lastLogCatchUpForRestoreOperationId": null,
                    "lastRefreshTimestamp": null,
                    "lastRequestedRefreshTimestamp": null,
                    "logCatchUpForRestoreDispatched": false,
                    "originalDatabaseName": null,
                    "pitrBased": false,
                    "provisionOperationId": "63751472-ca25-4d94-8f65-54dasde80b59",
                    "refreshBlockerInfo": null,
                    "registeredDbservers": null,
                    "sanitised": false,
                    "secureInfo": null,
                    "sourceSnapshotId": null,
                    "stateBeforeRefresh": null,
                    "stateBeforeRestore": null,
                    "stateBeforeScaling": null,
                    "tmActivateOperationId": "66339401-2eda-4e28-abff-basdcb9f9031"
                },
                "metric": null,
                "name": "ujbcfnhq",
                "ownerId": "eac70dbf-22fb-462b-9498-94asd6ca1f73",
                "parentDatabaseId": null,
                "parentSourceDatabaseId": null,
                "parentTimeMachineId": null,
                "placeholder": false,
                "properties": [
                    {
                        "description": null,
                        "name": "version",
                        "ref_id": "2c836a15-16c7-4cb7-9341-6dasd36b684c",
                        "secure": false,
                        "value": "10.4"
                    },
                    {
                        "description": null,
                        "name": "vm_ip",
                        "ref_id": "2c836a15-16c7-4cb7-9341-6dasd36b684c",
                        "secure": false,
                        "value": "xx.xx.xx.xx"
                    },
                    {
                        "description": null,
                        "name": "postgres_software_home",
                        "ref_id": "2c836a15-16c7-4cb7-9341-6asd36b684c",
                        "secure": false,
                        "value": "%2Fusr%2Fpgsql-10.4"
                    },
                    {
                        "description": null,
                        "name": "db_parameter_profile_id",
                        "ref_id": "2c836a15-16c7-4cb7-9341-670dasb684c",
                        "secure": false,
                        "value": "a80ac1fb-8787-4442-8f38-eebdas7a8cbb"
                    },
                    {
                        "description": null,
                        "name": "auth",
                        "ref_id": "2c836a15-16c7-4cb7-9341-67dasb684c",
                        "secure": false,
                        "value": "md5"
                    },
                    {
                        "description": null,
                        "name": "AUTO_EXTEND_DB_STAGE",
                        "ref_id": "2c83das15-16c7-4cb7-9341-670bd36b684c",
                        "secure": false,
                        "value": "true"
                    },
                    {
                        "description": null,
                        "name": "provisioning_spec",
                        "ref_id": "2sada15-16c7-4cb7-9341-6dasd36b684c",
                        "secure": false,
                        "value": ""
                    },
                    {
                        "description": null,
                        "name": "listener_port",
                        "ref_id": "2c836a15-16c7-4cb7-9341-670dasdf6b684c",
                        "secure": false,
                        "value": "5432"
                    }
                ],
                "status": "READY",
                "tags": [
                    {
                        "entityId": "2c83wea15-16c7-4cb7-9341-6asd36b684c",
                        "entityType": "DATABASE",
                        "tagId": "a5312c47-b4aa-4133-88cd-079387423g279",
                        "tagName": "test1",
                        "value": "check1"
                    }
                ],
                "timeMachine": null,
                "timeMachineId": "a71as3e0-5dc5-4336-8484-8214ea43a440",
                "timeZone": "UTC",
                "type": "postgres_database"
            }
        ]

"""

from ..module_utils.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.utils import format_filters_map  # noqa: E402


def get_module_spec():

    filters_spec = dict(
        detailed=dict(type="bool"),
        load_dbserver_cluster=dict(type="bool"),
        order_by_dbserver_cluster=dict(type="bool"),
        order_by_dbserver_logical_cluster=dict(type="bool"),
        value=dict(type="str"),
        value_type=dict(
            type="str",
            choices=[
                "ip",
                "name",
                "database-name",
            ],
        ),
        time_zone=dict(type="str"),
    )
    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        filters=dict(
            type="dict",
            options=filters_spec,
        ),
    )

    return module_args


def get_database(module, result):
    database = DatabaseInstance(module)
    query_params = module.params.get("filters")
    query_params = format_filters_map(query_params)

    if module.params.get("name"):
        name = module.params["name"]
        resp, err = database.get_database(name=name, query=query_params)
    else:
        uuid = module.params["uuid"]
        resp, err = database.get_database(uuid=uuid, query=query_params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching database info", **result)
    result["response"] = resp


def get_databases(module, result):
    database = DatabaseInstance(module)
    query_params = module.params.get("filters")
    query_params = format_filters_map(query_params)

    resp = database.read(query=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("name", "uuid")],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_database(module, result)
    else:
        get_databases(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
