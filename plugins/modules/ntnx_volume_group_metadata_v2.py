#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_metadata_v2
short_description: Update Volume Group Metadata Info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the Metadata Info associated with a
    Volume Group in Nutanix Prism Central.
  - Metadata Info includes the owner reference, owner user name, project
    reference, project name, and category IDs associated with the Volume Group.
  - The underlying Volume Group must already exist. This module does not create
    or delete Volume Groups themselves; it only manages the metadata-info sub
    resource of an existing Volume Group.
  - The Volume Group Metadata Info API is a deprecated storage v4 API kept for
    backwards compatibility. New consumers should prefer the Volume Group
    Metadata API (C(ntnx_volume_groups_metadata_v2)) when available.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Update Volume Group Metadata Info) -
      Required Roles: Prism Admin, Super Admin, Storage Admin, Project Manager
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is provided then the
        operation will update the Volume Group Metadata Info.
      - The C(absent) state is not supported by the underlying API since the
        metadata-info sub-resource cannot be deleted independently of its
        Volume Group; the module fails with a descriptive error if invoked
        with C(state=absent).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the Volume Group whose metadata information
        is being updated.
      - Required for the update operation.
    type: str
    required: false
  owner_reference_id:
    description:
      - A globally unique identifier that represents the owner of the
        Volume Group resource.
      - Must be a UUID.
    type: str
    required: false
  owner_user_name:
    description:
      - The user name of the owner of the Volume Group resource.
      - Maximum length is 128 characters.
    type: str
    required: false
  project_reference_id:
    description:
      - A globally unique identifier that represents the project this
        Volume Group belongs to.
      - Must be a UUID.
    type: str
    required: false
  project_name:
    description:
      - The name of the project this Volume Group belongs to.
      - Maximum length is 128 characters.
    type: str
    required: false
  category_ids:
    description:
      - A list of globally unique identifiers that represent all the
        categories the Volume Group is associated with.
      - Each entry must be a category UUID.
    type: list
    elements: str
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
- name: Update Volume Group Metadata Info with all fields
  nutanix.ncp.ntnx_volume_group_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    owner_reference_id: "00000000-0000-0000-0000-000000000000"
    owner_user_name: "admin"
    project_reference_id: "11111111-1111-1111-1111-111111111111"
    project_name: "ansible-project"
    category_ids:
      - "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result
  ignore_errors: true

- name: Update Volume Group Metadata Info with categories only
  nutanix.ncp.ntnx_volume_group_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    category_ids:
      - "566b844b-d245-4894-a8b5-eeef1ec4b638"
      - "77c4844b-d245-4894-a8b5-eeef1ec4b639"
  register: result
  ignore_errors: true

- name: Clear all Volume Group Metadata Info fields
  nutanix.ncp.ntnx_volume_group_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    category_ids: []
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating Volume Group Metadata Info.
    - Contains the Metadata dict as returned by the Nutanix PC v4 storage API
      after the update.
  returned: always
  type: dict
  sample:
    {
      "category_ids": [
        "566b844b-d245-4894-a8b5-eeef1ec4b638"
      ],
      "owner_reference_id": "00000000-0000-0000-0000-000000000000",
      "owner_user_name": "admin",
      "project_name": "ansible-project",
      "project_reference_id": "11111111-1111-1111-1111-111111111111"
    }

ext_id:
  description:
    - The external ID of the Volume Group whose metadata info was updated.
  returned: always
  type: str
  sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

task_ext_id:
  description:
    - The external ID of the task, if the underlying API returned one.
    - The metadata-info update API is synchronous and typically returns the
      updated Metadata payload directly, so this field is often C(None).
  returned: always
  type: str
  sample: null

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the operation was skipped because the current
      Metadata Info already matches the desired state (idempotency).
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description:
    - This indicates the message if any message occurred (idempotency skip,
      check mode preview, or error text).
  returned: contextual
  type: str
  sample: "Volume Group Metadata Info with ext_id '68e4c68e-1acf-4c05-7792-e062119acb68' already matches the desired state. Skipping update."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.storage.helpers import (  # noqa: E402
    get_volume_group_metadata_info,
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

    module_args = dict(
        ext_id=dict(type="str"),
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )
    return module_args


def create_volume_group_metadata_info(module, result, api_instance):
    """
    Placeholder for the create operation.

    The underlying storage v4 API only exposes GET and POST update-metadata-info
    endpoints for VolumeGroupMetadataInfo. Metadata Info always exists alongside
    its parent Volume Group and cannot be created independently. Callers that
    reach this branch (state=present with no ext_id) get a descriptive error
    telling them to supply the Volume Group ext_id and use update instead.
    """
    module.fail_json(
        msg=(
            "Create is not supported for Volume Group Metadata Info. "
            "It is an intrinsic sub-resource of a Volume Group. "
            "Provide 'ext_id' (Volume Group external identifier) to update its "
            "metadata info instead."
        ),
        **result,
    )


def _build_metadata_spec(module, existing_metadata=None):
    """Build a storage_sdk.Metadata spec from module params.

    When ``existing_metadata`` is provided, it is used as the base so we only
    overwrite the attributes the user explicitly supplied.
    """
    sg = SpecGenerator(module)
    if existing_metadata is not None:
        base_spec = deepcopy(existing_metadata)
    else:
        base_spec = storage_sdk.Metadata()
    return sg.generate_spec(obj=base_spec)


def _is_idempotent(current_dict, desired_dict):
    """Return True when the current and desired Metadata dicts are equivalent."""
    current = strip_internal_attributes(deepcopy(current_dict) or {})
    desired = strip_internal_attributes(deepcopy(desired_dict) or {})
    return current == desired


def check_for_idempotency_of_volume_group_metadata_info(
    module, result, api_instance, ext_id
):
    """Return (current_response, current_metadata_dict) for idempotency comparison."""
    current_response = get_volume_group_metadata_info(module, api_instance, ext_id)
    current_metadata = current_response.data if current_response else None
    current_metadata_dict = (
        current_metadata.to_dict() if current_metadata is not None else {}
    )
    return current_response, current_metadata_dict


def update_volume_group_metadata_info(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id"])

    current_response, current_metadata_dict = (
        check_for_idempotency_of_volume_group_metadata_info(
            module, result, api_instance, ext_id
        )
    )
    etag = get_etag(data=current_response)

    current_metadata_obj = (
        current_response.data if current_response is not None else None
    )
    update_spec, err = _build_metadata_spec(
        module, existing_metadata=current_metadata_obj
    )
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update Volume Group Metadata Info spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        result["msg"] = (
            "Volume Group Metadata Info with ext_id '{0}' will be updated.".format(
                ext_id
            )
        )
        return

    if _is_idempotent(current_metadata_dict, update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_metadata_dict)
        result["msg"] = (
            "Volume Group Metadata Info with ext_id '{0}' already matches the "
            "desired state. Skipping update.".format(ext_id)
        )
        return

    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.update_volume_group_metadata_info(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Volume Group Metadata Info",
        )

    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id

    if resp is not None and resp.data is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        refreshed = get_volume_group_metadata_info(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(
            refreshed.data.to_dict() if refreshed.data else {}
        )
    result["changed"] = True


def delete_volume_group_metadata_info(module, result, api_instance):
    """
    Delete is not supported by the underlying storage v4 API for Volume Group
    Metadata Info. The metadata-info payload lives alongside its parent Volume
    Group and can only be cleared by updating with empty values (which is
    already supported via ``state=present``).
    """
    ext_id = module.params.get("ext_id")
    if ext_id:
        result["ext_id"] = ext_id
    module.fail_json(
        msg=(
            "Delete is not supported for Volume Group Metadata Info. "
            "The metadata-info sub-resource cannot be removed independently of "
            "its Volume Group. To clear metadata fields, run this module with "
            "state=present and supply empty values (e.g. category_ids: [])."
        ),
        **result,
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("ext_id",)),
            ("state", "absent", ("ext_id",)),
        ],
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
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_volume_group_metadata_info(module, result, api_instance)
        else:
            create_volume_group_metadata_info(module, result, api_instance)
    else:
        delete_volume_group_metadata_info(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
