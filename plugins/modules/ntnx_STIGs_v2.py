#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_STIGs_v2
short_description: Fetch STIG rule details and issue counts for each cluster
version_added: 2.4.0
description:
  - The Security Technical Implementation Guide (STIG) is a configuration standard consisting of cybersecurity requirements for a specific product.
  - Fetch the current number of issues found by STIG for each cluster.
  - Fetch the STIG controls details for STIG rules on each cluster if C(stig_details) is true.
  - This module uses PC v4 APIs based SDKs
options:
  stig_details:
    description:
      - Whether to fetch detailed STIG control information.
      - If true, detailed information about each STIG control will be retrieved.
    type: bool
    default: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch summary report for the current number of issues found by STIG for each cluster.
  nutanix.ncp.ntnx_STIGs_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    stig_summary: true
  register: result

- name: Fetch detailed STIG control information for each cluster.
  nutanix.ncp.ntnx_STIGs_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    stig_details: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching STIG details.
        - A list of STIG control details for each cluster.
        - If C(stig_details) is true, it will contain detailed information about each STIG control.
        - If C(stig_details) is false or not provided, it will contain a summary of STIG issues.
    type: dict
    returned: always
    sample:
      [
        {
          "cluster_ext_id": "00063a1c-a953-2048-0000-000000028f57",
          "ext_id": "7c38080b-feec-4098-5cb3-5c4acc6e6f64",
          "failed_count": 17,
          "links": null,
          "not_applicable_count": 46,
          "passed_count": 68,
          "tenant_id": null
        }
      ]
changed:
    description: Indicates if any changes were made by the module.
    type: bool
    returned: always
    sample: false
failed:
    description: Indicates if the module execution failed.
    type: bool
    returned: always
    sample: false
error:
    description: Error message if any.
    type: str
    returned: always
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import get_stigs_api_instance  # noqa: E402
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_stig_controls_details,
    get_stig_summary,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(stig_details=dict(type="bool", default=False))
    return module_args


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    stig_api_instance = get_stigs_api_instance(module)
    resp = None
    if module.params.get("stig_details"):
        resp = get_stig_controls_details(module, stig_api_instance)
    else:
        resp = get_stig_summary(module, stig_api_instance)
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
