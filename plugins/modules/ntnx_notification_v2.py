#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_notification_v2
short_description: Compute LCM upgrade plan and notifications for a set of entities
version_added: 2.7.0
description:
  - This module allows you to compute the LCM (Life Cycle Manager) upgrade plan and
    notifications for a set of LCM entities and their target versions in Nutanix Prism Central.
  - The compute-notifications API generates upgrade notifications (for example, host
    location moves, entity-level warnings, non-migratable VM information) that must be
    reviewed before actually performing the upgrade.
  - This is an asynchronous API; the module creates a task and, when C(wait) is true,
    waits for the task to complete and fetches the resulting notification resource by
    its external ID.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Compute LCM upgrade notifications) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present) the module will compute LCM upgrade notifications.
      - Notifications resource does not expose an update or delete API, so C(absent)
        is not supported.
    type: str
    choices:
      - present
    default: present
  notifications_spec:
    description:
      - List of LCM entities and the target versions for which the upgrade plan and
        notifications should be computed.
      - Corresponds to the C(notificationsSpec) body attribute of the LCM v4
        compute-notifications API.
      - Required for the compute-notifications operation.
    type: list
    elements: dict
    required: true
    suboptions:
      entity_uuid:
        description:
          - UUID of the LCM entity to be upgraded.
          - Can be obtained via M(nutanix.ncp.ntnx_lcm_entities_info_v2) after running
            an LCM inventory.
        type: str
        required: true
      to_version:
        description:
          - Version to upgrade the entity to.
          - Must be one of the available versions reported for the entity by LCM.
        type: str
        required: true
  cluster_ext_id:
    description:
      - Cluster external ID on which the compute-notifications operation should be
        performed.
      - If not provided, the operation targets the Prism Central itself; if the
        external ID of a Prism Element cluster is provided, the operation targets
        that PE cluster.
      - We can get the external ID of a cluster using
        M(nutanix.ncp.ntnx_clusters_info_v2).
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
- name: Compute LCM upgrade notifications for a PC entity
  nutanix.ncp.ntnx_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    notifications_spec:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.1.0"
  register: notification_result

- name: Compute LCM upgrade notifications for a PE cluster entity
  nutanix.ncp.ntnx_notification_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db4-a450-e685-0fda-cdf9ca935bfd"
    notifications_spec:
      - entity_uuid: "15570c98-beaf-4633-afd2-b6a306ff1001"
        to_version: "5.0.0"
      - entity_uuid: "7f8e2a1c-1234-4321-9abc-def012345678"
        to_version: "3.2.1"
  register: notification_result
"""

RETURN = r"""
response:
  description:
    - Response for the compute-notifications operation.
    - When C(wait) is true and the task succeeds, this contains the LCM upgrade
      notification resource (list of per-entity notification items with severity
      levels, messages, target versions, location info and hypervisor type).
    - When C(wait) is false, this contains the task reference details.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_id": null,
        "ext_id": "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5",
        "links": null,
        "notifications": [
            {
                "details": [
                    {
                        "message": "Host will enter maintenance mode during upgrade.",
                        "severity_level": "WARNING"
                    }
                ],
                "entity_class": "PC CORE CLUSTER",
                "entity_model": "Calm Policy Engine",
                "entity_type": "SOFTWARE",
                "entity_version": "3.8.0",
                "ext_id": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
                "hardware_family": null,
                "hypervisor_type": null,
                "location_info": null,
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
  sample: "ZXJnb24=:a784c0b7-1038-49cf-40b5-2845231d242f"

ext_id:
  description:
    - The external ID of the generated LCM upgrade notification resource.
    - Populated once the task completes and the notification ext_id can be resolved
      from the task; used by M(nutanix.ncp.ntnx_lcm_notifications_info_v2) to fetch
      the same resource later.
  returned: when C(wait) is true and the task succeeds
  type: str
  sample: "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5"

changed:
  description: This indicates whether the module made any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: Status/error message emitted by the module.
  returned: When there is an error or an informational message is emitted
  type: str
  sample: "Api Exception raised while computing LCM upgrade notifications"

error:
  description: Error details if the module failed.
  returned: When an error occurs
  type: str
  sample: "Failed generating spec for computing LCM upgrade notifications"

failed:
  description: This indicates whether the module failed.
  returned: always
  type: bool
  sample: false
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
    get_entity_ext_id_from_task,
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        notifications_spec=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            required=True,
            obj=life_cycle_management_sdk.EntityUpdateSpec,
        ),
        cluster_ext_id=dict(type="str", required=False),
    )

    return module_args


def _resolve_notification_ext_id(task):
    """
    Best-effort resolution of the notification resource ext_id from the compute
    notifications task. The task's entities_affected typically carries the newly
    created notification's ext_id; the completion_details may also carry it under
    a name such as "notificationExtId"/"resourceId".
    """
    ext_id = get_entity_ext_id_from_task(task)
    if ext_id:
        return ext_id
    for name in ("notificationExtId", "resourceId", "resource_id"):
        ext_id = get_ext_id_from_task_completion_details(task, name=name)
        if ext_id:
            return ext_id
    return None


def compute_notifications(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    validate_required_params(module, ["notifications_spec"])

    sg = SpecGenerator(module)
    default_spec = life_cycle_management_sdk.NotificationsSpec(notifications_spec=[])
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for computing LCM upgrade notifications",
            **result,
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
            msg="Api Exception raised while computing LCM upgrade notifications",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

        notification_ext_id = _resolve_notification_ext_id(task)
        if notification_ext_id:
            result["ext_id"] = notification_ext_id
            notification = get_lcm_notification(
                module, api_instance, notification_ext_id
            )
            if notification is not None:
                result["response"] = strip_internal_attributes(notification.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to resolve LCM notification ext_id from the compute-notifications task"
                ),
                msg="Failed to resolve LCM notification ext_id from the compute-notifications task",
            )


def run_module():
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
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_notifications_api_instance(module)
    compute_notifications(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
