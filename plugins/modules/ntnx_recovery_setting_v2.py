#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_setting_v2
short_description: Create, Update, Delete custom recovery settings on a Nutanix Recovery Plan
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete custom recovery settings
    on a Nutanix Recovery Plan in Prism Central.
  - A recovery setting overrides the default recovery behavior for a specific VM,
    a specific Volume Group, or all VMs in a given category during a failover
    orchestrated by the parent Recovery Plan.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Recovery Setting) -
      Required Roles: Disaster Recovery Admin, NCM Connector, Prism Admin, Super Admin
    - >-
      B(Update a Recovery Setting) -
      Required Roles: Disaster Recovery Admin, NCM Connector, Prism Admin, Super Admin
    - >-
      B(Delete a Recovery Setting) -
      Required Roles: Disaster Recovery Admin, NCM Connector, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create recovery setting.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update recovery setting.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete recovery setting.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External identifier of the recovery setting.
      - Required for update and delete operations.
    type: str
    required: false
  recovery_plan_ext_id:
    description:
      - External identifier of the parent recovery plan.
      - Required for all create, update, and delete operations.
    type: str
    required: true
  recovery_setting:
    description:
      - Recovery setting to be applied to a VM, VM category, or Volume Group.
      - Exactly one of C(vm), C(vm_category), or C(volume_group) must be provided.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      vm:
        description:
          - Recovery configuration for a specific VM.
        type: dict
        required: false
        suboptions:
          vm:
            description:
              - External reference of the VM to which this recovery setting applies.
            type: dict
            required: true
            suboptions:
              ext_id:
                description:
                  - External identifier of the VM.
                type: str
                required: true
          power_state:
            description:
              - Desired power state of the VM after recovery.
            type: str
            required: false
            choices:
              - "ON"
              - "OFF"
          in_guest_script_execution_config:
            description:
              - In-guest script execution configuration for the VM.
            type: dict
            required: false
            suboptions:
              is_enabled:
                description:
                  - Whether to run in-guest scripts as part of the recovery process.
                type: bool
                required: false
              timeout_secs:
                description:
                  - Maximum time in seconds to wait for the in-guest script to complete.
                type: int
                required: false
          volume_group_attachments:
            description:
              - Volume Groups that should be attached to the recovered VM.
            type: list
            elements: dict
            required: false
            suboptions:
              volume_group:
                description:
                  - External reference of the Volume Group to attach.
                type: dict
                required: true
                suboptions:
                  ext_id:
                    description:
                      - External identifier of the Volume Group.
                    type: str
                    required: true
              attachment_type:
                description:
                  - Attachment type of the Volume Group.
                type: str
                required: false
                choices:
                  - DIRECT
                  - EXTERNAL
              protocol:
                description:
                  - Protocol used to attach the Volume Group.
                type: str
                required: false
                choices:
                  - ISCSI
                  - NVMF
              client_features:
                description:
                  - Client side features for the Volume Group attachment.
                type: dict
                required: false
                suboptions:
                  iscsi_features:
                    description:
                      - iSCSI specific settings for the client of the recovered Volume Group.
                    type: dict
                    required: false
                    suboptions:
                      enabled_authentication:
                        description:
                          - iSCSI authentication type.
                        type: str
                        required: true
                        choices:
                          - CHAP
                          - NONE
                      secret:
                        description:
                          - iSCSI target CHAP secret.
                          - Required when C(enabled_authentication=CHAP).
                          - Sensitive value; not logged.
                        type: str
                        required: false
          ip_mappings:
            description:
              - IP mapping between primary and recovery networks for the VM's NICs.
            type: list
            elements: dict
            required: false
            suboptions:
              network_mapping_ext_id:
                description:
                  - External identifier of the Network Mapping this IP mapping belongs to.
                type: str
                required: true
              primary_ip:
                description:
                  - IP address on the primary site.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address on the primary site.
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
                          - Prefix length of the IPv4 subnet.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - IPv6 address on the primary site.
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
                          - Prefix length of the IPv6 subnet.
                        type: int
                        required: false
                        default: 128
              recovery_ip:
                description:
                  - IP address to assign after a real failover on the recovery site.
                type: dict
                required: false
                suboptions:
                  ipv4:
                    description:
                      - IPv4 address on the recovery site.
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
                          - Prefix length of the IPv4 subnet.
                        type: int
                        required: false
                        default: 32
                  ipv6:
                    description:
                      - IPv6 address on the recovery site.
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
                          - Prefix length of the IPv6 subnet.
                        type: int
                        required: false
                        default: 128
              primary_test_ip:
                description:
                  - IP address used when the VM is running as a test on the primary site.
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
                          - Prefix length of the IPv4 subnet.
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
                          - Prefix length of the IPv6 subnet.
                        type: int
                        required: false
                        default: 128
              recovery_test_ip:
                description:
                  - IP address used when the VM is running as a test on the recovery site.
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
                          - Prefix length of the IPv4 subnet.
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
                          - Prefix length of the IPv6 subnet.
                        type: int
                        required: false
                        default: 128
          floating_ip_associations:
            description:
              - Floating IP address associations for the VM's NICs.
            type: list
            elements: dict
            required: false
            suboptions:
              nic_ext_id:
                description:
                  - External identifier of the virtual NIC corresponding to which the floating IP address is to be assigned.
                type: str
                required: true
              primary_floating_ip:
                description:
                  - Floating IP configuration on the primary site.
                type: dict
                required: false
                suboptions:
                  should_allocate_dynamically:
                    description:
                      - Whether to dynamically allocate a floating IP.
                    type: bool
                    required: false
                  ip_address:
                    description:
                      - Static floating IP address.
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
                              - Prefix length of the IPv4 subnet.
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
                              - Prefix length of the IPv6 subnet.
                            type: int
                            required: false
                            default: 128
              recovery_floating_ip:
                description:
                  - Floating IP configuration on the recovery site during real failover.
                type: dict
                required: false
                suboptions:
                  should_allocate_dynamically:
                    description:
                      - Whether to dynamically allocate a floating IP.
                    type: bool
                    required: false
                  ip_address:
                    description:
                      - Static floating IP address.
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
                              - Prefix length of the IPv4 subnet.
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
                              - Prefix length of the IPv6 subnet.
                            type: int
                            required: false
                            default: 128
              primary_test_floating_ip:
                description:
                  - Floating IP configuration used during test failover on the primary site.
                type: dict
                required: false
                suboptions:
                  should_allocate_dynamically:
                    description:
                      - Whether to dynamically allocate a floating IP.
                    type: bool
                    required: false
                  ip_address:
                    description:
                      - Static floating IP address.
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
                              - Prefix length of the IPv4 subnet.
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
                              - Prefix length of the IPv6 subnet.
                            type: int
                            required: false
                            default: 128
              recovery_test_floating_ip:
                description:
                  - Floating IP configuration used during test failover on the recovery site.
                type: dict
                required: false
                suboptions:
                  should_allocate_dynamically:
                    description:
                      - Whether to dynamically allocate a floating IP.
                    type: bool
                    required: false
                  ip_address:
                    description:
                      - Static floating IP address.
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
                              - Prefix length of the IPv4 subnet.
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
                              - Prefix length of the IPv6 subnet.
                            type: int
                            required: false
                            default: 128
      vm_category:
        description:
          - Recovery configuration applied to all VMs in a given category.
        type: dict
        required: false
        suboptions:
          vm_category_ext_id:
            description:
              - External identifier of the VM category.
            type: str
            required: true
          power_state:
            description:
              - Desired power state of the VMs after recovery.
            type: str
            required: false
            choices:
              - "ON"
              - "OFF"
          in_guest_script_execution_config:
            description:
              - In-guest script execution configuration for the VMs.
            type: dict
            required: false
            suboptions:
              is_enabled:
                description:
                  - Whether to run in-guest scripts as part of the recovery process.
                type: bool
                required: false
              timeout_secs:
                description:
                  - Maximum time in seconds to wait for the in-guest script to complete.
                type: int
                required: false
      volume_group:
        description:
          - Recovery configuration for a specific Volume Group.
        type: dict
        required: false
        suboptions:
          volume_group:
            description:
              - External reference of the Volume Group.
            type: dict
            required: true
            suboptions:
              ext_id:
                description:
                  - External identifier of the Volume Group.
                type: str
                required: true
          iscsi_target_features:
            description:
              - iSCSI specific settings for the recovered Volume Group target.
            type: dict
            required: false
            suboptions:
              enabled_authentication:
                description:
                  - iSCSI authentication type.
                type: str
                required: true
                choices:
                  - CHAP
                  - NONE
              secret:
                description:
                  - iSCSI target CHAP secret.
                  - Required when C(enabled_authentication=CHAP).
                  - Sensitive value; not logged.
                type: str
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
- name: Create a VM recovery setting
  nutanix.ncp.ntnx_recovery_setting_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
    recovery_setting:
      vm:
        vm:
          ext_id: "0005c1c1-0000-0000-0000-000000000001"
        power_state: "ON"
        in_guest_script_execution_config:
          is_enabled: true
          timeout_secs: 300
  register: result

- name: Update a VM recovery setting
  nutanix.ncp.ntnx_recovery_setting_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
    ext_id: "d1a2b3c4-5555-6666-7777-8888aabbccdd"
    recovery_setting:
      vm:
        vm:
          ext_id: "0005c1c1-0000-0000-0000-000000000001"
        power_state: "OFF"
        in_guest_script_execution_config:
          is_enabled: false
  register: result

- name: Delete a recovery setting
  nutanix.ncp.ntnx_recovery_setting_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    recovery_plan_ext_id: "b7d1f5c3-3f2a-4d4e-9b8b-1c1d3e2f8a11"
    ext_id: "d1a2b3c4-5555-6666-7777-8888aabbccdd"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting recovery setting
    - If the operation is create or update and C(wait) is true, it will return the recovery setting details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "ext_id": "d1a2b3c4-5555-6666-7777-8888aabbccdd",
      "links": null,
      "recovery_setting": {
        "floating_ip_associations": null,
        "in_guest_script_execution_config": {
          "is_enabled": true,
          "timeout_secs": 300
        },
        "ip_mappings": null,
        "power_state": "ON",
        "vm": {
          "ext_id": "0005c1c1-0000-0000-0000-000000000001",
          "name": null
        },
        "volume_group_attachments": null
      },
      "scope": "VM",
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
    - The external ID of the recovery setting.
  returned: always
  type: str
  sample: "d1a2b3c4-5555-6666-7777-8888aabbccdd"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
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
  sample: "Api Exception raised while creating recovery setting"
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
from ..module_utils.v4.data_policies.helpers import get_recovery_setting  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
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


def _build_ipv4_spec():
    return dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )


def _build_ipv6_spec():
    return dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )


def _build_ip_address_spec():
    return dict(
        ipv4=dict(
            type="dict",
            options=_build_ipv4_spec(),
            required=False,
            obj=data_policies_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=_build_ipv6_spec(),
            required=False,
            obj=data_policies_sdk.IPv6Address,
        ),
    )


def _build_floating_ip_spec():
    return dict(
        should_allocate_dynamically=dict(type="bool", required=False),
        ip_address=dict(
            type="dict",
            options=_build_ip_address_spec(),
            required=False,
            obj=data_policies_sdk.IPAddress,
        ),
    )


def get_module_spec():

    entity_reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    in_guest_script_spec = dict(
        is_enabled=dict(type="bool", required=False),
        timeout_secs=dict(type="int", required=False),
    )

    iscsi_features_spec = dict(
        enabled_authentication=dict(
            type="str", required=True, choices=["CHAP", "NONE"]
        ),
        secret=dict(type="str", required=False, no_log=True),
    )

    volume_group_client_features_obj_map = {
        "iscsi_features": data_policies_sdk.IscsiFeatures,
    }

    volume_group_client_features_spec = dict(
        iscsi_features=dict(
            type="dict",
            options=iscsi_features_spec,
            required=False,
        ),
    )

    volume_group_attachment_spec = dict(
        volume_group=dict(
            type="dict",
            options=entity_reference_spec,
            required=True,
            obj=data_policies_sdk.EntityReference,
        ),
        attachment_type=dict(
            type="str",
            required=False,
            choices=["DIRECT", "EXTERNAL"],
        ),
        protocol=dict(
            type="str",
            required=False,
            choices=["ISCSI", "NVMF"],
        ),
        client_features=dict(
            type="dict",
            options=volume_group_client_features_spec,
            required=False,
            obj=volume_group_client_features_obj_map,
        ),
    )

    ip_mapping_spec = dict(
        network_mapping_ext_id=dict(type="str", required=True),
        primary_ip=dict(
            type="dict",
            options=_build_ip_address_spec(),
            required=False,
            obj=data_policies_sdk.IPAddress,
        ),
        recovery_ip=dict(
            type="dict",
            options=_build_ip_address_spec(),
            required=False,
            obj=data_policies_sdk.IPAddress,
        ),
        primary_test_ip=dict(
            type="dict",
            options=_build_ip_address_spec(),
            required=False,
            obj=data_policies_sdk.IPAddress,
        ),
        recovery_test_ip=dict(
            type="dict",
            options=_build_ip_address_spec(),
            required=False,
            obj=data_policies_sdk.IPAddress,
        ),
    )

    floating_ip_association_spec = dict(
        nic_ext_id=dict(type="str", required=True),
        primary_floating_ip=dict(
            type="dict",
            options=_build_floating_ip_spec(),
            required=False,
            obj=data_policies_sdk.FloatingIp,
        ),
        recovery_floating_ip=dict(
            type="dict",
            options=_build_floating_ip_spec(),
            required=False,
            obj=data_policies_sdk.FloatingIp,
        ),
        primary_test_floating_ip=dict(
            type="dict",
            options=_build_floating_ip_spec(),
            required=False,
            obj=data_policies_sdk.FloatingIp,
        ),
        recovery_test_floating_ip=dict(
            type="dict",
            options=_build_floating_ip_spec(),
            required=False,
            obj=data_policies_sdk.FloatingIp,
        ),
    )

    vm_recovery_setting_spec = dict(
        vm=dict(
            type="dict",
            options=entity_reference_spec,
            required=True,
            obj=data_policies_sdk.EntityReference,
        ),
        power_state=dict(type="str", required=False, choices=["ON", "OFF"]),
        in_guest_script_execution_config=dict(
            type="dict",
            options=in_guest_script_spec,
            required=False,
            obj=data_policies_sdk.InGuestScriptExecutionConfig,
        ),
        volume_group_attachments=dict(
            type="list",
            elements="dict",
            options=volume_group_attachment_spec,
            required=False,
            obj=data_policies_sdk.VolumeGroupAttachment,
        ),
        ip_mappings=dict(
            type="list",
            elements="dict",
            options=ip_mapping_spec,
            required=False,
            obj=data_policies_sdk.IpMapping,
        ),
        floating_ip_associations=dict(
            type="list",
            elements="dict",
            options=floating_ip_association_spec,
            required=False,
            obj=data_policies_sdk.FloatingIpAssociation,
        ),
    )

    vm_category_recovery_setting_spec = dict(
        vm_category_ext_id=dict(type="str", required=True),
        power_state=dict(type="str", required=False, choices=["ON", "OFF"]),
        in_guest_script_execution_config=dict(
            type="dict",
            options=in_guest_script_spec,
            required=False,
            obj=data_policies_sdk.InGuestScriptExecutionConfig,
        ),
    )

    volume_group_recovery_setting_spec = dict(
        volume_group=dict(
            type="dict",
            options=entity_reference_spec,
            required=True,
            obj=data_policies_sdk.EntityReference,
        ),
        iscsi_target_features=dict(
            type="dict",
            options=iscsi_features_spec,
            required=False,
            obj=data_policies_sdk.IscsiFeatures,
        ),
    )

    recovery_setting_obj_map = {
        "vm": data_policies_sdk.VmRecoverySetting,
        "vm_category": data_policies_sdk.VmCategoryRecoverySetting,
        "volume_group": data_policies_sdk.VolumeGroupRecoverySetting,
    }

    recovery_setting_spec = dict(
        vm=dict(
            type="dict",
            options=vm_recovery_setting_spec,
            required=False,
        ),
        vm_category=dict(
            type="dict",
            options=vm_category_recovery_setting_spec,
            required=False,
        ),
        volume_group=dict(
            type="dict",
            options=volume_group_recovery_setting_spec,
            required=False,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        recovery_plan_ext_id=dict(type="str", required=True),
        recovery_setting=dict(
            type="dict",
            options=recovery_setting_spec,
            required=False,
            obj=recovery_setting_obj_map,
        ),
    )
    return module_args


def create_recovery_setting(module, result, api_instance):
    validate_required_params(module, ["recovery_plan_ext_id", "recovery_setting"])
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")

    sg = SpecGenerator(module)
    default_spec = data_policies_sdk.RecoverySetting()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create recovery setting spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_recovery_setting(
            recoveryPlanExtId=recovery_plan_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating recovery setting",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.RECOVERY_SETTING
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_recovery_setting(
                module, api_instance, recovery_plan_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Recovery Setting"
                ),
                msg="Failed to get entity ext_id from task for Recovery Setting",
            )
    result["changed"] = True


def _check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_recovery_setting(module, result, api_instance):
    validate_required_params(module, ["recovery_plan_ext_id", "ext_id"])
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_recovery_setting(module, api_instance, recovery_plan_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating recovery setting", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update recovery setting spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Recovery setting with ext_id:{0} is already in the desired state. "
            "Nothing to change.".format(ext_id)
        )

    resp = None
    try:
        resp = api_instance.update_recovery_setting_by_id(
            recoveryPlanExtId=recovery_plan_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating recovery setting",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_recovery_setting(module, api_instance, recovery_plan_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_recovery_setting(module, result, api_instance):
    validate_required_params(module, ["recovery_plan_ext_id", "ext_id"])
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Recovery setting with ext_id:{0} on recovery plan {1} will be deleted.".format(
                ext_id, recovery_plan_ext_id
            )
        )
        return

    old_spec = get_recovery_setting(module, api_instance, recovery_plan_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_recovery_setting_by_id(
            recoveryPlanExtId=recovery_plan_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting recovery setting",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
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
    }
    api_instance = get_recovery_plans_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_recovery_setting(module, result, api_instance)
        else:
            create_recovery_setting(module, result, api_instance)
    else:
        delete_recovery_setting(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
