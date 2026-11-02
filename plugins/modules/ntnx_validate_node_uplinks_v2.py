#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_validate_node_uplinks_v2
short_description: Validate hypervisor bundle and node uplinks before expanding a Nutanix cluster
version_added: 2.7.0
description:
    - This module validates hypervisor bundle compatibility or the network
      uplink configuration of target nodes before they are added to a Nutanix
      cluster.
    - The validation is performed against an existing Prism Element cluster
      referenced by C(cluster_ext_id).
    - C(spec) is a OneOf between C(bundle_param) (hypervisor-bundle validation)
      and C(uplink_nodes) (list of node uplink configurations). Exactly one
      must be provided.
    - The API is asynchronous. When C(wait) is true and C(spec.bundle_param) is
      used, the module polls the task and fetches the validated bundle info via
      C(fetchTaskResponse) with response type C(VALIDATE_BUNDLE_INFO). For
      C(spec.uplink_nodes), the module returns the completed task details.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Validate Cluster Node) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
      Project Manager, Super Admin, Self-Service Admin (deprecated)
    - This API is not supported for the C(XEN) hypervisor type.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will validate node uplinks or
              hypervisor bundle compatibility.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - External ID (UUID) of the target Prism Element cluster on which the
              validation is executed.
        type: str
        required: true
    spec:
        description:
            - Validate-node request body OneOf. Provide exactly one of
              C(bundle_param) or C(uplink_nodes).
        type: dict
        required: true
        suboptions:
            bundle_param:
                description:
                    - Hypervisor bundle validation spec.
                    - Provide this when validating hypervisor bundle (ISO)
                      compatibility against a list of target nodes.
                    - Mutually exclusive with C(uplink_nodes).
                type: dict
                required: false
                suboptions:
                    bundle_info:
                        description:
                            - Hypervisor bundle information used for validation.
                        type: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - Name of the hypervisor bundle (for example
                                      the ISO name).
                                type: str
                                required: false
                    node_list:
                        description:
                            - List of target node attributes to validate against
                              the hypervisor bundle.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            node_uuid:
                                description:
                                    - UUID of the node.
                                type: str
                                required: false
                            block_id:
                                description:
                                    - ID of the block that houses the node.
                                type: str
                                required: false
                            node_position:
                                description:
                                    - Position of the node within the block.
                                type: str
                                required: false
                            hypervisor_type:
                                description:
                                    - Hypervisor type running on the node.
                                    - The C(XEN) hypervisor type is not supported
                                      by the underlying validate-node API.
                                type: str
                                required: false
                                choices:
                                    - AHV
                                    - ESX
                                    - HYPERV
                                    - XEN
                                    - NATIVEHOST
                            hypervisor_hostname:
                                description:
                                    - Hypervisor hostname of the target node.
                                type: str
                                required: false
                            hypervisor_version:
                                description:
                                    - Hypervisor version of the target node.
                                type: str
                                required: false
                            nos_version:
                                description:
                                    - Nutanix Operating System (AOS) version
                                      running on the node.
                                type: str
                                required: false
                            is_light_compute:
                                description:
                                    - Whether the node is a light-compute node.
                                type: bool
                                required: false
                            is_robo_mixed_hypervisor:
                                description:
                                    - Whether the node is a mixed-hypervisor node
                                      in a ROBO deployment.
                                type: bool
                                required: false
                            model:
                                description:
                                    - Node hardware model.
                                type: str
                                required: false
                            current_network_interface:
                                description:
                                    - Name of the current network interface of the
                                      node.
                                type: str
                                required: false
                            ipmi_ip:
                                description:
                                    - IPMI IP address of the node.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description:
                                            - IPv4 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv4 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - Prefix length of the IPv4
                                                      address.
                                                    - Defaults to 32 on the server
                                                      if left unset.
                                                type: int
                                                required: false
                                    ipv6:
                                        description:
                                            - IPv6 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv6 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - Prefix length of the IPv6
                                                      address.
                                                    - Defaults to 128 on the
                                                      server if left unset.
                                                type: int
                                                required: false
                            cvm_ip:
                                description:
                                    - Controller VM (CVM) IP address of the node.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description:
                                            - IPv4 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv4 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - Prefix length of the IPv4
                                                      address.
                                                    - Defaults to 32 on the server
                                                      if left unset.
                                                type: int
                                                required: false
                                    ipv6:
                                        description:
                                            - IPv6 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv6 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - Prefix length of the IPv6
                                                      address.
                                                    - Defaults to 128 on the
                                                      server if left unset.
                                                type: int
                                                required: false
                            hypervisor_ip:
                                description:
                                    - Hypervisor IP address of the node.
                                type: dict
                                required: false
                                suboptions:
                                    ipv4:
                                        description:
                                            - IPv4 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv4 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - Prefix length of the IPv4
                                                      address.
                                                    - Defaults to 32 on the server
                                                      if left unset.
                                                type: int
                                                required: false
                                    ipv6:
                                        description:
                                            - IPv6 address.
                                        type: dict
                                        required: false
                                        suboptions:
                                            value:
                                                description:
                                                    - The IPv6 address value.
                                                type: str
                                                required: true
                                            prefix_length:
                                                description:
                                                    - Prefix length of the IPv6
                                                      address.
                                                    - Defaults to 128 on the
                                                      server if left unset.
                                                type: int
                                                required: false
                            digital_certificate_map_list:
                                description:
                                    - List of digital certificate mappings for the
                                      node.
                                type: list
                                elements: dict
                                required: false
                                suboptions:
                                    key:
                                        description:
                                            - Certificate map key.
                                        type: str
                                        required: false
                                    value:
                                        description:
                                            - Certificate map value.
                                        type: str
                                        required: false
            uplink_nodes:
                description:
                    - List of target nodes whose network uplink configuration
                      should be validated.
                    - Provide this when validating uplink connectivity of one or
                      more candidate nodes.
                    - Mutually exclusive with C(bundle_param).
                type: list
                elements: dict
                required: false
                suboptions:
                    cvm_ip:
                        description:
                            - Controller VM (CVM) IP address of the node to
                              validate.
                        type: dict
                        required: true
                        suboptions:
                            ipv4:
                                description:
                                    - IPv4 address.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description:
                                            - The IPv4 address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - Prefix length of the IPv4 address.
                                            - Defaults to 32 on the server if left
                                              unset.
                                        type: int
                                        required: false
                            ipv6:
                                description:
                                    - IPv6 address.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description:
                                            - The IPv6 address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - Prefix length of the IPv6 address.
                                            - Defaults to 128 on the server if
                                              left unset.
                                        type: int
                                        required: false
                    hypervisor_ip:
                        description:
                            - Hypervisor IP address of the node to validate.
                        type: dict
                        required: false
                        suboptions:
                            ipv4:
                                description:
                                    - IPv4 address.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description:
                                            - The IPv4 address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - Prefix length of the IPv4 address.
                                            - Defaults to 32 on the server if left
                                              unset.
                                        type: int
                                        required: false
                            ipv6:
                                description:
                                    - IPv6 address.
                                type: dict
                                required: false
                                suboptions:
                                    value:
                                        description:
                                            - The IPv6 address value.
                                        type: str
                                        required: true
                                    prefix_length:
                                        description:
                                            - Prefix length of the IPv6 address.
                                            - Defaults to 128 on the server if
                                              left unset.
                                        type: int
                                        required: false
                    networks:
                        description:
                            - Active and standby uplink information of the target
                              node grouped by uplink network name.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            name:
                                description:
                                    - Name of the uplink network (e.g. C(br0)).
                                type: str
                                required: false
                            networks:
                                description:
                                    - List of network names attached to the
                                      uplink.
                                type: list
                                elements: str
                                required: false
                            vswitch_ext_id:
                                description:
                                    - External ID of the virtual switch that the
                                      uplinks connect to.
                                type: str
                                required: false
                            uplinks:
                                description:
                                    - Active and standby uplink information for
                                      the network.
                                type: dict
                                required: false
                                suboptions:
                                    active:
                                        description:
                                            - Active uplink information.
                                        type: list
                                        elements: dict
                                        required: false
                                        suboptions:
                                            mac:
                                                description:
                                                    - MAC address of the uplink.
                                                type: str
                                                required: false
                                            name:
                                                description:
                                                    - Name of the uplink.
                                                type: str
                                                required: false
                                            value:
                                                description:
                                                    - Uplink value.
                                                type: str
                                                required: false
                                    standby:
                                        description:
                                            - Standby uplink information.
                                        type: list
                                        elements: dict
                                        required: false
                                        suboptions:
                                            mac:
                                                description:
                                                    - MAC address of the uplink.
                                                type: str
                                                required: false
                                            name:
                                                description:
                                                    - Name of the uplink.
                                                type: str
                                                required: false
                                            value:
                                                description:
                                                    - Uplink value.
                                                type: str
                                                required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Validate node uplinks before cluster expansion
  nutanix.ncp.ntnx_validate_node_uplinks_v2:
    cluster_ext_id: "0005b289-8340-119a-0000-00000000a31f"
    spec:
      uplink_nodes:
        - cvm_ip:
            ipv4:
              value: "10.44.76.31"
              prefix_length: 24
          hypervisor_ip:
            ipv4:
              value: "10.44.76.32"
              prefix_length: 24
          networks:
            - name: "br0"
              vswitch_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
              networks:
                - "Management"
              uplinks:
                active:
                  - mac: "1c:f4:7b:5f:a9:2a"
                    name: "eth1"
                    value: "eth1"
                standby:
                  - mac: "12:ee:23:33:2f:43"
                    name: "eth2"
                    value: "eth2"
  register: uplinks_validation
  ignore_errors: true

- name: Validate hypervisor bundle compatibility for a list of unconfigured nodes
  nutanix.ncp.ntnx_validate_node_uplinks_v2:
    cluster_ext_id: "0005b289-8340-119a-0000-00000000a31f"
    spec:
      bundle_param:
        bundle_info:
          name: "AHV-20220304.242.iso"
        node_list:
          - node_uuid: "54b7581b-2e35-413e-8608-0531b065a5d8"
            block_id: "18SM8B010159"
            node_position: "B"
            hypervisor_type: "AHV"
            hypervisor_version: "10.0-793"
            nos_version: "7.0"
            model: "NX-3060-G5"
            is_light_compute: false
            is_robo_mixed_hypervisor: false
            cvm_ip:
              ipv4:
                value: "10.44.76.31"
                prefix_length: 24
            hypervisor_ip:
              ipv4:
                value: "10.44.76.32"
                prefix_length: 24
            ipmi_ip:
              ipv4:
                value: "10.44.76.33"
                prefix_length: 24
  register: bundle_validation
  ignore_errors: true

- name: Validate node uplinks without waiting for task completion
  nutanix.ncp.ntnx_validate_node_uplinks_v2:
    cluster_ext_id: "0005b289-8340-119a-0000-00000000a31f"
    wait: false
    spec:
      uplink_nodes:
        - cvm_ip:
            ipv4:
              value: "10.44.76.31"
          networks:
            - name: "br0"
  register: uplinks_validation
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the validate-node action.
        - When C(wait) is C(true) and C(spec.bundle_param) is used, this contains
          the resolved task response from C(fetchTaskResponse) with
          C(taskResponseType=VALIDATE_BUNDLE_INFO).
        - When C(wait) is C(true) and C(spec.uplink_nodes) is used, this contains
          the final task payload after completion.
        - When C(wait) is C(false), this contains the initial task details.
        - When C(check_mode) is set, this contains the generated request spec.
    returned: always
    type: dict
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T13:25:19.252016+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T13:25:18.960093+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:e7e30d3b-ba3e-429f-7472-d1fff4c4304a",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T13:25:19.252015+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 0,
            "operation": "Validate Uplinks Info",
            "operation_description": "Validate Uplinks Info",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T13:25:18.985980+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
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
    sample: "Api Exception raised while validating node"

error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:e7e30d3b-ba3e-429f-7472-d1fff4c4304a"

ext_id:
    description: The external ID of the target Prism Element cluster on which the validation was performed.
    returned: always
    type: str
    sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
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
try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


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
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=clustermgmt_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            obj=clustermgmt_sdk.IPv6Address,
            required=False,
        ),
    )

    digital_certificate_map_list_spec = dict(
        key=dict(type="str", required=False, no_log=False),
        value=dict(type="str", required=False),
    )

    node_info_spec = dict(
        node_uuid=dict(type="str", required=False),
        block_id=dict(type="str", required=False),
        node_position=dict(type="str", required=False),
        hypervisor_type=dict(
            type="str",
            choices=["AHV", "ESX", "HYPERV", "XEN", "NATIVEHOST"],
            obj=clustermgmt_sdk.HypervisorType,
            required=False,
        ),
        hypervisor_hostname=dict(type="str", required=False),
        hypervisor_version=dict(type="str", required=False),
        nos_version=dict(type="str", required=False),
        is_light_compute=dict(type="bool", required=False),
        is_robo_mixed_hypervisor=dict(type="bool", required=False),
        model=dict(type="str", required=False),
        current_network_interface=dict(type="str", required=False),
        ipmi_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=clustermgmt_sdk.IPAddress,
            required=False,
        ),
        cvm_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=clustermgmt_sdk.IPAddress,
            required=False,
        ),
        hypervisor_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=clustermgmt_sdk.IPAddress,
            required=False,
        ),
        digital_certificate_map_list=dict(
            type="list",
            elements="dict",
            options=digital_certificate_map_list_spec,
            obj=clustermgmt_sdk.DigitalCertificateMapReference,
            required=False,
        ),
    )

    bundle_info_spec = dict(
        name=dict(type="str", required=False),
    )

    bundle_param_spec = dict(
        bundle_info=dict(
            type="dict",
            options=bundle_info_spec,
            obj=clustermgmt_sdk.BundleInfo,
            required=True,
        ),
        node_list=dict(
            type="list",
            elements="dict",
            options=node_info_spec,
            obj=clustermgmt_sdk.NodeInfo,
            required=True,
        ),
    )

    uplinks_field_spec = dict(
        mac=dict(type="str", required=False),
        name=dict(type="str", required=False),
        value=dict(type="str", required=False),
    )

    uplinks_spec = dict(
        active=dict(
            type="list",
            elements="dict",
            options=uplinks_field_spec,
            obj=clustermgmt_sdk.UplinksField,
            required=False,
        ),
        standby=dict(
            type="list",
            elements="dict",
            options=uplinks_field_spec,
            obj=clustermgmt_sdk.UplinksField,
            required=False,
        ),
    )

    uplink_network_item_spec = dict(
        name=dict(type="str", required=False),
        networks=dict(type="list", elements="str", required=False),
        vswitch_ext_id=dict(type="str", required=False),
        uplinks=dict(
            type="dict",
            options=uplinks_spec,
            obj=clustermgmt_sdk.Uplinks,
            required=False,
        ),
    )

    uplink_node_spec = dict(
        cvm_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=clustermgmt_sdk.IPAddress,
            required=True,
        ),
        hypervisor_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=clustermgmt_sdk.IPAddress,
            required=False,
        ),
        networks=dict(
            type="list",
            elements="dict",
            options=uplink_network_item_spec,
            obj=clustermgmt_sdk.UplinkNetworkItem,
            required=True,
        ),
    )

    spec_obj_map = {
        "bundle_param": clustermgmt_sdk.BundleParam,
        "uplink_nodes": clustermgmt_sdk.UplinkNode,
    }

    spec_options = dict(
        bundle_param=dict(
            type="dict",
            options=bundle_param_spec,
            required=False,
        ),
        uplink_nodes=dict(
            type="list",
            elements="dict",
            options=uplink_node_spec,
            required=False,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        spec=dict(
            type="dict",
            required=True,
            options=spec_options,
            obj=spec_obj_map,
            mutually_exclusive=[("bundle_param", "uplink_nodes")],
            required_one_of=[("bundle_param", "uplink_nodes")],
        ),
    )
    return module_args


def validate_node(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.ValidateNodeParam()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating validate-node spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.validate_node(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while validating node",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        if (module.params.get("spec") or {}).get("bundle_param"):
            if ":" in task_ext_id:
                task_ext_id = task_ext_id.split(":")[1]
            task_status = api_instance.fetch_task_response(
                extId=task_ext_id,
                taskResponseType="VALIDATE_BUNDLE_INFO",
            )
            result["response"] = strip_internal_attributes(task_status.data.to_dict())
        else:
            result["response"] = strip_internal_attributes(task_status.to_dict())


def run_module():
    module = BaseModuleV4(
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
        "failed": False,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_clusters_api_instance(module)
    validate_node(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
