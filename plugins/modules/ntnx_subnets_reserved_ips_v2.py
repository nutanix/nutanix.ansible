#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_subnets_reserved_ips_v2
short_description: Reserve and unreserve IP addresses on a managed subnet in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module reserves and unreserves IP addresses on a managed subnet in Nutanix Prism Central.
  - When C(state) is C(present), it reserves IPs
  - When C(state) is C(absent), it unreserves IPs
  - Reserved IPs are excluded from automatic IPAM allocations for the target subnet.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Reserve IP addresses on a subnet) -
    Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Super Admin,
    Tenant Admin, VPC Admin
  - >-
    B(Unreserve IP addresses on a subnet) -
    Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Super Admin,
    Tenant Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is C(present), reserve IP addresses on the subnet.
      - If C(state) is C(absent), unreserve IP addresses on the subnet.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  subnet_ext_id:
    description:
      - External ID (UUID) of the managed subnet on which IPs are reserved or unreserved.
      - Required for all operations.
    type: str
    required: true
  reserve_type:
    description:
      - Strategy used to select which IPs to reserve. Used when C(state=present).
      - C(IP_ADDRESS_COUNT) reserves C(count) free IPs from the pool.
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
      - C(IP_ADDRESS_LIST) unreserves the explicit list of C(ip_addresses).
      - C(IP_ADDRESS_RANGE) unreserves C(count) consecutive IPs starting from C(start_ip_address).
      - C(CONTEXT) unreserves every IP tagged with the same C(client_context).
    type: str
    required: false
    choices:
      - IP_ADDRESS_LIST
      - IP_ADDRESS_RANGE
      - CONTEXT
  count:
    description:
      - Number of IP addresses to reserve or unreserve.
      - Required when C(reserve_type) is C(IP_ADDRESS_COUNT) or C(IP_ADDRESS_RANGE),
        or when C(unreserve_type) is C(IP_ADDRESS_RANGE).
    type: int
    required: false
  start_ip_address:
    description:
      - Starting IP address for a range reserve or unreserve.
      - Required when C(reserve_type) or C(unreserve_type) is C(IP_ADDRESS_RANGE).
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
              - The IPv4 address value in dotted decimal notation.
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
      - Required when C(reserve_type) or C(unreserve_type) is C(IP_ADDRESS_LIST).
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
              - The IPv4 address value in dotted decimal notation.
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
  client_context:
    description:
      - Opaque label attached to the reservation.
      - Required when C(unreserve_type) is C(CONTEXT).
      - Length must be between 1 and 64 characters when set.
    type: str
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
- name: Reserve 2 IPs from the pool
  nutanix.ncp.ntnx_subnets_reserved_ips_v2:
    state: present
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    reserve_type: IP_ADDRESS_COUNT
    count: 2
    client_context: "ansible-count"
  register: result
  ignore_errors: true

- name: Reserve an explicit list of IPs
  nutanix.ncp.ntnx_subnets_reserved_ips_v2:
    state: present
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    reserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "10.30.30.81"
      - ipv4:
          value: "10.30.30.82"
    client_context: "ansible-list"
  register: result
  ignore_errors: true

- name: Reserve a range of IPs
  nutanix.ncp.ntnx_subnets_reserved_ips_v2:
    state: present
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    reserve_type: IP_ADDRESS_RANGE
    start_ip_address:
      ipv4:
        value: "10.30.30.80"
    count: 3
    client_context: "ansible-range"
  register: result
  ignore_errors: true

- name: Unreserve a specific list of IPs
  nutanix.ncp.ntnx_subnets_reserved_ips_v2:
    state: absent
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    unreserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "10.30.30.81"
      - ipv4:
          value: "10.30.30.82"
  register: result
  ignore_errors: true

- name: Unreserve a range of IPs
  nutanix.ncp.ntnx_subnets_reserved_ips_v2:
    state: absent
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    unreserve_type: IP_ADDRESS_RANGE
    start_ip_address:
      ipv4:
        value: "10.30.30.80"
    count: 3
  register: result
  ignore_errors: true

- name: Unreserve every IP tagged with a client context
  nutanix.ncp.ntnx_subnets_reserved_ips_v2:
    state: absent
    subnet_ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    unreserve_type: CONTEXT
    client_context: "ansible-context-tag"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the reserve or unreserve action.
    - When C(wait) is true, this is the completed task object as returned by the tasks API.
    - When C(wait) is false, this is the task reference returned immediately by the API call.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-21T06:35:24.224345+00:00",
      "completion_details": [
        {
          "name": "reserved_or_unreserved_ips",
          "value": "{\"unreserved_ips\": [\"10.30.30.75\", \"10.30.30.76\"]}"
        }
      ],
      "created_time": "2026-07-21T06:35:24.115619+00:00",
      "entities_affected": [
        {
          "ext_id": "61959708-6efc-4d80-8c86-92c01f080672",
          "name": null,
          "rel": "networking:config:subnet"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:521746d7-f26f-4652-b5fb-1b38c89a1dca",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T06:35:24.224344+00:00",
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
      "started_time": "2026-07-21T06:35:24.129524+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null
    }

ext_id:
  description:
    - External ID (UUID) of the subnet the action was performed against.
  returned: always
  type: str
  sample: "61959708-6efc-4d80-8c86-92c01f080672"

task_ext_id:
  description:
    - The external ID of the reserve or unreserve task.
  returned: always
  type: str
  sample: "ZXJnb24=:521746d7-f26f-4652-b5fb-1b38c89a1dca"

changed:
  description: This indicates whether the action resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the status/error message if any occurred.
  returned: When there is an error or in check mode.
  type: str
  sample: "Api Exception raised while reserving IPs on subnet"

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
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
            choices=["IP_ADDRESS_LIST", "IP_ADDRESS_RANGE", "CONTEXT"],
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


def reserve_ips(module, result, api_instance):
    """Reserve IP addresses on the subnet identified by ``subnet_ext_id``."""
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["ext_id"] = subnet_ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.IpReserveSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for reserving IPs on subnet", **result
        )

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
            msg="Api Exception raised while reserving IPs on subnet",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def unreserve_ips(module, result, api_instance):
    """Unreserve IP addresses on the subnet identified by ``subnet_ext_id``."""
    subnet_ext_id = module.params.get("subnet_ext_id")
    result["ext_id"] = subnet_ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.IpUnreserveSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for unreserving IPs on subnet", **result
        )

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
            msg="Api Exception raised while unreserving IPs on subnet",
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
            ("reserve_type", "IP_ADDRESS_COUNT", ("count",)),
            ("reserve_type", "IP_ADDRESS_LIST", ("ip_addresses",)),
            ("reserve_type", "IP_ADDRESS_RANGE", ("start_ip_address", "count")),
            ("unreserve_type", "IP_ADDRESS_LIST", ("ip_addresses",)),
            ("unreserve_type", "IP_ADDRESS_RANGE", ("start_ip_address", "count")),
            ("unreserve_type", "CONTEXT", ("client_context",)),
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
        reserve_ips(module, result, api_instance)
    else:
        unreserve_ips(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
