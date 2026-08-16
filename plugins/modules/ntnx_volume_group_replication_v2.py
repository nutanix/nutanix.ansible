#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_replication_v2
short_description: Pause or resume synchronous replication for a Volume Group in Nutanix PC
version_added: 2.7.0
description:
    - Pause or resume synchronous replication for a protected Volume Group in Nutanix Prism Central.
    - Use C(state=absent) to pause synchronous replication on the given Volume Group.
    - Use C(state=present) to resume synchronous replication on the given Volume Group.
    - The target Volume Group must already be protected by a synchronous protection policy.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - Desired state of synchronous replication for the given Volume Group.
            - If C(state) is set to C(present), the module resumes synchronous replication.
            - If C(state) is set to C(absent), the module pauses synchronous replication.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external identifier of the Volume Group whose synchronous replication
              should be paused or resumed.
        type: str
        required: true
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
- name: Resume synchronous replication for a Volume Group
  nutanix.ncp.ntnx_volume_group_replication_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: resume_result

- name: Pause synchronous replication for a Volume Group
  nutanix.ncp.ntnx_volume_group_replication_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: pause_result
"""

RETURN = r"""
response:
    description:
        - Task details describing the pause or resume synchronous replication operation.
        - When C(wait=true), holds the final Prism task response.
        - When C(wait=false), holds the async task reference returned by the API.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T06:26:51.524581+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T06:26:47.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
                    "rel": "volumes:config:volume-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T06:26:51.524581+00:00",
            "legacy_error_message": null,
            "operation": "PauseVolumeGroupSynchronousReplication",
            "operation_description": "Pause volume group synchronous replication",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-21T06:26:47.185754+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: Contextual status or error message.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while pausing synchronous replication for Volume Group"

error:
    description:
        - This field typically holds information about any error that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed to get etag for Volume Group"

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task returned by the API.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the Volume Group whose synchronous replication was paused or resumed.
    returned: always
    type: str
    sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_volume_group_api_instance,
)
from ..module_utils.v4.storage.helpers import get_volume_group  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    # Imported for the missing-dependency check surfaced in run_module();
    # the SDK objects themselves are constructed inside the storage
    # ``api_client`` helper, so no symbols are used from this module.
    import ntnx_storage_py_client  # noqa: F401  # pylint: disable=unused-import
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def _execute_replication_action(module, result, api_instance, action):
    """
    Shared executor for pause/resume synchronous replication.

    Args:
        module: AnsibleModule wrapper.
        result: mutable result dict.
        api_instance: ``VolumeGroupApi`` instance.
        action: Either ``"pause"`` or ``"resume"``.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if action == "pause":
        sdk_method = api_instance.pause_volume_group_synchronous_replication
        error_msg = "Api Exception raised while pausing synchronous replication for Volume Group"
    else:
        sdk_method = api_instance.resume_volume_group_synchronous_replication
        error_msg = "Api Exception raised while resuming synchronous replication for Volume Group"

    if module.check_mode:
        result["response"] = {
            "ext_id": ext_id,
            "action": action,
        }
        result["changed"] = True
        return

    vg = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(vg)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = sdk_method(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(module=module, exception=e, msg=error_msg)

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def pause_volume_group_synchronous_replication(module, result, api_instance):
    _execute_replication_action(module, result, api_instance, "pause")


def resume_volume_group_synchronous_replication(module, result, api_instance):
    _execute_replication_action(module, result, api_instance, "resume")


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_volume_group_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        resume_volume_group_synchronous_replication(module, result, api_instance)
    else:
        pause_volume_group_synchronous_replication(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
