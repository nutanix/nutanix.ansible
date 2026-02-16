#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_hosts_info_v2
short_description: Retrieve information about Nutanix hosts from PC.
version_added: 2.0.0
description:
  - This module retrieves information about Nutanix hosts from PC.
  - Fetch particular host info using external ID.
  - Fetch multiple hosts info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the host.
      - If not provided, multiple hosts info will be fetched.
    type: str
  cluster_ext_id:
    description:
      - The external ID of the cluster to filter hosts by.
      - If provided, hosts info will be fetched for the specified cluster.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: Get host by external ID
  nutanix.ncp.ntnx_hosts_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9
  register: result

- name: Get hosts by cluster external ID
  nutanix.ncp.ntnx_hosts_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: 3a5b8c0e-1d7b-4c1d-9c3e-6f6e4d5b7a8c
  register: result

- name: List all hosts
  nutanix.ncp.ntnx_hosts_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: List all hosts with filter
  nutanix.ncp.ntnx_hosts_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: hostName eq 'host1'
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching host info.
        - Returns host info if ext_id is provided or list of multiple hosts.
    type: dict
    returned: always
    sample:
        {
          "extId": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
          "hostName": "ansible_ag",
          "hostType": "HYPER_CONVERGED",
          "hypervisor":
            {
              "externalAddress":
                { "ipv4": { "value": "10.0.0.1", "prefixLength": 32 } },
              "userName": "root",
              "fullName": "Nutanix124",
              "type": "AHV",
              "numberOfVms": 1,
              "state": "ACROPOLIS_NORMAL",
              "acropolisConnectionState": "CONNECTED",
            },
          "cluster":
            {
              "uuid": "00061de8-3ccd-9d88-185b-ac1f6b6f97e2",
              "name": "ansible_ag",
            },
          "controllerVm":
            {
              "id": 2,
              "externalAddress":
                { "ipv4": { "value": "10.0.0.2", "prefixLength": 32 } },
              "backplaneAddress":
                { "ipv4": { "value": "10.0.0.3", "prefixLength": 32 } },
              "ipmi":
                {
                  "ip": { "ipv4": { "value": "10.0.0.4", "prefixLength": 32 } },
                  "username": "ADMIN",
                },
              "rackableUnitUuid": "f2522411-7085-4771-9007-262286cbaa9b",
            },
          "disk":
            [
              {
                "uuid": "742fd128-721e-4cbb-96af-8f1211c27e95",
                "mountPath": "/home/nutnanix/temp",
                "sizeInBytes": 1800937370625,
                "serialId": "ABCD",
                "storageTier": "HDD",
              }
            ],
          "isSecureBooted": false,
          "isHardwareVirtualized": false,
          "hasCsr": false,
          "numberOfCpuCores": 16,
          "numberOfCpuThreads": 32,
          "numberOfCpuSockets": 2,
          "cpuFrequencyHz": 2100000000,
          "cpuModel": "Model_Name",
          "bootTimeUsecs": 1720164675311071,
          "memorySizeBytes": 269813284864,
          "blockSerial": "128MSLLI",
          "blockModel": "NX-1065-G5",
          "maintenanceState": "normal",
          "nodeStatus": "NORMAL",
        }
ext_id:
    description:
        - The external ID of the host.
    type: str
    returned: always
    sample: af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching hosts info"
error:
    description: Error message if any.
    type: str
    returned: always
total_available_results:
    description:
        - The total number of available hosts in PC.
    type: int
    returned: when all hosts are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_host  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def get_host_by_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    clusters = get_clusters_api_instance(module)
    resp = get_host(module, clusters, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_hosts(module, result):
    clusters = get_clusters_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json("Failed creating query parameters for fetching hosts info")
    resp = None
    try:
        cluster_ext_id = module.params.get("cluster_ext_id")
        if not cluster_ext_id:
            resp = clusters.list_hosts(**kwargs)
        else:
            resp = clusters.list_hosts_by_cluster_id(
                clusterExtId=cluster_ext_id, **kwargs
            )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching hosts info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id") or module.params.get("name"):
        get_host_by_ext_id(module, result)
    else:
        get_hosts(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
