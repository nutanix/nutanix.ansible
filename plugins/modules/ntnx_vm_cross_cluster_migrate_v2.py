#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_cross_cluster_migrate_v2
short_description: Migrate a VM across clusters
version_added: "2.7.0"
description:
    - Migrates a VM from the current cluster to a new target cluster.
    - Supports the dry-run option, which if used results only in validation of the cross-cluster
      migration parameters and pre-requisites.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Migrate a VM across clusters) -
      Required Roles: Backup Admin, Project Admin, Project Manager, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    target_availability_zone:
        description:
            - Reference to an availability zone.
        type: dict
        required: true
        suboptions:
            ext_id:
                description:
                    - The globally unique identifier of an availability zone type UUID.
                type: str
                required: true
    target_cluster:
        description:
            - Reference to a cluster.
        type: dict
        required: false
        suboptions:
            ext_id:
                description:
                    - The globally unique identifier of a cluster type UUID.
                type: str
                required: true
    is_live_migration:
        description:
            - Indicates if the migration is performed with a running VM.
        type: bool
        required: true
    should_migrate_storage:
        description:
            - Indicates if the VM storage is to be migrated to the target cluster or not.
        type: bool
        required: false
    overrides:
        description:
            - Cross cluster migration overrides the VM configuration.
        type: dict
        required: false
        suboptions:
            override_nic_list:
                description:
                    - The NIC configuration to apply on the target cluster when migrating a VM from the source
                      cluster to the target cluster.
                type: list
                elements: dict
                required: false
                suboptions:
                    backing_info:
                        description:
                            - Defines a NIC emulated by the hypervisor.
                        type: dict
                        required: false
                        suboptions:
                            model:
                                description:
                                    - Options for the NIC emulation.
                                type: str
                                required: false
                                choices:
                                    - VIRTIO
                                    - E1000
                            mac_address:
                                description:
                                    - MAC address of the NIC.
                                type: str
                                required: false
                            is_connected:
                                description:
                                    - Indicates whether the NIC is connected or not.
                                type: bool
                                required: false
                            num_queues:
                                description:
                                    - The number of Tx/Rx queue pairs for this NIC.
                                type: int
                                required: false
                    nic_backing_info:
                        description:
                            - Information about how NIC is associated with a VM.
                        type: dict
                        required: false
                        suboptions:
                            virtual_ethernet_nic:
                                description:
                                    - Defines a Virtual Ethernet NIC.
                                type: dict
                                required: false
                                suboptions:
                                    model:
                                        description:
                                            - Options for the NIC emulation.
                                        type: str
                                        required: false
                                        choices:
                                            - VIRTIO
                                            - E1000
                                    mac_address:
                                        description:
                                            - MAC address of the NIC.
                                        type: str
                                        required: false
                                    is_connected:
                                        description:
                                            - Indicates whether the NIC is connected or not.
                                        type: bool
                                        required: false
                                    num_queues:
                                        description:
                                            - The number of Tx/Rx queue pairs for this NIC.
                                        type: int
                                        required: false
                    network_info:
                        description:
                            - Networking information object for a NIC.
                        type: dict
                        required: false
                        suboptions:
                            nic_type:
                                description:
                                    - Type of the NIC.
                                type: str
                                required: false
                                choices:
                                    - NORMAL_NIC
                                    - DIRECT_NIC
                                    - NETWORK_FUNCTION_NIC
                                    - SPAN_DESTINATION_NIC
                            network_function_chain:
                                description:
                                    - Reference to a network function chain.
                                type: dict
                                required: false
                                suboptions:
                                    ext_id:
                                        description:
                                            - External identifier of the network function chain.
                                        type: str
                                        required: true
                            network_function_nic_type:
                                description:
                                    - Type of the network function NIC.
                                type: str
                                required: false
                                choices:
                                    - INGRESS
                                    - EGRESS
                                    - TAP
                            subnet:
                                description:
                                    - Reference to a subnet.
                                type: dict
                                required: false
                                suboptions:
                                    ext_id:
                                        description:
                                            - External identifier of the subnet.
                                        type: str
                                        required: true
                            vlan_mode:
                                description:
                                    - VLAN mode for the NIC.
                                type: str
                                required: false
                                choices:
                                    - ACCESS
                                    - TRUNK
                            trunked_vlans:
                                description:
                                    - List of networks to trunk if VLAN mode is marked as TRUNKED.
                                    - If empty and VLAN mode is set to TRUNKED, all the VLANs are trunked.
                                type: list
                                elements: int
                                required: false
                            should_allow_unknown_macs:
                                description:
                                    - Indicates whether an unknown unicast traffic is forwarded to this NIC or not.
                                    - This is applicable only for the NICs on the overlay subnets.
                                type: bool
                                required: false
                            ipv4_config:
                                description:
                                    - The IP address configurations.
                                type: dict
                                required: false
                                suboptions:
                                    should_assign_ip:
                                        description:
                                            - If set to true, an IP address must be assigned to the VM NIC.
                                            - If false, then no IP assignment is required for this VM NIC.
                                        type: bool
                                        required: false
                                    ip_address:
                                        description:
                                            - The IP address configurations.
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
                                                type: int
                                                required: false
                                    secondary_ip_address_list:
                                        description:
                                            - Secondary IP address configurations.
                                        type: list
                                        elements: dict
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
                                                type: int
                                                required: false
                    nic_network_info:
                        description:
                            - Networking information object for a NIC.
                        type: dict
                        required: false
                        suboptions:
                            virtual_ethernet_nic_network_info:
                                description:
                                    - Networking information object for a Virtual Ethernet NIC.
                                type: dict
                                required: false
                                suboptions:
                                    nic_type:
                                        description:
                                            - Type of the NIC.
                                        type: str
                                        required: false
                                        choices:
                                            - NORMAL_NIC
                                            - DIRECT_NIC
                                            - NETWORK_FUNCTION_NIC
                                            - SPAN_DESTINATION_NIC
                                    network_function_chain:
                                        description:
                                            - Reference to a network function chain.
                                        type: dict
                                        required: false
                                        suboptions:
                                            ext_id:
                                                description:
                                                    - External identifier of the network function chain.
                                                type: str
                                                required: true
                                    network_function_nic_type:
                                        description:
                                            - Type of the network function NIC.
                                        type: str
                                        required: false
                                        choices:
                                            - INGRESS
                                            - EGRESS
                                            - TAP
                                    subnet:
                                        description:
                                            - Reference to a subnet.
                                        type: dict
                                        required: false
                                        suboptions:
                                            ext_id:
                                                description:
                                                    - External identifier of the subnet.
                                                type: str
                                                required: true
                                    vlan_mode:
                                        description:
                                            - VLAN mode for the NIC.
                                        type: str
                                        required: false
                                        choices:
                                            - ACCESS
                                            - TRUNK
                                    trunked_vlans:
                                        description:
                                            - List of networks to trunk if VLAN mode is marked as TRUNKED.
                                            - If empty and VLAN mode is set to TRUNKED, all the VLANs are trunked.
                                        type: list
                                        elements: int
                                        required: false
                                    should_allow_unknown_macs:
                                        description:
                                            - Indicates whether an unknown unicast traffic is forwarded to this NIC
                                              or not.
                                            - This is applicable only for the NICs on the overlay subnets.
                                        type: bool
                                        required: false
                                    ipv4_config:
                                        description:
                                            - The IP address configurations.
                                        type: dict
                                        required: false
                                        suboptions:
                                            should_assign_ip:
                                                description:
                                                    - If set to true, an IP address must be assigned to the VM NIC.
                                                    - If false, then no IP assignment is required for this VM NIC.
                                                type: bool
                                                required: false
                                            ip_address:
                                                description:
                                                    - The IP address configurations.
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
                                                        type: int
                                                        required: false
                                            secondary_ip_address_list:
                                                description:
                                                    - Secondary IP address configurations.
                                                type: list
                                                elements: dict
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
                                                        type: int
                                                        required: false
            storage_containers_mapping:
                description:
                    - This optional field specifies the storage container mapping to apply when migrating a VM from
                      the source cluster to the target cluster.
                    - It is supported on un-protected VMs only.
                type: list
                elements: dict
                required: false
                suboptions:
                    source_storage_container:
                        description:
                            - This reference is for disk level storage container preference.
                            - This preference specifies the storage container to which this disk belongs.
                        type: dict
                        required: false
                        suboptions:
                            ext_id:
                                description:
                                    - A globally unique identifier of a VM disk container. It should be of type UUID.
                                type: str
                                required: true
                    target_storage_container:
                        description:
                            - This reference is for disk level storage container preference.
                            - This preference specifies the storage container to which this disk belongs.
                        type: dict
                        required: false
                        suboptions:
                            ext_id:
                                description:
                                    - A globally unique identifier of a VM disk container. It should be of type UUID.
                                type: str
                                required: true
    dryrun:
        description:
            - A URL query parameter that allows long running operations to execute in a dry-run mode providing ability
              to identify trouble spots and system failures without performing the actual operation.
            - The operation runs in dry-run mode only if the provided value is true.
        type: bool
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
- name: Migrate a VM across clusters
  nutanix.ncp.ntnx_vm_cross_cluster_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "129e835e-56c6-4948-ac88-737527740f97"
    target_availability_zone:
      ext_id: "df69a24b-fd65-4c0e-be09-78071ad984ee"
    target_cluster:
      ext_id: "8341930a-cf3d-4ef1-8cfa-694a7b0f99a4"
    is_live_migration: false
  register: result

- name: Live migrate a VM across clusters with overrides
  nutanix.ncp.ntnx_vm_cross_cluster_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "129e835e-56c6-4948-ac88-737527740f97"
    target_availability_zone:
      ext_id: "df69a24b-fd65-4c0e-be09-78071ad984ee"
    target_cluster:
      ext_id: "8341930a-cf3d-4ef1-8cfa-694a7b0f99a4"
    is_live_migration: true
    should_migrate_storage: true
    overrides:
      override_nic_list:
        - nic_backing_info:
            virtual_ethernet_nic:
              model: VIRTIO
              is_connected: true
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
  register: result

- name: Validate a cross-cluster migration in dry-run mode
  nutanix.ncp.ntnx_vm_cross_cluster_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "129e835e-56c6-4948-ac88-737527740f97"
    target_availability_zone:
      ext_id: "df69a24b-fd65-4c0e-be09-78071ad984ee"
    is_live_migration: false
    dryrun: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for migrate a VM across clusters.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
            "status": "SUCCEEDED",
            "operation": "CrossClusterMigrateVm",
            "progress_percentage": 100
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
    description: The external ID of the VM.
    type: str
    returned: always
    sample: "129e835e-56c6-4948-ac88-737527740f97"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "VM with ext_id:129e835e-56c6-4948-ac88-737527740f97 will be cross-cluster migrated."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
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
        ),
        target_storage_container=dict(
            type="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigVmDiskContainerReference,
        ),
    )

    overrides_spec = dict(
        override_nic_list=dict(
            type="list",
            elements="dict",
            options=vm_specs.nic_spec,
            obj=vmm_sdk.AhvConfigNic,
        ),
        storage_containers_mapping=dict(
            type="list",
            elements="dict",
            options=storage_container_mapping_spec,
            obj=vmm_sdk.StorageContainerMapping,
        ),
    )

    module_args = dict(
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
        ),
        is_live_migration=dict(type="bool", required=True),
        should_migrate_storage=dict(type="bool"),
        overrides=dict(
            type="dict",
            options=overrides_spec,
            obj=vmm_sdk.VmCrossClusterMigrateOverrides,
        ),
        dryrun=dict(type="bool"),
    )
    return module_args


def cross_cluster_migrate_vm(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

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
    etag = get_etag(data=vm)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for cross-cluster migrating VM", **result
        )

    kwargs = {"if_match": etag}
    dryrun = module.params.get("dryrun")
    if dryrun is not None:
        kwargs["_dryrun"] = dryrun

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
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }
    api_instance = get_vm_api_instance(module)
    cross_cluster_migrate_vm(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
