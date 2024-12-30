#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
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
                    - Specifies the sub location of the replication location.
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
                    - The label of the source location.
                type: str
                required: true
            remote_location_label:
                description:
                    - The label of the remote location.
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
                        type: int
                        required: true
                    retention:
                        description:
                            - Specifies the retention policy of the schedule.
                        type: dict
                        required: false
                        suboptions:
                            linear:
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
                            auto_rollup_retention_details:
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
            - Specifies the category ids of the protection policy.
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
"""

RETURN = r"""
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protection_policies_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_protection_policy,
)
from ..module_utils.v4.prism.pc_api_client import get_etag  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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
        "linear": datapolicies_sdk.LinearRetention,
        "auto_rollup_retention_details": datapolicies_sdk.AutoRollupRetentionDetails,
    }
    nutanix_cluster_spec = dict(
        cluster_ext_ids=dict(type="list", elements="str"),
    )
    replication_sub_location_spec = dict(
        nutanix_cluster=dict(type="dict", options=nutanix_cluster_spec),
    )
    replication_locations_spec = dict(
        label=dict(type="str", required=True),
        domain_manager_ext_id=dict(type="str", required=True),
        replication_sub_location=dict(
            type="dict",
            options=replication_sub_location_spec,
            obj=replication_sub_location_obj_map,
        ),
        is_primary=dict(type="bool"),
    )
    linear_spec = dict(
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
    auto_rollup_retention_details_spec = dict(
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
        linear=dict(
            type="dict",
            options=linear_spec,
        ),
        auto_rollup_retention_details=dict(
            type="dict",
            options=auto_rollup_retention_details_spec,
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
        schedule=dict(type="dict", options=schedule_spec, required=True),
    )
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str", required=True),
        description=dict(type="str"),
        replication_locations=dict(
            type="list",
            elements="dict",
            options=replication_locations_spec,
            required=True,
        ),
        replication_configurations=dict(
            type="list",
            elements="dict",
            options=replication_configurations_spec,
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
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
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
        "error": None,
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
