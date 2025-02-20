#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_protection_policies_v2
short_description: Create, Update, Delete protection policy in Nutanix Prism Central
description:
  - This module allows you to create, update, and delete protection policy in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - if C(state) is present, it will create or update the protection policy.
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create protection policy.
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update protection policy.
      - If C(state) is set to C(absent) and ext_id is provided then the operation will be delete protection policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external id of the protection policy.
    type: str
    required: false
  name:
    description:
      - The name of the protection policy.
    type: str
    required: true
  description:
    description:
      - The description of the protection policy.
    type: str
    required: false
  replication_locations:
    description:
      - Indicates all the locations participating in the protection policy.
      - You can specify up to 3 replication locations.
    type: list
    elements: dict
    required: true
    suboptions:
      label:
        description:
          - This is a unique user defined label of the replication location.
          - It is used to identify the location in the replication configurations.
        type: str
        required: true
      domain_manager_ext_id:
        description:
          - The external id of the domain manager.
        type: str
        required: true
      replication_sub_location:
        description:
          - Specifies the replication sublocations where recovery points can be created or replicated.
        type: dict
        required: false
        suboptions:
          nutanix_cluster:
            description:
              - Specifies the Nutanix cluster where the recovery points can be created or replicated.
            type: dict
            required: false
            suboptions:
              cluster_ext_ids:
                description:
                  - Specifies the external ids of the Nutanix cluster.
                type: list
                elements: str
                required: false
      is_primary:
        description:
          - Indicates whether the location is primary or not.
          - One of the locations must be specified as the primary location.
          - All the other locations must be connected to the primary location.
        type: bool
        required: false
  replication_configurations:
    description:
      - Specifies the connections between various replication locations and its schedule.
      - Connections from both source-to-target and target-to-source should be specified.
    type: list
    elements: dict
    required: true
    suboptions:
      source_location_label:
        description:
          - Label of the source location from the replication locations list, where the entity is running.
          - The location of type MST can not be specified as the replication source.
        type: str
        required: true
      remote_location_label:
        description:
          - The label of the remote location.
          - Label of the source location from the replication locations list, where the entity will be replicated.
        type: str
        required: false
      schedule:
        description:
          - Specifies the schedule of the replication.
        type: dict
        required: true
        suboptions:
          recovery_point_type:
            description:
              - Specifies the type of recovery point.
            type: str
            required: false
            choices:
              - CRASH_CONSISTENT
              - APPLICATION_CONSISTENT
          recovery_point_objective_time_seconds:
            description:
              - The Recovery point objective of the schedule in seconds and specified in multiple of 60 seconds.
              - Only following RPO values can be provided for rollup retention type
              - Minute(s) -> 1, 2, 3, 4, 5, 6, 10, 12, 15
              - Hour(s) -> 1, 2, 3, 4, 6, 8, 12
              - Day(s) -> 1
              - Week(s) -> 1, 2
            type: int
            required: true
          retention:
            description:
              - Specifies the retention policy for the recovery point schedule.
            type: dict
            required: false
            suboptions:
              linear_retention:
                description:
                  - Specifies the linear retention policy.
                type: dict
                required: false
                suboptions:
                  local:
                    description:
                      - Specifies the number of recovery points to retain on the local location.
                    type: int
                    required: true
                  remote:
                    description:
                      - Specifies the number of recovery points to retain on the remote location.
                    type: int
                    required: false
              auto_rollup_retention:
                description:
                  - Specifies the auto rollup retention policy.
                type: dict
                required: false
                suboptions:
                  local:
                    description:
                      - Specifies the auto rollup retention policy for the local location.
                    type: dict
                    required: true
                    suboptions:
                      snapshot_interval_type:
                        description:
                          - Specifies the snapshot interval type.
                        type: str
                        required: true
                        choices:
                          - YEARLY
                          - WEEKLY
                          - DAILY
                          - MONTHLY
                          - HOURLY
                      frequency:
                        description:
                          - Specifies the frequency of the snapshot interval.
                        type: int
                        required: true
                  remote:
                    description:
                      - Specifies the auto rollup retention policy for the remote location.
                    type: dict
                    required: false
                    suboptions:
                      snapshot_interval_type:
                        description:
                          - Specifies the snapshot interval type.
                        type: str
                        required: true
                        choices:
                          - YEARLY
                          - WEEKLY
                          - DAILY
                          - MONTHLY
                          - HOURLY
                      frequency:
                        description:
                          - Specifies the frequency of the snapshot interval.
                        type: int
                        required: true
          start_time:
            description:
              - Specifies the start time of the schedule.
            type: str
            required: false
          sync_replication_auto_suspend_timeout_seconds:
            description:
              - Specifies the timeout in seconds for the sync replication to auto suspend.
            type: int
            required: false
  category_ids:
    description:
      - Specifies the list of external identifiers of categories that must be added to the protection policy.
    type: list
    elements: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create linear protection policy
  nutanix.ncp.ntnx_protection_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "linear-protection-policy-name"
    description: "linear-protection-policy-description"
    replication_locations:
      - label: "ansible-label-linear-label1"
        domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
        is_primary: true
      - label: "ansible-label-linear-label2"
        domain_manager_ext_id: "11111111-1111-1111-1111-111111111111"
        is_primary: false
    replication_configurations:
      - source_location_label: "ansible-label-linear-label1"
        remote_location_label: "ansible-label-linear-label2"
        schedule:
          recovery_point_type: "CRASH_CONSISTENT"
          recovery_point_objective_time_seconds: 3600
          retention:
            linear_retention:
              local: 1
              remote: 1
          start_time: "16h:12m"
          sync_replication_auto_suspend_timeout_seconds: 300
      - source_location_label: "ansible-label-linear-label2"
        remote_location_label: "ansible-label-linear-label1"
        schedule:
          recovery_point_type: "CRASH_CONSISTENT"
          recovery_point_objective_time_seconds: 3600
          retention:
            linear_retention:
              local: 1
              remote: 1
          start_time: "16h:12m"
          sync_replication_auto_suspend_timeout_seconds: 300
    category_ids:
      - "22222222-2222-2222-2222-222222222222"
    register: result

- name: Create auto retention protection policy
  nutanix.ncp.ntnx_protection_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "auto-retention-protection-policy-name"
    description: "auto-retention-protection-policy-description"
    replication_locations:
      - label: "ansible-label-auto-label1"
        domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
        is_primary: true
      - label: "ansible-label-auto-label2"
        domain_manager_ext_id: "11111111-1111-1111-1111-111111111111"
        is_primary: false
    replication_configurations:
      - source_location_label: "ansible-label-auto-label1"
        remote_location_label: "ansible-label-auto-label2"
        schedule:
          recovery_point_type: "CRASH_CONSISTENT"
          recovery_point_objective_time_seconds: 3600
          retention:
            auto_rollup_retention:
              local:
                snapshot_interval_type: "DAILY"
                frequency: 1
              remote:
                snapshot_interval_type: "DAILY"
                frequency: 1
          start_time: "16h:12m"
          sync_replication_auto_suspend_timeout_seconds: 300
      - source_location_label: "ansible-label-auto-label2"
        remote_location_label: "ansible-label-auto-label1"
        schedule:
          recovery_point_type: "CRASH_CONSISTENT"
          recovery_point_objective_time_seconds: 3600
          retention:
            auto_rollup_retention:
              local:
                snapshot_interval_type: "DAILY"
                frequency: 1
              remote:
                snapshot_interval_type: "DAILY"
                frequency: 1
          start_time: "16h:12m"
          sync_replication_auto_suspend_timeout_seconds: 300
    category_ids:
      - "22222222-2222-2222-2222-222222222222"
    register: result

- name: Update linear protection policy
  nutanix.ncp.ntnx_protection_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    name: "linear-protection-policy-name-updated"
    description: "linear-protection-policy-description-updated"
    replication_locations:
      - label: "ansible-label-linear-label1"
        domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
        is_primary: true
      - label: "ansible-label-linear-label2"
        domain_manager_ext_id: "11111111-1111-1111-1111-111111111111"
        is_primary: false
    replication_configurations:
      - source_location_label: "ansible-label-linear-label1"
        remote_location_label: "ansible-label-linear-label2"
        schedule:
          recovery_point_type: "CRASH_CONSISTENT"
          recovery_point_objective_time_seconds: 7200
          retention:
            linear_retention:
              local: 2
              remote: 2
          start_time: "16h:12m"
          sync_replication_auto_suspend_timeout_seconds: 90
      - source_location_label: "ansible-label-linear-label2"
        remote_location_label: "ansible-label-linear-label1"
        schedule:
          recovery_point_type: "CRASH_CONSISTENT"
          recovery_point_objective_time_seconds: 7200
          retention:
            linear_retention:
              local: 2
              remote: 2
          start_time: "20h:36m"
          sync_replication_auto_suspend_timeout_seconds: 90
    category_ids:
      - "22222222-2222-2222-2222-222222222222"
    register: result

- name: Delete protection policy
  nutanix.ncp.ntnx_protection_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    state: absent
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting protection policy
    - It will return the protection policy details if the operation is create or update
    - It will return the task details if the operation is delete
  returned: always
  type: dict
  sample:
    {
      "category_ids": ["bbc3555a-133b-5348-9764-bfff196e84e4"],
      "description": "ansible-description-linear-hYTLnwHRltSf",
      "ext_id": "e7ae4b0d-726d-410d-87c2-af46f8bea264",
      "is_approval_policy_needed": null,
      "links": null,
      "name": "ansible-name-linear-hYTLnwHRltSf",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "replication_configurations":
        [
          {
            "remote_location_label": "ansible-label-OSggSJTEEfyG",
            "schedule":
              {
                "recovery_point_objective_time_seconds": 3600,
                "recovery_point_type": "CRASH_CONSISTENT",
                "retention": { "local": 1, "remote": 1 },
                "start_time": "15h:19m",
                "sync_replication_auto_suspend_timeout_seconds": 300,
              },
            "source_location_label": "ansible-label-RQEKSGCttXaN",
          },
          {
            "remote_location_label": "ansible-label-RQEKSGCttXaN",
            "schedule":
              {
                "recovery_point_objective_time_seconds": 3600,
                "recovery_point_type": "CRASH_CONSISTENT",
                "retention": { "local": 1, "remote": 1 },
                "start_time": "15h:19m",
                "sync_replication_auto_suspend_timeout_seconds": 300,
              },
            "source_location_label": "ansible-label-OSggSJTEEfyG",
          },
        ],
      "replication_locations":
        [
          {
            "domain_manager_ext_id": "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f",
            "is_primary": true,
            "label": "ansible-label-RQEKSGCttXaN",
            "replication_sub_location": null,
          },
          {
            "domain_manager_ext_id": "425cd2d4-32e0-4c2d-a026-31d81fa4c805",
            "is_primary": false,
            "label": "ansible-label-OSggSJTEEfyG",
            "replication_sub_location": null,
          },
        ],
      "tenant_id": null,
    }

task_ext_id:
  description:
    - The external id of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

protection_policy_ext_id:
  description:
    - The external id of the protection policy.
  returned: always
  type: str
  sample: "e7ae4b0d-726d-410d-87c2-af46f8bea264"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_protection_policies_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_protection_policy  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_etag  # noqa: E402
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
    import ntnx_datapolicies_py_client as datapolicies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as datapolicies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    replication_sub_location_obj_map = {
        "nutanix_cluster": datapolicies_sdk.NutanixCluster,
    }
    retention_obj_map = {
        "linear_retention": datapolicies_sdk.LinearRetention,
        "auto_rollup_retention": datapolicies_sdk.AutoRollupRetention,
    }
    nutanix_cluster_spec = dict(
        cluster_ext_ids=dict(type="list", elements="str"),
    )
    replication_sub_location_spec = dict(
        nutanix_cluster=dict(type="dict", options=nutanix_cluster_spec),
    )
    replication_locations_spec = dict(
        label=dict(type="str", required=True),
        domain_manager_ext_id=dict(
            type="str",
            required=True,
        ),
        replication_sub_location=dict(
            type="dict",
            options=replication_sub_location_spec,
            obj=replication_sub_location_obj_map,
        ),
        is_primary=dict(type="bool"),
    )
    linear_retention_spec = dict(
        local=dict(type="int", required=True),
        remote=dict(type="int"),
    )
    auto_retention_spec = dict(
        snapshot_interval_type=dict(
            type="str",
            required=True,
            choices=["YEARLY", "WEEKLY", "DAILY", "MONTHLY", "HOURLY"],
        ),
        frequency=dict(type="int", required=True),
    )
    auto_rollup_retention_spec = dict(
        local=dict(
            type="dict",
            required=True,
            options=auto_retention_spec,
            obj=datapolicies_sdk.AutoRollupRetentionDetails,
        ),
        remote=dict(
            type="dict",
            options=auto_retention_spec,
            obj=datapolicies_sdk.AutoRollupRetentionDetails,
        ),
    )
    retention_spec = dict(
        linear_retention=dict(
            type="dict",
            options=linear_retention_spec,
        ),
        auto_rollup_retention=dict(
            type="dict",
            options=auto_rollup_retention_spec,
        ),
    )

    schedule_spec = dict(
        recovery_point_type=dict(
            type="str", choices=["CRASH_CONSISTENT", "APPLICATION_CONSISTENT"]
        ),
        recovery_point_objective_time_seconds=dict(type="int", required=True),
        retention=dict(
            type="dict",
            options=retention_spec,
            obj=retention_obj_map,
        ),
        start_time=dict(type="str"),
        sync_replication_auto_suspend_timeout_seconds=dict(type="int"),
    )
    replication_configurations_spec = dict(
        source_location_label=dict(type="str", required=True),
        remote_location_label=dict(type="str"),
        schedule=dict(
            type="dict",
            options=schedule_spec,
            required=True,
            obj=datapolicies_sdk.Schedule,
        ),
    )
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str", required=True),
        description=dict(type="str"),
        replication_locations=dict(
            type="list",
            elements="dict",
            options=replication_locations_spec,
            obj=datapolicies_sdk.ReplicationLocation,
            required=True,
        ),
        replication_configurations=dict(
            type="list",
            elements="dict",
            options=replication_configurations_spec,
            obj=datapolicies_sdk.ReplicationConfiguration,
            required=True,
        ),
        category_ids=dict(type="list", elements="str"),
    )

    return module_args


def create_protection_policy(module, protection_policies, result):
    sg = SpecGenerator(module)
    default_spec = datapolicies_sdk.ProtectionPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create protection policy Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = protection_policies.create_protection_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating protection policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        protection_policy_ext_id = get_ext_id_from_task_completion_details(
            resp, name=TASK_CONSTANTS.CompletetionDetailsName.PROTECTION_POLICY
        )
        if protection_policy_ext_id:
            result["protection_policy_ext_id"] = protection_policy_ext_id
            resp = get_protection_policy(
                module, protection_policies, protection_policy_ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_protection_policy(module, protection_policies, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_protection_policy(module, protection_policies, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating protection policy", **result
        )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update protection policy Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = protection_policies.update_protection_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating protection policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        resp = get_protection_policy(module, protection_policies, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_protection_policy(module, protection_policies, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = None
    try:
        resp = protection_policies.delete_protection_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting protection policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    protection_policies = get_protection_policies_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_protection_policy(module, protection_policies, result)
        else:
            create_protection_policy(module, protection_policies, result)
    else:
        delete_protection_policy(module, protection_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
