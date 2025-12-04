#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_imaged_clusters_info
short_description: Nutanix module which returns the imaged clusters within the Foundation Central
version_added: 1.1.0
description: 'List all the imaged clusters created in Foundation Central.'
options:
  imaged_cluster_uuid:
    description:
      - Return the cluster details given it's uuid
    type: str
    required: false
  length:
    description:
      - Return the list of imaged clusters upto the length or by default 10.
    type: int
    required: false
    default: 10
  offset:
    description:
      - Returns the list of imaged clusters starting with offset index.
    type: int
    required: false
    default: 0
  filters:
    description:
      - Returns the list of imaged clusters based on archived status
    type: dict
    required: false
    suboptions:
        archived:
            description:
              - archived clusters
            type: bool
            required: false
            default: false
  custom_filter:
    description:
      - write
    type: dict
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations
      - nutanix.ncp.ntnx_logger
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Abhishek Chaudhary (@abhimutant)
"""

EXAMPLES = r"""
- name: Get cluster details using uuid
  ntnx_foundation_central_imaged_nodes_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    imaged_cluster_uuid: "{{node_uuid}}"

- name: Get imaged clusters list based on filters
  ntnx_foundation_central_imaged_nodes_info:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filters:
    archived: false
    length: 5
    offset: 1
"""

RETURN = r"""
Imaged_Clusters_list:
  description: All the imaged clusters within Foundation Central
  returned: always
  type: list
  sample:
   [
            {
                "archived": false,
                "cluster_external_ip": "",
                "cluster_name": "test_cluster",
                "cluster_size": 0,
                "cluster_status": {
                    "aggregate_percent_complete": 100,
                    "cluster_creation_started": true,
                    "cluster_progress_details": {
                        "cluster_name": "test_cluster",
                        "message_list": [],
                        "percent_complete": 100,
                        "status": "All operations completed successfully"
                    },
                    "current_foundation_ip": "10.x.xx.xx",
                    "foundation_session_id": "<session_id>",
                    "imaging_stopped": true,
                    "intent_picked_up": true,
                    "node_progress_details": [
                        {
                            "imaged_node_uuid": "<node_uuid>",
                            "imaging_stopped": true,
                            "intent_picked_up": true,
                            "message_list": [],
                            "percent_complete": 100,
                            "status": "All operations completed successfully"
                        },
                        {
                            "imaged_node_uuid": "<node_uuid>",
                            "imaging_stopped": true,
                            "intent_picked_up": true,
                            "message_list": [],
                            "percent_complete": 100,
                            "status": "All operations completed successfully"
                        },
                        {
                            "imaged_node_uuid": "<node_uuid>",
                            "imaging_stopped": true,
                            "intent_picked_up": true,
                            "message_list": [],
                            "percent_complete": 100,
                            "status": "All operations completed successfully"
                        }
                    ]
                },
                "common_network_settings": {
                    "cvm_dns_servers": [
                        "10.x.xx.xx"
                    ],
                    "cvm_ntp_servers": null,
                    "hypervisor_dns_servers": [
                        "10.x.xx.xx"
                    ],
                    "hypervisor_ntp_servers": null
                },
                "created_timestamp": "2021-12-05T20:37:25.000-08:00",
                "current_time": "2022-04-25T11:45:04.000-07:00",
                "destroyed": false,
                "foundation_init_config": {
                    "blocks": [
                        {
                            "block_id": "<block_id>",
                            "nodes": [
                                {
                                    "cvm_ip": "10.x.xx.xx",
                                    "fc_imaged_node_uuid": "<node_uuid>",
                                    "hypervisor": "kvm",
                                    "hypervisor_hostname": "Host-1",
                                    "hypervisor_ip": "10.x.xx.xx",
                                    "image_now": true,
                                    "ipmi_ip": "10.x.xx.xx",
                                    "ipv6_address": "<ipv6_address>",
                                    "node_position": "A",
                                    "node_serial": "<node_serial>"
                                },
                                {
                                    "cvm_ip": "10.x.xx.xx",
                                    "fc_imaged_node_uuid": "<node_uuid>",
                                    "hypervisor": "kvm",
                                    "hypervisor_hostname": "Host-2",
                                    "hypervisor_ip": "10.x.xx.xx",
                                    "image_now": true,
                                    "ipmi_ip": "10.x.xx.xx",
                                    "ipv6_address": "<ipv6_address>",
                                    "node_position": "B",
                                    "node_serial": "<node_serial>"
                                },
                                {
                                    "cvm_ip": "10.x.xx.xx",
                                    "fc_imaged_node_uuid": "<node_uuid>",
                                    "hypervisor": "kvm",
                                    "hypervisor_hostname": "Host-3",
                                    "hypervisor_ip": "10.x.xx.xx",
                                    "image_now": true,
                                    "ipmi_ip": "10.x.xx.xx",
                                    "ipv6_address": "<ipv6_address>",
                                    "node_position": "C",
                                    "node_serial": "<node_serial>"
                                }
                            ]
                        }
                    ],
                    "clusters": [
                        {
                            "cluster_external_ip": "",
                            "cluster_init_now": true,
                            "cluster_init_successful": false,
                            "cluster_members": [
                                "10.x.xx.xx",
                                "10.x.xx.xx",
                                "10.x.xx.xx"
                            ],
                            "cluster_name": "test_cluster",
                            "cvm_dns_servers": "10.x.xx.xx",
                            "hypervisor_nameserver": "10.x.xx.xx",
                            "redundancy_factor": 2,
                            "timezone": "Africa/Abidjan"
                        }
                    ],
                    "cvm_gateway": "10.x.xx.xx",
                    "cvm_netmask": "xx.xx.xx.xx",
                    "dns_servers": "10.x.xx.xx",
                    "hyperv_product_key": "",
                    "hyperv_sku": "",
                    "hypervisor_gateway": "10.xx.xx.xx",
                    "hypervisor_iso_url": {
                        "hypervisor_type": "",
                        "sha256sum": "",
                        "url": ""
                    },
                    "hypervisor_isos": [
                        {
                            "hypervisor_type": "kvm",
                            "sha256sum": "",
                            "url": "<url>"
                        }
                    ],
                    "hypervisor_netmask": "xx.xx.xx.xx",
                    "ipmi_gateway": "10.x.xx.xx",
                    "ipmi_netmask": "xx.xx.xx.xx",
                    "nos_package_url": {
                        "sha256sum": "",
                        "url": "<url>"
                    }
                },
                "foundation_init_node_uuid": "<node_uuid>",
                "imaged_cluster_uuid": "<cluster_uuid>",
                "imaged_node_uuid_list": [
                    "<imaged-node-uuid-1>",
                    "<imaged-node-uuid-2>",
                    "<imaged-node-uuid-3>"
                ],
                "redundancy_factor": 2,
                "skip_cluster_creation": false,
                "storage_node_count": 0,
                "updated_timestamp": "2021-12-05T23:13:05.000-08:00",
                "workflow_type": "FOUNDATION_WORKFLOW"
            },
        ]

"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.fc.imaged_clusters import ImagedCluster  # noqa: E402


def get_module_spec():
    module_args = dict(
        imaged_cluster_uuid=dict(type="str"),
        filters=dict(
            type="dict", options=dict(archived=dict(type="bool", default=False))
        ),
        custom_filter=dict(type="dict"),
        offset=dict(type="int", default=0),
        length=dict(type="int", default=10),
    )

    return module_args


def list_clusters_nodes(module, result):
    imaged_cluster_uuid = module.params.get("imaged_cluster_uuid")
    list_imaged_clusters = ImagedCluster(module)

    if imaged_cluster_uuid:
        result["response"] = list_imaged_clusters.read(imaged_cluster_uuid)
    else:
        spec, error = list_imaged_clusters.get_spec()
        if error:
            result["error"] = error
            module.fail_json(msg="Failed generating Image Clusters Spec", **result)

        if module.check_mode:
            result["response"] = spec
            return

        resp = list_imaged_clusters.list(spec)
        result["response"] = resp
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    list_clusters_nodes(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
