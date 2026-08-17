#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vnic_migrate_v2
short_description: Migrate a virtual NIC (vNIC) between subnets in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to migrate a virtual NIC (vNIC) between subnets in Nutanix Prism Central.
  - Migration is typically used to move a vNIC from the Acropolis (legacy) networking stack to the
    Atlas (advanced VLAN / VPC) stack, or vice-versa, without recreating the underlying interface.
  - The vNIC is identified by its external ID and re-attached to the destination subnet supplied via
    C(network_uuid).
  - Optionally, one or more C(requested_ip_addresses) may be passed to retain / request specific IPs
    on the destination subnet.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Migrate a vNIC to another subnet) -
    Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported since vNIC migration is an action, not a lifecycle CRUD operation.
    type: str
    required: false
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the vNIC to be migrated.
    type: str
    required: true
  network_uuid:
    description:
      - UUID of the destination subnet the vNIC will be re-attached to.
      - Required for the migrate operation.
    type: str
    required: true
  requested_ip_addresses:
    description:
      - Optional list of IP addresses to assign / retain on the vNIC after migration.
      - If omitted, IP assignment is left to the destination subnet's configuration.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address to assign on the destination subnet.
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
            default: 32
      ipv6:
        description:
          - IPv6 address to assign on the destination subnet.
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
              - Prefix length of the IPv6 address.
            type: int
            required: false
            default: 128
  project_ext_id:
    description:
      - External ID of the Prism Central project to associate with the migrated vNIC for
        multi-tenancy and RBAC purposes.
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
- name: Migrate vNIC to another subnet
  nutanix.ncp.ntnx_vnic_migrate_v2:
    state: present
    ext_id: "7147b563-7b80-4be5-96b5-d8ff63187a5c"
    network_uuid: "7131f3ca-47ce-4f1d-990c-fa17800bd94d"
    requested_ip_addresses:
      - ipv4:
          value: "10.51.144.137"
          prefix_length: 32
    project_ext_id: "8f0ed6e-30c8-48be-9c8f-e7cb4153416a"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for migrating a virtual NIC (vNIC) to another subnet.
    - If C(wait) is true, it will return the task details after successful task completion.
    - If C(wait) is false, it will return the task reference details returned by the API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T09:41:12.345000+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T09:40:47.123000+00:00",
      "entities_affected": [
          {
              "ext_id": "7147b563-7b80-4be5-96b5-d8ff63187a5c",
              "name": null,
              "rel": "networking:config:vnic"
          },
          {
              "ext_id": "7131f3ca-47ce-4f1d-990c-fa17800bd94d",
              "name": null,
              "rel": "networking:config:subnet"
          }
      ],
      "ext_id": "ZXJnb24=:cf1cdd41-2a5f-4dfe-9c31-6d05ba5f6d7a",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T09:41:12.345000+00:00",
      "legacy_error_message": null,
      "number_of_subtasks": 0,
      "operation": "MIGRATE_VNIC",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T09:40:47.500000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with the vNIC migrate operation.
  returned: always
  type: str
  sample: "ZXJnb24=:cf1cdd41-2a5f-4dfe-9c31-6d05ba5f6d7a"

ext_id:
  description:
    - The external ID of the vNIC that was migrated.
  returned: always
  type: str
  sample: "7147b563-7b80-4be5-96b5-d8ff63187a5c"

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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while migrating vNIC"
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

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        network_uuid=dict(type="str", required=True),
        requested_ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        project_ext_id=dict(type="str", required=False),
    )
    return module_args


def migrate_vnic(module, subnet_migrations_api, result):
    """Perform the vNIC migrate action.

    Builds a VnicMigrationItemSpec from the module parameters, invokes the
    networking v4 `migrate_vnic_by_id` API, and (optionally) waits for the
    resulting task to complete before returning.
    """
    validate_required_params(module, ["ext_id", "network_uuid"])

    vnic_ext_id = module.params.get("ext_id")
    result["ext_id"] = vnic_ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.VnicMigrationItemSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating migrate vNIC spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = subnet_migrations_api.migrate_vnic_by_id(extId=vnic_ext_id, body=spec)
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
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
        "skipped": False,
    }
    subnet_migrations_api = get_subnet_migrations_api_instance(module)
    migrate_vnic(module, subnet_migrations_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
