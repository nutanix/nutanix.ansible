#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_bgp_session_v2
short_description: Create, Update and Delete BGP sessions in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update and delete BGP sessions in Nutanix Prism Central.
  - A BGP session represents the peering relationship between a local BGP gateway (Flow / Transit VPC gateway)
    and a remote BGP peer (e.g. Provider Edge Router, Azure Route Server, external firewall).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a BGP Session) -
      Required Roles: Network Admin, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a BGP Session) -
      Required Roles: Network Admin, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a BGP Session) -
      Required Roles: Network Admin, Prism Admin, Super Admin, VPC Admin
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
    type: str
    required: false
  description:
    description:
      - Description of the BGP session.
    type: str
    required: false
  local_gateway_reference:
    description:
      - External ID (UUID) of the local BGP gateway (Flow / Transit VPC gateway) that owns this session.
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - External ID (UUID) of the remote BGP gateway that represents the external peer.
      - Required for create operation.
    type: str
    required: false
  local_gateway_interface_ip_address:
    description:
      - IP address of the local gateway interface that establishes the peering.
      - Used to disambiguate which of the local BGP gateway's interfaces the session
        should be brought up on.
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
              - Prefix length of the network (0-32).
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
              - Prefix length of the network (0-128).
            type: int
            required: false
            default: 128
  dynamic_route_priority:
    description:
      - Priority for routes learned/advertised over this session.
      - Used to influence route selection when multiple sessions can advertise the same prefix.
      - Valid range is 300..1000 (SDK-enforced).
    type: int
    required: false
  password:
    description:
      - MD5 password used to authenticate the BGP session with the remote peer.
      - The remote peer MUST be configured with the same password.
    type: str
    required: false
  should_advertise_all_externally_routable_prefixes:
    description:
      - When true, all Externally Routable Prefixes (ERPs) configured on the local BGP
        gateway/VPC are advertised over this session.
      - When false, only the prefixes explicitly listed in
        I(externally_routable_prefixes_to_advertise) are advertised.
    type: bool
    required: false
  externally_routable_prefixes_to_advertise:
    description:
      - Explicit list of IP subnets (Externally Routable Prefixes) to advertise over this
        BGP session.
      - Ignored (or should be omitted) when
        I(should_advertise_all_externally_routable_prefixes) is C(true).
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 subnet specification.
        type: dict
        required: false
        suboptions:
          ip:
            description:
              - The IPv4 address specification.
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
                  - Prefix length of the network (0-32).
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
          - IPv6 subnet specification.
        type: dict
        required: false
        suboptions:
          ip:
            description:
              - The IPv6 address specification.
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
                  - Prefix length of the network (0-128).
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
      - Ordered list of Autonomous System Numbers that will be prepended to the AS path
        of routes advertised over this session.
      - Used to influence inbound route selection at the remote peer.
    type: list
    elements: int
    required: false
  advertised_routes_communities:
    description:
      - BGP communities that will be attached to routes advertised over this session.
    type: list
    elements: dict
    required: false
    suboptions:
      autonomous_system_number:
        description:
          - Autonomous System Number that originated the community.
          - Valid range is 1..65535 (SDK-enforced).
        type: int
        required: false
      community_value:
        description:
          - Community value.
          - Valid range is 1..65535 (SDK-enforced).
        type: int
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
- name: Create BGP session
  nutanix.ncp.ntnx_bgp_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "bgp_session_ansible"
    description: "BGP session created by Ansible"
    local_gateway_reference: "3e0f9d59-8fa2-4b7f-9e21-2b3a4d5e6f70"
    remote_gateway_reference: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    local_gateway_interface_ip_address:
      ipv4:
        value: "10.44.10.5"
        prefix_length: 32
    dynamic_route_priority: 300
    password: "S3cretBgpPass"
    should_advertise_all_externally_routable_prefixes: false
    externally_routable_prefixes_to_advertise:
      - ipv4:
          ip:
            value: "10.50.0.0"
            prefix_length: 16
          prefix_length: 16
    prepended_autonomous_system_path:
      - 65001
      - 65001
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
    ext_id: "6f8bd5f3-1234-4702-4c2d-b769fd5f94b0"
    name: "bgp_session_ansible_updated"
    description: "BGP session updated by Ansible"
    dynamic_route_priority: 500
    should_advertise_all_externally_routable_prefixes: true
  register: result
  ignore_errors: true

- name: Delete BGP session
  nutanix.ncp.ntnx_bgp_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "6f8bd5f3-1234-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting BGP session.
    - If the operation is create or update and C(wait) is true, it will return the BGP session details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "advertised_routes_communities": null,
      "description": "BGP session created by Ansible",
      "dynamic_route_priority": 300,
      "ext_id": "6f8bd5f3-1234-4702-4c2d-b769fd5f94b0",
      "externally_routable_prefixes_to_advertise": [
          {
              "ipv4": {
                  "ip": {"prefix_length": 32, "value": "10.50.0.0"},
                  "prefix_length": 16
              },
              "ipv6": null
          }
      ],
      "links": null,
      "local_gateway": null,
      "local_gateway_interface_ip_address": {
          "ipv4": {"prefix_length": 32, "value": "10.44.10.5"},
          "ipv6": null
      },
      "local_gateway_reference": "3e0f9d59-8fa2-4b7f-9e21-2b3a4d5e6f70",
      "metadata": null,
      "name": "bgp_session_ansible",
      "password": null,
      "prepended_autonomous_system_path": [65001, 65001],
      "remote_gateway": null,
      "remote_gateway_reference": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "should_advertise_all_externally_routable_prefixes": false,
      "status": {"message": "Established", "state": "UP"},
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
  sample: "6f8bd5f3-1234-4702-4c2d-b769fd5f94b0"

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
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


READ_ONLY_FIELDS = (
    "status",
    "local_gateway",
    "remote_gateway",
    "links",
    "tenant_id",
    "metadata",
    "ext_id",
)


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
            obj=networking_sdk.IPAddress,
        ),
        dynamic_route_priority=dict(type="int"),
        password=dict(type="str", no_log=True),
        should_advertise_all_externally_routable_prefixes=dict(type="bool"),
        externally_routable_prefixes_to_advertise=dict(
            type="list",
            elements="dict",
            options=ip_subnet_spec,
            obj=networking_sdk.IPSubnet,
        ),
        prepended_autonomous_system_path=dict(
            type="list",
            elements="int",
        ),
        advertised_routes_communities=dict(
            type="list",
            elements="dict",
            options=bgp_community_spec,
            obj=networking_sdk.BgpCommunity,
        ),
    )
    return module_args


def create_bgp_session(module, api_instance, result):
    validate_required_params(
        module,
        ["name", "local_gateway_reference", "remote_gateway_reference"],
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
            resp = get_bgp_session(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for BGP Session"
                ),
                msg="Failed to get entity ext_id from task for BGP Session",
            )
    result["changed"] = True


def check_bgp_session_idempotency(old_spec, update_spec):
    """Compare current spec vs desired spec (dicts) after stripping server-only fields."""
    old_spec = strip_internal_attributes(deepcopy(old_spec))
    update_spec = strip_internal_attributes(deepcopy(update_spec))
    for field in READ_ONLY_FIELDS:
        old_spec.pop(field, None)
        update_spec.pop(field, None)
    return old_spec == update_spec


def update_bgp_session(module, api_instance, result):
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

    if check_bgp_session_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

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
        resp = get_bgp_session(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_bgp_session(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "BGP session with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_bgp_session(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting BGP session", **result
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.delete_bgp_session_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting BGP session",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
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
