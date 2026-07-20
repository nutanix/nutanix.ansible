#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recommendation_v2
short_description: Compute LCM (Life Cycle Manager) update recommendations
version_added: 2.7.0
description:
  - This module allows you to compute LCM (Life Cycle Manager) update
    recommendations for a set of entities in Nutanix Prism Central.
  - The compute-recommendations API is asynchronous. It kicks off a task and,
    once the task completes, the resulting recommendation resource can be
    fetched with M(nutanix.ncp.ntnx_lcm_recommendations_info_v2) using the
    returned C(ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Compute LCM recommendations.) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported since this is an action-style module that
        computes recommendations on demand.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - External ID of the cluster on which recommendations should be
        computed.
      - It maps to the C(X-Cluster-Id) HTTP header of the underlying v4 API.
      - If omitted, LCM recommendations are computed for the Prism Central.
      - If a Prism Element cluster external ID is passed, recommendations are
        computed for that PE cluster.
    type: str
    required: false
  entity_types:
    description:
      - Compute recommendations for whole categories of LCM entities.
      - Use this variant when you want a broad recommendation across all
        entities of a given type (e.g. all C(SOFTWARE) or all C(FIRMWARE)).
      - Mutually exclusive with C(target_entities), C(entity_update_specs) and
        C(entity_deploy_specs).
    type: list
    elements: str
    choices:
      - SOFTWARE
      - FIRMWARE
    required: false
  target_entities:
    description:
      - Compute recommendations for a list of LCM target entities identified
        by their model / class attributes and a desired target version.
      - Use this variant when the caller does not know the exact
        C(entity_uuid) of every node/component but does know the intended
        C(entity_class), C(entity_model) and C(version).
      - Mutually exclusive with C(entity_types), C(entity_update_specs) and
        C(entity_deploy_specs).
    type: list
    elements: dict
    required: false
    suboptions:
      version:
        description:
          - The requested update version of an LCM entity.
        type: str
        required: true
      device_id:
        description:
          - Unique identifier of an LCM entity (e.g. HDD serial number).
        type: str
        required: false
      entity_class:
        description:
          - LCM entity class (e.g. C(AOS)).
        type: str
        required: false
      entity_model:
        description:
          - LCM entity model.
        type: str
        required: false
      entity_type:
        description:
          - Type of the LCM entity.
        type: str
        required: false
        choices:
          - SOFTWARE
          - FIRMWARE
      entity_version:
        description:
          - Current version of the LCM entity.
        type: str
        required: false
      hardware_family:
        description:
          - Hardware family of the LCM entity.
        type: str
        required: false
      ext_id:
        description:
          - External ID of the LCM entity.
        type: str
        required: false
      location_info:
        description:
          - Location of the LCM entity — a tuple of location type
            (node / cluster / PC) and its UUID.
        type: dict
        required: false
        suboptions:
          uuid:
            description:
              - Location UUID of the resource.
            type: str
            required: false
          location_type:
            description:
              - Location type of the LCM entity.
            type: str
            required: false
            choices:
              - NODE
              - CLUSTER
              - PC
          location_name:
            description:
              - Name of the location.
            type: str
            required: false
  entity_update_specs:
    description:
      - Compute recommendations for a list of LCM entities identified
        precisely by their C(entity_uuid) and a target version.
      - Use this variant for strict, exact upgrade planning when the caller
        already has the LCM entity UUID and desired version.
      - Mutually exclusive with C(entity_types), C(target_entities) and
        C(entity_deploy_specs).
    type: list
    elements: dict
    required: false
    suboptions:
      entity_uuid:
        description:
          - UUID of the LCM entity to consider for update.
        type: str
        required: true
      to_version:
        description:
          - Target version for the LCM entity.
        type: str
        required: true
  entity_deploy_specs:
    description:
      - Compute recommendations for entities that are about to be deployed
        (do not exist yet on the cluster).
      - Use this variant when planning a fresh deployment (e.g. new File
        Server, PC, or Nutanix Infrastructure Manager) so LCM can validate
        dependencies before the deployment starts.
      - Mutually exclusive with C(entity_types), C(target_entities) and
        C(entity_update_specs).
    type: list
    elements: dict
    required: false
    suboptions:
      entity_identifier:
        description:
          - Identifier of the LCM entity being deployed.
        type: dict
        required: true
        suboptions:
          entity_class:
            description:
              - LCM entity class.
            type: str
            required: false
          entity_model:
            description:
              - LCM entity model.
            type: str
            required: false
          entity_type:
            description:
              - Type of the LCM entity.
            type: str
            required: false
            choices:
              - SOFTWARE
              - FIRMWARE
          entity_version:
            description:
              - Version of the LCM entity being deployed.
            type: str
            required: false
          hardware_family:
            description:
              - Hardware family of the LCM entity.
            type: str
            required: false
          ext_id:
            description:
              - External ID of the LCM entity.
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
- name: Compute LCM recommendations for all SOFTWARE entities on Prism Central
  nutanix.ncp.ntnx_recommendation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    entity_types:
      - SOFTWARE
  register: result
  ignore_errors: true

- name: Compute LCM recommendations for a specific entity by UUID
  nutanix.ncp.ntnx_recommendation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db4-a450-e685-0fda-cdf9ca935bfd"
    entity_update_specs:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
        to_version: "4.0.0"
  register: result
  ignore_errors: true

- name: Compute LCM recommendations using target entity model + version
  nutanix.ncp.ntnx_recommendation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    target_entities:
      - entity_class: "PC CORE CLUSTER"
        entity_model: "Calm Policy Engine"
        entity_type: "SOFTWARE"
        version: "4.0.0"
        location_info:
          location_type: "PC"
          uuid: "1e9a1996-50e2-485f-a67c-22355cb43055"
  register: result
  ignore_errors: true

- name: Compute LCM recommendations for a new deployment (deploy spec)
  nutanix.ncp.ntnx_recommendation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    entity_deploy_specs:
      - entity_identifier:
          entity_class: "PC CORE CLUSTER"
          entity_model: "File Server Manager"
          entity_type: "SOFTWARE"
          entity_version: "5.0.0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for computing LCM recommendations.
    - When C(wait) is C(true), it returns the LCM recommendation resource
      (dictionary of update recommendations) if the API surfaced a
      recommendation C(ext_id) in the task; otherwise it returns the
      completed task details.
    - When C(wait) is C(false), it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "addable_entities": null,
      "cluster_ext_id": "1e9a1996-50e2-485f-a67c-22355cb43055",
      "deployable_versions": [],
      "entity_update_specs": [
        {
          "entity_uuid": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
          "to_version": "4.0.0"
        }
      ],
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "links": null,
      "modifiable_entities": null,
      "skipped_entities": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task that computes recommendations.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the computed LCM recommendation resource.
    - Populated when the compute task surfaces the recommendation ext_id
      via C(entities_affected) or C(completion_details).
  returned: always
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
  description:
    - Status/error message emitted by the module.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while computing LCM recommendations"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_recommendations_api_instance,
)
from ..module_utils.v4.lcm.helpers import (  # noqa: E402
    build_recommendation_spec,
    get_lcm_recommendation,
)
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
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

    location_info_spec = dict(
        uuid=dict(type="str", required=False),
        location_type=dict(
            type="str",
            required=False,
            choices=["NODE", "CLUSTER", "PC"],
        ),
        location_name=dict(type="str", required=False),
    )

    target_entity_spec = dict(
        version=dict(type="str", required=True),
        device_id=dict(type="str", required=False),
        entity_class=dict(type="str", required=False),
        entity_model=dict(type="str", required=False),
        entity_type=dict(
            type="str",
            required=False,
            choices=["SOFTWARE", "FIRMWARE"],
        ),
        entity_version=dict(type="str", required=False),
        hardware_family=dict(type="str", required=False),
        ext_id=dict(type="str", required=False),
        location_info=dict(
            type="dict",
            options=location_info_spec,
            required=False,
        ),
    )

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    entity_base_model_spec = dict(
        entity_class=dict(type="str", required=False),
        entity_model=dict(type="str", required=False),
        entity_type=dict(
            type="str",
            required=False,
            choices=["SOFTWARE", "FIRMWARE"],
        ),
        entity_version=dict(type="str", required=False),
        hardware_family=dict(type="str", required=False),
        ext_id=dict(type="str", required=False),
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
            choices=["SOFTWARE", "FIRMWARE"],
        ),
        target_entities=dict(
            type="list",
            elements="dict",
            options=target_entity_spec,
        ),
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
        ),
        entity_deploy_specs=dict(
            type="list",
            elements="dict",
            options=entity_deploy_spec,
        ),
    )

    return module_args


def _extract_recommendation_ext_id(task_data):
    """Return the recommendation ext_id from a completed compute task or None."""
    ext_id = get_entity_ext_id_from_task(
        task_data, rel=TASK_CONSTANTS.RelEntityType.LCM_RECOMMENDATION
    )
    if ext_id:
        return ext_id
    # Fallback #1: entities_affected without a specific rel filter.
    ext_id = get_entity_ext_id_from_task(task_data)
    if ext_id:
        return ext_id
    # Fallback #2: completion_details (LCM sometimes reports the recommendation
    # resource id in the task's completion_details map).
    return get_ext_id_from_task_completion_details(task_data)


def compute_recommendations(module, api_instance, result):
    """Kick off the compute-recommendations action and, on completion, fetch
    the resulting recommendation resource."""
    cluster_ext_id = module.params.get("cluster_ext_id")

    spec, err = build_recommendation_spec(module, life_cycle_management_sdk)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating compute LCM recommendations spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
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

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        recommendation_ext_id = _extract_recommendation_ext_id(task)
        if recommendation_ext_id:
            result["ext_id"] = recommendation_ext_id
            recommendation = get_lcm_recommendation(
                module, api_instance, recommendation_ext_id
            )
            result["response"] = strip_internal_attributes(recommendation.to_dict())

    result["changed"] = True


def run_module():

    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            (
                "entity_types",
                "target_entities",
                "entity_update_specs",
                "entity_deploy_specs",
            ),
        ],
        required_one_of=[
            (
                "entity_types",
                "target_entities",
                "entity_update_specs",
                "entity_deploy_specs",
            ),
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
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }

    api_instance = get_recommendations_api_instance(module)
    compute_recommendations(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
