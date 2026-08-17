#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_batch_v2
short_description: Submit a batch operation in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to submit a bulk (batch) operation in Nutanix Prism Central.
  - >-
    A batch is a JSON-driven request that groups multiple CRUD or action calls
    against one entity type (VMs, Categories, Subnets, Images, LCM, ...) into a
    single asynchronous request. The batch service returns a parent task whose
    subtasks track each individual operation.
  - The module returns the parent task reference; use M(nutanix.ncp.ntnx_pc_tasks_info_v2)
    to poll the task status.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Submit a batch operation) -
      Required Roles: Prism Admin, Super Admin. The user must also have the entity-level
      permissions for every operation carried in the batch payload.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported; submitting a batch is an action.
    type: str
    choices:
      - present
    default: present
  metadata:
    description:
      - Metadata describing the batch request as a whole.
      - Required for submit operation.
    type: dict
    required: false
    suboptions:
      action:
        description:
          - Type of action carried by every payload entry in this batch.
          - C(CREATE), C(MODIFY) and C(DELETE) map to the standard entity CRUD verbs.
          - C(ACTION) is used for entity actions such as power state changes on VMs.
        type: str
        choices:
          - ACTION
          - CREATE
          - DELETE
          - MODIFY
        required: false
      name:
        description:
          - Human-readable name of the batch. Shown in the tasks list and useful
            for correlating batches across audit logs.
        type: str
        required: false
      uri:
        description:
          - Target REST URI (relative to the Prism Central base URL) against which
            each payload entry is applied.
          - Example - C(/api/vmm/v4.0/ahv/config/vms) for a VM bulk create.
        type: str
        required: false
      should_stop_on_error:
        description:
          - Whether the batch service should stop processing further payload
            entries as soon as one of them fails.
        type: bool
        required: false
      chunk_size:
        description:
          - Number of payload entries the batch service will execute in parallel.
          - Defaults to C(1) on the server (sequential execution).
        type: int
        required: false
  payload:
    description:
      - Ordered list of individual operations that make up the batch.
      - Each entry has its own request C(metadata) (headers/path) and a free-form
        C(data) body specific to the target entity's schema.
      - Required for submit operation.
    type: list
    elements: dict
    required: false
    suboptions:
      metadata:
        description:
          - Per-entry request metadata carrying HTTP headers and path parameters
            that the batch service should apply when calling the target entity API.
        type: dict
        required: false
        suboptions:
          headers:
            description:
              - HTTP headers to be sent for this payload entry.
              - Use this to pass conditional headers such as C(If-Match) with an ETag.
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - HTTP header name.
                type: str
                required: true
              value:
                description:
                  - HTTP header value.
                type: str
                required: true
          path:
            description:
              - Path parameters to substitute in the target URI (for example
                C(extId) when the URI is C(/vms/{extId})).
            type: list
            elements: dict
            required: false
            suboptions:
              name:
                description:
                  - Path parameter name (matches the placeholder in the target URI).
                type: str
                required: true
              value:
                description:
                  - Path parameter value.
                type: str
                required: true
      data:
        description:
          - Free-form request body sent as the individual operation's payload.
          - The exact schema depends on the entity C(uri) targeted by the batch
            metadata (VM create body, Category update body, etc.).
        type: dict
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
- name: Submit a batch to create multiple categories
  nutanix.ncp.ntnx_batch_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    metadata:
      action: CREATE
      name: "ansible-batch-create-categories"
      uri: "/api/prism/v4.1/config/categories"
      should_stop_on_error: false
      chunk_size: 2
    payload:
      - metadata:
          headers:
            - name: "Content-Type"
              value: "application/json"
        data:
          key: "ansible-batch-key-1"
          value: "one"
          description: "Category created via ansible batch"
      - metadata:
          headers:
            - name: "Content-Type"
              value: "application/json"
        data:
          key: "ansible-batch-key-1"
          value: "two"
          description: "Category created via ansible batch"
  register: result
  ignore_errors: true

- name: Submit a batch that stops on the first error
  nutanix.ncp.ntnx_batch_v2:
    metadata:
      action: MODIFY
      name: "ansible-batch-modify"
      uri: "/api/prism/v4.1/config/categories"
      should_stop_on_error: true
      chunk_size: 1
    payload:
      - metadata:
          headers:
            - name: "If-Match"
              value: "W/\"0-1\""
          path:
            - name: "extId"
              value: "6f8b4a2e-1111-2222-3333-abcdef012345"
        data:
          description: "Renamed via ansible batch"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response returned by the Submit Batch API.
    - When C(wait) is true the response is replaced by the final batch task details.
    - When C(wait) is false the response is the initial task reference returned
      by the batch service.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-20T15:30:22.514+00:00",
      "created_time": "2026-07-20T15:30:12.001+00:00",
      "entities_affected": [
        {
          "ext_id": "0005b21e-ansible-batch",
          "rel": "prism:operations:batch"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8",
      "operation": "BATCH-CREATE",
      "operation_description": "Submit Batch",
      "progress_percentage": 100,
      "started_time": "2026-07-20T15:30:12.010+00:00",
      "status": "SUCCEEDED",
      "sub_tasks": [
        {
          "ext_id": "ZXJnb24=:0d18cb98-3362-412e-87ef-0566c65a4223",
          "rel": "subtask"
        }
      ]
    }

task_ext_id:
  description:
    - External ID of the parent batch task.
    - Use it with M(nutanix.ncp.ntnx_pc_tasks_info_v2) to inspect subtasks and status.
  returned: always
  type: str
  sample: "ZXJnb24=:e38e02b7-d946-4069-8291-e9407e3a15d8"

ext_id:
  description:
    - External ID of the submitted Batch entity, if the batch service returned one
      in the task entities_affected.
  returned: when the batch service returns a Batch entity ext_id
  type: str
  sample: "0005b21e-ansible-batch"

changed:
  description: Indicates whether the module submitted a batch request.
  returned: always
  type: bool
  sample: true

msg:
  description: Message returned by the module.
  returned: When there is an error or a check-mode invocation
  type: str
  sample: "Api Exception raised while submitting batch"

error:
  description: Detailed error information if the module failed.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the module failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_batches_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    header_spec = dict(
        name=dict(type="str", required=True),
        value=dict(type="str", required=True),
    )

    path_spec = dict(
        name=dict(type="str", required=True),
        value=dict(type="str", required=True),
    )

    payload_metadata_spec = dict(
        headers=dict(
            type="list",
            elements="dict",
            options=header_spec,
            obj=prism_sdk.BatchSpecPayloadMetadataHeader,
            required=False,
        ),
        path=dict(
            type="list",
            elements="dict",
            options=path_spec,
            obj=prism_sdk.BatchSpecPayloadMetadataPath,
            required=False,
        ),
    )

    payload_spec = dict(
        metadata=dict(
            type="dict",
            options=payload_metadata_spec,
            obj=prism_sdk.BatchSpecPayloadMetadata,
            required=False,
        ),
        data=dict(type="dict", required=False),
    )

    batch_metadata_spec = dict(
        action=dict(
            type="str",
            choices=["ACTION", "CREATE", "DELETE", "MODIFY"],
            obj=prism_sdk.ActionType,
            required=False,
        ),
        name=dict(type="str", required=False),
        uri=dict(type="str", required=False),
        should_stop_on_error=dict(type="bool", required=False),
        chunk_size=dict(type="int", required=False),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        metadata=dict(
            type="dict",
            options=batch_metadata_spec,
            obj=prism_sdk.BatchSpecMetadata,
            required=False,
        ),
        payload=dict(
            type="list",
            elements="dict",
            options=payload_spec,
            obj=prism_sdk.BatchSpecPayload,
            required=False,
        ),
    )

    return module_args


def submit_batch(module, result, api_instance):
    """Submit a batch operation to Prism Central."""
    validate_required_params(module, ["metadata", "payload"])

    sg = SpecGenerator(module)
    default_spec = prism_sdk.BatchSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for submit batch", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.submit_batch(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while submitting batch",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        task_dict = task.to_dict() if hasattr(task, "to_dict") else dict(task)
        result["response"] = strip_internal_attributes(task_dict)
        entities_affected = task_dict.get("entities_affected") or []
        for entity in entities_affected:
            entity_ext_id = entity.get("ext_id") if isinstance(entity, dict) else None
            if entity_ext_id and entity_ext_id != task_ext_id:
                result["ext_id"] = entity_ext_id
                break

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_batches_api_instance(module)
    submit_batch(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
