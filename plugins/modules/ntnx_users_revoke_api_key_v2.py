#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_users_revoke_api_key_v2
short_description: Module to revoke the requested API key for a user in Nutanix Prism Central.
version_added: 2.2.0
description:
    - This module can be used to revoke the requested API key for a user in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
options:
    user_ext_id:
        description:
            - The external identifier of the user.
        type: str
        required: true
    ext_id:
        description:
            - The external identifier of the key.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""
import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_api_instance  # noqa: E402
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        user_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def revoke_user_api_key(module, users_api, result):
    user_ext_id = module.params.get("user_ext_id")
    ext_id = module.params.get("ext_id")

    try:
        users_api.revoke_user_key(userExtId=user_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while revoking user api key",
        )

    result["user_ext_id"] = user_ext_id
    result["ext_id"] = ext_id
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    users = get_user_api_instance(module)
    revoke_user_api_key(module, users, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
