#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_aws_vpcs_info_v2
short_description: Fetch AWS VPCs (NC2A) info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch AWS VPCs info in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular AWS VPC using client-side filtering
    of the list response (there is no Get-by-ID API).
  - If C(ext_id) is not provided, list AWS VPCs for the target NC2A cluster.
  - C(cluster_ext_id) is required — the AWS VPC catalogue is scoped to a single NC2A cluster.
  - The Nutanix v4 API exposes only a list endpoint for AWS VPCs (no Get-by-ID and no
    OData query parameters such as filter, limit, page, orderby, or select).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View NC2 AWS VPC) -
    Required Roles: Network Infra Admin, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the AWS VPC.
      - When provided, only the matching AWS VPC from the target cluster is returned.
      - AWS VPCs have no dedicated get-by-ID endpoint; this is applied as a client-side filter.
    type: str
  cluster_ext_id:
    description:
      - Prism Element / NC2A cluster UUID (maps to the C(X-Cluster-Id) header).
      - Required because the AWS VPC catalogue is always scoped to a single NC2A cluster.
    type: str
    required: true
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all AWS VPCs available to an NC2A cluster
  nutanix.ncp.ntnx_aws_vpcs_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: Fetch a specific AWS VPC by external ID
  nutanix.ncp.ntnx_aws_vpcs_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "vpc-0a1b2c3d4e5f67890"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AWS VPCs info v4 API.
    - It can be a single AWS VPC if external ID is provided.
    - It is a list of AWS VPCs if external ID is not provided.
  returned: always
  type: dict
  sample:
    {
      "annotation": null,
      "cidrs": ["10.0.0.0/16"],
      "cloud_type": "AWS",
      "ext_id": "vpc-0a1b2c3d4e5f67890",
      "links": null,
      "tenant_id": null,
      "vpc_id": "vpc-0a1b2c3d4e5f67890"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the AWS VPC.
  type: str
  returned: when external ID is provided
  sample: "vpc-0a1b2c3d4e5f67890"

total_available_results:
  description: The total number of available AWS VPCs on the target NC2A cluster.
  type: int
  returned: when all AWS VPCs are fetched
  sample: 3

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching AWS VPCs info"

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_aws_vpcs_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str", required=True),
    )

    return module_args


def _list_aws_vpcs(module, api_instance):
    kwargs = {"X_Cluster_Id": module.params.get("cluster_ext_id")}
    try:
        return list_entities(
            api_instance.list_aws_vpcs,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AWS VPCs info",
        )


def get_aws_vpc_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = _list_aws_vpcs(module, api_instance)

    stripped = strip_internal_attributes(resp.to_dict())
    entries = stripped.get("data") or []
    match = next((item for item in entries if item.get("ext_id") == ext_id), None)
    if match is None:
        module.fail_json(
            msg="AwsVpc with ext_id '{0}' not found on cluster '{1}'".format(
                ext_id, module.params.get("cluster_ext_id")
            ),
            failed=True,
            response=None,
            ext_id=ext_id,
        )

    result["ext_id"] = ext_id
    result["response"] = match


def get_aws_vpcs(module, api_instance, result):
    resp = _list_aws_vpcs(module, api_instance)

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
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_aws_vpcs_api_instance(module)
    if module.params.get("ext_id"):
        get_aws_vpc_by_ext_id(module, api_instance, result)
    else:
        get_aws_vpcs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
