#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_category_v2
short_description: Associate or disassociate categories with a Volume Group in Nutanix Prism Central.
version_added: 2.5.0
description:
  - This module allows you to associate or disassociate categories with a Volume Group
    in Nutanix Prism Central using the storage v4 APIs.
  - If C(state) is C(present) the requested categories are associated with the Volume Group.
  - If C(state) is C(absent) the requested categories are disassociated from the Volume Group.
  - The module is idempotent - it inspects the existing category associations on the Volume
    Group and skips the API call when no change is required.
  - This module uses PC v4 APIs based SDKs (ntnx_storage_py_client).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Associate category to a Volume Group) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Project Manager,
    Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(Disassociate category from a Volume Group) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Project Manager,
    Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - The desired state of the category association.
      - If C(present), the module associates the given categories with the Volume Group.
      - If C(absent), the module disassociates the given categories from the Volume Group.
    type: str
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the Volume Group to associate or disassociate categories with.
      - Required for both associate (C(state=present)) and disassociate (C(state=absent)) operations.
    type: str
    required: true
  categories:
    description:
      - List of category references to be associated with or disassociated from the Volume Group.
      - Each element must reference a Category entity by its C(ext_id).
      - Required for both associate and disassociate operations.
    type: list
    elements: dict
    required: true
    suboptions:
      ext_id:
        description:
          - The external identifier of the Category to (dis)associate.
        type: str
        required: false
      name:
        description:
          - Optional display name of the referenced Category entity.
        type: str
        required: false
      uris:
        description:
          - Optional list of URIs for the referenced entity.
        type: list
        elements: str
        required: false
      entity_type:
        description:
          - The entity type of the referenced object.
          - For category associations this is typically C(CATEGORY).
        type: str
        required: false
        choices:
          - CATEGORY
          - CLUSTER
          - DIRECT_CONNECT
          - DIRECT_CONNECT_VIF
          - DISK_RECOVERY_POINT
          - FLOATING_IP
          - IMAGE
          - NODE
          - ROUTING_POLICY
          - STORAGE_CONTAINER
          - SUBNET
          - TASK
          - VIRTUAL_NIC
          - VIRTUAL_SWITCH
          - VM
          - VM_DISK
          - VOLUME_DISK
          - VOLUME_GROUP
          - VPC
          - VPN_CONNECTION
          - VPN_GATEWAY
          - VTEP_GATEWAY
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
- name: Associate categories with a Volume Group
  nutanix.ncp.ntnx_volume_group_category_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
  register: result

- name: Disassociate categories from a Volume Group
  nutanix.ncp.ntnx_volume_group_category_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
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
    - When C(wait) is C(true) (the default), this holds the completed Ergon task.
    - When C(wait) is C(false), this holds the initial task reference returned by the API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-20T15:21:02.402685+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T15:21:02.374289+00:00",
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
      "last_updated_time": "2026-07-20T15:21:02.402684+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "UpdateCategoryAssociations_kOperationAttach",
      "operation_description": "Associate Category",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-20T15:21:02.382944+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external identifier of the Ergon task created for the operation.
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
  description: Whether the module made any change.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - True when the module short-circuited because the requested state already matched
      the current category associations on the Volume Group (idempotency).
  returned: when applicable
  type: bool
  sample: false

msg:
  description:
    - Human readable status message. Present on idempotent skips, check_mode runs, and errors.
  returned: contextual
  type: str
  sample: "All requested categories are already associated with Volume Group. Skipping association."

error:
  description: Error details, if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: Whether the task failed.
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
from ..module_utils.v4.storage.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.storage.helpers import (  # noqa: E402
    get_associated_category_ext_ids,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: E402

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
                "CATEGORY",
                "CLUSTER",
                "DIRECT_CONNECT",
                "DIRECT_CONNECT_VIF",
                "DISK_RECOVERY_POINT",
                "FLOATING_IP",
                "IMAGE",
                "NODE",
                "ROUTING_POLICY",
                "STORAGE_CONTAINER",
                "SUBNET",
                "TASK",
                "VIRTUAL_NIC",
                "VIRTUAL_SWITCH",
                "VM",
                "VM_DISK",
                "VOLUME_DISK",
                "VOLUME_GROUP",
                "VPC",
                "VPN_CONNECTION",
                "VPN_GATEWAY",
                "VTEP_GATEWAY",
            ],
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        categories=dict(
            type="list",
            elements="dict",
            options=categories_spec,
            obj=storage_sdk.EntityReference,
            required=True,
        ),
    )

    return module_args


def _requested_category_ext_ids(module):
    """Collect the set of category ext_ids explicitly listed in module params."""
    requested = set()
    for category in module.params.get("categories") or []:
        cat_ext_id = category.get("ext_id") if isinstance(category, dict) else None
        if cat_ext_id:
            requested.add(cat_ext_id)
    return requested


def _build_spec(module):
    """Build the CategoryEntityReferences body from module params."""
    sg = SpecGenerator(module)
    default_spec = storage_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    return spec, err


def create_CategoryAssociation(module, result, api_instance):
    """Associate categories with the given Volume Group."""
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec, err = _build_spec(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating category association spec for Volume Group",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    requested = _requested_category_ext_ids(module)
    if requested:
        associated = get_associated_category_ext_ids(module, api_instance, ext_id)
        if requested.issubset(associated):
            result["skipped"] = True
            result["changed"] = False
            result["msg"] = (
                "All requested categories are already associated with Volume Group "
                "'{0}'. Skipping association.".format(ext_id)
            )
            return

    resp = None
    try:
        resp = api_instance.associate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories with Volume Group",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def update_CategoryAssociation(module, result, api_instance):
    """
    Update the category associations on the given Volume Group.

    The storage v4 API does not expose a dedicated update endpoint for
    CategoryAssociation - re-associating already-associated categories is a
    no-op on the server. This method preserves the state-based dispatch by
    routing ``state=present`` calls (which always require ``ext_id``) into the
    associate flow, while still applying an idempotency short-circuit.
    """
    create_CategoryAssociation(module, result, api_instance)


def delete_CategoryAssociation(module, result, api_instance):
    """Disassociate categories from the given Volume Group."""
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec, err = _build_spec(module)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating category disassociation spec for Volume Group",
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "Categories will be disassociated from Volume Group with ext_id:{0}.".format(
                ext_id
            )
        )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    requested = _requested_category_ext_ids(module)
    if requested:
        associated = get_associated_category_ext_ids(module, api_instance, ext_id)
        if not requested.intersection(associated):
            result["skipped"] = True
            result["changed"] = False
            result["msg"] = (
                "None of the requested categories are associated with Volume Group "
                "'{0}'. Skipping disassociation.".format(ext_id)
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
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_CategoryAssociation(module, result, api_instance)
        else:
            create_CategoryAssociation(module, result, api_instance)
    else:
        delete_CategoryAssociation(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
