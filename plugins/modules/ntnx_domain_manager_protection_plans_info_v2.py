#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_domain_manager_protection_plans_info_v2
short_description: Fetch domain manager protection plans info
version_added: "2.7.0"
description:
    - This module allows you to fetch information about domain manager
      protection plans in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific domain manager
      protection plan.
    - If C(ext_id) is not provided, list multiple domain manager protection
      plans optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get domain manager protection plan by ext_id) -
      Required Roles: Super Admin, Prism Admin, Domain Manager Viewer,
      Domain Manager Admin
    - >-
      B(List domain manager protection plans) -
      Required Roles: Super Admin, Prism Admin, Domain Manager Viewer,
      Domain Manager Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    ext_id:
        description:
            - The external ID of the domain manager protection plan.
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
- name: Fetch domain manager protection plans info
  hosts: localhost
  gather_facts: false
  module_defaults:
    group/nutanix.ncp.ntnx:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
  tasks:
    - name: Get domain manager protection plan using ext_id
      nutanix.ncp.ntnx_domain_manager_protection_plans_info_v2:
        ext_id: "11111111-1111-1111-1111-111111111111"
      register: result
      ignore_errors: true

    - name: List all domain manager protection plans
      nutanix.ncp.ntnx_domain_manager_protection_plans_info_v2:
      register: result
      ignore_errors: true

    - name: List domain manager protection plans with filter
      nutanix.ncp.ntnx_domain_manager_protection_plans_info_v2:
        filter: "domainManagerExtId eq '00000000-0000-0000-0000-000000000001'"
      register: result
      ignore_errors: true

    - name: List domain manager protection plans with limit
      nutanix.ncp.ntnx_domain_manager_protection_plans_info_v2:
        limit: 1
      register: result
      ignore_errors: true

    - name: List all domain manager protection plans with fetch_all
      nutanix.ncp.ntnx_domain_manager_protection_plans_info_v2:
        fetch_all: true
      register: result
      ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - The response from the Nutanix domain manager protection plan info v4
        API
      - It can be a single domain manager protection plan if External ID is
        provided.
      - List of multiple domain manager protection plan if External ID is not
        provided with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    {
        "domain_manager_ext_id": "00000000-0000-0000-0000-000000000001",
        "ext_id": "11111111-1111-1111-1111-111111111111",
        "failover_network_details": {
            "network_ext_id": "00000000-0000-0000-0000-000000000003"
        },
        "remote_location": {
            "ext_id": "00000000-0000-0000-0000-000000000002",
            "name": "remote-cluster"
        },
        "remote_site": {
            "cluster_type": "AOS",
            "external_address": {
                "ipv4": {
                    "value": "10.0.0.10"
                }
            },
            "name": "remote-pc-cluster",
            "port": 9440
        },
        "status": "SYNCED"
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
  sample: "Api Exception raised while fetching domain manager protection plans info"

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
  description: External ID of the domain manager protection plan
  type: str
  returned: when external ID is provided
  sample: "11111111-1111-1111-1111-111111111111"

total_available_results:
  description: The total number of available domain manager protection plans in PC.
  type: int
  returned: when all domain manager protection plans are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import (  # noqa: E402
    get_domain_manager_protection_plan,
)
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_protection_plan_api_instance,
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
        ext_id=dict(type="str"),
    )

    return module_args


def get_domain_manager_protection_plan_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_domain_manager_protection_plan(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_domain_manager_protection_plans(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating domain manager protection plans info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_domain_manager_protection_plans,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching domain manager protection plans info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data") or []
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
    api_instance = get_domain_manager_protection_plan_api_instance(module)
    if module.params.get("ext_id"):
        get_domain_manager_protection_plan_using_ext_id(module, api_instance, result)
    else:
        get_domain_manager_protection_plans(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
