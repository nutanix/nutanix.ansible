#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_clusters
short_description: category module which supports pc category management CRUD operations
version_added: 1.5.0
description: "Create, Update, Delete categories"
options:

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
from ..module_utils.karbon.clusters import Cluster  # noqa: E402
from ..module_utils.prism.tasks import Task  # noqa: E402


def get_module_spec():
    mutually_exclusive = [("name", "uuid")]

    entity_by_spec = dict(name=dict(type="str"), uuid=dict(type="str"))

    resource_spec = dict(
        num_instances=dict(type="int", required=True),
        cpu=dict(type="int", required=True),
        memory_gb=dict(type="int", required=True),
        disk_gb=dict(type="int", required=True),
    )

    cni_spec = dict(
        node_cidr_mask_size=dict(type="int"),
        service_ipv4_cidr=dict(type="str"),
        pod_ipv4_cidr=dict(type="str"),
        flannel_config=dict(type="dict"),
    )

    storage_class_spec = dict(
        default_storage_class=dict(type="bool"),
        name=dict(type="str", required=True),
        reclaim_policy=dict(type="str"),
        storage_container=dict(type="str", required=True),
        file_system=dict(type="str", choices=["ext4", "xfs"]),
        flash_mode=dict(type="bool"),
    )

    module_args = dict(
        name=dict(type="str"),
        cluster_uuid=dict(type="str"),
        # type=dict(type="str", required=True),
        cluster=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        k8s_version=dict(type="str"),
        host_os=dict(type="str"),
        node_subnet=dict(
            type="dict", options=entity_by_spec, mutually_exclusive=mutually_exclusive
        ),
        cni=dict(type="dict", options=cni_spec),
        etcd=dict(type="dict", options=resource_spec),
        masters=dict(type="dict", options=resource_spec),
        storage_class=dict(type="dict", options=storage_class_spec),
        workers=dict(type="dict", options=resource_spec),
    )

    return module_args


def create_cluster(module, result):
    cluster = Cluster(module)
    # name = module.params["name"]
    # if cluster.get_uuid(name):
    #     module.fail_json(msg="Cluster with given name already exists", **result)

    spec, error = cluster.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating create cluster spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    resp = cluster.create(spec)
    cluster_uuid = resp["cluster_uuid"]
    task_uuid = resp["task_uuid"]
    result["cluster_uuid"] = cluster_uuid
    result["changed"] = True

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = cluster.read(cluster_uuid)

    result["response"] = resp


def delete_cluster(module, result):
    cluster_uuid = module.params["cluster_uuid"]
    if not cluster_uuid:
        result["error"] = "Missing parameter cluster_uuid in playbook"
        module.fail_json(msg="Failed deleting cluster", **result)

    cluster = Cluster(module)
    resp = cluster.delete(cluster_uuid)
    result["changed"] = True
    result["cluster_uuid"] = cluster_uuid
    task_uuid = resp["task_uuid"]
    result["task_uuid"] = task_uuid

    if module.params.get("wait"):
        task = Task(module)
        task.wait_for_completion(task_uuid)
        resp = cluster.read(cluster_uuid)

    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "cluster_uuid"), True),
            ("state", "absent", ("cluster_uuid",)),
        ],
        required_together=[
            (
                "name", "cluster", "k8s_version",
                "host_os", "node_subnet", "cni",
                "etcd", "masters", "storage_class",
                "workers"),
        ]
    )
    utils.remove_param_with_none_value(module.params)
    result = {
        "response": {},
        "error": None,
        "changed": False,
    }
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
