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
    - This modules uses PC v4 APIs based SDKs.
options:
    user_ext_id:
        description:
            - The external identifier of the user.
        type: str
        required: true
    ext_id:
        description:
            - The external identifier of the key.
            - Required in case of deleting the key.
        type: str
    name:
        description:
            - Identifier for the key in the form of a name.
            - Required in case of creating new key.
        type: str
    description:
        description:
            - Brief description of the key.
        type: str
    key_type:
        description:
            - The type of the key.
            - Required in case of creating new key.
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
    assigned_to:
        description:
            - External client to whom the given key is allocated.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create an API key
  nutanix.ncp.ntnx_users_api_key_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_ext_id: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"
    name: "api_key_1"
    description: "description_api_key_1"
    key_type: "API_KEY"
    expiry_time: "2025-12-31T23:59:59Z"
  register: result

- name: Delete an API key
  nutanix.ncp.ntnx_users_api_key_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_ext_id: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"
    ext_id: "9i8h7g6f-5e4d-3c2b-1a0j-k2l3m4n5o6p"
    state: absent
  register: result
"""

RETURN = r"""
    user_ext_id:
        description:
            - The external identifier of the user (service account).
        type: str
        returned: always
        sample: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"
    ext_id:
        description:
            - The external identifier of the key.
        type: str
        returned: always
        sample: "9i8h7g6f-5e4d-3c2b-1a0j-k2l3m4n5o6p"
    changed:
        description:
            - Indicates whether the module made any changes.
        type: bool
        returned: always
        sample: true
    error:
        description:
            - Error message if any occurred during the operation.
        type: str
        returned: when error occurs
        sample: "Api Exception raised while creating user api key"
    response:
        description:
            - The response from the API call of creating/deleting an user API key.
        type: dict
        returned: always
        sample: {
                "assigned_to": null,
                "created_by": "00000000-0000-0000-0000-000000000000",
                "created_time": "2025-04-16T05:36:16.745708+00:00",
                "creation_type": "USERDEFINED",
                "description": "user_test_xoLHTszFziTH_description_api_key_1",
                "expiry_time": "2025-04-18T05:36:16.126000+00:00",
                "ext_id": "64008b39-fba5-5aa6-94ca-75c21ce7ced5",
                "key_details": {
                    "api_key": "2c8059752b8645b08dc64b9bca98df43"
                },
                "key_type": "API_KEY",
                "last_updated_by": "00000000-0000-0000-0000-000000000000",
                "last_updated_time": "2025-04-16T05:36:16.745708+00:00",
                "last_used_time": "2025-04-16T05:36:16.745708+00:00",
                "links": null,
                "name": "user_test_xoLHTszFziTH_api_key_1",
                "status": "VALID",
                "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df"
            }
"""
import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_user_api_instance,
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
        return module.fail_json("Unable to fetch etag for deleting user API key", **result)

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
