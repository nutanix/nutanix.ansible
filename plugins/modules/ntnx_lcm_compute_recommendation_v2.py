#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_compute_recommendation_v2
short_description: Compute LCM update recommendations for a set of entities
version_added: 2.5.0
description:
    - This module computes LCM (Life Cycle Manager) update recommendations for a
      given set of entities in Nutanix Prism Central.
    - This module invokes the LCM v4 recommendations action C(POST
      /lifecycle/v4.2/operations/$actions/compute-recommendations) which
      returns a task reference. Once the task completes, the recommendation
      resource external ID is available from the task's C(completion_details)
      and can be fetched via M(nutanix.ncp.ntnx_compute_recommendations_info_v2).
    - The caller must have completed an LCM inventory before calling this
      module so the recommendations engine has fresh entity data to work with.
    - This module uses PC v4 APIs based SDKs.
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Compute LCM update recommendations for a set of entities.) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If state is C(present), the module will compute LCM update recommendations.
            - The C(absent) state is not supported for this action-style module.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - External identifier of the cluster on which the operation should
              be performed. It is passed to the API as the C(X-Cluster-Id)
              header.
            - If nothing is passed, the recommendations are computed on the
              Prism Central. If a Prism Element (PE) cluster external ID is
              passed, the recommendations are computed on that PE cluster.
            - Use M(nutanix.ncp.ntnx_clusters_info_v2) to look up the external
              ID of the cluster.
        type: str
        required: false
    entity_types:
        description:
            - List of LCM entity types to compute recommendations for. When
              provided, LCM returns recommendations for all entities of these
              types available on the target cluster / Prism Central.
            - Mutually exclusive with I(entity_update_specs), I(target_entities)
              and I(entity_deploy_specs).
        type: list
        elements: str
        choices:
            - FIRMWARE
            - SOFTWARE
    entity_update_specs:
        description:
            - Explicit list of update specifications to compute recommendations
              for. Each item pins an LCM entity to a target version.
            - Mutually exclusive with I(entity_types), I(target_entities) and
              I(entity_deploy_specs).
        type: list
        elements: dict
        suboptions:
            entity_uuid:
                description:
                    - External identifier of the LCM entity to update. Use
                      M(nutanix.ncp.ntnx_lcm_entities_info_v2) to look it up.
                type: str
                required: true
            to_version:
                description:
                    - Target version for the entity update.
                type: str
                required: true
    target_entities:
        description:
            - Explicit list of target entities for which to compute
              recommendations. Each item describes an LCM entity plus the
              desired target C(version).
            - Mutually exclusive with I(entity_types), I(entity_update_specs)
              and I(entity_deploy_specs).
        type: list
        elements: dict
        suboptions:
            version:
                description:
                    - Target version for the entity.
                type: str
            device_id:
                description:
                    - Device identifier for firmware entities that are pinned
                      to a specific device.
                type: str
            entity_class:
                description:
                    - Entity class as reported by LCM inventory (for example
                      C(PC CORE CLUSTER)).
                type: str
            entity_model:
                description:
                    - Entity model as reported by LCM inventory (for example
                      C(Calm Policy Engine)).
                type: str
            entity_type:
                description:
                    - Type of the LCM entity.
                type: str
                choices:
                    - FIRMWARE
                    - SOFTWARE
            entity_version:
                description:
                    - Current version of the entity as reported by LCM
                      inventory.
                type: str
            hardware_family:
                description:
                    - Hardware family for firmware entities.
                type: str
            ext_id:
                description:
                    - External identifier of the LCM entity as returned by
                      M(nutanix.ncp.ntnx_lcm_entities_info_v2).
                type: str
            location_info:
                description:
                    - Location on which the entity lives.
                type: dict
                suboptions:
                    uuid:
                        description:
                            - External identifier of the location.
                        type: str
                    location_type:
                        description:
                            - Type of the location.
                        type: str
                        choices:
                            - PC
                            - CLUSTER
                            - NODE
                    location_name:
                        description:
                            - Human readable name of the location.
                        type: str
    entity_deploy_specs:
        description:
            - Explicit list of deploy specifications used to add new entities
              to the cluster via LCM. Each item wraps an entity descriptor.
            - Mutually exclusive with I(entity_types), I(entity_update_specs)
              and I(target_entities).
        type: list
        elements: dict
        suboptions:
            entity_identifier:
                description:
                    - LCM entity identifier used to select the entity to
                      deploy.
                type: dict
                required: true
                suboptions:
                    ext_id:
                        description:
                            - External identifier of the entity.
                        type: str
                    entity_class:
                        description:
                            - Entity class as reported by LCM inventory.
                        type: str
                    entity_model:
                        description:
                            - Entity model as reported by LCM inventory.
                        type: str
                    entity_type:
                        description:
                            - Type of the LCM entity.
                        type: str
                        choices:
                            - FIRMWARE
                            - SOFTWARE
                    entity_version:
                        description:
                            - Current version of the entity.
                        type: str
                    hardware_family:
                        description:
                            - Hardware family for firmware entities.
                        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Compute LCM recommendations for all SOFTWARE entities on Prism Central
  nutanix.ncp.ntnx_lcm_compute_recommendation_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    entity_types:
      - SOFTWARE
  register: recommendations_task

- name: Compute LCM recommendations for a specific entity target version
  nutanix.ncp.ntnx_lcm_compute_recommendation_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    entity_update_specs:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.0.0"
  register: recommendations_task

- name: Compute LCM recommendations for a target entity descriptor
  nutanix.ncp.ntnx_lcm_compute_recommendation_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    target_entities:
      - entity_type: SOFTWARE
        entity_model: "Calm Policy Engine"
        entity_version: "3.8.0"
        version: "4.0.0"
  register: recommendations_task
"""

RETURN = r"""
response:
    description:
        - Response returned by the compute-recommendations action.
        - When I(wait) is C(true) (the default), this is the final Prism task
          object once the compute-recommendations task has reached a terminal
          state.
        - When I(wait) is C(false), this is the initial task reference returned
          by the API.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T09:11:23.912241+00:00",
            "completion_details": [
                {
                    "name": "resourceId",
                    "value": "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e"
                }
            ],
            "created_time": "2026-07-20T09:10:58.314367+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T09:11:23.912240+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 0,
            "operation": "kLcmRootTask",
            "operation_description": "Compute Recommendations",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-07-20T09:10:58.314367+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: External identifier of the compute-recommendations task.
    type: str
    returned: always
    sample: "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720"
ext_id:
    description:
        - External identifier of the recommendation resource produced by the
          task. It is extracted from the task's C(completion_details) after
          successful completion and can be used with
          M(nutanix.ncp.ntnx_compute_recommendations_info_v2) to fetch the
          detailed recommendation payload.
    type: str
    returned: when the task completes and returns a recommendation resource
    sample: "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e"
changed:
    description: Whether the module made any changes on the cluster.
    type: bool
    returned: always
    sample: true
skipped:
    description: Whether the action was skipped (only set in check mode).
    type: bool
    returned: when applicable
    sample: false
failed:
    description: Whether the module invocation failed.
    type: bool
    returned: always
    sample: false
msg:
    description: Status or error message.
    type: str
    returned: contextual
    sample: "Api Exception raised while computing LCM recommendations"
error:
    description: Details about any error encountered.
    type: str
    returned: When an error occurs
    sample: "Failed generating compute recommendations spec"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_recommendations_api_instance,
)
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

ENTITY_TYPE_CHOICES = ["FIRMWARE", "SOFTWARE"]
LOCATION_TYPE_CHOICES = ["PC", "CLUSTER", "NODE"]

# Only one of these input flavours may be supplied at a time — they map to
# the OneOf `recommendationSpec` field on the SDK request body.
RECOMMENDATION_SPEC_INPUTS = (
    "entity_types",
    "entity_update_specs",
    "target_entities",
    "entity_deploy_specs",
)


def get_module_spec():

    location_info_spec = dict(
        uuid=dict(type="str"),
        location_type=dict(type="str", choices=LOCATION_TYPE_CHOICES),
        location_name=dict(type="str"),
    )

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    target_entity_spec = dict(
        version=dict(type="str"),
        device_id=dict(type="str"),
        entity_class=dict(type="str"),
        entity_model=dict(type="str"),
        entity_type=dict(type="str", choices=ENTITY_TYPE_CHOICES),
        entity_version=dict(type="str"),
        hardware_family=dict(type="str"),
        ext_id=dict(type="str"),
        location_info=dict(type="dict", options=location_info_spec),
    )

    entity_base_model_spec = dict(
        ext_id=dict(type="str"),
        entity_class=dict(type="str"),
        entity_model=dict(type="str"),
        entity_type=dict(type="str", choices=ENTITY_TYPE_CHOICES),
        entity_version=dict(type="str"),
        hardware_family=dict(type="str"),
    )

    entity_deploy_spec = dict(
        entity_identifier=dict(
            type="dict",
            options=entity_base_model_spec,
            required=True,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str"),
        entity_types=dict(
            type="list",
            elements="str",
            choices=ENTITY_TYPE_CHOICES,
        ),
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
        ),
        target_entities=dict(
            type="list",
            elements="dict",
            options=target_entity_spec,
        ),
        entity_deploy_specs=dict(
            type="list",
            elements="dict",
            options=entity_deploy_spec,
        ),
    )

    return module_args


def _build_location_info(data):
    if not data:
        return None
    loc = lifecycle_sdk.LocationInfo()
    if data.get("uuid") is not None:
        loc.uuid = data["uuid"]
    if data.get("location_type") is not None:
        loc.location_type = getattr(lifecycle_sdk.LocationType, data["location_type"])
    if data.get("location_name") is not None:
        loc.location_name = data["location_name"]
    return loc


def _copy_entity_base_fields(target, data):
    """Copy shared LCM entity fields from a dict on to an SDK object."""

    if data.get("ext_id") is not None:
        target.ext_id = data["ext_id"]
    if data.get("entity_class") is not None:
        target.entity_class = data["entity_class"]
    if data.get("entity_model") is not None:
        target.entity_model = data["entity_model"]
    if data.get("entity_type") is not None:
        target.entity_type = getattr(lifecycle_sdk.EntityType, data["entity_type"])
    if data.get("entity_version") is not None:
        target.entity_version = data["entity_version"]
    if data.get("hardware_family") is not None:
        target.hardware_family = data["hardware_family"]


def _build_entity_update_specs(items):
    specs = []
    for item in items:
        spec = lifecycle_sdk.EntityUpdateSpec(
            entity_uuid=item["entity_uuid"],
            to_version=item["to_version"],
        )
        specs.append(spec)
    return specs


def _build_target_entities(items):
    specs = []
    for item in items:
        te = lifecycle_sdk.TargetEntity()
        _copy_entity_base_fields(te, item)
        if item.get("version") is not None:
            te.version = item["version"]
        if item.get("device_id") is not None:
            te.device_id = item["device_id"]
        loc = _build_location_info(item.get("location_info"))
        if loc is not None:
            te.location_info = loc
        specs.append(te)
    return specs


def _build_entity_deploy_specs(items):
    specs = []
    for item in items:
        ident_data = item.get("entity_identifier") or {}
        identifier = lifecycle_sdk.EntityBaseModel()
        _copy_entity_base_fields(identifier, ident_data)
        deploy_spec = lifecycle_sdk.EntityDeploySpec(entity_identifier=identifier)
        specs.append(deploy_spec)
    return specs


def _selected_recommendation_input(module):
    selected = [name for name in RECOMMENDATION_SPEC_INPUTS if module.params.get(name)]
    return selected


def _build_recommendation_spec_body(module, result):
    """Assemble the SDK `RecommendationSpec` request body from module params."""

    selected = _selected_recommendation_input(module)
    if not selected:
        result["error"] = (
            "One of {0} must be supplied to compute LCM recommendations".format(
                ", ".join(RECOMMENDATION_SPEC_INPUTS)
            )
        )
        module.fail_json(msg="Missing recommendation spec input", **result)

    body = lifecycle_sdk.RecommendationSpec()
    input_name = selected[0]
    params = module.params

    if input_name == "entity_types":
        body.recommendation_spec = [
            getattr(lifecycle_sdk.EntityType, value) for value in params["entity_types"]
        ]
    elif input_name == "entity_update_specs":
        body.recommendation_spec = _build_entity_update_specs(
            params["entity_update_specs"]
        )
    elif input_name == "target_entities":
        body.recommendation_spec = _build_target_entities(params["target_entities"])
    elif input_name == "entity_deploy_specs":
        body.recommendation_spec = _build_entity_deploy_specs(
            params["entity_deploy_specs"]
        )

    return body


def compute_lcm_recommendations(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    spec = _build_recommendation_spec_body(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = True
        result["msg"] = (
            "Compute LCM recommendations was skipped due to check_mode. "
            "Returning the generated spec instead."
        )
        return

    try:
        resp = api_instance.compute_recommendations(
            body=spec, X_Cluster_Id=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while computing LCM recommendations",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True

    if task_ext_id and module.params.get("wait"):
        # raise_error=False keeps the task_ext_id and other context we've
        # already stashed on `result`; we surface any FAILED status ourselves
        # so the caller sees the full task payload.
        task = wait_for_completion(module, task_ext_id, raise_error=False)
        task_dict = strip_internal_attributes(task.to_dict())
        result["response"] = task_dict

        task_status = task_dict.get("status")
        if task_status != "SUCCEEDED":
            result["failed"] = True
            module.fail_json(
                msg=(
                    "Compute LCM recommendations task ended with status "
                    "{0}".format(task_status)
                ),
                **result,
            )

        recommendation_ext_id = get_ext_id_from_task_completion_details(
            data=task, name="resourceId"
        )
        if recommendation_ext_id:
            result["ext_id"] = recommendation_ext_id
        else:
            module.fail_json(
                msg=(
                    "Compute LCM recommendations task completed but the "
                    "recommendation resource ext_id was not present in the "
                    "task completion details"
                ),
                **result,
            )


def run_module():

    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            list(RECOMMENDATION_SPEC_INPUTS),
        ],
        required_one_of=[
            list(RECOMMENDATION_SPEC_INPUTS),
        ],
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
    }

    api_instance = get_recommendations_api_instance(module)

    compute_lcm_recommendations(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
