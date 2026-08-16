#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_consistency_rules_info_v2
short_description: Fetch consistency rules info of a protection policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ConsistencyRule in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ConsistencyRule.
  - If C(ext_id) is not provided, list multiple ConsistencyRule optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get a Consistency Rule by ext_id) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List Consistency Rules) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  protection_policy_ext_id:
    description:
      - The external identifier of the parent Protection Policy.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the Consistency Rule.
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
- name: Fetch a consistency rule using external ID
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    ext_id: "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7"
  register: result
  ignore_errors: true

- name: List all consistency rules of a protection policy
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
  register: result
  ignore_errors: true

- name: List consistency rules with filter
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    filter: "name eq 'consistency_rule_ansible'"
  register: result
  ignore_errors: true

- name: List consistency rules with limit
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ConsistencyRule info v4 API.
    - It can be a single ConsistencyRule if external ID is provided.
    - List of multiple ConsistencyRule if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "category_ids": ["22222222-2222-2222-2222-222222222222"],
      "ext_id": "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7",
      "links": null,
      "name": "consistency_rule_ansible",
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
  sample: "Api Exception raised while fetching consistency rules info"

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
  description: External ID of the consistency rule
  type: str
  returned: when external ID is provided
  sample: "5c9a2d54-1f18-4f0e-b2b4-3a5cee0031b7"

total_available_results:
  description: The total number of available consistency rules under the specified protection policy.
  type: int
  returned: when all consistency rules are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_protection_policies_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_consistency_rule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        protection_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_consistency_rule_using_ext_id(module, api_instance, result):
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_consistency_rule(module, api_instance, protection_policy_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_consistency_rules(module, api_instance, result):
    protection_policy_ext_id = module.params.get("protection_policy_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating consistency rules info spec", **result)

    try:
        resp = api_instance.list_consistency_rules_by_protection_policy_id(
            protectionPolicyExtId=protection_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching consistency rules info",
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
    api_instance = get_protection_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_consistency_rule_using_ext_id(module, api_instance, result)
    else:
        get_consistency_rules(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
