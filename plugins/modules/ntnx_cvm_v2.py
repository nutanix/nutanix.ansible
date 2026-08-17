#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cvm_v2
short_description: Reconfigure CVMs (Controller VMs) associated with a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to reconfigure CVMs (Controller VMs) within a Nutanix cluster from Prism Central.
  - Reconfiguration is limited to updating vCPU count and memory allocation of the CVMs.
  - The reconfigure operation is asynchronous and returns a task reference; the module waits for the task
    to complete when C(wait) is set to true (default).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Reconfigure CVMs) -
    Required Roles: Prism Admin, Super Admin, Cluster Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module reconfigures the CVMs of the given cluster.
      - This module does not support C(absent) — CVMs cannot be deleted via this API.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - External identifier (UUID) of the parent cluster whose CVMs will be reconfigured.
    type: str
    required: true
  ext_id:
    description:
      - External identifier of a specific CVM that has been reconfigured.
      - Populated in the result after the reconfigure task completes when the task
        reports the affected CVM entity.
    type: str
    required: false
  num_vcpus:
    description:
      - Number of vCPUs to assign to each CVM.
      - Must be a positive integer (minimum 1).
      - At least one of C(num_vcpus) or C(memory_size_bytes) MUST be provided.
    type: int
    required: false
  memory_size_bytes:
    description:
      - Memory (in bytes) to assign to each CVM in the cluster.
      - Must be a positive integer (minimum 1).
      - At least one of C(num_vcpus) or C(memory_size_bytes) MUST be provided.
    type: int
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
- name: Reconfigure CVM vCPUs and memory
  nutanix.ncp.ntnx_cvm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    num_vcpus: 12
    memory_size_bytes: 34359738368
  register: result
  ignore_errors: true

- name: Reconfigure only CVM vCPUs
  nutanix.ncp.ntnx_cvm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    num_vcpus: 10
  register: result
  ignore_errors: true

- name: Reconfigure only CVM memory
  nutanix.ncp.ntnx_cvm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "0006288e-4d5d-4364-0000-000000024e5f"
    memory_size_bytes: 42949672960
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for reconfiguring CVMs within a cluster.
    - Task details when C(wait) is true (task run to completion).
    - Task reference details when C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0006288e-4d5d-4364-0000-000000024e5f"
      ],
      "completed_time": "2026-07-20T12:45:32.524581+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T12:44:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "0006288e-4d5d-4364-0000-000000024e5f",
          "rel": "clustermgmt:config:cluster"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T12:45:32.524581+00:00",
      "legacy_error_message": null,
      "operation": "ReconfigureCvms",
      "operation_description": "Reconfigure CVMs",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T12:44:47.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while reconfiguring CVMs"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str
  sample: "Not Found"

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description:
    - The external ID of the CVM affected by the reconfigure operation, when reported by the task.
  returned: always
  type: str
  sample: "6a24ee94-8c26-4d10-9c60-6c67d4c47dc2"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cvms_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        num_vcpus=dict(type="int", required=False),
        memory_size_bytes=dict(type="int", required=False),
    )
    return module_args


def _extract_cvm_ext_id_from_task(task):
    """Return the CVM ext_id from a completed reconfigure task, if reported.

    The ReconfigureCvms task normally reports the parent cluster as the
    affected entity. Some backends also emit an entry for the CVM itself in
    ``entities_affected``; when present, we prefer that.
    """
    entities_affected = getattr(task, "entities_affected", None) or []
    fallback_ext_id = None
    for entity in entities_affected:
        rel = getattr(entity, "rel", "") or ""
        ext_id = getattr(entity, "ext_id", None)
        if not ext_id:
            continue
        if "cvm" in rel.lower():
            return ext_id
        if fallback_ext_id is None:
            fallback_ext_id = ext_id
    return fallback_ext_id


def reconfigure_Cvm(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")

    if (
        module.params.get("num_vcpus") is None
        and module.params.get("memory_size_bytes") is None
    ):
        module.fail_json(
            msg=(
                "At least one of num_vcpus or memory_size_bytes must be provided "
                "to reconfigure CVMs."
            ),
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.CvmReconfigurationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating CVM reconfiguration spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.reconfigure_cvms(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reconfiguring CVMs",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        cvm_ext_id = _extract_cvm_ext_id_from_task(task)
        if cvm_ext_id:
            result["ext_id"] = cvm_ext_id
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_one_of=[("num_vcpus", "memory_size_bytes")],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": module.params.get("ext_id"),
        "task_ext_id": None,
    }

    api_instance = get_cvms_api_instance(module)
    reconfigure_Cvm(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
