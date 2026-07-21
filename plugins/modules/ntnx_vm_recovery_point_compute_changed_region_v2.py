#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_point_compute_changed_region_v2
short_description: Compute VM recovery point changed regions in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to compute the changed regions between two VM
      disk recovery points (Changed Block Tracking).
    - It returns the list of changed regions of a disk recovery point that
      belongs to a VM recovery point which itself belongs to a top-level
      recovery point.
    - Backup software can use this metadata to efficiently transfer only
      the modified (or non-zero) regions between two disk recovery points.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Compute VM recovery point changed regions) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin,
      Kubernetes Data Services System, Prism Admin, Project Manager,
      Super Admin, Self-Service Admin (deprecated).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will compute changed regions.
            - Any other value will fail as this module only supports action.
        type: str
        choices:
            - present
        default: present
    recovery_point_ext_id:
        description:
            - The external identifier of the top-level recovery point that
              owns the VM recovery point.
        type: str
        required: true
    vm_recovery_point_ext_id:
        description:
            - The external identifier of the VM recovery point that owns the
              disk recovery point.
        type: str
        required: true
    disk_recovery_point_ext_id:
        description:
            - The external identifier of the disk recovery point for which
              the changed regions must be computed.
        type: str
        required: true
    offset:
        description:
            - The start offset value (in bytes) from which the changed
              region computation should begin.
            - If not provided, computation starts from offset 0.
            - The start offset may be automatically aligned to a
              system-defined block boundary.
        type: int
        required: false
    length:
        description:
            - The length (in bytes) starting from I(offset) that should be
              considered for changed region computation.
        type: int
        required: false
    block_size_byte:
        description:
            - The block size (in bytes) to be used for the changed region
              computation granularity.
            - The SDK constrains this value to be less than or equal to
              C(262144) (256 KiB); passing a value larger than this will
              result in an SDK-side validation error before the request is
              sent.
        type: int
        required: false
    reference_recovery_point_ext_id:
        description:
            - The external identifier of the reference top-level recovery
              point to compare against.
            - Required only when specifying a reference disk recovery point.
              All three of I(reference_recovery_point_ext_id),
              I(reference_vm_recovery_point_ext_id) and
              I(reference_disk_recovery_point_ext_id) must be provided
              together.
        type: str
        required: false
    reference_vm_recovery_point_ext_id:
        description:
            - The external identifier of the reference VM recovery point to
              compare against.
            - Required only when specifying a reference disk recovery point.
        type: str
        required: false
    reference_disk_recovery_point_ext_id:
        description:
            - The external identifier of the reference disk recovery point
              to compare against.
            - Required only when specifying a reference disk recovery point.
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
- name: Compute changed regions for a VM disk recovery point (full disk)
  nutanix.ncp.ntnx_vm_recovery_point_compute_changed_region_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    disk_recovery_point_ext_id: "21d467f0-ccef-4733-91cc-f04db58a92eb"
  register: full_regions

- name: Compute incremental changed regions between two disk recovery points
  nutanix.ncp.ntnx_vm_recovery_point_compute_changed_region_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    disk_recovery_point_ext_id: "21d467f0-ccef-4733-91cc-f04db58a92eb"
    offset: 0
    length: 1048576
    block_size_byte: 262144
    reference_recovery_point_ext_id: "0bc9d9a7-eaf1-46f4-9f3c-2b52a5f57b6d"
    reference_vm_recovery_point_ext_id: "9bd35b60-1c26-4c0c-a2ba-8a2b7cb7fbcd"
    reference_disk_recovery_point_ext_id: "3f18f321-59e5-4a09-b74a-4b6d1adf5d47"
  register: incremental_regions
"""

RETURN = r"""
response:
    description:
        - The response for computing changed regions of a VM disk recovery
          point.
        - When the API returns a list of changed regions, this will be a
          dict with a C(changed_regions) key containing the list of regions.
        - Each changed region contains C(offset), C(length) and
          C(region_type) (C(ZEROED) or C(REGULAR)).
    returned: always
    type: dict
    sample:
        {
            "changed_regions": [
                {
                    "length": 1048576,
                    "offset": 0,
                    "region_type": "REGULAR"
                },
                {
                    "length": 2097152,
                    "offset": 1048576,
                    "region_type": "ZEROED"
                }
            ]
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the disk recovery point.
    returned: always
    type: str
    sample: "21d467f0-ccef-4733-91cc-f04db58a92eb"

task_ext_id:
    description:
        - The external ID of the task.
        - This action is synchronous and does not create a task, so this
          value is typically null.
    returned: always
    type: str
    sample: null

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error, or the operation is executed in check mode.
    type: str
    sample: "Api Exception raised while computing changed regions for VM disk recovery point"

error:
    description: This field typically holds information about if any error occurred during the task execution.
    returned: When an error occurs.
    type: str
    sample: null

failed:
    description: This field indicates whether the task failed.
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


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        recovery_point_ext_id=dict(type="str", required=True),
        vm_recovery_point_ext_id=dict(type="str", required=True),
        disk_recovery_point_ext_id=dict(type="str", required=True),
        offset=dict(type="int", required=False),
        length=dict(type="int", required=False),
        block_size_byte=dict(type="int", required=False),
        reference_recovery_point_ext_id=dict(type="str", required=False),
        reference_vm_recovery_point_ext_id=dict(type="str", required=False),
        reference_disk_recovery_point_ext_id=dict(type="str", required=False),
    )
    return module_args


def _normalize_response_data(data):
    """Convert a heterogeneous SDK response body into a JSON-serialisable dict.

    The compute-changed-regions API can return either a list of ChangedRegion
    objects (success) or an empty payload. Ansible modules generally return
    a mapping under ``response``; wrap the list in ``changed_regions`` so
    callers can iterate deterministically.
    """
    if data is None:
        return {"changed_regions": []}

    if isinstance(data, list):
        regions = []
        for item in data:
            if hasattr(item, "to_dict"):
                regions.append(strip_internal_attributes(item.to_dict()))
            elif isinstance(item, dict):
                regions.append(strip_internal_attributes(item))
            else:
                regions.append(item)
        return {"changed_regions": regions}

    if hasattr(data, "to_dict"):
        return strip_internal_attributes(data.to_dict())

    if isinstance(data, dict):
        return strip_internal_attributes(data)

    return {"changed_regions": [data]}


def compute_vm_recovery_point_changed_regions(module, result, api_instance):
    """Compute changed regions of a VM disk recovery point.

    Sends the compute-changed-regions POST request for the given VM disk
    recovery point identifiers and returns the list of ``ChangedRegion``
    entries in ``result['response']``. All body parameters are optional per
    the SDK; if a reference disk recovery point is desired, all three
    reference IDs must be provided together.
    """
    recovery_point_ext_id = module.params.get("recovery_point_ext_id")
    vm_recovery_point_ext_id = module.params.get("vm_recovery_point_ext_id")
    disk_recovery_point_ext_id = module.params.get("disk_recovery_point_ext_id")
    result["ext_id"] = disk_recovery_point_ext_id

    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.VmRecoveryPointChangedRegionsComputeSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for computing changed regions of VM disk recovery point",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "VM recovery point compute changed regions spec generated in check mode; "
            "no API call was made."
        )
        return

    try:
        resp = api_instance.vm_recovery_point_compute_changed_regions(
            recoveryPointExtId=recovery_point_ext_id,
            vmRecoveryPointExtId=vm_recovery_point_ext_id,
            extId=disk_recovery_point_ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while computing changed regions for VM disk recovery point",
        )

    result["response"] = _normalize_response_data(getattr(resp, "data", None))
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_together=[
            (
                "reference_recovery_point_ext_id",
                "reference_vm_recovery_point_ext_id",
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_recovery_point_api_instance(module)
    compute_vm_recovery_point_changed_regions(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
