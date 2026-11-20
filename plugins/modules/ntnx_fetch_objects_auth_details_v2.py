#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_fetch_objects_auth_details_v2
short_description: Fetch objects auth details for an access key in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch secret key and user details for a given access key ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Fetch objects auth details) -
      Required Roles: Nutanix Central Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will fetch objects auth details.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    access_key:
        description:
            - The access key which is used to retrieve the auth details.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch objects auth details for an access key
  nutanix.ncp.ntnx_fetch_objects_auth_details_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    access_key: "AKIAIOSFODNN7EXAMPLE"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for fetching objects auth details.
        - Contains secret key and user details for the access key.
    returned: always
    type: dict
    sample:
        {
            "assigned_to": "client1",
            "creation_type": "USERDEFINED",
            "custom_claims": {},
            "email_id": "user@example.com",
            "idp_id": "37f30135-455b-5ebd-995f-b47e817a59f2",
            "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
            "user_id": "00000000-0000-0000-0000-000000000001",
            "user_type": "LOCAL",
            "username": "user@example.com"
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

ext_id:
    description: The external ID of the resource
    returned: always
    type: str
    sample: null

task_ext_id:
    description: The task external ID
    returned: always
    type: str
    sample: null

msg:
    description: This indicates the message if any message occurred
    returned: when there is an error
    type: str
    sample: "Api Exception raised while fetching objects auth details"

error:
    description: This indicates the error message if any error occurred
    returned: when an error occurs
    type: str
    sample: null

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        access_key=dict(type="str", required=True, no_log=True),
    )
    return module_args


def run_action(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.ObjectsAuthSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating fetch objects auth details spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.fetch_objects_auth_details(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching objects auth details",
        )

    if resp is None or getattr(resp, "data", None) is None:
        result["response"] = {}
        result["changed"] = False
        return

    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = False


def run_module():
    module = BaseModuleV4(
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
        "failed": False,
        "response": None,
    }

    api_instance = get_user_api_instance(module)
    run_action(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
