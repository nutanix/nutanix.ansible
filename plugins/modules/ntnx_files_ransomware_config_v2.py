#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_ransomware_config_v2
short_description: Create, Update, Delete ransomware configuration of a file server in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete the ransomware configuration of a file server in Nutanix Prism Central.
  - Ransomware protection blocks and detects the configured file extension patterns on the file server.
  - This module uses PC v4 APIs based SDKs
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be to create the ransomware configuration.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be to update the ransomware configuration.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be to delete the ransomware configuration.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server on which the ransomware configuration is managed.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the ransomware configuration of the file server.
      - Required for update and delete operations.
    type: str
    required: false
  file_extensions:
    description:
      - Ransomware file patterns to block and detect on the file server.
      - For example C(*.txt), C(?.db).
      - Required for the create operation.
    type: list
    elements: str
    required: false
  excluded_mount_target_ext_ids:
    description:
      - List of mount targets (shares) to be excluded from the ransomware configuration.
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
- name: Create ransomware config for a file server
  nutanix.ncp.ntnx_files_ransomware_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    file_extensions:
      - "*.crypto"
      - "*.locked"
      - "?.enc"
    excluded_mount_target_ext_ids:
      - "5f0d1c2b-3a4e-4d5c-8b7a-9e0f1a2b3c4d"
  register: result
  ignore_errors: true

- name: Update ransomware config for a file server
  nutanix.ncp.ntnx_files_ransomware_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    file_extensions:
      - "*.crypto"
      - "*.locked"
      - "*.ransom"
    excluded_mount_target_ext_ids:
      - "5f0d1c2b-3a4e-4d5c-8b7a-9e0f1a2b3c4d"
      - "7a8b9c0d-1e2f-4a3b-8c4d-5e6f7a8b9c0d"
  register: result
  ignore_errors: true

- name: Delete ransomware config of a file server
  nutanix.ncp.ntnx_files_ransomware_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting the ransomware configuration.
    - If the operation is create or update and C(wait) is true, it will return the ransomware configuration details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "b1c2d3e4-f5a6-4789-90ab-cdef01234567",
      "excluded_mount_target_ext_ids": [
          "5f0d1c2b-3a4e-4d5c-8b7a-9e0f1a2b3c4d"
      ],
      "file_extensions": [
          "*.crypto",
          "*.locked",
          "?.enc"
      ],
      "links": null,
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
    - The external ID of the ransomware configuration.
  returned: always
  type: str
  sample: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
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
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating ransomware config"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_ransomware_configs_api_instance,
)
from ..module_utils.v4.files.helpers import get_ransomware_config  # noqa: E402
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
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Read-only attributes populated by the platform that must not be sent on update.
READ_ONLY_FIELDS = ["links", "tenant_id"]


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        file_extensions=dict(type="list", elements="str"),
        excluded_mount_target_ext_ids=dict(type="list", elements="str"),
    )
    return module_args


def create_ransomware_config(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    validate_required_params(module, ["file_extensions"])
    sg = SpecGenerator(module)
    default_spec = files_sdk.RansomwareConfig()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create ransomware config spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_ransomware_config(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating ransomware config",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.RANSOMWARE_CONFIG
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_ransomware_config(
                module, api_instance, file_server_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Ransomware Config"
                ),
                msg="Failed to get entity ext_id from task for Ransomware Config",
            )
    result["changed"] = True


def check_ransomware_configs_idempotency(old_spec, update_spec):
    """Return True if the existing config already matches the desired spec."""
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_ransomware_config(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_ransomware_config(module, api_instance, file_server_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating ransomware config", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update ransomware config spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_ransomware_configs_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_ransomware_config_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating ransomware config",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ransomware_config(module, api_instance, file_server_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_ransomware_config(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Ransomware config with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_ransomware_config_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting ransomware config",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_ransomware_configs_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_ransomware_config(module, result, api_instance)
        else:
            create_ransomware_config(module, result, api_instance)
    else:
        delete_ransomware_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
