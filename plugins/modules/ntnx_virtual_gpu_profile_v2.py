#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_virtual_gpu_profile_v2
short_description: Manage Virtual GPU Profiles (read-only shim) in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module is the CRUD-style counterpart to
    M(nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2) for the Prism Central
    V4 C(VirtualGpuProfile) entity in the C(clustermgmt) namespace.
  - Virtual GPU profiles describe functionally equivalent vGPU devices
    (frame buffer size, number of virtual display heads, max resolution,
    licenses, etc.) that are discovered from the AHV Acropolis Device
    Manager (ADM) and aggregated at Prism Central per cluster.
  - The V4 C(clustermgmt) API only exposes a read-only C(list) endpoint for
    C(VirtualGpuProfile); there are no supported Create, Update, or Delete
    endpoints. Because of that, when C(state=present) or C(state=absent) is
    invoked this module fails with a descriptive message instead of
    silently performing a no-op. Use
    M(nutanix.ncp.ntnx_virtual_gpu_profiles_info_v2) to fetch profiles.
  - In C(check_mode) the module returns the requested spec without failing,
    so the module can still be included in dry-run playbooks.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to
    the user performing the operation.
  - >-
    B(View Cluster Vgpu Profiles) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
    Project Manager, Super Admin, Self-Service Admin (deprecated)
  - >-
    The V4 C(clustermgmt) API exposes only
    C(listVirtualGpuProfiles)
    (C(GET /api/clustermgmt/v4.3/config/clusters/{clusterExtId}/virtual-gpu-profiles)).
    There are no Create, Update, or Delete operations for this entity, so
    C(state=present) / C(state=absent) fail outside of C(check_mode).
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided the
        operation would be create Virtual GPU profile, which is B(not
        supported) by the V4 API - the module fails with a descriptive
        message.
      - If C(state) is set to C(present) and C(ext_id) is provided the
        operation would be update Virtual GPU profile, which is B(not
        supported) by the V4 API - the module fails with a descriptive
        message.
      - If C(state) is set to C(absent) and C(ext_id) is provided the
        operation would be delete Virtual GPU profile, which is B(not
        supported) by the V4 API - the module fails with a descriptive
        message.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - External ID (UUID) of the Prism Element cluster that owns the
        Virtual GPU profile.
      - Maps to the C(clusterExtId) path parameter of
        C(listVirtualGpuProfiles).
    type: str
    required: false
  ext_id:
    description:
      - The external ID of the Virtual GPU profile.
      - Required for update and delete operations. The V4 API does not
        support Create, Update, or Delete for this entity.
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
- name: Attempt to create a Virtual GPU profile (will fail - read-only entity)
  nutanix.ncp.ntnx_virtual_gpu_profile_v2:
    state: present
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Attempt to update a Virtual GPU profile (will fail - read-only entity)
  nutanix.ncp.ntnx_virtual_gpu_profile_v2:
    state: present
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"
  register: result
  ignore_errors: true

- name: Attempt to delete a Virtual GPU profile (will fail - read-only entity)
  nutanix.ncp.ntnx_virtual_gpu_profile_v2:
    state: absent
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The full request spec that the module would have submitted if the
      operation were supported. Returned only in C(check_mode).
    - Outside of C(check_mode) the module fails before an SDK call is
      attempted because the C(clustermgmt) V4 SDK is read-only for this
      entity.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "ext_id": null,
      "state": "present"
    }

task_ext_id:
  description:
    - The external ID of the task.
    - Always null because no task is submitted (the SDK does not expose a
      task-producing endpoint for this entity).
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the Virtual GPU profile.
  returned: always
  type: str
  sample: "0005a1ef-b3aa-4fc4-9c8c-1c8c8f3a0000"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

skipped:
  description:
    - This indicates whether the task was skipped.
    - Applicable when the module cannot proceed (for example when the
      requested operation is not supported by the V4 SDK).
  returned: when applicable
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message describing the outcome of the task.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: >-
    Virtual GPU profile create is not supported by the clustermgmt V4 SDK.
    Use ntnx_virtual_gpu_profiles_info_v2 to list profiles.
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.utils import validate_required_params  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client  # noqa: F401,E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as ntnx_clustermgmt_py_client  # noqa: F401,E402  # fmt: skip

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_UNSUPPORTED_MSG = (
    "Virtual GPU profile {op} is not supported by the clustermgmt V4 SDK. "
    "Use ntnx_virtual_gpu_profiles_info_v2 to list profiles."
)


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str"),
        ext_id=dict(type="str"),
    )
    return module_args


def _spec_snapshot(module):
    """Return a JSON-safe dict describing the requested operation.

    Used in check_mode so callers still get a deterministic ``response``
    payload without contacting Prism Central.
    """
    return {
        "state": module.params.get("state"),
        "cluster_ext_id": module.params.get("cluster_ext_id"),
        "ext_id": module.params.get("ext_id"),
    }


def create_VirtualGpuProfile(module, result):
    validate_required_params(module, ["cluster_ext_id"])

    if module.check_mode:
        result["response"] = _spec_snapshot(module)
        result["msg"] = _UNSUPPORTED_MSG.format(op="create")
        result["skipped"] = True
        return

    result["failed"] = True
    result["msg"] = _UNSUPPORTED_MSG.format(op="create")
    result["response"] = _spec_snapshot(module)
    module.fail_json(**result)


def update_VirtualGpuProfile(module, result):
    validate_required_params(module, ["cluster_ext_id", "ext_id"])

    result["ext_id"] = module.params.get("ext_id")

    if module.check_mode:
        result["response"] = _spec_snapshot(module)
        result["msg"] = _UNSUPPORTED_MSG.format(op="update")
        result["skipped"] = True
        return

    result["failed"] = True
    result["msg"] = _UNSUPPORTED_MSG.format(op="update")
    result["response"] = _spec_snapshot(module)
    module.fail_json(**result)


def delete_VirtualGpuProfile(module, result):
    validate_required_params(module, ["cluster_ext_id", "ext_id"])

    result["ext_id"] = module.params.get("ext_id")

    if module.check_mode:
        result["response"] = _spec_snapshot(module)
        result["msg"] = _UNSUPPORTED_MSG.format(op="delete")
        result["skipped"] = True
        return

    result["failed"] = True
    result["msg"] = _UNSUPPORTED_MSG.format(op="delete")
    result["response"] = _spec_snapshot(module)
    module.fail_json(**result)


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
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_VirtualGpuProfile(module, result)
        else:
            create_VirtualGpuProfile(module, result)
    else:
        delete_VirtualGpuProfile(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
