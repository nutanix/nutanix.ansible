#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_summaries_info_v2
short_description: Fetch LCM (Life Cycle Manager) summaries info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about LcmSummary in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific LcmSummary.
  - If C(ext_id) is not provided, list multiple LcmSummary optionally filtered / paginated.
  - The LCM summary is a cluster wide, read-only snapshot that is refreshed
    after every inventory or upgrade operation.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get LCM summary by ext_id) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List LCM summaries) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the LCM summary (cluster UUID).
      - If provided, fetch a single LCM summary entity.
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
- name: List all LCM summaries
  nutanix.ncp.ntnx_lcm_summaries_info_v2:
  register: lcm_summaries
  ignore_errors: true

- name: List LCM summaries with a limit of 1
  nutanix.ncp.ntnx_lcm_summaries_info_v2:
    limit: 1
  register: lcm_summaries_limited
  ignore_errors: true

- name: List LCM summaries filtered by hasAvailableUpgrades=true
  nutanix.ncp.ntnx_lcm_summaries_info_v2:
    filter: "hasAvailableUpgrades eq true"
  register: upgradable_summaries
  ignore_errors: true

- name: Fetch a specific LCM summary using external ID
  nutanix.ncp.ntnx_lcm_summaries_info_v2:
    ext_id: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
  register: single_lcm_summary
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LcmSummary info v4 API.
    - It can be a single LcmSummary if external ID is provided.
    - List of multiple LcmSummary if external ID is not provided
      with optional filter, limit, orderby, select or pagination.
  returned: always
  type: dict
  sample:
    {
      "available_version": "3.3.1.1.79152",
      "capabilities": [
        "MCL_INVENTORY",
        "TARGETED_INVENTORY",
        "MCL_UPGRADE",
        "MCL_UNIFIED_UPLOADS"
      ],
      "cluster_ext_id": "cae459ec-08db-475e-a5e5-151e390c9484",
      "cluster_type": "PRISM_CENTRAL",
      "compatibility_bundle_version": null,
      "connectivity_type": "CONNECTED_SITE",
      "current_version": "3.4.86535",
      "ext_id": "cae459ec-08db-475e-a5e5-151e390c9484",
      "hardware_vendor": null,
      "in_progress_operation": null,
      "is_url_accessible": true,
      "links": null,
      "restricted_mode_type": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the LCM summary (cluster UUID).
  type: str
  returned: when external ID is provided
  sample: "cae459ec-08db-475e-a5e5-151e390c9484"

total_available_results:
  description: The total number of available LCM summaries in PC.
  type: int
  returned: when all LCM summaries are fetched
  sample: 2

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching LCM summaries info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: When an error occurs
  sample: "Failed generating LCM summaries info spec"

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_lcm_summaries_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_summary  # noqa: E402
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


def get_lcm_summary_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_summary(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_lcm_summaries(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating LCM summaries info spec", **result)

    try:
        resp = api_instance.list_lcm_summaries(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM summaries info",
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

    api_instance = get_lcm_summaries_api_instance(module)
    if module.params.get("ext_id"):
        get_lcm_summary_using_ext_id(module, api_instance, result)
    else:
        get_lcm_summaries(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
