#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_BgpSession_v2
short_description: Create, Update, Delete BGP sessions in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to create, update, and delete BGP sessions in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a BGP Session) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update a BGP Session) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete a BGP Session) -
      Required Roles: Prism Admin, Super Admin
    - Requires the referenced local and remote gateways to exist before creating a BGP session.
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
      - Reference to the local gateway for the BGP session.
      - Required for create operation.
    type: str
    required: false
  remote_gateway_reference:
    description:
      - Reference to the remote gateway for the BGP session.
      - Required for create operation.
    type: str
    required: false
  local_gateway_interface_ip_address:
    description:
      - Local gateway interface IP address.
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
  dynamic_route_priority:
    description:
      - Priority assigned to routes received over this BGP session.
    type: int
    required: false
  password:
    description:
      - BGP session password for authentication.
    type: str
    required: false
  should_advertise_all_externally_routable_prefixes:
    description:
      - Whether to advertise all externally routable prefixes.
    type: bool
    required: false
  externally_routable_prefixes_to_advertise:
    description:
      - List of IP subnets to advertise over this BGP session.
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
              - IPv4 address for the subnet.
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
                  - Prefix length.
                type: int
                required: false
          prefix_length:
            description:
              - Prefix length of the subnet.
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
              - IPv6 address for the subnet.
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
                  - Prefix length.
                type: int
                required: false
          prefix_length:
            description:
              - Prefix length of the subnet.
            type: int
            required: true
  prepended_autonomous_system_path:
    description:
      - List of autonomous system numbers to prepend to the AS path.
    type: list
    elements: int
    required: false
  advertised_routes_communities:
    description:
      - List of BGP communities to attach to advertised routes.
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
          - Community value.
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
- name: Create BGP session with required fields
  nutanix.ncp.ntnx_BgpSession_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "bgp_session_1"
    local_gateway_reference: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    remote_gateway_reference: "f1e2d3c4-b5a6-7890-abcd-ef0987654321"
  register: result
  ignore_errors: true

- name: Create BGP session with all fields
  nutanix.ncp.ntnx_BgpSession_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "bgp_session_full"
    description: "BGP session with all attributes"
    local_gateway_reference: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    remote_gateway_reference: "f1e2d3c4-b5a6-7890-abcd-ef0987654321"
    local_gateway_interface_ip_address:
      ipv4:
        value: "10.0.0.1"
        prefix_length: 32
    dynamic_route_priority: 100
    password: "bgp_secret"
    should_advertise_all_externally_routable_prefixes: true
    externally_routable_prefixes_to_advertise:
      - ipv4:
          ip:
            value: "192.168.1.0"
          prefix_length: 24
    prepended_autonomous_system_path:
      - 65001
      - 65002
    advertised_routes_communities:
      - autonomous_system_number: 65001
        community_value: 100
  register: result
  ignore_errors: true

- name: Update BGP session
  nutanix.ncp.ntnx_BgpSession_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "bgp_session_updated"
    description: "Updated BGP session"
    dynamic_route_priority: 200
  register: result
  ignore_errors: true

- name: Delete BGP session
  nutanix.ncp.ntnx_BgpSession_v2:
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
    - Response for creating, updating, or deleting BGP session.
    - If the operation is create or update and C(wait) is true, it will return the BGP session details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "name": "bgp_session_1",
      "description": "BGP session with all attributes",
      "local_gateway_reference": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "remote_gateway_reference": "f1e2d3c4-b5a6-7890-abcd-ef0987654321",
      "local_gateway_interface_ip_address": null,
      "dynamic_route_priority": 100,
      "password": null,
      "status": null,
      "local_gateway": null,
      "remote_gateway": null,
      "should_advertise_all_externally_routable_prefixes": true,
      "externally_routable_prefixes_to_advertise": null,
      "prepended_autonomous_system_path": null,
      "advertised_routes_communities": null,
      "metadata": null,
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
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
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: Explains why the operation was skipped (e.g. idempotency)
  returned: when applicable
  type: str
  sample: "Nothing to change."

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
  description: Status or error message
  returned: contextual
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
        prefix_length=dict(type="int", required=False),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
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
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.BGP_SESSION
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_bgp_session(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    for key in ("status", "local_gateway", "remote_gateway"):
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


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
        module.exit_json(msg="Nothing to change.")

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
        resp = get_bgp_session(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
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
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
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
