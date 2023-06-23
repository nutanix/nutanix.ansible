#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_clusters_node_pools
short_description: Create,Update and Delete a worker node pools with the provided configuration.
version_added: 1.9.0
description: "Create, update and and Delete worker node pools"
options:
    cluster_name:
        type: str
        description: Unique name of the k8s node_pool.
        required: true
    node_pool_name:
        type: str
        description:
            - Unique name of the k8s cluster's node pool.
            - We can create, update or delete by using the  name
        required: true
    node_subnet:
        type: dict
        description: Configuration of the node pools that the nodes in the etcd,workers,master cluster belong to
        suboptions:
            name:
                type: str
                description:
                 - Subnet name
                 - Mutually exclusive with C(uuid)
            uuid:
                type: str
                description:
                    - Subnet UUID
                    - Mutually exclusive with C(name)
    node_iscsi_subnet:
        type: dict
        description:
            - Configuration of the node pools that the nodes in the etcd,workers,master cluster belong to
        suboptions:
            name:
                type: str
                description:
                 - Subnet name
                 - Mutually exclusive with C(uuid)
            uuid:
                type: str
                description:
                    - Subnet UUID
                    - Mutually exclusive with C(name)
    pool_config:
        type: dict
        description:
                -  Configuration of the node pools that the workers belong to.
                -  The worker nodes require a minimum of 8,192 MiB memory and 122,880 MiB disk space.
                - disk space >=120880 Mib
                - Memory >= 8192 Mib
        suboptions:
            num_instances:
                type: int
                default: 1
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
    add_labels:
        type: dict
        description: Map of user-provided labels for the nodes in the node pool.
    remove_labels:
        type: list
        description: Map of user-provided labels for the nodes in the node pool to remove.
        elements: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
author:
    - Prem Karat (@premkarat)
    - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
    - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Create node pool with subnet uuid
  ntnx_karbon_clusters_node_pools:
    node_subnet:
      uuid: "<uuid>"
    node_pool_name:  "node_pool_name"
    cluster_name:  "cluster_name"
    pool_config:
      num_instances: 2
      cpu: 4
      memory_gb: 8
      disk_gb: 120
  register: result
  ignore_errors: true

- name: update pool by increasing cpu,memory_gb,num_instances and add labels
  ntnx_karbon_clusters_node_pools:
    wait: True
    node_pool_name:  "node_name"
    cluster_name:  "cluster_name"
    pool_config:
        cpu: 6
        memory_gb: 10
        disk_gb: 150
        num_instances: 4
    add_labels:
      property1: "test-property1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: List of node worker pools
  returned: always
  type: dict
  sample: {
            "ahv_config": {
                "cpu": 8,
                "disk_mib": 122880,
                "memory_mib": 8192,
                "network_name": "",
                "network_uuid": "",
                "prism_element_cluster_uuid": ""
            },
            "assigned_gpu_config_list": [],
            "category": "worker",
            "default": true,
            "labels": {
                "nke-default": "true"
            },
            "name": "test-module21-worker-pool",
            "node_os_version": "ntnx-1.5",
            "nodes": [
                {
                    "hostname": "test-module21-b5fe00-worker-0",
                    "ipv4_address": ""
                }
            ],
            "num_instances": 1
    }
cluster_name:
  description: kubernetes cluster name
  returned: always
  type: str
  sample: "test_cluster"
node_pool_name:
  description: worker node pool name
  returned: always
  type: str
  sample: "node_pool_A"
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
        pool_config=dict(type="dict", apply_defaults=True, options=resource_spec),
        node_subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        node_iscsi_subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        add_labels=dict(type="dict"),
        remove_labels=dict(type="list", elements="str"),
    )

    return module_args


def create_pool(module, result):
    node_pool = NodePool(module)
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]

    pool = node_pool.get_node_pool(cluster_name, pool_name)
    if pool:
        update_pool(module, result, pool)
        return

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
    result["node_pool_name"] = pool_name
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = node_pool.get_node_pool(cluster_name, pool_name)

    result["response"] = resp


def update_pool(module, result, pool=None):
    node_pool = NodePool(module)
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]
    nodes_expected_count = module.params.get("pool_config", {}).get("num_instances")
    nodes_actual_count = len(pool.get("nodes", []))
    add_labels = module.params.get("add_labels")
    remove_labels = module.params.get("remove_labels")
    wait = module.params.get("wait")
    nothing_to_change = False

    if not (nodes_expected_count or add_labels or remove_labels):
        result["error"] = (
            "Missing parameter in playbook."
            "One of attributes pool_config.num_instances|add_labels|remove_labels is required"
        )
        module.fail_json(msg="Failed updating node pool", **result)

    # resize pool
    if nodes_expected_count:
        if nodes_expected_count != nodes_actual_count:
            resp = node_pool.update_nodes_count(
                cluster_name, pool_name, nodes_actual_count, nodes_expected_count
            )
            task_uuid = resp.get("task_uuid")
            result["nodes_update_response"] = resp
            result["changed"] = True
            if task_uuid and wait:
                task = Task(module)
                task.wait_for_completion(task_uuid)
        else:
            nothing_to_change = True

    # update labels
    if add_labels or remove_labels:
        labels_spec = node_pool.get_labels_spec()
        if module.check_mode:
            result["response"] = labels_spec
            return
        raise_error = False if result["changed"] else True
        resp = node_pool.update_labels(
            cluster_name, pool_name, labels_spec, raise_error
        )
        result["labels_update_response"] = resp
        task_uuid = resp.get("task_uuid")

        if task_uuid:
            result["changed"] = True
            if wait:
                task = Task(module)
                resp = task.wait_for_completion(task_uuid, raise_error)
                state = resp.get("status")
                if state == "FAILED":
                    result["skipped"] = True
                    result["error"] = resp.get("error_detail")
        else:
            result["skipped"] = True
    else:
        if nothing_to_change:
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.")

    pool = node_pool.get_node_pool(cluster_name, pool_name)
    result["response"] = pool
    result["cluster_name"] = cluster_name
    result["node_pool_name"] = pool_name


def delete_nodes_of_pool(module, result):
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]

    node_pool = NodePool(module)
    resp = node_pool.remove_pool_nodes(cluster_name, pool_name)
    result["changed"] = True
    task_uuid = resp.get("task_uuid")

    if task_uuid:
        task = Task(module)
        task.wait_for_completion(task_uuid)


def delete_pool(module, result):
    cluster_name = module.params["cluster_name"]
    pool_name = module.params["node_pool_name"]

    delete_nodes_of_pool(module, result)

    node_pool = NodePool(module, resource_type="/v1-beta.1/k8s/clusters")
    resp = node_pool.remove_node_pool(cluster_name, pool_name)

    result["changed"] = True
    result["cluster_name"] = cluster_name
    result["node_pool_name"] = pool_name
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
        required_if=[("state", "absent", ("cluster_name", "node_pool_name"))],
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
