#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_aws_subnets_info_v2
short_description: Fetch AWS subnets (NC2A) info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch AWS subnets info in Nutanix Prism Central.
  - Fetch multiple AWS subnets info with/without using filters, limit, etc.
  - C(cluster_ext_id) is required — the AWS subnet catalogue is scoped to a single NC2A cluster.
  - The Nutanix v4 API exposes only a list endpoint for AWS subnets (no Get-by-ID).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View NC2 AWS Subnets) -
    Required Roles: Network Infra Admin, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - Prism Element / NC2A cluster UUID (maps to the C(X-Cluster-Id) header).
      - Required because the AWS subnet catalogue is always scoped to a single NC2A cluster.
    type: str
    required: true
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
- name: List all AWS subnets available to an NC2A cluster
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
  register: result
  ignore_errors: true

- name: List AWS subnets filtered by AWS VPC ID
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    filter: "vpcId eq 'vpc-0abc123def4567890'"
  register: result
  ignore_errors: true

- name: List AWS subnets with a limit
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    limit: 5
  register: result
  ignore_errors: true

- name: List all AWS subnets with fetch_all
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AWS subnets info v4 API.
    - It is a list of AWS subnets, with optional filter or limit.
  returned: always
  type: list
  sample:
    [
      {
          "annotation": null,
          "availability_zone": "us-west-2a",
          "cidr": "10.0.1.0/24",
          "cloud_type": "AWS",
          "ext_id": "a4d1e6cf-4a2c-4d38-b0f4-2f6cd3a5b8d1",
          "gateway_ip": "10.0.1.1",
          "links": null,
          "subnet_id": "subnet-0abc123def4567890",
          "tenant_id": null,
          "vpc_id": "vpc-0abc123def4567890"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available AWS subnets on the target NC2A cluster.
  returned: when all AWS subnets are fetched
  type: int
  sample: 3

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching AWS subnets info"

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
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_aws_subnets_api_instance,
)
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
    )

    return module_args


def get_aws_subnets(module, aws_subnets_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating AWS subnets info spec", **result)

    kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")

    try:
        resp = list_entities(
            aws_subnets_api.list_aws_subnets,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AWS subnets info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    aws_subnets_api = get_aws_subnets_api_instance(module)
    get_aws_subnets(module, aws_subnets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
