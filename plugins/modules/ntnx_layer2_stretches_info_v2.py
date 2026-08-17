#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_layer2_stretches_info_v2
short_description: Fetch Layer2Stretch information in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Layer2Stretch in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Layer2Stretch.
  - If C(ext_id) is not provided, list multiple Layer2Stretch optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Layer2Stretch by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - >-
      B(Get list of Layer2Stretch) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the Layer2Stretch.
    type: str
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
- name: Get Layer2Stretch using ext_id
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all Layer2Stretches
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
  register: result
  ignore_errors: true

- name: List Layer2Stretches with filter
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    filter: "name eq 'layer2_stretch_ansible'"
  register: result
  ignore_errors: true

- name: List Layer2Stretches with limit
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Layer2Stretch info v4 API.
    - It can be a single Layer2Stretch if external ID is provided.
    - List of multiple Layer2Stretch if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "connection_type": "VPN",
      "description": "Layer2Stretch created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "high_availability_status": null,
      "links": null,
      "local_site_params": {
        "connection_reference": "a4f3f04f-1222-8544-7896-28b62bcc3e3e",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "18553f0f-7ce0-4c33-a697-0eecfb27fc10",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "b0cce620-3654-8522-9876-a91e2c037862",
        "vpn_interface_ip_address": null
      },
      "metadata": null,
      "mtu": 1500,
      "name": "layer2_stretch_ansible",
      "remote_site_params": {
        "connection_reference": "e7f3f04f-2222-3333-4444-28b62bcc3e3f",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "78e0d3ac-9e08-4d0c-8f1c-3d90ac2a55f0",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "b7c94b93-2222-3333-4444-91e2c0378621",
        "vpn_interface_ip_address": null
      },
      "remote_stretch_status": null,
      "stretch_status": null,
      "tenant_id": null,
      "vni": null
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
  sample: "Api Exception raised while fetching Layer2Stretch info"

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
  description: External ID of the Layer2Stretch
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: The total number of available Layer2Stretches in PC.
  type: int
  returned: when all Layer2Stretches are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_layer2_stretches_api_instance,
)
from ..module_utils.v4.network.helpers import get_layer2_stretch  # noqa: E402
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


def get_layer2_stretch_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_layer2_stretch(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_layer2_stretches(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Layer2Stretches info spec", **result)

    try:
        resp = api_instance.list_layer2_stretches(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Layer2Stretches info",
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
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_layer2_stretches_api_instance(module)
    if module.params.get("ext_id"):
        get_layer2_stretch_using_ext_id(module, api_instance, result)
    else:
        get_layer2_stretches(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
