#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_reconfigure_cvm_v2
short_description: Reconfigure Controller VMs (CVMs) of a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - Reconfigure the Controller Virtual Machines (CVMs) of a given cluster.
  - This module drives a rolling change across every CVM of the target cluster to
    adjust their vCPU count and/or memory size.
  - Provide at least one of C(num_vcpus) and C(memory_size_bytes) — providing
    both applies both changes in the same rolling operation.
  - Modifying CVM vCPU is not supported through the Prism Central UI (as of AOS 7.5);
    this module is the supported v4 API workflow.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Reconfigure CVMs of a cluster) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module triggers the CVM reconfiguration action.
      - Only C(present) is supported for this action module.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - External ID (UUID) of the cluster whose CVMs are to be reconfigured.
      - Required for triggering the reconfigure CVMs action.
    type: str
    required: true
  num_vcpus:
    description:
      - The desired number of vCPUs to assign to every CVM in the cluster.
      - Must be a positive integer (minimum 1).
      - At least one of C(num_vcpus) and C(memory_size_bytes) must be provided.
    type: int
    required: false
  memory_size_bytes:
    description:
      - The desired memory size, in B(bytes), for every CVM in the cluster.
      - Must be a positive integer (minimum 1).
      - For example, 36 GiB equals 36 * 1024 * 1024 * 1024 = 38654705664 bytes.
      - At least one of C(num_vcpus) and C(memory_size_bytes) must be provided.
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
- name: Reconfigure CVMs of a cluster — change vCPU only
  nutanix.ncp.ntnx_reconfigure_cvm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005f6f4-7b8c-11ee-8a0d-000000000000"
    num_vcpus: 12
  register: result
  ignore_errors: true

- name: Reconfigure CVMs of a cluster — change memory only (36 GiB)
  nutanix.ncp.ntnx_reconfigure_cvm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005f6f4-7b8c-11ee-8a0d-000000000000"
    memory_size_bytes: 38654705664
  register: result
  ignore_errors: true

- name: Reconfigure CVMs of a cluster — change both vCPU and memory
  nutanix.ncp.ntnx_reconfigure_cvm_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005f6f4-7b8c-11ee-8a0d-000000000000"
    num_vcpus: 12
    memory_size_bytes: 38654705664
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for reconfiguring CVMs of the cluster.
    - Task details if C(wait) is C(true) (the task terminal state is returned).
    - Task reference (with task ext_id) if C(wait) is C(false).
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0005f6f4-7b8c-11ee-8a0d-000000000000"
      ],
      "completed_time": "2026-07-20T13:24:11.524581+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T13:20:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "0005f6f4-7b8c-11ee-8a0d-000000000000",
          "name": null,
          "rel": "clustermgmt:config:cluster"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T13:24:11.524581+00:00",
      "legacy_error_message": null,
      "operation": "ReconfigureCvms",
      "operation_description": "Reconfigure CVMs of a cluster",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T13:20:47.185754+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the status/error message emitted by the module.
  returned: When there is an error, or in check mode.
  type: str
  sample: "Api Exception raised while reconfiguring CVMs"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  returned: When an error occurs
  type: str
  sample: "Failed generating spec for reconfiguring CVMs"

failed:
  description: This field typically holds information about whether the task failed.
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task triggered by the reconfigure CVMs action.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the cluster whose CVMs were reconfigured.
  returned: always
  type: str
  sample: "0005f6f4-7b8c-11ee-8a0d-000000000000"
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        num_vcpus=dict(type="int", required=False),
        memory_size_bytes=dict(type="int", required=False),
    )
    return module_args


def reconfigure_cvm(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if (
        module.params.get("num_vcpus") is None
        and module.params.get("memory_size_bytes") is None
    ):
        module.fail_json(
            msg="At least one of 'num_vcpus' or 'memory_size_bytes' must be provided.",
            **result,
        )

    for field in ("num_vcpus", "memory_size_bytes"):
        value = module.params.get(field)
        if value is not None and value < 1:
            module.fail_json(
                msg="Invalid value for '{0}': must be a positive integer (>= 1).".format(
                    field
                ),
                **result,
            )

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.CvmReconfigurationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for reconfiguring CVMs", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "CVMs of cluster with ext_id:{0} will be reconfigured "
            "with the following spec.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.reconfigure_cvms(clusterExtId=ext_id, body=spec)
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
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_cvms_api_instance(module)
    reconfigure_cvm(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
