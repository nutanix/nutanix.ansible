#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_profiles
short_description: module for create, update and delete of profiles
version_added: 1.8.0
description:
    - module for create, update and delete of profiles
    - currently, compute, network, database parameters and software profiles are supported
    - only software profile supports versions operations
    - version related operations can be configured under "software"
    - only software profile supports multi cluster availibility
options:
      profile_uuid:
        description:
            - uuid of profile for delete or update
        type: str
      name:
        description:
            - name of profile
        type: str
      desc:
        description:
            - profile description
        type: str
      type:
        description:
            - type of profile
            - required for creation
        type: str
        choices: ["software", "compute", "network", "database_parameter"]
      database_type:
        description:
            - database engine type
            - required for database params, network and software profile
        type: str
        choices: ["postgres"]
      compute:
        description:
            - for creating compute profile
            - idempotency not supported
        type: dict
        suboptions:
            publish:
                description:
                    - set to publish the profile
                    - only valid during update
                type: bool
            vcpus:
                description:
                    - vcpus
                type: int
            cores_per_cpu:
                description:
                    - cores per vcpu
                type: int
            memory:
                description:
                    - memory
                type: int
      clusters:
            description:
                - list of clusters where profiles should be available
                - only applicable for software profile
            type: list
            elements: dict
            suboptions:
                name:
                    description:
                        - name of cluster
                        - mutually exclusive with C(uuid)
                    type: str
                uuid:
                    description:
                        - uuid of cluster
                        - mutually exclusive with C(name)
                    type: str
      software:
        description:
            - software profile configuration
            - during create, it will create base version
            - idempotency not supported
        type: dict
        suboptions:
            publish:
                description:
                    - set to publish the profile
                    - only valid during update
                type: bool
            deprecate:
                description:
                    - set to deprecate the profile
                    - only valid during update
                type: bool
            topology:
                description:
                    - topology of profile
                type: str
                choices: ["single", "cluster"]
            state:
                description:
                    - when C(state)=present, it will create new version
                    - when C(state)=absent, it will create version as per version_uuid
                type: str
                choices: ["present", "absent"]
                default: "present"
            version_uuid:
                description:
                    - version uuid for version update or delete
                type: str
            name:
                description:
                    - name of version
                type: str
            desc:
                description:
                    - description of version
                type: str
            notes:
                description:
                    - notes
                    - update not supported
                type: dict
                suboptions:
                    os:
                        description:
                            - operating system notes in profile
                        type: str
                    db_software:
                        description:
                            - database software notes in profile
                        type: str
            db_server_vm:
                description:
                    - source database server vm for creating software profile
                type: dict
                suboptions:
                    name:
                        description:
                            - name of database server vm
                            - mutually exclusive with C(uuid)
                        type: str
                    uuid:
                        description:
                            - uuid of database server vm
                            - mutually exclusive with C(name)
                        type: str
      network:
        description:
            - network profile configuration
            - idempotency not supported
        type: dict
        suboptions:
            publish:
                description:
                    - set to publish the profile
                    - only valid during update
                type: bool
            topology:
                description:
                    - topology of profile
                type: str
                choices: ["single", "cluster"]
            vlans:
                description:
                    - list of vlans configuration to be added in network profile
                type: list
                elements: dict
                suboptions:
                    cluster:
                        description:
                            - cluster of vlan
                        type: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - name of cluster
                                    - mutually exclusive with C(uuid)
                                type: str
                            uuid:
                                description:
                                    - uuid of cluster
                                    - mutually exclusive with C(name)
                                type: str
                    vlan_name:
                        description:
                            - name of vlan to be added
                        type: str
                        required: true
            enable_ip_address_selection:
                description:
                    - set to enable ip address selection
                type: bool
      database_parameter:
        description:
            - database parameter profile configuration
            - idempotency not supported
        type: dict
        suboptions:
            publish:
                description:
                    - set to publish the profile
                    - only valid during update
                type: bool
            postgres:
                description:
                    - database params for postgres
                type: dict
                suboptions:
                            max_connections:
                                description:
                                    - max number of connections
                                    - default is 100
                                type: int
                            max_replication_slots:
                                description:
                                    - maximum replication slots
                                    - default is 10
                                type: int
                            max_locks_per_transaction:
                                description:
                                    - max locks per transactions
                                    - default is 64
                                type: int
                            effective_io_concurrency:
                                description:
                                    - effective I/O concurrency
                                    - default is 1
                                type: int
                            timezone:
                                description:
                                    - timezone
                                    - default is 'UTC'
                                type: str
                            max_prepared_transactions:
                                description:
                                    - maximum prepared transactions
                                    - default is 0
                                type: int
                            max_wal_senders:
                                description:
                                    - max wal senders
                                    - default 10
                                type: int
                            min_wal_size:
                                description:
                                    - max wal logs size in MB
                                    - default is 80
                                type: int
                            max_wal_size:
                                description:
                                    - max wal logs size in GB
                                    - default is 1
                                type: int
                            wal_keep_segments:
                                description:
                                    - wal logs keep segments
                                    - default is 700
                                type: int
                            max_worker_processes:
                                description:
                                    - max number of worker processes
                                    - default is 8
                                type: int
                            checkpoint_timeout:
                                description:
                                    - checkpoint time out in minutes
                                    - default is 5
                                type: int
                            autovacuum:
                                description:
                                    - on/off autovaccum
                                    - default is on
                                type: str
                                choices: ["on", "off"]
                            checkpoint_completion_target:
                                description:
                                    - checkpoint completion target
                                    - deafult is 0.5
                                type: float
                            autovacuum_freeze_max_age:
                                description:
                                    - autovacuum freeze max age
                                    - default is 200000000
                                type: int
                            autovacuum_vacuum_threshold:
                                description:
                                    - auto vacuum threshold
                                    - default is 50
                                type: int
                            autovacuum_vacuum_scale_factor:
                                description:
                                    - autovacuum scale factor
                                    - default is 0.2
                                type: float
                            autovacuum_work_mem:
                                description:
                                    - autovacum work memory in KB
                                    - default is -1
                                type: int
                            autovacuum_max_workers:
                                description:
                                    - autovacuum max workers
                                    - deafult is 3
                                type: int
                            autovacuum_vacuum_cost_delay:
                                description:
                                    - autovacuum cost delay in milliseconds
                                    - default is 2
                                type: int
                            wal_buffers:
                                description:
                                    - wal buffers
                                    - default is -1
                                type: int
                            synchronous_commit:
                                description:
                                    - synchronous commit flag
                                type: str
                                choices: ["on", "off", "local", "remote_apply", "remote_write"]
                            random_page_cost:
                                description:
                                    - random page cost
                                    - default is 4
                                type: int

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: creation of db params profile
  ntnx_ndb_profiles:
    name: "{{profile1_name}}"
    desc: "testdesc"
    type: database_parameter
    database_type: postgres
    database_parameter:
      postgres:
        max_connections: "{{max_connections}}"
        max_replication_slots: "{{max_replication_slots}}"
        max_locks_per_transaction: "{{max_locks_per_transaction}}"
        effective_io_concurrency: "{{effective_io_concurrency}}"
        timezone: "{{timezone}}"
        max_prepared_transactions: "{{max_prepared_transactions}}"
        max_wal_senders: "{{max_wal_senders}}"
        min_wal_size: "{{min_wal_size}}"
        max_wal_size: "{{max_wal_size}}"
        wal_keep_segments: "{{wal_keep_segments}}"
        max_worker_processes: "{{max_worker_processes}}"
        checkpoint_timeout: "{{checkpoint_timeout}}"
        autovacuum: "{{autovacuum}}"
        checkpoint_completion_target: "{{checkpoint_completion_target}}"
        autovacuum_freeze_max_age: "{{autovacuum_freeze_max_age}}"
        autovacuum_vacuum_threshold: "{{autovacuum_vacuum_threshold}}"
        autovacuum_vacuum_scale_factor: "{{autovacuum_vacuum_scale_factor}}"
        autovacuum_work_mem: "{{autovacuum_work_mem}}"
        autovacuum_max_workers: "{{autovacuum_max_workers}}"
        autovacuum_vacuum_cost_delay:  "{{autovacuum_vacuum_cost_delay}}"
        wal_buffers: "{{wal_buffers}}"
        synchronous_commit: "{{synchronous_commit}}"
        random_page_cost: "{{random_page_cost}}"
  register: result

- name: create of single cluster network profile
  ntnx_ndb_profiles:
    name: "{{profile1_name}}"
    desc: "testdesc"
    type: network
    database_type: postgres
    network:
      topology: single
      vlans:
        -
          cluster:
            name: "{{network_profile.single.cluster.name}}"
          vlan_name: "{{network_profile.single.vlan_name}}"
      enable_ip_address_selection: true
  register: result

- name: create of multiple cluster network profile
  ntnx_ndb_profiles:
    name: "{{profile3_name}}"
    desc: "testdesc"
    type: network
    database_type: postgres
    network:
      topology: cluster
      vlans:
        -
          cluster:
            name: "{{network_profile.HA.cluster1.name}}"
          vlan_name: "{{network_profile.HA.cluster1.vlan_name}}"
        -
          cluster:
            name: "{{network_profile.HA.cluster2.name}}"
          vlan_name: "{{network_profile.HA.cluster2.vlan_name}}"

- name: creation of compute profile
  ntnx_ndb_profiles:
    name: "{{profile1_name}}"
    desc: "testdesc"
    type: compute
    compute:
          vcpus: 2
          cores_per_cpu: 4
          memory: 8
  register: result

- name: create software profile with base version and cluster instance topology. Replicated to multiple clusters
  ntnx_ndb_profiles:
    name: "{{profile1_name}}-replicated"
    desc: "{{profile1_name}}-desc-replicated"
    type: "software"
    database_type: "postgres"
    software:
      topology: "cluster"
      name: "v1.0"
      desc: "v1.0-desc"
      notes:
        os: "os_notes"
        db_software: "db_notes"
      db_server_vm:
        uuid: "{{db_server_vm.uuid}}"
    clusters:
      - name: "{{cluster.cluster1.name}}"
      - uuid: "{{cluster.cluster2.uuid}}"
  register: result

- name: create software profile version
  ntnx_ndb_profiles:
    profile_uuid: "{{profile_uuid}}"
    database_type: "postgres"
    software:
      name: "v2.0"
      desc: "v2.0-desc"
      notes:
        os: "os_notes for v2"
        db_software: "db_notes for v2"
      db_server_vm:
        uuid: "{{db_server_vm.uuid}}"

  register: result


- name: update software profile version
  ntnx_ndb_profiles:
    profile_uuid: "{{profile_uuid}}"
    database_type: "postgres"
    software:
      version_uuid: "{{result.version_uuid}}"
      name: "v2.0-updated"
      desc: "v2.0-desc-updated"

  register: result

- name: publish software profile version
  ntnx_ndb_profiles:
    profile_uuid: "{{profile_uuid}}"
    software:
      version_uuid: "{{version_uuid}}"
      publish: True
  register: result

"""

RETURN = r"""
response:
  description: response when profile is created
  returned: always
  type: dict
  sample: {
            "dateCreated": "2023-02-28 10:54:56",
            "dateModified": "2023-02-28 10:54:56",
            "dbVersion": "ALL",
            "description": "new_name",
            "engineType": "postgres_database",
            "id": "76c1d0eb-28b8-4f37-aa8a-e17dfa1c87a6",
            "latestVersion": "1.0",
            "latestVersionId": "801c60da-9273-45bc-ab00-81fd452a5fa2",
            "name": "new_name1",
            "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
            "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "status": "READY",
            "systemProfile": false,
            "topology": "cluster",
            "type": "Network",
            "versions": [
                {
                    "dateCreated": "2023-02-28 10:54:56",
                    "dateModified": "2023-02-28 10:54:56",
                    "dbVersion": "ALL",
                    "deprecated": false,
                    "description": "new_name",
                    "engineType": "postgres_database",
                    "id": "801c60da-9273-45bc-ab00-81fd452a5fa2",
                    "name": "new_name1 (1.0)",
                    "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "profileId": "76c1d0eb-28b8-4f37-aa8a-e17dfa1c87a6",
                    "properties": [
                        {
                            "name": "CLUSTER_NAME_0",
                            "secure": false,
                            "value": "c1"
                        },
                        {
                            "name": "CLUSTER_ID_0",
                            "secure": false,
                            "value": "0a3b964f-8616-40b9-a564-99cf35f4b8d8"
                        },
                        {
                            "name": "CLUSTER_NAME_1",
                            "secure": false,
                            "value": "c2"
                        },
                        {
                            "name": "CLUSTER_ID_1",
                            "secure": false,
                            "value": "94c3e490-69e2-4144-83ff-68867e47889d"
                        },
                        {
                            "name": "VLAN_NAME_1",
                            "secure": false,
                            "value": "vlan.xxxxx"
                        },
                        {
                            "name": "VLAN_NAME_0",
                            "secure": false,
                            "value": "vlan.xxxxx"
                        },
                        {
                            "name": "NUM_CLUSTERS",
                            "secure": false,
                            "value": "2"
                        },
                        {
                            "name": "ENABLE_IP_ADDRESS_SELECTION",
                            "secure": false,
                            "value": "false"
                        },
                        {
                            "name": "VLAN_ID_1",
                            "secure": false,
                            "value": "91b11a7e-563f-480c-85bd-9cfe63a28e9d"
                        },
                        {
                            "name": "VLAN_TYPE_1",
                            "secure": false,
                            "value": "DHCP"
                        }
                    ],
                    "propertiesMap": {
                        "CLUSTER_ID_0": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
                        "CLUSTER_ID_1": "94c3e490-69e2-4144-83ff-68867e47889d",
                        "CLUSTER_NAME_0": "c1",
                        "CLUSTER_NAME_1": "c2",
                        "ENABLE_IP_ADDRESS_SELECTION": "false",
                        "NUM_CLUSTERS": "2",
                        "VLAN_ID_1": "91b11a7e-563f-480c-85bd-9cfe63a28e9d",
                        "VLAN_NAME_0": "vlan.xxxxx",
                        "VLAN_NAME_1": "vlan.xxxxx",
                        "VLAN_TYPE_1": "DHCP"
                    },
                    "published": false,
                    "status": "READY",
                    "systemProfile": false,
                    "topology": "cluster",
                    "type": "Network",
                    "version": "1.0"
                }
            ]
        }
profile:
  description: part of response when profile is updated
  returned: always
  type: dict
  sample: {
            "dateCreated": "2023-02-28 10:54:56",
            "dateModified": "2023-02-28 10:54:56",
            "dbVersion": "ALL",
            "description": "new_name",
            "engineType": "postgres_database",
            "id": "76c1d0eb-28b8-4f37-aa8a-e17dfa1c87a6",
            "latestVersion": "1.0",
            "latestVersionId": "801c60da-9273-45bc-ab00-81fd452a5fa2",
            "name": "new_name1",
            "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
            "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "status": "READY",
            "systemProfile": false,
            "topology": "cluster",
            "type": "Network",
            "versions": [
                {
                    "dateCreated": "2023-02-28 10:54:56",
                    "dateModified": "2023-02-28 10:54:56",
                    "dbVersion": "ALL",
                    "deprecated": false,
                    "description": "new_name",
                    "engineType": "postgres_database",
                    "id": "801c60da-9273-45bc-ab00-81fd452a5fa2",
                    "name": "new_name1 (1.0)",
                    "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "profileId": "76c1d0eb-28b8-4f37-aa8a-e17dfa1c87a6",
                    "properties": [
                        {
                            "name": "CLUSTER_NAME_0",
                            "secure": false,
                            "value": "c1"
                        },
                        {
                            "name": "CLUSTER_ID_0",
                            "secure": false,
                            "value": "0a3b964f-8616-40b9-a564-99cf35f4b8d8"
                        },
                        {
                            "name": "CLUSTER_NAME_1",
                            "secure": false,
                            "value": "c2"
                        },
                        {
                            "name": "CLUSTER_ID_1",
                            "secure": false,
                            "value": "94c3e490-69e2-4144-83ff-68867e47889d"
                        },
                        {
                            "name": "VLAN_NAME_1",
                            "secure": false,
                            "value": "vlan.xxxxx"
                        },
                        {
                            "name": "VLAN_NAME_0",
                            "secure": false,
                            "value": "vlan.xxxxx"
                        },
                        {
                            "name": "NUM_CLUSTERS",
                            "secure": false,
                            "value": "2"
                        },
                        {
                            "name": "ENABLE_IP_ADDRESS_SELECTION",
                            "secure": false,
                            "value": "false"
                        },
                        {
                            "name": "VLAN_ID_1",
                            "secure": false,
                            "value": "91b11a7e-563f-480c-85bd-9cfe63a28e9d"
                        },
                        {
                            "name": "VLAN_TYPE_1",
                            "secure": false,
                            "value": "DHCP"
                        }
                    ],
                    "propertiesMap": {
                        "CLUSTER_ID_0": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
                        "CLUSTER_ID_1": "94c3e490-69e2-4144-83ff-68867e47889d",
                        "CLUSTER_NAME_0": "c1",
                        "CLUSTER_NAME_1": "c2",
                        "ENABLE_IP_ADDRESS_SELECTION": "false",
                        "NUM_CLUSTERS": "2",
                        "VLAN_ID_1": "91b11a7e-563f-480c-85bd-9cfe63a28e9d",
                        "VLAN_NAME_0": "vlan.xxxxx",
                        "VLAN_NAME_1": "vlan.xxxxx",
                        "VLAN_TYPE_1": "DHCP"
                    },
                    "published": false,
                    "status": "READY",
                    "systemProfile": false,
                    "topology": "cluster",
                    "type": "Network",
                    "version": "1.0"
                }
            ]
        }
version:
  description: part of response denoting status of any version operation during update or delete
  returned: always
  type: dict
  sample: {
            "dateCreated": "2023-02-28 10:54:56",
            "dateModified": "2023-02-28 10:54:56",
            "dbVersion": "ALL",
            "deprecated": false,
            "description": "new_name",
            "engineType": "postgres_database",
            "id": "801c60da-9273-45bc-ab00-81fd452a5fa2",
            "name": "new_name1 (1.0)",
            "owner": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "profileId": "76c1d0eb-28b8-4f37-aa8a-e17dfa1c87a6",
            "properties": [
                {
                    "name": "CLUSTER_NAME_0",
                    "secure": false,
                    "value": "c1"
                },
                {
                    "name": "CLUSTER_ID_0",
                    "secure": false,
                    "value": "0a3b964f-8616-40b9-a564-99cf35f4b8d8"
                },
                {
                    "name": "CLUSTER_NAME_1",
                    "secure": false,
                    "value": "c2"
                },
                {
                    "name": "CLUSTER_ID_1",
                    "secure": false,
                    "value": "94c3e490-69e2-4144-83ff-68867e47889d"
                },
                {
                    "name": "VLAN_NAME_1",
                    "secure": false,
                    "value": "vlan.xxxxx"
                },
                {
                    "name": "VLAN_NAME_0",
                    "secure": false,
                    "value": "vlan.xxxxx"
                },
                {
                    "name": "NUM_CLUSTERS",
                    "secure": false,
                    "value": "2"
                },
                {
                    "name": "ENABLE_IP_ADDRESS_SELECTION",
                    "secure": false,
                    "value": "false"
                },
                {
                    "name": "VLAN_ID_1",
                    "secure": false,
                    "value": "91b11a7e-563f-480c-85bd-9cfe63a28e9d"
                },
                {
                    "name": "VLAN_TYPE_1",
                    "secure": false,
                    "value": "DHCP"
                }
            ],
            "propertiesMap": {
                "CLUSTER_ID_0": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
                "CLUSTER_ID_1": "94c3e490-69e2-4144-83ff-68867e47889d",
                "CLUSTER_NAME_0": "c1",
                "CLUSTER_NAME_1": "c2",
                "ENABLE_IP_ADDRESS_SELECTION": "false",
                "NUM_CLUSTERS": "2",
                "VLAN_ID_1": "91b11a7e-563f-480c-85bd-9cfe63a28e9d",
                "VLAN_NAME_0": "vlan.xxxxx",
                "VLAN_NAME_1": "vlan.xxxxx",
                "VLAN_TYPE_1": "DHCP"
            },
            "published": false,
            "status": "READY",
            "systemProfile": false,
            "topology": "cluster",
            "type": "Network",
            "version": "1.0"
        }
profile_uuid:
  description: profile uuid
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
version_uuid:
  description: uuid of profile version when any operation is done on version of profile
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""

import time  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.profiles.profile_types import get_profile_type_obj  # noqa: E402
from ..module_utils.ndb.profiles.profiles import Profile  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402

profile_types_with_version_support = ["software"]
profile_types_with_wait_support = ["software"]


# Notes:
# 1. publish/deprecate/unpublish can only be done using update.
# 2. keep version spec as part of profile related spec,
#    as module avoids version operations if profile related spec is not found.
def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    postgres_params = dict(
        max_connections=dict(type="int"),
        max_replication_slots=dict(type="int"),
        max_locks_per_transaction=dict(type="int"),
        effective_io_concurrency=dict(type="int"),
        timezone=dict(type="str"),
        max_prepared_transactions=dict(type="int"),
        max_wal_senders=dict(type="int"),
        min_wal_size=dict(type="int"),
        max_wal_size=dict(type="int"),
        wal_keep_segments=dict(type="int"),
        max_worker_processes=dict(type="int"),
        checkpoint_timeout=dict(type="int"),
        autovacuum=dict(type="str", choices=["on", "off"]),
        checkpoint_completion_target=dict(type="float"),
        autovacuum_freeze_max_age=dict(type="int"),
        autovacuum_vacuum_threshold=dict(type="int"),
        autovacuum_vacuum_scale_factor=dict(type="float"),
        autovacuum_work_mem=dict(type="int"),
        autovacuum_max_workers=dict(type="int"),
        autovacuum_vacuum_cost_delay=dict(type="int"),
        wal_buffers=dict(type="int"),
        synchronous_commit=dict(
            type="str", choices=["on", "off", "local", "remote_apply", "remote_write"]
        ),
        random_page_cost=dict(type="int"),
    )

    vlan = dict(
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        vlan_name=dict(type="str", required=True),
    )

    notes = dict(os=dict(type="str"), db_software=dict(type="str"))

    compute = dict(
        vcpus=dict(type="int"),
        cores_per_cpu=dict(type="int"),
        memory=dict(type="int"),
        publish=dict(type="bool", required=False),
    )

    network = dict(
        topology=dict(type="str", choices=["single", "cluster"]),
        vlans=dict(type="list", elements="dict", options=vlan),
        enable_ip_address_selection=dict(type="bool"),
        publish=dict(type="bool", required=False),
    )

    software = dict(
        topology=dict(type="str", choices=["single", "cluster"]),
        state=dict(type="str", choices=["present", "absent"], default="present"),
        version_uuid=dict(type="str"),
        name=dict(type="str"),
        desc=dict(type="str"),
        notes=dict(type="dict", options=notes),
        db_server_vm=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        publish=dict(type="bool", required=False),
        deprecate=dict(type="bool", required=False),
    )

    database_parameter = dict(
        postgres=dict(type="dict", options=postgres_params),
        publish=dict(type="bool", required=False),
    )

    module_args = dict(
        profile_uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        type=dict(
            type="str",
            choices=["software", "compute", "network", "database_parameter"],
            required=False,
        ),
        database_type=dict(type="str", choices=["postgres"]),
        compute=dict(type="dict", options=compute, required=False),
        software=dict(type="dict", options=software, required=False),
        network=dict(type="dict", options=network, required=False),
        database_parameter=dict(
            type="dict", options=database_parameter, required=False
        ),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
    )
    return module_args


def check_profile_idempotency(old_spec, new_spec):
    """
    This routine is used to check idempotency of a profile
    """

    if old_spec.get("name") != new_spec.get("name"):
        return False
    if old_spec.get("description") != new_spec.get("description"):
        return False

    # check cluster availability update for software profile
    if new_spec.get("updateClusterAvailability"):
        old_clusters = []
        for cluster in old_spec.get("clusterAvailability", []):
            if cluster["status"] == "ACTIVE":
                old_clusters.append(cluster["nxClusterId"])

        new_clusters = new_spec.get("availableClusterIds", [])

        if len(new_clusters) != len(old_clusters):
            return False

        # update if availibility of cluster is required
        for cluster in new_clusters:
            if cluster not in old_clusters:
                return False

    return True


def create_profile_version(module, result, profile_uuid, profile_obj):
    spec, err = profile_obj.get_spec(create=True, version=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating profile version create spec", **result)

    if module.check_mode:
        result["response"]["version"] = spec
        return

    resp = profile_obj.create_version(profile_uuid, data=spec)
    version_uuid = resp.get("entityId")
    result["version_uuid"] = version_uuid
    result["response"]["version"] = resp

    profile_type = profile_obj.get_type().lower()
    if (
        module.params.get("wait")
        and profile_type in profile_types_with_wait_support
        and resp.get("operationId")
    ):

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        result["response"]["version"] = profile_obj.get_profile_by_version(
            uuid=profile_uuid, version_uuid=version_uuid
        )

    result["changed"] = True


def update_profile_version(module, result, profile_uuid, profile_obj):
    profile_type = profile_obj.get_type().lower()
    config = module.params.get(profile_type)

    version_uuid = "latest"
    if config and config.get("version_uuid"):
        version_uuid = config.get("version_uuid")

    version = profile_obj.get_profile_by_version(
        uuid=profile_uuid, version_uuid=version_uuid
    )
    version_uuid = version.get("entityId") or version.get("id")
    result["version_uuid"] = version_uuid

    engine_type = version.get("engineType")

    default_spec = profile_obj.get_default_version_update_spec(override_spec=version)

    kwargs = {"version": True, "update": True, "engine_type": engine_type}
    spec, err = profile_obj.get_spec(old_spec=default_spec, **kwargs)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating profile version update spec", **result)

    if spec.get("propertiesMap"):
        spec.pop("propertiesMap")

    if module.check_mode:
        result["response"]["version"] = spec
        return

    resp = profile_obj.update_version(profile_uuid, version_uuid, spec)
    result["response"]["version"] = resp
    result["changed"] = True

    if (
        module.params.get("wait")
        and profile_type in profile_types_with_wait_support
        and resp.get("operationId")
    ):

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        result["response"]["version"] = profile_obj.get_profile_by_version(
            uuid=profile_uuid, version_uuid=version_uuid
        )


def delete_profile_version(module, result, profile_uuid, profile_obj):
    profile_type = profile_obj.get_type().lower()

    config = module.params.get(profile_type)

    version_uuid = config.get("version_uuid")
    if not version_uuid:
        module.fail_json(msg="uuid is required field for version delete", **result)

    resp = profile_obj.delete_version(
        profile_uuid=profile_uuid, version_uuid=version_uuid
    )
    result["response"]["version"] = resp
    result["changed"] = True


def version_operations(module, result, profile_uuid, profile_obj):
    profile_type = profile_obj.get_type().lower()
    result["profile_type"] = profile_type
    if profile_type not in profile_types_with_version_support:
        update_profile_version(module, result, profile_uuid, profile_obj)
    else:
        profile_config = module.params.get(profile_type)
        state = profile_config.get("state", "present")
        if state == "present":
            if profile_config.get("version_uuid"):
                update_profile_version(module, result, profile_uuid, profile_obj)
            else:
                create_profile_version(module, result, profile_uuid, profile_obj)
        else:
            delete_profile_version(module, result, profile_uuid, profile_obj)


def create_profile(module, result):
    profile_type = module.params.get("type")
    if not profile_type:
        return module.fail_json(
            "'type' is required field for creating profile of certain type"
        )

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)
    if err:
        result["error"] = err
        err_msg = "Failed getting object for profile type {0}".format(profile_type)
        module.fail_json(msg=err_msg, **result)

    spec, err = _profile.get_spec(create=True)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create profile spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = _profile.create(data=spec)
    result["response"] = resp
    uuid = resp.get("id")

    # incase there is process of replication triggered, operation info is recieved
    if profile_type == "software" and not uuid:
        uuid = resp.get("entityId")

    if not uuid:
        return module.fail_json(
            msg="Failed fetching uuid post profile creation", **result
        )

    result["profile_uuid"] = uuid

    # polling is only required for software profile
    if (
        module.params.get("wait")
        and profile_type in profile_types_with_wait_support
        and resp.get("operationId")
    ):

        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(3)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=10)

        resp = _profile.get_profiles(uuid=uuid)
        result["response"] = resp

    result["changed"] = True


def update_profile(module, result):
    uuid = module.params.get("profile_uuid")
    if not uuid:
        module.fail_json(msg="profile_uuid is required field for update", **result)

    result["profile_uuid"] = uuid

    _profile = Profile(module)

    profile = _profile.get_profiles(uuid=uuid)

    profile_type = module.params.get("type") or profile.get("type", "").lower()
    if not profile_type:
        result["response"] = profile
        return module.fail_json(msg="Failed getting profile type", **result)

    _profile, err = get_profile_type_obj(module, profile_type=profile_type)
    if err:
        result["error"] = err
        err_msg = "Failed generating object for profile type {0}".format(profile_type)
        module.fail_json(msg=err_msg, **result)

    # profile update operations
    default_update_spec = _profile.get_default_update_spec(override_spec=profile)

    profile_update_spec, err = _profile.get_spec(
        old_spec=default_update_spec, update=True
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed creating profile update spec", **result)

    result["response"] = {}

    if module.check_mode:
        result["response"]["profile"] = profile_update_spec

    if not module.check_mode and not check_profile_idempotency(
        profile, profile_update_spec
    ):
        resp = _profile.update(data=profile_update_spec, uuid=uuid)
        result["response"]["profile"] = resp
        result["changed"] = True
        if (
            module.params.get("wait")
            and profile_type in profile_types_with_wait_support
            and resp.get("operationId")
        ):

            ops_uuid = resp["operationId"]
            operations = Operation(module)
            time.sleep(3)  # to get operation ID functional
            operations.wait_for_completion(ops_uuid, delay=10)

            resp = _profile.get_profiles(uuid=uuid)
            result["response"]["profile"] = resp

    # perform versions related crud as per support
    # version spec needs to be part of spec of profile type
    if module.params.get(profile_type):
        version_operations(module, result, profile_uuid=uuid, profile_obj=_profile)

    if not module.check_mode:
        resp = _profile.get_profiles(uuid=uuid)
        result["response"]["profile"] = resp


def delete_profile(module, result):
    profiles = Profile(module)

    uuid = module.params.get("profile_uuid")
    if not uuid:
        return module.fail_json(msg="'profile_uuid' is a required for deleting profile")

    if module.check_mode:
        result["uuid"] = uuid
        result["response"] = "Profile with uuid:{0} will be deleted.".format(uuid)
        return

    resp = profiles.delete(uuid)

    result["uuid"] = uuid
    result["response"] = resp
    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        required_if=[
            ("state", "present", ("name", "profile_uuid"), True),
            ("state", "absent", ("profile_uuid",)),
        ],
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "profile_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("profile_uuid"):
            update_profile(module, result)
        else:
            create_profile(module, result)
    else:
        delete_profile(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
