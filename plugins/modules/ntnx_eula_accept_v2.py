#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_eula_accept_v2
short_description: Allows users to accept End User License Agreement.
version_added: 2.4.0
description:
  - Allows users to accept End User License Agreement.
  - This module uses PC v4 APIs based SDKs
options:
    user_name:
        description:
            - User name of the user accepting the End User License Agreement.
        required: true
        type: str
    login_id:
        description:
            - Login ID of the user accepting the End User License Agreement.
        required: true
        type: str
    job_title:
        description:
            - Job title of the user accepting the End User License Agreement.
        required: true
        type: str
    company_name:
        description:
            - Company name of the user accepting the End User License Agreement.
        required: true
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Accept End of User License Agreement
  nutanix.ncp.ntnx_eula_accept_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_name: "user_name"
    login_id: "login_id"
    job_title: "job_title"
    company_name: "company_name"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - The response from the eula accept v4 API.
  returned: always
  type: dict
  sample:
    {
        "data": [
            {
                "arguments_map": null,
                "code": "200",
                "error_group": null,
                "locale": null,
                "message": "Eula accepted by user successfully",
                "severity": "$UNKNOWN"
            }
        ],
        "metadata": null
    }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.licensing.api_client import get_eula_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_licensing_py_client as licensing_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as licensing_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        user_name=dict(type="str", required=True),
        login_id=dict(type="str", required=True),
        job_title=dict(type="str", required=True),
        company_name=dict(type="str", required=True),
    )
    return module_args


def accept_eula(module, result):
    eula_api_instance = get_eula_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = licensing_sdk.EndUser()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating accept eula Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = eula_api_instance.add_user(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while accepting End User License Agreement",
        )

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_licensing_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    accept_eula(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
