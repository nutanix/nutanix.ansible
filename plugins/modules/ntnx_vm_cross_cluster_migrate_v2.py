#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_cross_cluster_migrate_v2
short_description: Migrate an AHV VM across clusters (On-Demand Cross-Cluster Migration)
version_added: 2.5.0
description:
  - This module triggers an on-demand Cross-Cluster VM Migration (OD-CCLM) for an AHV VM
    registered under a Nutanix Prism Central.
  - The VM identified by C(ext_id) is migrated to a target cluster located in the specified
    availability zone. When C(is_live_migration) is true the migration is performed while
    the VM is running (Cross-Cluster Live Migration).
  - Optional NIC and storage container overrides are applied on the target cluster.
  - This is an action-type module. It invokes the SDK method C(cross_cluster_migrate_vm)
    (POST /api/vmm/v4.2/ahv/config/vms/{extId}/$actions/migrate).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Cross-Cluster Migrate a VM) -
    Required Roles: Prism Admin, Super Admin, Virtual Machine Admin, Project Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported. The module triggers the migrate action.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the VM to be migrated across clusters.
      - Required for the migrate action.
    type: str
    required: true
  target_availability_zone:
    description:
      - Reference to the target availability zone (Prism Central) that hosts the
        destination cluster.
      - This attribute is required by the API.
    type: dict
    required: true
    suboptions:
      ext_id:
        description:
          - The globally unique identifier of the target availability zone.
        type: str
        required: true
  target_cluster:
    description:
      - Reference to the target cluster on which the VM will be created after migration.
      - When omitted, the platform may choose an appropriate cluster in the target
        availability zone based on placement policies.
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - The globally unique identifier of the target cluster.
        type: str
        required: true
  is_live_migration:
    description:
      - When C(true), the migration is performed while the VM is powered on
        (Cross-Cluster Live Migration).
      - When C(false), the VM is migrated in a powered-off (cold) state.
      - This attribute is required by the API.
    type: bool
    required: true
  overrides:
    description:
      - Optional per-VM overrides that alter the migrated VM configuration on the
        target cluster.
    type: dict
    required: false
    suboptions:
      override_nic_list:
        description:
          - List of NIC entries whose backing / network configuration must be
            replaced on the target cluster (e.g. remap to a different subnet).
        type: list
        elements: dict
        required: false
        suboptions:
          backing_info:
            description:
              - Deprecated backing information for the NIC. Prefer C(nic_backing_info).
            type: dict
            required: false
            suboptions:
              model:
                description: Model of the emulated NIC.
                type: str
                required: false
                choices:
                  - VIRTIO
                  - E1000
              mac_address:
                description: MAC address of the NIC.
                type: str
                required: false
              is_connected:
                description: Whether the NIC should be connected.
                type: bool
                required: false
              num_queues:
                description: Number of queues for the NIC.
                type: int
                required: false
          nic_backing_info:
            description:
              - Backing information about how the NIC is associated with a VM.
            type: dict
            required: false
            suboptions:
              virtual_ethernet_nic:
                description: Virtual ethernet NIC configuration.
                type: dict
                required: false
                suboptions:
                  model:
                    description: Model of the virtual ethernet NIC.
                    type: str
                    required: false
                    choices:
                      - VIRTIO
                      - E1000
                  mac_address:
                    description: MAC address of the NIC.
                    type: str
                    required: false
                  is_connected:
                    description: Whether the NIC should be connected.
                    type: bool
                    required: false
                  num_queues:
                    description: Number of queues for the NIC.
                    type: int
                    required: false
          network_info:
            description:
              - Deprecated network configuration for the NIC. Prefer C(nic_network_info).
            type: dict
            required: false
            suboptions:
              nic_type:
                description: Type of the NIC.
                type: str
                required: false
                choices:
                  - NORMAL_NIC
                  - DIRECT_NIC
                  - NETWORK_FUNCTION_NIC
                  - SPAN_DESTINATION_NIC
              network_function_chain:
                description: Network function chain reference.
                type: dict
                required: false
                suboptions:
                  ext_id:
                    description: External ID of the network function chain.
                    type: str
                    required: true
              network_function_nic_type:
                description: Type of the network function NIC.
                type: str
                required: false
                choices:
                  - INGRESS
                  - EGRESS
                  - TAP
              subnet:
                description: Subnet on the target cluster to which the NIC must attach.
                type: dict
                required: false
                suboptions:
                  ext_id:
                    description: External ID of the subnet on the target cluster.
                    type: str
                    required: true
              vlan_mode:
                description: VLAN mode for the NIC.
                type: str
                required: false
                choices:
                  - ACCESS
                  - TRUNK
              trunked_vlans:
                description: List of trunked VLAN IDs when C(vlan_mode) is TRUNK.
                type: list
                elements: int
                required: false
              should_allow_unknown_macs:
                description: Whether unknown MAC addresses are allowed on the NIC.
                type: bool
                required: false
              ipv4_config:
                description: IPv4 configuration for the NIC on the target cluster.
                type: dict
                required: false
                suboptions:
                  should_assign_ip:
                    description: Whether an IP should be auto-assigned.
                    type: bool
                    required: false
                  ip_address:
                    description: Static IPv4 address for the NIC.
                    type: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv4 address value.
                        type: str
                        required: true
                      prefix_length:
                        description: Prefix length of the IPv4 address.
                        type: int
                        required: false
                  secondary_ip_address_list:
                    description: Secondary IPv4 addresses for the NIC.
                    type: list
                    elements: dict
                    required: false
                    suboptions:
                      value:
                        description: The IPv4 address value.
                        type: str
                        required: true
                      prefix_length:
                        description: Prefix length of the IPv4 address.
                        type: int
                        required: false
          nic_network_info:
            description:
              - Network configuration for the NIC.
            type: dict
            required: false
            suboptions:
              virtual_ethernet_nic_network_info:
                description: Network configuration for a virtual ethernet NIC.
                type: dict
                required: false
                suboptions:
                  nic_type:
                    description: Type of the NIC.
                    type: str
                    required: false
                    choices:
                      - NORMAL_NIC
                      - DIRECT_NIC
                      - NETWORK_FUNCTION_NIC
                      - SPAN_DESTINATION_NIC
                  network_function_chain:
                    description: Network function chain reference.
                    type: dict
                    required: false
                    suboptions:
                      ext_id:
                        description: External ID of the network function chain.
                        type: str
                        required: true
                  network_function_nic_type:
                    description: Type of the network function NIC.
                    type: str
                    required: false
                    choices:
                      - INGRESS
                      - EGRESS
                      - TAP
                  subnet:
                    description: Subnet on the target cluster to which the NIC must attach.
                    type: dict
                    required: false
                    suboptions:
                      ext_id:
                        description: External ID of the subnet on the target cluster.
                        type: str
                        required: true
                  vlan_mode:
                    description: VLAN mode for the NIC.
                    type: str
                    required: false
                    choices:
                      - ACCESS
                      - TRUNK
                  trunked_vlans:
                    description: List of trunked VLAN IDs when C(vlan_mode) is TRUNK.
                    type: list
                    elements: int
                    required: false
                  should_allow_unknown_macs:
                    description: Whether unknown MAC addresses are allowed on the NIC.
                    type: bool
                    required: false
                  ipv4_config:
                    description: IPv4 configuration for the NIC on the target cluster.
                    type: dict
                    required: false
                    suboptions:
                      should_assign_ip:
                        description: Whether an IP should be auto-assigned.
                        type: bool
                        required: false
                      ip_address:
                        description: Static IPv4 address for the NIC.
                        type: dict
                        required: false
                        suboptions:
                          value:
                            description: The IPv4 address value.
                            type: str
                            required: true
                          prefix_length:
                            description: Prefix length of the IPv4 address.
                            type: int
                            required: false
                      secondary_ip_address_list:
                        description: Secondary IPv4 addresses for the NIC.
                        type: list
                        elements: dict
                        required: false
                        suboptions:
                          value:
                            description: The IPv4 address value.
                            type: str
                            required: true
                          prefix_length:
                            description: Prefix length of the IPv4 address.
                            type: int
                            required: false
      storage_containers_mapping:
        description:
          - Optional mapping between source and target storage containers to use
            when placing the migrated VM disks on the target cluster.
          - Applied only to unprotected VMs.
        type: list
        elements: dict
        required: false
        suboptions:
          source_storage_container:
            description:
              - Reference to the storage container on the source cluster.
            type: dict
            required: true
            suboptions:
              ext_id:
                description: External ID of the source storage container.
                type: str
                required: true
          target_storage_container:
            description:
              - Reference to the storage container on the target cluster.
            type: dict
            required: true
            suboptions:
              ext_id:
                description: External ID of the target storage container.
                type: str
                required: true
  dry_run:
    description:
      - When C(true) the migrate action is executed in dry-run mode. The API validates
        the request and reports pre-check results without performing the actual
        migration.
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
- name: Cold-migrate an AHV VM to a target cluster in another availability zone
  nutanix.ncp.ntnx_vm_cross_cluster_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    target_availability_zone:
      ext_id: "7d994cce-72d8-4993-833c-c44c3e642ae3"
    target_cluster:
      ext_id: "000631e1-8c6f-c066-0110-89e97c4a7603"
    is_live_migration: false
  register: result

- name: Live-migrate an AHV VM with NIC and storage container overrides
  nutanix.ncp.ntnx_vm_cross_cluster_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    target_availability_zone:
      ext_id: "7d994cce-72d8-4993-833c-c44c3e642ae3"
    target_cluster:
      ext_id: "000631e1-8c6f-c066-0110-89e97c4a7603"
    is_live_migration: true
    overrides:
      override_nic_list:
        - nic_backing_info:
            virtual_ethernet_nic:
              model: VIRTIO
              is_connected: true
              num_queues: 1
          nic_network_info:
            virtual_ethernet_nic_network_info:
              nic_type: NORMAL_NIC
              subnet:
                ext_id: "9306c8d3-bb00-4b98-b354-ef2dfbd2c7ba"
              vlan_mode: ACCESS
      storage_containers_mapping:
        - source_storage_container:
            ext_id: "77c1d0c6-aa90-4fdd-a63d-1eca02cbaaed"
          target_storage_container:
            ext_id: "5007f144-f2f9-48d7-a47f-9f8739d55045"

- name: Validate a cross-cluster migration in dry-run mode
  nutanix.ncp.ntnx_vm_cross_cluster_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    target_availability_zone:
      ext_id: "7d994cce-72d8-4993-833c-c44c3e642ae3"
    is_live_migration: false
    dry_run: true
"""

RETURN = r"""
response:
  description:
    - Response for the cross-cluster VM migration task.
    - If C(wait) is true, the task details are returned after completion.
    - If C(wait) is false, the initial task submission response is returned.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2",
        "000631e1-8c6f-c066-0110-89e97c4a7603"
      ],
      "completed_time": "2026-04-14T00:00:00.000000+00:00",
      "completion_details": null,
      "created_time": "2026-04-14T00:00:00.000000+00:00",
      "entities_affected": [
        {
          "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
          "rel": "vmm:ahv:config:vm"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "is_cancelable": false,
      "last_updated_time": "2026-04-14T00:00:00.000000+00:00",
      "legacy_error_message": null,
      "operation": "CrossClusterMigrateVm",
      "operation_description": "Cross-cluster migrate VM",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-04-14T00:00:00.000000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with the migrate operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID (UUID) of the source VM being migrated.
  returned: always
  type: str
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"

changed:
  description:
    - Indicates whether the task resulted in any changes.
    - Always C(true) for a successful (non check-mode) migrate action.
  returned: always
  type: bool
  sample: true

skipped:
  description: Indicates whether the operation was skipped.
  returned: when applicable
  type: bool
  sample: false

failed:
  description: Indicates whether the module failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Contextual status or error message emitted by the module.
    - Set on validation failures, API failures and in check mode.
  returned: When there is an error, in check mode or when a status message is emitted
  type: str
  sample: "Api Exception raised while cross-cluster migrating VM"

error:
  description:
    - Error details, if any, encountered while executing the migrate action.
  returned: When an error occurs
  type: str
  sample: "Failed generating cross-cluster migrate VM spec"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    storage_container_mapping_spec = dict(
        source_storage_container=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigVmDiskContainerReference,
            required=True,
        ),
        target_storage_container=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigVmDiskContainerReference,
            required=True,
        ),
    )

    overrides_spec = dict(
        override_nic_list=dict(
            type="list",
            elements="dict",
            options=vm_specs.nic_spec,
            obj=vmm_sdk.AhvConfigNic,
            required=False,
        ),
        storage_containers_mapping=dict(
            type="list",
            elements="dict",
            options=storage_container_mapping_spec,
            obj=vmm_sdk.StorageContainerMapping,
            required=False,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        target_availability_zone=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.AvailabilityZoneReference,
            required=True,
        ),
        target_cluster=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigClusterReference,
            required=False,
        ),
        is_live_migration=dict(type="bool", required=True),
        overrides=dict(
            type="dict",
            options=overrides_spec,
            obj=vmm_sdk.VmCrossClusterMigrateOverrides,
            required=False,
        ),
        dry_run=dict(type="bool", required=False),
    )
    return module_args


def cross_cluster_migrate_vm(module, result, api_instance):
    """Trigger the cross-cluster migrate action for a VM.

    This is an action-type operation on the VmApi. The VM identified by
    C(ext_id) is submitted for migration to the target availability zone
    / target cluster with the supplied overrides.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(
        module, ["ext_id", "target_availability_zone", "is_live_migration"]
    )

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmCrossClusterMigrateParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cross-cluster migrate VM spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "VM with ext_id:{0} will be cross-cluster migrated.".format(
            ext_id
        )
        return

    vm = get_vm(module, api_instance, ext_id)
    etag = get_etag(vm)
    if not etag:
        module.fail_json(
            msg="Failed to fetch eTag for VM {0} required by cross-cluster migrate".format(
                ext_id
            ),
            **result,
        )

    kwargs = {"if_match": etag}
    dry_run = module.params.get("dry_run")
    if dry_run is not None:
        kwargs["_dryrun"] = dry_run

    resp = None
    try:
        resp = api_instance.cross_cluster_migrate_vm(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while cross-cluster migrating VM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    cross_cluster_migrate_vm(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
