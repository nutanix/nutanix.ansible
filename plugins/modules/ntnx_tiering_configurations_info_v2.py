#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_tiering_configurations_info_v2
short_description: Fetch tiering configurations info for Nutanix Files in Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about TieringConfiguration in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific TieringConfiguration.
  - If C(ext_id) is not provided, list multiple TieringConfiguration optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the tiering configuration.
      - When provided, the module fetches a single tiering configuration for the given file server.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server the tiering configuration belongs to.
      - Required for all fetch/list operations.
    type: str
    required: true
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
- name: Fetch tiering configuration using external ID
  nutanix.ncp.ntnx_tiering_configurations_info_v2:
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
    ext_id: "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af"
  register: result
  ignore_errors: true

- name: List all tiering configurations for a file server
  nutanix.ncp.ntnx_tiering_configurations_info_v2:
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
  register: result
  ignore_errors: true

- name: List tiering configurations with filter
  nutanix.ncp.ntnx_tiering_configurations_info_v2:
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
    filter: "memoryThresholdPercent eq 80"
  register: result
  ignore_errors: true

- name: List tiering configurations with limit
  nutanix.ncp.ntnx_tiering_configurations_info_v2:
    file_server_ext_id: "3ec0fb37-8c1e-40b3-9d7f-3cc45f0e1234"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC TieringConfiguration info v4 API.
    - It can be a single TieringConfiguration if external ID is provided.
    - List of multiple TieringConfiguration if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
        "cooloff_period_seconds": 604800,
        "ext_id": "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af",
        "links": null,
        "memory_threshold_percent": 80,
        "minimum_file_size_bytes": 65536,
        "mount_target_ext_ids": null,
        "mount_targets_enablement_type": "ALL_FUTURE_MOUNT_TARGETS",
        "schedule": [
            {
                "day_of_week": 1,
                "schedules": [
                    {
                        "duration_minutes": 240,
                        "start_hours": 0,
                        "start_minutes": 0
                    }
                ]
            }
        ],
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
  sample: "Api Exception raised while fetching tiering configurations info"

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
  description: External ID of the tiering configuration
  type: str
  returned: when external ID is provided
  sample: "b04eef3c-4a3f-4c6d-9d2c-1cd21f18e2af"

total_available_results:
  description: The total number of available tiering configurations for the file server.
  type: int
  returned: when all tiering configurations are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_tier_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import (  # noqa: E402
    get_tiering_configuration,
    list_tiering_configurations,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_tiering_configuration_using_ext_id(module, tier_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_tiering_configuration(module, tier_api, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_tiering_configurations(module, tier_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating tiering configurations info spec", **result
        )

    resp = list_tiering_configurations(module, tier_api, file_server_ext_id, **kwargs)

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
    tier_api = get_tier_api_instance(module)
    if module.params.get("ext_id"):
        get_tiering_configuration_using_ext_id(module, tier_api, result)
    else:
        get_tiering_configurations(module, tier_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
