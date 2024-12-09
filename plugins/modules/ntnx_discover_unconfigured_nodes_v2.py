#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_discover_unconfigured_nodes_v2
short_description: Discover unconfigured nodes from Nutanix Prism Central
description:
  - Discover unconfigured nodes from Nutanix Prism Central.
version_added: "2.0.0"
options:
  address_type:
    description:
      - Specifies the type of address, either IPv4 or IPv6.
    type: str
    choices:
      - IPV4
      - IPV6
  ip_filter_list:
    description:
      - IP addresses of the unconfigured nodes.
    type: list
    elements: dict
    suboptions:
      ipv4:
        description:
          - Configuration for IPv4 address.
        type: dict
        suboptions:
          value:
            description:
              - The IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix length of the IPv4 address.
            type: int
            required: false
      ipv6:
        description:
          - Configuration for IPv6 address.
        type: dict
        suboptions:
          value:
            description:
              - The IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix length of the IPv6 address.
            type: int
            required: false
  uuid_filter_list:
    description:
      - Unconfigured node UUIDs.
    type: list
    elements: str
  interface_filter_list:
    description:
      - Interface name that is used for packet broadcasting.
    type: list
    elements: str
  is_manual_discovery:
    description:
      - Indicates if the discovery is manual or not.
    type: bool
  timeout:
    description:
      - Timeout for the workflow in seconds.
    type: int
  cluster_ext_id:
    description:
      - External ID of the cluster.
      - If not provided, Prism Central cluster will be fetched.
    type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Prem Karat (@premkarat)
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Discover unconfigured node
  ntnx_discover_unconfigured_nodes_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    address_type: "IPV4"
    ip_filter_list:
      - ipv4:
          value: "10.12.102.22"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the discover unconfigured node operation.
        - This field typically holds the task details.
    type: dict
    returned: always
    sample:
      {
        "node_list":
          [
            {
              "arch": null,
              "attributes": null,
              "cluster_id": null,
              "cpu_type": null,
              "current_cvm_vlan_tag": "null",
              "current_network_interface": null,
              "cvm_ip":
                {
                  "ipv4": { "prefix_length": 32, "value": "10.37.186.154" },
                  "ipv6": null,
                },
              "foundation_version": null,
              "host_name": "ntnx-nahv-671ddc077298f65ebce337ed-1\n",
              "host_type": "HYPER_CONVERGED",
              "hypervisor_ip": null,
              "hypervisor_type": "AHV",
              "hypervisor_version": "10.0-727",
              "interface_ipv6": null,
              "ipmi_ip": null,
              "is_one_node_cluster_supported": true,
              "is_secure_booted": null,
              "is_two_node_cluster_supported": true,
              "node_position": "A",
              "node_serial_number": "10-37-186-154",
              "node_uuid": null,
              "nos_version": "6.9",
              "rackable_unit_max_nodes": null,
              "rackable_unit_model": "NestedAHV",
              "rackable_unit_serial": "10-37-186-154",
            },
          ],
      }

task_ext_id:
    description: Task external ID.
    type: str
    returned: always
    sample: "ZXJnb24=:5235a162-25c2-41b7-50ba-71b2e545fdba"

error:
    description: Error message if an error occurs.
    type: str
    returned: when an error occurs
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
        ipv4=dict(type="dict", options=ipv4_spec),
        ipv6=dict(type="dict", options=ipv6_spec),
    )
    module_args = dict(
        address_type=dict(type="str", choices=["IPV4", "IPV6"]),
        ip_filter_list=dict(type="list", elements="dict", options=ip_address_spec),
        uuid_filter_list=dict(type="list", elements="str"),
        interface_filter_list=dict(type="list", elements="str"),
        is_manual_discovery=dict(type="bool"),
        timeout=dict(type="int"),
        cluster_ext_id=dict(type="str"),
    )
    return module_args


def discover_unconfigured_cluster_node(module, cluster_node_api, result):
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.NodeDiscoveryParams()
    spec, err = sg.generate_spec(default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for discovering cluster nodes", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    resp = None
    if module.params.get("cluster_ext_id"):
        cluster_ext_id = module.params.get("cluster_ext_id")
    else:
        params = {
            "filter": "config/clusterFunction/any(t:t eq Clustermgmt.Config.ClusterFunctionRef'PRISM_CENTRAL')"
        }
        sg = SpecGenerator(module)
        kwargs, err = sg.get_info_spec(attr=params)
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed generating spec for fetching prism central cluster",
                **result,
            )
        try:
            pc_cluster = cluster_node_api.list_clusters(**kwargs)
        except Exception as e:
            raise_api_exception(
                module=module,
                exception=e,
                msg="Api Exception raised while fetching clusters info",
            )
        if not pc_cluster.data:
            module.fail_json(
                msg="No Prism Central cluster found in the environment", **result
            )
        cluster_ext_id = pc_cluster.data[0].ext_id
    result["cluster_ext_id"] = cluster_ext_id
    try:
        resp = cluster_node_api.discover_unconfigured_nodes(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while discovering cluster nodes",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        if ":" in task_ext_id:
            task_ext_id = task_ext_id.split(":")[1]
        task_status = cluster_node_api.fetch_task_response(
            extId=task_ext_id, taskResponseType="UNCONFIGURED_NODES"
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
        "cluster_ext_id": None,
    }
    cluster_node_api = get_clusters_api_instance(module)
    discover_unconfigured_cluster_node(module, cluster_node_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
