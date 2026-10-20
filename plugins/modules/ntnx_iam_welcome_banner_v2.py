#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iam_welcome_banner_v2
short_description: Update the IAM Welcome Banner in Nutanix Prism Central
version_added: 2.7.0
description:
  - Update the IAM Welcome Banner configuration in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Update the Welcome Banner) - Required Roles: Super Admin, Prism Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  state:
    description:
      - state is not supported for this module.
      - It will always be present.
    type: str
    choices: ['present']
    default: present
  content:
    description:
      - Content of the welcome banner.
    type: str
    required: false
  is_enabled:
    description:
      - Flag to denote whether the welcome banner is enabled or not.
    type: bool
    required: false
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
- name: Update the welcome banner
  nutanix.ncp.ntnx_iam_welcome_banner_v2:
    content: "Authorized personnel only. All activity is monitored and recorded."
    is_enabled: true
  register: result

- name: Disable the welcome banner
  nutanix.ncp.ntnx_iam_welcome_banner_v2:
    is_enabled: false
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for updating the welcome banner.
    - Returns the full welcome banner details.
  returned: always
  type: dict
  sample:
    {
      "content": "Authorized personnel only. All activity is monitored and recorded.",
      "created_time": "2026-06-29T07:18:36.280134+00:00",
      "is_enabled": true,
      "last_updated_time": "2026-07-21T06:36:56.065999+00:00",
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or in check mode operation
  type: str
  sample: "Api Exception raised while updating the welcome banner"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_welcome_banner_api_instance,
)
from ..module_utils.v4.iam.helpers import get_welcome_banner  # noqa: E402
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        content=dict(type="str"),
        is_enabled=dict(type="bool"),
    )
    return module_args


def update_welcome_banner(module, result, api_instance):
    current = get_welcome_banner(module, api_instance)
    etag = get_etag(data=current)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating the welcome banner", **result
        )

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    default_spec = identity_and_access_management_sdk.WelcomeBanner()
    update_spec, err = sg.generate_spec(obj=deepcopy(default_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating welcome banner update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.update_welcome_banner(body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating the welcome banner",
        )

    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }

    api_instance = get_welcome_banner_api_instance(module)
    update_welcome_banner(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
