#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_eula_info_v2
short_description: Fetches active End User License Agreement.
version_added: 2.4.0
description:
    - Fetches active End User License Agreement.
    - This module uses PC v4 APIs based SDKs
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get End of User License Agreement info
  nutanix.ncp.ntnx_eula_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - The response from the eula info v4 API.
  returned: always
  type: dict
  sample:
    {
        "acceptances": [
            {
                "acceptance_time": "1970-01-21T06:52:29+00:00",
                "accepted_by": {
                    "company_name": "Nutanix",
                    "job_title": "MTS",
                    "login_id": "admin",
                    "user_name": "Nutanix"
                }
            }
        ],
        "content": "content",
        "ext_id": "f4c1e524-f1df-45fd-aff3-9492c41da5e9",
        "is_enabled": true,
        "links": null,
        "tenant_id": null,
        "updated_time": "1970-01-21T06:52:27+00:00",
        "version": "4.5"
    }

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.licensing.api_client import get_eula_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_eula(module, result):
    eula_api_instance = get_eula_api_instance(module)

    try:
        resp = eula_api_instance.get_eula()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching end user license agreement info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=dict(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    get_eula(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
