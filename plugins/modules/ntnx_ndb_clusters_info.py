#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ndb_clusters_info
short_description: info module for ndb clusters info
version_added: 1.8.0
description: 'Get clusters info'
options:
      name:
        description:
            - cluster name
        type: str
      uuid:
        description:
            - cluster id
        type: str
      filters:
        description:
            - params to be considered for filtering response
        type: dict
        suboptions:
            count_entities:
                description:
                    - to show dependent entities of clusters
                type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_ndb_info_base_module
      - nutanix.ncp.ntnx_logger
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
"""

EXAMPLES = r"""
- name: List all era clusters
  ntnx_ndb_clusters_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
  register: clusters

- name: get era clusters using it's name
  ntnx_ndb_clusters_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    name: "test_cluster"
  register: result

- name: List clusters use id
  ntnx_ndb_clusters_info:
    nutanix_host: "<ndb_era_ip>"
    nutanix_username: "<ndb_era_username>"
    nutanix_password: "<ndb_era_password>"
    validate_certs: false
    uuid: "<uuid of cluster>"
  register: result
"""
RETURN = r"""
response:
  description: listing all clusters
  returned: always
  type: list
  sample:  [
            {
                "cloudInfo": null,
                "cloudType": "NTNX",
                "dateCreated": "2022-09-30 11:09:58.232685",
                "dateModified": "2022-10-08 05:20:02.513367",
                "description": "",
                "entityCounts": null,
                "fqdns": null,
                "healthy": true,
                "hypervisorType": "AHV",
                "hypervisorVersion": "6.1",
                "id": "d7844b99-5a9d-4da7-8e7d-c938499214de",
                "ipAddresses": [
                    "000.000.000.000"
                ],
                "managementServerInfo": null,
                "name": "EraCluster",
                "nxClusterUUID": "4705e777-bfc7-11e4-3507-ac1f6b60292f",
                "ownerId": "eac70dbf-42fb-468b-9498-949796ca1f73",
                "password": null,
                "properties": [
                    {
                        "description": null,
                        "name": "CLUSTER_ID",
                        "ref_id": null,
                        "secure": false,
                        "value": "0005e777-bf47-11e4-3507-ac1f6b60292f::3821212059792582959"
                    },
                    {
                        "description": null,
                        "name": "CLUSTER_INCARNATION_ID",
                        "ref_id": null,
                        "secure": false,
                        "value": "1661876478172260"
                    },
                    {
                        "description": null,
                        "name": "ERA_STORAGE_CONTAINER",
                        "ref_id": null,
                        "secure": false,
                        "value": "default-container-75707403530678"
                    },
                    {
                        "description": null,
                        "name": "MODEL_NAME",
                        "ref_id": null,
                        "secure": false,
                        "value": "NX-1065-G5"
                    },
                    {
                        "description": null,
                        "name": "ONDEMAND_REPLICATION_SUPPORTED",
                        "ref_id": null,
                        "secure": false,
                        "value": "true"
                    },
                    {
                        "description": null,
                        "name": "PRISM_VM_LIST_PAGINATION_LIMIT",
                        "ref_id": null,
                        "secure": false,
                        "value": "500"
                    },
                    {
                        "description": null,
                        "name": "PRISM_VM_LIST_PAGINATION_SIZE",
                        "ref_id": null,
                        "secure": false,
                        "value": "50"
                    },
                    {
                        "description": null,
                        "name": "RESOURCE_CONFIG",
                        "ref_id": null,
                        "secure": false,
                        "value": "{\"storageThresholdPercentage\":95.0,\"memoryThresholdPercentage\":95.0}"
                    },
                    {
                        "description": null,
                        "name": "TIMEZONE",
                        "ref_id": null,
                        "secure": false,
                        "value": "UTC"
                    }
                ],
                "referenceCount": 0,
                "resourceConfig": {
                    "memoryThresholdPercentage": 95.0,
                    "storageThresholdPercentage": 95.0
                },
                "status": "UP",
                "uniqueName": "ERACLUSTER",
                "username": null,
                "version": "v2"
            }
        ]

"""

from ..module_utils.v3.ndb.base_info_module import NdbBaseInfoModule  # noqa: E402
from ..module_utils.v3.ndb.clusters import Cluster  # noqa: E402


def get_module_spec():

    filters_spec = dict(
        count_entities=dict(type="bool"),
    )

    module_args = dict(
        name=dict(type="str"),
        uuid=dict(type="str"),
        filters=dict(
            type="dict",
            options=filters_spec,
        ),
    )

    return module_args


def get_cluster(module, result):
    cluster = Cluster(module)
    if module.params.get("name"):
        name = module.params["name"]
        resp, err = cluster.get_cluster(name=name)
    else:
        uuid = module.params["uuid"]
        resp, err = cluster.get_cluster(uuid=uuid)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed fetching cluster info", **result)
    result["response"] = resp


def get_clusters(module, result):
    cluster = Cluster(module)
    query_params = module.params.get("filters")

    resp = cluster.read(query=query_params)

    result["response"] = resp


def run_module():
    module = NdbBaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("name", "uuid"),
            ("name", "filters"),
            ("uuid", "filters"),
        ],
    )
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("name") or module.params.get("uuid"):
        get_cluster(module, result)
    else:
        get_clusters(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
