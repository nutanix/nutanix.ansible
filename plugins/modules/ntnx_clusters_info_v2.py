#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_info_v2
short_description: Retrieve information about Nutanix clusters from PC
version_added: 2.0.0
description:
    - This module retrieves information about Nutanix clusters from PC.
    - Fetch particular cluster info using external ID
    - Fetch multiple clusters info with/without using filters, limit, etc.
    - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the cluster.
      - If not provided, multiple clusters info will be fetched.
    type: str
    required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: fetch cluster info using external ID
  nutanix.ncp.ntnx_clusters_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
  register: result

- name: fetch all clusters info
  nutanix.ncp.ntnx_clusters_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: fetch all clusters info with filter
  nutanix.ncp.ntnx_clusters_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: "name eq 'cluster1'"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching cluster info.
        - Returns cluster info if ext_id is provided or list of multiple clusters.
    type: dict
    returned: always
    sample:
        {
  "config":
    {
      "authorized_public_key_list":
        [
          {
            "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDQ6",
            "name": "key1",
          },
        ],
      "build_info":
        {
          "build_type": "release",
          "commit_id": "9b27c8bcb5fcaac58016f3bed74009655a157049",
          "full_version": "el8.5-release-fraser-6.8-stable-9b27c8bcb5fcaac58016f3bed74009655a157049",
          "short_commit_id": "9b27c8",
          "version": "fraser-6.8-stable",
        },
      "cluster_arch": "X86_64",
      "cluster_function": ["AOS", "ONE_NODE"],
      "cluster_software_map":
        [
          { "software_type": "NCC", "version": "ncc-5.0.0" },
          {
            "software_type": "NOS",
            "version": "el8.5-release-fraser-6.8-stable-9b27c8bcb5fcaac58016f3bed74009655a157049",
          },
        ],
      "encryption_in_transit_status": null,
      "encryption_option": null,
      "encryption_scope": null,
      "fault_tolerance_state":
        {
          "current_max_fault_tolerance": 0,
          "desired_max_fault_tolerance": 0,
          "domain_awareness_level": "DISK",
        },
      "hypervisor_types": ["AHV"],
      "incarnation_id": 1283123882137,
      "is_lts": false,
      "operation_mode": "NORMAL",
      "password_remote_login_enabled": true,
      "redundancy_factor": 1,
      "remote_support": false,
      "timezone": "UTC",
    },
  "container_name": null,
  "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
  "inefficient_vm_count": null,
  "links": null,
  "name": "ansible_ag",
  "network":
    {
      "backplane":
        {
          "is_segmentation_enabled": false,
          "netmask": null,
          "subnet": null,
          "vlan_tag": null,
        },
      "external_address":
        {
          "ipv4": { "prefix_length": 32, "value": "10.0.0.1" },
          "ipv6": null,
        },
      "external_data_service_ip":
        {
          "ipv4": { "prefix_length": 32, "value": "10.0.0.2" },
          "ipv6": null,
        },
      "fqdn": null,
      "key_management_server_type": null,
      "management_server": null,
      "masquerading_ip": null,
      "masquerading_port": null,
      "name_server_ip_list":
        [
          {
            "fqdn": null,
            "ipv4": { "prefix_length": 32, "value": "10.0.0.6" },
            "ipv6": null,
          },
        ],
      "nfs_subnet_whitelist": null,
      "ntp_server_ip_list":
        [
          {
            "fqdn": { "value": "0.ntp.org" },
            "ipv4": null,
            "ipv6": null,
          },
        ],
      "smtp_server":
        {
          "email_address": "test@test.com",
          "server":
            {
              "ip_address":
                {
                  "ipv4": { "prefix_length": 32, "value": "10.0.0.8" },
                  "ipv6": null,
                },
              "password": null,
              "port": 25,
              "username": "username",
            },
          "type": "STARTTLS",
        },
    },
  "nodes":
    {
      "node_list":
        [
          {
            "controller_vm_ip":
              {
                "ipv4": { "prefix_length": 32, "value": "10.0.0.6" },
                "ipv6": null,
              },
            "host_ip":
              {
                "ipv4": { "prefix_length": 32, "value": "10.0.0.10" },
                "ipv6": null,
              },
            "node_uuid": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
          },
        ],
      "number_of_nodes": 1,
    },
  "run_prechecks_only": null,
  "tenant_id": null,
  "upgrade_status": "SUCCEEDED",
  "vm_count": 1,
}
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching clusters info"
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs
ext_id:
    description:
        - The external ID of the cluster if given in input.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
total_available_results:
    description:
        - The total number of available clusters in PC.
    type: int
    returned: when all clusters are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster  # noqa: E402
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


def get_cluster_by_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    clusters = get_clusters_api_instance(module)
    resp = get_cluster(module, clusters, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_clusters(module, result):
    clusters = get_clusters_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json("Failed creating query parameters for fetching clusters info")
    resp = None
    try:
        resp = clusters.list_clusters(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching clusters info",
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
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id") or module.params.get("name"):
        get_cluster_by_ext_id(module, result)
    else:
        get_clusters(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
