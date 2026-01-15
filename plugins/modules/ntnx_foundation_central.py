#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central
short_description: Nutanix module to imaged Nodes and optionally create cluster
version_added: 1.1.0
description: 'Nutanix module to imaged Nodes and optionally create cluster'
options:
  imaged_cluster_uuid:
    description:
      - Cluster external IP
    type: str
  cluster_external_ip:
    description:
      - Cluster external IP
    type: str
    required: false
  storage_node_count:
    description:
      - Number of storage only nodes in the cluster. AHV iso for storage node will be taken from aos package.
    type: int
    required: false
  redundancy_factor:
    description:
      - Redundancy factor of the cluster.
    type: int
    required: true
  cluster_name:
    description:
      - Name of the cluster.
    type: str
    default: test
  aos_package_url:
    description:
      - URL to download AOS package. required only if imaging is needed.
    type: str
    required: true
  aos_package_sha256sum:
    description:
      - Sha256sum of AOS package.
    type: str
    required: false
  timezone:
    description:
      - Timezone to be set on the cluster.
    type: str
    required: false
  skip_cluster_creation:
    description:
    - skip cluster creation. Only imaging needed.
    type: bool
    default: false
  cluster_size:
    description:
      - Number of nodes in the cluster.
    type: int
    required: false
  common_network_settings:
    description:
      - Common network settings across the nodes in the cluster.
    type: dict
    required: true
    suboptions:
         cvm_dns_servers:
             description:
                - List of dns servers for the cvms in the cluster.
             type: list
             required: false
             elements: str
         hypervisor_dns_servers:
             description:
                - List of dns servers for the hypervisors in the cluster.
             type: list
             required: false
             elements: str
         cvm_ntp_servers:
             description:
                - List of ntp servers for the cvms in the cluster.
             type: list
             elements: str
             required: true
         hypervisor_ntp_servers:
             description:
                - List of ntp servers for the hypervisors in the cluster.
             type: list
             elements: str
             required: true
  hypervisor_iso_details:
    description:
      - Details of the hypervisor iso.
    type: dict
    required: false
    suboptions:
         hyperv_sku:
             description:
                - SKU of hyperv to be installed if hypervisor_type is hyperv.
             type: str
             required: false
         url:
             description:
                - URL to download hypervisor iso. required only if imaging is needed.
             type: str
             required: true
         hyperv_product_key:
             description:
                - Product key for hyperv isos. required only if the hypervisor type is hyperv and product key is mandatory.
             type: str
             required: false
         sha256sum:
             description:
                - sha256sum of the hypervisor iso
             type: str
             required: false
  nodes_list:
    description:
      - List of details of nodes out of which the cluster needs to be created.
    type: list
    elements : dict
    required: true
    suboptions:
        discovery_mode:
                        description:
                            - write
                        type: dict
                        suboptions:
                            node_serial:
                                description:
                                    - write
                                type: str
                                required: true
                            image_now:
                                description:
                                    - write
                                type: bool
                                default: true
                            discovery_override:
                                description:
                                    - write
                                type: dict
                                required: false
                                suboptions:
                                    hypervisor_hostname:
                                        description:
                                            - Name to be set for the hypervisor host.
                                        type: str
                                        required: false
                                    hypervisor_ip:
                                        description:
                                            - write
                                        type: str
                                        required: false
                                    cvm_ip:
                                        description:
                                            - IP address to be set for the cvm on the node.
                                        type: str
                                        required: false
                                    ipmi_ip:
                                        description:
                                            - IP address to be set for the ipmi of the node.
                                        type: str
                                        required: false
                                    imaged_node_uuid:
                                        description:
                                            - UUID of the node.
                                        type: str
                                        required: false
                                    ipmi_netmask:
                                        description:
                                            - Netmask of the ipmi.
                                        type: str
                                        required: false
                                    ipmi_gateway:
                                        description:
                                            - Gateway of the ipmi.
                                        type: str
                                    hardware_attributes_override:
                                        description:
                                            - Hardware attributes override json for the node.
                                        type: dict
        manual_mode:
            description:
                    - write
            type: dict
            suboptions:
                hypervisor_ip:
                    description:
                        - write
                    type: str
                    required: true
                cvm_gateway:
                    description:
                        - Gateway of the cvm.
                    type: str
                    required: true
                ipmi_netmask:
                    description:
                        - Netmask of the ipmi.
                    type: str
                    required: true
                rdma_passthrough:
                    description:
                        - Passthrough RDMA nic to CVM if possible, default to false.
                    type: bool
                    required: false
                    default: false
                imaged_node_uuid:
                    description:
                        - UUID of the node.
                    type: str
                    required: true
                cvm_vlan_id:
                    description:
                        - Vlan tag of the cvm, if the cvm is on a vlan.
                    type: int
                    required: false
                hypervisor_type:
                    description:
                        - Type of hypervisor to be installed.
                    type: str
                    required: true
                    choices:
                        - kvm
                        - esx
                        - hyperv
                image_now:
                    description:
                        - True, if the node should be imaged, False, otherwise.
                    type: bool
                    required: false
                    default: true
                hypervisor_hostname:
                    description:
                        - Name to be set for the hypervisor host.
                    type: str
                    required: true
                hypervisor_netmask:
                    description:
                        - Netmask of the hypervisor.
                    type: str
                    required: true
                cvm_netmask:
                    description:
                        - Netmask of the cvm.
                    type: str
                    required: true
                ipmi_ip:
                    description:
                        - IP address to be set for the ipmi of the node.
                    type: str
                    required: true
                hypervisor_gateway:
                    description:
                        - Gateway of the hypervisor.
                    type: str
                    required: true
                hardware_attributes_override:
                    description:
                        - Hardware attributes override json for the node.
                    type: dict
                cvm_ram_gb:
                    description:
                        - Amount of memory to be assigned for the cvm.
                    type: int
                    required: false
                cvm_ip:
                    description:
                        - IP address to be set for the cvm on the node.
                    type: str
                    required: true
                use_existing_network_settings:
                    description:
                        - Decides whether to use the existing network settings for the node. If True, the existing network settings of the node will
                          be used during cluster creation. If False, then client must provide new network settings. If all nodes are booted in phoenix,
                          this field is, by default, considered to be False.
                    type: bool
                    required: false
                    default: false
                ipmi_gateway:
                    description:
                        - Gateway of the ipmi.
                    type: str
                    required: true
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
- name: image nodes and create cluster
  ntnx_foundation_central:
    state: present
    nutanix_host: '{{ pc }}'
    nutanix_username: '{{ username }}'
    nutanix_password: '{{ password }}'
    validate_certs: false
    cluster_name: test-cls
    common_network_settings:
      cvm_dns_servers:
        - xx.xx.xx.xx
      hypervisor_dns_servers:
        - xx.xx.xx.xx
      cvm_ntp_servers:
        - xx.x.x.xx
      hypervisor_ntp_servers:
        - xx.x.x.xx
    nodes_list:
      # manual based nodes
      - manual_mode:
          cvm_gateway: 10.xx.xx.xx
          cvm_netmask: xx.xx.xx.xx
          cvm_ip: 10.x.xx.xx
          hypervisor_gateway: 10.x.xx.xxx
          hypervisor_netmask: xx.xx.xx.xx
          hypervisor_ip: 10.x.x.xx
          hypervisor_hostname: Host-1
          imaged_node_uuid: <node_uuid>
          use_existing_network_settings: false
          ipmi_gateway: 10.x.xx.xx
          ipmi_netmask: xx.xx.xx.xx
          ipmi_ip: 10.x.xx.xx
          image_now: true
          hypervisor_type: kvm
      - manual_mode:
          cvm_gateway: 10.xx.xx.xx
          cvm_netmask: xx.xx.xx.xx
          cvm_ip: 10.x.xx.xx
          hypervisor_gateway: 10.x.xx.xxx
          hypervisor_netmask: xx.xx.xx.xx
          hypervisor_ip: 10.x.x.xx
          hypervisor_hostname: Host-2
          imaged_node_uuid: <node_uuid>
          use_existing_network_settings: false
          ipmi_gateway: 10.x.xx.xx
          ipmi_netmask: xx.xx.xx.xx
          ipmi_ip: 10.x.xx.xx
          image_now: true
          hypervisor_type: kvm
      # discovery nodes based on node serial
      - discovery_mode:
          node_serial: <node-serial>
      - discovery_mode:
          node_serial: <node-serial>
          discovery_override:
            hypervisor_hostname: <host-11>
            cvm_ip: <cvm-ip>
            ipmi_ip: <ipmi-ip>
    redundancy_factor: 2
    skip_cluster_creation: true
    aos_package_url: <aos_package_url>
"""

RETURN = r"""
response:
  description: Sample response when only Imaging is done.
  returned: always
  type: dict
  sample: {
        "archived": false,
        "cluster_external_ip": "",
        "cluster_name": "test-cls",
        "cluster_size": 0,
        "cluster_status": {
            "aggregate_percent_complete": 100,
            "cluster_creation_started": true,
            "cluster_progress_details": {
                "message_list": null
            },
            "current_foundation_ip": "10.x.xx.xx",
            "foundation_session_id": "<session-id>",
            "imaging_stopped": true,
            "intent_picked_up": true,
            "node_progress_details": [
                {
                    "imaged_node_uuid": "<node-uuid-1>",
                    "imaging_stopped": true,
                    "intent_picked_up": true,
                    "message_list": [],
                    "percent_complete": 100,
                    "status": "All operations completed successfully"
                },
                {
                    "imaged_node_uuid": "<node-uuid-2>",
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
            "cvm_ntp_servers": [
                ""
            ],
            "hypervisor_dns_servers": [
                "10.x.xx.xx"
            ],
            "hypervisor_ntp_servers": [
                ""
            ]
        },
        "created_timestamp": "2022-04-26T03:25:02.000-07:00",
        "current_time": "2022-04-26T03:40:03.000-07:00",
        "destroyed": false,
        "foundation_init_config": {
            "blocks": [
                {
                    "block_id": "<block-id>",
                    "nodes": [
                        {
                            "cvm_ip": "10.x.xx.xx",
                            "fc_imaged_node_uuid": "<imaged-node-uuid>",
                            "hypervisor": "kvm",
                            "hypervisor_hostname": "HOST-1",
                            "hypervisor_ip": "10.x.xx.xx",
                            "image_now": false,
                            "ipmi_ip": "10.x.xx.xx",
                            "ipv6_address": "<node-ipv6-address>",
                            "node_position": "D",
                            "node_serial": "<node-serial>"
                        },
                        {
                            "cvm_ip": "10.x.xx.xx",
                            "fc_imaged_node_uuid": "<imaged-node-uuid>",
                            "hypervisor": "kvm",
                            "hypervisor_hostname": "HOST-2",
                            "hypervisor_ip": "10.x.xx.xx",
                            "image_now": false,
                            "ipmi_ip": "10.x.xx.xx",
                            "ipv6_address": "<node-ipv6-address>",
                            "node_position": "E",
                            "node_serial": "<node-serial>"
                        }
                    ]
                }
            ],
            "clusters": [],
            "cvm_gateway": "10.x.xx.xx",
            "cvm_netmask": "xx.xx.xx.xx",
            "dns_servers": "10.x.xx.xx",
            "hyperv_product_key": "",
            "hyperv_sku": "",
            "hypervisor_gateway": "10.x.xx.xx",
            "hypervisor_iso_url": {
                "hypervisor_type": "",
                "sha256sum": "",
                "url": ""
            },
            "hypervisor_isos": null,
            "hypervisor_netmask": "xx.xx.xx.xx",
            "ipmi_gateway": "10.x.xx.xx",
            "ipmi_netmask": "10.x.xx.xx",
            "nos_package_url": {
                "sha256sum": "",
                "url": "<url>"
            }
        },
        "foundation_init_node_uuid": "<foundation-uuid>",
        "imaged_cluster_uuid": "<imaged-cluster-uuid>",
        "imaged_node_uuid_list": [
            "<node-uuid-1>",
            "<node-uuid-2>"
        ],
        "redundancy_factor": 2,
        "skip_cluster_creation": true,
        "storage_node_count": 0,
        "updated_timestamp": "2022-04-26T03:36:02.000-07:00",
        "workflow_type": "FOUNDATION_WORKFLOW"
}
"""

import time  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v3.fc.imaged_clusters import ImagedCluster  # noqa: E402
from ..module_utils.v3.fc.imaged_nodes import ImagedNode  # noqa: E402


def get_module_spec():
    common_network_setting_spec_dict = dict(
        cvm_dns_servers=dict(type="list", elements="str"),
        hypervisor_dns_servers=dict(type="list", elements="str"),
        cvm_ntp_servers=dict(type="list", required=True, elements="str"),
        hypervisor_ntp_servers=dict(type="list", required=True, elements="str"),
    )

    hypervisor_iso_details_spec_dict = dict(
        hyperv_sku=dict(type="str", default=None),
        url=dict(type="str", required=True),
        hyperv_product_key=dict(type="str", default=None, no_log=True),
        sha256sum=dict(type="str", default=None),
    )

    manual_node_spec_dict = dict(
        cvm_gateway=dict(type="str", required=True),
        ipmi_netmask=dict(type="str", required=True),
        rdma_passthrough=dict(type="bool", default=False),
        imaged_node_uuid=dict(type="str", required=True),
        cvm_vlan_id=dict(type="int", default=None),
        hypervisor_type=dict(
            type="str", required=True, choices=["kvm", "esx", "hyperv"]
        ),
        image_now=dict(type="bool", default=True),
        hypervisor_hostname=dict(type="str", required=True),
        hypervisor_netmask=dict(type="str", required=True),
        cvm_netmask=dict(type="str", required=True),
        ipmi_ip=dict(type="str", required=True),
        hypervisor_gateway=dict(type="str", required=True),
        hardware_attributes_override=dict(type="dict", default=None),
        cvm_ram_gb=dict(type="int", default=None),
        cvm_ip=dict(type="str", required=True),
        hypervisor_ip=dict(type="str", required=True),
        use_existing_network_settings=dict(type="bool", default=False),
        ipmi_gateway=dict(type="str", required=True),
    )

    discovery_override = dict(
        hypervisor_hostname=dict(type="str", required=False),
        hypervisor_ip=dict(type="str", required=False),
        cvm_ip=dict(type="str", required=False),
        ipmi_ip=dict(type="str", required=False),
        imaged_node_uuid=dict(type="str", required=False),
        ipmi_netmask=dict(type="str", required=False),
        ipmi_gateway=dict(type="str", required=False),
        hardware_attributes_override=dict(type="dict", default=None),
    )

    node_mode_constraints = [("manual_mode", "discovery_mode")]

    discovery_mode_spec_dict = dict(
        node_serial=dict(type="str", required=True),
        image_now=dict(type="bool", default=True),
        discovery_override=dict(
            type="dict", required=False, options=discovery_override
        ),
    )
    node_modes = dict(
        manual_mode=dict(type="dict", options=manual_node_spec_dict),
        discovery_mode=dict(type="dict", options=discovery_mode_spec_dict),
    )

    module_args = dict(
        cluster_external_ip=dict(type="str", default=None),
        storage_node_count=dict(type="int", default=None),
        redundancy_factor=dict(type="int", required=True),
        cluster_name=dict(type="str", default="test"),
        aos_package_url=dict(type="str", required=True),
        cluster_size=dict(type="int", default=None),
        aos_package_sha256sum=dict(type="str", default=None),
        timezone=dict(type="str", default=None),
        common_network_settings=dict(
            type="dict", required=True, options=common_network_setting_spec_dict
        ),
        hypervisor_iso_details=dict(
            type="dict", options=hypervisor_iso_details_spec_dict
        ),
        nodes_list=dict(
            type="list",
            required=True,
            elements="dict",
            options=node_modes,
            mutually_exclusive=node_mode_constraints,
            required_one_of=node_mode_constraints,
        ),
        skip_cluster_creation=dict(type="bool", default=False),
        imaged_cluster_uuid=dict(type="str"),
    )

    return module_args


def imageNodes(module, result):
    imaging = ImagedCluster(module)
    spec, error = imaging.get_spec()
    if error:
        result["error"] = error
        module.fail_json(msg="Failed generating Image Nodes Spec", **result)

    if module.check_mode:
        result["response"] = spec
        return

    check_node_available(module, spec["nodes_list"], result)

    resp = imaging.create(spec)
    result["imaged_cluster_uuid"] = resp["imaged_cluster_uuid"]

    wait_till_imaging(module, result)


def check_node_available(module, nodes, result):
    av = ImagedNode(module)
    for node in nodes:
        node_detail = av.read(node["imaged_node_uuid"])
        node_state = node_detail["node_state"]
        if node_state != "STATE_AVAILABLE":
            avial, err = wait_till_node_available(
                module, node["imaged_node_uuid"], node_state
            )
            if err:
                result["error"] = err
                result["response"] = avial
                module.fail_json(
                    msg="Nodes not available or may be part of other cluster", **result
                )


def wait_till_node_available(module, node_uuid, node_state):
    timeout = time.time() + 1800
    delay = 60
    img = ImagedNode(module)
    while node_state != "STATE_AVAILABLE":
        node_detail = img.read(node_uuid)
        new_node_state = node_detail["node_state"]
        if new_node_state != "STATE_AVAILABLE":
            if time.time() > timeout:
                return (None, "Timeout. Node is in {0}\n".format(new_node_state))
            time.sleep(delay)
        else:
            node_state = new_node_state

    return node_state, None


def wait_till_imaging(module, result):
    imaged_cluster_uuid = result["imaged_cluster_uuid"]
    resp, err = wait_for_completion(module, imaged_cluster_uuid)
    result["response"] = resp
    if err:
        result["error"] = err
        result["response"] = resp
        module.fail_json(msg="Failed to image nodes", **result)
    result["changed"] = True


def wait_for_completion(module, uuid):
    state = ""
    delay = 30
    time.sleep(15 * 60)
    timeout = time.time() + (3 * 60 * 60)
    progress = ImagedCluster(module)
    while state != "COMPLETED":
        response = progress.read(uuid)
        stopped = response["cluster_status"]["imaging_stopped"]
        aggregate_percent_complete = response["cluster_status"][
            "aggregate_percent_complete"
        ]
        if stopped:
            if aggregate_percent_complete < 100:
                status = _get_progress_error_status(response)
                return response, status
            state = "COMPLETED"
        else:
            state = "PENDING"
            if time.time() > timeout:
                return (
                    None,
                    "Failed to poll on image node progress. Reason: Timeout",
                )
            time.sleep(delay)
    return response, None


def _get_progress_error_status(progress):
    return "Imaging stopped before completion.\nClusters: {0}\nNodes: {1}".format(
        _get_cluster_progress_messages(
            progress, "cluster_progress_details", "cluster_name"
        ),
        _get_node_progress_messages(
            progress, "node_progress_details", "imaged_node_uuid"
        ),
    )


def _get_cluster_progress_messages(progress, entity_type, entity_name):
    res = ""
    cluster = progress["cluster_status"][entity_type]
    if cluster is not None:
        if cluster.get(entity_name):
            res += "cluster_name: {0}\n".format(cluster[entity_name])
        if cluster.get("status"):
            res += "status:\n{0}\n".format(cluster["status"])

    return res


def _get_node_progress_messages(progress, entity_type, entity_name):
    res = ""
    nodes = progress["cluster_status"][entity_type]
    if nodes:
        for c in nodes:
            res += "node_uuid: {0}\n".format(c[entity_name])
            res += "status:\n{0}\n".format(c["status"])
    return res


def deleteCluster(module, result):
    cluster_uuid = module.params.get("imaged_cluster_uuid")
    cluster = ImagedCluster(module)

    if module.check_mode:
        result["imaged_cluster_uuid"] = cluster_uuid
        result["msg"] = "Cluster with uuid:{0} will be deleted.".format(cluster_uuid)
        return

    resp = cluster.delete(cluster_uuid, no_response=True)
    result["response"] = resp
    result["imaged_cluster_uuid"] = cluster_uuid
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("nodes_list",)),
            ("state", "absent", ("imaged_cluster_uuid",)),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "imaged_cluster_uuid": None,
    }
    state = module.params["state"]
    if state == "present":
        imageNodes(module, result)
    elif state == "absent":
        deleteCluster(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
