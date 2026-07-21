#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unreserve_ips_by_subnet_id_v2
short_description: Unreserve IP addresses on a managed subnet in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to unreserve IP addresses on a managed subnet in Nutanix Prism Central.
  - The unreserve action supports three modes selected via C(unreserve_type).
  - C(IP_ADDRESS_LIST) releases a specific list of previously reserved IPs.
  - C(IP_ADDRESS_RANGE) releases C(count) consecutive IPs starting from C(start_ip_address).
  - C(CONTEXT) releases every reservation that was originally created with the supplied C(client_context) tag.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Unreserve IP addresses on a subnet) -
    Required Roles: Account Owner, Administrator, Prism Admin, Project Admin, Super Admin, VPC Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module performs the unreserve action against the given subnet.
      - C(absent) is not supported for this action module and will fail with a descriptive error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External ID (UUID) of the subnet on which the IP addresses are unreserved.
      - Required for the unreserve action.
    type: str
    required: true
  unreserve_type:
    description:
      - Selects the unreserve mode.
      - C(IP_ADDRESS_LIST) requires C(ip_addresses).
      - C(IP_ADDRESS_RANGE) requires C(start_ip_address) and C(count).
      - C(CONTEXT) requires C(client_context).
    type: str
    required: true
    choices:
      - IP_ADDRESS_LIST
      - IP_ADDRESS_RANGE
      - CONTEXT
  count:
    description:
      - Number of IP addresses to unreserve.
      - Required when C(unreserve_type) is C(IP_ADDRESS_RANGE).
      - Ignored for other unreserve types.
    type: int
    required: false
  start_ip_address:
    description:
      - Starting IP address of the range to unreserve.
      - Required when C(unreserve_type) is C(IP_ADDRESS_RANGE).
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
      - Explicit list of IP addresses to unreserve.
      - Required when C(unreserve_type) is C(IP_ADDRESS_LIST).
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
      - The client context tag originally used to reserve the IPs.
      - Required when C(unreserve_type) is C(CONTEXT).
      - Every reservation that was created with this tag on the given subnet is released.
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
- name: Unreserve a specific list of IPs from a subnet
  nutanix.ncp.ntnx_unreserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    unreserve_type: IP_ADDRESS_LIST
    ip_addresses:
      - ipv4:
          value: "10.30.30.81"
      - ipv4:
          value: "10.30.30.82"
  register: result

- name: Unreserve a range of IPs from a subnet
  nutanix.ncp.ntnx_unreserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    unreserve_type: IP_ADDRESS_RANGE
    start_ip_address:
      ipv4:
        value: "10.30.30.80"
    count: 3
  register: result

- name: Unreserve every IP tagged with a client context
  nutanix.ncp.ntnx_unreserve_ips_by_subnet_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "61959708-6efc-4d80-8c86-92c01f080672"
    unreserve_type: CONTEXT
    client_context: "ansible-context-tag"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for the unreserve action.
    - When C(wait) is true, this is the completed task object as returned by the tasks API.
    - When C(wait) is false, this is the task reference returned immediately by the unreserve call.
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
    - External ID (UUID) of the subnet the unreserve action was performed against.
  returned: always
  type: str
  sample: "61959708-6efc-4d80-8c86-92c01f080672"

task_ext_id:
  description:
    - The external ID of the unreserve task.
  returned: always
  type: str
  sample: "ZXJnb24=:521746d7-f26f-4652-b5fb-1b38c89a1dca"

changed:
  description: This indicates whether the module made any change on the cluster.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the module skipped execution (only set when applicable).
  returned: when applicable
  type: bool
  sample: false

msg:
  description: Status or error message emitted by the module.
  returned: contextual
  type: str
  sample: "IP addresses will be unreserved on subnet '61959708-6efc-4d80-8c86-92c01f080672'."

error:
  description: Error details when the module fails.
  returned: When an error occurs
  type: str

failed:
  description: Whether the module failed.
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
        ext_id=dict(type="str", required=True),
        unreserve_type=dict(
            type="str",
            required=True,
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


def _validate_unreserve_params(module):
    """
    Validate that the parameters required for the chosen unreserve_type are
    present. The v4 API rejects requests that mix modes or omit the mandatory
    payload for the selected mode, so fail early in Ansible with a clear
    message.
    """
    unreserve_type = module.params.get("unreserve_type")
    if unreserve_type == "IP_ADDRESS_LIST":
        validate_required_params(module, ["ip_addresses"])
    elif unreserve_type == "IP_ADDRESS_RANGE":
        validate_required_params(module, ["start_ip_address", "count"])
    elif unreserve_type == "CONTEXT":
        validate_required_params(module, ["client_context"])


def unreserve_ips_by_subnet_id(module, result, api_instance):
    """
    Perform the unreserve action against the given subnet.

    The spec is generated from module.params using SpecGenerator so nested
    IPAddress/IPv4Address/IPv6Address suboptions are materialised as proper
    SDK objects before being sent to the API.
    """
    _validate_unreserve_params(module)

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

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
        result["msg"] = "IP addresses will be unreserved on subnet '{0}'.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.unreserve_ips_by_subnet_id(extId=ext_id, body=spec)
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
        required_if=[
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

    state = module.params.get("state")
    if state == "absent":
        module.fail_json(
            msg=(
                "state=absent is not supported by ntnx_unreserve_ips_by_subnet_id_v2. "
                "Use state=present with the appropriate unreserve_type to release "
                "reserved IPs on a subnet."
            ),
            **result,
        )

    api_instance = get_subnet_ip_reservation_api_instance(module)
    unreserve_ips_by_subnet_id(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
