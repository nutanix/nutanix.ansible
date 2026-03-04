#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_policies_info_v2
short_description: Fetch storage policies info in Nutanix Prism Central
version_added: 2.4.0
description:
  - This module allows you to fetch storage policies info or specific storage policy in Nutanix Prism Central.
  - If ext_id is provided, fetch particular storage policy info using external ID
  - If ext_id is not provided, fetch multiple storage policies info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external identifier of the storage policy.
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
- name: Fetch storage policy using external ID
  nutanix.ncp.ntnx_storage_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "7bea69e9-684c-4736-7805-d658ee17c1b6"
  register: result

- name: List all storage policies
  nutanix.ncp.ntnx_storage_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
  register: result

- name: Fetch storage policy using filter
  nutanix.ncp.ntnx_storage_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    filter: "name eq 'storage_policy_name_updated'"
  register: result
  ignore_errors: true

- name: Fetch storage policy using limit
  nutanix.ncp.ntnx_storage_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    limit: 1
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - Response for fetching storage policies info
    - Specific storage policy info if External ID is provided
    - List of multiple storage policies info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
      "category_ext_ids": ["bf71eb79-3fd1-4981-aee5-0b011bdbee6c"],
      "compression_spec": { "compression_state": "POSTPROCESS" },
      "encryption_spec": { "encryption_state": "ENABLED" },
      "ext_id": "7bea69e9-684c-4736-7805-d658ee17c1b6",
      "fault_tolerance_spec": { "replication_factor": "THREE" },
      "links": null,
      "name": "storage_policy_name",
      "policy_type": "USER",
      "qos_spec": { "throttled_iops": 1000 },
      "tenant_id": null,
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
  sample: "Api Exception raised while fetching storage policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs
  sample: null

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the storage policy
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available storage policies in PC.
  type: int
  returned: when all storage policies are fetched
  sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_storage_policies_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_storage_policy  # noqa: E402
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


def get_storage_policy_using_ext_id(module, storage_policies, result):
    ext_id = module.params.get("ext_id")
    resp = get_storage_policy(module, storage_policies, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_storage_policies(module, storage_policies, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating storage policies info Spec", **result)

    try:
        resp = storage_policies.list_storage_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage policies info",
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
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "error": None}
    storage_policies = get_storage_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_storage_policy_using_ext_id(module, storage_policies, result)
    else:
        get_storage_policies(module, storage_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
