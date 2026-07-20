#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_settings_info_v2
short_description: Fetch custom recovery settings info from a Nutanix Recovery Plan
version_added: 2.5.0
description:
  - This module allows you to fetch information about RecoverySetting in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RecoverySetting.
  - If C(ext_id) is not provided, list multiple RecoverySetting optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get a recovery setting by ext_id) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, NCM Connector, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - >-
      B(List recovery settings) -
      Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, NCM Connector, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  ext_id:
    description:
      - The external identifier of the recovery setting.
      - If provided, only that recovery setting is returned.
    type: str
  recovery_plan_ext_id:
    description:
      - External identifier of the parent recovery plan.
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
"""

EXAMPLES = r"""
- name: Fetch recovery setting by ext_id
  nutanix.ncp.ntnx_recovery_settings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
    ext_id: "d1a2b3c4-5555-6666-7777-8888aabbccdd"
  register: result

- name: List all recovery settings under a recovery plan
  nutanix.ncp.ntnx_recovery_settings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
  register: result

- name: List recovery settings with filter
  nutanix.ncp.ntnx_recovery_settings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
    filter: "scope eq Datapolicies.Config.RecoverySettingScope'VM'"
  register: result
  ignore_errors: true

- name: List recovery settings with limit
  nutanix.ncp.ntnx_recovery_settings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RecoverySetting info v4 API.
    - It can be a single RecoverySetting if external ID is provided.
    - It is a list of multiple RecoverySetting if external ID is not provided, optionally filtered / paginated.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "d1a2b3c4-5555-6666-7777-8888aabbccdd",
      "links": null,
      "recovery_setting": {
        "floating_ip_associations": null,
        "in_guest_script_execution_config": {
          "is_enabled": true,
          "timeout_secs": 300
        },
        "ip_mappings": null,
        "power_state": "ON",
        "vm": {
          "ext_id": "0005c1c1-0000-0000-0000-000000000001",
          "name": null
        },
        "volume_group_attachments": null
      },
      "scope": "VM",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching recovery settings info"

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
  description: External ID of the recovery setting
  type: str
  returned: when external ID is provided
  sample: "d1a2b3c4-5555-6666-7777-8888aabbccdd"

total_available_results:
  description: The total number of available recovery settings on the recovery plan.
  type: int
  returned: when all recovery settings are listed
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_recovery_setting  # noqa: E402
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
        recovery_plan_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_recovery_setting_using_ext_id(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_recovery_setting(module, api_instance, recovery_plan_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_recovery_settings(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating recovery settings info spec", **result)

    try:
        resp = api_instance.list_recovery_settings(
            recoveryPlanExtId=recovery_plan_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery settings info",
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
    api_instance = get_recovery_plans_api_instance(module)
    if module.params.get("ext_id"):
        get_recovery_setting_using_ext_id(module, api_instance, result)
    else:
        list_recovery_settings(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
