#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_point_replicate_v2
short_description: Replicate recovery points
version_added: 2.0.0
description:
    - Replicate recovery points using external ID
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will replicate a recovery point.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - Recovery point external ID
        type: str
        required: true
    pc_ext_id:
        description:
            - External ID of the target Prism Central(PC)
            - Notes Use remote cluster uuid from availability zone info
        type: str
    cluster_ext_id:
        description:
            - External ID of the target cluster
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: Replicate a Recovery Point
  nutanix.ncp.ntnx_recovery_point_replicate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    pc_ext_id: "63bebabf-744c-48ff-a6d7-cb028707f972"
    cluster_ext_id: "000620a9-8183-2553-1fc3-ac1f6b6029c1"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for replicating recovery points
        - Task details
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2024-09-04T10:18:39.599580+00:00",
            "completion_details": [
                {
                    "name": "recoveryPointExtId",
                    "value": "6ec8e20d-5662-404f-a475-4ac569521f82"
                }
            ],
            "created_time": "2024-09-04T10:17:47.283752+00:00",
            "entities_affected": [
                {
                    "ext_id": "1ca2963d-77b6-453a-ae23-2c19e7a954a3",
                    "rel": "dataprotection:config:recovery-point"
                },
                {
                    "ext_id": "522670d7-e92d-45c5-9139-76ccff6813c2",
                    "rel": "dataprotection:config:vm-recovery-point"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a",
            "is_cancelable": false,
            "last_updated_time": "2024-09-04T10:18:39.599579+00:00",
            "legacy_error_message": null,
            "operation": "EntitySnapshotReplicate",
            "operation_description": "Replicate Recovery Point",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-09-04T10:17:47.300538+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
changed:
    description: Indicates if any change is made
    returned: always
    type: bool
    sample: true
error:
    description: Error message if any
    returned: when an error occurs
    type: str
    sample: null
task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a"
ext_id:
    description: External ID of the recovery point
    returned: always
    type: str
    sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
failed:
    description: Indicates if the task failed
    returned: always
    type: bool
    sample: false
"""
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_etag,
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import get_recovery_point  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        pc_ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
    )
    return module_args


def replicate_recovery_point_with_ext_id(module, result):
    recovery_points = get_recovery_point_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.RecoveryPointReplicationSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating replicate recovery point Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_recovery_point(module, recovery_points, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(msg="Failed to get etag for recovery point", **result)

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = recovery_points.replicate_recovery_point(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while replicating recovery point",
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
            msg=missing_required_lib("ntnx_dataprotection_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    replicate_recovery_point_with_ext_id(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
