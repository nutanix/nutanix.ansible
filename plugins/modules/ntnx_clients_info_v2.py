#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clients_info_v2
short_description: Fetch registered clients info in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch information about Registered Clients in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific registered client.
    - If C(ext_id) is not provided, list multiple registered clients optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get registered client by ext_id) -
      Required Roles: Account Owner, Administrator, NCM Admin, Nutanix Central Admin, Prism Admin,
        Prism Viewer, Project Manager, Self-Service Admin, Super Admin, User
    - >-
      B(List all the registered clients) -
      Required Roles: Account Owner, Administrator, NCM Admin, Nutanix Central Admin, Prism Admin,
        Prism Viewer, Project Manager, Self-Service Admin, Super Admin, User
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    ext_id:
        description:
            - The external ID of the registered client.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get registered client using ext_id
  nutanix.ncp.ntnx_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "21bc5e8e-5854-5bd4-8dcc-924f24b0ddf4"
  register: result
  ignore_errors: true

- name: List all registered clients
  nutanix.ncp.ntnx_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List registered clients with filter
  nutanix.ncp.ntnx_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'Prism Service'"
  register: result
  ignore_errors: true

- name: List registered clients with limit
  nutanix.ncp.ntnx_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List all registered clients with fetch_all
  nutanix.ncp.ntnx_clients_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Registered Clients info v4 API.
    - It can be a single registered client if External ID is provided.
    - List of multiple registered clients if External ID is not provided with optional filter or limit.
  returned: always
  type: dict
   sample:
     {
       "created_by": null,
       "created_time": "2026-10-14T07:25:50.338347+00:00",
       "deployment_list": [
         "onPrem"
       ],
       "description": "description",
       "display_name": "CatalogService",
       "ext_id": "1b214b08-275a-4753-62a1-53c2501f999e",
       "last_updated_time": "2026-10-14T07:25:50.338347+00:00",
       "links": null,
       "name": "CatalogService",
       "tenant_id": null
     }
 changed:
   description: This indicates whether the task resulted in any changes
   returned: always
   type: bool
   sample: false
 msg:
   description: This indicates the message if any message occurred
   returned: When there is an error
   type: str
   sample: "Api Exception raised while fetching registered clients info"
 error:
   description: This field typically holds information about if the task have errors that occurred during the task execution
   returned: when an error occurs
   type: str
 failed:
   description: This field typically holds information about if the task have failed
   returned: always
   type: bool
   sample: false
 ext_id:
   description: External ID of the registered client
   returned: when external ID is provided
   type: str
   sample: "1b214b08-275a-4753-62a1-53c2501f999e"
total_available_results:
  description: The total number of available registered clients in PC.
  returned: when all registered clients are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_registered_client_api_instance,
)
from ..module_utils.v4.iam.helpers import get_registered_client  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_registered_client_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_registered_client(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_registered_clients(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating registered clients info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_registered_clients,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching registered clients info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data")

    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_registered_client_api_instance(module)
    if module.params.get("ext_id"):
        get_registered_client_using_ext_id(module, api_instance, result)
    else:
        get_registered_clients(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
