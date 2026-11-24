#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_external_storage_info_v2
short_description: Fetch external storage info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch external storage info in Nutanix Prism Central.
  - This API has been deprecated. Fetch a specific external storage by its
    external ID using C(ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get external storage by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Storage Admin, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the external storage.
      - Required to fetch a specific external storage.
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
- name: Get external storage using ext_id (prism deprecated API)
  nutanix.ncp.ntnx_external_storage_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix external storage info v4 API. The host is Prism Central (PC).
    - It is a single external storage if external ID is provided.
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
        "storage_pool": {
          "name": "sp-01",
          "protection_domain_name": "pd-01",
          "storage_pool_id": "sp-id-01"
        },
        "system_id": "powerflex-system-01"
      },
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "name": "external_storage_ansible",
      "provider_type": "DELL_POWERFLEX",
      "tenant_id": null,
      "total_capacity_bytes": 1099511627776,
      "free_capacity_bytes": 549755813888
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching external storage info using ext_id"

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the external storage.
  type: str
  returned: When external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"
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


def get_external_storage_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_external_storage(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_external_storages_api_instance(module)
    get_external_storage_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
