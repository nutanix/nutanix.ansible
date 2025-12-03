#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_prechecks_v2
short_description: Perform LCM Prechecks
description:
    - This module allows you to perform LCM Prechecks.
version_added: "2.1.0"
author:
 - George Ghawali (@george-ghawali)
 - Abhinav Bansal (@abhinavbansal29)
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will perform LCM prechecks.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    management_server:
        description:
            - Cluster management server configuration used while updating clusters with ESX or Hyper-V.
        type: dict
        suboptions:
            hypervisor_type:
                description:
                    - Type of Hypervisor present in the cluster.
                type: str
                required: true
                choices:
                    - ESX
                    - AHV
                    - HYPERV
            ip:
                description:
                    - Management server IP.
                type: str
                required: true
            username:
                description:
                    - Management server username.
                type: str
                required: true
            password:
                description:
                    - Management server password.
                type: str
                required: true
    entity_update_specs:
        description:
            - List of entity update objects for getting recommendations.
        type: list
        elements: dict
        required: true
        suboptions:
            entity_uuid:
                description:
                    - LCM Entity UUID.
                type: str
                required: true
            to_version:
                description:
                    - Version to upgrade to.
                type: str
                required: true
    skipped_precheck_flags:
        description:
            - List of skipped precheck flags.
        type: list
        elements: str
        choices:
            - POWER_OFF_UVMS
    cluster_ext_id:
        description:
            - Cluster external ID.
            - It is used to perform LCM prechecks on entities on a particular cluster, it performs LCM prechecks on Prism Central entities if nothing passed.
            - If we give PE cluster's external ID, it will perform LCM prechecks on PE cluster entities.
            - We can get the external ID of the cluster using ntnx_clusters_info_v2 module.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Perform LCM prechecks
  nutanix.ncp.ntnx_lcm_prechecks_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    management_server:
      ip: "10.0.0.2"
      username: "admin"
      password: "password"
      hypervisor_type: "AHV"
    entity_update_specs:
      - entity_uuid: "3c196eac-e1d5-4c8a-9b01-c133f6907ca"
        to_version: "5.0.0"
    skipped_precheck_flags: ["POWER_OFF_UVMS"]
  register: lcm_prechecks
"""

RETURN = r"""
response:
    description: Response for performing LCM prechecks.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2025-02-16T10:12:26.000269+00:00",
            "completion_details": null,
            "created_time": "2025-02-16T10:11:27.891274+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:7b891b72-e645-4676-6259-18d19ea25c91",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-02-16T10:12:26.000267+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 1,
            "operation": "kLcmRootTask",
            "operation_description": "Run Lcm Root Task",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-02-16T10:11:27.891274+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:ffc1b1c2-3616-4e55-5eef-41501e45c7b5",
                    "href": "https://10.101.177.78:9440/api/prism/v4.0/config/tasks/ZXJnb24=:ffc1b1c2-3616-4e55-5eef-41501e45c7b5",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
task_ext_id:
    description: Task external ID.
    type: str
    returned: always
    sample: ZXJnb24=:f2efc360-5377-42d3-8e69-f5e3cd7d8f83
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while performing LCM prechecks"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str
  sample: "Failed generating create LCM prechecks Spec"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_prechecks_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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


def get_module_spec():

    hypervisor_type_spec = dict(
        type="str",
        required=True,
        choices=["ESX", "AHV", "HYPERV"],
    )

    management_server_spec = dict(
        hypervisor_type=hypervisor_type_spec,
        ip=dict(type="str", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        management_server=dict(
            type="dict",
            options=management_server_spec,
            obj=lifecycle_sdk.ManagementServer,
        ),
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            obj=lifecycle_sdk.EntityUpdateSpec,
            required=True,
        ),
        skipped_precheck_flags=dict(
            type="list",
            elements="str",
            choices=["POWER_OFF_UVMS"],
            obj=lifecycle_sdk.SystemAutoMgmtFlag,
        ),
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def lcm_prechecks(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.PrechecksSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create LCM prechecks Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.perform_prechecks(X_Cluster_Id=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing LCM prechecks",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():

    module = BaseModule(
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

    api_instance = get_prechecks_api_instance(module)

    lcm_prechecks(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
