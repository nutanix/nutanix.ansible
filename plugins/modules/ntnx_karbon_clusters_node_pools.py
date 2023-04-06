#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_clusters_node_pools
short_description: Create, Delete a k8s cluster with the provided configuration.
version_added: 1.6.0
description: "Create, Update and Delete node pools"
options:
    cluster_name:
        type: str
        description: Unique name of the k8s node_pool.
        required: true
    node_pool_name:
        type: str
        description: Unique name of the k8s cluster's node pool.
        required: true
    node_subnet:
        type: dict
        description: Configuration of the node pools that the nodes in the etcd,workers,master cluster belong to
        suboptions:
            name:
                type: str
                description: Subnet name
            uuid:
                type: str
                description: Subnet UUID
    node_iscsi_subnet:
        type: dict
        description: Configuration of the node pools that the nodes in the etcd,workers,master cluster belong to
        suboptions:
            name:
                type: str
                description: Subnet name
            uuid:
                type: str
                description: Subnet UUID
    pool_configs:
        type: dict
        description: write
        suboptions:
            num_instances:
                type: int
                description: Number of nodes in the node pool.
            cpu:
                type: int
                description: The number of VCPUs allocated for each VM on the PE node_pool.
                default: 4
            disk_gb:
                type: int
                description: Size of local storage for each VM on the PE cluster in GiB.
                default: 120
            memory_gb:
                type: int
                description: Memory allocated for each VM on the PE cluster in GiB.
                default: 8
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
from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.karbon.node_pools import NodePool  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    resource_spec = dict(
        num_instances=dict(type="int", default=1),
        cpu=dict(type="int", default=4),
        memory_gb=dict(type="int", default=8),
        disk_gb=dict(type="int", default=120),
    )

    module_args = dict(
        cluster_name=dict(type="str", required=True),
        node_pool_name=dict(type="str", required=True),
        pool_config=dict(type="dict", options=resource_spec),
        node_subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        node_iscsi_subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        nodes_count=dict(type="int"),
        add_labels=dict(type="dict"),
        remove_labels=dict(type="list"),

    )

    return module_args


def create_pool(module, result):
    node_pool = NodePool(module)
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]
    spec, error = node_pool.get_pool_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create pool spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = node_pool.add_node_pool(cluster_name, spec)
    task_uuid = resp["task_uuid"]
    result["cluster_name"] = cluster_name
    result["pool_name"] = pool_name
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = node_pool.read_node_pools(cluster_name)

    result["response"] = resp


def update_pool(module, result):
    node_pool = NodePool(module)
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["pool_name"]

    node_pool = node_pool.read_node_pool(cluster_name, pool_name)
    # resize pool
    if module.params.get("count"):
        if module.params.get("count") > node_pool["count"]:
            resp = node_pool.add_node(cluster_name, pool_name)
        else:
            resp = node_pool.remove_node(cluster_name, pool_name)
        pass
    # update labels
    if module.params.get("add_labels") or module.params.get("remove_labels"):
        resp = node_pool.update_labels()


def delete_nodes_of_pool(module, result):
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]

    node_pool = NodePool(module)
    resp = node_pool.remove_nodes_of_pool(cluster_name, pool_name)
    result["changed"] = True
    task_uuid = resp.get("task_uuid")

    if task_uuid:
        task = Task(module)
        task.wait_for_completion(task_uuid)


def delete_pool(module, result):
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]
    if not pool_name:
        result["error"] = "Missing parameter node_pool_name in playbook"
        module.fail_json(msg="Failed deleting node pool", **result)

    delete_nodes_of_pool(module, result)

    node_pool = NodePool(module, resource_type="/v1-beta.1/k8s/clusters")
    resp = node_pool.remove_node_pool(cluster_name, pool_name)

    result["changed"] = True
    result["cluster_name"] = cluster_name
    result["pool_name"] = pool_name
    task_uuid = resp["task_uuid"]
    result["task_uuid"] = task_uuid

    if module.params.get("wait"):
        task = Task(module)
        resp = task.wait_for_completion(task_uuid)

    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
        ],
        required_together=[
        ],
    )
    utils.remove_param_with_none_value(module.params)
    result = {"response": {}, "error": None, "changed": False}
    state = module.params["state"]
    if state == "present":
        create_pool(module, result)
    else:
        delete_pool(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
