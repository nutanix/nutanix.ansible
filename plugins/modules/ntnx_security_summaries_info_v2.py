#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_summaries_info_v2
short_description: Fetch security summaries of the ecosystem in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about SecuritySummary in Nutanix Prism Central.
  - SecuritySummary provides the overall security status of the ecosystem, aggregating
    STIG (Security Technical Implementation Guide), vulnerability, security configuration
    and password issue statistics for each cluster managed by Prism Central.
  - The list API supports optional pagination (C(page), C(limit)), filtering (C(filter))
    using OData V4.01 conventions, ordering (C(orderby)), field selection (C(select))
    and expanding related resources (C(expand)).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List Security Summaries) -
      Required Roles: Prism Admin, Prism Viewer, Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
  expand:
    description:
      - A URL query parameter that allows clients to request related resources when a
        resource that satisfies a particular request is retrieved.
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
- name: List all security summaries in Prism Central
  nutanix.ncp.ntnx_security_summaries_info_v2:
  register: result
  ignore_errors: true

- name: List security summaries with a filter on clusterExtId
  nutanix.ncp.ntnx_security_summaries_info_v2:
    filter: "clusterExtId eq '00000000-0000-0000-0000-000000000000'"
  register: result_filter
  ignore_errors: true

- name: List security summaries with a limit
  nutanix.ncp.ntnx_security_summaries_info_v2:
    limit: 1
  register: result_limit
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SecuritySummary info v4 API.
    - List of multiple SecuritySummary optionally filtered / paginated.
  returned: always
  type: dict
  sample:
    [
      {
        "cluster_ext_id": "00063e6e-18f3-aefb-0ace-e59ff1cc2885",
        "ext_id": "00063e6e-18f3-aefb-0ace-e59ff1cc2885",
        "last_refresh_time": "2026-07-20T10:15:00+00:00",
        "links": null,
        "password_summary": {
          "current_issue_count": 0,
          "trends": null
        },
        "security_config_summary": {
          "current_issue_count": 0,
          "is_cluster_lockdown_enabled": false,
          "is_consent_banner_enabled": false,
          "is_log_forwarding_enabled": false,
          "is_secure_boot_enabled": false,
          "trends": null
        },
        "stig_summary": {
          "current_issue_count": 0,
          "trends": null
        },
        "tenant_id": null,
        "trend_type": null,
        "vulnerabilities_summary": {
          "current_issue_count": 0,
          "trends": null,
          "vulnerability_details": null
        }
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching security summaries info"

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
  description: The total number of available security summaries in PC.
  type: int
  returned: when all security summaries are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_security_summaries_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        expand=dict(type="str"),
    )
    return module_args


def list_security_summaries(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating security summaries info spec", **result)

    try:
        resp = api_instance.list_security_summaries(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching security summaries info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "error": None}
    api_instance = get_security_summaries_api_instance(module)
    list_security_summaries(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
