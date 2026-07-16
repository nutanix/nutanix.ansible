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
version_added: 2.6.0
description:
  - This module allows you to create, update, and delete BGP sessions in Nutanix Prism Central.
  - A BGP session is peered between a local BGP gateway (managed by Prism Central) and a
    remote BGP gateway (typically an on-prem router or another cloud) so that the two sides
    can exchange dynamic routes.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a BGP session) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a BGP session) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a BGP session) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - >-
      The referenced local and remote BGP gateways must already exist before creating a
      BGP session — the API returns a "not found" error otherwise.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a BGP session.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the BGP session.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the BGP session.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the BGP session.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - BGP session name (maximum 128 characters).
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - BGP session description (maximum 1000 characters).
    type: str
    required: false
  local_gateway_reference:
    description:
      - External ID (UUID) of the local BGP gateway.
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - External ID (UUID) of the remote BGP gateway.
      - Required for create operation.
    type: str
    required: false
  local_gateway_interface_ip_address:
    description:
      - IP address of the local BGP gateway interface used for this BGP session.
      - When the local BGP gateway has multiple interfaces, this pins the session to a specific one.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 form of the local gateway interface address.
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
          - IPv6 form of the local gateway interface address.
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
  dynamic_route_priority:
    description:
      - Priority assigned to routes received over this BGP session.
      - Must be between 300 and 1000 (inclusive) as enforced by the BGP session API.
    type: int
    required: false
  password:
    description:
      - BGP authentication password used to secure the peering session.
    type: str
    required: false
  should_advertise_all_externally_routable_prefixes:
    description:
      - When true, advertise all externally routable prefixes of the associated VPC over this BGP session.
      - When false, only the prefixes listed in I(externally_routable_prefixes_to_advertise) are advertised.
    type: bool
    required: false
  externally_routable_prefixes_to_advertise:
    description:
      - VPC externally-routable IP prefixes (IPv4 or IPv6) to advertise over this BGP session.
      - Ignored when I(should_advertise_all_externally_routable_prefixes) is true.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 subnet form of the prefix to advertise.
        type: dict
        required: false
        suboptions:
          ip:
            description:
              - IPv4 network address of the subnet.
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
                  - Prefix length of the IPv4 address itself.
                type: int
                required: false
                default: 32
          prefix_length:
            description:
              - Prefix length of the IPv4 subnet.
            type: int
            required: true
      ipv6:
        description:
          - IPv6 subnet form of the prefix to advertise.
        type: dict
        required: false
        suboptions:
          ip:
            description:
              - IPv6 network address of the subnet.
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
                  - Prefix length of the IPv6 address itself.
                type: int
                required: false
                default: 128
          prefix_length:
            description:
              - Prefix length of the IPv6 subnet.
            type: int
            required: true
  prepended_autonomous_system_path:
    description:
      - Ordered list of ASNs to prepend to the AS_PATH attribute of BGP updates for this session.
      - Used for BGP AS path prepending traffic engineering.
    type: list
    elements: int
    required: false
  advertised_routes_communities:
    description:
      - BGP community tags to attach to advertised routes for this session.
    type: list
    elements: dict
    required: false
    suboptions:
      autonomous_system_number:
        description:
          - Autonomous System Number that originated the community.
        type: int
        required: true
      community_value:
        description:
          - Numeric value component of the BGP community.
        type: int
        required: true
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
- name: Create BGP session with minimum attributes
  nutanix.ncp.ntnx_bgp_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "bgp_session_ansible_min"
    local_gateway_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    remote_gateway_reference: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
  ignore_errors: true

- name: Create BGP session with all attributes
  nutanix.ncp.ntnx_bgp_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "bgp_session_ansible_full"
    description: "BGP session created by Ansible with full attributes"
    local_gateway_reference: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    remote_gateway_reference: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    local_gateway_interface_ip_address:
      ipv4:
        value: "10.10.10.1"
        prefix_length: 32
    dynamic_route_priority: 500
    password: "s3cr3t"
    should_advertise_all_externally_routable_prefixes: false
    externally_routable_prefixes_to_advertise:
      - ipv4:
          ip:
            value: "192.168.10.0"
          prefix_length: 24
    prepended_autonomous_system_path: [65001, 65002]
    advertised_routes_communities:
      - autonomous_system_number: 65001
        community_value: 100
  register: result
  ignore_errors: true

- name: Update BGP session
  nutanix.ncp.ntnx_bgp_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "bgp_session_ansible_updated"
    description: "Updated BGP session description"
    dynamic_route_priority: 700
    should_advertise_all_externally_routable_prefixes: true
    prepended_autonomous_system_path: [65001, 65002, 65003]
  register: result
  ignore_errors: true

- name: Delete BGP session
  nutanix.ncp.ntnx_bgp_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a BGP session.
    - If the operation is create or update and C(wait) is true, it will return the BGP session details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "name": "bgp_session_ansible_full",
      "description": "BGP session created by Ansible with full attributes",
      "local_gateway_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "remote_gateway_reference": "8300384a-56ee-4750-aeb8-3d1c42908bee",
      "local_gateway_interface_ip_address": {
          "ipv4": {"value": "10.10.10.1", "prefix_length": 32},
          "ipv6": null
      },
      "dynamic_route_priority": 500,
      "should_advertise_all_externally_routable_prefixes": false,
      "externally_routable_prefixes_to_advertise": [
          {
              "ipv4": {"ip": {"value": "192.168.10.0", "prefix_length": 32}, "prefix_length": 24},
              "ipv6": null
          }
      ],
      "prepended_autonomous_system_path": [65001, 65002],
      "advertised_routes_communities": [
          {"autonomous_system_number": 65001, "community_value": 100}
      ],
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "status": null,
      "local_gateway": null,
      "remote_gateway": null,
      "metadata": null,
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the BGP session.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: Indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: Indicates whether the task was skipped due to idempotency.
  returned: when applicable
  type: str
  sample: "BGP session with name 'bgp_session_ansible_min' already exists. Skipping creation."

error:
  description: Error details if any error occurred; None on success.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Human-readable status message; populated on errors, idempotency, and delete check mode.
  returned: When there is an error, module is idempotent or check mode
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
        autonomous_system_number=dict(type="int", required=True),
        community_value=dict(type="int", required=True),
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
        dynamic_route_priority=dict(type="int"),
        password=dict(type="str", no_log=True),
        should_advertise_all_externally_routable_prefixes=dict(type="bool"),
        externally_routable_prefixes_to_advertise=dict(
            type="list",
            elements="dict",
            options=ip_subnet_spec,
            required=False,
            obj=networking_sdk.IPSubnet,
        ),
        prepended_autonomous_system_path=dict(
            type="list",
            elements="int",
            required=False,
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


def create_BgpSession(module, result, api_instance):
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
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.BGP_SESSION
        )
        if ext_id:
            result["ext_id"] = ext_id
            session = get_bgp_session(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(session.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    # BGP status, local_gateway, remote_gateway are server-populated projections
    # and must not participate in idempotency comparison.
    for k in ("status", "local_gateway", "remote_gateway"):
        old_spec_dict.pop(k, None)
        update_spec_dict.pop(k, None)
    return old_spec_dict == update_spec_dict


def _remove_read_only_attributes(spec):
    """Remove read-only projection attributes before update API call."""
    spec.status = None
    spec.local_gateway = None
    spec.remote_gateway = None


def update_BgpSession(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_bgp_session(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating BGP session", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update BGP session spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    _remove_read_only_attributes(update_spec)

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


def delete_BgpSession(module, result, api_instance):
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
        task_status = wait_for_completion(module, task_ext_id, raise_error=True)
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
        "task_ext_id": None,
    }
    api_instance = get_bgp_sessions_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_BgpSession(module, result, api_instance)
        else:
            create_BgpSession(module, result, api_instance)
    else:
        delete_BgpSession(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
