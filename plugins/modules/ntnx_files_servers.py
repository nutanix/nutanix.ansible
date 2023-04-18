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

from ..module_utils.base_module import BaseModule
from ..module_utils.utils import remove_param_with_none_value
from ..module_utils.files.file_servers import FileServer
from ..module_utils.prism.tasks import Task

def get_module_spec():
    entity_by_spec = dict(
        name = dict(type="str"),
        uuid = dict(type="str")
    )

    ntp_server = dict(
        ip=dict(type="str"),
        fqdn=dict(type="str")
    )
    ntp_server_mutually_exclusive_attrs = [("ipv4", "ipv6", "fqdn")]

    network = dict(
        is_managed = dict(type="bool", required=True),
        subnet = dict(type="dict", options=entity_by_spec, mutually_exclusive=[("name", "uuid")]),
        protocol = dict(type="str", choices=["ipv4", "ipv6"]),
        virtual_ip = dict(type="str"),
        ip_addresses = dict(type="list", elements="str"),
        default_gateway = dict(type="str"),
        netmask = dict(type="str"),
        prefix_length = dict(type="str")
    )

    vms_config = dict(
        memory_gb = dict(type="int"),
        vcpus = dict(type="int"),
        vms_count = dict(type="int"),
    )

    module_args = dict(
        name = dict(type="str"),
        version = dict(type="str"),
        cluster = dict(type="dict", options=entity_by_spec, mutually_exclusive=[("name", "uuid")]),
        size_gb = dict(type="int"),
        vms_config = dict(type="dict", options=vms_config),
        dns_domain_name = dict(type="str"),
        dns_servers = dict(type="list", elements="str"),
        ntp_servers = dict(type="list", elements="dict", option=ntp_server, mutually_exclusive=ntp_server_mutually_exclusive_attrs),
        file_blocking_extensions = dict(type="list", elements="str"),
        external_networks = dict(type="list", elements="dict", options=network),
        internal_networks = dict(type="list", elements="dict", options=network)
    )
    return module_args


def create_file_server(module, result):
    file_servers = FileServer(module)
    spec, err = file_servers.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating file server create spec", **result)
    
    if module.check_mode:
        result["response"] = spec
        return

    name = spec.get("name")
    cluster_uuid = spec.get("clusterExtId")

    resp = file_servers.create(spec)
    task_uuid = resp.get("data", {}).get("extId")
    uuid = file_servers.get_file_server_uuid(name=name, cluster_uuid=cluster_uuid)

    result["task_uuid"] = task_uuid
    result["uuid"] = uuid
    
    if task_uuid and module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
    
    resp = file_servers.read(uuid=uuid, query={"$mode":"pretty"})
    result["response"] = resp
    result["changed"] = True



def update_file_server(module, result):
    pass

def delete_file_server(module, result):
    pass


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "uuid": None}
    if module.params["state"] == "present":
        if module.params.get("uuid"):
            update_file_server(module, result)
        else:
            create_file_server(module, result)
    else:
        delete_file_server(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
