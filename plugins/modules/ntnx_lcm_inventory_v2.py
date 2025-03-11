#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_inventory_v2
short_description: Perform Inventory
description:
    - This module performs inventory.
    - Perform inventory using cluster external ID.
version_added: 2.1.0
author:
    - Abhinav Bansal (@abhinavbansal29)
options:
    cluster_ext_id:
        description:
            - The external ID of the cluster.
            - It is used to perform inventory on a particular cluster, it performs inventory on Prism Central if nothing passed.
            - If we give PE cluster's external ID, it will perform inventory on PE cluster.
            - We can get the external ID of the cluster using ntnx_clusters_info_v2 module.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Perform inventory of LCM
  nutanix.ncp.ntnx_lcm_inventory_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    cluster_ext_id: "00062e00-87eb-ef15-0000-00000000b71a"
  register: lcm_inventory
"""

RETURN = r"""
response:
    description: Task response for performing inventory
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2025-02-16T10:11:12.512241+00:00",
            "completion_details": null,
            "created_time": "2025-02-16T10:08:58.314367+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-02-16T10:11:12.512240+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 2,
            "operation": "kLcmRootTask",
            "operation_description": "Inventory Root Task",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-02-16T10:08:58.314367+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:302b65d2-783c-41b0-609d-3a7454e0b491",
                    "href": "https://10.101.177.78:9440/api/prism/v4.0/config/tasks/ZXJnb24=:302b65d2-783c-41b0-609d-3a7454e0b491",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:30b19489-70ca-44c0-626c-a634e527ea61",
                    "href": "https://10.101.177.78:9440/api/prism/v4.0/config/tasks/ZXJnb24=:30b19489-70ca-44c0-626c-a634e527ea61",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
task_ext_id:
    description: The task external ID
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_inventory_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str"),
    )
    return module_args


def lcm_inventory(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = None

    try:
        resp = api_instance.perform_inventory(X_Cluster_Id=cluster_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing inventory",
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

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
    }
    api_instance = get_inventory_api_instance(module)
    lcm_inventory(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
