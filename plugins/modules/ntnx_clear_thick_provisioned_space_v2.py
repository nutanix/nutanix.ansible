#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clear_thick_provisioned_space_v2
short_description: Clear thick provisioned space on a Nutanix Storage Container
version_added: 2.7.0
description:
    - This module allows you to clear (release) the thick provisioned space of a Storage Container
      in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Clear Thick Provisioned Space Storage Container) -
      Required Roles: Prism Admin, Project Manager, Storage Admin, Super Admin,
      Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will clear thick provisioned space for the
              Storage Container identified by C(ext_id).
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier (UUID) of the Storage Container whose thick provisioned
              space must be cleared.
        type: str
        required: true
    cluster_ext_id:
        description:
            - The external ID of the remote Prism Element cluster to which the request should
              be forwarded via the C(X-Cluster-Id) header.
            - Typically not required when the Storage Container is already resolvable from
              Prism Central.
        type: str
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
- name: Clear thick provisioned space for a storage container
  nutanix.ncp.ntnx_clear_thick_provisioned_space_v2:
    ext_id: "cb3fd049-7896-9632-8555-e4f088711991"
  register: result
  ignore_errors: true

- name: Clear thick provisioned space and route to a specific remote cluster
  nutanix.ncp.ntnx_clear_thick_provisioned_space_v2:
    ext_id: "cb3fd049-7896-9632-8555-e4f088711991"
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the clear thick provisioned space action.
        - Task details when C(wait) is true.
        - Task reference (containing only the task C(ext_id)) when C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T12:55:59.889590+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T12:55:59.830125+00:00",
            "entities_affected": [
                {
                    "ext_id": "32c5b693-595b-4909-b99e-202eea0d9e2d",
                    "name": "ansible-ctps-AbqnFAccWhjq",
                    "rel": "clustermgmt:config:storage-containers"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:8a2c5587-391f-4c45-9cd0-1d4f6634ceb0",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T12:55:59.889590+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 1,
            "operation": "ClearStorageContainerThickProvisionedSpace",
            "operation_description": "Clear storage container thick provisioned space",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T12:55:59.845479+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:24458492-ea60-4190-9138-744fbbd980dc",
                    "href": "https://10.44.76.28:9440/api/prism/v4.3/config/tasks/ZXJnb24=:24458492-ea60-4190-9138-744fbbd980dc",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: on error or check mode
    type: str
    sample: "Api Exception raised while clearing thick provisioned space for storage container"

error:
    description: This field typically holds information about if the task have errors that
        occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Not Found"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:8a2c5587-391f-4c45-9cd0-1d4f6634ceb0"

ext_id:
    description: The external ID of the Storage Container on which the action was performed.
    returned: always
    type: str
    sample: "32c5b693-595b-4909-b99e-202eea0d9e2d"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_storage_containers_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str"),
    )
    return module_args


def clear_thick_provisioned_space(module, storage_containers_api, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Clear thick provisioned space will be triggered for "
            "storage container with ext_id:{0}".format(ext_id)
        )
        return

    kwargs = {}
    cluster_ext_id = module.params.get("cluster_ext_id")
    if cluster_ext_id:
        kwargs["X_Cluster_Id"] = cluster_ext_id

    resp = None
    try:
        resp = storage_containers_api.clear_thick_provisioned_space(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while clearing thick provisioned space "
            "for storage container",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    storage_containers_api = get_storage_containers_api_instance(module)
    clear_thick_provisioned_space(module, storage_containers_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
