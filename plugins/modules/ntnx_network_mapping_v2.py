#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_network_mapping_v2
short_description: Create, Update, Delete Recovery Plan Network Mappings in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete Network Mappings that belong to a Recovery Plan in Nutanix Prism Central.
  - A Network Mapping maps a primary/source subnet to a recovery/target subnet
    (and optionally the corresponding test networks) so that virtual NICs can be
    recreated on the correct network during a failover or failback.
  - This module uses PC v4 APIs based SDKs (ntnx_datapolicies_py_client).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Network Mapping) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Super Admin
    - >-
      B(Update a Network Mapping) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Super Admin
    - >-
      B(Delete a Network Mapping) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create network mapping.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update network mapping.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete network mapping.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the network mapping.
      - Required for update and delete operations.
    type: str
    required: false
  recovery_plan_ext_id:
    description:
      - External identifier of the parent recovery plan under which the
        network mapping is created, updated or deleted.
      - Required for every operation.
    type: str
    required: true
  primary_network:
    description:
      - Network configuration for the source (primary) location of the mapping.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      subnet_ext_id:
        description:
          - External identifier of the subnet.
          - Only one of C(subnet_ext_id) or C(subnet_name) may be specified at a time.
        type: str
        required: false
      subnet_name:
        description:
          - Name of the subnet or port group.
          - Only one of C(subnet_ext_id) or C(subnet_name) may be specified at a time.
        type: str
        required: false
      vpc:
        description:
          - Reference of the VPC that owns the subnet.
          - Required when the subnet is an overlay network.
        type: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the VPC entity.
            type: str
            required: true
          name:
            description:
              - Name of the VPC entity.
            type: str
            required: false
      ip_config:
        description:
          - IP configuration of the subnet.
          - Only required when C(is_ip_mapping_enabled) is true and static IP mapping is desired.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 configuration of the subnet.
            type: dict
            required: true
            suboptions:
              default_gateway_ip:
                description:
                  - Subnet gateway IP address.
                type: str
                required: false
              prefix_length:
                description:
                  - Subnet prefix length (0-32).
                type: int
                required: false
              network_ip_address:
                description:
                  - Network IP address.
                type: str
                required: false
              domain_name_servers:
                description:
                  - DNS servers IP addresses.
                type: list
                elements: str
                required: false
              domain_search_suffixes:
                description:
                  - DNS search suffixes.
                type: list
                elements: str
                required: false
              ip_pool:
                description:
                  - Start/end IP address range for the subnet.
                type: dict
                required: false
                suboptions:
                  start_ip:
                    description:
                      - Starting IPv4 address of the pool.
                    type: dict
                    required: true
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
                  end_ip:
                    description:
                      - Ending IPv4 address of the pool.
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
  recovery_network:
    description:
      - Network configuration for the recovery/target location used during
        planned or unplanned failover.
    type: dict
    required: false
    suboptions:
      subnet_ext_id:
        description:
          - External identifier of the subnet.
          - Only one of C(subnet_ext_id) or C(subnet_name) may be specified at a time.
        type: str
        required: false
      subnet_name:
        description:
          - Name of the subnet or port group.
        type: str
        required: false
      vpc:
        description:
          - Reference of the VPC that owns the subnet.
        type: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the VPC entity.
            type: str
            required: true
          name:
            description:
              - Name of the VPC entity.
            type: str
            required: false
      ip_config:
        description:
          - IP configuration of the subnet at the recovery location.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 configuration of the recovery subnet.
            type: dict
            required: true
            suboptions:
              default_gateway_ip:
                description:
                  - Subnet gateway IP address.
                type: str
                required: false
              prefix_length:
                description:
                  - Subnet prefix length (0-32).
                type: int
                required: false
              network_ip_address:
                description:
                  - Network IP address.
                type: str
                required: false
              domain_name_servers:
                description:
                  - DNS servers IP addresses.
                type: list
                elements: str
                required: false
              domain_search_suffixes:
                description:
                  - DNS search suffixes.
                type: list
                elements: str
                required: false
              ip_pool:
                description:
                  - Start/end IP address range for the subnet.
                type: dict
                required: false
                suboptions:
                  start_ip:
                    description:
                      - Starting IPv4 address of the pool.
                    type: dict
                    required: true
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
                  end_ip:
                    description:
                      - Ending IPv4 address of the pool.
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
  primary_test_network:
    description:
      - Network configuration at the source location that is used when a
        test failover is triggered. This must be an isolated network to
        avoid IP collisions with running production VMs.
    type: dict
    required: false
    suboptions:
      subnet_ext_id:
        description:
          - External identifier of the subnet.
        type: str
        required: false
      subnet_name:
        description:
          - Name of the subnet or port group.
        type: str
        required: false
      vpc:
        description:
          - Reference of the VPC that owns the subnet.
        type: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the VPC entity.
            type: str
            required: true
          name:
            description:
              - Name of the VPC entity.
            type: str
            required: false
      ip_config:
        description:
          - IP configuration of the test subnet.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 configuration of the test subnet.
            type: dict
            required: true
            suboptions:
              default_gateway_ip:
                description:
                  - Subnet gateway IP address.
                type: str
                required: false
              prefix_length:
                description:
                  - Subnet prefix length (0-32).
                type: int
                required: false
              network_ip_address:
                description:
                  - Network IP address.
                type: str
                required: false
              domain_name_servers:
                description:
                  - DNS servers IP addresses.
                type: list
                elements: str
                required: false
              domain_search_suffixes:
                description:
                  - DNS search suffixes.
                type: list
                elements: str
                required: false
              ip_pool:
                description:
                  - Start/end IP address range for the subnet.
                type: dict
                required: false
                suboptions:
                  start_ip:
                    description:
                      - Starting IPv4 address of the pool.
                    type: dict
                    required: true
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
                  end_ip:
                    description:
                      - Ending IPv4 address of the pool.
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
  recovery_test_network:
    description:
      - Network configuration at the recovery location used when a test
        failover is triggered. This must be an isolated network to avoid
        IP collisions with production VMs.
    type: dict
    required: false
    suboptions:
      subnet_ext_id:
        description:
          - External identifier of the subnet.
        type: str
        required: false
      subnet_name:
        description:
          - Name of the subnet or port group.
        type: str
        required: false
      vpc:
        description:
          - Reference of the VPC that owns the subnet.
        type: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the VPC entity.
            type: str
            required: true
          name:
            description:
              - Name of the VPC entity.
            type: str
            required: false
      ip_config:
        description:
          - IP configuration of the recovery test subnet.
        type: dict
        required: false
        suboptions:
          ipv4:
            description:
              - IPv4 configuration of the recovery test subnet.
            type: dict
            required: true
            suboptions:
              default_gateway_ip:
                description:
                  - Subnet gateway IP address.
                type: str
                required: false
              prefix_length:
                description:
                  - Subnet prefix length (0-32).
                type: int
                required: false
              network_ip_address:
                description:
                  - Network IP address.
                type: str
                required: false
              domain_name_servers:
                description:
                  - DNS servers IP addresses.
                type: list
                elements: str
                required: false
              domain_search_suffixes:
                description:
                  - DNS search suffixes.
                type: list
                elements: str
                required: false
              ip_pool:
                description:
                  - Start/end IP address range for the subnet.
                type: dict
                required: false
                suboptions:
                  start_ip:
                    description:
                      - Starting IPv4 address of the pool.
                    type: dict
                    required: true
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
                  end_ip:
                    description:
                      - Ending IPv4 address of the pool.
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
  is_ip_mapping_enabled:
    description:
      - When true, static IPs of recovered VMs are mapped according to the
        target network and configured inside the guest VMs. Requires
        Nutanix Guest Tools (NGT) to be installed on the protected VMs.
      - When false, VMs may recover with any IP allocated by the DHCP
        server on the target network.
    type: bool
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create network mapping using subnet external IDs
  nutanix.ncp.ntnx_network_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
    primary_network:
      subnet_ext_id: "5a6f8f2c-3f2b-4a1c-9c14-2d17b3e6b555"
    recovery_network:
      subnet_ext_id: "6b7e9d3c-4a1f-5b12-8e15-3d17b3e6c666"
    primary_test_network:
      subnet_ext_id: "7c8f1e4d-5b12-6c23-9d16-4e17b3e6d777"
    recovery_test_network:
      subnet_ext_id: "8d9e2f5e-6c23-7d34-9e17-5f17b3e6e888"
    is_ip_mapping_enabled: false
  register: created

- name: Create network mapping with static IP mapping and IP pool
  nutanix.ncp.ntnx_network_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
    primary_network:
      subnet_ext_id: "5a6f8f2c-3f2b-4a1c-9c14-2d17b3e6b555"
      ip_config:
        ipv4:
          default_gateway_ip: "10.10.0.1"
          prefix_length: 24
          ip_pool:
            start_ip:
              value: "10.10.0.10"
            end_ip:
              value: "10.10.0.100"
    recovery_network:
      subnet_ext_id: "6b7e9d3c-4a1f-5b12-8e15-3d17b3e6c666"
      ip_config:
        ipv4:
          default_gateway_ip: "10.20.0.1"
          prefix_length: 24
          ip_pool:
            start_ip:
              value: "10.20.0.10"
            end_ip:
              value: "10.20.0.100"
    is_ip_mapping_enabled: true
  register: created

- name: Update network mapping
  nutanix.ncp.ntnx_network_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
    ext_id: "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f"
    primary_network:
      subnet_ext_id: "5a6f8f2c-3f2b-4a1c-9c14-2d17b3e6b555"
    recovery_network:
      subnet_ext_id: "9e1a3d6f-7d34-8e45-af18-6f17b3e6f999"
    is_ip_mapping_enabled: false
  register: updated

- name: Delete network mapping
  nutanix.ncp.ntnx_network_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    recovery_plan_ext_id: "b0e1a7b2-8c31-4a41-9f2c-3f2f0f76de11"
    ext_id: "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f"
  register: deleted
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a network mapping.
    - If the operation is create or update and C(wait) is true, it returns the network mapping details.
    - If the operation is create or update and C(wait) is false, it returns the task details.
    - If the operation is delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f",
      "is_ip_mapping_enabled": false,
      "links": null,
      "primary_network": {
        "ip_config": null,
        "subnet_ext_id": "5a6f8f2c-3f2b-4a1c-9c14-2d17b3e6b555",
        "subnet_name": null,
        "vpc": null
      },
      "primary_test_network": null,
      "recovery_network": {
        "ip_config": null,
        "subnet_ext_id": "6b7e9d3c-4a1f-5b12-8e15-3d17b3e6c666",
        "subnet_name": null,
        "vpc": null
      },
      "recovery_test_network": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the network mapping.
  returned: always
  type: str
  sample: "1cadd9f5-52fa-4ad9-9dcb-11ab8b6c3d7f"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (idempotency)
  returned: always
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating network mapping"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_etag,
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_network_mapping  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_policies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv4_pool_spec = dict(
        start_ip=dict(
            type="dict",
            required=True,
            options=ipv4_address_spec,
            obj=data_policies_sdk.IPv4Address,
        ),
        end_ip=dict(
            type="dict",
            required=False,
            options=ipv4_address_spec,
            obj=data_policies_sdk.IPv4Address,
        ),
    )

    ipv4_config_spec = dict(
        default_gateway_ip=dict(type="str", required=False),
        prefix_length=dict(type="int", required=False),
        network_ip_address=dict(type="str", required=False),
        domain_name_servers=dict(type="list", elements="str", required=False),
        domain_search_suffixes=dict(type="list", elements="str", required=False),
        ip_pool=dict(
            type="dict",
            required=False,
            options=ipv4_pool_spec,
            obj=data_policies_sdk.IPv4Pool,
        ),
    )

    ip_config_spec = dict(
        ipv4=dict(
            type="dict",
            required=True,
            options=ipv4_config_spec,
            obj=data_policies_sdk.IPv4Config,
        ),
    )

    entity_reference_spec = dict(
        ext_id=dict(type="str", required=True),
        name=dict(type="str", required=False),
    )

    network_config_spec = dict(
        subnet_ext_id=dict(type="str", required=False),
        subnet_name=dict(type="str", required=False),
        vpc=dict(
            type="dict",
            required=False,
            options=entity_reference_spec,
            obj=data_policies_sdk.EntityReference,
        ),
        ip_config=dict(
            type="dict",
            required=False,
            options=ip_config_spec,
            obj=data_policies_sdk.IPConfig,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        recovery_plan_ext_id=dict(type="str", required=True),
        primary_network=dict(
            type="dict",
            required=False,
            options=network_config_spec,
            obj=data_policies_sdk.NetworkConfig,
        ),
        recovery_network=dict(
            type="dict",
            required=False,
            options=network_config_spec,
            obj=data_policies_sdk.NetworkConfig,
        ),
        primary_test_network=dict(
            type="dict",
            required=False,
            options=network_config_spec,
            obj=data_policies_sdk.NetworkConfig,
        ),
        recovery_test_network=dict(
            type="dict",
            required=False,
            options=network_config_spec,
            obj=data_policies_sdk.NetworkConfig,
        ),
        is_ip_mapping_enabled=dict(type="bool", required=False),
    )
    return module_args


def _resolve_network_mapping_ext_id(task_data):
    """Resolve the network mapping ext_id from a completed task, first via
    completion details (preferred), then via entities affected."""
    ext_id = get_ext_id_from_task_completion_details(
        task_data, name=TASK_CONSTANTS.CompletetionDetailsName.NETWORK_MAPPING
    )
    if ext_id:
        return ext_id
    return get_entity_ext_id_from_task(
        task_data, rel=TASK_CONSTANTS.RelEntityType.NETWORK_MAPPING
    )


def create_network_mapping(module, result, api_instance):
    validate_required_params(module, ["primary_network"])
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")

    sg = SpecGenerator(module)
    default_spec = data_policies_sdk.NetworkMapping()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create network mapping spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_network_mapping(
            recoveryPlanExtId=recovery_plan_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating network mapping",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = _resolve_network_mapping_ext_id(task_resp)
        if ext_id:
            result["ext_id"] = ext_id
            nm_resp = get_network_mapping(
                module, api_instance, recovery_plan_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(nm_resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Network Mapping"
                ),
                msg="Failed to get entity ext_id from task for Network Mapping",
            )
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_network_mapping(module, result, api_instance):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["primary_network"])

    current = get_network_mapping(module, api_instance, recovery_plan_ext_id, ext_id)
    etag = get_etag(data=current)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating network mapping", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update network mapping spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(current.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change.",
            **result,
        )

    kwargs = {"if_match": etag}
    try:
        resp = api_instance.update_network_mapping_by_id(
            recoveryPlanExtId=recovery_plan_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating network mapping",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        nm_resp = get_network_mapping(
            module, api_instance, recovery_plan_ext_id, ext_id
        )
        result["response"] = strip_internal_attributes(nm_resp.to_dict())
    result["changed"] = True


def delete_network_mapping(module, result, api_instance):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Network mapping with ext_id:{0} for recovery plan:{1} "
            "will be deleted.".format(ext_id, recovery_plan_ext_id)
        )
        return

    try:
        resp = api_instance.delete_network_mapping_by_id(
            recoveryPlanExtId=recovery_plan_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting network mapping",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_recovery_plans_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_network_mapping(module, result, api_instance)
        else:
            create_network_mapping(module, result, api_instance)
    else:
        delete_network_mapping(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
