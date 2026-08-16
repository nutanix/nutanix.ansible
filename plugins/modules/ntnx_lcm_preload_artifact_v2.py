#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_preload_artifact_v2
short_description: Preload LCM artifacts on to a Nutanix cluster
version_added: 2.7.0
description:
    - This module allows you to preload LCM (Life Cycle Manager) artifacts on to a Nutanix cluster
      using Prism Central v4 APIs.
    - Preloading downloads the target upgrade images to the cluster nodes ahead of the actual
      upgrade so that the subsequent upgrade window is shorter.
    - The operation is asynchronous - the module returns the task response and, when
      C(wait) is true, waits for the task to reach a terminal state.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Preload artifacts on the cluster.) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will trigger preload of LCM artifacts.
            - Any other value is not supported.
        type: str
        choices:
            - present
        default: present
    entity_update_specs:
        description:
            - List of entity update objects that identify which LCM entities to preload and to
              which version.
            - Each element pairs an LCM entity UUID with its target version. The entity UUIDs
              are obtained by running an LCM inventory and listing the LCM entities.
        type: list
        elements: dict
        required: true
        suboptions:
            entity_uuid:
                description:
                    - UUID of the LCM entity for which artifacts should be preloaded.
                    - Discover this using M(nutanix.ncp.ntnx_lcm_entities_info_v2) after
                      running an LCM inventory.
                type: str
                required: true
            to_version:
                description:
                    - Target version to which the entity's artifacts should be preloaded.
                    - Must be one of the available versions reported for the entity.
                type: str
                required: true
    cluster_ext_id:
        description:
            - External ID of the cluster on which the preload operation should be performed.
            - When not set, the operation is performed against Prism Central itself.
            - Pass the Prism Element cluster external ID (mapped to the C(X-Cluster-Id) header)
              to preload artifacts on a specific PE cluster.
            - You can fetch the cluster external ID using M(nutanix.ncp.ntnx_clusters_info_v2).
        type: str
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
- name: Preload LCM artifacts for a specific entity on Prism Central
  nutanix.ncp.ntnx_lcm_preload_artifact_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    entity_update_specs:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.0.0"
  register: preload_result

- name: Preload LCM artifacts on a specific Prism Element cluster
  nutanix.ncp.ntnx_lcm_preload_artifact_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    cluster_ext_id: "00062db4-a450-e685-0fda-cdf9ca935bfd"
    entity_update_specs:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.0.0"
      - entity_uuid: "15570c98-beaf-4633-afd2-b6a306ff1001"
        to_version: "5.0.0"
  register: preload_result_pe
"""

RETURN = r"""
response:
    description:
        - Response for preloading LCM artifacts.
        - It will contain the task info; when C(wait) is true, it is the terminal task
          response of the preload operation.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": ["cae459ec-08db-475e-a5e5-151e390c9484"],
            "completed_time": "2026-07-20T14:50:14.741791+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T14:50:13.996963+00:00",
            "entities_affected": null,
            "error_messages": [
                {
                    "arguments_map": {
                        "cluster_uuid": "cae459ec-08db-475e-a5e5-151e390c9484",
                        "name": "preloadArtifacts",
                        "opName": "Inventory",
                        "task_uuid": "ef3c47f4-3675-48df-57b9-4e633125de91"
                    },
                    "code": "LIF-10006",
                    "error_group": "OPERATION_IN_PROGRESS_ERROR",
                    "locale": "en_US",
                    "message": "Failed to perform the operation preloadArtifacts on cluster cae459ec-08db-475e-a5e5-151e390c9484 due to an ongoing operation Inventory and root task ef3c47f4-3675-48df-57b9-4e633125de91.",
                    "severity": "ERROR"
                }
            ],
            "ext_id": "ZXJnb24=:2a57e142-a34a-52ee-8103-810e674da40c",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T14:50:14.741789+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 0,
            "operation": "PreloadArtifacts",
            "operation_description": "Preload Artifacts",
            "owned_by": {"ext_id": "00000000-0000-0000-0000-000000000000", "name": "admin"},
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-07-20T14:50:13.996963+00:00",
            "status": "FAILED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: The external ID of the preload task returned by the API.
    returned: always
    type: str
    sample: "ZXJnb24=:2a57e142-a34a-52ee-8103-810e674da40c"
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true
msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while preloading LCM artifacts"
error:
    description:
        - This field typically holds information about if the task have errors that occurred
          during the task execution.
    returned: When an error occurs
    type: str
    sample: "Failed generating spec for preloading LCM artifacts"
failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_entity_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            required=True,
            obj=life_cycle_management_sdk.EntityUpdateSpec,
        ),
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def preload_artifacts(module, api_instance, result):
    """Trigger the LCM preload-artifacts action.

    Builds a ``PreloadSpec`` from the module params, invokes
    ``EntitiesApi.preload_artifacts``, captures the returned task, and (when
    ``wait`` is true) polls the task until completion.
    """
    cluster_ext_id = module.params.get("cluster_ext_id")

    sg = SpecGenerator(module)
    default_spec = life_cycle_management_sdk.PreloadSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for preloading LCM artifacts", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.preload_artifacts(X_Cluster_Id=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while preloading LCM artifacts",
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
    }

    api_instance = get_entity_api_instance(module)
    preload_artifacts(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
