#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_network_controllers_info_v2
short_description: Fetch network controllers info in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to fetch network controllers info or specific network controller in Nutanix Prism Central.
  - If ext_id is provided, fetch particular network controller info using external ID
  - If ext_id is not provided, fetch list of multiple network controllers info with/without using page and limit parameters.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get network controller by ext_id) -
      Required Roles: Prism User, Super Admin
    - >-
      B(Get list of Network Controllers) -
      Required Roles: Prism User, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external identifier of the network controller.
    type: str
  page:
    description:
      - The page number
    type: int
  limit:
    description:
      - The number of network controllers to fetch per page
    type: int
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Get network controller using ext_id
  nutanix.ncp.ntnx_network_controllers_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all network controllers
  nutanix.ncp.ntnx_network_controllers_info_v2:
  register: result
  ignore_errors: true

- name: List network controllers with limit
  nutanix.ncp.ntnx_network_controllers_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - Response for fetching network controllers info
    - Specific network controller info if External ID is provided
    - List of multiple network controllers info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
      "cloud_substrate": null,
      "controller_health": null,
      "controller_status": "UP",
      "controller_version": "6.5",
      "default_vlan_stack": "ADVANCED",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "metadata": null,
      "minimum_ahv_version": null,
      "minimum_nos_version": null,
      "project_ext_id": null,
      "tenant_id": null,
      "vpc_global_config": {
          "is_overlapping_erps_enabled": false
      }
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
  sample: "Api Exception raised while fetching network controllers info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs
  sample: null

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the network controller
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available network controllers in PC.
  type: int
  returned: when all network controllers are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_network_controllers_api_instance,
)
from ..module_utils.v4.network.helpers import get_network_controller  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
    )

    return module_args


def get_network_controller_using_ext_id(module, network_controllers, result):
    ext_id = module.params.get("ext_id")
    resp = get_network_controller(module, network_controllers, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_network_controllers(module, network_controllers, result):

    kwargs = {}
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")

    try:
        resp = network_controllers.list_network_controllers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network controllers info",
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
    result = {"changed": False, "response": None}
    network_controllers = get_network_controllers_api_instance(module)
    if module.params.get("ext_id"):
        get_network_controller_using_ext_id(module, network_controllers, result)
    else:
        get_network_controllers(module, network_controllers, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
