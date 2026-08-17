#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_aws_subnets_info_v2
short_description: Fetch AWS subnets (NC2A) info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch information about AwsSubnet in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific AwsSubnet.
  - If C(ext_id) is not provided, list multiple AwsSubnet optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List NC2A subnets) -
    Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin,
    Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of a specific AWS subnet mapping to fetch.
      - When set, the module fetches only the AWS subnet whose C(extId) matches this value.
      - The underlying v4.3 API only exposes a list endpoint, so this filter is applied
        using an OData C($filter=extId eq '...') expression on top of the list call.
    type: str
    required: false
  cluster_ext_id:
    description:
      - Prism Element / NC2A cluster UUID.
      - Passed as the required C(X-Cluster-Id) header on the underlying
        C(GET /networking/v4.3/aws/config/subnets) API.
      - Required for every invocation of this info module because the AWS subnet
        catalogue is always scoped to a single NC2A cluster.
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

- name: Fetch a specific AWS subnet by ext_id
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    ext_id: "a4d1e6cf-4a2c-4d38-b0f4-2f6cd3a5b8d1"
  register: result

- name: List AWS subnets filtered by AWS VPC ID
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    filter: "vpcId eq 'vpc-0abc123def4567890'"
  register: result

- name: List first 5 AWS subnets ordered by CIDR
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    limit: 5
    orderby: "cidr"
  register: result

- name: Page through AWS subnets and select a subset of fields
  nutanix.ncp.ntnx_aws_subnets_info_v2:
    cluster_ext_id: "0005f9f2-1c1c-9d68-0000-000000012345"
    page: 0
    limit: 10
    select: "subnetId,cidr,availabilityZone,cloudType"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AwsSubnet info v4 API.
    - It can be a single AwsSubnet if external ID is provided.
    - It is a list of multiple AwsSubnet if external ID is not provided, optionally
      filtered by C(filter), C(limit), C(page), C(orderby), C(select).
  returned: always
  type: dict
  sample:
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

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the AWS subnet, echoed back when the caller filters by C(ext_id).
  returned: when external ID is provided
  type: str
  sample: "a4d1e6cf-4a2c-4d38-b0f4-2f6cd3a5b8d1"

total_available_results:
  description: The total number of AWS subnets available on the target NC2A cluster (from the list response metadata).
  returned: when all AWS subnets are fetched (no C(ext_id))
  type: int
  sample: 3

msg:
  description: Human-readable status/error message. Populated on error or when an C(ext_id) lookup returns no match.
  returned: When there is an error or when no AWS subnet matches the provided C(ext_id)
  type: str
  sample: "No AWS subnet with ext_id 'a4d1e6cf-4a2c-4d38-b0f4-2f6cd3a5b8d1' was found on cluster '0005f9f2-1c1c-9d68-0000-000000012345'."

error:
  description: Error details returned by the SDK when the underlying API call fails.
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
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the argument spec for this info module.

    The list_aws_subnets SDK signature is:
        list_aws_subnets(X_Cluster_Id, _page=None, _limit=None,
                        _filter=None, _orderby=None, _select=None)

    The pagination/query params (page, limit, filter, orderby, select) come
    from the info fragment (see BaseInfoModule.info_argument_spec). Only the
    entity-specific options are declared here.
    """

    module_args = dict(
        ext_id=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=True),
    )

    return module_args


def _build_list_kwargs(module, extra_filter=None):
    """Assemble the OData/query kwargs passed to list_aws_subnets."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        return None, err

    if extra_filter:
        existing = kwargs.get("_filter")
        if existing:
            kwargs["_filter"] = "{0} and {1}".format(existing, extra_filter)
        else:
            kwargs["_filter"] = extra_filter

    kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")
    return kwargs, None


def get_aws_subnet_using_ext_id(module, aws_subnets_api, result):
    """Fetch a single AWS subnet by ext_id.

    The AwsSubnetsApi only exposes a list endpoint, so we hit the list API
    with an OData filter on ``extId`` and return the (at most one) match.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    kwargs, err = _build_list_kwargs(
        module, extra_filter="extId eq '{0}'".format(ext_id)
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating AWS subnet info spec", **result)

    try:
        resp = aws_subnets_api.list_aws_subnets(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AWS subnet info by ext_id",
        )

    stripped = strip_internal_attributes(resp.to_dict())
    data = stripped.get("data") or []
    if not data:
        result["response"] = {}
        result["msg"] = (
            "No AWS subnet with ext_id '{0}' was found on cluster '{1}'.".format(
                ext_id, module.params.get("cluster_ext_id")
            )
        )
        return

    result["response"] = data[0]


def get_aws_subnets(module, aws_subnets_api, result):
    """List AWS subnets scoped to the target NC2A cluster."""
    kwargs, err = _build_list_kwargs(module)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating AWS subnets info spec", **result)

    try:
        resp = aws_subnets_api.list_aws_subnets(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AWS subnets info",
        )

    stripped = strip_internal_attributes(resp.to_dict())
    metadata = stripped.get("metadata") or {}
    result["total_available_results"] = metadata.get("total_available_results")

    data = stripped.get("data")
    if not data:
        data = []
    result["response"] = data


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
    aws_subnets_api = get_aws_subnets_api_instance(module)
    if module.params.get("ext_id"):
        get_aws_subnet_using_ext_id(module, aws_subnets_api, result)
    else:
        get_aws_subnets(module, aws_subnets_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
