#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_users_info_v2
short_description: Get users info
version_added: 2.0.0
description:
    - Get users info using user external ID or list multiple users
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID of the user
            - It can be used to get specific user info
        required: false
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List all users
  nutanix.ncp.ntnx_users_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: users

- name: List users using user ext_id criteria
  nutanix.ncp.ntnx_users_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "04e7b47e-a861-5b57-a494-10ca57e6ec4a"
  register: result

- name: List users using filter
  nutanix.ncp.ntnx_users_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "username eq 'test_user'"
"""
RETURN = r"""
response:
    description:
        - Response for fetching users info
        - Returns users info using users external ID or list multiple users
    type: dict
    returned: always
    sample:
        {
            "additional_attributes": null,
            "buckets_access_keys": null,
            "created_by": "00000000-0000-0000-0000-000000000000",
            "created_time": "2024-05-28T09:03:05.778320+00:00",
            "display_name": "admin",
            "email_id": "",
            "ext_id": "00000000-0000-0000-0000-000000000000",
            "first_name": "admin",
            "idp_id": "37f30135-455b-5ebd-995f-b47e817a59f2",
            "is_force_reset_password_enabled": false,
            "last_login_time": "2024-06-25T07:33:22.803659+00:00",
            "last_name": "",
            "last_updated_by": "00000000-0000-0000-0000-000000000000",
            "last_updated_time": "2024-05-28T09:28:51.567099+00:00",
            "links": null,
            "locale": "en-US",
            "middle_initial": "",
            "password": null,
            "region": "en-US",
            "status": "ACTIVE",
            "tenant_id": null,
            "user_type": "LOCAL",
            "username": "admin"
            }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the user
    returned: always
    type: str
    sample: 04e7b47e-a861-5b57-a494-10ca57e6ec4a

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_user  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_user_by_ext_id(module, users, result):
    ext_id = module.params.get("ext_id")
    resp = get_user(module, users, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_users(module, users, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating users info Spec", **result)

    try:
        resp = users.list_users(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching users info",
        )

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
    result = {"changed": False, "response": None}
    users = get_user_api_instance(module)
    if module.params.get("ext_id"):
        get_user_by_ext_id(module, users, result)
    else:
        get_users(module, users, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
