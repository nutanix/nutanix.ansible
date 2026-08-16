#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virus_scan_policies_info_v2
short_description: Fetch virus scan policies for a Nutanix Files file server
version_added: 2.7.0
description:
  - This module allows you to fetch information about VirusScanPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VirusScanPolicy.
  - If C(ext_id) is not provided, list multiple VirusScanPolicy optionally filtered / paginated.
  - This module uses the Nutanix Files v4 APIs based SDK.
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the virus scan policy.
      - When provided, only that specific policy is returned.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the file server that owns the virus scan policies.
      - Required for all fetch operations.
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
- name: Get virus scan policy using ext_id
  nutanix.ncp.ntnx_virus_scan_policies_info_v2:
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
    ext_id: "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1"
  register: result

- name: List all virus scan policies for a file server
  nutanix.ncp.ntnx_virus_scan_policies_info_v2:
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
  register: result

- name: List virus scan policies with limit
  nutanix.ncp.ntnx_virus_scan_policies_info_v2:
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
    limit: 1
  register: result

- name: List virus scan policies with filter on mountTargetReference
  nutanix.ncp.ntnx_virus_scan_policies_info_v2:
    file_server_ext_id: "b6b74a04-5b9c-4a5f-9e2e-3b1d5f6d1a11"
    filter: "mountTargetReference eq '5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1'"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VirusScanPolicy info v4 API.
    - It can be a single VirusScanPolicy if external ID is provided.
    - List of multiple VirusScanPolicy if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1",
      "excluded_file_extensions": ["iso", "tmp"],
      "is_anti_virus_enabled": true,
      "is_file_access_blocked": false,
      "is_scan_on_read_enabled": true,
      "is_scan_on_write_enabled": true,
      "links": null,
      "max_file_size_threshold_bytes": 10485760,
      "mount_target_reference": null,
      "scan_timeout_interval_secs": 60,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching virus scan policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the virus scan policy.
  type: str
  returned: when external ID is provided
  sample: "5e17ff0d-3a55-4c78-95bb-83a5b6b6bda1"

total_available_results:
  description: The total number of available virus scan policies for the file server.
  type: int
  returned: when all virus scan policies are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_virus_scan_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_virus_scan_policy  # noqa: E402
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
        file_server_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_virus_scan_policy_using_ext_id(module, api_instance, result):
    """Fetch a single virus scan policy using its external ID."""
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    resp = get_virus_scan_policy(module, api_instance, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_virus_scan_policies(module, api_instance, result):
    """List virus scan policies with the optional OData query parameters."""
    file_server_ext_id = module.params.get("file_server_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating virus scan policies info spec", **result
        )

    try:
        resp = api_instance.list_virus_scan_policies(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching virus scan policies info",
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
    api_instance = get_virus_scan_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_virus_scan_policy_using_ext_id(module, api_instance, result)
    else:
        get_virus_scan_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
