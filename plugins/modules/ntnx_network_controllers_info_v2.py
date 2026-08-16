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
version_added: 2.5.0
description:
  - This module allows you to fetch information about NetworkController in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific NetworkController.
  - If C(ext_id) is not provided, list multiple NetworkController optionally paginated.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Network Controller by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin,
      Prism Viewer, Project Admin, Super Admin, VPC Admin
    - >-
      B(Get list of Network Controllers) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin,
      Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the network controller.
      - If provided, only the specific controller is fetched; otherwise all controllers are listed.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
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
    - The response from the Nutanix PC NetworkController info v4 API.
    - It can be a single NetworkController if external ID is provided.
    - List of multiple NetworkController if external ID is not provided with optional limit.
  returned: always
  type: dict
  sample:
    {
      "cloud_substrate": null,
      "controller_status": "UP",
      "controller_version": "7.6.0",
      "default_vlan_stack": "LEGACY",
      "ext_id": "98fac596-6e4f-407e-bfbb-89681ca72415",
      "links": null,
      "metadata": null,
      "minimum_ahv_version": "11.2",
      "minimum_nos_version": "7.0",
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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_network_controller_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_network_controller(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_network_controllers(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating network controllers info spec", **result
        )

    kwargs.pop("_filter", None)
    kwargs.pop("_orderby", None)
    kwargs.pop("_select", None)

    try:
        resp = api_instance.list_network_controllers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network controllers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_network_controllers_api_instance(module)
    if module.params.get("ext_id"):
        get_network_controller_using_ext_id(module, api_instance, result)
    else:
        get_network_controllers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
