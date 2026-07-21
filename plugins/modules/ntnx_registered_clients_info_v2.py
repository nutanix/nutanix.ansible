#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_registered_clients_info_v2
short_description: Fetch registered client info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about RegisteredClient in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RegisteredClient.
  - The Nutanix IAM v4 API for RegisteredClient only supports get-by-id;
    listing multiple registered clients is not exposed by the SDK for this
    version. C(ext_id) is therefore required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get registered client by ext_id) -
    Required Roles: Super Admin, Prism Admin, Prism Viewer.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - The external identifier of the registered client to fetch.
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
- name: Fetch registered client using external ID
  nutanix.ncp.ntnx_registered_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RegisteredClient info v4 API.
    - Contains the RegisteredClient details for the provided external ID.
  returned: always
  type: dict
  sample:
    {
      "created_by": null,
      "created_time": "2026-06-29T07:20:18.080897+00:00",
      "deployment_list": ["onPrem"],
      "description": "description",
      "display_name": "CatalogService",
      "ext_id": "21bc5e8e-5854-5bd4-8dcc-924f24b0ddf4",
      "last_updated_time": "2026-06-29T07:20:18.080897+00:00",
      "links": null,
      "name": "CatalogService",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching registered client info using ext_id"

error:
  description:
    - This field typically holds information about if the task have errors that
      occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the registered client.
  type: str
  returned: when external ID is provided
  sample: "21bc5e8e-5854-5bd4-8dcc-924f24b0ddf4"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_registered_client_api_instance,
)
from ..module_utils.v4.iam.helpers import get_registered_client  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_registered_client_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_registered_client(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "ext_id": None, "failed": False}
    api_instance = get_registered_client_api_instance(module)
    get_registered_client_by_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
