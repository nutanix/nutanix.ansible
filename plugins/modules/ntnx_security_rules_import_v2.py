#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_rules_import_v2
short_description: Import network security policies into Nutanix Prism Central
version_added: "2.6.0"
description:
  - This module imports Flow network security policies into Nutanix Prism Central from a data file.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Import Network Security Policies) -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
  path:
    description:
      - Local path to the network security policies file to import.
    type: path
    required: true
  purge_policies:
    description:
      - Specifies whether the existing policies need to be deleted (C(true)) or retained (C(false)) upon import.
    type: bool
    required: false
  dryrun:
    description:
      - Whether to execute in a dry-run mode providing ability to identify trouble spots and system failures without performing the actual operation.
      - This mode offers a summary snapshot of the resultant system in order to better understand how things fit together.
      - The operation runs in dry-run mode only if the provided value is true.
    type: bool
    required: false
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Import network security policies from a file
  nutanix.ncp.ntnx_security_rules_import_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    path: "/tmp/network_security_policies_export.flw"
  register: result
  ignore_errors: true

- name: Import network security policies and purge existing ones
  nutanix.ncp.ntnx_security_rules_import_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    path: "/tmp/network_security_policies_export.flw"
    purge_policies: true
  register: result
  ignore_errors: true

- name: Dry-run import of network security policies
  nutanix.ncp.ntnx_security_rules_import_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    path: "/tmp/network_security_policies_export.flw"
    dryrun: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for importing network security policies.
    - If C(wait) is true, it returns the completed task details.
    - If C(wait) is false, it returns the task reference details.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-06-18T12:46:31.475401+00:00",
      "completion_details": null,
      "created_time": "2026-06-18T12:46:31.399813+00:00",
      "entities_affected": null,
      "error_messages": null,
      "ext_id": "ZXJnb24=:9bfb6e09-8cdf-4c80-94de-affc5292cded",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-06-18T12:46:31.475400+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 0,
      "number_of_subtasks": 0,
      "operation": "kNetworkSecurityPolicyImportApply",
      "operation_description": "Import Network Security Policy and Associated entities",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-06-18T12:46:31.411897+00:00",
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
  returned: When there is an error or in check mode
  type: str

path:
  description: The path of the file that was used for the import.
  returned: always
  type: str
  sample: "/tmp/network_security_policies_export.flw"
"""

import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_network_security_policy_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        path=dict(type="path", required=True),
        purge_policies=dict(type="bool", required=False),
        dryrun=dict(type="bool", required=False),
    )
    return module_args


def import_policies(module, network_security_policies, result):
    file_path = Path(module.params.get("path"))
    result["path"] = str(file_path)

    if module.check_mode:
        result["msg"] = (
            "Network security policies from file:{0} will be imported.".format(
                str(file_path)
            )
        )
        return

    if not file_path.is_file():
        module.fail_json(
            msg="The provided path '{0}' is not a valid file".format(str(file_path)),
            **result,
        )

    kwargs = {}
    if module.params.get("purge_policies") is not None:
        kwargs["NTNX_Purge_Policies"] = module.params.get("purge_policies")
    if module.params.get("dryrun") is not None:
        kwargs["_dryrun"] = module.params.get("dryrun")

    resp = None
    try:
        resp = network_security_policies.apply_network_security_policy_import(
            path=file_path, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while importing network security policies",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
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
    import_policies(module, network_security_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
