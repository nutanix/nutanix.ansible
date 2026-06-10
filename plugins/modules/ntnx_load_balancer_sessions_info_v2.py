#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_load_balancer_sessions_info_v2
short_description: Fetch load balancer sessions info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch load balancer sessions in Nutanix Prism Central.
  - If ext_id is provided, fetch particular load balancer session info using external ID.
  - If ext_id is not provided, fetch multiple load balancer sessions info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a Load Balancer Session) -
      Required Roles: Account Owner, Administrator, Prism Admin, Prism Viewer, Super Admin, User, VPC Admin
    - >-
      B(List Load Balancer Sessions) -
      Required Roles: Account Owner, Administrator, Prism Admin, Prism Viewer, Super Admin, User, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external identifier of the load balancer session.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Get load balancer session using ext_id
  nutanix.ncp.ntnx_load_balancer_sessions_info_v2:
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: List all load balancer sessions
  nutanix.ncp.ntnx_load_balancer_sessions_info_v2:
  register: result
  ignore_errors: true

- name: List load balancer sessions with filter
  nutanix.ncp.ntnx_load_balancer_sessions_info_v2:
    filter: "name eq 'load_balancer_session_name'"
  register: result
  ignore_errors: true

- name: List load balancer sessions with limit
  nutanix.ncp.ntnx_load_balancer_sessions_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - Response for fetching load balancer sessions info
    - Specific load balancer session info if External ID is provided
    - List of multiple load balancer sessions info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
      "algorithm": "FIVE_TUPLE_HASH",
      "description": "ansible test updated",
      "ext_id": "b83e9fc6-dfba-48d1-8319-fe208be30238",
      "health_check_config": {
          "failure_threshold": 12,
          "interval_secs": 13,
          "success_threshold": 10,
          "timeout_secs": 14
      },
      "links": null,
      "listener": {
          "port_ranges": [
              {
                  "end_port": 105,
                  "start_port": 100
              }
          ],
          "protocol": "TCP",
          "virtual_ip": {
              "assignment_type": "DYNAMIC",
              "ip_address": {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "192.168.1.100"
                  },
                  "ipv6": null
              },
              "subnet_reference": "a40c3403-9f4c-4205-8506-64f524545be4"
          }
      },
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": null,
          "project_reference_id": null
      },
      "name": "YHjdsObUDrBeansible-lbs_updated",
      "targets_config": {
          "category_targets": null,
          "nic_targets": [
              {
                  "health": "UNHEALTHY",
                  "port": 1080,
                  "virtual_nic_reference": "34ed7568-8d2d-40a6-a702-0d27fe33c536",
                  "vm_reference": "6238f063-fda8-461f-5ed2-ad6b7f32875f"
              }
          ]
      },
      "tenant_id": null,
      "type": "NETWORK_LOAD_BALANCER",
      "vpc_reference": "ff1c27f0-1f10-42f6-8ffc-45f3179c4bff"
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
  sample: "Api Exception raised while fetching load balancer sessions info"

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
  description: External ID of the load balancer session
  type: str
  returned: when external ID is provided
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

total_available_results:
  description: The total number of available load balancer sessions in PC.
  type: int
  returned: when all load balancer sessions are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_load_balancer_sessions_api_instance,
)
from ..module_utils.v4.network.helpers import get_load_balancer_session  # noqa: E402
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


def get_load_balancer_session_using_ext_id(module, load_balancer_sessions, result):
    ext_id = module.params.get("ext_id")
    resp = get_load_balancer_session(module, load_balancer_sessions, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_load_balancer_sessions(module, load_balancer_sessions, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating load balancer sessions info spec", **result
        )

    try:
        resp = load_balancer_sessions.list_load_balancer_sessions(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching load balancer sessions info",
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
    result = {"changed": False, "response": None}
    load_balancer_sessions = get_load_balancer_sessions_api_instance(module)
    if module.params.get("ext_id"):
        get_load_balancer_session_using_ext_id(module, load_balancer_sessions, result)
    else:
        get_load_balancer_sessions(module, load_balancer_sessions, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
