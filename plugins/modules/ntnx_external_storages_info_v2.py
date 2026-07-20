#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_external_storages_info_v2
short_description: Fetch external storage info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ExternalStorage in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ExternalStorage.
  - The Prism v4 API for ExternalStorage exposes only the get-by-id operation
    (the full CRUD API for ExternalStorage lives under the
    C(clustermgmt) namespace); providing C(ext_id) is therefore mandatory
    for this module.
  - This module uses PC v4 APIs based SDKs (ntnx_prism_py_client).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get External Storage by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, Storage Admin, Storage Viewer.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the external storage resource to fetch.
      - Required for this module because the Prism v4 SDK for ExternalStorage
        only exposes a get-by-id operation and does not support listing.
    type: str
    required: true
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
- name: Get external storage by ext_id
  nutanix.ncp.ntnx_external_storages_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ExternalStorage info v4 API.
    - Returns a single ExternalStorage entity when C(ext_id) is provided.
    - The Prism v4 SDK for ExternalStorage does not expose a list operation,
      so this module always returns a single entity dict.
  returned: always
  type: dict
  sample:
    {
      "config": {
        "address": {
          "fqdn": null,
          "ipv4": {
            "prefix_length": 32,
            "value": "10.44.76.100"
          },
          "ipv6": null
        },
        "system_id": "5a5f3a2c9b0f7c01",
        "storage_pool": {
          "name": "pool-01",
          "protection_domain_name": "pd-01",
          "storage_pool_id": "8f0d1e5c9a2b4d3e"
        }
      },
      "ext_id": "d4e44c2b-944c-48b0-8de1-b0adae3d54c6",
      "free_capacity_bytes": 1099511627776,
      "links": null,
      "name": "external-storage-dell-powerflex-01",
      "provider_type": "DELL_POWERFLEX",
      "tenant_id": null,
      "total_capacity_bytes": 5497558138880
    }

ext_id:
  description:
    - The external ID of the external storage resource that was fetched.
  returned: when external ID is provided
  type: str
  sample: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching external storage info using ext_id"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_external_storage  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_external_storages_api_instance,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_external_storage_using_ext_id(module, external_storages_api, result):
    """Fetch a single ExternalStorage entity by its external ID."""
    ext_id = module.params.get("ext_id")
    resp = get_external_storage(module, external_storages_api, ext_id)
    result["ext_id"] = ext_id
    if resp is None:
        result["response"] = None
        return
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "ext_id": None, "failed": False}
    external_storages_api = get_external_storages_api_instance(module)
    get_external_storage_using_ext_id(module, external_storages_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
