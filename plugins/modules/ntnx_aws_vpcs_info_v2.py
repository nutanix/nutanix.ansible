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
  - List AWS VPCs for the target NC2A cluster, optionally projecting fields with C(select).
  - C(cluster_ext_id) is required — the AWS VPC catalogue is scoped to a single NC2A cluster.
  - The Nutanix v4 API exposes only a list endpoint for AWS VPCs (no Get-by-ID and no
    OData query parameters such as filter, limit, page, orderby, or fetch_all).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View NC2 AWS VPC) -
    Required Roles: Network Infra Admin, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - Prism Element / NC2A cluster UUID (maps to the C(X-Cluster-Id) header).
      - Required because the AWS VPC catalogue is always scoped to a single NC2A cluster.
    type: str
    required: true
  select:
    description:
      - An OData V4.01 conformant C($select) query parameter that lets the client request a
        specific subset of properties per entity.
      - Expression specified with the C($select) must conform to the OData V4.01 URL conventions.
      - If a C($select) expression consists of a single select item that is an asterisk (i.e., C(*)),
        then all properties on the matching resource will be returned.
    type: str
    required: false
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

- name: List AWS VPCs with selected attributes
  nutanix.ncp.ntnx_aws_vpcs_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    select: "extId,vpcId,cidrs"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AWS VPCs info v4 API.
    - It is a list of AWS VPCs, optionally projected with C(select).
  returned: always
  type: list
  sample:
    [
      {
          "annotation": null,
          "cidrs": ["10.0.0.0/16"],
          "cloud_type": "AWS",
          "ext_id": "vpc-0a1b2c3d4e5f67890",
          "links": null,
          "tenant_id": null,
          "vpc_id": "vpc-0a1b2c3d4e5f67890"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

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
        select=dict(type="str"),
    )

    return module_args


def get_aws_vpcs(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating AWS VPCs info spec", **result)

    kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")

    try:
        resp = list_entities(
            api_instance.list_aws_vpcs,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AWS VPCs info",
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
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_aws_vpcs_api_instance(module)
    get_aws_vpcs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
