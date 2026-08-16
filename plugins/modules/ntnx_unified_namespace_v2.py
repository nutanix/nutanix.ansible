#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unified_namespace_v2
short_description: Create, Update, Delete Files Unified Namespace in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Files Unified Namespace resources in Nutanix Prism Central.
  - A Unified Namespace (also known as Federation Policy) pools a single file namespace across multiple
    Nutanix and/or external file servers so that clients see a single logical share hierarchy.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a Unified Namespace) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Update a Unified Namespace) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete a Unified Namespace) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create Unified Namespace.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update Unified Namespace.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete Unified Namespace.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Unified Namespace.
      - Required for update and delete operations.
    type: str
    required: false
  namespace_member_configs:
    description:
      - List of file server members that make up the Unified Namespace.
      - Exactly one member MUST be marked as core (C(is_core_member=true)) — the core member acts as
        the master file server and represents the entry point of the federated namespace.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      file_server_ext_id:
        description:
          - External ID of the file server that participates in this Unified Namespace.
        type: str
        required: true
      is_core_member:
        description:
          - Whether this file server is the core (master) member of the federation.
          - Exactly one member in a Unified Namespace must be a core member.
        type: bool
        required: false
      file_server_type:
        description:
          - Origin/management type of the file server participating in the federation.
          - C(NUTANIX) refers to standard Nutanix Files instances running on AOS clusters.
          - C(EXTERNAL) refers to third-party (non-Nutanix) file servers, typically used as
            migration sources.
        type: str
        required: false
        choices:
          - NUTANIX
          - EXTERNAL
      should_include_all_mount_targets:
        description:
          - Whether all mount targets (shares) hosted on this member should be automatically
            included in the federated namespace.
        type: bool
        required: false
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
- name: Create Unified Namespace with a Nutanix core member and one edge member
  nutanix.ncp.ntnx_unified_namespace_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    namespace_member_configs:
      - file_server_ext_id: "11111111-1111-1111-1111-111111111111"
        is_core_member: true
        file_server_type: "NUTANIX"
        should_include_all_mount_targets: true
      - file_server_ext_id: "22222222-2222-2222-2222-222222222222"
        is_core_member: false
        file_server_type: "NUTANIX"
        should_include_all_mount_targets: true
  register: result
  ignore_errors: true

- name: Update Unified Namespace to add an external migration source
  nutanix.ncp.ntnx_unified_namespace_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    namespace_member_configs:
      - file_server_ext_id: "11111111-1111-1111-1111-111111111111"
        is_core_member: true
        file_server_type: "NUTANIX"
        should_include_all_mount_targets: true
      - file_server_ext_id: "22222222-2222-2222-2222-222222222222"
        is_core_member: false
        file_server_type: "NUTANIX"
        should_include_all_mount_targets: true
      - file_server_ext_id: "33333333-3333-3333-3333-333333333333"
        is_core_member: false
        file_server_type: "EXTERNAL"
        should_include_all_mount_targets: false
  register: result
  ignore_errors: true

- name: Delete Unified Namespace
  nutanix.ncp.ntnx_unified_namespace_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a Unified Namespace.
    - If the operation is create or update and C(wait) is true, it will return the Unified Namespace details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
      "namespace_member_configs": [
        {
          "file_server_ext_id": "11111111-1111-1111-1111-111111111111",
          "is_core_member": true,
          "file_server_type": "NUTANIX",
          "should_include_all_mount_targets": true
        },
        {
          "file_server_ext_id": "22222222-2222-2222-2222-222222222222",
          "is_core_member": false,
          "file_server_type": "NUTANIX",
          "should_include_all_mount_targets": true
        }
      ],
      "created_timestamp_usecs": null,
      "modified_timestamp_usecs": null,
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
    - The external ID of the Unified Namespace.
  returned: always
  type: str
  sample: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. idempotent update).
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating unified namespace"
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
    get_unified_namespaces_api_instance,
)
from ..module_utils.v4.files.helpers import get_unified_namespace  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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


def get_module_spec():

    namespace_member_config_spec = dict(
        file_server_ext_id=dict(type="str", required=True),
        is_core_member=dict(type="bool", required=False),
        file_server_type=dict(
            type="str",
            required=False,
            choices=["NUTANIX", "EXTERNAL"],
            obj=files_sdk.FileServerType,
        ),
        should_include_all_mount_targets=dict(type="bool", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        namespace_member_configs=dict(
            type="list",
            elements="dict",
            options=namespace_member_config_spec,
            obj=files_sdk.NamespaceMemberConfig,
        ),
    )
    return module_args


def create_unified_namespace(module, api_instance, result):
    validate_required_params(module, ["namespace_member_configs"])
    sg = SpecGenerator(module)
    default_spec = files_sdk.UnifiedNamespace()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create unified namespace spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_unified_namespace(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating unified namespace",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.UNIFIED_NAMESPACE
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_unified_namespace(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Unified Namespace"
                ),
                msg="Failed to get entity ext_id from task for Unified Namespace",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    # Keep only fields the user can influence when comparing
    for _spec in (old_spec_dict, update_spec_dict):
        for field in (
            "created_timestamp_usecs",
            "modified_timestamp_usecs",
            "links",
            "tenant_id",
            "ext_id",
        ):
            _spec.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_unified_namespace(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_unified_namespace(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating unified namespace", **result
        )

    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update unified namespace spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Unified namespace with ext_id: {0} is already in the desired state.".format(
                ext_id
            ),
            **result,
        )

    resp = None
    try:
        resp = api_instance.update_unified_namespace_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating unified namespace",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_unified_namespace(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_unified_namespace(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Unified namespace with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_unified_namespace_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting unified namespace",
        )
    task_ext_id = resp.data.ext_id
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
    api_instance = get_unified_namespaces_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_unified_namespace(module, api_instance, result)
        else:
            create_unified_namespace(module, api_instance, result)
    else:
        delete_unified_namespace(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
