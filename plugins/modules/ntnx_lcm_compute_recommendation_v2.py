#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_compute_recommendation_v2
short_description: Compute LCM update recommendations for a set of entities
version_added: "2.7.0"
description:
    - Compute LCM update recommendations for a set of entities.
    - An LCM inventory should be completed before calling this module.
    - This module uses PC v4 APIs based SDKs
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
            - If C(state) is C(present), the module will compute LCM update recommendations.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - Cluster UUID for which recommendations are computed.
            - When omitted, recommendations are computed on Prism Central.
            - Passed to the API as the C(X-Cluster-Id) header.
        type: str
        required: false
    recommendation_spec:
        description:
            - Specification for computing upgrade recommendations.
            - Corresponds to the API C(recommendationSpec) oneOf body field.
            - Exactly one of the mutually exclusive suboptions must be provided.
        type: dict
        required: true
        suboptions:
            entity_types:
                description:
                    - List of LCM entity types to compute recommendations for.
                    - Mutually exclusive with I(entity_update_specs), I(target_entities)
                      and I(entity_deploy_specs).
                type: list
                elements: str
                choices:
                    - FIRMWARE
                    - SOFTWARE
            entity_update_specs:
                description:
                    - Explicit list of update specifications for recommendations.
                    - Mutually exclusive with I(entity_types), I(target_entities) and
                      I(entity_deploy_specs).
                type: list
                elements: dict
                suboptions:
                    entity_uuid:
                        description:
                            - External identifier of the LCM entity to update.
                        type: str
                        required: true
                    to_version:
                        description:
                            - Target version for the entity update.
                        type: str
                        required: true
            target_entities:
                description:
                    - Explicit list of target entities for recommendations.
                    - Mutually exclusive with I(entity_types), I(entity_update_specs)
                      and I(entity_deploy_specs).
                type: list
                elements: dict
                suboptions:
                    version:
                        description:
                            - The requested update version of an LCM entity.
                        type: str
                        required: true
                    device_id:
                        description:
                            - Unique identifier of an LCM entity, for example an HDD serial number.
                        type: str
                    entity_class:
                        description:
                            - LCM entity class (for example C(Core Cluster)).
                        type: str
                    entity_model:
                        description:
                            - LCM entity model (for example C(AOS)).
                        type: str
                    entity_type:
                        description:
                            - Type of an LCM entity.
                        type: str
                        choices:
                            - FIRMWARE
                            - SOFTWARE
                    entity_version:
                        description:
                            - Current version of an LCM entity.
                        type: str
                    hardware_family:
                        description:
                            - Hardware family for an LCM entity (for example C(dell_gen_12)).
                        type: str
                    location_info:
                        description:
                            - Location info for the entity (location type and optional name).
                            - C(uuid) is read-only in the API and is not accepted by this module.
                        type: dict
                        suboptions:
                            location_type:
                                description:
                                    - Scope of the entity location (PC, cluster, or node).
                                type: str
                                choices:
                                    - PC
                                    - CLUSTER
                                    - NODE
                            location_name:
                                description:
                                    - Name of the location (for example a node hostname).
                                type: str
            entity_deploy_specs:
                description:
                    - Explicit list of deploy specifications for recommendations.
                    - Mutually exclusive with I(entity_types), I(entity_update_specs)
                      and I(target_entities).
                type: list
                elements: dict
                suboptions:
                    entity_identifier:
                        description:
                            - LCM entity identifier used to select the entity to deploy.
                        type: dict
                        required: true
                        suboptions:
                            entity_class:
                                description:
                                    - LCM entity class (for example C(Core Cluster)).
                                type: str
                            entity_model:
                                description:
                                    - LCM entity model (for example C(AOS)).
                                type: str
                            entity_type:
                                description:
                                    - Type of an LCM entity.
                                type: str
                                choices:
                                    - FIRMWARE
                                    - SOFTWARE
                            entity_version:
                                description:
                                    - Current version of an LCM entity.
                                type: str
                            hardware_family:
                                description:
                                    - Hardware family for an LCM entity (for example C(dell_gen_12)).
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
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    recommendation_spec:
      entity_types:
        - SOFTWARE
  register: recommendations_task

- name: Compute LCM recommendations for a specific entity target version
  nutanix.ncp.ntnx_lcm_compute_recommendation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    recommendation_spec:
      entity_update_specs:
        - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
          to_version: "4.0.0"
  register: recommendations_task

- name: Compute LCM recommendations for a target entity descriptor
  nutanix.ncp.ntnx_lcm_compute_recommendation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    recommendation_spec:
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
        - Response for compute LCM recommendations.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "completed_time": "2026-07-20T09:11:23.912241+00:00",
            "completion_details": [
                {
                    "name": "resourceId",
                    "value": "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e"
                }
            ],
            "ext_id": "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720",
            "operation": "kLcmRootTask",
            "operation_description": "Compute Recommendations",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720"
ext_id:
    description:
        - The external ID of the recommendation resource from task completion details.
    type: str
    returned: when the task completes and returns a recommendation resource
    sample: "8d3d0c2f-1c8b-4bf1-8a5b-4a2f96b6f97e"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error or in check mode operation
    sample: "Failed generating LCM compute recommendations Spec"
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
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

# recommendation_spec oneOf flavours (mutually exclusive suboptions).
RECOMMENDATION_SPEC_INPUTS = (
    "entity_types",
    "entity_update_specs",
    "target_entities",
    "entity_deploy_specs",
)


def get_module_spec():

    location_info_spec = dict(
        location_type=dict(type="str", choices=LOCATION_TYPE_CHOICES),
        location_name=dict(type="str"),
    )

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    target_entity_spec = dict(
        version=dict(type="str", required=True),
        device_id=dict(type="str"),
        entity_class=dict(type="str"),
        entity_model=dict(type="str"),
        entity_type=dict(type="str", choices=ENTITY_TYPE_CHOICES),
        entity_version=dict(type="str"),
        hardware_family=dict(type="str"),
        location_info=dict(
            type="dict",
            options=location_info_spec,
            obj=lifecycle_sdk.LocationInfo,
        ),
    )

    entity_base_model_spec = dict(
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
            obj=lifecycle_sdk.EntityBaseModel,
            required=True,
        ),
    )

    recommendation_spec_options = dict(
        entity_types=dict(
            type="list",
            elements="str",
            choices=ENTITY_TYPE_CHOICES,
        ),
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            obj=lifecycle_sdk.EntityUpdateSpec,
        ),
        target_entities=dict(
            type="list",
            elements="dict",
            options=target_entity_spec,
            obj=lifecycle_sdk.TargetEntity,
        ),
        entity_deploy_specs=dict(
            type="list",
            elements="dict",
            options=entity_deploy_spec,
            obj=lifecycle_sdk.EntityDeploySpec,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str"),
        recommendation_spec=dict(
            type="dict",
            required=True,
            options=recommendation_spec_options,
            mutually_exclusive=[list(RECOMMENDATION_SPEC_INPUTS)],
            required_one_of=[list(RECOMMENDATION_SPEC_INPUTS)],
        ),
    )

    return module_args


def _prepare_recommendation_spec_for_generator(module):
    """Expand nested oneOf into the SDK recommendation_spec list field.

    SpecGenerator matches module param names to SDK attributes. The API field is
    C(recommendationSpec) (a oneOf list); Ansible nests the four flavours under
    C(recommendation_spec) for mutual exclusion. Flatten the selected flavour so
    C(sg.generate_spec(obj=RecommendationSpec())) works like other modules.
    """
    rec = module.params.get("recommendation_spec") or {}
    selected = [name for name in RECOMMENDATION_SPEC_INPUTS if rec.get(name)]
    flavour = selected[0]
    value = rec[flavour]
    flavour_schema = module.argument_spec_with_extra_keys["recommendation_spec"][
        "options"
    ][flavour]

    if flavour == "entity_types":
        module.params["recommendation_spec"] = [
            getattr(lifecycle_sdk.EntityType, item) for item in value
        ]
        module.argument_spec_with_extra_keys["recommendation_spec"] = dict(
            type="list",
            elements="str",
            choices=ENTITY_TYPE_CHOICES,
        )
        return

    module.params["recommendation_spec"] = value
    module.argument_spec_with_extra_keys["recommendation_spec"] = flavour_schema


def compute_lcm_recommendations(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    _prepare_recommendation_spec_for_generator(module)

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.RecommendationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating LCM compute recommendations Spec",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "LCM compute recommendations will be performed."
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
                msg=("Failed to get entity ext_id from task for LCM recommendation"),
                **result,
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
        "failed": False,
        "response": None,
        "ext_id": None,
    }

    api_instance = get_recommendations_api_instance(module)

    compute_lcm_recommendations(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
