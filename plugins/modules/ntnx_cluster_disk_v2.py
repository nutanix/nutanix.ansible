#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_disk_v2
short_description: Add, update LED state or remove a Disk from a cluster in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to add a physical disk to a cluster, update the LED
    state of a disk, or remove a disk from a cluster in Nutanix Prism Central.
  - Add-disk requires the target cluster external ID and the physical disk serial
    number; the disk is repartitioned and added to the cluster.
  - Update operation toggles the physical disk locator LED state (on/off) so a
    field engineer can identify the drive in the chassis.
  - Delete marks the disk for removal from the cluster; the platform drains data
    off the drive before it becomes safely detachable.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation. The required roles depend on the operation
    being performed.
  - >-
    B(Add a Disk to a cluster) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Update Disk LED state) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Remove a Disk from a cluster) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, the
        operation will add a new Disk to the cluster identified by
        C(cluster_ext_id).
      - If C(state) is set to C(present) and C(ext_id) is provided, the
        operation will update the Disk LED state.
      - If C(state) is set to C(absent) and C(ext_id) is provided, the
        operation will remove the Disk from its cluster.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Disk.
      - Required for update (LED state) and delete operations.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the cluster on which the Disk will be added.
      - Required for the add-disk (create) operation.
    type: str
    required: false
  serial_number:
    description:
      - The physical disk serial number that identifies the drive to be added
        to the cluster.
      - Required for the add-disk (create) operation.
    type: str
    required: false
  disk_partition_info:
    description:
      - Optional partitioning information used while adding a disk to a
        cluster. When omitted, the platform defaults are used.
    type: dict
    required: false
    suboptions:
      partition_type:
        description:
          - The filesystem partition type to be created on the disk.
        type: str
        required: false
        choices:
          - EXT4
          - XFS
      drive_replacement_option:
        description:
          - Indicates whether the disk is being added as an RMA replacement of
            an existing drive or as part of a capacity upgrade.
        type: str
        required: false
        choices:
          - CAPACITY_UPGRADE
          - RMA
  is_engaged:
    description:
      - Indicates the desired LED state of the Disk. Set to C(true) to turn
        the locator LED on, C(false) to turn it off.
      - Required for the update (LED state) operation.
    type: bool
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Add a Disk to a cluster with minimal spec
  nutanix.ncp.ntnx_cluster_disk_v2:
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    serial_number: "S3Z1NB0M600001"
  register: result
  ignore_errors: true

- name: Add a Disk to a cluster with full spec
  nutanix.ncp.ntnx_cluster_disk_v2:
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    serial_number: "S3Z1NB0M600002"
    disk_partition_info:
      partition_type: "EXT4"
      drive_replacement_option: "CAPACITY_UPGRADE"
  register: result
  ignore_errors: true

- name: Turn Disk locator LED on
  nutanix.ncp.ntnx_cluster_disk_v2:
    state: present
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    is_engaged: true
  register: result
  ignore_errors: true

- name: Turn Disk locator LED off
  nutanix.ncp.ntnx_cluster_disk_v2:
    state: present
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    is_engaged: false
  register: result
  ignore_errors: true

- name: Remove a Disk from its cluster
  nutanix.ncp.ntnx_cluster_disk_v2:
    state: absent
    ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for adding, updating LED state, or removing a Disk.
    - If the operation is add-disk and C(wait) is true, it will return the Disk
      details.
    - If the operation is add-disk and C(wait) is false, it will return the
      task details.
    - If the operation is update LED state or delete, and C(wait) is true, it
      will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "000653ea-e2f2-ee30-0000-000000019bcd",
      "cluster_name": "auto_cluster_prod_f6b78dc0aa70",
      "cvm_ip_address": {
        "ipv4": {"prefix_length": 32, "value": "10.46.137.52"},
        "ipv6": null
      },
      "disk_advance_config": {
        "has_boot_partitions_only": false,
        "is_boot_disk": false,
        "is_data_migrated": false,
        "is_diagnostic_info_available": false,
        "is_error_found_in_log": false,
        "is_marked_for_removal": false,
        "is_mounted": true,
        "is_online": true,
        "is_password_protected": null,
        "is_planned_outage": false,
        "is_self_encrypting_drive": false,
        "is_self_managed_nvme": false,
        "is_spdk_managed": false,
        "is_suspected_unhealthy": false,
        "is_under_diagnosis": false,
        "is_unhealthy": false
      },
      "disk_size_bytes": 1900344033280,
      "ext_id": "2a4b79a6-2cb0-470c-88c1-49f3d81d37de",
      "firmware_version": "TN04",
      "host_name": "Beerus-4",
      "links": null,
      "location": 2,
      "model": "ST2000NM0055-1V4104",
      "mount_path": "/home/nutanix/data/stargate-storage/disks/ZC22T3DW",
      "node_ext_id": "4ef8c07f-ec03-40dc-b277-e81c306899b0",
      "node_ip_address": {
        "ipv4": {"prefix_length": 32, "value": "10.46.137.48"},
        "ipv6": null
      },
      "nvme_pcie_path": null,
      "physical_capacity_bytes": 2000398934016,
      "serial_number": "ZC22T3DW",
      "service_vm_id": "000653ea-e2f2-ee30-0000-000000019bcd::3",
      "status": "NORMAL",
      "storage_pool_ext_id": "c5c0459e-a94f-4d32-8caf-363a58422905",
      "storage_tier": "DAS_SATA",
      "target_firmware_version": "TN04",
      "tenant_id": null,
      "vendor": "Not Available"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0b36021e-6e2c-45c9-4727-6e1809ef0b4d"

ext_id:
  description:
    - The external ID of the Disk.
  returned: always
  type: str
  sample: "2a4b79a6-2cb0-470c-88c1-49f3d81d37de"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. LED state is
    already the desired one).
  returned: When applicable
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Disk with ext_id:62cd8f7a-9f0f-4a26-b1ab-2f0a72c48d0e will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_disks_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_disk  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
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
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    disk_partition_info_spec = dict(
        partition_type=dict(
            type="str",
            required=False,
            choices=["EXT4", "XFS"],
        ),
        drive_replacement_option=dict(
            type="str",
            required=False,
            choices=["CAPACITY_UPGRADE", "RMA"],
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=False),
        serial_number=dict(type="str", required=False),
        disk_partition_info=dict(
            type="dict",
            options=disk_partition_info_spec,
            required=False,
            obj=cluster_management_sdk.DiskPartitionInfo,
        ),
        is_engaged=dict(type="bool", required=False),
    )
    return module_args


def create_Disk(module, result, api_instance):
    """Add a Disk to a cluster."""
    validate_required_params(module, ["cluster_ext_id", "serial_number"])

    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.DiskAdditionSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating add Disk spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.add_disk(extId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding Disk to cluster {0}".format(
                cluster_ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.DISK
        )
        if ext_id:
            result["ext_id"] = ext_id
            disk = get_disk(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(disk.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception("Failed to get entity ext_id from task for Disk"),
                msg="Failed to get entity ext_id from task for Disk after add-disk",
            )
    result["changed"] = True


def update_Disk(module, result, api_instance):
    """Update the LED state of an existing Disk.

    The GET Disk API does not expose the current LED state, so an
    idempotency check cannot be based on it. To avoid firing repeated
    write requests, the module verifies the target Disk exists via
    GET-by-ext_id and forwards the desired LED state to the platform,
    which itself treats a same-state request as a no-op.
    """
    validate_required_params(module, ["ext_id", "is_engaged"])

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    is_engaged = module.params.get("is_engaged")

    current_disk = get_disk(module, api_instance, ext_id)

    if module.check_mode:
        led_spec = cluster_management_sdk.LEDStateUpdationSpec()
        led_spec.is_engaged = is_engaged
        result["response"] = strip_internal_attributes(led_spec.to_dict())
        return

    etag = get_etag(data=current_disk)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    led_spec = cluster_management_sdk.LEDStateUpdationSpec()
    led_spec.is_engaged = is_engaged

    resp = None
    try:
        resp = api_instance.update_disk_led_state(extId=ext_id, body=led_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating LED state of Disk {0}".format(
                ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        disk = get_disk(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(disk.to_dict())
    result["changed"] = True


def delete_Disk(module, result, api_instance):
    """Remove a Disk from its cluster."""
    validate_required_params(module, ["ext_id"])

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Disk with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_disk_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while removing Disk {0}".format(ext_id),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=False)
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
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_disks_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_Disk(module, result, api_instance)
        else:
            create_Disk(module, result, api_instance)
    else:
        delete_Disk(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
