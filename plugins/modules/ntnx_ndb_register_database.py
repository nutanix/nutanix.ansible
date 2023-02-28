#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_register_database
short_description: module for database instance registration
version_added: 1.8.0
description:
    - module for database instance registration
    - currently, only postgres single instance database registration is supported
options:
    name:
        description:
            - name of database instance to be created in ndb
        type: str
        required: true
    desc:
        description:
            - description of database instance
        type: str
    db_vm:
        description:
            - source database server vm details
            - either registered or non registered vm can be configured as source
        type: dict
        required: true
        suboptions:
            registered:
                description:
                    - configure a registered vm as source
                type: dict
                suboptions:
                    name:
                        description:
                            - name of database server vm
                            - mutually exclusive with C(uuid) and C(ip)
                        type: str
                    uuid:
                        description:
                            - name of database server vm
                            - mutually exclusive with C(name) and C(ip)
                        type: str
                    ip:
                        description:
                            - ip of database server vm
                            - mutually exclusive with C(uuid) and C(name)
                        type: str
            unregistered:
                description:
                    - configure a unregistered vm as source
                    - registration of database will also register given vm
                type: dict
                suboptions:
                    ip:
                        description:
                            - ip of vm
                        type: str
                        required: true
                    username:
                        description:
                            - username of vm
                        type: str
                        required: true
                    private_key:
                        description:
                            - private key of vm
                            - mutually exclusive with C(password)
                        type: str
                    password:
                        description:
                            - password of vm
                            - mutually exclusive with C(private_key)
                        type: str
                    desc:
                        description:
                            - set description of vm
                        type: str
                    reset_desc_in_ntnx_cluster:
                        description:
                            - reset description in cluster to C(desc) given
                        type: bool
                        default: false
                    cluster:
                        description:
                            - cluster where vm is present
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
    time_machine:
        description:
            - configure new time machine for database instance
        type: dict
        required: true
        suboptions:
            name:
                description:
                    - name of time machine
                type: str
                required: true
            desc:
                description:
                    - description of time machine
                type: str
            sla:
                description:
                    - configure sla
                type: dict
                required: true
                suboptions:
                    name:
                        description:
                            - name of sla
                            - mutually exclusive with C(uuid)
                        type: str
                    uuid:
                        description:
                            - uuid of sla
                            - mutually exclusive with C(name)
                        type: str
            schedule:
                description:
                    - configure schedule of snapshots
                type: dict
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
                description:
                    - set flag for auto tuning of log drive
                type: bool
                default: true
    postgres:
        description:
            - potgres related configuration
        type: dict
        suboptions:
            listener_port:
                description:
                    - listener port of database in vm
                type: str
                default: "5432"
            db_name:
                description:
                    - intial database that would be added
                type: str
                required: true
            db_password:
                description:
                    - password of C(db_user) in database instance
                type: str
                required: true
            db_user:
                description:
                    - user name for connecting to database instance in vm
                type: str
                default: "postgres"
            software_path:
                description:
                    - path where desired postgres instance is located. For ex. "/usr/pgsql-10.4"
                type: str
            type:
                description:
                    - architecture type of database
                type: str
                choices: ["single"]
                default: "single"
    tags:
        description:
            - dict of tag name as key and tag value as value
        type: dict
    auto_tune_staging_drive:
        description:
            - flag for auto tuning staging drive
        type: bool
    working_directory:
        description:
            - directory path to be created and used by ndb for its scripts
        type: str
        default: "/tmp"
    automated_patching:
        description:
            - automated patching configuration
        type: dict

extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_base_module
      - nutanix.ncp.ntnx_operations
      - nutanix.ncp.ntnx_AutomatedPatchingSpec

author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
"""
RETURN = r"""
"""
import time  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.database_instances import DatabaseInstance  # noqa: E402
from ..module_utils.ndb.db_server_vm import DBServerVM  # noqa: E402
from ..module_utils.ndb.maintenance_window import (  # noqa: E402
    AutomatedPatchingSpec,
    MaintenanceWindow,
)
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.ndb.tags import Tag  # noqa: E402
from ..module_utils.ndb.time_machines import TimeMachine  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))
    automated_patching = deepcopy(
        AutomatedPatchingSpec.automated_patching_argument_spec
    )
    registered_vm = dict(
        name=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        ip=dict(type="str", required=False),
    )

    unregistered_vm = dict(
        ip=dict(type="str", required=True),
        username=dict(type="str", required=True),
        private_key=dict(type="str", required=False, no_log=True),
        password=dict(type="str", required=False, no_log=True),
        desc=dict(type="str", required=False),
        reset_desc_in_ntnx_cluster=dict(type="bool", default=False, required=False),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )

    db_vm = dict(
        registered=dict(
            type="dict",
            options=registered_vm,
            mutually_exclusive=[("name", "uuid", "ip")],
            required=False,
        ),
        unregistered=dict(
            type="dict",
            options=unregistered_vm,
            mutually_exclusive=[("password", "private_key")],
            required=False,
        ),
    )

    sla = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
    )

    schedule = dict(
        daily=dict(type="str", required=False),
        weekly=dict(type="str", required=False),
        monthly=dict(type="int", required=False),
        quaterly=dict(type="str", required=False),
        yearly=dict(type="str", required=False),
        log_catchup=dict(type="int", choices=[15, 30, 60, 90, 120], required=False),
        snapshots_per_day=dict(type="int", required=False, default=1),
    )

    time_machine = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        sla=dict(
            type="dict",
            options=sla,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        schedule=dict(type="dict", options=schedule, required=False),
        auto_tune_log_drive=dict(type="bool", required=False, default=True),
    )

    postgres = dict(
        listener_port=dict(type="str", default="5432", required=False),
        db_name=dict(type="str", required=True),
        db_password=dict(type="str", required=True, no_log=True),
        db_user=dict(type="str", default="postgres", required=False),
        software_path=dict(type="str", required=False),
        type=dict(type="str", choices=["single"], default="single", required=False),
    )

    module_args = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=False),
        db_vm=dict(
            type="dict",
            options=db_vm,
            mutually_exclusive=[("registered", "unregistered")],
            required=True,
        ),
        time_machine=dict(type="dict", options=time_machine, required=True),
        postgres=dict(type="dict", options=postgres, required=False),
        tags=dict(type="dict", required=False),
        auto_tune_staging_drive=dict(type="bool", required=False),
        working_directory=dict(type="str", default="/tmp", required=False),
        automated_patching=dict(
            type="dict", options=automated_patching, required=False
        ),
    )
    return module_args


def get_registration_spec(module, result):

    # create database instance obj
    db_instance = DatabaseInstance(module=module)

    # get default spec
    spec = db_instance.get_default_registration_spec()

    # populate VM related spec
    db_vm = DBServerVM(module=module)

    use_registered_server = (
        True if module.params.get("db_vm", {}).get("registered") else False
    )
    register_server = not use_registered_server

    kwargs = {
        "use_registered_server": use_registered_server,
        "register_server": register_server,
        "db_instance_register": True,
    }
    spec, err = db_vm.get_spec(old_spec=spec, **kwargs)
    if err:
        result["error"] = err
        err_msg = "Failed getting vm spec for new database instance registration"
        module.fail_json(msg=err_msg, **result)

    # populate database engine related spec
    spec, err = db_instance.get_db_engine_spec(spec, register=True)
    if err:
        result["error"] = err
        err_msg = "Failed getting database engine related spec for database instance registration"
        module.fail_json(msg=err_msg, **result)

    # populate database instance related spec
    spec, err = db_instance.get_spec(spec, register=True)
    if err:
        result["error"] = err
        err_msg = "Failed getting spec for database instance registration"
        module.fail_json(msg=err_msg, **result)

    # populate time machine related spec
    time_machine = TimeMachine(module)
    spec, err = time_machine.get_spec(spec)
    if err:
        result["error"] = err
        err_msg = (
            "Failed getting spec for time machine for database instance registration"
        )
        module.fail_json(msg=err_msg, **result)

    # populate tags related spec
    tags = Tag(module)
    spec, err = tags.get_spec(spec, associate_to_entity=True, type="DATABASE")
    if err:
        result["error"] = err
        err_msg = "Failed getting spec for tags for database instance registration"
        module.fail_json(msg=err_msg, **result)

    # configure automated patching
    if module.params.get("automated_patching"):
        mw = MaintenanceWindow(module)
        mw_spec, err = mw.get_spec(configure_automated_patching=True)
        if err:
            result["error"] = err
            err_msg = "Failed getting spec for automated patching in database instance"
            module.fail_json(msg=err_msg, **result)
        spec["maintenanceTasks"] = mw_spec

    return spec


def register_instance(module, result):
    db_instance = DatabaseInstance(module)

    spec = get_registration_spec(module, result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = db_instance.register(data=spec)
    result["response"] = resp
    result["db_uuid"] = resp["entityId"]
    db_uuid = resp["entityId"]

    if module.params.get("wait"):
        ops_uuid = resp["operationId"]
        operations = Operation(module)
        time.sleep(5)  # to get operation ID functional
        operations.wait_for_completion(ops_uuid, delay=15)
        query = {"detailed": True, "load-dbserver-cluster": True}
        resp = db_instance.read(db_uuid, query=query)
        result["response"] = resp

    result["changed"] = True


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "db_uuid": None}
    register_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
