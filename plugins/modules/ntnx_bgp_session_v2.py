#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_bgp_session_v2
short_description: Create, Update, Delete BGP sessions in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete BGP sessions in Nutanix Prism Central.
  - A BGP session establishes an eBGP peering relationship between a Nutanix
    BGP gateway (local) and an external remote BGP gateway.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a BGP session) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a BGP session) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a BGP session) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create BGP session.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update BGP session.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete BGP session.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the BGP session.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - BGP session name.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - BGP session description.
      - Maximum 1000 characters.
    type: str
    required: false
  local_gateway_reference:
    description:
      - Local BGP gateway reference (external ID of the local BGP gateway).
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - Remote BGP gateway reference (external ID of the remote BGP gateway).
      - Required for create operation.
    type: str
    required: false
  local_gateway_interface_ip_address:
    description:
      - IP address of the local BGP gateway interface used for this session.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the local gateway interface.
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
          - IPv6 address of the local gateway interface.
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
  dynamic_route_priority:
    description:
      - Priority assigned to routes received over this BGP session.
      - Used to break ties when the same route is learned over multiple BGP sessions.
      - Minimum 300, maximum 1000.
    type: int
    required: false
  password:
    description:
      - BGP password used to secure the peering session.
      - The value is treated as sensitive and is not logged.
    type: str
    required: false
  should_advertise_all_externally_routable_prefixes:
    description:
      - When true, all externally routable prefixes (ERPs) of the local VPC are advertised over this session.
      - When false, only the prefixes listed in
        I(externally_routable_prefixes_to_advertise) are advertised.
    type: bool
    required: false
  externally_routable_prefixes_to_advertise:
    description:
      - Explicit list of externally routable prefixes to advertise on this
        BGP session.
      - Only meaningful when
        I(should_advertise_all_externally_routable_prefixes) is false.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 subnet to advertise.
        type: dict
        required: false
        suboptions:
          ip:
            description:
              - IPv4 address of the subnet.
            type: dict
            required: true
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the address.
                type: int
                required: false
                default: 32
          prefix_length:
            description:
              - Prefix length of the subnet.
            type: int
            required: true
      ipv6:
        description:
          - IPv6 subnet to advertise.
        type: dict
        required: false
        suboptions:
          ip:
            description:
              - IPv6 address of the subnet.
            type: dict
            required: true
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the address.
                type: int
                required: false
                default: 128
          prefix_length:
            description:
              - Prefix length of the subnet.
            type: int
            required: true
  prepended_autonomous_system_path:
    description:
      - Ordered list of ASNs to prepend to the AS_path attribute of BGP
        updates advertised over this session.
      - Used to influence upstream route selection.
    type: list
    elements: int
    required: false
  advertised_routes_communities:
    description:
      - BGP community tags attached to routes advertised over this session.
    type: list
    elements: dict
    required: false
    suboptions:
      autonomous_system_number:
        description:
          - Autonomous System Number that originated the community.
        type: int
        required: false
      community_value:
        description:
          - Community value paired with the ASN.
        type: int
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
- name: Create BGP session with minimum attributes
  nutanix.ncp.ntnx_bgp_session_v2:
    state: present
    name: "bgp_session_min"
    local_gateway_reference: "6c1d75a9-38f1-4fb9-9c11-91d7dbde2a1e"
    remote_gateway_reference: "8b8a20d0-e112-4cf7-9a3d-5ef2f2f5aaee"
  register: result

- name: Create BGP session with all attributes
  nutanix.ncp.ntnx_bgp_session_v2:
    state: present
    name: "bgp_session_full"
    description: "BGP session created by Ansible with all attributes"
    local_gateway_reference: "6c1d75a9-38f1-4fb9-9c11-91d7dbde2a1e"
    remote_gateway_reference: "8b8a20d0-e112-4cf7-9a3d-5ef2f2f5aaee"
    local_gateway_interface_ip_address:
      ipv4:
        value: "10.44.5.10"
        prefix_length: 32
    dynamic_route_priority: 500
    password: "s3cret-bgp"
    should_advertise_all_externally_routable_prefixes: false
    externally_routable_prefixes_to_advertise:
      - ipv4:
          ip:
            value: "10.100.0.0"
            prefix_length: 24
          prefix_length: 24
    prepended_autonomous_system_path:
      - 65001
      - 65002
    advertised_routes_communities:
      - autonomous_system_number: 65001
        community_value: 100
  register: result

- name: Update BGP session
  nutanix.ncp.ntnx_bgp_session_v2:
    state: present
    ext_id: "9f5f2a7c-4a4e-4bcb-83d6-6b26fe5c1a20"
    name: "bgp_session_full_updated"
    description: "Updated BGP session"
    local_gateway_reference: "6c1d75a9-38f1-4fb9-9c11-91d7dbde2a1e"
    remote_gateway_reference: "8b8a20d0-e112-4cf7-9a3d-5ef2f2f5aaee"
    dynamic_route_priority: 700
    should_advertise_all_externally_routable_prefixes: true
  register: result

- name: Delete BGP session
  nutanix.ncp.ntnx_bgp_session_v2:
    state: absent
    ext_id: "9f5f2a7c-4a4e-4bcb-83d6-6b26fe5c1a20"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting BGP session
    - If the operation is create or update and C(wait) is true, it will return the BGP session details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "advertised_routes_communities": null,
      "description": "BGP session created by Ansible with all attributes",
      "dynamic_route_priority": 500,
      "ext_id": "9f5f2a7c-4a4e-4bcb-83d6-6b26fe5c1a20",
      "externally_routable_prefixes_to_advertise": [
        {
          "ipv4": {
            "ip": {"value": "10.100.0.0", "prefix_length": 24},
            "prefix_length": 24
          },
          "ipv6": null
        }
      ],
      "links": null,
      "local_gateway": null,
      "local_gateway_interface_ip_address": {
        "ipv4": {"value": "10.44.5.10", "prefix_length": 32},
        "ipv6": null
      },
      "local_gateway_reference": "6c1d75a9-38f1-4fb9-9c11-91d7dbde2a1e",
      "metadata": null,
      "name": "bgp_session_full",
      "password": null,
      "prepended_autonomous_system_path": [65001, 65002],
      "remote_gateway": null,
      "remote_gateway_reference": "8b8a20d0-e112-4cf7-9a3d-5ef2f2f5aaee",
      "should_advertise_all_externally_routable_prefixes": false,
      "status": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the BGP session.
  returned: always
  type: str
  sample: "9f5f2a7c-4a4e-4bcb-83d6-6b26fe5c1a20"

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating BGP session"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_bgp_sessions_api_instance,
    get_etag,
)
from ..module_utils.v4.network.helpers import get_bgp_session  # noqa: E402
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

    ipv4_subnet_spec = dict(
        ip=dict(
            type="dict",
            options=ipv4_address_spec,
            required=True,
            obj=networking_sdk.IPv4Address,
        ),
        prefix_length=dict(type="int", required=True),
    )

    ipv6_subnet_spec = dict(
        ip=dict(
            type="dict",
            options=ipv6_address_spec,
            required=True,
            obj=networking_sdk.IPv6Address,
        ),
        prefix_length=dict(type="int", required=True),
    )

    ip_subnet_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_subnet_spec,
            required=False,
            obj=networking_sdk.IPv4Subnet,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_subnet_spec,
            required=False,
            obj=networking_sdk.IPv6Subnet,
        ),
    )

    bgp_community_spec = dict(
        autonomous_system_number=dict(type="int", required=False),
        community_value=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        local_gateway_reference=dict(type="str"),
        remote_gateway_reference=dict(type="str"),
        local_gateway_interface_ip_address=dict(
            type="dict",
            options=ip_address_spec,
            required=False,
            obj=networking_sdk.IPAddress,
        ),
        dynamic_route_priority=dict(type="int", required=False),
        password=dict(type="str", required=False, no_log=True),
        should_advertise_all_externally_routable_prefixes=dict(
            type="bool", required=False
        ),
        externally_routable_prefixes_to_advertise=dict(
            type="list",
            elements="dict",
            options=ip_subnet_spec,
            required=False,
            obj=networking_sdk.IPSubnet,
        ),
        prepended_autonomous_system_path=dict(
            type="list", elements="int", required=False
        ),
        advertised_routes_communities=dict(
            type="list",
            elements="dict",
            options=bgp_community_spec,
            required=False,
            obj=networking_sdk.BgpCommunity,
        ),
    )
    return module_args


def create_bgp_session(module, api_instance, result):
    validate_required_params(
        module, ["name", "local_gateway_reference", "remote_gateway_reference"]
    )
    sg = SpecGenerator(module)
    default_spec = networking_sdk.BgpSession()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create BGP session spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_bgp_session(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating BGP session",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.BGP_SESSION
        )
        if ext_id:
            result["ext_id"] = ext_id
            session = get_bgp_session(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(session.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for BGP Session"
                ),
                msg="Failed to get entity ext_id from task for BGP Session",
            )
    result["changed"] = True


def check_bgp_session_idempotency(current_spec, update_spec):
    current = strip_internal_attributes(current_spec.to_dict())
    updated = strip_internal_attributes(update_spec.to_dict())
    # Status, local_gateway and remote_gateway are read-only, computed by the
    # backend and should not participate in idempotency comparison.
    for key in ("status", "local_gateway", "remote_gateway", "links", "tenant_id"):
        current.pop(key, None)
        updated.pop(key, None)
    return current == updated


def update_bgp_session(module, api_instance, result):
    validate_required_params(
        module, ["name", "local_gateway_reference", "remote_gateway_reference"]
    )
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_bgp_session(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating BGP session", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update BGP session spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_bgp_session_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    # Strip fields that are read-only in the API response but the SDK still
    # carries on the model — sending them back can cause a 400.
    update_spec.status = None
    update_spec.local_gateway = None
    update_spec.remote_gateway = None

    resp = None
    try:
        resp = api_instance.update_bgp_session_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating BGP session",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        session = get_bgp_session(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(session.to_dict())
    result["changed"] = True


def delete_bgp_session(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "BGP session with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_bgp_session_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting BGP session",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
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
        "skipped": False,
    }
    api_instance = get_bgp_sessions_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_bgp_session(module, api_instance, result)
        else:
            create_bgp_session(module, api_instance, result)
    else:
        delete_bgp_session(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
