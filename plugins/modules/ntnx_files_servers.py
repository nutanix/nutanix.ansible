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
        uuid = dict(type="str"),
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
    _file_server = FileServer(module)
    kwargs = {"create": True}
    spec, err = _file_server.get_spec(**kwargs)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating file server create spec", **result)
    
    if module.check_mode:
        result["response"] = spec
        return

    name = spec.get("name")
    cluster_uuid = spec.get("clusterExtId")

    resp = _file_server.create(spec)
    task_uuid = resp.get("data", {}).get("extId")
    uuid = _file_server.get_file_server_uuid(name=name, cluster_uuid=cluster_uuid)

    result["task_uuid"] = task_uuid
    result["uuid"] = uuid
    
    if task_uuid and module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
    
    resp = _file_server.read(uuid=uuid).get("data")
    result["response"] = resp
    result["changed"] = True



def update_file_server(module, result):
    uuid = module.params.get("uuid")
    if not uuid:
        return module.fail_json("'uuid' is mandatory for update", **result)
    
    _file_server = FileServer(module)
    resp = _file_server.read(uuid, include_etag=True)
    file_server = resp.get("data")
    if not file_server:
        return module.fail_json("unable to fetch file server's info", **result)
    
    # get etag
    if not resp.get("etag"):
        return module.fail_json("unable to fetch etag from file server's info", **result)

    etag = resp.pop("etag")

    # create update spec
    kwargs={"update": True}
    update_spec, err = _file_server.get_spec(old_spec=file_server, **kwargs)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating file server update spec", **result)
    
    result["uuid"] = uuid

    if module.check_mode:
        result["response"] = update_spec
        return
    
    # update platform related fields
    resp = _file_server.update(data=update_spec, uuid=uuid, etag=etag)
    task_uuid = resp.get("data", {}).get("extId")
    if task_uuid and module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
    
    resp = _file_server.read(uuid=uuid).get("data")
    result["response"] = resp
    result["changed"] = True

def delete_file_server(module, result):
    uuid = module.params.get("uuid")
    if not uuid:
        return module.fail_json("'uuid' is mandatory for update", **result)
    
    _file_server = FileServer(module)
    resp = _file_server.delete(uuid=uuid)
    task_uuid = resp.get("data", {}).get("extId")
    if task_uuid and module.params.get("wait"):
        task = Task(module)
        resp = task.wait_for_completion(task_uuid)
    
    result["response"] = resp
    result["changed"] = True


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
