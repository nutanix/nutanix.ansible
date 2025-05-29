#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_db_server_vms
short_description: module for create, delete and update of database server vms
version_added: 1.8.0
description:
    - module for create, delete and update of database server vms
options:
    state:
        description:
            - when C(state)=present and uuid given, it will update db server vm
            - when C(state)=present and uuid not given, it will create new db server vm
            - when C(state)=absent, by default it will perform unregistration process unless supported arguments are given
    name:
        description:
            - name of database server vm
            - update allowed
        type: str
    uuid:
        description:
            - uuid of database server vm for updating or deleting vm
            - will be used to update if C(state) is C(present) and to delete if C(state) is C(absent)
        type: str
    desc:
        description:
            - description of vm
            - allowed for update
        type: str
    reset_name_in_ntnx_cluster:
        description:
            - set this to reset name of vm to name in ndb in cluster as well
        type: bool
        default: false
    reset_desc_in_ntnx_cluster:
        description:
            - set this to reset description of vm to name in ndb in cluster as well
        type: bool
        default: false
    cluster:
        description:
            - ndb cluster where the vm will be hosted
            - required for create
        type: dict
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
    network_profile:
        description:
            - network profile details
            - required for create
        type: dict
        suboptions:
            name:
                description:
                    - name of profile
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of profile
                    - mutually exclusive with C(name)
                type: str
    compute_profile:
        description:
            - required for create
            - compute profile details
        type: dict
        suboptions:
            name:
                description:
                    - name of profile
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of profile
                    - mutually exclusive with C(name)
                type: str
    software_profile:
        description:
            - use software profile as source for creating vm
            - required for create
            - either name or uuid is mandatory
        type: dict
        suboptions:
            name:
                description:
                    - name of profile
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of profile
                    - mutually exclusive with C(name)
                type: str
            version_uuid:
                description:
                    - version UUID for software profile
                    - if not given then latest version will be used
                type: str
    time_machine:
        description:
            - use time machine as source for creating vm
            - either name or uuid is mandatory
        type: dict
        suboptions:
            name:
                description:
                    - name of time machine
                    - mutually exclusive with C(uuid)
                type: str
            uuid:
                description:
                    - uuid of time machine
                    - mutually exclusive with C(name)
                type: str
            snapshot_uuid:
                description:
                    - source snapshot uuid
                    - required for create
                type: str
    password:
        description:
            - password of vm
        type: str
    pub_ssh_key:
        description:
            - give access using user's public ssh key
        type: str
    time_zone:
        description:
            - timezone of vm
        type: str
        default: "Asia/Calcutta"
    database_type:
        description:
            - database engine type
        type: str
        choices: ["postgres_database"]
    automated_patching:
        description:
            - configure automated patching using maintenance windows
            - to be only used while creation
        type: dict
        suboptions:
            maintenance_window:
                description:
                    - maintenance window details
                type: dict
                suboptions:
                    name:
                        description:
                            - name of maintenance window
                            - mutually exclusive with C(uuid)
                        type: str
                    uuid:
                        description:
                            - uuid of maintenance window
                            - mutually exclusive with C(name)
                        type: str
            tasks:
                description:
                    - list of maintenance pre-post tasks
                type: list
                elements: dict
                suboptions:
                    type:
                        description:
                            - type of patching
                        type: str
                        choices: ["OS_PATCHING", "DB_PATCHING"]
                    pre_task_cmd:
                        description:
                            - full os command which needs to run before patching task in db server vm
                        type: str
                    post_task_cmd:
                        description:
                            - full os command which needs to run after patching task in db server vm
                        type: str
    tags:
        description:
            - dict of tag name as key and tag value as value
            - update allowed
            - during update, given input will override existing tags
        type: dict
    update_credentials:
        description:
            - update credentials of vm in ndb
            - this update should be done post vm credentials update in source cluster
        type: list
        elements: dict
        suboptions:
            username:
                description:
                    - username
                type: str
                required: true
            password:
                description:
                    - password
                type: str
                required: true
    delete_from_cluster:
        description:
            - set this during c(state) = absent to delete vm from source cluster
        type: bool
        default: False
    delete_vgs:
        description:
            - set this during c(state) = absent to delete volume groups from source cluster
        type: bool
        default: False
    delete_vm_snapshots:
        description:
            - set this during c(state) = absent to delete vm's snapshot from source cluster
        type: bool
        default: False
    soft_remove:
        description:
            - set this during c(state) = absent to perform soft remove of database server vm
        type: bool
        default: False
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
"""
RETURN = r"""
response:
  description: database server intent response
  returned: always
  type: dict
  sample: {
    "id": "7615993c-8455-4bc6-b562-8075a840991e",
    "name": "test-setup-dnd",
    "description": "DBServer for test-setup-dnd",
    "dateCreated": "2023-02-24 07:42:55",
    "dateModified": "2023-02-28 09:44:34",
    "properties": [
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "software_profile_version_id",
            "value": "ab966132-7d7d-4418-b89d-dc814c2ef1b3",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "current_op_id",
            "value": "32536509-0ca0-4475-a347-016c23855bfd",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "isEraCreated",
            "value": "true",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "software_home",
            "value": "/usr/pgsql-10.4",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "vm_ip_address_list",
            "value": "xx.xx.xx.xx",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "working_dir",
            "value": "/tmp",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "os_type",
            "value": "linux",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "application_type",
            "value": "postgres_database",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "application_version",
            "value": "10.4",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "os_info",
            "value": "Linux test-setup-dnd 5.10.0-1.el7.elrepo.x86_64 #1 SMP Sun Dec 13 18:34:48 EST 2020 x86_64 x86_64 x86_64 GNU/Linux\n",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "node_type",
            "value": "database",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "era_base",
            "value": "/opt/era_base",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "era_user",
            "value": "era",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "compute_profile_id",
            "value": "19b1241e-d4e0-411e-abfc-6639ba713d13",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "network_profile_id",
            "value": "6cf4fe44-5030-41a5-a0cd-4e62a55cd85a",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "software_profile_id",
            "value": "96b3c1a2-4427-41c1-87eb-a942c52247a2",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "vm_cpu_count",
            "value": "1",
            "secure": false,
            "description": null
        },
        {
            "ref_id": "7615993c-8455-4bc6-b562-8075a840991e",
            "name": "vm_core_count",
            "value": "1",
            "secure": false,
            "description": null
        }
    ],
    "tags": [],
    "eraCreated": true,
    "dbserverClusterId": null,
    "vmClusterName": "test-setup-dnd",
    "vmClusterUuid": "1626600d-aa20-438e-94e8-3d3f0a5c948f",
    "ipAddresses": [
        "10.44.78.125"
    ],
    "fqdns": null,
    "macAddresses": [
        ""
    ],
    "type": "DBSERVER",
    "status": "UP",
    "clientId": "147e09d5-53fd-4da8-8a46-6c82d7ab5c6e",
    "nxClusterId": "0a3b964f-8616-40b9-a564-99cf35f4b8d8",
    "eraDriveId": "44dcffdf-235b-465f-b07f-ad253c26d93b",
    "eraVersion": "2.5.1",
    "vmTimeZone": "UTC",
    "vmInfo": {
        "secureInfo": null,
        "info": null,
        "deregisterInfo": null,
        "osType": null,
        "osVersion": null,
        "distribution": null,
        "networkInfo": [
            {
                "vlanName": "vlan.sds",
                "vlanUuid": "61213511-6383-4a38-9ac8-4a552c0e5865",
                "vlanType": "Static",
            }
        ]
    },
    "info": null,
    "metric": null,
    "clustered": false,
    "requestedVersion": null,
    "is_server_driven": false,
    "associated_time_machine_id": null,
    "time_machine_info": null,
    "eraDrive": null,
    "databases": null,
    "clones": null,
    "accessKey": null,
    "softwareInstallations": null,
    "protectionDomainId": "ef185e83-fc47-4111-bff5-3e5f003bb610",
    "protectionDomain": null,
    "queryCount": 0,
    "databaseType": "postgres_database",
    "dbserverInValidEaState": true,
    "workingDirectory": "/tmp",
    "validDiagnosticBundleState": true,
    "windowsDBServer": false,
    "associatedTimeMachineIds": null,
    "accessKeyId": "ed3c5a82-c5c1-4728-85e1-d38cba63c107"
}
uuid:
  description: created db server UUID
  returned: always
  type: str
  sample: "be524e70-60ad-4a8c-a0ee-8d72f954d7e6"
"""

import time  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.v3.ndb.db_server_vm import DBServerVM  # noqa: E402
from ..module_utils.v3.ndb.maintenance_window import (  # noqa: E402
    AutomatedPatchingSpec,
    MaintenanceWindow,
)
from ..module_utils.v3.ndb.operations import Operation  # noqa: E402
from ..module_utils.v3.ndb.tags import Tag  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    automated_patching = deepcopy(
        AutomatedPatchingSpec.automated_patching_argument_spec
    )

    software_profile = dict(
        name=dict(type="str"), uuid=dict(type="str"), version_uuid=dict(type="str")
    )
    time_machine = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        snapshot_uuid=dict(type="str", required=False),
    )
    credential = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )
    module_args = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        reset_name_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        reset_desc_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        network_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        compute_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        software_profile=dict(
            type="dict",
            options=software_profile,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        time_machine=dict(
            type="dict",
            options=time_machine,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        password=dict(type="str", required=False, no_log=True),
        pub_ssh_key=dict(type="str", required=False, no_log=True),
        time_zone=dict(type="str", default="Asia/Calcutta", required=False),
        database_type=dict(type="str", choices=["postgres_database"], required=False),
        tags=dict(type="dict", required=False),
        update_credentials=dict(
            type="list", elements="dict", options=credential, required=False
        ),
        automated_patching=dict(
            type="dict", options=automated_patching, required=False
        ),
        delete_from_cluster=dict(type="bool", default=False, required=False),
        delete_vgs=dict(type="bool", default=False, required=False),
        delete_vm_snapshots=dict(type="bool", default=False, required=False),
        soft_remove=dict(type="bool", default=False, required=False),
    )
    return module_args


def get_provision_spec(module, result):
    db_servers = DBServerVM(module)

    default_spec = db_servers.get_default_spec_for_provision()
    spec, err = db_servers.get_spec(old_spec=default_spec, provision_new_server=True)

    if err:
        result["error"] = err
        module.fail_json("Failed getting DB server vm create spec", **result)

    # populate tags related spec
    if module.params.get("tags"):
        tags = Tag(module)
        spec, err = tags.get_spec(
            spec, associate_to_entity=True, type="DATABASE_SERVER"
        )
        if err:
            result["error"] = err
            err_msg = "Failed getting spec for tags for new db server vm"
            module.fail_json(msg=err_msg, **result)

    # configure automated patching
    if module.params.get("automated_patching"):
        mw = MaintenanceWindow(module)
        mw_spec, err = mw.get_spec(configure_automated_patching=True)
        if err:
            result["error"] = err
            err_msg = "Failed getting spec for automated patching for new db server vm"
            module.fail_json(msg=err_msg, **result)
        spec["maintenanceTasks"] = mw_spec

    return spec


def create_db_server(module, result):
    db_servers = DBServerVM(module)

    spec = get_provision_spec(module, result)
    if module.check_mode:
        result["response"] = spec
        return

    resp = db_servers.provision(data=spec)
    result["response"] = resp
    result["uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_servers.read(db_uuid)
        db_servers.format_response(resp)
        result["response"] = resp

    result["changed"] = True


def check_idempotency(old_spec, new_spec):

    # check for arguments
    args = ["name", "description"]
    for arg in args:
        if old_spec[arg] != new_spec[arg]:
            return False

    # check for resets
    args = ["resetDescriptionInNxCluster", "resetNameInNxCluster", "resetCredential"]
    for arg in args:
        if new_spec.get(arg, False):
            return False

    # check for new tags
    if len(old_spec["tags"]) != len(new_spec["tags"]):
        return False

    old_tag_values = {}
    new_tag_values = {}
    for i in range(len(old_spec["tags"])):
        old_tag_values[old_spec["tags"][i]["tagName"]] = old_spec["tags"][i]["value"]
        new_tag_values[new_spec["tags"][i]["tagName"]] = new_spec["tags"][i]["value"]

    if old_tag_values != new_tag_values:
        return False

    return True


def update_db_server(module, result):
    db_servers = DBServerVM(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json("'uuid' is required for updating db server vm")

    db_server = db_servers.read(uuid=uuid)
    update_spec = db_servers.get_default_spec_for_update(override=db_server)
    update_spec, err = db_servers.get_spec(old_spec=update_spec, update=True)
    if err:
        result["error"] = err
        module.fail_json("Failed getting db server vm update spec", **result)

    # populate tags related spec
    if module.params.get("tags"):
        tags = Tag(module)
        update_spec, err = tags.get_spec(
            update_spec, associate_to_entity=True, type="DATABASE_SERVER"
        )
        if err:
            result["error"] = err
            err_msg = "Failed getting spec for tags for db server vm update"
            module.fail_json(msg=err_msg, **result)
        update_spec["resetTags"] = True

    if module.check_mode:
        result["response"] = update_spec
        return

    if check_idempotency(old_spec=db_server, new_spec=update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = db_servers.update(data=update_spec, uuid=uuid)
    db_servers.format_response(resp)
    result["response"] = resp
    result["uuid"] = uuid
    result["changed"] = True


def delete_db_server(module, result):
    db_servers = DBServerVM(module)

    uuid = module.params.get("uuid")
    if not uuid:
        module.fail_json("'uuid' is required for deleting db server vm")

    spec = db_servers.get_default_delete_spec()
    spec, err = db_servers.get_spec(old_spec=spec, delete=True)
    if err:
        result["error"] = err
        module.fail_json("Failed getting db server delete update spec", **result)

    spec["remove"] = not spec["delete"]
    result["uuid"] = uuid

    if module.check_mode:
        result["response"] = spec

        result["msg"] = "Db server with uuid:{0} will be deleted.".format(uuid)
        return

    resp = db_servers.delete(data=spec, uuid=uuid)
    result["response"] = resp

    if module.params.get("wait") and resp.get("operationId"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        resp = operations.wait_for_completion(ops_uuid, delay=5)
        result["response"] = resp

    result["changed"] = True


def run_module():
    mutually_exclusive_list = [
        ("uuid", "database_type"),
        ("uuid", "time_zone"),
        ("uuid", "pub_ssh_key"),
        ("uuid", "password"),
        ("uuid", "time_machine"),
        ("uuid", "cluster"),
        ("uuid", "network_profile"),
        ("uuid", "software_profile"),
        ("uuid", "compute_profile"),
    ]
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        mutually_exclusive=mutually_exclusive_list,
        required_if=[
            ("state", "present", ("name", "uuid"), True),
            ("state", "absent", ("uuid",)),
        ],
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("uuid"):
            update_db_server(module, result)
        else:
            create_db_server(module, result)
    else:
        delete_db_server(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
