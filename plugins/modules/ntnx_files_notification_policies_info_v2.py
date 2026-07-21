#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_notification_policies_info_v2
short_description: Fetch notification policies info from a Nutanix Files server
version_added: 2.7.0
description:
  - This module allows you to fetch information about NotificationPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific NotificationPolicy.
  - If C(ext_id) is not provided, list multiple NotificationPolicy optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the notification policy.
      - If provided, the specific notification policy will be fetched.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the notification policy.
      - Required for all operations.
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
- name: Get notification policy using ext_id
  nutanix.ncp.ntnx_files_notification_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b"
  register: result
  ignore_errors: true

- name: List all notification policies for a file server
  nutanix.ncp.ntnx_files_notification_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: List notification policies with filter
  nutanix.ncp.ntnx_files_notification_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    filter: "name eq 'notification_policy_ansible'"
  register: result
  ignore_errors: true

- name: List notification policies with limit
  nutanix.ncp.ntnx_files_notification_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC NotificationPolicy info v4 API.
    - It can be a single NotificationPolicy if external ID is provided.
    - List of multiple NotificationPolicy if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "blocked_clients": null,
      "description": "Notification policy created by Ansible",
      "ext_id": "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b",
      "file_blocking_mode": null,
      "file_extensions": null,
      "has_secured_connection": false,
      "links": null,
      "mount_target_ext_ids": null,
      "name": "notification_policy_ansible",
      "operations": [
          "FILE_CREATE",
          "FILE_DELETE"
      ],
      "partner_server_ext_ids": [
          "3c9a1f3b-3ddb-4585-9159-26d2318269e3"
      ],
      "protocol_types": [
          "SMB"
      ],
      "should_include_all_mount_targets": true,
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
  sample: "Api Exception raised while fetching notification policies info"

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
  description: External ID of the notification policy
  type: str
  returned: when external ID is provided
  sample: "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b"

total_available_results:
  description: The total number of available notification policies for the file server in PC.
  type: int
  returned: when all notification policies are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_notification_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_notification_policy  # noqa: E402
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


def get_notification_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    resp = get_notification_policy(module, api_instance, ext_id, file_server_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_notification_policies(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating notification policies info spec", **result
        )

    try:
        resp = api_instance.list_notification_policies(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching notification policies info",
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
    api_instance = get_notification_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_notification_policy_using_ext_id(module, api_instance, result)
    else:
        get_notification_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
