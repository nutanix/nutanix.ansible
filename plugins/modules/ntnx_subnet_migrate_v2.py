#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnet_migrate_v2
short_description: Migrate VLAN subnets or vNICs in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to migrate networking resources in Nutanix Prism Central.
  - It supports two action-type operations exposed by the Subnet Migrations v4 API.
  - >-
    Migrate one or more VLAN subnets from VLAN basic mode to VLAN advanced mode
    (Flow / Advanced Networking) by supplying their subnet UUIDs.
  - >-
    Migrate a virtual NIC (vNIC) from Acropolis-managed networking to Atlas
    (or vice-versa) by supplying the vNIC C(vnic_ext_id) and the destination network.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Migrate Subnet) -
    Required Roles: Network Infra Admin, Prism Admin, Super Admin
  - >-
    B(Migrate VNIC) -
    Required Roles: Network Infra Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported since subnet and vNIC migration are actions,
        not lifecycle CRUD operations.
    type: str
    required: false
    choices:
      - present
    default: present
  vnic_ext_id:
    description:
      - UUID of the NIC to be migrated.
      - When provided, the module will invoke the Migrate VNIC API instead of
        migrating subnets.
      - Required for the vNIC migration operation.
    type: str
    required: false
  subnets:
    description:
      - VLAN subnet details that need to be migrated from VLAN basic to VLAN advanced.
      - Required for the Migrate Subnet operation (when C(vnic_ext_id) is not set).
    type: list
    elements: dict
    required: false
    suboptions:
      subnet_uuid:
        description:
          - UUID of the subnet to be migrated.
        type: str
        required: true
  network_uuid:
    description:
      - NIC network UUID for the destination subnet.
      - Used only for the Migrate VNIC operation.
      - Required when C(vnic_ext_id) is set.
    type: str
    required: false
  requested_ip_addresses:
    description:
      - Optional list of IP addresses to assign or retain on the vNIC after migration.
      - API allows at most one IP address entry.
      - Used only for the Migrate VNIC operation.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address specification.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv4 address of the host.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix length of the network to which this host IPv4 address belongs.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address specification.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv6 address of the host.
            type: str
            required: true
          prefix_length:
            description:
              - The prefix length of the network to which this host IPv6 address belongs.
            type: int
            required: false
            default: 128
  metadata:
    description:
      - Metadata associated with this resource.
      - Used only for the Migrate VNIC operation.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
      owner_user_name:
        description:
          - The userName of the owner of this resource.
        type: str
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
      project_name:
        description:
          - The name of the project this resource belongs to.
        type: str
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str
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
- name: Migrate a VLAN basic subnet to VLAN advanced
  nutanix.ncp.ntnx_subnet_migrate_v2:
    state: present
    subnets:
      - subnet_uuid: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
  register: result

- name: Migrate multiple VLAN basic subnets to VLAN advanced
  nutanix.ncp.ntnx_subnet_migrate_v2:
    state: present
    subnets:
      - subnet_uuid: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
      - subnet_uuid: "b8f5f8ea-2c1c-4b1a-a2f8-9a20b32b5f2f"
  register: result

- name: Migrate a vNIC to a different destination subnet
  nutanix.ncp.ntnx_subnet_migrate_v2:
    state: present
    vnic_ext_id: "7147b563-7b80-4be5-96b5-d8ff63187a5c"
    network_uuid: "18f0ed6e-30c8-48be-9c8f-e7cb4153416a"
    requested_ip_addresses:
      - ipv4:
          value: "10.51.144.137"
          prefix_length: 32
  register: result

- name: Migrate VLAN subnets without waiting for task completion
  nutanix.ncp.ntnx_subnet_migrate_v2:
    subnets:
      - subnet_uuid: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    wait: false
  register: result
"""

RETURN = r"""
response:
  description:
    - Response of the subnet or vNIC migration operation.
    - If C(wait) is true, it returns the completed task details (see sample).
    - If C(wait) is false, it returns the task submission details (task reference).
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T06:06:35.405168+00:00",
      "completion_details": [
          {
              "name": "migration_info",
              "value": "{\"<subnet-uuid>\": {\"status\": \"Succeeded\", \"subnet_name\": \"...\", \"cluster_name\": \"...\"}}"
          }
      ],
      "created_time": "2026-07-21T06:06:32.082314+00:00",
      "entities_affected": null,
      "error_messages": null,
      "ext_id": "ZXJnb24=:68c6d622-1fe2-4c0d-a628-7ee12404371b",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:06:35.405167+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 0,
      "number_of_subtasks": 0,
      "operation": "kVlanSubnetMigration",
      "operation_description": "VLAN Basic to VLAN subnet migration",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "project_ext_id": "00000000-0000-0000-0000-000000000000",
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-07-21T06:06:32.094975+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the asynchronous task associated with this migration.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the primary entity impacted by the migration.
    - For subnet migration, the UUID of the first migrated subnet.
    - For vNIC migration, the UUID of the migrated vNIC.
  returned: always
  type: str
  sample: "9cc4abba-f27d-40db-90ba-c1592dccaedf"

changed:
  description: This indicates whether the migration resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: The error details, if any, encountered during the operation.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the module failed.
  returned: always
  type: bool
  sample: false

msg:
  description: A status or error message describing the outcome of the operation.
  returned: When there is an error, or during check mode
  type: str
  sample: "Api Exception raised while migrating VLAN subnets"
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
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        vnic_ext_id=dict(type="str", required=False),
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


def migrate_subnets(module, api_instance, result):
    """Trigger the MigrateSubnets action (VLAN basic -> VLAN advanced)."""
    validate_required_params(module, ["subnets"])

    sg = SpecGenerator(module)
    default_spec = networking_sdk.VlanSubnetMigrationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating subnet migration spec", **result)

    subnet_uuids = [s.get("subnet_uuid") for s in module.params.get("subnets") or []]
    if subnet_uuids:
        result["ext_id"] = subnet_uuids[0]

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
            msg="Api Exception raised while migrating VLAN subnets",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def migrate_vnic(module, api_instance, result):
    """Trigger the MigrateVnicById action for the provided vNIC ext_id."""
    validate_required_params(module, ["vnic_ext_id", "network_uuid"])

    vnic_ext_id = module.params.get("vnic_ext_id")
    result["ext_id"] = vnic_ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.VnicMigrationItemSpec()
    # Path param C(vnic_ext_id) is not a body field; keep unrelated keys out of the body.
    attr = dict(module.params)
    attr.pop("vnic_ext_id", None)
    spec, err = sg.generate_spec(obj=default_spec, attr=attr)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating migrate vNIC spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.migrate_vnic_by_id(extId=vnic_ext_id, body=spec)
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
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ("vnic_ext_id", "subnets"),
        ],
        required_one_of=[
            ("vnic_ext_id", "subnets"),
        ],
        required_by={
            "network_uuid": ("vnic_ext_id",),
            "requested_ip_addresses": ("vnic_ext_id",),
            "metadata": ("vnic_ext_id",),
        },
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_subnet_migrations_api_instance(module)

    if module.params.get("vnic_ext_id"):
        migrate_vnic(module, api_instance, result)
    else:
        migrate_subnets(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
