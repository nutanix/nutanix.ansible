#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_stages_info_v2
short_description: Fetch Recovery stages info in a Nutanix Recovery Plan
version_added: 2.7.0
description:
  - This module allows you to fetch information about RecoveryStage in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RecoveryStage.
  - If C(ext_id) is not provided, list multiple RecoveryStage optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get Recovery stage by ext_id) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, NCM Connector, Prism Admin, Prism Viewer, Project Manager, Super Admin
  - >-
    B(List Recovery stages) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, NCM Connector, Prism Admin, Prism Viewer, Project Manager, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  recovery_plan_ext_id:
    description:
      - External identifier of the parent Recovery Plan whose Recovery stages you want to query.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the Recovery stage.
      - If provided, only that particular Recovery stage is fetched.
    type: str
    required: false
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
- name: Get Recovery stage using ext_id
  nutanix.ncp.ntnx_recovery_stages_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    ext_id: "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c"
  register: result

- name: List all Recovery stages of a Recovery plan
  nutanix.ncp.ntnx_recovery_stages_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
  register: result

- name: List Recovery stages with limit
  nutanix.ncp.ntnx_recovery_stages_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    limit: 1
  register: result

- name: List Recovery stages with filter
  nutanix.ncp.ntnx_recovery_stages_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    filter: "entityType eq Datapolicies.Config.RecoverableEntityType'VM'"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RecoveryStage info v4 API.
    - It can be a single RecoveryStage if external ID is provided.
    - List of multiple RecoveryStage if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "category_ext_ids": null,
      "entities": [
        {
          "ext_id": "9e9c7f6a-4b28-4d5f-a1d9-1f1b3a92aa11",
          "name": "webserver-vm"
        }
      ],
      "entity_type": "VM",
      "ext_id": "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c",
      "links": null,
      "post_actions": [
        {
          "config": {
            "delay_secs": 30
          }
        }
      ],
      "priority": 1,
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
  sample: "Api Exception raised while fetching recovery stages info"

error:
  description: This field holds information about any error that occurred during the task.
  type: str
  returned: when an error occurs

failed:
  description: This field holds information about whether the task has failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Recovery stage.
  type: str
  returned: when external ID is provided
  sample: "1ab8a1c3-2ff9-4b57-b6ce-2e6c74aaa72c"

total_available_results:
  description: The total number of available Recovery stages under the given Recovery plan.
  type: int
  returned: when Recovery stages are listed
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_recovery_stage  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        recovery_plan_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )

    return module_args


def get_recovery_stage_using_ext_id(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_recovery_stage(module, api_instance, recovery_plan_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_recovery_stages(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating recovery stages info spec", **result)

    try:
        resp = api_instance.list_recovery_stages(
            recoveryPlanExtId=recovery_plan_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery stages info",
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
        get_recovery_stage_using_ext_id(module, api_instance, result)
    else:
        get_recovery_stages(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
