#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_nics_info_v2
short_description: Fetch host NIC info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about HostNic in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific HostNic.
  - If C(ext_id) is not provided, list multiple HostNic optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get host NIC by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin, Network Infra Admin,
      Virtual Machine Admin, Virtual Machine Viewer
    - >-
      B(List host NICs) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin, Network Infra Admin,
      Virtual Machine Admin, Virtual Machine Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the host NIC.
      - When provided, C(cluster_ext_id) and C(host_ext_id) MUST also be supplied so that
        the get-by-ID call can locate the NIC under its parent cluster/host.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the cluster that owns the host NIC.
      - Required together with C(host_ext_id) when fetching a single host NIC by C(ext_id).
      - Required together with C(host_ext_id) when listing host NICs scoped to a specific host.
    type: str
    required: false
  host_ext_id:
    description:
      - The external ID of the host that owns the host NIC.
      - Required together with C(cluster_ext_id) when fetching a single host NIC by C(ext_id).
      - Required together with C(cluster_ext_id) when listing host NICs scoped to a specific host.
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
- name: Fetch a specific host NIC using ext_id, cluster_ext_id and host_ext_id
  nutanix.ncp.ntnx_cluster_host_nics_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
  register: host_nic

- name: List all host NICs on a specific host
  nutanix.ncp.ntnx_cluster_host_nics_info_v2:
    cluster_ext_id: "0005b3f7-1234-4321-abcd-0123456789ab"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: host_nics_by_host

- name: List all host NICs across Prism Central
  nutanix.ncp.ntnx_cluster_host_nics_info_v2:
  register: all_host_nics

- name: List host NICs with a filter
  nutanix.ncp.ntnx_cluster_host_nics_info_v2:
    filter: "name eq 'eth0'"
  register: filtered_host_nics

- name: List host NICs with a limit
  nutanix.ncp.ntnx_cluster_host_nics_info_v2:
    limit: 5
  register: limited_host_nics
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC HostNic info v4 API.
    - It can be a single HostNic if external ID is provided.
    - List of multiple HostNic if external ID is not provided (with optional filter or limit).
  returned: always
  type: dict
  sample:
    {
        "attached_switch_interface_list": null,
        "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
        "discovery_protocol": null,
        "driver_version": "igb:5.19.10",
        "ext_id": "084af8fb-87f8-46e6-a2f4-cabeffc81850",
        "firmware_version": "1.63, 0x80000a05",
        "host_description": "Intel Corporation I350 Gigabit Network Connection (Super Micro Computer Inc X10DRW-i)",
        "interface_status": "0",
        "ipv4_addresses": null,
        "ipv6_addresses": null,
        "is_dhcp_enabled": null,
        "link_capacity_in_mbps": 1000,
        "link_speed_in_kbps": 0,
        "links": null,
        "mac_address": "ac:1f:6b:6f:9e:49",
        "mtu_in_bytes": 1500,
        "name": "eth1",
        "nic_profile_ext_id": null,
        "node_uuid": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
        "pci_model_id": "8086:1521",
        "rx_ring_size_in_bytes": 256,
        "supported_capabilities": ["PCIEPASSTHROUGH"],
        "switch_device_id": null,
        "switch_mac_address": null,
        "switch_management_ip": null,
        "switch_port_id": null,
        "switch_vendor_info": null,
        "switch_vlan_id": null,
        "tenant_id": null,
        "tx_ring_size_in_bytes": 256,
        "virtual_nic_ext_ids": null,
        "virtual_switch_ext_id": "22672efd-210f-41dc-9934-d3cb5908b727"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching host NICs info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the host NIC.
  type: str
  returned: When external ID is provided
  sample: "084af8fb-87f8-46e6-a2f4-cabeffc81850"

total_available_results:
  description: The total number of available host NICs matching the query.
  type: int
  returned: When a list call is made (no C(ext_id) provided).
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
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        host_ext_id=dict(type="str"),
    )

    return module_args


def get_host_nic_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    if not cluster_ext_id or not host_ext_id:
        module.fail_json(
            msg=(
                "cluster_ext_id and host_ext_id are required together with ext_id "
                "to fetch a specific host NIC."
            ),
            **result,
        )

    resp = get_host_nic(module, api_instance, ext_id, cluster_ext_id, host_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_host_nics(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating host NICs info spec", **result)

    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")

    if cluster_ext_id and host_ext_id:
        # Scoped to a host under a cluster.
        try:
            resp = api_instance.list_host_nics_by_host_id(
                clusterExtId=cluster_ext_id,
                hostExtId=host_ext_id,
                **kwargs,
            )
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching host NICs for the given host",
            )
    elif cluster_ext_id or host_ext_id:
        # One is provided without the other — hard-fail with a clear message
        # so the caller understands the scoped-list contract.
        module.fail_json(
            msg=(
                "cluster_ext_id and host_ext_id must be provided together to list "
                "host NICs scoped to a specific host."
            ),
            **result,
        )
    else:
        # Global list.
        try:
            resp = api_instance.list_host_nics(**kwargs)
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching host NICs info",
            )

    total_available_results = None
    if getattr(resp, "metadata", None) is not None:
        total_available_results = getattr(
            resp.metadata, "total_available_results", None
        )
    if total_available_results is not None:
        result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
        required_by={
            "ext_id": ["cluster_ext_id", "host_ext_id"],
        },
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_host_nic_by_ext_id(module, api_instance, result)
    else:
        list_host_nics(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
