#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nodess_info_v2
short_description: Fetch nodes info managed by Foundation Central
version_added: 2.7.0
description:
  - This module allows you to fetch nodes info or a specific node managed by Foundation Central.
  - If C(ext_id) is provided, fetch a particular node info using its external ID.
  - If C(ext_id) is not provided, fetch multiple nodes info with/without using filters, limit, etc.
  - This module uses the Life Cycle Management v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central) (FCVM/Foundation), NOT to Prism Central.
    Set C(nutanix_host) to the Foundation Central endpoint.
  - >-
    B(Get a Node by ext_id) - Requires the appropriate Foundation Central role on the FCVM.
  - >-
    B(List Nodes) - Requires the appropriate Foundation Central role on the FCVM.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - The external ID of the node.
      - If provided, a single node is returned.
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
- name: Get node using ext_id
  nutanix.ncp.ntnx_nodess_info_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true

- name: List all nodes
  nutanix.ncp.ntnx_nodess_info_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List nodes with filter
  nutanix.ncp.ntnx_nodess_info_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "manufacturer eq 'Nutanix'"
  register: result
  ignore_errors: true

- name: List nodes with limit
  nutanix.ncp.ntnx_nodess_info_v2:
    nutanix_host: "{{ foundation_central_ip }}"
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
    - The response from the Nutanix nodes info v4 API (host is FCVM/Foundation, not PC).
    - It can be a single node if the external ID is provided.
    - List of multiple nodes if the external ID is not provided, with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "aos_version": "7.0",
      "block_serial_number": "20SM6M420001",
      "cpu_info": {
        "capacity_g_hz": 2.5,
        "logical_core_count": 40,
        "manufacturer": "Intel",
        "model": "Xeon Gold 6248",
        "socket_count": 2
      },
      "custom_attributes": ["rack=1"],
      "cvm_connectivity_status": "CONNECTED",
      "ext_id": "d1a1a1a1-1111-2222-3333-444455556666",
      "host_connectivity_status": "CONNECTED",
      "host_type": "AHV",
      "host_version": "10.0",
      "hostname": "node-ansible",
      "identifiers": [{"type": "SERIAL_NUMBER", "value": "ZM204S000001"}],
      "links": null,
      "manufacturer": "Nutanix",
      "memory_gb": 512,
      "model": "NX-3060-G7",
      "network_details": null,
      "owner_ext_id": null,
      "provider_connection_ext_id": null,
      "provider_data": null,
      "provider_ext_id": null,
      "state": "ONBOARDED",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: contextual
  type: str
  sample: "Api Exception raised while fetching nodes info"

error:
  description: This field holds the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

ext_id:
  description: External ID of the node.
  returned: when a single node is fetched (ext_id provided)
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

total_available_results:
  description: The total number of available nodes in Foundation Central.
  returned: when all nodes are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_nodes_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_node  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
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


def get_node_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_node(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def get_nodes(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating nodes info spec", **result)

    try:
        resp = api_instance.list_nodes(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching nodes info",
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
    api_instance = get_nodes_api_instance(module)
    if module.params.get("ext_id"):
        get_node_by_ext_id(module, api_instance, result)
    else:
        get_nodes(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
