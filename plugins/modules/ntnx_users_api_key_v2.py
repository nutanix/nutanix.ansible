#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_users_api_key_v2
short_description: Module to create/delete key of a requested type for a user in Nutanix Prism Central.
version_added: 2.2.0
description:
    - This module can be used to create or delete a key of a requested type for a user in Nutanix Prism Central.
    - If state is present, this module will create a key for the user.
    - If state is absent, this module will delete the key for the user.
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
    name:
        description:
            - Identifier for the key in the form of a name.
        type: str
    description:
        description:
            - Brief description of the key.
        type: str
    key_type:
        description:
            - The type of the key.
        type: str
        choices:
            - API_KEY
            - OBJECT_KEY
    creation_type:
        description:
            - The creation mechanism for the key.
        type: str
        choices:
            - PREDEFINED
            - SERVICEDEFINED
            - USERDEFINED
    expiry_time:
        description:
            - The time when the key will expire.
        type: str
    status:
        description:
            - The status of the key.
        type: str
        choices:
            - REVOKED
            - VALID
            - EXPIRED
    assigned_to:
        description:
            - External client to whom the given key is allocated.
        type: str
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""
import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_user_api_instance,
    get_etag,
)
from ..module_utils.v4.iam.helpers import get_requested_key  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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
        name=dict(type="str"),
        description=dict(type="str"),
        key_type=dict(type="str", choices=["API_KEY", "OBJECT_KEY"]),
        creation_type=dict(
            type="str",
            choices=["PREDEFINED", "SERVICEDEFINED", "USERDEFINED"],
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

    old_spec = get_requested_key(module, users_api, ext_id, user_ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for Deletion", **result)

    kwargs = {"if_match": etag}
    try:
        users_api.delete_user_key_by_id(userExtId=user_ext_id, extId=ext_id, **kwargs)
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
            (
                "state",
                "present",
                ("name", "key_type"),
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
