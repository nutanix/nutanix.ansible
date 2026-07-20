#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_layer2_stretches_info_v2
short_description: Fetch Layer2 Stretch info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Layer2 Stretch in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Layer2 Stretch.
  - If C(ext_id) is not provided, list multiple Layer2 Stretch optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Layer2 Stretch by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - >-
      B(Get list of Layer2 Stretches) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID of the Layer2 Stretch.
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
- name: Get Layer2 Stretch using ext_id
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all Layer2 Stretches
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Layer2 Stretches with filter
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'l2_stretch_ansible'"
  register: result
  ignore_errors: true

- name: List Layer2 Stretches with limit
  nutanix.ncp.ntnx_layer2_stretches_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Layer2 Stretch info v4 API.
    - It can be a single Layer2 Stretch if external ID is provided.
    - List of multiple Layer2 Stretch if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "connection_type": "VPN",
      "description": "Layer2 Stretch over VPN created by Ansible",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "high_availability_status": null,
      "links": null,
      "local_site_params": {
        "connection_reference": "3f9e5c2d-1111-4e00-9999-0000000000cc",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "5ab1b1a2-1111-4e00-9999-0000000000aa",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "8b5df6bc-1111-4e00-9999-0000000000bb",
        "vpn_interface_ip_address": null
      },
      "metadata": null,
      "mtu": null,
      "name": "l2_stretch_vpn_ansible",
      "remote_site_params": {
        "connection_reference": "4a0f6d3e-2222-4e00-9999-0000000000ff",
        "default_gateway_ip_address": null,
        "high_availability_group": null,
        "pc_cluster_reference": "6bc2b2b3-2222-4e00-9999-0000000000dd",
        "stretch_interface_ip_address": null,
        "stretch_subnet_reference": "9c6ef7cd-2222-4e00-9999-0000000000ee",
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
  sample: "Api Exception raised while fetching Layer2 Stretches info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Layer2 Stretch
  type: str
  returned: when external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available Layer2 Stretches in PC.
  type: int
  returned: when all Layer2 Stretches are fetched
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
        module.fail_json(msg="Failed generating Layer2 Stretches info spec", **result)

    try:
        resp = api_instance.list_layer2_stretches(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Layer2 Stretches info",
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
