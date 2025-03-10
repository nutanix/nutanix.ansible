#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""
import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_user  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_users_empty_attributes,
)

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        user_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        name=dict(type="str", required=True),
        description=dict(type="str"),
        key_type=dict(type="str", choices=["API_KEY", "OBJECT_KEY"], required=True),
        creation_type=dict(
            type="str",
            choices=["PREDEFINED", "SERVICEDEFINED", "USERDEFINED"],
            required=True,
        ),
        expiry_time=dict(type="str"),
        status=dict(type="str", choices=["REVOKED", "VALID", "EXPIRED"]),
        assigned_to=dict(type="str"),
    )

    return module_args


def create_user_api_key(module, users_api, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.Key()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create users api key", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    user_ext_id = module.params.get("user_ext_id")
    resp = None
    try:
        resp = users_api.create_user_key(userExtId=user_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating user api key",
        )

    result["user_ext_id"] = user_ext_id
    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_user_api_key(module, users_api, result):
    user_ext_id = module.params.get("user_ext_id")
    ext_id = module.params.get("ext_id")

    try:
        users_api.delete_user_key(userExtId=user_ext_id, extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting user api key",
        )

    result["user_ext_id"] = user_ext_id
    result["ext_id"] = ext_id
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "absent",
                ("ext_id",),
            ),
        ],
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
    state = module.params["state"]
    users = get_user_api_instance(module)
    if state == "present":
        create_user_api_key(module, users, result)
    else:
        delete_user_api_key(module, users, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
