#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_key_management_server_info_v2
short_description: Get key management server info
version_added: 2.4.0
description:
    - Get key management server info using key management server external ID or list all key management servers
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - This module is used to get key management server info
            - It can be used to get key management server info using key management server external ID or list all key management servers
        type: str
        required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List key management servers
  nutanix.ncp.ntnx_key_management_server_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch key management server using uuid criteria
  nutanix.ncp.ntnx_key_management_server_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
  register: result

"""

RETURN = r"""
response:
    description:
        - Response for fetching key management server info.
        - Returns key management server info using key management server external ID or list all key management servers.
    type: dict
    returned: always
    sample:

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
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import get_kms_api_instance  # noqa: E402
from ..module_utils.v4.security.helpers import get_kms_by_ext_id, list_kms  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_kms(module, kms_api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_kms_by_ext_id(module, kms_api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_all_kms(module, kms_api_instance, result):
    resp = list_kms(module, kms_api_instance)
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    kms_api_instance = get_kms_api_instance(module)
    if module.params.get("ext_id"):
        get_kms(module, kms_api_instance, result)
    else:
        get_all_kms(module, kms_api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
