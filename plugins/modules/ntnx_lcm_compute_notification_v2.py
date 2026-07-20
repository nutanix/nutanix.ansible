#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_compute_notification_v2
short_description: Compute LCM upgrade plan and notifications for a set of entities.
version_added: 2.7.0
description:
    - This module triggers the LCM V(compute-notifications) action in Nutanix Prism Central.
    - The action asynchronously computes the LCM upgrade plan and generates the corresponding
      notifications (severity messages, host reboots, VM migrations, maintenance-mode entries,
      etc.) for a set of entities and their target versions.
    - The API returns a task reference; after the task completes, the resulting notification
      resource identifier is placed in the task V(completion_details) and can be fetched with
      M(nutanix.ncp.ntnx_compute_notifications_info_v2).
    - The computed notification resource is cached and remains valid for one hour from the
      time it is created.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module triggers the compute-notifications action.
            - The module does not support C(absent) state because the notifications resource
              is server-managed and expires automatically after one hour.
        type: str
        choices:
            - present
        default: present
    entity_update_specs:
        description:
            - List of entity update specifications.
            - Every element identifies an LCM entity and the target version to which it should
              be upgraded when computing the notifications.
            - This option is required to trigger the compute-notifications action.
        type: list
        elements: dict
        required: true
        suboptions:
            entity_uuid:
                description:
                    - UUID of the LCM entity for which the notification should be computed.
                type: str
                required: true
            to_version:
                description:
                    - Target version the entity should be upgraded to.
                type: str
                required: true
    cluster_ext_id:
        description:
            - External ID of the target Prism Element cluster.
            - When operating from Prism Central, use this to target notifications computation
              at a specific PE cluster. If omitted, the action is executed on Prism Central.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Compute LCM upgrade notifications.) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Compute LCM upgrade notifications for a single entity on Prism Central
  nutanix.ncp.ntnx_lcm_compute_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    entity_update_specs:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.1.0"
  register: compute_notifications_pc

- name: Compute LCM upgrade notifications for entities on a Prism Element cluster
  nutanix.ncp.ntnx_lcm_compute_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db4-a450-e685-0fda-cdf9ca935bfd"
    entity_update_specs:
      - entity_uuid: "15570c98-beaf-4633-afd2-b6a306ff1001"
        to_version: "5.0.0"
      - entity_uuid: "9ebc7f9c-1234-4b16-a9d1-1f9e5f8b5a3c"
        to_version: "3.8.0"
    credentials:
      - credential_ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: compute_notifications_pe
"""

RETURN = r"""
response:
    description:
        - Response for the compute-notifications action.
        - When C(wait) is true and the resulting notification resource external ID is available
          on the task V(completion_details), the module returns the fetched notification detail
          (severity, per-entity actions, target versions, etc.).
        - When C(wait) is true but no notification resource external ID is exposed by the task,
          the module returns the task detail.
        - When C(wait) is false, the module returns the initial task response containing the
          task external ID.
        - In C(check_mode) the module returns the request specification that would have been
          submitted.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_id": "00062db4-a450-e685-0fda-cdf9ca935bfd",
            "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
            "links": null,
            "notifications": [
                {
                    "entity_class": "PC CORE CLUSTER",
                    "entity_model": "Calm Policy Engine",
                    "entity_type": "SOFTWARE",
                    "entity_version": "4.0.0",
                    "ext_id": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
                    "details": [
                        {
                            "message": "Some hosts will be rebooted during the upgrade.",
                            "severity_level": "WARNING"
                        }
                    ],
                    "hardware_family": null,
                    "hypervisor_type": null,
                    "location_info": {
                        "location_name": null,
                        "location_type": "PC",
                        "uuid": "1e9a1996-50e2-485f-a67c-22355cb43055"
                    },
                    "notification_type": "ENTITY",
                    "to_version": "4.1.0"
                }
            ],
            "tenant_id": null
        }

task_ext_id:
    description:
        - The external ID of the compute-notifications task.
    returned: always
    type: str
    sample: "ZXJnb24=:f2efc360-5377-42d3-8e69-f5e3cd7d8f83"

ext_id:
    description:
        - The external ID of the LCM notification resource created by the action.
        - The resource is server-managed and remains valid for one hour after creation.
    returned: when the notification resource external ID is present on the task completion details
    type: str
    sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

skipped:
    description: This indicates whether the task was skipped.
    returned: when applicable
    type: bool
    sample: false

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
    returned: When there is an error or in check mode
    type: str
    sample: "Api Exception raised while computing LCM notifications"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_notifications_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_notification  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as life_cycle_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as life_cycle_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the argument spec for the compute-notifications action module."""

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            obj=life_cycle_management_sdk.EntityUpdateSpec,
            required=True,
        ),
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def _build_notifications_spec(module):
    """Build a NotificationsSpec object from the module params.

    The SDK's NotificationsSpec exposes the target entities via the
    C(notifications_spec) attribute (a list of C(EntityUpdateSpec) objects).
    The Ansible module keeps the C(entity_update_specs) option name for
    consistency with other LCM v2 action modules, so we translate the
    per-element dict inputs into SDK EntityUpdateSpec instances here.
    """
    entity_update_specs = []
    for item in module.params.get("entity_update_specs") or []:
        entity_update_specs.append(
            life_cycle_management_sdk.EntityUpdateSpec(
                entity_uuid=item.get("entity_uuid"),
                to_version=item.get("to_version"),
            )
        )
    return life_cycle_management_sdk.NotificationsSpec(
        notifications_spec=entity_update_specs
    )


def compute_notifications(module, api_instance, result):
    """Trigger the compute-notifications LCM action and populate the result dict."""
    validate_required_params(module, ["entity_update_specs"])
    cluster_ext_id = module.params.get("cluster_ext_id")

    try:
        spec = _build_notifications_spec(module)
    except Exception as e:
        result["error"] = str(e)
        module.fail_json(
            msg="Failed generating LCM compute-notifications spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.compute_notifications(
            body=spec, X_Cluster_Id=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while computing LCM notifications",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        notification_ext_id = get_ext_id_from_task_completion_details(task_status)
        if notification_ext_id:
            result["ext_id"] = notification_ext_id
            notifications_api = get_notifications_api_instance(module)
            notification = get_lcm_notification(
                module, notifications_api, notification_ext_id
            )
            result["response"] = strip_internal_attributes(notification.to_dict())

    result["changed"] = True


def run_module():
    """Ansible entry point orchestrating the compute-notifications action."""

    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
        "ext_id": None,
        "failed": False,
    }

    api_instance = get_notifications_api_instance(module)

    compute_notifications(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
