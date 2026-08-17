# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as storage_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class VolumeDiskSpecs:
    """Reusable argument-spec fragments shared across Volume Disk modules."""

    flash_mode = dict(
        is_enabled=dict(type="bool", required=True),
    )

    disk_storage_features = dict(
        flash_mode=dict(
            type="dict",
            options=flash_mode,
            required=True,
            obj=storage_sdk.FlashMode,
        ),
    )

    disk_data_source_reference = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        entity_type=dict(
            type="str",
            choices=[
                "STORAGE_CONTAINER",
                "VOLUME_DISK",
                "VM_DISK",
                "DISK_RECOVERY_POINT",
            ],
        ),
    )

    @classmethod
    def get_disk_storage_features_spec(cls):
        return deepcopy(cls.disk_storage_features)

    @classmethod
    def get_disk_data_source_reference_spec(cls):
        return deepcopy(cls.disk_data_source_reference)
