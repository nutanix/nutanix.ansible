#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_submit_batch_v2
short_description: Submit a batch operation in Nutanix Prism Central
version_added: 2.7.0
description:
    - Submit a batch operation to perform bulk CRUD or custom actions on multiple entities
      in a single asynchronous API call.
    - The batch service returns a parent task (Ergon) that fans out one subtask per
      payload item; the overall progress and per-item status can be polled using the
      returned C(task_ext_id) or fetched later via M(nutanix.ncp.ntnx_submit_batches_info_v2).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Submit a Batch) -
      Required Roles: Super Admin, Prism Admin (and the underlying entity-level roles
      required to execute each sub-request in the payload, e.g.
      B(Virtual Machine Admin) for VM operations).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    state:
        description:
            - State of the module.
            - This is an action-type module, only C(present) is supported.
            - If C(state) is C(present), the module will submit the batch operation.
        type: str
        choices:
            - present
        default: present
    metadata:
        description:
            - The metadata section of the batch operation input specification.
            - Describes the target URI, action type and batch-level execution options.
        type: dict
        required: true
        suboptions:
            action:
                description:
                    - Type of batch action to perform on the target URI.
                    - C(CREATE) creates entities in bulk.
                    - C(MODIFY) updates entities in bulk.
                    - C(DELETE) deletes entities in bulk.
                    - C(ACTION) executes a custom action in bulk.
                type: str
                required: true
                choices:
                    - CREATE
                    - MODIFY
                    - DELETE
                    - ACTION
            name:
                description:
                    - User friendly name for the batch.
                    - Maximum 256 characters.
                type: str
                required: true
            uri:
                description:
                    - The absolute URI of the API operation on which batching will be
                      performed (e.g. C(/api/networking/v4.0/config/address-groups)).
                type: str
                required: true
            should_stop_on_error:
                description:
                    - A flag indicating whether the batch processing should halt or
                      continue when an error response is received from the server
                      during the execution of a batch chunk.
                type: bool
                required: false
                default: false
            chunk_size:
                description:
                    - The chunk size to use during the batching operation.
                    - Minimum value is 1.
                type: int
                required: false
                default: 1
    payload:
        description:
            - The list of payload items for the batch operation.
            - Each item contains an optional per-item metadata block (headers / path
              parameters) and the entity data to submit.
        type: list
        elements: dict
        required: true
        suboptions:
            metadata:
                description:
                    - Per-item metadata (headers / path parameters) applied to the
                      individual sub-request.
                type: dict
                required: false
                suboptions:
                    headers:
                        description:
                            - List of header parameters to apply to this specific
                              sub-request.
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                            name:
                                description:
                                    - Name of the header parameter.
                                    - Maximum 256 characters.
                                type: str
                                required: true
                            value:
                                description:
                                    - Value of the header parameter.
                                type: str
                                required: true
                    path:
                        description:
                            - List of path parameters to substitute in the target URI
                              for this specific sub-request (for example C(extId) when
                              the URI is templated like C(/foo/{extId})).
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                            name:
                                description:
                                    - Name of the path parameter.
                                    - Maximum 256 characters.
                                type: str
                                required: true
                            value:
                                description:
                                    - Value of the path parameter.
                                type: str
                                required: true
            data:
                description:
                    - The data section (JSON body) of the payload provided to the
                      batch operation.
                    - The schema of this dict is defined by the target URI's API
                      contract (for example an address-group create body).
                type: dict
                required: false
    request_id:
        description:
            - Idempotency-key value sent as the C(NTNX-Request-Id) header on the
              batch submission call.
            - Required by the Prism Central batch service to safely retry a
              submission; when omitted, a fresh UUID is auto-generated per
              invocation.
        type: str
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
- name: Submit a batch to create multiple address groups
  nutanix.ncp.ntnx_submit_batch_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    metadata:
      action: CREATE
      name: "ansible_batch_create_address_groups"
      uri: "/api/microseg/v4.0/config/address-groups"
      should_stop_on_error: false
      chunk_size: 2
    payload:
      - metadata:
          headers:
            - name: "Content-Type"
              value: "application/json"
        data:
          name: "ag_batch_1"
          description: "Address group #1 created via SubmitBatch"
          ipv4Addresses:
            - value: "10.0.0.1"
              prefixLength: 32
      - metadata:
          headers:
            - name: "Content-Type"
              value: "application/json"
        data:
          name: "ag_batch_2"
          description: "Address group #2 created via SubmitBatch"
          ipv4Addresses:
            - value: "10.0.0.2"
              prefixLength: 32
  register: batch_result

- name: Submit a batch to delete multiple address groups by extId
  nutanix.ncp.ntnx_submit_batch_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    metadata:
      action: DELETE
      name: "ansible_batch_delete_address_groups"
      uri: "/api/microseg/v4.0/config/address-groups/{extId}"
      should_stop_on_error: false
      chunk_size: 1
    payload:
      - metadata:
          path:
            - name: "extId"
              value: "0e2cf83a-b0f2-4a35-9db2-1111aaaa1111"
      - metadata:
          path:
            - name: "extId"
              value: "0e2cf83a-b0f2-4a35-9db2-2222bbbb2222"
  register: batch_result
"""

RETURN = r"""
response:
    description:
        - Response for the SubmitBatch operation.
        - If C(wait) is true the response contains the completed parent task details
          (Ergon task, including subtasks and per-item outcomes).
        - If C(wait) is false the response contains the immediately-returned parent
          task reference.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T15:34:15.092891+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T15:34:12.593544+00:00",
            "entities_affected": [
                {
                    "ext_id": "0e2cf83a-b0f2-4a35-9db2-1111aaaa1111",
                    "name": "ag_batch_1",
                    "rel": "networking:config:address-group"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T15:34:15.092888+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 2,
            "operation": "kSubmitBatch",
            "operation_description": "Submit batch operation",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T15:34:12.602785+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:f9856c8f-d619-42d6-65b3-5651e8825a6c",
                    "href": "https://10.0.0.1:9440/api/prism/v4.0/config/tasks/ZXJnb24=:f9856c8f-d619-42d6-65b3-5651e8825a6c",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }

task_ext_id:
    description: External ID of the parent task representing this batch submission.
    returned: always
    type: str
    sample: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"

ext_id:
    description:
        - The external ID of the submitted batch (populated from the parent task's
          entity reference when available; may be C(null) if the SDK/task does not
          surface a distinct batch ext_id yet).
    returned: always
    type: str
    sample: "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while submitting batch"

error:
    description:
        - This field typically holds information about if the task have errors
          that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import uuid  # noqa: E402
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

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
        ),
        path=dict(
            type="list",
            elements="dict",
            options=path_spec,
            obj=prism_sdk.BatchSpecPayloadMetadataPath,
        ),
    )

    payload_spec = dict(
        metadata=dict(
            type="dict",
            options=payload_metadata_spec,
            obj=prism_sdk.BatchSpecPayloadMetadata,
        ),
        data=dict(type="dict"),
    )

    metadata_spec = dict(
        action=dict(
            type="str",
            required=True,
            choices=["CREATE", "MODIFY", "DELETE", "ACTION"],
            obj=prism_sdk.ActionType,
        ),
        name=dict(type="str", required=True),
        uri=dict(type="str", required=True),
        should_stop_on_error=dict(type="bool", default=False),
        chunk_size=dict(type="int", default=1),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        metadata=dict(
            type="dict",
            required=True,
            options=metadata_spec,
            obj=prism_sdk.BatchSpecMetadata,
        ),
        payload=dict(
            type="list",
            elements="dict",
            required=True,
            options=payload_spec,
            obj=prism_sdk.BatchSpecPayload,
        ),
        request_id=dict(type="str"),
    )
    return module_args


def submit_batch(module, api_instance, result):
    """Submit a batch operation and (optionally) wait for the parent task."""
    sg = SpecGenerator(module)
    default_spec = prism_sdk.BatchSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating submit batch spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # The Prism v4 batch endpoint requires an idempotency-key header
    # (`NTNX-Request-Id`). Auto-generate one per invocation unless the user
    # explicitly supplied `request_id` (useful for safe retries).
    request_id = module.params.get("request_id") or str(uuid.uuid4())
    kwargs = {"NTNX-Request-Id": request_id}

    resp = None
    try:
        resp = api_instance.submit_batch(body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while submitting batch",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    # SubmitBatch returns a task reference; batch ext_id is surfaced through
    # the parent task, so mirror the task ext_id here for consistency with
    # other action-style v2 modules until a distinct batch ext_id is exposed.
    result["ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        # A batch task can legitimately end up in a FAILED / partially-successful
        # state when some subtasks fail. Surface the completed task details to
        # the caller instead of aborting the module so they can inspect per-item
        # outcomes.
        task = wait_for_completion(module, task_ext_id, raise_error=False)
        result["response"] = strip_internal_attributes(task.to_dict())
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
    submit_batch(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
