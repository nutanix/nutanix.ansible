#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_reserve_ips_by_subnet_id_v2
short_description: Reserve or unreserve IP addresses on a managed subnet in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to reserve or unreserve IP addresses on a managed subnet in Nutanix Prism Central.
  - This is an action-style module — a reservation does not have its own external ID.
  - When C(state=present) the module invokes the Reserve IPs API on the given subnet.
  - When C(state=absent) the module invokes the Unreserve IPs API on the given subnet.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Reserve IPs on a subnet) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Unreserve IPs on a subnet) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module will reserve IPs on the subnet identified by C(ext_id).
      - If C(state) is set to C(absent) the module will unreserve IPs on the subnet identified by C(ext_id).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the managed subnet on which IPs are (un)reserved.
      - Required for both reserve (C(state=present)) and unreserve (C(state=absent)) operations.
    type: str
    required: true
  count:
    description:
      - Number of IP addresses to reserve (when C(state=present)) or unreserve (when C(state=absent)).
      - Required when C(reserve_type=IP_ADDRESS_COUNT) on reserve.
    type: int
    required: false
  start_ip_address:
    description:
      - Starting IP address for range-based reserve / unreserve.
      - Required when C(reserve_type=IP_ADDRESS_RANGE) on reserve or C(unreserve_type=IP_ADDRESS_RANGE) on unreserve.
    type: dict
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
          - IPv6 address specification.
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
  ip_addresses:
    description:
      - Explicit list of IP addresses to reserve or unreserve.
      - Required when C(reserve_type=IP_ADDRESS_LIST) on reserve or C(unreserve_type=IP_ADDRESS_LIST) on unreserve.
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
          - IPv6 address specification.
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
  reserve_type:
    description:
      - How the caller wants to reserve IPs on the subnet.
      - Required for reserve operation (C(state=present)).
      - C(IP_ADDRESS_COUNT) reserves C(count) random free IPs.
      - C(IP_ADDRESS_LIST) reserves the explicit C(ip_addresses).
      - C(IP_ADDRESS_RANGE) reserves C(count) IPs starting from C(start_ip_address).
    type: str
    required: false
    choices:
      - IP_ADDRESS_COUNT
      - IP_ADDRESS_LIST
      - IP_ADDRESS_RANGE
  unreserve_type:
    description:
      - How the caller wants to unreserve IPs on the subnet.
      - Required for unreserve operation (C(state=absent)).
      - C(IP_ADDRESS_LIST) unreserves the explicit C(ip_addresses).
      - C(IP_ADDRESS_RANGE) unreserves C(count) IPs starting from C(start_ip_address).
      - C(CONTEXT) unreserves every IP tagged with the supplied C(client_context).
    type: str
    required: false
    choices:
      - IP_ADDRESS_LIST
      - IP_ADDRESS_RANGE
      - CONTEXT
  client_context:
    description:
      - Free-form string that the client can use to tag / correlate reserved IPs.
      - Required when C(unreserve_type=CONTEXT).
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
- name: Reserve a specific list of IPs on a managed subnet
  nutanix.ncp.ntnx_reserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    reserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "192.168.0.21"
      - ipv4:
          value: "192.168.0.22"
    client_context: "ansible_reserve_test"
  register: result

- name: Reserve N random IPs on a managed subnet
  nutanix.ncp.ntnx_reserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    reserve_type: IP_ADDRESS_COUNT
    count: 3
    client_context: "ansible_reserve_count"
  register: result

- name: Reserve a range of IPs starting from a given address
  nutanix.ncp.ntnx_reserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    reserve_type: IP_ADDRESS_RANGE
    start_ip_address:
      ipv4:
        value: "192.168.0.25"
    count: 2
    client_context: "ansible_reserve_range"
  register: result

- name: Unreserve a specific list of IPs
  nutanix.ncp.ntnx_reserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    unreserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "192.168.0.21"
      - ipv4:
          value: "192.168.0.22"
  register: result

- name: Unreserve every IP previously tagged with client_context
  nutanix.ncp.ntnx_reserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "9cc4abba-f27d-40db-90ba-c1592dccaedf"
    unreserve_type: CONTEXT
    client_context: "ansible_reserve_count"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the reserve / unreserve IP operation on the subnet.
    - When C(wait=true) this is the completed task payload from Prism Central.
    - When C(wait=false) this is the task reference returned by the SDK.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T05:51:41.861959+00:00",
      "completion_details": [
          {
              "name": "reserved_or_unreserved_ips",
              "value": "{\"reserved_ips\": [\"192.168.214.21\", \"192.168.214.22\"]}"
          }
      ],
      "created_time": "2026-07-21T05:51:41.730026+00:00",
      "entities_affected": [
          {
              "ext_id": "6be3e46b-794a-43f9-ab3e-04b94acf9f2e",
              "name": null,
              "rel": "networking:config:subnet"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:b7d0e296-5968-43b1-a14e-10480ba7191b",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T05:51:41.861958+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "kSubnetReserveIp",
      "operation_description": "Reserve or Unreserve IP on Managed Subnet",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-21T05:51:41.739554+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the Prism Central task created by the reserve / unreserve operation.
  returned: always
  type: str
  sample: "ZXJnb24=:b7d0e296-5968-43b1-a14e-10480ba7191b"

ext_id:
  description:
    - The external ID of the subnet on which IPs were reserved / unreserved.
  returned: always
  type: str
  sample: "6be3e46b-794a-43f9-ab3e-04b94acf9f2e"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped (e.g. check mode with no changes).
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
  description: Status / informational message from the module.
  returned: When there is an error or the module runs in check mode
  type: str
  sample: "Api Exception raised while reserving IPs on subnet"
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
        ext_id=dict(type="str", required=True),
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
        reserve_type=dict(
            type="str",
            required=False,
            choices=["IP_ADDRESS_COUNT", "IP_ADDRESS_LIST", "IP_ADDRESS_RANGE"],
            obj=networking_sdk.ReserveType,
        ),
        unreserve_type=dict(
            type="str",
            required=False,
            choices=["IP_ADDRESS_LIST", "IP_ADDRESS_RANGE", "CONTEXT"],
            obj=networking_sdk.UnreserveType,
        ),
        client_context=dict(type="str", required=False),
    )
    return module_args


def _validate_reserve_params(module):
    """Enforce SDK-level required combinations for reserve operation."""
    validate_required_params(module, ["reserve_type"])
    reserve_type = module.params.get("reserve_type")
    if reserve_type == "IP_ADDRESS_COUNT":
        validate_required_params(module, ["count"])
    elif reserve_type == "IP_ADDRESS_LIST":
        validate_required_params(module, ["ip_addresses"])
    elif reserve_type == "IP_ADDRESS_RANGE":
        validate_required_params(module, ["start_ip_address", "count"])


def _validate_unreserve_params(module):
    """Enforce SDK-level required combinations for unreserve operation."""
    validate_required_params(module, ["unreserve_type"])
    unreserve_type = module.params.get("unreserve_type")
    if unreserve_type == "IP_ADDRESS_LIST":
        validate_required_params(module, ["ip_addresses"])
    elif unreserve_type == "IP_ADDRESS_RANGE":
        validate_required_params(module, ["start_ip_address", "count"])
    elif unreserve_type == "CONTEXT":
        validate_required_params(module, ["client_context"])


def create_ReserveIpsBySubnetId(module, result, api_instance):
    """Reserve IPs on the target subnet (state=present)."""
    subnet_ext_id = module.params.get("ext_id")
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
        result["msg"] = "IPs will be reserved on subnet ext_id: {0}".format(
            subnet_ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.reserve_ips_by_subnet_id(extId=subnet_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reserving IPs on subnet",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_ReserveIpsBySubnetId(module, result, api_instance):
    """Unreserve IPs on the target subnet (state=absent)."""
    subnet_ext_id = module.params.get("ext_id")
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
        result["msg"] = "IPs will be unreserved on subnet ext_id: {0}".format(
            subnet_ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.unreserve_ips_by_subnet_id(extId=subnet_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unreserving IPs on subnet",
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
        required_if=[
            ("state", "present", ("reserve_type",)),
            ("state", "absent", ("unreserve_type",)),
        ],
        mutually_exclusive=[
            ("reserve_type", "unreserve_type"),
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
        create_ReserveIpsBySubnetId(module, result, api_instance)
    else:
        delete_ReserveIpsBySubnetId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
