#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_csr_info_v2
short_description: Fetch Certificate Signing Request (CSR) info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module fetches Certificate Signing Request (CSR) information for a cluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular CSR using its external ID.
  - If C(ext_id) is not provided, fetch a list of CSRs for the cluster with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Cluster Certificate Signing Request) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - The referenced cluster must exist before fetching CSR information from it.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster to fetch CSR information from.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the Certificate Signing Request.
      - When provided, a single CSR is returned.
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
- name: Get a Certificate Signing Request using ext_id
  nutanix.ncp.ntnx_csr_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: List Certificate Signing Requests with filter
  nutanix.ncp.ntnx_csr_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    filter: "purpose eq 'SERVER_AUTH'"
  register: result
  ignore_errors: true

- name: List Certificate Signing Requests with limit
  nutanix.ncp.ntnx_csr_info_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the CSR info v4 API. The host is Prism Central (PC).
    - It can be a single CSR if external ID is provided.
    - List of multiple CSRs if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "certificate_info": {
        "city": "San Jose",
        "common_name": "ansible.nutanix.com",
        "country_code": "US",
        "private_key_algorithm": "RSA_2048",
        "state": "California"
      },
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "links": null,
      "purpose": "SERVER_AUTH",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching CSR info"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the fetched Certificate Signing Request.
  type: str
  returned: when external ID is provided
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

cluster_ext_id:
  description: External ID of the cluster whose CSRs were queried.
  type: str
  returned: always
  sample: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"

total_available_results:
  description: The total number of available Certificate Signing Requests on the cluster.
  type: int
  returned: when all entities are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_certificate_manager_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_csr  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
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


def get_csr_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = ext_id
    result["cluster_ext_id"] = cluster_ext_id

    resp = get_csr(module, api_instance, ext_id, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_csrs(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating CSR info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_csrs_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching CSR info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


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
    api_instance = get_certificate_manager_api_instance(module)
    if module.params.get("ext_id"):
        get_csr_using_ext_id(module, api_instance, result)
    else:
        get_csrs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
