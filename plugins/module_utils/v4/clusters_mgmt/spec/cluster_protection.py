# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:
    from ....v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


class ClusterProtectionSpecs:
    """Module specs related to cluster protection and recovery operations."""

    protection_spec = dict(
        protection_rpo_minutes=dict(type="int"),
        local_snapshot_retention_policy=dict(type="int"),
        protection_target=dict(
            type="str",
            choices=["LOCAL", "LTSS"],
            obj=clusters_sdk.ProtectionTarget,
        ),
    )

    recovery_spec = dict(
        destination_cluster_ext_id=dict(type="str"),
    )

    @classmethod
    def get_protection_spec(cls):
        return deepcopy(cls.protection_spec)

    @classmethod
    def get_recovery_spec(cls):
        return deepcopy(cls.recovery_spec)
