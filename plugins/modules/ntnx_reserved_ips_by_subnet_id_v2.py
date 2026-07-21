#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_reserved_ips_by_subnet_id_v2
short_description: Reserve and unreserve IP addresses on a managed subnet in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to reserve and unreserve IP addresses on a managed subnet in Nutanix Prism Central.
  - When C(state) is C(present), it reserves IPs on the subnet.
  - When C(state) is C(absent), it unreserves IPs on the subnet.
  - Reserved IPs are excluded from automatic IPAM allocations for the target subnet.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Reserve IPs on a Subnet) -
    Required Roles/Permissions: Reserve_Subnet_Ip. VPC Admin and Network Infra Admin roles include this by default.
  - >-
    B(Unreserve IPs on a Subnet) -
    Required Roles/Permissions: Unreserve_Subnet_Ip. VPC Admin and Network Infra Admin roles include this by default.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) the operation reserves IP addresses on the subnet.
      - If C(state) is set to C(absent) the operation unreserves IP addresses on the subnet.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  subnet_ext_id:
    description:
      - The external ID (UUID) of the managed subnet on which IPs are reserved / unreserved.
      - Required for all operations.
    type: str
    required: true
  reserve_type:
    description:
      - Strategy used to select which IPs to reserve. Used when C(state=present).
      - C(IP_ADDRESS_COUNT) reserves the requested C(count) of random free IPs.
      - C(IP_ADDRESS_LIST) reserves the explicit list of C(ip_addresses).
      - C(IP_ADDRESS_RANGE) reserves C(count) consecutive IPs starting from C(start_ip_address).
    type: str
    required: false
    choices:
      - IP_ADDRESS_COUNT
      - IP_ADDRESS_LIST
      - IP_ADDRESS_RANGE
  unreserve_type:
    description:
      - Strategy used to select which IPs to unreserve. Used when C(state=absent).
      - C(CONTEXT) unreserves every IP tagged with the same C(client_context).
      - C(IP_ADDRESS_LIST) unreserves the explicit list of C(ip_addresses).
      - C(IP_ADDRESS_RANGE) unreserves C(count) consecutive IPs starting from C(start_ip_address).
    type: str
    required: false
    choices:
      - CONTEXT
      - IP_ADDRESS_LIST
      - IP_ADDRESS_RANGE
  count:
    description:
      - Number of IP addresses to reserve (with C(IP_ADDRESS_COUNT) / C(IP_ADDRESS_RANGE))
        or unreserve (with C(IP_ADDRESS_RANGE)).
    type: int
    required: false
  start_ip_address:
    description:
      - Starting IP address for the reservation / unreservation.
      - Required when C(reserve_type) or C(unreserve_type) is C(IP_ADDRESS_RANGE).
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
              - IPv4 address value.
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
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the network.
            type: int
            required: false
            default: 128
  ip_addresses:
    description:
      - Explicit list of IP addresses to reserve / unreserve.
      - Required when C(reserve_type) or C(unreserve_type) is C(IP_ADDRESS_LIST).
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
              - IPv4 address value.
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
              - IPv6 address value.
            type: str
            required: true
          prefix_length:
            description:
              - Prefix length of the network.
            type: int
            required: false
            default: 128
  client_context:
    description:
      - Optional opaque label attached to the reservation.
      - When C(unreserve_type) is C(CONTEXT) every IP tagged with the same value is unreserved.
      - Must be between 1 and 64 characters when set.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Reserve 2 random IPs on a managed subnet
  nutanix.ncp.ntnx_reserved_ips_by_subnet_id_v2:
    state: present
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    reserve_type: IP_ADDRESS_COUNT
    count: 2
    client_context: "ansible-count"
  register: reserve_count_result

- name: Reserve an explicit list of IPv4 addresses
  nutanix.ncp.ntnx_reserved_ips_by_subnet_id_v2:
    state: present
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    reserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "10.44.10.50"
      - ipv4:
          value: "10.44.10.51"
    client_context: "ansible-list"
  register: reserve_list_result

- name: Reserve a consecutive range of IPs
  nutanix.ncp.ntnx_reserved_ips_by_subnet_id_v2:
    state: present
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    reserve_type: IP_ADDRESS_RANGE
    start_ip_address:
      ipv4:
        value: "10.44.10.100"
    count: 5
    client_context: "ansible-range"
  register: reserve_range_result

- name: Unreserve every IP tagged with a client context
  nutanix.ncp.ntnx_reserved_ips_by_subnet_id_v2:
    state: absent
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    unreserve_type: CONTEXT
    client_context: "ansible-count"

- name: Unreserve an explicit list of IPs
  nutanix.ncp.ntnx_reserved_ips_by_subnet_id_v2:
    state: absent
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    unreserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "10.44.10.50"
      - ipv4:
          value: "10.44.10.51"

- name: Unreserve a consecutive range of IPs
  nutanix.ncp.ntnx_reserved_ips_by_subnet_id_v2:
    state: absent
    subnet_ext_id: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"
    unreserve_type: IP_ADDRESS_RANGE
    start_ip_address:
      ipv4:
        value: "10.44.10.100"
    count: 5
"""

RETURN = r"""
response:
  description:
    - Response for the reserve or unreserve IPs operation.
    - When C(wait) is true, the task status is returned once the operation completes.
    - When C(wait) is false, the intermediate task reference is returned.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": ["00062db1-4470-e5e0-4c22-ac1f6b3d4e5f"],
      "completed_time": "2026-07-21T05:35:52.001Z",
      "completion_details": null,
      "created_time": "2026-07-21T05:35:51.010Z",
      "entities_affected": [
        {
          "ext_id": "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d",
          "name": null,
          "rel": "networking:config:subnet"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:15b0c8ff-4a3c-4d1d-9d8b-6acd3b0b1122",
      "last_updated_time": "2026-07-21T05:35:52.010Z",
      "legacy_error_message": null,
      "number_of_subtasks": 0,
      "operation": "ReserveIps",
      "operation_description": "Reserve IP addresses on a subnet",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T05:35:51.020Z",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null
    }

task_ext_id:
  description:
    - The external ID of the reserve / unreserve task.
  returned: always
  type: str
  sample: "ZXJnb24=:15b0c8ff-4a3c-4d1d-9d8b-6acd3b0b1122"

ext_id:
  description:
    - The external ID of the subnet targeted by the reservation.
  returned: always
  type: str
  sample: "3b2f4e40-4d99-4d33-9e70-93a3c8412d6d"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (currently only in check mode delete).
  returned: when applicable
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while reserving IP addresses on subnet"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_subnet_ip_reservation_api_instance,
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

    module_args = dict(
        subnet_ext_id=dict(type="str", required=True),
        reserve_type=dict(
            type="str",
            required=False,
            choices=["IP_ADDRESS_COUNT", "IP_ADDRESS_LIST", "IP_ADDRESS_RANGE"],
            obj=networking_sdk.ReserveType,
        ),
        unreserve_type=dict(
            type="str",
            required=False,
            choices=["CONTEXT", "IP_ADDRESS_LIST", "IP_ADDRESS_RANGE"],
            obj=networking_sdk.UnreserveType,
        ),
        count=dict(type="int", required=False),
        start_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        ip_addresses=dict(
            type="list",
            elements="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        client_context=dict(type="str", required=False),
    )
    return module_args


def _validate_reserve_params(module):
    """
    Validate that the caller supplied the fields required by the chosen
    reserve_type. The SDK enforces this at server side too but a local
    check gives a clearer error early.
    """
    validate_required_params(module, ["reserve_type"])
    reserve_type = module.params.get("reserve_type")
    if reserve_type == "IP_ADDRESS_COUNT":
        validate_required_params(module, ["count"])
    elif reserve_type == "IP_ADDRESS_LIST":
        validate_required_params(module, ["ip_addresses"])
    elif reserve_type == "IP_ADDRESS_RANGE":
        validate_required_params(module, ["count", "start_ip_address"])


def _validate_unreserve_params(module):
    """
    Validate that the caller supplied the fields required by the chosen
    unreserve_type. Server-side validation still applies.
    """
    validate_required_params(module, ["unreserve_type"])
    unreserve_type = module.params.get("unreserve_type")
    if unreserve_type == "CONTEXT":
        validate_required_params(module, ["client_context"])
    elif unreserve_type == "IP_ADDRESS_LIST":
        validate_required_params(module, ["ip_addresses"])
    elif unreserve_type == "IP_ADDRESS_RANGE":
        validate_required_params(module, ["count", "start_ip_address"])


def create_ReservedIpsBySubnetId(module, result, api_instance):
    """
    Reserve IP addresses on the subnet identified by ``subnet_ext_id``.
    Maps to the SubnetIPReservationApi.reserve_ips_by_subnet_id SDK method.
    """
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["ext_id"] = subnet_ext_id

    _validate_reserve_params(module)

    sg = SpecGenerator(module)
    default_spec = networking_sdk.IpReserveSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating reserve IPs spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.reserve_ips_by_subnet_id(extId=subnet_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reserving IP addresses on subnet",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def update_ReservedIpsBySubnetId(module, result, api_instance):
    """
    The SubnetIPReservationApi does not expose an update semantic — every
    write path is either "reserve" (add reservations) or "unreserve" (remove
    reservations). We keep this function to match the module layout expected
    by the code-gen instructions and route it to reserve so a caller that
    provides a subnet ext_id with C(state=present) still performs a valid
    reserve operation.
    """
    create_ReservedIpsBySubnetId(module, result, api_instance)


def delete_ReservedIpsBySubnetId(module, result, api_instance):
    """
    Unreserve IP addresses on the subnet identified by ``subnet_ext_id``.
    Maps to the SubnetIPReservationApi.unreserve_ips_by_subnet_id SDK method.
    """
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["ext_id"] = subnet_ext_id

    _validate_unreserve_params(module)

    sg = SpecGenerator(module)
    default_spec = networking_sdk.IpUnreserveSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating unreserve IPs spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Reserved IPs on subnet with ext_id:{0} will be unreserved.".format(
                subnet_ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.unreserve_ips_by_subnet_id(extId=subnet_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unreserving IP addresses on subnet",
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
            ("reserve_type", "unreserve_type"),
        ],
        required_if=[
            ("state", "present", ("reserve_type",)),
            ("state", "absent", ("unreserve_type",)),
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
    }
    api_instance = get_subnet_ip_reservation_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ReservedIpsBySubnetId(module, result, api_instance)
        else:
            create_ReservedIpsBySubnetId(module, result, api_instance)
    else:
        delete_ReservedIpsBySubnetId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
