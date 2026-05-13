#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_category_mapping_v2
short_description: Create, Update, Delete DS category mapping
version_added: 2.6.0
description:
    - Create, Update, Delete a mapping between a group in Active Directory and a Category.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a DS Category Mapping) -
      Operation Name: Create Category Mapping -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - >-
      B(Delete a DS Category Mapping) -
      Operation Name: Delete Category Mapping -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - >-
      B(Update a DS Category Mapping by external identifier) -
      Operation Name: Update Category Mapping -
      Required Roles: Flow Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
    ext_id:
        description:
            - External ID to update or delete specific DS category mapping.
        type: str
        required: false
    name:
        description:
            - A short identifier / name of the DS category mapping.
        type: str
    category_name:
        description:
            - The category key name for the mapping.
        type: str
    category_value:
        description:
            - The category value for the mapping.
        type: str
    ad_info:
        description:
            - Active Directory information for the category mapping.
        type: dict
        suboptions:
            directory_service_reference:
                description:
                    - External ID of the directory service configuration.
                type: str
                required: true
            object_identifier:
                description:
                    - The object identifier (UUID) used in the mapping.
                type: str
                required: true
            object_path:
                description:
                    - The LDAP path of the AD object.
                type: str
                required: false

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create DS category mapping
  nutanix.ncp.ntnx_category_mapping_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    name: "ansible-category-mapping"
    category_name: "AppType"
    category_value: "Default"
    ad_info:
      directory_service_reference: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
      object_identifier: "00000000-0000-0000-0000-000000000001"
  register: result
  ignore_errors: true

- name: Update DS category mapping
  nutanix.ncp.ntnx_category_mapping_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    ext_id: "b215708c-252f-400c-bc90-2f36242d3d3c"
    name: "ansible-category-mapping-updated"
    category_name: "AppType"
    category_value: "Default"
    ad_info:
      directory_service_reference: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
      object_identifier: "00000000-0000-0000-0000-000000000001"
  register: result
  ignore_errors: true

- name: Delete DS category mapping
  nutanix.ncp.ntnx_category_mapping_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: absent
    ext_id: "b215708c-252f-400c-bc90-2f36242d3d3c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response when we create, update or delete a DS category mapping.
    - Response will contain DS category mapping details if C(wait) is true and the operation is create or update.
    - Response will contain Task details if C(wait) is true and the operation is delete.
    - Response will contain Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
        "ad_info": {
            "directory_service_reference": "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a",
            "object_identifier": "00000000-0000-0000-0000-000000000001",
            "object_path": null,
            "status": "USABLE"
        },
        "category_name": "AppType",
        "category_value": "Default",
        "ext_id": "b215708c-252f-400c-bc90-2f36242d3d3c",
        "links": null,
        "name": "ansible-category-mapping",
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str

failed:
    description: This field indicates if the task execution failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Failed generating create DS category mapping Spec"

ext_id:
  description: The DS category mapping ext_id
  returned: always
  type: str
  sample: "b215708c-252f-400c-bc90-2f36242d3d3c"

task_ext_id:
  description: The task ext_id for the operation
  returned: when applicable
  type: str

skipped:
  description: Whether the operation was skipped due to idempotency
  returned: when idempotent
  type: bool
  sample: true
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_microseg_py_client as mic_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as mic_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ad_info_spec = dict(
        directory_service_reference=dict(type="str", required=True),
        object_identifier=dict(type="str", required=True),
        object_path=dict(type="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        category_name=dict(type="str"),
        category_value=dict(type="str"),
        ad_info=dict(
            type="dict",
            options=ad_info_spec,
            obj=mic_sdk.AdInfo,
        ),
    )

    return module_args


def create_category_mapping(module, api_instance, result):
    sg = SpecGenerator(module)
    default_spec = mic_sdk.CategoryMapping()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create DS category mapping Spec", **result
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
            msg="Api Exception raised while creating DS category mapping",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.CATEGORY_MAPPING
        )
        if ext_id:
            resp = get_ds_category_mapping(module, api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_category_mapping_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False

    return True


def update_category_mapping(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_ds_category_mapping(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating DS category mapping update spec", **result
        )

    sg2 = SpecGenerator(module)
    default_spec = mic_sdk.CategoryMapping()
    spec, err2 = sg2.generate_spec(obj=default_spec)

    if err2:
        result["error"] = err2
        module.fail_json(
            msg="Failed generating DS category mapping update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_category_mapping_idempotency(
        current_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    etag = get_etag(current_spec)
    kwargs = {"if_match": etag}
    resp = None

    try:
        resp = api_instance.update_ds_category_mapping_by_id(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating DS category mapping",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ds_category_mapping(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_category_mapping(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "DS category mapping with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    try:
        resp = api_instance.delete_ds_category_mapping_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting DS category mapping",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("ext_id",)),
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
        "error": None,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_directory_server_configs_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_category_mapping(module, api_instance, result)
        else:
            create_category_mapping(module, api_instance, result)
    else:
        delete_category_mapping(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
