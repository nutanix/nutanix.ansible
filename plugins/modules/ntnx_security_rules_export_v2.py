#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_rules_export_v2
short_description: Export network security policies in Nutanix Prism Central
version_added: "2.6.0"
description:
  - This module exports one or more Flow network security policies in Nutanix Prism Central.
  - If C(policy_references) is not provided, all network security policies are exported.
  - The exported content is always downloaded and saved to a local file. The local path is returned in C(path).
  - If C(path) is not provided, the file is saved to the current working directory using the server-provided file name.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Export Network Security Policies) -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
  policy_references:
    description:
      - A list of network security policy external ids to export.
      - If not provided, all network security policies are exported.
    type: list
    elements: str
    required: false
  path:
    description:
      - Local destination path where the exported network security policies file is saved.
      - The file can later be used by the C(ntnx_security_rules_import_v2) module to import the policies.
      - The module always waits for the export task to complete in order to download the file.
      - If not provided, the file is downloaded to the current working directory using the
        file name returned by the server. The final location is always returned in C(path).
    type: path
    required: false
  wait:
    description:
      - Wait for the export task to complete.
      - This module must always wait for the export task to finish, because the exported
        file can only be downloaded once the task is complete.
      - Only C(true) is supported.
    type: bool
    required: false
    default: true
    choices:
      - true
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Export specific network security policies to a file
  nutanix.ncp.ntnx_security_rules_export_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    policy_references:
      - "ac8e7c8a-3e6f-4f2a-8d2b-9f3a6b6f97e2"
      - "18dbfce0-f7e1-4b19-a9e6-43b0be8c2507"
    path: "/tmp/network_security_policies_export.flw"
  register: result
  ignore_errors: true

- name: Export all network security policies to a file
  nutanix.ncp.ntnx_security_rules_export_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    path: "/tmp/network_security_policies_export.flw"
  register: result
  ignore_errors: true

- name: Export all network security policies without specifying a path
  nutanix.ncp.ntnx_security_rules_export_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for exporting network security policies.
    - It returns the completed task details.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-06-18T12:34:19.213650+00:00",
      "completion_details": null,
      "created_time": "2026-06-18T12:34:19.124020+00:00",
      "entities_affected": [
          {
              "ext_id": "38d9f279-c0d7-4951-ae52-33925ac4dd11",
              "name": "Quarantine Strict Policy",
              "rel": "microseg:config:policy"
          },
          {
              "ext_id": "6c8c9d38-c39c-4626-9b88-85f45e700a33",
              "name": "ansible-nsr-kxigsDsDbiLt1",
              "rel": "microseg:config:policy"
          },
          {
              "ext_id": "d376aa6f-e5ad-4052-890e-e56d4b1b1b09",
              "name": "Quarantine Forensic Policy",
              "rel": "microseg:config:policy"
          },
          {
              "ext_id": "7329e3d6-5eac-4395-6671-4ca9527780ba",
              "name": "AnsibleSecurityRuleTest:AnsibleSecurityRuleTestkxigsDsDbiLt1",
              "rel": "prism:config:category"
          },
          {
              "ext_id": "4c313d99-ad50-5480-ae34-6c29ee35ed92",
              "name": "Quarantine:Default",
              "rel": "prism:config:category"
          },
          {
              "ext_id": "252887b5-1462-501e-9e1d-aac971085a45",
              "name": "Quarantine:Forensics",
              "rel": "prism:config:category"
          },
          {
              "ext_id": "8714753a-18d7-4bf7-5912-3ba62952f829",
              "name": "AnsibleSecurityRuleTest:AnsibleSecurityRuleTestkxigsDsDbiLt0",
              "rel": "prism:config:category"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:4c34bfa3-294d-4ac4-933a-b527e03f7f9a",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-06-18T12:34:19.213649+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 7,
      "number_of_subtasks": 0,
      "operation": "kNetworkSecurityPolicyExportAsync",
      "operation_description": "Export Network Security Policy and Associated entities",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-06-18T12:34:19.135460+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external id of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Failed to determine the downloaded export file path"

path:
  description:
    - The local path of the downloaded export file.
  returned: always
  type: str
  sample: "/tmp/network_security_policies_export.flw"
"""

import os  # noqa: E402
import shutil  # noqa: E402
import traceback  # noqa: E402
import uuid  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_network_security_policy_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_microseg_py_client as mic_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as mic_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        policy_references=dict(type="list", elements="str", required=False),
        path=dict(type="path", required=False),
        wait=dict(type="bool", default=True, choices=[True]),
    )
    return module_args


def download_export_file(module, network_security_policies, request_id, path, result):
    # When the user provides a path, download into its directory; otherwise let
    # the SDK use its default download directory (the current working directory).
    if path:
        dest_dir = os.path.dirname(os.path.abspath(path))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        network_security_policies.api_client.configuration.download_directory = dest_dir

    headers = {
        "NTNX-Request-Id": request_id,
        "Accept": "application/octet-stream",
    }
    resp = None
    try:
        resp = network_security_policies.list_network_security_policies(**headers)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading network security policies export file",
        )

    data = resp.data
    if isinstance(data, dict):
        downloaded_path = data.get("path")
    else:
        downloaded_path = getattr(data, "path", None)

    if not downloaded_path:
        module.fail_json(
            msg="Failed to determine the downloaded export file path", **result
        )

    downloaded_path = str(downloaded_path)
    # If a destination path was requested, move the downloaded file there;
    # otherwise return the SDK default location as-is.
    if path and os.path.abspath(downloaded_path) != os.path.abspath(path):
        shutil.move(downloaded_path, path)
        return path
    return downloaded_path


def export_policies(module, network_security_policies, result):
    sg = SpecGenerator(module)
    default_spec = mic_sdk.NetworkSecurityPolicyExportSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating network security policy export spec", **result
        )

    path = module.params.get("path")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["path"] = path
        return

    request_id = str(uuid.uuid4())
    kwargs = {"NTNX-Request-Id": request_id}
    resp = None
    try:
        resp = network_security_policies.export_network_security_policy(
            body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while exporting network security policies",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    # The export file can only be downloaded once the prepare-export task
    # completes, so always wait for it before downloading.
    if task_ext_id:
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["path"] = download_export_file(
        module, network_security_policies, request_id, path, result
    )
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    network_security_policies = get_network_security_policy_api_instance(module)
    export_policies(module, network_security_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
