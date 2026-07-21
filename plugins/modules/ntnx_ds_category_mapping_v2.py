#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ds_category_mapping_v2
short_description: Create, Update, Delete AD group to Category mappings (DsCategoryMapping) in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update and delete a mapping between an Active Directory
    group and a Nutanix Category (DsCategoryMapping) in Nutanix Prism Central.
  - A DsCategoryMapping links an AD group (identified by its objectGUID) served by a configured
    Directory Server to a Category key/value pair used by Flow Network Security policies.
  - The module uses Prism Central v4.2 Flow Management (microseg) APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create an AD Group and Category Mapping) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Update an AD Group and Category Mapping) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete an AD Group and Category Mapping) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will
        be create DsCategoryMapping.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be
        update DsCategoryMapping.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be
        delete DsCategoryMapping.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the DsCategoryMapping.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the Category Mapping.
      - Required for create operation.
      - Maximum 1000 characters.
    type: str
    required: false
  category_name:
    description:
      - The name (key) of the Category that this mapping is for.
      - Required for create operation.
      - Maximum 200 characters.
    type: str
    required: false
  category_value:
    description:
      - The value of the Category that this mapping is for.
      - Required for create operation.
      - Maximum 1000 characters.
    type: str
    required: false
  ad_info:
    description:
      - A mapping to an object in Active Directory.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      directory_service_reference:
        description:
          - The external ID (UUID) of the Directory Service that will be used for the mapping.
          - Required when C(ad_info) is provided.
        type: str
        required: true
      object_identifier:
        description:
          - The objectGUID (UUID) for the AD group being mapped.
          - Required when C(ad_info) is provided.
        type: str
        required: true
      object_path:
        description:
          - The distinguished path for the mapped object in Active Directory.
          - Maximum 1000 characters.
        type: str
        required: false
      status:
        description:
          - The mapping status of the AD Mapping. Typically populated by the platform.
        type: str
        required: false
        choices:
          - USABLE
          - DELETED
          - DIRECTORY_NOT_CONFIGURED
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
- name: Create AD group to Category mapping
  nutanix.ncp.ntnx_ds_category_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_ds_category_mapping"
    category_name: "AppType"
    category_value: "Finance"
    ad_info:
      directory_service_reference: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
      object_identifier: "b1a1e59d-6f9a-4bde-8f0f-2b6f8c9f6a11"
      object_path: "CN=Finance,OU=Groups,DC=example,DC=com"
  register: result

- name: Update AD group to Category mapping
  nutanix.ncp.ntnx_ds_category_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "8b9c1a7e-2c1a-4c30-9f0e-f3b3c7a1e2d1"
    name: "ansible_ds_category_mapping_updated"
    category_name: "AppType"
    category_value: "Engineering"
    ad_info:
      directory_service_reference: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
      object_identifier: "b1a1e59d-6f9a-4bde-8f0f-2b6f8c9f6a11"
      object_path: "CN=Engineering,OU=Groups,DC=example,DC=com"
  register: result

- name: Delete AD group to Category mapping
  nutanix.ncp.ntnx_ds_category_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "8b9c1a7e-2c1a-4c30-9f0e-f3b3c7a1e2d1"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting DsCategoryMapping.
    - If the operation is create or update and C(wait) is true, it will return the DsCategoryMapping details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
        "ad_info": {
            "directory_service_reference": "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a",
            "object_identifier": "b1a1e59d-6f9a-4bde-8f0f-2b6f8c9f6a11",
            "object_path": "CN=Finance,OU=Groups,DC=example,DC=com",
            "status": "USABLE"
        },
        "category_name": "AppType",
        "category_value": "Finance",
        "ext_id": "8b9c1a7e-2c1a-4c30-9f0e-f3b3c7a1e2d1",
        "links": null,
        "name": "ansible_ds_category_mapping",
        "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the DsCategoryMapping.
  returned: always
  type: str
  sample: "8b9c1a7e-2c1a-4c30-9f0e-f3b3c7a1e2d1"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. update idempotency).
  returned: always
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
  description: This indicates the message returned by the module (e.g. on error, idempotency or check-mode delete).
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating DsCategoryMapping"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_directory_server_configs_api_instance,
    get_etag,
)
from ..module_utils.v4.flow.helpers import get_ds_category_mapping  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_microseg_py_client as flow_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as flow_management_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ad_info_spec = dict(
        directory_service_reference=dict(type="str", required=True),
        object_identifier=dict(type="str", required=True),
        object_path=dict(type="str", required=False),
        status=dict(
            type="str",
            required=False,
            choices=["USABLE", "DELETED", "DIRECTORY_NOT_CONFIGURED"],
            obj=flow_management_sdk.AdStatus,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        category_name=dict(type="str"),
        category_value=dict(type="str"),
        ad_info=dict(
            type="dict",
            options=ad_info_spec,
            obj=flow_management_sdk.AdInfo,
        ),
    )
    return module_args


def create_ds_category_mapping(module, api_instance, result):
    """Create a new AD Group and Category Mapping."""
    validate_required_params(
        module, ["name", "category_name", "category_value", "ad_info"]
    )
    sg = SpecGenerator(module)
    default_spec = flow_management_sdk.CategoryMapping()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create DsCategoryMapping spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_category_mapping(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating DsCategoryMapping",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.DS_CATEGORY_MAPPING
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_ds_category_mapping(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for DsCategoryMapping"
                ),
                msg="Failed to get entity ext_id from task for DsCategoryMapping",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare current and target dicts to determine if any change is needed."""
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    return old_spec_dict == update_spec_dict


def update_ds_category_mapping(module, api_instance, result):
    """Update an existing DsCategoryMapping identified by ext_id."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_ds_category_mapping(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating DsCategoryMapping", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update DsCategoryMapping spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    # Read-only fields populated by the platform must not be sent on update.
    strip_read_only_fields(update_spec, fields=["links", "tenant_id"])

    resp = None
    try:
        resp = api_instance.update_ds_category_mapping_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating DsCategoryMapping",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ds_category_mapping(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_ds_category_mapping(module, api_instance, result):
    """Delete a DsCategoryMapping identified by ext_id."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "DsCategoryMapping with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_ds_category_mapping(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_ds_category_mapping_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting DsCategoryMapping",
        )
    task_ext_id = getattr(resp.data, "ext_id", None) if resp else None
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_directory_server_configs_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ds_category_mapping(module, api_instance, result)
        else:
            create_ds_category_mapping(module, api_instance, result)
    else:
        delete_ds_category_mapping(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
