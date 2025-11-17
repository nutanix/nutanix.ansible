#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_users_api_key_info_v2
short_description: Module to fetch user api keys in Nutanix Prism Central.
version_added: 2.2.0
description:
    - If ext_id is provided, this module will fetch the specific user api key.
    - If ext_id is not provided, this module will fetch multiple user api keys with/without filters, limit, etc.
    - This modules uses PC v4 APIs based SDKs.
options:
    user_ext_id:
        description:
            - The external identifier of the user.
        type: str
        required: true
    ext_id:
        description:
            - The external identifier of the user api key.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all API keys
  nutanix.ncp.ntnx_users_api_key_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_ext_id: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"
  register: result

- name: List all API keys with filter
  nutanix.ncp.ntnx_users_api_key_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_ext_id: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"
    filter: "name eq 'api_key_1'"
  register: result

- name: Get Details of Specific API key
  nutanix.ncp.ntnx_users_api_key_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_ext_id: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"
    ext_id: "9i8h7g6f-5e4d-3c2b-1a0j-k2l3m4n5o6p"
  register: result
"""

RETURN = r"""
changed:
    description:
        - Indicates whether the module made any changes.
    type: bool
    returned: always
    sample: false

error:
    description:
        - Error message if any error occurs.
    type: str
    returned: when an error occurs
    sample: null

failed:
    description:
        - Indicates whether the module failed.
    type: bool
    returned: always
    sample: false

user_ext_id:
    description:
        - The external identifier of the user.
    type: str
    returned: always
    sample: "f7e6d5c4-b3a2-4i9h-8g7f-6e5d4c3b2a1k"

ext_id:
    description:
        - The external identifier of the user api key.
    type: str
    returned: when ext_id is provided
    sample: "9i8h7g6f-5e4d-3c2b-1a0j-k2l3m4n5o6p"

response:
    description:
        - The list of API keys info if API key external ID is not passed.
        - The respone of API key info using API key external ID.
    type: dict
    returned: always
    sample: [
            {
                "assigned_to": null,
                "created_by": "00000000-0000-0000-0000-000000000000",
                "created_time": "2025-04-16T05:36:16.745709+00:00",
                "creation_type": "USERDEFINED",
                "description": "user_test_xoLHTszFziTH_description_api_key_1",
                "expiry_time": "2025-04-18T05:36:16.126000+00:00",
                "ext_id": "64008b39-fba5-5aa6-94ca-75c21ce7ced5",
                "key_details": null,
                "key_type": "API_KEY",
                "last_updated_by": "00000000-0000-0000-0000-000000000000",
                "last_updated_time": "2025-04-16T05:36:16.745709+00:00",
                "last_used_time": "2025-04-16T05:36:16.745709+00:00",
                "links": null,
                "name": "user_test_xoLHTszFziTH_api_key_1",
                "status": "VALID",
                "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df"
            }
        ]
total_available_results:
    description:
        - The total number of available user api keys in PC.
    type: int
    returned: when all user api keys are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_requested_key  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        user_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_user_key_by_ext_id(module, users, result):
    ext_id = module.params.get("ext_id")
    user_ext_id = module.params.get("user_ext_id")
    resp = get_requested_key(module, users, ext_id, user_ext_id)
    result["ext_id"] = ext_id
    result["user_ext_id"] = user_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_user_api_keys(module, users, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating user api keys info Spec", **result)

    user_ext_id = module.params.get("user_ext_id")
    result["user_ext_id"] = user_ext_id
    try:
        resp = users.list_user_keys(userExtId=user_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user api keys info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    users = get_user_api_instance(module)
    if module.params.get("ext_id"):
        get_user_key_by_ext_id(module, users, result)
    else:
        get_user_api_keys(module, users, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
