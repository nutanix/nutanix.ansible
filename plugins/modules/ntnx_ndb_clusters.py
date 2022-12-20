#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_clusters
short_description: Create, Delete a k8s cluster with the provided configuration.
version_added: 1.6.0
description: "Create, Delete clusters"
options:
    name:
        type: str
        description: Name of the cluster.
        required: true

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
    - Prem Karat (@premkarat)
    - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
    - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

from ..module_utils import utils  # noqa: E402
from ..module_utils.ndb.base_module import NdbBaseModule  # noqa: E402
from ..module_utils.ndb.clusters import Cluster  # noqa: E402
from ..module_utils.ndb.operations import Operation  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():

    credentials_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    agent_network_spec = dict(
        dns_servers=dict(type="list"),
        ntp_servers=dict(type="list"),
    )

    vlan_access_spec = dict(
        vlan_name=dict(type="str"),
        vlan_type=dict(type="str", choices=["DHCP", "Static"]),
        static_ip=dict(type="str"),
        gateway=dict(type="str"),
        subnet_mask=dict(type="str"),
    )

    vlan_access_type_spec = dict(
        prism_vlan=dict(type="dict", options=vlan_access_spec),
        dsip_vlan=dict(type="dict", options=vlan_access_spec),
        dbserver_vlan=dict(type="dict", options=vlan_access_spec),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        desc=dict(type="str"),
        name_prefix=dict(type="str"),
        cluster_ip=dict(type="str"),
        cluster_credentials=dict(type="dict", options=credentials_spec),
        agent_network=dict(type="dict", options=agent_network_spec),
        vlan_access=dict(type="dict", options=vlan_access_type_spec),
        storage_container=dict(type="str"),
    )

    return module_args


def create_cluster(module, result):
    cluster = Cluster(module, api_version="v0.8")

    spec, err = cluster.get_spec()
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create cluster spec", **result)

    if cluster.get_cluster_by_ip():
        module.fail_json(
            msg="The provided cluster IP is already registered with NDB.", **result
        )

    if module.check_mode:
        result["response"] = spec
        return

    resp = cluster.create(spec)
    cluster_name = resp["entityName"]
    ops_uuid = resp["operationId"]
    resp, err = cluster.get_cluster(name=cluster_name)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create cluster spec", **result)

    cluster_uuid = resp["id"]
    result["cluster_uuid"] = cluster_uuid
    result["changed"] = True

    if module.params.get("wait"):
        operations = Operation(module)
        operations.wait_for_completion(ops_uuid)
        resp = cluster.read(cluster_uuid)

    result["response"] = resp


def update_cluster(module, result):
    cluster_uuid = module.params["uuid"]

    cluster = Cluster(module)

    resp = cluster.read(cluster_uuid)
    old_spec = cluster.get_default_update_spec(override_spec=resp)

    update_spec, err = cluster.get_spec(old_spec=old_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update cluster spec", **result)

    if module.check_mode:
        result["response"] = old_spec
        return

    resp = cluster.update(update_spec)
    ops_uuid = resp["operationId"]
    result["cluster_uuid"] = cluster_uuid
    result["changed"] = True

    if module.params.get("wait"):
        operations = Operation(module)
        operations.wait_for_completion(ops_uuid)
        resp = cluster.read(cluster_uuid)

    result["response"] = resp


def delete_cluster(module, result):
    cluster_name = module.params["name"]
    if not cluster_name:
        result["error"] = "Missing parameter name in playbook"
        module.fail_json(msg="Failed deleting cluster", **result)

    cluster = Cluster(module)
    resp = cluster.delete(cluster_name)
    result["changed"] = True
    result["cluster_name"] = cluster_name
    task_uuid = resp["task_uuid"]
    result["task_uuid"] = task_uuid

    if module.params.get("wait"):
        task = Task(module)
        resp = task.wait_for_completion(task_uuid)

    result["response"] = resp


def run_module():
    module = NdbBaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("uuid", "name_prefix"),
            ("uuid", "agent_network"),
            ("uuid", "vlan_access"),
            ("uuid", "storage_container"),
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"response": {}, "error": None, "changed": False}
    state = module.params["state"]
    if state == "present":
        create_cluster(module, result)
    else:
        delete_cluster(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
