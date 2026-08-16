#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_category_v2
short_description: Associate or disassociate categories with a Volume Group in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to associate or disassociate categories with a Volume Group in Nutanix Prism Central.
  - When C(state) is C(present), the categories passed in C(categories) are associated with the Volume Group.
  - When C(state) is C(absent), the categories passed in C(categories) are disassociated from the Volume Group.
  - Both the associate and disassociate operations are idempotent, i.e. only the categories that need to be
    added/removed to reach the requested state are sent to the API.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Associate category to a Volume Group) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin,
    Super Admin, Self-Service Admin (deprecated)
  - >-
    B(Disassociate category from a Volume Group) -
    Required Roles: CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin,
    Super Admin, Self-Service Admin (deprecated)
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
          - For a category reference this should typically be C(CATEGORY).
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

- name: Update category associations for a Volume Group (associate additional categories)
  nutanix.ncp.ntnx_volume_group_category_v2:
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    categories:
      - ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
        entity_type: "CATEGORY"
      - ext_id: "7c5b1c92-6f4a-4a24-8ce5-4b6c4e3c1def"
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
    - When C(wait) is C(true), it holds the completed task details.
    - When C(wait) is C(false), it holds the accepted task details.
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

skipped:
  description:
    - This indicates whether the operation was skipped because the requested state is already satisfied.
    - True when idempotency detected all categories are already associated (on C(state=present))
      or already disassociated (on C(state=absent)).
  returned: when applicable
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode is enabled.
  type: str
  sample: "Api Exception raised while associating categories with Volume Group"

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


def _get_associated_category_ext_ids(module, api_instance, volume_group_ext_id):
    """Return the set of category ext_ids currently associated with the Volume Group.

    Uses the deprecated but still-functional list-category-associations endpoint. Pages
    through until either no more pages are returned or the API returns fewer results
    than the page size (max 100 per page).
    """
    associated = set()
    page = 0
    page_size = 100
    while True:
        try:
            resp = api_instance.list_category_associations_by_volume_group_id(
                volumeGroupExtId=volume_group_ext_id,
                _page=page,
                _limit=page_size,
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while listing existing category associations for Volume Group",
            )
        data = getattr(resp, "data", None) or []
        for item in data:
            item_ext_id = getattr(item, "ext_id", None)
            if item_ext_id:
                associated.add(item_ext_id)
        if len(data) < page_size:
            break
        page += 1
    return associated


def _build_category_references_spec(module, result):
    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Volume Group category associations spec", **result
        )
    return spec


def _filter_categories_for_operation(spec, keep_ext_ids):
    """Return a new CategoryEntityReferences spec containing only categories whose ext_id
    appears in keep_ext_ids. Categories that reference by name/uris only (no ext_id) are
    always retained since we cannot infer their identity."""
    if spec.categories is None:
        return spec
    filtered = []
    for category in spec.categories:
        cat_ext_id = getattr(category, "ext_id", None)
        if cat_ext_id is None:
            filtered.append(category)
            continue
        if cat_ext_id in keep_ext_ids:
            filtered.append(category)
    spec.categories = filtered
    return spec


def _wait_and_finalize_task(module, resp, result):
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def _perform_associate(module, api_instance, ext_id, spec, result):
    try:
        resp = api_instance.associate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories with Volume Group",
        )
    _wait_and_finalize_task(module, resp, result)


def _perform_disassociate(module, api_instance, ext_id, spec, result):
    try:
        resp = api_instance.disassociate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories from Volume Group",
        )
    _wait_and_finalize_task(module, resp, result)


def create_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    """Associate categories with a Volume Group when no update state is known yet.

    In practice this branch is unreachable because C(ext_id) is required at the argument
    spec level. It is kept to conform to the mandated state-based dispatch pattern and
    provides a defensive error path.
    """
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_category_references_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # Ensure the Volume Group exists before attempting the associate action.
    get_volume_group(module, api_instance, ext_id)

    _perform_associate(module, api_instance, ext_id, spec, result)


def update_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    """Idempotently associate the requested categories with the Volume Group.

    Categories that are already associated are stripped from the request. If nothing
    remains to associate, the module exits early with C(changed=false) and
    C(skipped=true).
    """
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_category_references_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # Ensure the Volume Group exists before attempting the associate action.
    get_volume_group(module, api_instance, ext_id)

    requested_ext_ids = {
        cat.ext_id for cat in (spec.categories or []) if getattr(cat, "ext_id", None)
    }
    if requested_ext_ids:
        associated = _get_associated_category_ext_ids(module, api_instance, ext_id)
        to_associate = requested_ext_ids - associated
        if not to_associate:
            result["skipped"] = True
            result["changed"] = False
            module.exit_json(
                msg=(
                    "CategoryAssociationsByVolumeGroupId with ext_id '{0}' already has "
                    "the requested categories associated. Skipping association."
                ).format(ext_id),
                **result,
            )
        # Only send categories that still need to be associated.
        spec = _filter_categories_for_operation(spec, to_associate)

    _perform_associate(module, api_instance, ext_id, spec, result)


def delete_CategoryAssociationsByVolumeGroupId(module, result, api_instance):
    """Disassociate the requested categories from the Volume Group idempotently."""
    validate_required_params(module, ["ext_id", "categories"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_category_references_spec(module, result)

    if module.check_mode:
        result["msg"] = (
            "Categories will be disassociated from Volume Group with ext_id:{0}.".format(
                ext_id
            )
        )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # Ensure the Volume Group exists before attempting the disassociate action.
    get_volume_group(module, api_instance, ext_id)

    requested_ext_ids = {
        cat.ext_id for cat in (spec.categories or []) if getattr(cat, "ext_id", None)
    }
    if requested_ext_ids:
        associated = _get_associated_category_ext_ids(module, api_instance, ext_id)
        to_disassociate = requested_ext_ids & associated
        if not to_disassociate:
            result["skipped"] = True
            result["changed"] = False
            module.exit_json(
                msg=(
                    "None of the requested categories are currently associated with "
                    "Volume Group ext_id '{0}'. Skipping disassociation."
                ).format(ext_id),
                **result,
            )
        # Only send categories that are actually associated and need to be removed.
        spec = _filter_categories_for_operation(spec, to_disassociate)

    _perform_disassociate(module, api_instance, ext_id, spec, result)


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
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_CategoryAssociationsByVolumeGroupId(module, result, api_instance)
        else:
            create_CategoryAssociationsByVolumeGroupId(module, result, api_instance)
    else:
        delete_CategoryAssociationsByVolumeGroupId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
