#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_categories_v2
short_description: Module to associate or disassociate categories with a volume group in Nutanix Prism Central.
version_added: 2.1.0
description:
  - This module can be used to associate or disassociate categories with a volume group in Nutanix Prism Central.
options:
    state:
        description:
            - The state of the category association.
            - If C(present), the module will associate the categories with the volume group.
            - If C(absent), the module will disassociate the categories from the volume group.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external identifier of the volume group.
        required: true
        type: str
    categories:
        description:
            - List of categories to associate or disassociate with the volume group.
        required: true
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - The external identifier of the category.
                type: str
                required: false
            name:
                description:
                    - The name of the category.
                type: str
                required: false
            uris:
                description:
                    - List of URIs of the category.
                type: list
                elements: str
                required: false
            entity_type:
                description:
                    - The entity type of the category.
                type: str
                required: false
                choices:
                    - VOLUME_GROUP
                    - ROUTING_POLICY
                    - DIRECT_CONNECT_VIF
                    - AVAILABILITY_ZONE
                    - STORAGE_CONTAINER
                    - VPC
                    - VPN_CONNECTION
                    - VOLUME_DISK
                    - VPN_GATEWAY
                    - IMAGE
                    - CATEGORY
                    - RECOVERY_PLAN
                    - CLUSTER
                    - DISK_RECOVERY_POINT
                    - CONSISTENCY_GROUP
                    - VIRTUAL_NIC
                    - TASK
                    - VIRTUAL_SWITCH
                    - VIRTUAL_NETWORK
                    - NODE
                    - FLOATING_IP
                    - SUBNET
                    - VM_DISK
                    - VTEP_GATEWAY
                    - VM
                    - DIRECT_CONNECT
                    - SUBNET_EXTENSION
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        default: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
 - George Ghawali (@george-ghawali)
 - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""
- name: Associate category with VG
  nutanix.ncp.ntnx_volume_groups_categories_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
  register: result

- name: Disassociate category from VG
  nutanix.ncp.ntnx_volume_groups_categories_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    state: absent
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
  register: result
"""
RETURN = r"""
response:
    description: Task response for associating or disassociating categories with a volume group.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2025-02-19T12:21:02.402685+00:00",
            "completion_details": null,
            "created_time": "2025-02-19T12:21:02.374289+00:00",
            "entities_affected": [
                {
                    "ext_id": "68e4c68e-1acf-4c05-7792-e062119acb68",
                    "name": null,
                    "rel": "volumes:config:volume-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:2cdebadf-10c5-4538-9da6-cb7700e79fbe",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-02-19T12:21:02.402684+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "UpdateCategoryAssociations_kOperationAttach",
            "operation_description": "Associate Category",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-02-19T12:21:02.382944+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description: The external identifier of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:2cdebadf-10c5-4538-9da6-cb7700e79fbe"

ext_id:
    description: The external identifier of the volume group.
    type: str
    returned: always
    sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while associating categories"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    categories_spec = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        uris=dict(type="list", elements="str"),
        entity_type=dict(
            type="str",
            choices=[
                "VOLUME_GROUP",
                "ROUTING_POLICY",
                "DIRECT_CONNECT_VIF",
                "AVAILABILITY_ZONE",
                "STORAGE_CONTAINER",
                "VPC",
                "VPN_CONNECTION",
                "VOLUME_DISK",
                "VPN_GATEWAY",
                "IMAGE",
                "CATEGORY",
                "RECOVERY_PLAN",
                "CLUSTER",
                "DISK_RECOVERY_POINT",
                "CONSISTENCY_GROUP",
                "VIRTUAL_NIC",
                "TASK",
                "VIRTUAL_SWITCH",
                "VIRTUAL_NETWORK",
                "NODE",
                "FLOATING_IP",
                "SUBNET",
                "VM_DISK",
                "VTEP_GATEWAY",
                "VM",
                "DIRECT_CONNECT",
                "SUBNET_EXTENSION",
            ],
        ),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        categories=dict(
            type="list",
            elements="dict",
            options=categories_spec,
            obj=volumes_sdk.EntityReference,
            required=True,
        ),
    )

    return module_args


def associate_categories(module, vgs, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume group category spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vgs.associate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def disassociate_categories(module, vgs, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume group category spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vgs.disassociate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories",
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
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    vgs = get_vg_api_instance(module)
    if state == "present":
        associate_categories(module, vgs, result)
    else:
        disassociate_categories(module, vgs, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
