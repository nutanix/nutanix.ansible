DOCUMENTATION = r"""
---
module: ntnx_foundation_central_imaged_nodes_info
short_description: Nutanix module which returns the imaged nodes within the Foudation Central
version_added: 1.1.0
description: 'List all the imaged nodes created in Foundation Central.'
options:
  nutanix_host:
    description:
      - Foundation VM hostname or IP address
    type: str
    required: true
  nutanix_port:
    description:
      - PC port
    type: str
    default: 8000
    required: false
  imaged_node_uuid:
    description:
      - Return the node details given it's uuid
    type: str
    required: false
    default: None
  length:
    description:
      - Return the list of imaged nodes upto the length or by default 10.
    type: int
    required: false
    default: 10
  offset:
    description:
      - Returns the list of imaged nodes starting with offset index.
    type: int
    required: false
    default: 0
  filters:
    description:
      - Returns the list of imaged nodes based on node state
    type: dict
    required: false
    suboptions:
        node_state:
            description:
              - Returns the nodes list given its node state
            type: str
            choices:
                - STATE_AVAILABLE
                - STATE_UNAVAILABLE
                - STATE_DISCOVERING
                - STATE_IMAGING
            required: false
            default: false
    default: None

author:
 - Abhishek Chaudhary (@abhimutant)
"""

EXAMPLES = r"""
  - name: Get node details using uuid
    ntnx_foundation_central_imaged_nodes_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      imaged_node_uuid: "{{node_uuid}}"

  - name: Get imaged node list based on filters
    ntnx_foundation_central_imaged_nodes_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      filters:
        node_state: STATE_AVAILABLE
      length: 5
      offset: 1
"""

RETURN = r"""
Imaged_Node_List
  description: Imaged Node list within Foundation Central
  return:  true
  type: list
  "imaged_nodes": [
            {
                "aos_version": "6.1",
                "api_key_uuid": "<api-key-uuid>",
                "available": false,
                "block_serial": "<block_serial>",
                "created_timestamp": "2021-12-05T22:59:02.000-08:00",
                "current_time": "2022-04-25T11:58:51.000-07:00",
                "cvm_gateway": "10.x.xx.xx",
                "cvm_ip": "10.x.xx.xx",
                "cvm_ipv6": "<ipv6>",
                "cvm_netmask": "xx.xx.xx.xx",
                "cvm_up": true,
                "cvm_uuid": "<cvm-uuid>",
                "cvm_vlan_id": 0,
                "foundation_version": "5.1",
                "hardware_attributes": {
                    "default_workload": "vdi",
                    "is_xpress_node": true,
                    "lcm_family": "<lcm-family>",
                    "maybe_1GbE_only": true,
                    "robo_mixed_hypervisor": true
                },
                "hypervisor_gateway": "10.x.xx.xx",
                "hypervisor_hostname": "KENOBI8-1",
                "hypervisor_ip": "10.x.xx.xx",
                "hypervisor_netmask": "xx.xx.xx.xx",
                "hypervisor_type": "kvm",
                "hypervisor_version": "<hypervisor-version>",
                "imaged_cluster_uuid": "<imaged-cluster-uuid>",
                "imaged_node_uuid": "<imaged-node-uuid>",
                "ipmi_gateway": "10.x.xx.xx",
                "ipmi_ip": "10.x.xx.xx",
                "ipmi_netmask": "xx.xx.xx.xx",
                "ipv6_interface": "eth0",
                "latest_hb_ts_list": [],
                "model": "<model>",
                "node_position": "A",
                "node_serial": "<node-serial>",
                "node_state": "STATE_UNAVAILABLE",
                "node_type": "on-prem",
                "object_version": 26,
                "supported_features": [
                    "API_KEY_DELETION",
                    "AHV_ISO_URL"
                ]
            }
        ],
        "metadata": {
            "length": 1,
            "total_matches": 1
        }
    }

"""

from __future__ import absolute_import, division, print_function

from ..module_utils.base_module import BaseModule
from ..module_utils.fc.imaged_nodes import ImagedNode
from ..module_utils.utils import remove_param_with_none_value


def get_module_spec():
    module_args = dict(
        imaged_node_uuid=dict(type="str"),
        filters=dict(
            type="dict",
            node_state=dict(
                type="str",
                choices=[
                    "STATE_AVAILABLE",
                    "STATE_UNAVAILABLE",
                    "STATE_DISCOVERING",
                    "STATE_IMAGING",
                ],
                default=None,
            ),
        ),
        custom_filter=dict(type="dict"),
    )

    return module_args


def list_imaged_nodes(module, result):
    imaged_node_uuid = module.params.get("imaged_node_uuid")
    list_imaged_nodes = ImagedNode(module)

    if imaged_node_uuid:
        result["imaged_node_details"] = list_imaged_nodes.read(imaged_node_uuid)
    else:
        spec, error = list_imaged_nodes.get_spec()
        if error:
            result["error"] = error
            module.fail_json(msg="Failed generating Image Nodes Spec", **result)

        if module.check_mode:
            result["response"] = spec
            return

        resp = list_imaged_nodes.list(spec)
        result["imaged_node_details"] = resp

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
    list_imaged_nodes(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
