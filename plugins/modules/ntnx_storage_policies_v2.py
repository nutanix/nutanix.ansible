#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_policies_v2
short_description: Create, Update, Delete storage policies in Nutanix Prism Central
version_added: 2.4.0
description:
  - This module allows you to create, update, and delete storage policies in Nutanix Prism Central.
  - For Create operation, at least one storage attribute (compression_spec, encryption_spec, qos_spec, fault_tolerance_spec) must be set to non default value.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - if C(state) is present, it will create or update the storage policy.
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create storage policy.
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update storage policy.
      - If C(state) is set to C(absent) and ext_id is provided then the operation will be delete storage policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the storage policy. Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the storage policy.
      - Required for create operation.
      - Name of the storage policy should be unique.
    type: str
    required: false
  category_ext_ids:
    description:
      - List of external identifiers of Categories included or to be included in the Storage Policy.
    type: list
    elements: str
    required: false
  compression_spec:
    description:
      - Compression parameters for the entities governed by the Storage Policy.
    type: dict
    suboptions:
      compression_state:
        description:
          - Enable or disable Compression for entities governed by the policy.
          - If the user has no explicit Compression preference, the system chooses an appropriate value.
        type: str
        choices:
          - INLINE
          - POSTPROCESS
          - DISABLED
          - SYSTEM_DERIVED
        required: true
    required: false
  encryption_spec:
    description:
      - Encryption parameters for the entities governed by the Storage Policy.
    type: dict
    suboptions:
      encryption_state:
        description:
          - Enable Encryption for entities. Once enabled, it cannot be disabled.
          - If the user does not have an explicit preference to enable Encryption, the system decides on an appropriate value.
        type: str
        choices:
          - ENABLED
          - SYSTEM_DERIVED
        required: true
    required: false
  qos_spec:
    description:
      - Storage QOS parameters for the entities.
    type: dict
    suboptions:
      throttled_iops:
        description:
          - Throttled IOPS for the entities being governed. The block size for the IO is 32kB.
        type: int
        required: true
    required: false
  fault_tolerance_spec:
    description:
      - Fault Tolerance parameters for the entities.
    type: dict
    suboptions:
      replication_factor:
        description:
          - Number of data copies for entities governed by the Storage Policy.
        type: str
        choices:
          - TWO
          - THREE
          - SYSTEM_DERIVED
        required: true
    required: false
  wait:
    description: Wait for the operation to complete.
    type: bool
    required: false
    default: true

extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create storage policy
  nutanix.ncp.ntnx_storage_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "storage_policy_name"
    category_ext_ids:
      - "0a236cc2-7a89-4faf-a05f-c5b358307aa9"
      - "b422bd2d-a765-4fc3-9231-890c85d1d208"
    compression_spec:
      compression_state: "INLINE"
    encryption_spec:
      encryption_state: "ENABLED"
    qos_spec:
      throttled_iops: 100
    fault_tolerance_spec:
      replication_factor: "TWO"
  register: result
  ignore_errors: true

- name: Update storage policy
  nutanix.ncp.ntnx_storage_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    name: "storage_policy_name_updated"
    category_ext_ids:
      - "0ded28e5-0452-4ccc-9f5a-3cb0af58f8a6"
    compression_spec:
      compression_state: "POSTPROCESS"
    encryption_spec:
      encryption_state: "ENABLED"
    qos_spec:
      throttled_iops: 1000
    fault_tolerance_spec:
      replication_factor: "THREE"
  register: result
  ignore_errors: true

- name: Delete Storage Policy
  nutanix.ncp.ntnx_storage_policies_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    state: absent
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting storage policy
    - It will return the storage policy details if the operation is create or update
    - It will return the task details if the operation is delete
  returned: always
  type: dict
  sample:
    {
      "category_ext_ids":
        [
          "5f27dddb-b6bb-4f0f-bd8a-fe9606b79229",
          "b4e890c7-ff0f-4098-8af1-e56fd20e4368",
        ],
      "compression_spec": { "compression_state": "INLINE" },
      "encryption_spec": { "encryption_state": "ENABLED" },
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "fault_tolerance_spec": { "replication_factor": "TWO" },
      "links": null,
      "name": "storage_policy_name",
      "policy_type": "USER",
      "qos_spec": { "throttled_iops": 100 },
      "tenant_id": null,
    }

task_ext_id:
  description:
    - The external id of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external id of the storage policy.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

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

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "state is present but all of the following are missing: name, ext_id"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_storage_policies_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_storage_policy  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_etag  # noqa: E402
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
    import ntnx_datapolicies_py_client as datapolicies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as datapolicies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    compression_spec = dict(
        compression_state=dict(
            type="str",
            choices=[
                "INLINE",
                "POSTPROCESS",
                "DISABLED",
                "SYSTEM_DERIVED",
            ],
            obj=datapolicies_sdk.CompressionState,
            required=True,
        )
    )

    encryption_spec = dict(
        encryption_state=dict(
            type="str",
            choices=[
                "ENABLED",
                "SYSTEM_DERIVED",
            ],
            obj=datapolicies_sdk.EncryptionState,
            required=True,
        )
    )

    qos_spec = dict(throttled_iops=dict(type="int", required=True))

    fault_tolerance_spec = dict(
        replication_factor=dict(
            type="str",
            choices=[
                "TWO",
                "THREE",
                "SYSTEM_DERIVED",
            ],
            required=True,
            obj=datapolicies_sdk.ReplicationFactor,
        )
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        category_ext_ids=dict(type="list", elements="str"),
        compression_spec=dict(
            type="dict", options=compression_spec, obj=datapolicies_sdk.CompressionSpec
        ),
        encryption_spec=dict(
            type="dict", options=encryption_spec, obj=datapolicies_sdk.EncryptionSpec
        ),
        qos_spec=dict(type="dict", options=qos_spec, obj=datapolicies_sdk.QosSpec),
        fault_tolerance_spec=dict(
            type="dict",
            options=fault_tolerance_spec,
            obj=datapolicies_sdk.FaultToleranceSpec,
        ),
    )
    return module_args


def create_storage_policy(module, storage_policies, result):
    sg = SpecGenerator(module)
    default_spec = datapolicies_sdk.StoragePolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create storage policy Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = storage_policies.create_storage_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating storage policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.STORAGE_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_storage_policy(module, storage_policies, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_storage_policy(module, storage_policies, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_storage_policy(module, storage_policies, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating storage policy", **result
        )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update storage policy Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    kwargs = {"if_match": etag}
    resp = None
    if hasattr(update_spec, "policy_type"):
        setattr(update_spec, "policy_type", None)
    try:
        resp = storage_policies.update_storage_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating storage policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        resp = get_storage_policy(module, storage_policies, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_storage_policy(module, storage_policies, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Storage policy with ext_id:{0} will be deleted.".format(ext_id)
        return

    old_spec = get_storage_policy(module, storage_policies, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting storage policy", **result
        )
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = storage_policies.delete_storage_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting storage policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    storage_policies = get_storage_policies_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_storage_policy(module, storage_policies, result)
        else:
            create_storage_policy(module, storage_policies, result)
    else:
        delete_storage_policy(module, storage_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
