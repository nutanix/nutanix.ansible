#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_aws_vpcs_info_v2
short_description: Fetch NC2A (Nutanix Cloud Clusters on AWS) VPC info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about AwsVpc in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific AwsVpc from the target cluster.
  - If C(ext_id) is not provided, list multiple AwsVpc for the target cluster.
  - AwsVpc is a read-only listing surface (only the list API is available in the SDK);
    filtering by C(ext_id) is done client-side against the list response.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get NC2A VPCs) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the AwsVpc.
      - When provided, only the matching AwsVpc from the target cluster is returned.
      - AwsVpc has no dedicated get-by-ID endpoint; this is applied as a client-side filter.
    type: str
  cluster_ext_id:
    description:
      - The external ID (UUID) of the target NC2A Prism Element cluster whose AWS VPCs should be listed.
      - Required by the underlying list API which passes this value as the C(X-Cluster-Id) header.
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
- name: List all AWS VPCs discovered by an NC2A cluster
  nutanix.ncp.ntnx_aws_vpcs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: Fetch a specific AWS VPC by external ID
  nutanix.ncp.ntnx_aws_vpcs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "vpc-0a1b2c3d4e5f67890"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AwsVpc info v4 API.
    - It can be a single AwsVpc if external ID is provided.
    - List of multiple AwsVpc if external ID is not provided.
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

ext_id:
  description:
    - External ID of the AwsVpc.
  type: str
  returned: when external ID is provided
  sample: "vpc-0a1b2c3d4e5f67890"

total_available_results:
  description:
    - The total number of AwsVpc entries returned by the target cluster.
  type: int
  returned: when all AwsVpcs are fetched
  sample: 3

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: When an error occurs

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching AWS VPCs info"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import get_aws_vpcs_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
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
    cluster_ext_id = module.params.get("cluster_ext_id")
    try:
        return api_instance.list_aws_vpcs(X_Cluster_Id=cluster_ext_id)
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
    resp_dict = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp_dict:
        resp_dict = []
    result["response"] = resp_dict


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
