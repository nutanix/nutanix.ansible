#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_cvms_info_v2
short_description: Fetch information about Controller VMs (CVMs) of a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to fetch information about CvmsbyClusterId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific CvmsbyClusterId.
  - If C(ext_id) is not provided, list multiple CvmsbyClusterId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get the list of CVMs of a cluster) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(Get CVM by ext_id) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose CVMs are to be fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of a specific CVM to fetch.
      - When provided, only the matching CVM is returned.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all CVMs of a cluster
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: Fetch a specific CVM by external ID
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "1bfd91f2-1b8e-4c62-9d20-9b1c5e46d5a6"
  register: result
  ignore_errors: true

- name: List CVMs of a cluster with limit
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    limit: 1
  register: result
  ignore_errors: true

- name: List CVMs of a cluster with filter
  nutanix.ncp.ntnx_cluster_cvms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    filter: "numVcpus eq 8"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC CvmsbyClusterId info v4 API.
    - It can be a single CvmsbyClusterId if external ID is provided.
    - List of multiple CvmsbyClusterId if external ID is not provided with optional filter or limit.
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
  description: This indicates whether the info module resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message returned by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching CVMs info"

error:
  description: Error details when an API/SDK error is raised.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the module failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external ID of the CVM, only when fetching by external ID.
  type: str
  returned: when external ID is provided
  sample: "f83f7ea6-4d56-5db6-8ebf-fb3157870d33"

total_available_results:
  description:
    - The total number of CVMs available on the target cluster.
  type: int
  returned: when all CVMs of the cluster are fetched
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_cvm_by_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_cvm(module, api_instance, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cvms_by_cluster_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for fetching CVMs info", **result)

    resp = None
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
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_cvms_api_instance(module)
    if module.params.get("ext_id"):
        get_cvm_by_ext_id(module, api_instance, result)
    else:
        get_cvms_by_cluster_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
