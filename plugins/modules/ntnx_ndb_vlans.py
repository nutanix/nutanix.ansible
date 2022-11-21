#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_vlans
short_description: Module for create, update and delete of single instance vlan. Currently, postgres type vlan is officially supported.
version_added: 1.8.0-beta.1
description: Module for create, update and delete of single instance vlan in Nutanix vlan Service
options:
  db_uuid:
    description:
      - uuid for update or delete of vlan instance
    type: str
  name:
    description:
      - name of vlan instance
      - update allowed
    type: str
  desc:
    description:
      - description of vlan
      - update allowed
    type: str
  db_params_profile:
    description:
      - DB parameters profile details
    type: dict
    suboptions:
      name:
        type: str
        description:
          - name of profile
          - mutually_exclusive with C(uuid)
      uuid:
        type: str
        description:
          - uuid of profile
          - mutually_exclusive with C(name)
  db_vm:
    description:
      - DB server VM details
    type: dict
    suboptions:
      create_new_server:
        description:
          - details for creating new db server vms
          - mutually_exclusive with C(use_registered_server)
        type: dict
        suboptions:
          name:
            type: str
            description: name of vm
            required: true
          pub_ssh_key:
            type: str
            description: public ssh key for access to vm
            required: true
          password:
            type: str
            description: set vm era driver user password
            required: true
          cluster:
            description:
              - era cluster details
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description:
                  - name of cluster
                  - mutually_exclusive with C(uuid)
              uuid:
                type: str
                description:
                  - uuid of cluster
                  - mutually_exclusive with C(name)
          software_profile:
            description:
              - software profile details
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description:
                  - name of profile
                  - mutually_exclusive with C(uuid)
              uuid:
                type: str
                description:
                  - uuid of profile
                  - mutually_exclusive with C(name)
              version_id:
                type: str
                description:
                  - version id of software profile
                  - by default latest version will be used
          network_profile:
            description:
              - network profile details
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description:
                  - name of profile
                  - mutually_exclusive with C(uuid)
              uuid:
                type: str
                description:
                  - uuid of profile
                  - mutually_exclusive with C(name)
          compute_profile:
            description:
              - compute profile details
            type: dict
            required: true
            suboptions:
              name:
                type: str
                description:
                  - name of profile
                  - mutually_exclusive with C(uuid)
              uuid:
                type: str
                description:
                  - uuid of profile
                  - mutually_exclusive with C(name)
      use_registered_server:
        description:
          - registered server details
          - mutually_exclusive with C(create_new_server)
        type: dict
        suboptions:
          name:
            type: str
            description:
              - name of registered vm
              - mutually_exclusive with C(uuid)
          uuid:
            type: str
            description:
              - uuid of registered vm
              - mutually_exclusive with C(name)
  time_machine:
    description:
      - time machine details
    type: dict
    suboptions:
      name:
        type: str
        description: name of time machine
        required: True
      desc:
        type: str
        description: description of time machine
      sla:
        type: dict
        description: sla details
        required: True
        suboptions:
          name:
            type: str
            description:
              - name of sla
              - mutually_exclusive with C(uuid)
          uuid:
            type: str
            description:
              - uuid of sla
              - mutually_exclusive with C(name)
      schedule:
          type: dict
          description: schedule for taking snapshot
          required: True
          suboptions:
            daily:
                type: str
                description: daily snapshot time in HH:MM:SS format
            weekly:
                type: str
                description: weekly snapshot day. For Example, "WEDNESDAY"
            monthly:
                type: int
                description: monthly snapshot day in a month
            quaterly:
                type: str
                description:
                  - quaterly snapshot month
                  - day of month is set based on C(monthly)
                  - C(monthly) is required for setting C(quaterly) else it is ignored
                  - For Example, "JANUARY"
            yearly:
                type: str
                description:
                  - yearly snapshot month
                  - day of month is set based on C(monthly)
                  - C(monthly) is required for setting C(yearly) else it is ignored
                  - For Example, "JANUARY"
            log_catchup:
                type: int
                description: log catchup intervals in minutes
                choices:
                  - 15
                  - 30
                  - 60
                  - 90
                  - 120
            snapshots_per_day:
                type: int
                description: num of snapshots per day
                default: 1
      auto_tune_log_drive:
        type: bool
        default: true
        description: enable/disable auto tuning of log drive
  postgres:
    type: dict
    description: action arguments for postgres type vlan
    suboptions:
      listener_port:
          type: str
          description: listener port for db
          required: true
      db_name:
          type: str
          description: initial vlan name
          required: true
      db_password:
          type: str
          description: postgres vlan password
          required: true
      auto_tune_staging_drive:
          type: bool
          default: true
          description: enable/disable autotuning of staging drive
      allocate_pg_hugepage:
          type: bool
          default: false
          description: enable/disable allocating HugePage in postgres
      auth_method:
          type: str
          default: md5
          description: auth method
      cluster_vlan:
          type: bool
          default: false
          description: if clustered vlan
      db_size:
          type: int
          description: vlan instance size
          required: true
      pre_create_script:
          type: str
          description: commands to run before vlan instance creation
          required: false
      post_create_script:
          type: str
          description: commands to run after vlan instance creation
          required: false
  tags:
    type: dict
    description:
      - dict of tag name as key and tag value as value
      - update allowed
  auto_tune_staging_drive:
    type: bool
    description:
      - enable/disable auto tuning of stage drive
      - enabled by default
  soft_delete:
    type: bool
    description:
      - only unregister from era in delete process
      - if not provided, vlan instance from db server VM will be deleted
  delete_time_machine:
    type: bool
    description: delete time machine as well in delete process
  timeout:
    description:
        - timeout for polling vlan operations in seconds
        - default is 2100 secs i.e. 35 minutes
    type: int
    required: false
    default: 2100
extends_documentation_fragment:
  - nutanix.ncp.ntnx_ndb_base_module
  - nutanix.ncp.ntnx_operations
author:
  - Prem Karat (@premkarat)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Create postgres vlan instance using with new vm
  ntnx_ndb_vlans:
    name: "test"

    db_params_profile:
      name: "TEST_PROFILE"

    db_vm:
      create_new_server:
        name: "test-vm"
        password: "test-vm-password"
        cluster:
          name: "EraCluster"
        software_profile:
          name: "TEST_SOFTWARE_PROFILE"
        network_profile:
          name: "TEST_NETWORK_PROFILE"
        compute_profile:
          name: "TEST_COMPUTE_PROFILE"
        pub_ssh_key: "<public-ssh-key>"

    postgres:
      listener_port: "5432"
      db_name: ansible_test
      db_password: "postgres-test-password"
      db_size: 200

    time_machine:
      name: POSTGRES_SERVER_PRAD_TM_1
      sla:
        name: "TEST_SLA"
      schedule:
        daily: "11:10:02"
        weekly: WEDNESDAY
        monthly: 4
        quaterly: JANUARY
        yearly: FEBRUARY
        log_catchup: 30
        snapshots_per_day: 2
  register: db
"""

RETURN = r"""
response:
  description: vlan creation response after provisioning
  returned: always
  type: dict
  sample: {
            "accessLevel": null,
            "category": "DB_GROUP_IMPLICIT",
            "clone": false,
            "clustered": false,
            "vlanClusterType": null,
            "vlanGroupStateInfo": null,
            "vlanName": "POSTGRES_vlan_ANSIBLE",
            "vlanNodes": [
                {
                    "accessLevel": null,
                    "vlanId": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "vlanStatus": "READY",
                    "dateCreated": "2022-10-19 18:49:25",
                    "dateModified": "2022-10-19 18:51:33",
                    "dbserver": null,
                    "dbserverId": "0bee18d7-1f7c-4a7b-8d52-cd7f22f3121a",
                    "description": "postgres_vlan POSTGRES_vlan_ANSIBLE on host 10.51.144.213",
                    "id": "7228a75f-86d9-4a5b-aa1a-cc52c1fcfce3",
                    "info": {
                        "info": {},
                        "secureInfo": null
                    },
                    "metadata": null,
                    "name": "POSTGRES_vlan_ANSIBLE",
                    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "primary": false,
                    "properties": [],
                    "protectionDomain": null,
                    "protectionDomainId": "d67b312c-6f3a-4322-a9f2-15ec0bdc9dc5",
                    "softwareInstallationId": "b48c4b34-a6a1-4040-b4df-0bd4ab9c9e2c",
                    "status": "READY",
                    "tags": []
                }
            ],
            "vlanStatus": "UNKNOWN",
            "vlans": null,
            "dateCreated": "2022-10-19 18:26:55",
            "dateModified": "2022-10-19 18:51:26",
            "dbserverLogicalClusterId": null,
            "dbserverlogicalCluster": null,
            "description": null,
            "eraCreated": true,
            "groupInfo": null,
            "id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
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
            "linkedvlans": [
                {
                    "vlanName": "prad",
                    "vlanStatus": "READY",
                    "dateCreated": "2022-10-19 18:48:37",
                    "dateModified": "2022-10-19 18:48:37",
                    "description": null,
                    "id": "6d4da687-a425-43f1-a9df-fa28a6b0af80",
                    "info": {
                        "info": {
                            "created_by": "user"
                        },
                        "secureInfo": null
                    },
                    "metadata": null,
                    "metric": null,
                    "name": "prad",
                    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "parentvlanId": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "parentLinkedvlanId": null,
                    "snapshotId": null,
                    "status": "READY",
                    "timeZone": null
                },
                {
                    "vlanName": "postgres",
                    "vlanStatus": "READY",
                    "dateCreated": "2022-10-19 18:48:37",
                    "dateModified": "2022-10-19 18:48:37",
                    "description": null,
                    "id": "67314b51-326f-4fc8-a345-668933a18cbd",
                    "info": {
                        "info": {
                            "created_by": "system"
                        },
                        "secureInfo": null
                    },
                    "metadata": null,
                    "metric": null,
                    "name": "postgres",
                    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "parentvlanId": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "parentLinkedvlanId": null,
                    "snapshotId": null,
                    "status": "READY",
                    "timeZone": null
                },
                {
                    "vlanName": "template0",
                    "vlanStatus": "READY",
                    "dateCreated": "2022-10-19 18:48:37",
                    "dateModified": "2022-10-19 18:48:37",
                    "description": null,
                    "id": "ba4bf273-b5ab-4743-a222-dffa178220f2",
                    "info": {
                        "info": {
                            "created_by": "system"
                        },
                        "secureInfo": null
                    },
                    "metadata": null,
                    "metric": null,
                    "name": "template0",
                    "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
                    "parentvlanId": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "parentLinkedvlanId": null,
                    "snapshotId": null,
                    "status": "READY",
                    "timeZone": null
                },
                {
                    "vlanName": "template1",
                    "vlanStatus": "READY",
                    "dateCreated": "2022-10-19 18:48:37",
                    "dateModified": "2022-10-19 18:48:37",
                    "description": null,
                    "id": "704d8464-d8aa-47ff-8f79-347cfae90abd",
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
                    "parentvlanId": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "parentLinkedvlanId": null,
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
                "originalvlanName": null,
                "pitrBased": false,
                "provisionOperationId": "d9b1924f-a768-4cd8-886b-7a69e61f5b89",
                "refreshBlockerInfo": null,
                "registeredDbservers": null,
                "sanitised": false,
                "secureInfo": null,
                "sourceSnapshotId": null,
                "stateBeforeRefresh": null,
                "stateBeforeRestore": null,
                "stateBeforeScaling": null,
                "tmActivateOperationId": "40d6b3a3-4f57-4c17-9ba2-9279d2f247c2"
            },
            "metric": null,
            "name": "POSTGRES_vlan_ANSIBLE",
            "ownerId": "eac70dbf-22fb-462b-9498-949796ca1f73",
            "parentvlanId": null,
            "parentSourcevlanId": null,
            "parentTimeMachineId": null,
            "placeholder": false,
            "properties": [
                {
                    "description": null,
                    "name": "db_parameter_profile_id",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "a80ac1fb-8787-4442-8f38-eeb2417a8cbb"
                },
                {
                    "description": null,
                    "name": "auth",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "md5"
                },
                {
                    "description": null,
                    "name": "AUTO_EXTEND_DB_STAGE",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "true"
                },
                {
                    "description": null,
                    "name": "provisioning_spec",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": ""
                },
                {
                    "description": null,
                    "name": "version",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "10.4"
                },
                {
                    "description": null,
                    "name": "vm_ip",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "xx.xx.xx.xx"
                },
                {
                    "description": null,
                    "name": "postgres_software_home",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "%2Fusr%2Fpgsql-10.4"
                },
                {
                    "description": null,
                    "name": "listener_port",
                    "ref_id": "e9374379-de51-4cc8-8d12-b1b6eb64d129",
                    "secure": false,
                    "value": "5432"
                }
            ],
            "status": "READY",
            "tags": [],
            "timeMachine": null,
            "timeMachineId": "be524e70-60ad-4a8c-a0ee-8d72f954d7e6",
            "timeZone": "UTC",
            "type": "postgres_vlan"
        }
db_uuid:
  description: created vlan UUID
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""
import time  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.vlans import VLAN  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    ip_pool_spec = dict(start_ip=dict(type="str"), end_ip=dict(type="str"))

    module_args = dict(

        name=dict(type="str"),
        vlan_type=dict(type="str", choices=["DHCP", "Static"]),
        vlan_uuid=dict(type="str"),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        ip_pools=dict(
            type="list",
            elements="dict",
            options=ip_pool_spec,
            required_together=[("start_ip", "end_ip")],
        ),
        gateway=dict(type="str"),
        subnet_mask=dict(type="str"),
        primary_dns=dict(type="str"),
        secondary_dns=dict(type="str"),
        dns_domain=dict(type="str"),
    )
    return module_args


def create_vlan(module, result):
    vlan = VLAN(module)

    name = module.params["name"]
    uuid, err = vlan.get_uuid(name)
    if uuid:
        module.fail_json(
            msg="vlan instance with given name already exists", **result
        )

    spec, err = vlan.get_spec()
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create vlan instance spec", **result
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = vlan.create(data=spec)
    result["response"] = resp
    vlan_uuid = resp["id"]
    result["vlan_uuid"] = vlan_uuid
    #
    # if module.params.get("wait"):
    #     ops_uuid = resp["operationId"]
    #     operations = Operation(module)
    #     time.sleep(5)  # to get operation ID functional
    #     operations.wait_for_completion(ops_uuid)
    #     resp = vlan.read(vlan_uuid)
    #     result["response"] = resp

    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if (
        old_spec["name"] != update_spec["name"]
        or old_spec["description"] != update_spec["description"]
    ):
        return False

    if len(old_spec["tags"]) != len(update_spec["tags"]):
        return False

    old_tag_values = {}
    new_tag_values = {}
    for i in range(len(old_spec["tags"])):
        old_tag_values[old_spec["tags"][i]["tagName"]] = old_spec["tags"][i]["value"]
        new_tag_values[update_spec["tags"][i]["tagName"]] = update_spec["tags"][i][
            "value"
        ]

    if old_tag_values != new_tag_values:
        return False

    return True


def update_vlan(module, result):
    _vlan = vlan(module)

    uuid = module.params.get("db_uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for update", **result)

    resp = _vlan.read(uuid)
    old_spec = _vlan.get_default_update_spec(override_spec=resp)

    update_spec, err = _vlan.get_spec(old_spec=old_spec)

    # due to field name changes
    if update_spec.get("vlanDescription"):
        update_spec["description"] = update_spec.pop("vlanDescription")

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update vlan instance spec", **result
        )

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = _vlan.update(data=update_spec, uuid=uuid)
    result["response"] = resp
    result["db_uuid"] = uuid
    result["changed"] = True


def delete_vlan(module, result):
    vlan = VLAN(module)

    uuid = module.params.get("vlan_uuid")
    if not uuid:
        module.fail_json(msg="uuid is required field for delete", **result)

    resp = vlan.delete(uuid)

    # if module.params.get("wait"):
    #     ops_uuid = resp["operationId"]
    #     time.sleep(5)  # to get operation ID functional
    #     operations = Operation(module)
    #     resp = operations.wait_for_completion(ops_uuid)

    result["response"] = resp
    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("db_uuid", "db_params_profile"),
        ("db_uuid", "db_vm"),
        ("db_uuid", "postgres"),
        ("db_uuid", "time_machine"),
        ("db_uuid", "auto_tune_staging_drive"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        mutually_exclusive=mutually_exclusive_list,
        required_if=[
            ("state", "present", ("name", "db_uuid"), True),
            ("state", "absent", ("vlan_uuid",)),
        ],
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}
    if module.params["state"] == "present":
        if module.params.get("db_uuid"):
            update_vlan(module, result)
        else:
            create_vlan(module, result)
    else:
        delete_vlan(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
