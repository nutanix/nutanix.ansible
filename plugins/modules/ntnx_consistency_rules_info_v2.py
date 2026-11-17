#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_consistency_rules_info_v2
short_description: Fetch Consistency Rules info in a Nutanix Protection Policy
version_added: "2.7.0"
description:
    - This module allows you to fetch information about Consistency Rules in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific Consistency Rule.
    - If C(ext_id) is not provided, list multiple Consistency Rules optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get Consistency Rule by ext_id) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin,
      Prism Viewer, Project Manager, Super Admin
    - >-
      B(List Consistency Rules) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin,
      Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
    protection_policy_ext_id:
        description:
            - The External ID of the parent Protection Policy whose Consistency Rules
              you want to query.
        type: str
        required: true
    ext_id:
        description:
            - The External ID of the Consistency Rule.
            - If provided, only that particular Consistency Rule is fetched.
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
- name: Get Consistency Rule using ext_id
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    ext_id: "63311404-8b2e-4dbf-9e33-7848cc88d330"
  register: result

- name: List all Consistency Rules of a Protection Policy
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
  register: result

- name: List Consistency Rules with filter
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    filter: "name eq 'example-consistency-rule'"
  register: result

- name: List Consistency Rules with limit
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    limit: 1
  register: result

- name: List all Consistency Rules with fetch_all
  nutanix.ncp.ntnx_consistency_rules_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    protection_policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Consistency Rules info v4 API.
        - It can be a single Consistency Rule if External ID is provided.
        - List of multiple Consistency Rules if External ID is not provided with optional filter or limit.
    returned: always
    type: dict
    sample: {}
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: always
    type: bool
    sample: false
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching consistency rules info"
ext_id:
    description: External ID of the Consistency Rule.
    type: str
    returned: when External ID is provided
    sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
total_available_results:
    description: The total number of available Consistency Rules under the given Protection Policy.
    type: int
    returned: when Consistency Rules are listed
    sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_consistency_rules_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_consistency_rule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        protection_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
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
        resp = list_entities(
            api_instance.list_consistency_rules_by_protection_policy_id,
            protectionPolicyExtId=protection_policy_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching consistency rules info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    api_instance = get_consistency_rules_api_instance(module)
    if module.params.get("ext_id"):
        get_consistency_rule_using_ext_id(module, api_instance, result)
    else:
        get_consistency_rules(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
