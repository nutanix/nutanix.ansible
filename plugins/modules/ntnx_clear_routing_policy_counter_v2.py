#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clear_routing_policy_counter_v2
short_description: Clear routing policy packet/byte counters in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module clears (resets to zero) the packet and byte match counters of routing policies in a VPC.
    - If C(routing_policy_ext_id) is provided, only that specific routing policy's counters are cleared.
    - If C(routing_policy_ext_id) is not provided, counters for all routing policies in the VPC are cleared.
    - The operation is asynchronous and returns a task reference; use C(wait=true) to block until completion.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Clear Routing Policy counters) -
      Required Roles: Internal Super Admin, Super Admin, Account Owner, Administrator, Prism Admin, VPC Admin, Tenant Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported; the module always performs the clear-counters action.
        type: str
        choices:
            - present
        default: present
    vpc_ext_id:
        description:
            - External ID of the VPC to which the routing policy (or policies) belong.
            - Required to identify the VPC whose routing policy counters should be cleared.
        type: str
        required: true
    routing_policy_ext_id:
        description:
            - External ID of a specific routing policy whose counters need to be cleared.
            - When omitted, counters for B(all) routing policies inside C(vpc_ext_id) are cleared.
        type: str
        required: false
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
- name: Clear counters for all routing policies inside a VPC
  nutanix.ncp.ntnx_clear_routing_policy_counter_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpc_ext_id: "a4f3f04f-1222-8544-7896-28b62bcc3e3e"
  register: result
  ignore_errors: true

- name: Clear counters of a specific routing policy inside a VPC
  nutanix.ncp.ntnx_clear_routing_policy_counter_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpc_ext_id: "a4f3f04f-1222-8544-7896-28b62bcc3e3e"
    routing_policy_ext_id: "b0cce620-3654-8522-9876-a91e2c037862"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for clearing routing policy counters.
        - Task details when C(wait) is true - contains the completed task record.
        - Task reference when C(wait) is false - contains the queued task reference.
    returned: always
    type: dict
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T13:07:22.114308+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T13:07:22.056881+00:00",
            "entities_affected": [
                {
                    "ext_id": "6eb8658e-1d92-4755-b969-56e2ecaa5953",
                    "name": null,
                    "rel": "networking:config:routing-policy"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:16ba14e7-0279-4a22-8696-6cdde437fef7",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T13:07:22.114307+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "kRoutingPolicyResetCountersAsync",
            "operation_description": "Routing Policy Reset Counters",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T13:07:22.070090+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

task_ext_id:
    description: The external ID of the task that performed the counter clear.
    returned: always
    type: str
    sample: "ZXJnb24=:16ba14e7-0279-4a22-8696-6cdde437fef7"

ext_id:
    description:
        - The external ID that identifies the target of the operation.
        - When a specific routing policy was targeted this is the C(routing_policy_ext_id).
        - Otherwise it is the C(vpc_ext_id) for which all routing policy counters were cleared.
    returned: always
    type: str
    sample: "6eb8658e-1d92-4755-b969-56e2ecaa5953"

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while clearing routing policy counters"

error:
    description: This field typically holds information about errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Not Found"

failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_routing_policy_stats_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        vpc_ext_id=dict(type="str", required=True),
        routing_policy_ext_id=dict(type="str", required=False),
    )
    return module_args


def clear_routing_policy_counters(module, result, api_instance):
    """Invoke the SDK clear_routing_policy_counters action.

    Behaviour follows the ``ntnx_vm_revert_v2`` action-module pattern:
    * Build the spec via ``SpecGenerator`` so ``vpc_ext_id`` /
      ``routing_policy_ext_id`` are propagated onto the SDK model.
    * Support ``check_mode`` — return the generated spec without an API call.
    * On success, capture the ``task_ext_id`` and — when ``wait`` is true —
      poll the task until it reaches a terminal state and return the full
      task record.
    """
    validate_required_params(module, ["vpc_ext_id"])

    vpc_ext_id = module.params.get("vpc_ext_id")
    routing_policy_ext_id = module.params.get("routing_policy_ext_id")

    result["ext_id"] = routing_policy_ext_id or vpc_ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.RoutingPolicyClearCountersSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating clear routing policy counters spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.clear_routing_policy_counters(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while clearing routing policy counters",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_routing_policy_stats_api_instance(module)
    clear_routing_policy_counters(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
