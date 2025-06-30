# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from copy import deepcopy

SDK_IMP_ERROR = None

try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ...sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

class UserSpecs:
    """Module specs related to IAM"""
    kvp_spec = dict(
        name=dict(type="str"),
        value=dict(type="str"),
    )

    users_spec = dict(
        ext_id=dict(type="str"),
        username=dict(type="str"),
        user_type=dict(
            type="str", choices=["LOCAL", "SAML", "LDAP", "EXTERNAL", "SERVICE_ACCOUNT"]
        ),
        display_name=dict(type="str"),
        first_name=dict(type="str"),
        middle_initial=dict(type="str"),
        last_name=dict(type="str"),
        email_id=dict(type="str"),
        locale=dict(type="str"),
        region=dict(type="str"),
        password=dict(type="str", no_log=True),
        idp_id=dict(type="str"),
        is_force_reset_password_enabled=dict(type="bool", default=False),
        additional_attributes=dict(
            type="list", elements="dict", options=kvp_spec, obj=iam_sdk.KVPair
        ),
        status=dict(type="str", choices=["ACTIVE", "INACTIVE"]),
        description=dict(type="str"),
        creation_type=dict(
            type="str", choices=["PREDEFINED", "SERVICEDEFINED", "USERDEFINED"]
        ),
    )

    @classmethod
    def get_users_spec(cls):
        return deepcopy(cls.users_spec)
