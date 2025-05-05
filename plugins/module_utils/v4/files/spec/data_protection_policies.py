# Copyright: 2021, Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause )
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

try:
    import ntnx_files_pc_py_client as files_sdk
except ImportError:
    from ...sdk_mock import mock_sdk as files_sdk


class ProtectionPolicySpec:
    """Files Data Protection Policy Spec"""

    schedule_types = [
        "SCHEDULETYPE_HOURLY",
        "SCHEDULETYPE_MINUTELY",
        "SCHEDULETYPE_SECONDLY",
    ]
    protected_entity = dict(
        source_mount_target_ext_id=dict(type="str", required=True),
        source_mount_target_path=dict(type="str", required=False),
        target_mount_target_ext_id=dict(type="str", required=False),
    )
    schedule = dict(
        schedule_type=dict(type="str", choices=schedule_types, required=True),
        multiple=dict(type="int", required=True),
        start_time_iso8601=dict(type="str", required=False),
    )
    sub_policy = dict(
        ext_id=dict(type="str", required=False),
        source_file_server_ext_id=dict(type="str", required=True),
        target_file_server_ext_id=dict(type="str", required=True),
        target_pc_ext_id=dict(type="str", required=False),
        protected_entities=dict(
            type="list",
            elements="dict",
            options=protected_entity,
            obj=files_sdk.ProtectedEntity,
            required=False,
        ),
        schedules=dict(
            type="list",
            elements="dict",
            options=schedule,
            obj=files_sdk.Schedule,
            required=True,
        ),
        include_new_mount_targets=dict(type="bool", required=False, default=False),
        is_reverse_policy=dict(type="bool", required=False),
    )
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        sub_policies=dict(
            type="list",
            elements="dict",
            options=sub_policy,
            obj=files_sdk.SubPolicy,
            required=False,
        ),
        type=dict(
            type="str",
            choices=["DATAPROTECTIONPOLICYTYPE_DR"],
            default="DATAPROTECTIONPOLICYTYPE_DR",
            required=False,
        ),
        is_reverse_policy=dict(type="bool", required=False),
        tenant_id=dict(type="str", required=False),
    )

    @classmethod
    def get_module_spec(cls):
        return deepcopy(cls.module_args)
