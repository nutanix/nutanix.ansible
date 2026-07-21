#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_category_associations_by_volume_group_id_v2
short_description: Associate or disassociate categories with a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to associate categories with a Volume Group or disassociate categories from a Volume Group in Nutanix Prism Central.
  - If C(state) is C(present) the module associates the provided C(categories) with the Volume Group identified by C(ext_id).
  - If C(state) is C(absent) the module disassociates the provided C(categories) from the Volume Group identified by C(ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Associate category to a Volume Group) -
      Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Disassociate category from a Volume Group) -
      Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    state:
        description:
            - The state of the category association on the Volume Group.
            - If C(present), the module associates the provided categories with the Volume Group.
            - If C(absent), the module disassociates the provided categories from the Volume Group.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external identifier of the Volume Group on which categories will be associated or disassociated.
        required: true
        type: str
    categories:
        description:
            - The list of categories to associate with or disassociate from the Volume Group.
            - This is a mandatory field for both associate and disassociate operations.
        required: true
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - A globally unique identifier of the category. This is the external identifier of the category to associate/disassociate.
                type: str
                required: false
            name:
                description:
                    - Name of the entity represented by this reference.
                type: str
                required: false
            uris:
                description:
                    - URI of the entity represented by this reference.
                type: list
                elements: str
                required: false
            entity_type:
                description:
                    - Entity type of the entity represented by this reference. For a category association this is typically C(CATEGORY).
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
            - Wait for the associate / disassociate category task to complete.
        type: bool
        default: true
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
- name: Associate categories with a Volume Group
  nutanix.ncp.ntnx_category_associations_by_volume_group_id_v2:
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
  register: result

- name: Disassociate categories from a Volume Group
  nutanix.ncp.ntnx_category_associations_by_volume_group_id_v2:
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
        - Task response for associating or disassociating categories with a Volume Group.
        - If C(wait) is true, the completed task details are returned.
        - If C(wait) is false, the initial task submission details are returned.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-02-19T12:21:02.402685+00:00",
            "completion_details": null,
            "created_time": "2026-02-19T12:21:02.374289+00:00",
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
            "last_updated_time": "2026-02-19T12:21:02.402684+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "UpdateCategoryAssociations_kOperationAttach",
            "operation_description": "Associate Category",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-02-19T12:21:02.382944+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description:
        - The external identifier of the associate/disassociate category task.
    returned: always
    type: str
    sample: "ZXJnb24=:2cdebadf-10c5-4538-9da6-cb7700e79fbe"

ext_id:
    description:
        - The external identifier of the Volume Group on which the operation was performed.
    returned: always
    type: str
    sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

skipped:
    description: This indicates whether the task was skipped.
    returned: when applicable
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error, module is idempotent or check mode
    type: str
    sample: "Api Exception raised while associating categories to Volume Group"

error:
    description: This field typically holds information about any errors that occurred during the task execution.
    returned: when an error occurs
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

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the Ansible argument spec for this module."""
    category_reference_spec = dict(
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
            options=category_reference_spec,
            obj=volumes_sdk.EntityReference,
            required=True,
        ),
    )
    return module_args


def _build_category_references_spec(module, result):
    """Build a CategoryEntityReferences SDK spec from module params.

    Fails the module with a descriptive error if spec generation fails.
    """
    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating category associations spec for Volume Group",
            **result,
        )
    return spec


def create_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    """Associate categories to a Volume Group.

    Corresponds to POST /api/volumes/v4.2/config/volume-groups/{extId}/$actions/associate-category.
    """
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_category_references_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.associate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories to Volume Group",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    """Disassociate categories from a Volume Group.

    Corresponds to POST /api/volumes/v4.2/config/volume-groups/{extId}/$actions/disassociate-category.
    """
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_category_references_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Categories will be disassociated from Volume Group with ext_id:{0}".format(
                ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.disassociate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories from Volume Group",
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
            msg=missing_required_lib("ntnx_volumes_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_CategoryAssociationsByVolumeGroupId(module, result, api_instance)
    else:
        delete_CategoryAssociationsByVolumeGroupId(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
