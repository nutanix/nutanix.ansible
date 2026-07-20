#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_plans_info_v2
short_description: Fetch recovery plans info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about RecoveryPlan in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RecoveryPlan.
  - If C(ext_id) is not provided, list multiple RecoveryPlan optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs (namespace C(datapolicies)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get recovery plan by ext_id) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List recovery plans) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  ext_id:
    description:
      - The external ID of the recovery plan.
      - When set, only the referenced recovery plan is returned.
    type: str
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
- name: Get recovery plan using ext_id
  nutanix.ncp.ntnx_recovery_plans_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
  register: result

- name: List all recovery plans
  nutanix.ncp.ntnx_recovery_plans_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List recovery plans with filter
  nutanix.ncp.ntnx_recovery_plans_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'recovery_plan_name'"
  register: result

- name: List recovery plans with limit
  nutanix.ncp.ntnx_recovery_plans_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RecoveryPlan info v4 API.
    - It can be a single RecoveryPlan if external ID is provided.
    - List of multiple RecoveryPlan if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "description": "Recovery plan created by Ansible",
      "ext_id": "e7ae4b0d-726d-410d-87c2-af46f8bea264",
      "is_protection_paused_post_failover": null,
      "links": null,
      "name": "recovery_plan_ansible",
      "num_network_mappings": 0,
      "num_stages": 0,
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "primary_location":
        {
          "clusters":
            [
              { "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57", "name": null }
            ],
          "domain_manager_ext_id": "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f",
          "project_ext_id": null
        },
      "project_ext_id": null,
      "recovery_location":
        {
          "clusters":
            [
              { "ext_id": "000649c4-1a2b-1234-5678-000000012345", "name": null }
            ],
          "domain_manager_ext_id": "425cd2d4-32e0-4c2d-a026-31d81fa4c805",
          "project_ext_id": null
        },
      "tenant_id": null,
      "witness": null,
      "witness_configuration": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching recovery plans info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the recovery plan.
  type: str
  returned: when external ID is provided
  sample: "e7ae4b0d-726d-410d-87c2-af46f8bea264"

total_available_results:
  description: The total number of available recovery plans in PC.
  type: int
  returned: when all recovery plans are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_recovery_plan  # noqa: E402
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
    )

    return module_args


def get_recovery_plan_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_recovery_plan(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_recovery_plans(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating recovery plans info spec", **result)

    try:
        resp = api_instance.list_recovery_plans(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery plans info",
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
    api_instance = get_recovery_plans_api_instance(module)
    if module.params.get("ext_id"):
        get_recovery_plan_using_ext_id(module, api_instance, result)
    else:
        get_recovery_plans(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
