#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_cvms_info_v2
short_description: Fetch CVMs (Controller VMs) associated with a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to fetch information about CVMs (Controller VMs) associated with a cluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific CVM belonging to the given cluster.
  - If C(ext_id) is not provided, list all CVMs of the cluster optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get CVM by ext_id) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Cluster Admin
  - >-
    B(List CVMs of a cluster) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Cluster Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - External identifier (UUID) of the parent cluster whose CVMs should be fetched.
    type: str
    required: true
  ext_id:
    description:
      - External identifier of a specific CVM in the given cluster.
      - If provided, the module returns a single CVM; otherwise, it returns the list of CVMs for the cluster.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get CVM using ext_id
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    ext_id: "6a24ee94-8c26-4d10-9c60-6c67d4c47dc2"
  register: result
  ignore_errors: true

- name: List all CVMs of a cluster
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
  register: result
  ignore_errors: true

- name: List CVMs of a cluster with filter
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    filter: "startswith(name, 'NTNX-')"
  register: result
  ignore_errors: true

- name: List CVMs of a cluster with limit
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    limit: 1
  register: result
  ignore_errors: true

- name: List CVMs of a cluster with ordering
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    orderby: "name desc"
  register: result
  ignore_errors: true

- name: List CVMs of a cluster with selection
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    select: "name,extId,numVcpus,memorySizeBytes"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC CVM info v4 API.
    - It can be a single CVM if external ID is provided.
    - List of multiple CVMs of the cluster if external ID is not provided with optional filter, limit, orderby, select.
  returned: always
  type: dict
  sample:
    {
      "backplane_ip_address": null,
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "ext_id": "f83f7ea6-4d56-5db6-8ebf-fb3157870d33",
      "hypervisor_type": "AHV",
      "ip_address": {
        "ipv4": {
          "prefix_length": null,
          "value": "10.46.136.32"
        },
        "ipv6": null
      },
      "links": null,
      "memory_size_bytes": 25769803776,
      "name": "NTNX-goku-4-CVM",
      "node_ext_id": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
      "num_vcpus": 8,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching CVMs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the CVM
  type: str
  returned: when external ID is provided
  sample: "f83f7ea6-4d56-5db6-8ebf-fb3157870d33"

total_available_results:
  description: The total number of available CVMs for the cluster.
  type: int
  returned: when listing CVMs for a cluster
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cvms_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cvm  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_cvm_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_cvm(module, api_instance, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cvms(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating CVMs info spec", **result)

    try:
        resp = api_instance.list_cvmsby_cluster_id(
            clusterExtId=cluster_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching CVMs info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_cvms_api_instance(module)
    if module.params.get("ext_id"):
        get_cvm_using_ext_id(module, api_instance, result)
    else:
        get_cvms(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
