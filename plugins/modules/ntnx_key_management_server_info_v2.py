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
    - If Key Management Server external ID is provided, fetches that particular key management server
    - If external ID is not provided, list all key management servers
    - Key management server is used to secure encryption keys when data encryption is enabled.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID of the Key Management Server
        type: str
        required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
author:
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List allkey management servers
  nutanix.ncp.ntnx_key_management_server_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch a particular key management server using ext_id
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
        - Returns specific key management server info if ext_id is provided
        - Returns list of all key management servers if ext_id is not provided
    type: dict
    returned: always
    sample:
      {
        "access_information": {
            "client_id": "ab414ed6-7d97-4f7a-b98f-fcba7cac3b8c",
            "client_secret": null,
            "credential_expiry_date": "2027-09-01",
            "endpoint_url": "https://test-kms-server-1.vault.azure.net/",
            "key_id": "test-kms-server-1-key:707213e0523744d9ad27bc7d58efde0e",
            "tenant_id": "bb047546-786f-4de1-bd75-24e5b6f79043",
            "truncated_client_secret": "0PJ"
        },
        "ext_id": "99540f69-5e1d-49f3-8260-ceb7e34fe4ae",
        "links": null,
        "name": "ansible_test_RcwzBKOAEUuy_updated",
        "tenant_id": null
      }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

total_available_results:
    description:
        - The total number of available key management servers.
    type: int
    returned: when all key management servers are fetched
    sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.security.api_client import get_kms_api_instance  # noqa: E402
from ..module_utils.v4.security.helpers import get_kms_by_ext_id  # noqa: E402
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


def get_kms_using_ext_id(module, kms_api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_kms_by_ext_id(module, kms_api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_all_kms(module, kms_api_instance, result):
    resp = None
    try:
        resp = kms_api_instance.list_key_management_servers()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Key Management Server list",
        )
    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    kms_api_instance = get_kms_api_instance(module)
    if module.params.get("ext_id"):
        get_kms_using_ext_id(module, kms_api_instance, result)
    else:
        get_all_kms(module, kms_api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
