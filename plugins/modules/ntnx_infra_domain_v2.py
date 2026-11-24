#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_infra_domain_v2
short_description: Create infrastructure domain in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Create infrastructure domain in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create an infrastructure domain) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will create the infrastructure domain.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    name:
        description:
            - Name of the infrastructure domain.
        type: str
        required: false
    description:
        description:
            - Description of the infrastructure domain.
        type: str
        required: false
    location:
        description:
            - Location of the infrastructure domain.
        type: str
        required: false
    fqdn:
        description:
            - Fully qualified domain name for the infrastructure domain.
        type: dict
        required: false
        suboptions:
            value:
                description:
                    - The fully qualified domain name value.
                type: str
                required: false
    cluster_associations:
        description:
            - Association between a cluster and the infrastructure domain.
        type: list
        elements: dict
        required: false
        suboptions:
            cluster_ext_id:
                description:
                    - External identifier of the cluster to associate with the infrastructure domain.
                type: str
                required: true
            is_hosting:
                description:
                    - Indicates whether the cluster is hosting the infrastructure domain.
                type: bool
                required: false
    platform_config:
        description:
            - Per-cluster configuration of the deployed infrastructure domain control plane.
        type: dict
        required: false
        suboptions:
            platform_cluster_ext_id:
                description:
                    - External identifier of the Platform cluster associated with the infrastructure domain cluster.
                type: str
                required: false
            virtual_ip:
                description:
                    - Virtual IP address for the platform cluster.
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
                                    - Prefix length of the network.
                                type: int
                                required: false
                                default: 32
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
                                    - Prefix length of the network.
                                type: int
                                required: false
                                default: 128
            name_server_ip:
                description:
                    - Name server IP address for the platform cluster.
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
                                    - Prefix length of the network.
                                type: int
                                required: false
                                default: 32
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
                                    - Prefix length of the network.
                                type: int
                                required: false
                                default: 128
            hosting_cluster_info:
                description:
                    - Hosting cluster information for the infrastructure domain.
                type: dict
                required: false
                suboptions:
                    network_config:
                        description:
                            - Configuration for mapping each hosting cluster to an existing subnet.
                        type: dict
                        required: false
                        suboptions:
                            cluster_subnet_configs:
                                description:
                                    - Per-cluster subnet configuration.
                                type: list
                                elements: dict
                                required: false
                                suboptions:
                                    cluster_ext_id:
                                        description:
                                            - External identifier of the hosting cluster mapped to the subnet.
                                        type: str
                                        required: true
                                    subnet_ext_id:
                                        description:
                                            - External identifier of the subnet.
                                        type: str
                                        required: false
            load_balancer_config:
                description:
                    - Network configuration for the load balancer fronting the infrastructure domain.
                type: list
                elements: dict
                required: false
                suboptions:
                    ip_addresses:
                        description:
                            - IP addresses assigned to the load balancer.
                        type: list
                        elements: dict
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
                                            - Prefix length of the network.
                                        type: int
                                        required: false
                                        default: 32
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
                                            - Prefix length of the network.
                                        type: int
                                        required: false
                                        default: 128
                    cluster_network_config:
                        description:
                            - Maps a hosting cluster to an existing subnet.
                        type: dict
                        required: false
                        suboptions:
                            cluster_ext_id:
                                description:
                                    - External identifier of the hosting cluster mapped to the subnet.
                                type: str
                                required: true
                            subnet_ext_id:
                                description:
                                    - External identifier of the subnet.
                                type: str
                                required: false
    size:
        description:
            - Deployment size for the infrastructure domain.
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
- name: Create infrastructure domain with minimal attributes
  nutanix.ncp.ntnx_infra_domain_v2:
    name: "test-infra-domain"
    description: "Test infra domain via Ansible"
    location: "us-west-1"
  register: result
  ignore_errors: true

- name: Create infrastructure domain with cluster associations
  nutanix.ncp.ntnx_infra_domain_v2:
    name: "test-infra-domain-full"
    description: "Test infra domain with clusters"
    location: "us-east-1"
    fqdn:
      value: "infra.example.com"
    cluster_associations:
      - cluster_ext_id: "00000000-0000-0000-0000-000000000001"
        is_hosting: true
    size: "SMALL"
  register: result
  ignore_errors: true

- name: Create infrastructure domain with platform config
  nutanix.ncp.ntnx_infra_domain_v2:
    name: "test-infra-domain-platform"
    description: "Test infra domain with platform config"
    location: "eu-central-1"
    platform_config:
      platform_cluster_ext_id: "00000000-0000-0000-0000-000000000002"
      virtual_ip:
        ipv4:
          value: "10.0.0.10"
          prefix_length: 32
      name_server_ip:
        ipv4:
          value: "10.0.0.11"
          prefix_length: 32
      hosting_cluster_info:
        network_config:
          cluster_subnet_configs:
            - cluster_ext_id: "00000000-0000-0000-0000-000000000001"
              subnet_ext_id: "00000000-0000-0000-0000-000000000003"
      load_balancer_config:
        - ip_addresses:
            - ipv4:
                value: "10.0.0.20"
                prefix_length: 32
          cluster_network_config:
            cluster_ext_id: "00000000-0000-0000-0000-000000000001"
            subnet_ext_id: "00000000-0000-0000-0000-000000000003"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - Response for creating infrastructure domain.
      - If C(wait) is true, it will contain the final task payload after completion.
      - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00066101-9650-faa8-0000-000000028f57"
      ],
      "completed_time": "2025-02-09T15:34:15.092891+00:00",
      "completion_details": null,
      "created_time": "2025-02-09T14:44:52.593544+00:00",
      "entities_affected": [
        {
          "ext_id": "00066101-9650-faa8-0000-000000028f57",
          "name": null,
          "rel": "prism:config:infra-domain"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:a6c95b0b-4a97-4165-6619-f09ba156bea1",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2025-02-09T15:34:15.092888+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 1,
      "operation": "CreateInfraDomain",
      "operation_description": "Create infrastructure domain",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2025-02-09T14:44:52.602785+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": [
        {
          "ext_id": "ZXJnb24=:f9856c8f-d619-42d6-65b3-5651e8825a6c",
          "href": "https://10.44.76.16:9440/api/prism/v4.5/config/tasks/ZXJnb24=:f9856c8f-d619-42d6-65b3-5651e8825a6c",
          "rel": "subtask"
        }
      ],
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the infrastructure domain.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while creating infra domain"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_infra_domain_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=prism_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=prism_sdk.IPv6Address,
        ),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=False),
    )

    cluster_association_spec = dict(
        cluster_ext_id=dict(type="str", required=True),
        is_hosting=dict(type="bool", required=False),
    )

    cluster_subnet_config_spec = dict(
        cluster_ext_id=dict(type="str", required=True),
        subnet_ext_id=dict(type="str", required=False),
    )

    subnet_config_spec = dict(
        cluster_subnet_configs=dict(
            type="list",
            elements="dict",
            options=cluster_subnet_config_spec,
            obj=prism_sdk.ClusterSubnetConfig,
        ),
    )

    hosting_cluster_info_spec = dict(
        network_config=dict(
            type="dict",
            options=subnet_config_spec,
            obj=prism_sdk.SubnetConfig,
        ),
    )

    load_balancer_config_spec = dict(
        ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            obj=prism_sdk.IPAddress,
        ),
        cluster_network_config=dict(
            type="dict",
            options=cluster_subnet_config_spec,
            obj=prism_sdk.ClusterSubnetConfig,
        ),
    )

    platform_config_spec = dict(
        platform_cluster_ext_id=dict(type="str", required=False),
        virtual_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=prism_sdk.IPAddress,
        ),
        name_server_ip=dict(
            type="dict",
            options=ip_address_spec,
            obj=prism_sdk.IPAddress,
        ),
        hosting_cluster_info=dict(
            type="dict",
            options=hosting_cluster_info_spec,
            obj=prism_sdk.HostingClusterInfo,
        ),
        load_balancer_config=dict(
            type="list",
            elements="dict",
            options=load_balancer_config_spec,
            obj=prism_sdk.LoadBalancerConfig,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        location=dict(type="str", required=False),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=prism_sdk.FQDN,
        ),
        cluster_associations=dict(
            type="list",
            elements="dict",
            options=cluster_association_spec,
            obj=prism_sdk.ClusterAssociation,
        ),
        platform_config=dict(
            type="dict",
            options=platform_config_spec,
            obj=prism_sdk.PlatformConfig,
        ),
        size=dict(type="str", required=False),
    )
    return module_args


def create_infra_domain(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = prism_sdk.InfraDomain()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create infra domain spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_infra_domain(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating infra domain",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_infra_domain_api_instance(module)
    create_infra_domain(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
