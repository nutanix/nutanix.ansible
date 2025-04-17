#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_nodes_network_info_v2
short_description: Get netowrk information for uncofigured cluster nodes
description:
  - This module allows you to Get netowrk information for uncofigured cluster nodes.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster.
    type: str
    required: true
  request_type:
    description:
        - Type of request, either it can be expand_cluster or npe.
    type: str
  node_list:
        description:
          - List of nodes to be added or removed.
        type: list
        elements: dict
        required: true
        suboptions:
          node_uuid:
            description: UUID of the node.
            type: str
            required: false
          block_id:
            description: ID of the block to which the node belongs.
            type: str
            required: false
          node_position:
            description: Position of the node.
            type: str
            required: false
          hypervisor_type:
            description: Type of the hypervisor.
            type: str
            choices: ['AHV', 'ESX', 'HYPERV', 'XEN', 'NATIVEHOST']
            required: false
          is_robo_mixed_hypervisor:
            description: Whether the node is a mixed hypervisor in a ROBO deployment.
            type: bool
            required: false
          hypervisor_version:
            description: Version of the hypervisor.
            type: str
            required: false
          nos_version:
            description: Version of the Nutanix Operating System (NOS).
            type: str
            required: false
          is_light_compute:
            description: Whether the node is a light compute node.
            type: bool
            required: false
          ipmi_ip:
            description: List of IP addresses for IPMI.
            type: dict
            suboptions:
              ipv4:
                description: IPv4 address.
                type: dict
                suboptions:
                  value:
                    description: IP address.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the IP address.
                    type: int
                    required: false
              ipv6:
                description: IPv6 address.
                type: dict
                suboptions:
                  value:
                    description: IP address.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the IP address.
                    type: int
                    required: false
            required: false
          digital_certificate_map_list:
            description: List of digital certificates.
            type: list
            elements: dict
            suboptions:
              key:
                description: Key of the digital certificate.
                type: str
              value:
                description: Value of the digital certificate.
                type: str
            required: false
          cvm_ip:
            description: List of IP addresses for CVM.
            type: dict
            suboptions:
              ipv4:
                description: IPv4 address.
                type: dict
                suboptions:
                  value:
                    description: IP address.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the IP address.
                    type: int
                    required: false
              ipv6:
                description: IPv6 address.
                type: dict
                suboptions:
                  value:
                    description: IP address.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the IP address.
                    type: int
                    required: false
            required: false
          hypervisor_ip:
            description: List of IP addresses for the hypervisor.
            type: dict
            suboptions:
              ipv4:
                description: IPv4 address.
                type: dict
                suboptions:
                  value:
                    description: IP address.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the IP address.
                    type: int
                    required: false
              ipv6:
                description: IPv6 address.
                type: dict
                suboptions:
                  value:
                    description: IP address.
                    type: str
                    required: true
                  prefix_length:
                    description: Prefix length of the IP address.
                    type: int
                    required: false
            required: false
          model:
            description: Model of the node.
            type: str
            required: false
          current_network_interface:
            description: Current network interface of the node.
            type: str
            required: false
          is_compute_only:
            description: Indicates whether the node is compute only or not.
            type: bool
            required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get network information for uncofigured cluster nodes
  nutanix.ncp.ntnx_nodes_network_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: 00061de6-1234-4321-1122-ac1f6b6f97e2
    node_list:
      - cvm_ip:
          ipv4:
            value: "10.0.0.1"
        hypervisor_ip:
          ipv4:
            value: "10.0.0.2"
    request_type: "expand_cluster"
"""

RETURN = r"""
response:
    description:
        - Response for getting network information for uncofigured cluster nodes.
    type: dict
    returned: always
    sample:
      {
        "ext_id": "54fbdaf3-972d-4d1c-4413-005a9fe1fc1d",
        "links": null,
        "response": {
            "network_info": {
                "hci": [
                    {
                        "hypervisor_type": "AHV",
                        "name": "br0",
                        "networks": [
                            "Management"
                        ]
                    }
                ],
                "so": [
                    {
                        "hypervisor_type": "AHV",
                        "name": "br0",
                        "networks": [
                            "Management"
                        ]
                    }
                ]
            },
            "uplinks": [
                {
                    "cvm_ip": {
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "10.39.6.77"
                        },
                        "ipv6": null
                    },
                    "uplink_list": [
                        {
                            "mac": "00:e0:ed:36:41:a8",
                            "name": "eth2"
                        },
                        {
                            "mac": "0c:c4:7a:c7:c2:0b",
                            "name": "eth1"
                        },
                        {
                            "mac": "00:e0:ed:36:41:a9",
                            "name": "eth3"
                        },
                        {
                            "mac": "0c:c4:7a:c7:c2:0a",
                            "name": "eth0"
                        }
                    ]
                }
            ],
            "warnings": null
        },
        "task_response_type": "NETWORKING_DETAILS",
        "tenant_id": null
      }
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs

cluster_ext_id:
    description: The external ID of the cluster.
    type: str
    returned: always

task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always

"""


import traceback  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ipv4_spec, obj=clustermgmt_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ipv6_spec, obj=clustermgmt_sdk.IPv6Address),
    )

    digital_certificate_map_list_spec = dict(
        key=dict(type="str", required=False, no_log=False),
        value=dict(type="str", required=False),
    )

    node_spec = dict(
        node_uuid=dict(type="str", required=False),
        block_id=dict(type="str", required=False),
        node_position=dict(type="str", required=False),
        cvm_ip=dict(
            type="dict", options=ip_address_spec, obj=clustermgmt_sdk.IPAddress
        ),
        hypervisor_ip=dict(
            type="dict", options=ip_address_spec, obj=clustermgmt_sdk.IPAddress
        ),
        ipmi_ip=dict(
            type="dict", options=ip_address_spec, obj=clustermgmt_sdk.IPAddress
        ),
        digital_certificate_map_list=dict(
            type="list",
            elements="dict",
            options=digital_certificate_map_list_spec,
            obj=clustermgmt_sdk.DigitalCertificateMapReference,
        ),
        model=dict(type="str", required=False),
        is_compute_only=dict(type="bool", required=False),
        is_light_compute=dict(type="bool", required=False),
        hypervisor_type=dict(
            type="str",
            choices=["AHV", "ESX", "HYPERV", "XEN", "NATIVEHOST"],
            obj=clustermgmt_sdk.HypervisorType,
            required=False,
        ),
        hypervisor_version=dict(type="str", required=False),
        nos_version=dict(type="str", required=False),
        current_network_interface=dict(type="str", required=False),
        is_robo_mixed_hypervisor=dict(type="bool", required=False),
    )
    module_args = dict(
        node_list=dict(
            type="list",
            elements="dict",
            options=node_spec,
            obj=clustermgmt_sdk.NodeListNetworkingDetails,
            required=True,
        ),
        cluster_ext_id=dict(type="str", required=True),
        request_type=dict(type="str"),
    )
    return module_args


def get_nodes_network_information(module, cluster_node_api, result):
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.NodeDetails()
    spec, err = sg.generate_spec(default_spec)
    if err:
        result["error"] = err
        msg = "Failed generating spec for getting network information for cluster nodes"
        module.fail_json(msg=msg, **result)
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    resp = None
    try:
        resp = cluster_node_api.fetch_node_networking_details(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while getting network information for cluster nodes",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        if ":" in task_ext_id:
            task_ext_id = task_ext_id.split(":")[1]
        task_status = cluster_node_api.fetch_task_response(
            extId=task_ext_id, taskResponseType="NETWORKING_DETAILS"
        )
        result["response"] = strip_internal_attributes(task_status.data.to_dict())


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }
    cluster_node_api = get_clusters_api_instance(module)
    get_nodes_network_information(module, cluster_node_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
