#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ndb_register_db_server_vm
short_description: module for registration of database server vm
version_added: 1.8.0
description:  module for registration of database server vm
options:
    ip:
        description:
            - IP of vm
        type: str
        required: true
    desc:
        description:
            - set description of vm in ndb
        type: str
    reset_desc_in_ntnx_cluster:
        description:
            - reset description of vm in cluster as per C(desc) in ndb
        type: bool
        default: false
    cluster:
        description:
            - cluster where db server vm is hosted
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
    postgres:
        description:
            - potgres related configuration
        type: dict
        suboptions:
            listener_port:
                description:
                    - listener port of database
                type: str
                default: "5432"
            software_path:
                description:
                    - path where desired postgres instance is located. For ex. "/usr/pgsql-10.4"
                type: str
                required: true
    username:
        description:
            - username to access vm
        type: str
        required: true
    password:
        description:
            - password for accessing vm
            - mutually_exclusive with C(private_ssh_key)
        type: str
    private_ssh_key:
        description:
            - private key for accessing vm
            - mutually_exclusive with C(password)
        type: str
    working_directory:
        description:
            - directory path to be created and used by ndb for its scripts
        type: str
        default: "/tmp"
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

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: register db server vm
  ntnx_ndb_register_db_server_vm:
    ip: "{{vm_ip}}"
    desc: "register-vm-desc"
    cluster:
      name: "{{cluster.cluster1.name}}"
    postgres:
      listener_port: 5432
      software_path: "{{postgres.software_home}}"
    username: "{{vm_username}}"
    password: "{{vm_password}}"
  register: result
  
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

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.db_server_vm import DBServerVM  # noqa: E402
from ..module_utils.ndb.maintenance_window import (  # noqa: E402
    AutomatedPatchingSpec,
    MaintenanceWindow,
)
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    automated_patching = deepcopy(
        AutomatedPatchingSpec.automated_patching_argument_spec
    )

    postgres = dict(
        listener_port=dict(type="str", default="5432", required=False),
        software_path=dict(type="str", required=True),
    )
    module_args = dict(
        ip=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        reset_desc_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        postgres=dict(type="dict", options=postgres, required=False),
        username=dict(type="str", required=True),
        password=dict(type="str", required=False, no_log=True),
        private_ssh_key=dict(type="str", required=False, no_log=True),
        automated_patching=dict(
            type="dict", options=automated_patching, required=False
        ),
        working_directory=dict(type="str", default="/tmp", required=False),
    )
    return module_args


def get_register_spec(module, result):
    db_server_vms = DBServerVM(module)
    default_spec = db_server_vms.get_default_spec_for_registration()
    spec, err = db_server_vms.get_spec(old_spec=default_spec, register_server=True)
    if err:
        result["error"] = err
        err_msg = "Failed getting spec for db server vm registration"
        module.fail_json(msg=err_msg, **result)

    # configure automated patching
    if module.params.get("automated_patching"):
        mw = MaintenanceWindow(module)
        mw_spec, err = mw.get_spec(configure_automated_patching=True)
        if err:
            result["error"] = err
            err_msg = "Failed getting spec for automated patching for db server vm"
            module.fail_json(msg=err_msg, **result)
        spec["maintenanceTasks"] = mw_spec

    if err:
        result["error"] = err
        err_msg = "Failed getting spec for db server vm registration"
        module.fail_json(msg=err_msg, **result)

    # populate database engine related spec
    spec, err = db_server_vms.get_db_engine_spec(spec, register=True)
    if err:
        result["error"] = err
        err_msg = "Failed getting database engine related spec for database instance registration"
        module.fail_json(msg=err_msg, **result)

    return spec


def register_db_server(module, result):
    db_server_vms = DBServerVM(module)

    spec = get_register_spec(module, result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_server_vms.register(data=spec)
    result["response"] = resp
    result["uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid)
        resp = db_server_vms.read(db_uuid)
        result["response"] = resp

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("state", "present", ("postgres",), True)],
        mutually_exclusive=[("private_ssh_key", "password")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    register_db_server(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
