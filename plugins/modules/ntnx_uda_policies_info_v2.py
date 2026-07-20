#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_uda_policies_info_v2
short_description: Fetch User-Defined Alert (UDA) policies info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about UdaPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific UdaPolicy.
  - If C(ext_id) is not provided, list multiple UdaPolicy optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get UdaPolicy by ext_id) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
    - >-
      B(Get list of User-Defined Alert policies) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the User-Defined Alert policy.
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
- name: Get User-Defined Alert policy using ext_id
  nutanix.ncp.ntnx_uda_policies_info_v2:
    ext_id: "cf3d9d0d-27e4-4c66-9a52-9d19ce6d7b02"
  register: single_result

- name: List all User-Defined Alert policies
  nutanix.ncp.ntnx_uda_policies_info_v2:
  register: all_result

- name: List User-Defined Alert policies with filter
  nutanix.ncp.ntnx_uda_policies_info_v2:
    filter: "title eq 'vm_high_cpu_uda_policy'"
  register: filtered_result

- name: List User-Defined Alert policies with limit and orderby
  nutanix.ncp.ntnx_uda_policies_info_v2:
    limit: 2
    orderby: "lastUpdatedTime desc"
  register: limited_result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UdaPolicy info v4 API.
    - It can be a single UdaPolicy if external ID is provided.
    - List of multiple UdaPolicy if external ID is not provided with optional filter / limit / orderby / select / page.
  returned: always
  type: dict
  sample:
    {
      "created_by": "admin",
      "description": "Trigger warning alert when cluster CPU usage exceeds 80%",
      "entity_type": "cluster",
      "ext_id": "ff30d9de-0648-427b-bf2c-646ee8ec23cb",
      "filters": [
          {"ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2", "type": "CLUSTER"}
      ],
      "impact_types": ["PERFORMANCE"],
      "is_auto_resolved": true,
      "is_enabled": true,
      "is_expected_to_error_on_conflict": null,
      "last_updated_time": "2026-07-20T15:36:58.758223+00:00",
      "links": null,
      "policies_to_override": null,
      "policyId": "Ac89aa5ad-9b13-41a5-956f-3c622c904499",
      "related_policies": null,
      "tenant_id": null,
      "title": "vm_high_cpu_uda_policy_ansible_updated",
      "trigger_conditions": [
          {
              "condition": {
                  "metric_name": "hypervisor_cpu_usage_ppm",
                  "operator": "GREATER_THAN",
                  "threshold_value": {"int_value": 800000}
              },
              "condition_type": "STATIC_THRESHOLD",
              "severity_level": "WARNING"
          }
      ],
      "trigger_wait_period": 900
    }

changed:
  description: This indicates whether the task resulted in any changes (always false for info modules).
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching User-Defined Alert policies info"

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the User-Defined Alert policy (only when a single entity is fetched).
  returned: When external ID is provided
  type: str
  sample: "cf3d9d0d-27e4-4c66-9a52-9d19ce6d7b02"

total_available_results:
  description: Total number of User-Defined Alert policies available on the PC.
  returned: When listing policies
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_user_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_uda_policy  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_uda_policy_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_uda_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def get_uda_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating User-Defined Alert policies info spec", **result
        )

    try:
        resp = api_instance.list_uda_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching User-Defined Alert policies info",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
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
    api_instance = get_user_defined_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_uda_policy_by_ext_id(module, api_instance, result)
    else:
        get_uda_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
