#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_recovery_point_compute_changed_region_v2
short_description: Compute changed regions between two Volume Group disk recovery points
version_added: 2.7.0
description:
    - Compute the list of changed regions of a disk recovery point that is part of a
      Volume Group recovery point.
    - When a reference disk recovery point is supplied, the API returns only the
      regions that changed relative to that reference (incremental / differential
      backup workflows).
    - When no reference is supplied, the API returns the changed regions from
      C(offset) 0 (or the supplied offset) up to C(length) bytes; C(ZEROED) regions
      can be skipped by a backup workflow to optimize network and storage usage.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Compute Volume Group recovery points changed regions) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin,
      Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin,
      Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If C(present), the module invokes the compute-changed-regions action.
            - Any other value causes the module to fail.
        type: str
        choices:
            - present
        default: present
    recovery_point_ext_id:
        description:
            - The external identifier of the top level recovery point that the
              Volume Group recovery point belongs to.
        type: str
        required: true
    volume_group_recovery_point_ext_id:
        description:
            - The external identifier of the Volume Group recovery point that owns
              the target disk recovery point.
        type: str
        required: true
    ext_id:
        description:
            - The external identifier of the disk recovery point on which changed
              regions are computed. This is the C(extId) path parameter of the API.
        type: str
        required: true
    offset:
        description:
            - The start offset (in bytes) from which to compute the changed region.
            - If not provided, the difference is computed from offset C(0).
            - The start offset might be automatically aligned to a system-defined
              block boundary.
        type: int
    length:
        description:
            - The length (in bytes) for which the changed region is computed.
            - If not provided, the difference is computed up to the end of the disk.
        type: int
    block_size_byte:
        description:
            - Block size (in bytes) used to align the returned changed regions.
            - When supplied, offsets and lengths of returned regions are aligned to
              multiples of this value.
        type: int
    reference_volume_group_recovery_point_ext_id:
        description:
            - External identifier of the Volume Group recovery point that owns the
              reference disk recovery point.
            - Required together with C(reference_recovery_point_ext_id) and
              C(reference_disk_recovery_point_ext_id) when computing an incremental
              diff against a reference disk recovery point.
        type: str
    reference_recovery_point_ext_id:
        description:
            - External identifier of the top-level recovery point that owns the
              reference Volume Group recovery point.
            - Required together with C(reference_volume_group_recovery_point_ext_id)
              and C(reference_disk_recovery_point_ext_id) when computing an
              incremental diff against a reference disk recovery point.
        type: str
    reference_disk_recovery_point_ext_id:
        description:
            - External identifier of the reference disk recovery point.
            - Required together with C(reference_volume_group_recovery_point_ext_id)
              and C(reference_recovery_point_ext_id) when computing an incremental
              diff against a reference disk recovery point.
        type: str
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
- name: Compute changed regions for a Volume Group disk recovery point (full scan)
  nutanix.ncp.ntnx_volume_group_recovery_point_compute_changed_region_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    volume_group_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    ext_id: "21d467f0-ccef-4733-91cc-f04db58a92eb"
  register: result

- name: Compute changed regions using an offset, length, and block size
  nutanix.ncp.ntnx_volume_group_recovery_point_compute_changed_region_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    volume_group_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    ext_id: "21d467f0-ccef-4733-91cc-f04db58a92eb"
    offset: 0
    length: 1048576
    block_size_byte: 65536
  register: result

- name: Compute incremental changed regions against a reference disk recovery point
  nutanix.ncp.ntnx_volume_group_recovery_point_compute_changed_region_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    volume_group_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    ext_id: "21d467f0-ccef-4733-91cc-f04db58a92eb"
    reference_recovery_point_ext_id: "6ec8e20d-5662-404f-a475-4ac569521f82"
    reference_volume_group_recovery_point_ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
    reference_disk_recovery_point_ext_id: "91aedb3c-39c9-4750-b553-6e8360d7c1ff"
  register: result
"""
RETURN = r"""
response:
    description:
        - Response returned by the compute-changed-regions action.
        - Contains the list of changed regions for the requested disk recovery point.
        - Each region is described by an C(offset) (bytes), a C(length) (bytes) and a
          C(region_type) (C(REGULAR) or C(ZEROED)).
    returned: always
    type: dict
    sample:
        {
            "changed_regions": [
                {
                    "length": 65536,
                    "offset": 0,
                    "region_type": "REGULAR"
                },
                {
                    "length": 131072,
                    "offset": 65536,
                    "region_type": "ZEROED"
                }
            ]
        }
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while computing changed regions for volume group disk recovery point"
error:
    description:
        - This field typically holds information about if the task have errors that
          occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: null
task_ext_id:
    description:
        - The external ID of the task.
        - Compute-changed-regions is a synchronous action and does not produce a
          task, so this field is always C(null) on success.
    returned: always
    type: str
    sample: null
ext_id:
    description: The external ID of the disk recovery point on which the action was invoked.
    returned: always
    type: str
    sample: "21d467f0-ccef-4733-91cc-f04db58a92eb"
failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Path parameters must not appear in the request body spec.
_PATH_ONLY_PARAMS = {
    "state",
    "recovery_point_ext_id",
    "volume_group_recovery_point_ext_id",
    "ext_id",
}


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        recovery_point_ext_id=dict(type="str", required=True),
        volume_group_recovery_point_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        offset=dict(type="int"),
        length=dict(type="int"),
        block_size_byte=dict(type="int"),
        reference_volume_group_recovery_point_ext_id=dict(type="str"),
        reference_recovery_point_ext_id=dict(type="str"),
        reference_disk_recovery_point_ext_id=dict(type="str"),
    )
    return module_args


def _build_spec(module, result):
    """
    Build the VolumeGroupRecoveryPointChangedRegionsComputeSpec body from module
    params (everything except the path parameters).
    """
    sg = SpecGenerator(module)
    default_spec = (
        data_protection_sdk.VolumeGroupRecoveryPointChangedRegionsComputeSpec()
    )

    body_args = {
        key: value
        for key, value in module.params.items()
        if key not in _PATH_ONLY_PARAMS
    }
    spec, err = sg.generate_spec(obj=default_spec, attr=body_args)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for volume group recovery point compute-changed-regions",
            **result,
        )
    return spec


def compute_changed_regions_for_volume_group_disk_recovery_point(
    module, result, api_instance
):
    recovery_point_ext_id = module.params.get("recovery_point_ext_id")
    volume_group_recovery_point_ext_id = module.params.get(
        "volume_group_recovery_point_ext_id"
    )
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.volume_group_recovery_point_compute_changed_regions(
            recoveryPointExtId=recovery_point_ext_id,
            volumeGroupRecoveryPointExtId=volume_group_recovery_point_ext_id,
            extId=ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while computing changed regions for volume "
                "group disk recovery point"
            ),
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_together=[
            (
                "reference_recovery_point_ext_id",
                "reference_volume_group_recovery_point_ext_id",
                "reference_disk_recovery_point_ext_id",
            )
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_dataprotection_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_recovery_point_api_instance(module)
    compute_changed_regions_for_volume_group_disk_recovery_point(
        module, result, api_instance
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
