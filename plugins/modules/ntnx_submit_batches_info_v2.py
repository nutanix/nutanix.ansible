#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_submit_batches_info_v2
short_description: Fetch batch operations info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about SubmitBatch in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific SubmitBatch.
  - If C(ext_id) is not provided, list multiple SubmitBatch optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get batch by ext_id) -
      Required Roles: Super Admin, Prism Admin, Prism Viewer
    - >-
      B(Get list of batches) -
      Required Roles: Super Admin, Prism Admin, Prism Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  ext_id:
    description:
      - The external ID of the batch.
      - When provided, the module fetches a single batch by its ext_id.
      - When omitted, the module lists all batches (optionally filtered / paginated).
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
- name: Get batch info using ext_id
  nutanix.ncp.ntnx_submit_batches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "e6d0a8b4-1234-4a35-9db2-1111aaaa1111"
  register: single_batch

- name: List all batches
  nutanix.ncp.ntnx_submit_batches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: batches

- name: List batches with filter
  nutanix.ncp.ntnx_submit_batches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'ansible_batch_create_address_groups'"
  register: filtered_batches

- name: List batches with limit
  nutanix.ncp.ntnx_submit_batches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: limited_batches
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SubmitBatch info v4 API.
    - It can be a single SubmitBatch if external ID is provided.
    - List of multiple SubmitBatch if external ID is not provided
      with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "completion_status": "SUCCEEDED",
      "end_time": "2026-07-20T15:34:15.092888+00:00",
      "execution_status": "COMPLETED",
      "ext_id": "e6d0a8b4-1234-4a35-9db2-1111aaaa1111",
      "failed_count": 0,
      "links": null,
      "name": "ansible_batch_create_address_groups",
      "should_stop_on_error": false,
      "size": 2,
      "start_time": "2026-07-20T15:34:12.593544+00:00",
      "success_count": 2,
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
  sample: "Api Exception raised while fetching batches info"

error:
  description:
    - This field typically holds information about if the task have errors
      that occurred during the task execution.
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the batch.
  type: str
  returned: when external ID is provided
  sample: "e6d0a8b4-1234-4a35-9db2-1111aaaa1111"

total_available_results:
  description: The total number of available batches in PC.
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


def get_batch_using_ext_id(module, api_instance, result):
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_batches_api_instance(module)
    if module.params.get("ext_id"):
        get_batch_using_ext_id(module, api_instance, result)
    else:
        get_batches(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
