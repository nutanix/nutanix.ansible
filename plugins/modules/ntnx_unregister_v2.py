#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unregister_v2
short_description: Unregister a registered remote cluster from the local cluster.
version_added: 2.7.0
description:
    - Unregister a registered remote cluster from the local domain manager (Prism Central) cluster.
    - This is an action module which triggers a task-based operation.
    - This module uses PC v4 APIs based SDKs.
notes:
    - This module talks to the domain manager (Prism Central) endpoint, set C(nutanix_host) to the Prism Central IP.
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Unregister a registered remote cluster from the local cluster) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  state:
    description:
      - State of the module.
      - If state is present, the module will unregister the remote cluster.
      - If state is not present, the module will fail.
    type: str
    choices:
      - present
    default: present
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    required: false
    default: true
  ext_id:
    description:
      - The external identifier of the local domain manager (Prism Central) resource.
    type: str
    required: true
  remote_cluster_ext_id:
    description:
      - Cluster UUID of the remote cluster to unregister from the local cluster.
    type: str
    required: true
  name:
    description:
      - Name of the remote cluster to unregister.
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
- name: Unregister a remote cluster from the local domain manager (Prism Central)
  nutanix.ncp.ntnx_unregister_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
    remote_cluster_ext_id: "86b54161-3214-5874-9632-89afcd365004"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Task response for unregistering the remote cluster.
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
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    type: bool
    returned: always
    sample: true

task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:7f0399f6-370c-59f8-b7a3-c50e4b91a6d0"

ext_id:
    description: The external identifier of the local domain manager (Prism Central) resource.
    type: str
    returned: always
    sample: "18553f0f-8547-4115-9696-2f698fbe7117"

skipped:
    description: This indicates whether the operation was skipped (for example in check mode).
    returned: when the operation is skipped
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while unregistering cluster"

error:
    description: Error message if any.
    type: str
    returned: When an error occurs

failed:
    description: This field typically holds information about if the task have failed.
    returned: when something fails
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
    get_etag,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
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
        ext_id=dict(type="str", required=True),
        remote_cluster_ext_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
    )
    return module_args


def unregister_cluster(module, domain_manager_api, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = prism_sdk.ClusterReference()
    spec.ext_id = module.params.get("remote_cluster_ext_id")
    if module.params.get("name") is not None:
        spec.name = module.params.get("name")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = True
        return

    current_spec = get_pc_config(module, domain_manager_api, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(msg="Failed fetching etag to unregister.", **result)

    resp = None
    try:
        resp = domain_manager_api.unregister(
            extId=ext_id, body=spec, if_match=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unregistering cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
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
        "task_ext_id": None,
    }
    domain_manager_api = get_domain_manager_api_instance(module)
    unregister_cluster(module, domain_manager_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
