#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_recovery_point_compute_changed_region_v2
short_description: Compute changed regions between two Volume Group disk recovery points
version_added: 2.7.0
description:
    - This module displays the calculated metadata with the changed region details between any two volume group disk recovery points of a file.
    - This API can be used for incremental and differential backups, as well as for a full backup, because it indicates the regions that are zeros,
      helping to avoid copying zero regions.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Compute Changed Regions Volume Group Recovery Point) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Kubernetes Data Services System,
      Prism Admin, Prism Viewer, Project Admin, Project Manager, Self-Service Admin (Deprecated), Super Admin,
      Tenant Admin, Tenant Consumer
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
            - The external identifier that can be used to retrieve the recovery point using its URL.
        type: str
        required: true
    volume_group_recovery_point_ext_id:
        description:
            - External identifier of the volume group recovery point.
        type: str
        required: true
    ext_id:
        description:
            - Disk recovery point identifier.
        type: str
        required: true
    offset:
        description:
            - The start offset value to compute the changed region.
            - If the value is not provided, then the difference is executed from the offset of 0.
            - The start offset might automatically align to a system-defined block boundary.
        type: int
        required: false
    length:
        description:
            - The length to compute the changed region.
            - If the value is not provided, then the difference is performed from the start offset to the end of the disk.
            - The end offset might automatically align to a system-defined block boundary.
        type: int
        required: false
    block_size_byte:
        description:
            - When blockSizeByte is set, all returned ranges start and end at blockSize addresses, and the changed blocks match the block size.
            - Supported values of blockSizeByte are [32768, 65536, 131072, 262144].
            - For example, if blockSizeByte is set to 32768 (i.e 32KB), all ranges start at multiple of 32KB and end at multiple of 32KB value.
        type: int
        required: false
    reference_recovery_point_ext_id:
        description:
            - The external identifier that can be used to retrieve the recovery point using its URL.
        type: str
        required: false
    reference_volume_group_recovery_point_ext_id:
        description:
            - The external identifier that can be used to retrieve the volume group recovery point using its URL
            - This attribute will be removed in future releases; therefore, use the volume group recovery point external identifier instead.
        type: str
        required: false
    reference_disk_recovery_point_ext_id:
        description:
            - Disk recovery point external identifier.
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
- name: Compute changed regions for a volume group disk recovery point
  nutanix.ncp.ntnx_volume_group_recovery_point_compute_changed_region_v2:
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    volume_group_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    ext_id: "21d467f0-ccef-4733-91cc-f04db58a92eb"
    offset: 0
    length: 1048576
    block_size_byte: 65536
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


def compute_changed_regions_for_volume_group_disk_recovery_point(
    module, result, api_instance
):
    recovery_point_ext_id = module.params.get("recovery_point_ext_id")
    volume_group_recovery_point_ext_id = module.params.get(
        "volume_group_recovery_point_ext_id"
    )
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = (
        data_protection_sdk.VolumeGroupRecoveryPointChangedRegionsComputeSpec()
    )
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for computing changed regions of volume group disk recovery point",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Volume group recovery point compute changed regions spec generated in "
            "check mode; no API call was made."
        )
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

    result["response"] = _normalize_response_data(getattr(resp, "data", None))
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
        "failed": False,
        "response": None,
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
