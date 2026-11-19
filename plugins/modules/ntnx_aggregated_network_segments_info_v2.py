#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_aggregated_network_segments_info_v2
short_description: Fetch aggregated network segments info
version_added: "2.7.0"
description:
  - This module allows you to fetch information about aggregated network segments in Nutanix Prism Central.
  - It lists multiple aggregated network segments optionally filtered or paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(View Aggregated Network Segment) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
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
- name: List aggregated network segments
  nutanix.ncp.ntnx_aggregated_network_segments_info_v2:
  register: result
  ignore_errors: true

- name: List aggregated network segments with filter
  nutanix.ncp.ntnx_aggregated_network_segments_info_v2:
    filter: "name eq 'segment1'"
  register: result
  ignore_errors: true

- name: List aggregated network segments with limit
  nutanix.ncp.ntnx_aggregated_network_segments_info_v2:
    limit: 5
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC aggregated network segments info v4 API.
    - List of aggregated network segments.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
        "name": "segment1",
        "vlan_id": 100
    }
changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching aggregated network segments"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs
failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
total_available_results:
  description: The total number of available aggregated network segments matching the query.
  type: int
  returned: When a list call is made.
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_network_segments_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict()


def list_aggregated_network_segments(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating aggregated network segments info spec", **result
        )
    try:
        resp = list_entities(
            api_instance.list_aggregated_network_segments, kwargs=kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching aggregated network segments",
        )
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(argument_spec=get_module_spec(), supports_check_mode=False)
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_network_segments_api_instance(module)
    list_aggregated_network_segments(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
