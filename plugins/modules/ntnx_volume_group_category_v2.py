#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_category_v2
short_description: Associate or disassociate categories with a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to associate or disassociate categories with a Volume Group in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Associate category to a Volume Group) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin,
    Project Admin, Project Manager, Self-Service Admin (deprecated),
    Storage Admin, Super Admin, Tenant Admin, Tenant Consumer
  - >-
    B(Disassociate category from a Volume Group) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin,
    Project Admin, Project Manager, Self-Service Admin (deprecated),
    Storage Admin, Super Admin, Tenant Admin, Tenant Consumer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - Specify state.
      - If C(state) is C(present), the categories are associated with the Volume Group referenced by C(ext_id).
      - If C(state) is C(absent), the categories are disassociated from the Volume Group referenced by C(ext_id).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the Volume Group to associate categories with or disassociate categories from.
    type: str
    required: true
  categories:
    description:
      - List of categories to associate with or disassociate from the Volume Group.
      - Required for both associate (C(state=present)) and disassociate (C(state=absent)) operations.
    type: list
    elements: dict
    required: true
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
          - The entity type of the category reference.
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
          - RECOVERY_PLAN_JOB
          - DIRECT_CONNECT
          - SUBNET_EXTENSION
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
- name: Associate categories with Volume Group
  nutanix.ncp.ntnx_volume_group_category_v2:
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
  register: result

- name: Disassociate categories from Volume Group
  nutanix.ncp.ntnx_volume_group_category_v2:
    state: absent
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for associating or disassociating categories with a Volume Group.
    - If C(wait) is true, it will return the task details after completion (including status).
    - If C(wait) is false, it will return the task submission details.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T06:01:24.177060+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T06:01:24.121781+00:00",
      "entities_affected": [
        {
          "ext_id": "a6165ec0-8936-405d-67bc-cc04c05e5622",
          "name": null,
          "rel": "volumes:config:volume-group"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0f7c0055-f47a-41bb-b72a-2ccf5b7e32bc",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:01:24.177059+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "UpdateCategoryAssociations_kOperationAttach",
      "operation_description": "Associate Category",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "projectExtId": "00000000-0000-0000-0000-000000000000",
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-07-21T06:01:24.132986+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description: The external identifier of the task performing the associate or disassociate action.
  returned: always
  type: str
  sample: "ZXJnb24=:0f7c0055-f47a-41bb-b72a-2ccf5b7e32bc"

ext_id:
  description: The external identifier of the Volume Group whose category associations are being managed.
  returned: always
  type: str
  sample: "a6165ec0-8936-405d-67bc-cc04c05e5622"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or in check mode operation.
  type: str
  sample: "Api Exception raised while associating categories with Volume Group {0}"

error:
  description: This field typically holds information about the error that occurred during the task execution.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.volumes.helpers import get_volume_group  # noqa: E402

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
                "RECOVERY_PLAN_JOB",
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


def associate_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating category associations by volume group id spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.associate_category(body=spec, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while associating categories with "
                "Volume Group {0}"
            ).format(ext_id),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def disassociate_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating category associations by volume group id spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.disassociate_category(body=spec, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while disassociating categories from "
                "Volume Group {0}"
            ).format(ext_id),
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
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        associate_CategoryAssociationsByVolumeGroupId(module, result, api_instance)
    else:
        disassociate_CategoryAssociationsByVolumeGroupId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
