#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_karbon_clusters_info
short_description: cluster  info module
version_added: 1.0.0
description: 'Get cluster info'
options:
      cluster_name:
        description:
            - cluster name
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List clusters 
    ntnx_karbon_clusters_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
    register: result

  - name: Get clusters using name
    ntnx_clusters_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      cluster_name: "cluster-name"
    register: result

"""
RETURN = r"""
    [
        {
            "cni_config": {
                "flannel_config": null,
                "node_cidr_mask_size": 24,
                "pod_ipv4_cidr": "172.20.0.0/16",
                "service_ipv4_cidr": "172.19.0.0/16"
            },
            "etcd_config": {
                "node_pools": [
                    "test-module21_etcd_pool"
                ]
            },
            "kubeapi_server_ipv4_address": "10.44.78.171",
            "master_config": {
                "deployment_type": "single-master",
                "node_pools": [
                    "test-module21_master_pool"
                ]
            },
            "name": "test-module21",
            "status": "kActive",
            "uuid": "70a9ca27-80c6-4bd1-5600-3764a5265ebd",
            "version": "1.19.8-0",
            "worker_config": {
                "node_pools": [
                    "test-module21_worker_pool"
                ]
            }
        }
    ]
"""

from ..module_utils.base_info_module import BaseInfoModule
from ..module_utils.karbon.clusters import Cluster  # noqa: E402


def get_module_spec():

    module_args = dict(
        cluster_name=dict(type="str")
    )

    return module_args


def get_cluster(module, result):
    cluster = Cluster(module)
    cluster_name = module.params.get("cluster_name")
    resp = cluster.read(cluster_name)

    result["response"] = resp


def get_clusters(module, result):
    cluster = Cluster(module, resource_type="/v1-beta.1/k8s/clusters")

    resp = cluster.read()

    result["response"] = resp


def run_module():
    info_module = BaseInfoModule.__new__()
    info_module.info_argument_spec = {}
    module = info_module(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("cluster_name"):
        get_cluster(module, result)
    else:
        get_clusters(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
