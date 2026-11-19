#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_validate_certificate_v2
short_description: Authenticate a CAC user using certificate validation
version_added: 2.7.0
description:
  - Authenticate a CAC user by validating the certificate.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Authenticate a CAC user) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will validate the certificate.
      - If C(state) is C(absent), the module will fail.
    type: str
    choices:
      - present
    default: present
  relay_state:
    description:
      - The session ID value tracking the current login session.
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
- name: Validate certificate for CAC user
  nutanix.ncp.ntnx_validate_certificate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    relay_state: "test-relay-state-123"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for validate certificate
    - If C(wait) is true, it will contain the final task payload after completion.
    - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
      "data": "auth_code_uri_example",
      "metadata": {
        "flags": [],
        "links": [],
        "messages": [],
        "total_available_results": 1
      }
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while validating certificate"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task
  returned: when applicable
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the resource
  returned: when applicable
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_login_requests_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as identity_and_access_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as identity_and_access_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        relay_state=dict(type="str", required=True),
    )
    return module_args


def run_action(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = identity_and_access_management_sdk.CertificateLoginRequest()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for validate certificate", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    relay_state = module.params.get("relay_state")
    resp = None
    try:
        resp = api_instance.validate_certificate(relayState=relay_state)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while validating certificate",
        )
    if resp:
        # resp may be string or object; handle both
        if hasattr(resp, "to_dict"):
            result["response"] = strip_internal_attributes(resp.to_dict())
        elif hasattr(resp, "data"):
            data = resp.data
            if hasattr(data, "to_dict"):
                result["response"] = strip_internal_attributes(data.to_dict())
            else:
                result["response"] = {"data": str(data)}
        else:
            result["response"] = {"data": str(resp)}
        # try to capture task or ext_id if present
        if hasattr(resp, "data") and hasattr(resp.data, "ext_id"):
            result["task_ext_id"] = resp.data.ext_id
    result["changed"] = True


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
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_login_requests_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
