#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_batches_info_v2
short_description: Fetch Batch information in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Batch in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Batch.
  - If C(ext_id) is not provided, list multiple Batch optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a Batch by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin.
    - >-
      B(List Batches) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  ext_id:
    description:
      - External ID of a specific Batch to fetch.
      - When omitted the module lists Batches.
    type: str
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
- name: Fetch a Batch using external ID
  nutanix.ncp.ntnx_batches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005b21e-batch-ext-id"
  register: result
  ignore_errors: true

- name: List all Batches
  nutanix.ncp.ntnx_batches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Batches with filter
  nutanix.ncp.ntnx_batches_info_v2:
    filter: "executionStatus eq Prism.Config.BatchExecutionStatus'COMPLETED'"
  register: result
  ignore_errors: true

- name: List Batches with limit
  nutanix.ncp.ntnx_batches_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Batch info v4 API.
    - It can be a single Batch if external ID is provided.
    - List of multiple Batch if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "completion_status": "SUCCEEDED",
      "end_time": "2026-07-20T15:30:22.514+00:00",
      "execution_status": "COMPLETED",
      "ext_id": "0005b21e-ansible-batch",
      "failed_count": 0,
      "links": null,
      "name": "ansible-batch-create-categories",
      "should_stop_on_error": false,
      "size": 2,
      "start_time": "2026-07-20T15:30:12.001+00:00",
      "success_count": 2,
      "tenant_id": null
    }

ext_id:
  description:
    - External ID of the fetched Batch.
  returned: when external ID is provided
  type: str
  sample: "0005b21e-ansible-batch"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching batches info"

error:
  description: Error details if the task fails.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available Batches in Prism Central.
  type: int
  returned: when all batches are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_batch  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_batches_api_instance  # noqa: E402
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


def get_batch_with_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_batch(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_batches(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating batches info spec", **result)

    try:
        resp = api_instance.list_batches(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching batches info",
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
    result = {"changed": False, "response": None}
    api_instance = get_batches_api_instance(module)
    if module.params.get("ext_id"):
        get_batch_with_ext_id(module, api_instance, result)
    else:
        get_batches(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
