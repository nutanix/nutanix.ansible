#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnet_migrate_v2
short_description: Migrate VLAN subnets and vNICs in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to trigger subnet-migration actions in Nutanix Prism Central.
  - If C(state) is C(present) and C(ext_id) is not provided, the module submits a
    bulk migration of one or more VLAN Basic subnets to VLAN Advanced using the
    C(migrate-subnets) action.
  - If C(state) is C(present) and C(ext_id) is provided, the module migrates the
    virtual NIC identified by C(ext_id) to a different subnet using the
    C(vnics/{extId}/migrate) action.
  - This module uses PC v4 APIs based SDKs.
notes:
    - This module models actions (POST). It does not manage a persistent resource,
      so C(state=absent) is not supported and will fail with a clear message.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, the operation
        will be a bulk VLAN subnet migration.
      - If C(state) is set to C(present) and C(ext_id) is provided, the operation
        will be a single vNIC migration where C(ext_id) is the vNIC UUID.
      - C(state=absent) is not supported for subnet migration actions.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External ID (UUID) of the virtual NIC to migrate.
      - When provided, the module invokes the vNIC migration action and C(network_uuid)
        MUST also be set to identify the destination subnet.
    type: str
    required: false
  subnets:
    description:
      - List of VLAN Basic subnets to migrate to VLAN Advanced.
      - Required for the bulk subnet-migration operation
        (i.e., C(state=present) with no C(ext_id)).
    type: list
    elements: dict
    required: false
    suboptions:
      subnet_uuid:
        description:
          - UUID of the source VLAN Basic subnet to be migrated.
        type: str
        required: true
  network_uuid:
    description:
      - UUID of the destination subnet for the vNIC being migrated.
      - Required for the vNIC migration operation (i.e., C(state=present) with C(ext_id)).
    type: str
    required: false
  requested_ip_addresses:
    description:
      - Optional list of IP addresses to request on the destination subnet for
        the migrated vNIC.
      - The API accepts at most one entry in this list.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address to request on the destination subnet.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv4 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv4 address.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address to request on the destination subnet.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the IPv6 address.
            type: int
            required: false
            default: 128
  metadata:
    description:
      - Metadata to attach to the migrated vNIC (only used with vNIC migration).
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - External ID of the owner of the vNIC.
        type: str
        required: false
      project_reference_id:
        description:
          - External ID of the project the vNIC is associated with.
        type: str
        required: false
      category_ids:
        description:
          - List of category external IDs associated with the vNIC.
        type: list
        elements: str
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
- name: Migrate a list of VLAN Basic subnets to VLAN Advanced
  nutanix.ncp.ntnx_subnet_migrate_v2:
    state: present
    subnets:
      - subnet_uuid: "5b5b8f0e-1b6a-4d2b-8a3f-1a2b3c4d5e6f"
      - subnet_uuid: "7c9e2b1d-2c4a-4d1a-9f2b-2a3c4d5e6f7a"
  register: result

- name: Migrate a single vNIC to a different subnet
  nutanix.ncp.ntnx_subnet_migrate_v2:
    state: present
    ext_id: "d3f1c2a4-5b6a-4d2b-8a3f-1a2b3c4d5e6f"
    network_uuid: "9c8b7a6d-5e4f-4a3b-9c2d-1e2f3a4b5c6d"
    requested_ip_addresses:
      - ipv4:
          value: "10.0.0.10"

- name: Migrate a single vNIC with metadata and a requested IP
  nutanix.ncp.ntnx_subnet_migrate_v2:
    state: present
    ext_id: "d3f1c2a4-5b6a-4d2b-8a3f-1a2b3c4d5e6f"
    network_uuid: "9c8b7a6d-5e4f-4a3b-9c2d-1e2f3a4b5c6d"
    requested_ip_addresses:
      - ipv4:
          value: "10.0.0.10"
    metadata:
      category_ids:
        - "6b48c37c-7c9b-4c1a-9d1c-1a2b3c4d5e6f"
"""

RETURN = r"""
response:
  description:
    - Response for the subnet migration operation.
    - If C(wait) is true, this holds the completed task details.
    - If C(wait) is false, this holds the initial task-reference payload
      returned by the API.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-07-19T12:42:35.182591+00:00",
      "completion_details": [
        {
          "name": "migration_info",
          "value": "{\"5b5b8f0e-1b6a-4d2b-8a3f-1a2b3c4d5e6f\": {\"status\": \"Success\"}}"
        }
      ],
      "created_time": "2026-07-19T12:42:35.015696+00:00",
      "entities_affected": null,
      "error_messages": null,
      "ext_id": "ZXJnb24=:36d176ec-cb84-41e1-85bc-7ef5d6991629",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-19T12:42:35.182590+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "kVlanSubnetMigration",
      "operation_description": "VLAN Basic to VLAN subnet migration",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-07-19T12:42:35.026449+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task created for the migration operation.
  returned: always
  type: str
  sample: "ZXJnb24=:c9d1b7a4-6f4b-4a2b-9c1e-1a2b3c4d5e6f"

ext_id:
  description:
    - External ID of the migrated vNIC (only when the vNIC migration action is invoked).
    - Empty / null for the bulk subnet migration operation.
  returned: always
  type: str
  sample: "d3f1c2a4-5b6a-4d2b-8a3f-1a2b3c4d5e6f"

changed:
  description:
    - This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Returned when the operation was skipped because there was nothing to do
      (for example, no subnets supplied in the input).
  returned: when applicable
  type: str
  sample: "No subnets supplied. Skipping migration."

error:
  description:
    - This indicates the error message if any error occurred during the operation.
  returned: When an error occurs
  type: str

failed:
  description:
    - This indicates whether the operation failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - This indicates the status/error message for the operation.
  returned: When there is an error, module is idempotent or in check mode
  type: str
  sample: "Api Exception raised while migrating subnets"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_subnet_migrations_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

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
            required=False,
            obj=networking_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=networking_sdk.IPv6Address,
        ),
    )

    subnet_info_spec = dict(
        subnet_uuid=dict(type="str", required=True),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        subnets=dict(
            type="list",
            elements="dict",
            options=subnet_info_spec,
            required=False,
            obj=networking_sdk.SubnetInfo,
        ),
        network_uuid=dict(type="str", required=False),
        requested_ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            required=False,
            obj=networking_sdk.Metadata,
        ),
    )
    return module_args


def _wait_task(module, task_ext_id, result):
    """Wait for the migration task and populate result with the final task data."""
    task = wait_for_completion(module, task_ext_id)
    result["response"] = strip_internal_attributes(task.to_dict())
    return task


def create_Subnet(module, result, api_instance):
    """Perform the bulk VLAN subnet migration (MigrateSubnets action).

    This corresponds to the "create" branch of the state dispatcher:
    C(state=present) with no C(ext_id). It converts C(subnets) into a
    VlanSubnetMigrationSpec body and calls the SDK's migrate_subnets action.
    """
    validate_required_params(module, ["subnets"])

    if not module.params.get("subnets"):
        result["skipped"] = "No subnets supplied. Skipping migration."
        result["changed"] = False
        module.exit_json(**result)

    sg = SpecGenerator(module)
    default_spec = networking_sdk.VlanSubnetMigrationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating subnet migration spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.migrate_subnets(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating subnets",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        _wait_task(module, task_ext_id, result)

    result["changed"] = True


def update_Subnet(module, result, api_instance):
    """Perform the vNIC migration (MigrateVnicById action).

    This corresponds to the "update" branch of the state dispatcher:
    C(state=present) with an C(ext_id). The C(ext_id) is the vNIC UUID
    and C(network_uuid) is the destination subnet UUID.
    """
    validate_required_params(module, ["ext_id", "network_uuid"])

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.VnicMigrationItemSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vNIC migration spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.migrate_vnic_by_id(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating vNIC",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        _wait_task(module, task_ext_id, result)

    result["changed"] = True


def delete_Subnet(module, result, api_instance):
    """Not applicable — subnet migration is an action (POST), not a resource.

    The state-dispatcher pattern mandates a delete branch, but there is no
    corresponding DELETE endpoint in the SubnetMigrationsApi. We fail cleanly
    so the caller gets a descriptive error rather than a silent no-op.
    """
    del api_instance
    result["msg"] = (
        "state=absent is not supported for subnet migration actions. "
        "This module models POST actions (MigrateSubnets, MigrateVnicById) "
        "and does not manage a persistent resource."
    )
    result["failed"] = True
    module.fail_json(**result)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
        required_together=[
            ("ext_id", "network_uuid"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "error": None,
    }

    api_instance = get_subnet_migrations_api_instance(module)

    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_Subnet(module, result, api_instance)
        else:
            create_Subnet(module, result, api_instance)
    else:
        delete_Subnet(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
