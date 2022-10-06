#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils.era.base_module import EraBaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]
    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    db_vm = dict(
        create_new=dict(type="bool", required=True),
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        pub_ssh_key=dict(type="str", required=True),
        password=dict(type="str", required=True),
        cluster=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        software_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        network_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
        compute_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=True,
        ),
    )

    # can override existing sla config
    sla = dict(
        uuid=dict(type="str", required=False),
        name=dict(type="str", required=False),
        daily=dict(type="str", required=False),
        weekly=dict(type="str", required=False),
        monthly=dict(type="int", required=False),
        yearly=dict(type="str", required=False),
        log_catchup=dict(type="int", choices=[15, 30, 60, 90, 120], required=False),
        snapshots_per_day=dict(type="int", required=False),
    )

    time_machine = dict(
        name=dict(type="str", required=True),
        desc=dict(type="str", required=True),
        sla=dict(type="dict", options=sla, required=True),
    )

    postgress = dict(
        listener_port=dict(type=int, required=True),
        db_size=dict(type="str", required=True),
        db_name=dict(type="str", required=True),
        db_password=dict(type="str", required=True),
        pre_create_script=dict(type="str", required=False),
        pre_create_script=dict(type="str", required=False),
    )

    module_args = dict(
        name=dict(type="str", required=False),
        desc=dict(type="str", required=False),
        db_params_profile=dict(
            type="dict",
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        db_vm=dict(
            type="dict",
            options=db_vm,
            options=entity_by_spec,
            mutually_exclusive=mutually_exclusive,
            required=False,
        ),
        time_machine=dict(type="dict", options=time_machine, required=False),
        postgress=dict(type="dict", options=postgress, required=False),
    )
    return module_args


def create_instance(module, result):
    pass


def update_instance(module, result):
    pass


def delete_instance(module, result):
    pass


def run_module():
    module = EraBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("uuid"):
            update_instance(module, result)
        else:
            create_instance(module, result)
    else:
        delete_instance(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
