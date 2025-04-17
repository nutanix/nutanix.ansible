# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class VGSpecs:
    """Module specs related to Volume Groups"""

    flash_mode = dict(
        is_enabled=dict(type="bool", required=True),
    )
    storage_features = dict(
        flash_mode=dict(
            type="dict", options=flash_mode, required=True, obj=volumes_sdk.FlashMode
        )
    )
    iscsi_features = dict(
        target_secret=dict(type="str", required=True, no_log=True),
        enabled_authentications=dict(
            type="str", choices=["CHAP", "NONE"], required=False
        ),
    )
    volume_group = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        should_load_balance_vm_attachments=dict(type="bool", required=False),
        sharing_status=dict(
            type="str", choices=["SHARED", "NOT_SHARED"], required=False
        ),
        target_prefix=dict(type="str", required=False),
        target_name=dict(type="str", required=False),
        enabled_authentications=dict(
            type="str", choices=["CHAP", "NONE"], required=False
        ),
        cluster_reference=dict(type="str", required=False),
        usage_type=dict(
            type="str", choices=["BACKUP_TARGET", "INTERNAL", "TEMPORARY", "USER"]
        ),
        is_hidden=dict(type="bool", required=False),
        storage_features=dict(
            type="dict",
            required=False,
            options=storage_features,
            obj=volumes_sdk.StorageFeatures,
        ),
        iscsi_features=dict(
            type="dict",
            required=False,
            options=iscsi_features,
            obj=volumes_sdk.IscsiFeatures,
        ),
    )

    @classmethod
    def get_volume_group_spec(cls):
        return deepcopy(cls.volume_group)

    @classmethod
    def get_storage_features_spec(cls):
        return deepcopy(cls.storage_features)
