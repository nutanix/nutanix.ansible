#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_quota_policies_info_v2
short_description: Fetch quota policies information for a Nutanix Files mount target
version_added: 2.7.0
description:
  - This module allows you to fetch information about QuotaPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific QuotaPolicy.
  - If C(ext_id) is not provided, list multiple QuotaPolicy optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
options:
  ext_id:
    description:
      - The external ID of the quota policy.
      - If provided, the module fetches the details of the specific quota policy.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the mount target.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - The external identifier of the mount target (share/export) for which the quota policies are configured.
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
- name: Get quota policy using ext_id
  nutanix.ncp.ntnx_files_quota_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: List all quota policies for a mount target
  nutanix.ncp.ntnx_files_quota_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: List quota policies with filter
  nutanix.ncp.ntnx_files_quota_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    filter: "principalName eq 'user1@ad.example.com'"
  register: result
  ignore_errors: true

- name: List quota policies with limit
  nutanix.ncp.ntnx_files_quota_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    mount_target_ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC QuotaPolicy info v4 API.
    - It can be a single QuotaPolicy if external ID is provided.
    - List of multiple QuotaPolicy if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "enforcement_type": "SOFT",
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "is_notification_enabled": true,
      "links": null,
      "notification_recipients": ["admin@ad.example.com"],
      "principal_name": "user1@ad.example.com",
      "principal_type": "USER",
      "size_in_bytes": 1073741824,
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
  sample: "Api Exception raised while fetching quota policies info"

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
  description: External ID of the quota policy
  type: str
  returned: when external ID is provided
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

total_available_results:
  description: The total number of available quota policies for the mount target in PC.
  type: int
  returned: when all quota policies are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_quota_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_quota_policy  # noqa: E402
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
        mount_target_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_quota_policy_using_ext_id(module, quota_policies, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    resp = get_quota_policy(
        module, quota_policies, file_server_ext_id, mount_target_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_quota_policies(module, quota_policies, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating quota policies info spec", **result)

    kwargs["fileServerExtId"] = module.params.get("file_server_ext_id")
    kwargs["mountTargetExtId"] = module.params.get("mount_target_ext_id")

    try:
        resp = quota_policies.list_quota_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching quota policies info",
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
    quota_policies = get_quota_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_quota_policy_using_ext_id(module, quota_policies, result)
    else:
        get_quota_policies(module, quota_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
