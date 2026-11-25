#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_gateway_upgrade_v2
short_description: Upgrade network gateways in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module upgrades a network gateway to the latest supported version in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Upgrade a Network Gateway) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Project Admin, Super Admin,
      Tenant Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will upgrade the gateway.
      - If C(state) is not C(present), the module will fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID of the gateway to upgrade.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Upgrade an existing gateway to the latest supported version
  nutanix.ncp.ntnx_gateway_upgrade_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for upgrading a network gateway.
    - Returns the task details for the upgrade operation.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-11-24T13:54:19.200292+00:00",
      "completion_details": null,
      "created_time": "2026-11-24T13:54:19.089383+00:00",
      "entities_affected": [
          {
              "ext_id": "0f3517fa-c805-4b62-a5dc-06d4a1e34623",
              "name": "gw_ansible_AnvouRHkqtba_all_updated",
              "rel": "networking:config:gateway"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:a126e802-1d02-46e7-b4ce-a4d1fadfc806",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-11-24T13:54:19.200291+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "kVpnGatewayUpdate",
      "operation_description": "Network Gateway Update",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "project_ext_id": "00000000-0000-0000-0000-000000000000",
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-11-24T13:54:19.108626+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:3c42282a-3dbe-4026-8469-fe8c145ad1e4"

ext_id:
  description:
    - The external ID of the gateway.
  returned: always
  type: str
  sample: "c13bf194-4017-4efb-abbf-d44c837818a9"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or check mode
  type: str
  sample: "Gateway with ext_id:c13bf194-4017-4efb-abbf-d44c837818a9 will be upgraded."
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import get_gateways_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def upgrade_gateway(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Gateway with ext_id:{0} will be upgraded.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.upgrade_gateway_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while upgrading gateway",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_gateways_api_instance(module)
    upgrade_gateway(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
