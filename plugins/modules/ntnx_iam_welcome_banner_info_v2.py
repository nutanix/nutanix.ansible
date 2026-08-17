#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iam_welcome_banner_info_v2
short_description: Fetch the IAM Welcome Banner from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about WelcomeBanner in Nutanix Prism Central.
  - The welcome banner is a singleton resource in Prism Central; there is no
    external ID and no list operation, so this module always returns the single
    welcome banner configuration.
  - The C(ext_id) option is accepted for consistency with the other v4 info
    modules and is otherwise ignored.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get the Welcome Banner) - Required Roles: Super Admin, Prism Admin,
    Prism Viewer. The banner GET endpoint is also invoked unauthenticated by
    the Prism Central login page.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - Placeholder external ID for the welcome banner.
      - The welcome banner is a singleton resource in Prism Central and has no
        real external ID; this option is accepted for consistency with the
        other v4 info modules and is otherwise ignored.
    type: str
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch the welcome banner configuration
  nutanix.ncp.ntnx_iam_welcome_banner_info_v2:
  register: result

- name: Fetch the welcome banner configuration (ext_id ignored - singleton)
  nutanix.ncp.ntnx_iam_welcome_banner_info_v2:
    ext_id: "welcome-banner"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC WelcomeBanner info v4 API.
    - The welcome banner is a singleton resource, so this is always the single
      welcome banner configuration as a dict. There is no list variant.
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
  description: Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Message if any error occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching welcome banner"

error:
  description:
    - This field holds information about any error that occurred during task execution.
  returned: When an error occurs
  type: str

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - Placeholder external ID for the welcome banner.
    - The welcome banner has no real external ID; this field is populated with
      the C(ext_id) input value when supplied, otherwise C(null).
  returned: when C(ext_id) is provided
  type: str
  sample: null
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_welcome_banner_api_instance,
)
from ..module_utils.v4.iam.helpers import get_welcome_banner  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def fetch_welcome_banner(module, api_instance, result):
    resp = get_welcome_banner(module, api_instance)
    ext_id = module.params.get("ext_id")
    if ext_id:
        result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        # WelcomeBanner is a singleton — the standard info-module filter/limit/
        # orderby/select/page options inherited from BaseInfoModule are accepted
        # but the API ignores them; we do not pass them to the SDK.
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_welcome_banner_api_instance(module)
    fetch_welcome_banner(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
