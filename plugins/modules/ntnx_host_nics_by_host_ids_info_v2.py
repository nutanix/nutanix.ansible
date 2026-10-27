#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_nics_by_host_ids_info_v2
short_description: Fetch host NICs information for a specific host in a Nutanix cluster.
version_added: 2.7.0
description:
  - This module allows you to fetch information about host NICs for a host in a cluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific host NIC belonging to the given host and cluster.
  - If C(ext_id) is not provided, list all host NICs of the host optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Cluster Host Nic) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin,
    Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - External identifier (UUID) of the parent cluster the host belongs to.
      - Required because the API endpoint is scoped by the parent cluster.
    type: str
    required: true
  host_ext_id:
    description:
      - External identifier (UUID) of the host whose NICs should be fetched.
      - Required because the API endpoint is scoped by the parent host.
    type: str
    required: true
  ext_id:
    description:
      - External identifier (UUID) of a specific host NIC on the given host.
      - If provided, the module returns a single host NIC; otherwise, it returns
        the list of host NICs for the host.
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
- name: List all host NICs for a given cluster and host
  nutanix.ncp.ntnx_host_nics_by_host_ids_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result
  ignore_errors: true

- name: Fetch a specific host NIC by external ID
  nutanix.ncp.ntnx_host_nics_by_host_ids_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "5b2e4e93-2222-3333-7777-a015d302eec2"
  register: result
  ignore_errors: true

- name: List host NICs filtered by name
  nutanix.ncp.ntnx_host_nics_by_host_ids_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    filter: "name eq 'eth0'"
  register: result
  ignore_errors: true

- name: List host NICs with limit
  nutanix.ncp.ntnx_host_nics_by_host_ids_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    limit: 1
  register: result
  ignore_errors: true

- name: List all host NICs for a host with fetch_all
  nutanix.ncp.ntnx_host_nics_by_host_ids_info_v2:
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC host NIC info v4 API.
    - It can be a single host NIC if external ID is provided.
    - List of multiple host NICs for the host if external ID is not provided with optional filter, limit, orderby, or select.
  returned: always
  type: dict
  sample:
    {
      "attached_switch_interface_list": null,
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "discovery_protocol": "LLDP",
      "driver_version": "ixgbe:6.3.4",
      "ext_id": "8ae64a0e-bf81-4424-b57f-5cbc8e8f24ac",
      "firmware_version": "0x800006d1, 255.65535.255",
      "host_description": "Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (Ethernet Server Adapter X520-2)",
      "interface_status": "1",
      "ipv4_addresses": null,
      "ipv6_addresses": null,
      "is_dhcp_enabled": null,
      "link_capacity_in_mbps": 10000,
      "link_speed_in_kbps": 10000000,
      "links": null,
      "mac_address": "00:e0:ed:94:40:ef",
      "mtu_in_bytes": 1500,
      "name": "eth3",
      "nic_profile_ext_id": null,
      "node_uuid": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
      "pci_model_id": "8086:10fb",
      "rx_ring_size_in_bytes": 512,
      "supported_capabilities": ["PCIEPASSTHROUGH"],
      "switch_device_id": "p5r7r04-leaf2",
      "switch_mac_address": "c4:5a:b1:20:49:05",
      "switch_management_ip": {
        "ipv4": null,
        "ipv6": {"prefix_length": 128, "value": "fe80::faf2:1eff:fe36:95c0"}
      },
      "switch_port_id": null,
      "switch_vendor_info": "5c:16:c7:00:00:01",
      "switch_vlan_id": null,
      "tenant_id": null,
      "tx_ring_size_in_bytes": 512,
      "virtual_nic_ext_ids": null,
      "virtual_switch_ext_id": "22672efd-210f-41dc-9934-d3cb5908b727"
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
  sample: "Api Exception raised while fetching host NICs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the host NIC (when requested via C(ext_id)).
  type: str
  returned: When external ID is provided
  sample: "1ada3cfc-c1c5-4bcd-a55d-d2f7e46a4b41"

total_available_results:
  description: The total number of host NICs available for the given cluster and host in PC.
  type: int
  returned: When listing host NICs
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_host_nic  # noqa: E402
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
        cluster_ext_id=dict(type="str", required=True),
        host_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_host_nic_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_host_nic(module, api_instance, ext_id, cluster_ext_id, host_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_host_nics(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating host NICs info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_host_nics_by_host_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
            hostExtId=host_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host NICs info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_host_nic_using_ext_id(module, api_instance, result)
    else:
        get_host_nics(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
