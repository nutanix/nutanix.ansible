#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_point_restore_v2
short_description: Restore recovery points, Creates a clone of the VM/VG from the selected recovery point
version_added: 2.0.0
description: "Restore recovery points using external ID"
options:
    ext_id:
        description:
            - External ID to restore recovery point
        type: str
        required: true
    cluster_ext_id:
        description:
            - By default, recovery points are restored to their associated location reference.
            - For cloud-based recovery points without a location reference, the client must specify the cluster's external identifier for restoration.
        type: str
    vm_recovery_point_restore_overrides:
        description:
            - List of specifications to restore a specific VM recovery point(s) that are a part of the top-level recovery point.
            - A specific VM recovery point can be selected for restore by specifying its external identifier along with override specification (if any).
        type: list
        elements: dict
        suboptions:
            vm_recovery_point_ext_id:
                description:
                    - External identifier of a VM recovery point, that is a part of the top-level recovery point.
                type: str
    volume_group_recovery_point_restore_overrides:
        description:
            - List of specifications to restore a specific volume group recovery point(s) that are a part of the top-level recovery point.
            - A specific volume group recovery point can be selected for restore by specifying its external identifier along with override specification (if any).
        type: list
        elements: dict
        suboptions:
            volume_group_recovery_point_ext_id:
                description:
                    - External identifier of a volume group recovery point, that is a part of the top-level recovery point.
                type: str
            volume_group_override_spec:
                description:
                    - Protected resource/recovery point restore that overrides the volume group configuration.
                    - The specified properties will be overridden for the restored volume group.
                type: dict
                suboptions:
                    name:
                        description:
                            - The name of the restored volume group.
                        type: str
extends_documentation_fragment:
        - nutanix.ncp.ntnx_credentials
        - nutanix.ncp.ntnx_operations_v2
author:
    - Prem Karat (@premkarat)
    - Abhinav Bansal (@abhinavbansal29)
    - Pradeepsingh Bhati (@bhati-pradeep)
"""
EXAMPLES = r"""
- name: Restore one of the VM recovery point from a recovery point
  ntnx_recovery_point_restore_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    vm_recovery_point_restore_overrides:
      - vm_recovery_point_ext_id: "c92aa134-5586-4cb1-b731-1ecafda83c12"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for restoring recovery point
        - Task details
    returned: always
    type: dict
    sample: {
            "cluster_ext_ids": null,
            "completed_time": "2024-09-03T06:23:43.729898+00:00",
            "completion_details": [
                {
                    "name": "vmExtIds",
                    "value": "e44621b1-da4e-40d1-87b1-cbb640001347"
                }
            ],
            "created_time": "2024-09-03T06:23:39.359388+00:00",
            "entities_affected": [
                {
                    "ext_id": "6f4ffcee-1dc4-4982-9401-aa1f65dd7177",
                    "rel": "dataprotection:config:recovery-point"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:958ee0db-18f3-45c3-9b5f-2cecb9a8819e",
            "is_cancelable": false,
            "last_updated_time": "2024-09-03T06:23:43.729897+00:00",
            "legacy_error_message": null,
            "operation": "RestoreRecoveryPoint",
            "operation_description": "Restore Recovery Point",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2024-09-03T06:23:39.373563+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:db656984-57cb-4aec-a36a-4d2d4fbd9dda",
                    "href": "https://10.44.76.48:9440/api/prism/v4.0.b1/config/tasks/ZXJnb24=:db656984-57cb-4aec-a36a-4d2d4fbd9dda",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:958ee0db-18f3-45c3-9b5f-2cecb9a8819e"
ext_id:
    description: The external ID of the recovery point
    returned: always
    type: str
    sample: "6f4ffcee-1dc4-4982-9401-aa1f65dd7177"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs
    sample: "Failed to get etag for restoring recovery point"
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
vms_ext_ids:
    description: List of VM external IDs
    returned: when recovery point is associated with VMs
    type: list
    sample: ["522670d7-e92d-45c5-9139-76ccff6813c2", "522670d7-e92d-45c5-9139-76ccff6813c3"]
vgs_ext_ids:
    description: List of Volume Group external IDs
    returned: when recovery point is associated with Volume Groups
    type: list
    sample: ["322770d0-b67d-78d2-4963-96cvff6313q9", "322770d0-b67d-78d2-4963-96cvff6313q8"]
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_etag,
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import get_recovery_point  # noqa: E402
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
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    vm_recovery_point_restore_overrides_sub_spec = dict(
        vm_recovery_point_ext_id=dict(type="str"),
    )

    volume_group_recovery_point_restore_overrides_sub_spec = dict(
        volume_group_recovery_point_ext_id=dict(type="str"),
        volume_group_override_spec=dict(
            type="dict",
            options=dict(
                name=dict(type="str"),
            ),
            obj=data_protection_sdk.VolumeGroupOverrideSpec,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str"),
        vm_recovery_point_restore_overrides=dict(
            type="list",
            elements="dict",
            options=vm_recovery_point_restore_overrides_sub_spec,
            obj=data_protection_sdk.VmRecoveryPointRestoreOverride,
        ),
        volume_group_recovery_point_restore_overrides=dict(
            type="list",
            elements="dict",
            options=volume_group_recovery_point_restore_overrides_sub_spec,
            obj=data_protection_sdk.VolumeGroupRecoveryPointRestoreOverride,
        ),
    )
    return module_args


def restore_recovery_points(module, result):
    recovery_points = get_recovery_point_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.RecoveryPointRestorationSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating restore recovery point Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_recovery_point(module, recovery_points, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(
            msg="Failed to get etag for restoring recovery point", **result
        )

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = recovery_points.restore_recovery_point(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while restoring recovery point",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        vms_ext_ids = get_ext_id_from_task_completion_details(
            resp, name=TASK_CONSTANTS.CompletetionDetailsName.VM_EXT_IDS
        )
        if vms_ext_ids:
            result["vms_ext_ids"] = vms_ext_ids
        vgs_ext_ids = get_ext_id_from_task_completion_details(
            resp, name=TASK_CONSTANTS.CompletetionDetailsName.VG_EXT_IDS
        )
        if vgs_ext_ids:
            result["vgs_ext_ids"] = vgs_ext_ids
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
    restore_recovery_points(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
