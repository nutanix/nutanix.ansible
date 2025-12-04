#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_unregistration_v2
short_description: Unregister a PC-PC setup connected using availability zone.
version_added: 2.1.0
description:
    - Unregister a PC-PC setup connected using availability zone.
    - This module cannot be used to unregister PC-PE.
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will unregister a Prism Central.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: False
    pc_ext_id:
        description:
            - External ID of the current Prism Central (Primary).
        type: str
        required: True
    ext_id:
        description:
            - External ID of the Availability Zone Prism Central (Secondary).
        type: str
        required: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Unregister PC
  nutanix.ncp.ntnx_pc_unregistration_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "86b54161-3214-5874-9632-89afcd365004"
    pc_ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
  register: result
"""

RETURN = r"""
response:
    description: Task response for unregistering the remote cluster.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": [
                "00062c47-4512-1233-1122-ac1f6b6f97e2"
            ],
            "completed_time": "2025-01-29T06:51:25.368280+00:00",
            "completion_details": null,
            "created_time": "2025-01-29T06:51:20.378947+00:00",
            "entities_affected": [
                {
                    "ext_id": "18553f0f-1232-4333-2222-2f698fbe7117",
                    "name": "PC_10.44.76.100",
                    "rel": "prism:management:domain_manager"
                },
                {
                    "ext_id": "86b54161-1221-1233-9875-89afcd365004",
                    "name": null,
                    "rel": "prism:management:domain_manager"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:7f0399f6-370c-59f8-b7a3-c50e4b91a6d0",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-01-29T06:51:25.368279+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 0,
            "operation": "UnregisterPC",
            "operation_description": "Unregister Prism Central",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-01-29T06:51:20.392266+00:00",
            "status": "SUCCEEDED",
            "sub_steps": [
                {
                    "name": "Unregistering cluster started"
                },
                {
                    "name": "Precheck completed successfully"
                },
                {
                    "name": "Successfully unconfigured entities"
                },
                {
                    "name": "Successfully revoked trust"
                },
                {
                    "name": "Unregister cluster 86b54161-1221-1233-9875-89afcd365004 completed successfully"
                }
            ],
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: External ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:7f0399f6-370c-59f8-b7a3-c50e4b91a6d0"

pc_ext_id:
    description: External ID of the local cluster.
    type: str
    returned: always
    sample: "18553f0f-8547-4115-9696-2f698fbe7117"

changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "API Exception raised while unregistering cluster"

error:
    description: Error message if any.
    type: str
    returned: When an error occurs
    sample: null
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
    get_etag,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        pc_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def unregister_cluster(module, domain_manager_api, result):
    pc_ext_id = module.params.get("pc_ext_id")
    result["pc_ext_id"] = pc_ext_id
    sg = SpecGenerator(module)
    default_spec = prism_sdk.ClusterUnregistrationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating unregistering cluster spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_pc_config(module, domain_manager_api, pc_ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(msg="Failed fetching etag to unregister.", **result)

    resp = None
    try:
        resp = domain_manager_api.unregister(
            extId=pc_ext_id, body=spec, if_match=etag_value
        )
        result["changed"] = True
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception raised while unregistering cluster",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    domain_manager_api = get_domain_manager_api_instance(module)
    unregister_cluster(module, domain_manager_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
