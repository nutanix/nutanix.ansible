#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_clusters_nodes_v2
short_description: Add or Remove nodes from cluster using Nutanix PC
description:
  - This module allows you to manage Nutanix cluster nodes.
version_added: "2.0.0"
options:
  node_params:
    description:
      - parameters for adding or removing cluster nodes.
    type: dict
    suboptions:
      block_list:
        description:
          - List of blocks to which the nodes belong.
        type: list
        elements: dict
        suboptions:
          block_id:
            description: ID of the block.
            type: str
            required: false
          rack_name:
            description: Name of the rack.
            type: str
            required: false
      node_list:
        description:
          - List of nodes to be added or removed.
        type: list
        elements: dict
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
          hypervisor_hostname:
            description: Hostname of the hypervisor.
            type: str
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
            description: IP address for IPMI.
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
            description: IP address for CVM.
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
            description: IP address for the hypervisor.
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
          networks:
            description: List of networks for the node.
            type: list
            elements: dict
            suboptions:
              name:
                description: Name of the network.
                type: str
              networks:
                description: List of network names.
                type: list
                elements: str
              uplinks:
                description: uplink information.
                type: dict
                suboptions:
                  active:
                    description: List of active uplinks.
                    type: list
                    elements: dict
                    suboptions:
                      mac:
                        description: MAC address of the uplink.
                        type: str
                      name:
                        description: Name of the uplink.
                        type: str
                      value:
                        description: Value of the uplink.
                        type: str
                  standby:
                    description: List of standby uplinks.
                    type: list
                    elements: dict
                    suboptions:
                      mac:
                        description: MAC address of the uplink.
                        type: str
                      name:
                        description: Name of the uplink.
                        type: str
                      value:
                        description: Value of the uplink.
                        type: str
            required: false
      compute_node_list:
        description:
          - List of compute nodes to be added or removed.
        type: list
        elements: dict
        suboptions:
          node_uuid:
            description: UUID of the compute node.
            type: str
            required: false
          block_id:
            description: ID of the block to which the compute node belongs.
            type: str
            required: false
          node_position:
            description: Position of the compute node.
            type: str
            required: false
          hypervisor_ip:
            description: IP address for the hypervisor.
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
          ipmi_ip:
            description: IP address for IPMI.
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
          hypervisor_hostname:
            description: Hostname of the hypervisor.
            type: str
            required: false
          model:
            description: Model of the compute node.
            type: str
            required: false
      hyperv_sku:
            description: write
            type: str
      bundle_info:
            description: write
            type: dict
            suboptions:
              name:
                description: write
                type: str
      should_skip_host_networking:
            description: write
            type: bool
      hypervisor_isos:
        description:
          - List of hypervisor ISOs.
        type: list
        elements: dict
        suboptions:
          type:
            description: Type of the hypervisor.
            type: str
            choices: ['AHV', 'ESX', 'HYPERV', 'XEN', 'NATIVEHOST']
          md5_sum:
            description: MD5 sum of the ISO.
            type: str
    required: false
  config_params:
    description:
      - configuration parameters.
    type: dict
    suboptions:
      should_skip_discovery:
        description: Whether to skip the discovery process.
        type: bool
        required: false
      should_skip_imaging:
        description: Whether to skip the imaging process.
        type: bool
        required: false
      should_validate_rack_awareness:
        description: Whether to validate rack awareness.
        type: bool
        required: false
      is_nos_compatible:
        description: Whether the nodes are compatible with the Nutanix Operating System (NOS).
        type: bool
        required: false
      is_compute_only:
        description: Whether the nodes are compute-only nodes.
        type: bool
        required: false
      is_never_scheduleable:
        description: Whether the nodes are never scheduleable.
        type: bool
        required: false
      target_hypervisor:
        description: Target hypervisor for the nodes.
        type: str
        required: false
      hyperv:
        description: hyper-v credentials.
        type: dict
        suboptions:
          domain_details:
            description: domain details.
            type: dict
            suboptions:
              username:
                description: Username for the domain.
                type: str
              password:
                description: Password for the domain.
                type: str
              cluster_name:
                description: Name of the cluster.
                type: str
            required: false
          failover_cluster_details:
            description: failover cluster details.
            type: dict
            suboptions:
              username:
                description: Username for the failover cluster.
                type: str
              password:
                description: Password for the failover cluster.
                type: str
              cluster_name:
                description: Name of the cluster.
                type: str
            required: false
    required: false
  should_skip_add_node:
    description: Whether to skip adding nodes.
    type: bool
    required: false
  should_skip_pre_expand_checks:
    description: Whether to skip pre-expand checks.
    type: bool
    required: false
  cluster_ext_id:
    description: External ID of the cluster.
    type: str
    required: true
  should_skip_prechecks:
    description: Whether to skip pre-checks.
    type: bool
    required: false
  should_skip_remove:
    description: Whether to skip removing nodes.
    type: bool
    required: false
  node_uuids:
    description: List of UUIDs of the nodes to be removed.
    type: list
    elements: str
    required: false
  extra_params:
    description:
      - extra parameters.
    type: dict
    suboptions:
      should_skip_upgrade_check:
        description: Whether to skip the upgrade check.
        type: bool
        required: false
      should_skip_space_check:
        description: Whether to skip the space check.
        type: bool
        required: false
      should_skip_add_check:
        description: Whether to skip the add check.
        type: bool
        required: false
    required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Prem Karat (@premkarat)
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Expand cluster
  ntnx_clusters_nodes_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "000628e4-4c8f-1239-5575-0cc47a9a3e6d"
    node_params:
      node_list:
        - block_id: "18SM8B010159"
          current_network_interface: "eth1"
          cvm_ip:
            ipv4:
              prefix_length: 32
              value: "10.0.0.1"
          hypervisor_hostname: "test"
          hypervisor_ip:
            ipv4:
              prefix_length: 32
              value: "10.0.0.2"
          hypervisor_type: "AHV"
          hypervisor_version: "10.0-793"
          ipmi_ip:
            ipv4:
              prefix_length: 32
              value: "10.0.0.3"
          is_light_compute: false
          is_robo_mixed_hypervisor: true
          model: "NX-3060-G5"
          networks:
            - name: "br0"
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
          node_position: "B"
          node_uuid: "54b7581b-2e35-413e-8608-0531b065a5d8"
          nos_version: "7.0"
    config_params:
      is_compute_only: false
      is_never_scheduleable: false
      is_nos_compatible: false
      should_skip_discovery: false
      should_skip_imaging: true
  register: result

- name: Remove node from cluster
  ntnx_clusters_nodes_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "000628e4-4c8f-1239-5575-0cc47a9a3e6d"
    node_uuids:
      - "54b7581b-2e35-413e-8608-0531b065a5d8"
  register: result
"""

RETURN = r"""
response:
  description: Task response for adding or removing cluster nodes.
  type: dict
  returned: always
  sample:
    {
      "cluster_ext_ids": [
          "000628e4-4c8f-1239-5575-0cc47a9a3e6d"
      ],
      "completed_time": "2024-12-10T06:26:48.551062+00:00",
      "completion_details": null,
      "created_time": "2024-12-10T06:17:52.467169+00:00",
      "entities_affected": [
          {
              "ext_id": "000628e4-4c8f-1239-5575-0cc47a9a3e6d",
              "name": null,
              "rel": "clustermgmt:config:cluster"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:a2734e72-f034-49de-a3c8-d50e2dbaf44a",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2024-12-10T06:26:48.551061+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 1,
      "operation": "Expand Cluster",
      "operation_description": "Expand Cluster",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2024-12-10T06:17:52.492332+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": [
          {
              "ext_id": "ZXJnb24=:74cb5bb6-f888-4c4a-7c99-74d95d76443a",
              "href": "https://10.44.76.117:9440/api/prism/v4.0/config/tasks/ZXJnb24=:74cb5bb6-f888-4c4a-7c99-74d95d76443a",
              "rel": "subtask"
          }
      ],
      "warnings": null
    }
task_ext_id:
  description: The external ID of the task.
  type: str
  returned: always
ext_id:
  description: The external ID of the cluster.
  type: str
  returned: always
changed:
  description: Whether the state of the cluster nodes has changed.
  type: bool
  returned: always
error:
  description: The error message, if any.
  type: str
  returned: on error
cluster_ext_id:
  description: The external ID of the cluster.
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
    block_list_spec = dict(
        block_id=dict(type="str", required=False),
        rack_name=dict(type="str", required=False),
    )
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
    uplinks_types_spec = dict(
        mac=dict(type="str", required=False),
        name=dict(type="str", required=False),
        value=dict(type="str", required=False),
    )
    uplinks_spec = dict(
        active=dict(
            type="list",
            elements="dict",
            options=uplinks_types_spec,
            obj=clustermgmt_sdk.UplinksField,
            required=False,
        ),
        standby=dict(
            type="list",
            elements="dict",
            options=uplinks_types_spec,
            obj=clustermgmt_sdk.UplinksField,
            required=False,
        ),
    )
    networks_spec = dict(
        name=dict(type="str", required=False),
        networks=dict(type="list", elements="str", required=False),
        uplinks=dict(
            type="dict",
            options=uplinks_spec,
            obj=clustermgmt_sdk.Uplinks,
            required=False,
        ),
    )
    node_list_spec = dict(
        node_uuid=dict(type="str", required=False),
        block_id=dict(type="str", required=False),
        node_position=dict(type="str", required=False),
        hypervisor_type=dict(
            type="str",
            choices=["AHV", "ESX", "HYPERV", "XEN", "NATIVEHOST"],
            obj=clustermgmt_sdk.HypervisorType,
            required=False,
        ),
        is_robo_mixed_hypervisor=dict(type="bool", required=False),
        hypervisor_hostname=dict(type="str", required=False),
        hypervisor_version=dict(type="str", required=False),
        nos_version=dict(type="str", required=False),
        is_light_compute=dict(type="bool", required=False),
        ipmi_ip=dict(
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
        model=dict(type="str", required=False),
        current_network_interface=dict(type="str", required=False),
        networks=dict(
            type="list",
            elements="dict",
            options=networks_spec,
            obj=clustermgmt_sdk.UplinkNetworkItem,
            required=False,
        ),
    )
    compute_node_list_spec = dict(
        node_uuid=dict(type="str", required=False),
        block_id=dict(type="str", required=False),
        node_position=dict(type="str", required=False),
        hypervisor_ip=dict(type="dict", options=ip_address_spec, required=False),
        ipmi_ip=dict(type="dict", options=ip_address_spec, required=False),
        digital_certificate_map_list=dict(
            type="list",
            elements="dict",
            options=digital_certificate_map_list_spec,
            required=False,
        ),
        hypervisor_hostname=dict(type="str", required=False),
        model=dict(type="str", required=False),
    )
    hypervisor_isos_spec = dict(
        type=dict(
            type="str",
            choices=["AHV", "ESX", "HYPERV", "XEN", "NATIVEHOST"],
            required=False,
        ),
        md5_sum=dict(type="str", required=False),
    )
    bundle_info_spec = dict(
        name=dict(type="str", required=False),
    )

    node_params_spec = dict(
        block_list=dict(
            type="list",
            elements="dict",
            options=block_list_spec,
            obj=clustermgmt_sdk.BlockItem,
            required=False,
        ),
        node_list=dict(
            type="list",
            elements="dict",
            options=node_list_spec,
            obj=clustermgmt_sdk.NodeItem,
            required=False,
        ),
        compute_node_list=dict(
            type="list",
            elements="dict",
            options=compute_node_list_spec,
            obj=clustermgmt_sdk.ComputeNodeItem,
            required=False,
        ),
        hypervisor_isos=dict(
            type="list",
            elements="dict",
            options=hypervisor_isos_spec,
            obj=clustermgmt_sdk.HypervisorIsoMap,
            required=False,
        ),
        hyperv_sku=dict(type="str", required=False),
        bundle_info=dict(
            type="dict",
            options=bundle_info_spec,
            obj=clustermgmt_sdk.BundleInfo,
            required=False,
        ),
        should_skip_host_networking=dict(type="bool", required=False),
    )
    user_info_spec = dict(
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=False),
        cluster_name=dict(type="str", required=False),
    )
    hyperv_spec = dict(
        domain_details=dict(type="dict", options=user_info_spec, required=False),
        failover_cluster_details=dict(
            type="dict", options=user_info_spec, required=False
        ),
    )
    config_params_spec = dict(
        should_skip_discovery=dict(type="bool", required=False),
        should_skip_imaging=dict(type="bool", required=False),
        should_validate_rack_awareness=dict(type="bool", required=False),
        is_nos_compatible=dict(type="bool", required=False),
        is_compute_only=dict(type="bool", required=False),
        is_never_scheduleable=dict(type="bool", required=False),
        target_hypervisor=dict(type="str", required=False),
        hyperv=dict(type="dict", options=hyperv_spec, required=False),
    )
    extra_params_spec = dict(
        should_skip_upgrade_check=dict(type="bool", required=False),
        should_skip_space_check=dict(type="bool", required=False),
        should_skip_add_check=dict(type="bool", required=False),
    )
    module_args = dict(
        node_params=dict(
            type="dict",
            options=node_params_spec,
            obj=clustermgmt_sdk.NodeParam,
            required=False,
        ),
        config_params=dict(
            type="dict",
            options=config_params_spec,
            obj=clustermgmt_sdk.ConfigParams,
            required=False,
        ),
        should_skip_add_node=dict(type="bool", required=False),
        should_skip_pre_expand_checks=dict(type="bool", required=False),
        cluster_ext_id=dict(type="str", required=True),
        should_skip_prechecks=dict(type="bool", required=False),
        should_skip_remove=dict(type="bool", required=False),
        node_uuids=dict(type="list", elements="str", required=False),
        extra_params=dict(
            type="dict",
            options=extra_params_spec,
            obj=clustermgmt_sdk.NodeRemovalExtraParam,
            required=False,
        ),
    )
    return module_args


def add_cluster_node(module, cluster_node_api, result):
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.ExpandClusterParams()
    spec, err = sg.generate_spec(default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for adding cluster node", **result)
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    resp = None

    try:
        resp = cluster_node_api.expand_cluster(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while expanding cluster",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["changed"] = True


def remove_cluster_node(module, cluster_node_api, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.NodeRemovalParams()
    spec, err = sg.generate_spec(default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for removing cluster node", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = cluster_node_api.remove_node(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while removing node",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("node_params",)),
            ("state", "absent", ("node_uuids",)),
        ],
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
        "ext_id": None,
    }
    state = module.params.get("state")
    cluster_node_api = get_clusters_api_instance(module)
    if state == "present":
        add_cluster_node(module, cluster_node_api, result)
    elif state == "absent":
        remove_cluster_node(module, cluster_node_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
