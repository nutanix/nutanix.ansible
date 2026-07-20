#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vulnerabilities_info_v2
short_description: Fetch vulnerabilities from the Nutanix Vulnerability Database (NXVD) in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about vulnerabilities in Nutanix Prism Central.
  - Vulnerabilities are sourced from the Nutanix Vulnerability Database (NXVD) and represent
    genuine security issues affecting Nutanix products such as AOS, AHV and Prism Central.
  - Each record contains a CVE / CESA identifier, severity, list of fix versions and the
    NXVD version at which the vulnerability was published.
  - The list supports OData style pagination, filtering, ordering and field selection.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get the vulnerabilities information) -
      Required Roles: Prism Admin, Prism Viewer, Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
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
- name: Fetch all vulnerabilities from the Nutanix Vulnerability Database (NXVD).
  nutanix.ncp.ntnx_vulnerabilities_info_v2:
  register: result

- name: Fetch all vulnerabilities with a limit of one record.
  nutanix.ncp.ntnx_vulnerabilities_info_v2:
    limit: 1
  register: result_limit

- name: Fetch only HIGH severity vulnerabilities.
  nutanix.ncp.ntnx_vulnerabilities_info_v2:
    filter: "severity eq Security.Report.Severity'HIGH'"
  register: result_filter

- name: Fetch vulnerabilities ordered by severity (highest severities first).
  nutanix.ncp.ntnx_vulnerabilities_info_v2:
    orderby: "severity asc"
    limit: 5
  register: result_orderby

- name: Fetch only the ext_id and severity fields of every vulnerability.
  nutanix.ncp.ntnx_vulnerabilities_info_v2:
    select: "extId,severity"
    limit: 5
  register: result_select
"""

RETURN = r"""
response:
  description:
    - Response for fetching vulnerabilities information from the Nutanix Vulnerability Database (NXVD).
    - A list of vulnerability records; each record contains its severity, CVE/CESA identifiers
      and the list of software versions that fix the vulnerability.
  returned: always
  type: dict
  sample:
    [
      {
        "cesa_id": null,
        "cve_ids": ["CVE-2023-38408"],
        "description": null,
        "ext_id": "1858faea-dfed-4ef8-411f-d4af4a4e2367",
        "fix_versions": ["6.7.1", "6.5.4", "6.7.0.6"],
        "links": null,
        "nxvd_created_time": null,
        "nxvd_version": null,
        "severity": "CRITICAL",
        "tenant_id": null
      },
      {
        "cesa_id": "CESA-2019:2571",
        "cve_ids": ["CVE-2019-1010238"],
        "description": null,
        "ext_id": "b1190ef8-0da5-4455-7bdd-db39c9f523d5",
        "fix_versions": ["5.10.9", "5.16", "5.11.2"],
        "links": null,
        "nxvd_created_time": null,
        "nxvd_version": null,
        "severity": "CRITICAL",
        "tenant_id": null
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
  sample: "Api Exception raised while fetching vulnerabilities information"

error:
  description:
    - This field typically holds information about if the task have errors that
      occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available vulnerabilities in the Nutanix Vulnerability Database (NXVD).
  type: int
  returned: when all vulnerabilities are fetched
  sample: 277
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_vulnerabilities_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict()


def get_vulnerabilities(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating vulnerabilities info spec",
            **result  # fmt: skip
        )

    try:
        resp = api_instance.list_vulnerabilities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching vulnerabilities information",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "error": None, "response": None}
    api_instance = get_vulnerabilities_api_instance(module)
    get_vulnerabilities(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
