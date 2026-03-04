#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_routes_v2
short_description: Module to create, update, and delete routes in route table in VPC
version_added: 2.0.0
description:
  - Create, Update, Delete routes in route table in VPC
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - State of the route.
      - if C(state) is C(present) and route external ID is given, then route will be updated.
      - if C(state) is C(present) and route external ID is absent, then route will be created.
      - if C(state) is C(absent) and route external ID is given, then route will be deleted.
    choices: ["present", "absent"]
    type: str
  ext_id:
    description:
      - External ID of the route.
    type: str
  vpc_reference:
    description:
      - Reference to the VPC where the route table is located.
    type: str
  metadata:
    description:
      - Metadata for the route.
    required: false
    type: dict
    suboptions:
      owner_reference_id:
        description:
          - Reference ID of the owner.
        required: false
        type: str
      project_reference_id:
        description:
          - Reference ID of the project.
        required: false
        type: str
      category_ids:
        description:
          - List of category IDs.
        required: false
        type: list
        elements: str
  name:
    description:
      - Name of the route.
    required: false
    type: str
  description:
    description:
      - Description of the route.
    required: false
    type: str
  destination:
    description:
      - Destination IP subnet for the route.
    required: false
    type: dict
    suboptions:
      ipv4:
        description:
          - IPv4 destination IP subnet.
        required: false
        type: dict
        suboptions:
          ip:
            description:
              - IPv4 address.
            type: dict
            required: true
            suboptions:
              value:
                description:
                  - IPv4 address.
                required: true
                type: str
              prefix_length:
                description:
                  - Prefix length of the subnet.
                type: int
          prefix_length:
            description:
              - Prefix length of the subnet.
            type: int
            required: true
      ipv6:
        description:
          - IPv6 destination IP subnet.
        required: false
        type: dict
        suboptions:
          ip:
            description:
              - IPv6 address.
            type: dict
            required: true
            suboptions:
              value:
                description:
                  - IPv4 address.
                required: true
                type: str
              prefix_length:
                description:
                  - Prefix length of the subnet.
                type: int
          prefix_length:
            description:
              - Prefix length of the subnet.
            type: int
            required: true
  route_table_ext_id:
    description:
      - External ID of the route table.
    type: str
    required: true
  external_routing_domain_reference:
    description:
      - Reference to the external routing domain.
    required: false
    type: str
  route_type:
    description:
      - Type of the route.
    type: str
    choices:
      - LOCAL
      - STATIC
  wait:
    description:
      - Wait for the task to complete
    type: bool
    default: true
  nexthop:
    description:
      - Nexthop information for the route.
    type: dict
    suboptions:
      nexthop_type:
        description:
          - Type of the nexthop.
        type: str
        required: true
        choices:
          - VPN_CONNECTION
          - EXTERNAL_SUBNET
      nexthop_reference:
        description:
          - Reference to the nexthop.
        type: str
      nexthop_ip_address:
        description:
          - IP address of the nexthop.
        type: dict
        suboptions:
          ipv4:
            description:
              - IPv4 address.
            type: dict
            suboptions:
              value:
                description:
                  - IPv4 address.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the subnet.
                type: int
          ipv6:
            description:
              - IPv6 address.
            type: dict
            suboptions:
              value:
                description:
                  - IPv4 address.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the subnet.
                type: int
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create route
  nutanix.ncp.ntnx_routes_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "route_test"
    description: "Route for testing"
    vpc_reference: "c9a4b37d-5f8d-4a2a-b639-2d8e1f5a0c67"
    route_table_ext_id: "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201"
    route_type: STATIC
    destination:
      ipv4:
        ip:
          value: "10.0.0.1"
        prefix_length: 32
    nexthop:
      nexthop_type: "EXTERNAL_SUBNET"
      nexthop_reference: "5e98d574-c54c-4775-9f7a-8ebb2bc77d2c"
    metadata:
      owner_reference_id: "a1f7c8d4-3b9e-4891-b7ae-6c2d4e5f9b21"
      project_reference_id: "d7f1b9c3-6a5e-40d2-a1c4-e3f8b6a4d9f0"
  register: result

- name: Update route
  nutanix.ncp.ntnx_routes_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "route_test"
    description: "Route for testing updated"
    vpc_reference: "c9a4b37d-5f8d-4a2a-b639-2d8e1f5a0c67"
    route_table_ext_id: "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201"
    ext_id: "ed3cf052-a96a-4222-8d60-143a33c77e9f"
    route_type: STATIC
    destination:
      ipv4:
        ip:
          value: "10.0.0.2"
        prefix_length: 32
  register: result

- name: Delete route
  nutanix.ncp.ntnx_routes_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "ed3cf052-a96a-4222-8d60-143a33c77e9f"
    route_table_ext_id: "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting routes.
    - Route details if C(wait) is true and the operation is create or update.
    - Task details if C(wait) is false or the operation is delete.
  type: dict
  returned: always
  sample:
    {
      "extId": "ed3cf052-a96a-4222-8d60-143a33c77e9f",
      "isActive": true,
      "priority": 32768,
      "metadata":
        { "ownerReferenceId": "00000000-0000-0000-0000-000000000000" },
      "name": "route_test",
      "destination":
        { "ipv4": { "ip": { "value": "10.0.0.1" }, "prefixLength": 32 } },
      "nexthop":
        {
          "nexthopName": "integration_test_Ext-Nat1",
          "nexthopType": "EXTERNAL_SUBNET",
          "nexthopReference": "5e98d574-c54c-4775-9f7a-8ebb2bc77d2c",
          "nexthopIpAddress":
            { "ipv4": { "value": "10.44.3.193", "prefixLength": 32 } },
        },
      "routeTableReference": "7f9a76a3-922b-4aba-8d79-e7eb5cdaf201",
      "vpcReference": "66a926de-c188-4121-8456-0b97cdf0f807",
      "routeType": "STATIC",
    }

task_ext_id:
  description: The task ext_id of the operation
  type: str
  returned: always
  sample: "ZXJnb24=:3a2267ad-5e17-4813-b474-b5c7ea0aa848"

ext_id:
  description: The external ID of the route
  type: str
  returned: always

route_table_ext_id:
  description: The external ID of the route table
  type: str
  returned: always

changed:
  description: Indicates if any changes were made during the operation
  type: bool
  returned: always

skipped:
  description: Indicates if the operation was skipped
  type: bool
  returned: always

failed:
  description: Indicates if the operation failed
  type: bool
  returned: always

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Failed generating create route spec"

error:
  description: Error message if any
  type: str
  returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_routes_api_instance,
)
from ..module_utils.v4.network.helpers import get_route  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as net_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as net_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ip_address_sub_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int"),
    )

    ipv4_subnet_spec = dict(
        ip=dict(
            type="dict",
            options=ip_address_sub_spec,
            obj=net_sdk.IPv4Address,
            required=True,
        ),
        prefix_length=dict(type="int", required=True),
    )

    ipv6_subnet_spec = dict(
        ip=dict(
            type="dict",
            options=ip_address_sub_spec,
            obj=net_sdk.IPv6Address,
            required=True,
        ),
        prefix_length=dict(type="int", required=True),
    )

    ip_address_spec = dict(
        ipv4=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv4Address),
        ipv6=dict(type="dict", options=ip_address_sub_spec, obj=net_sdk.IPv6Address),
    )

    ip_subnet_spec = dict(
        ipv4=dict(type="dict", options=ipv4_subnet_spec, obj=net_sdk.IPv4Subnet),
        ipv6=dict(type="dict", options=ipv6_subnet_spec, obj=net_sdk.IPv6Subnet),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        project_reference_id=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    nexthop_spec = dict(
        nexthop_type=dict(
            type="str",
            choices=[
                "VPN_CONNECTION",
                "EXTERNAL_SUBNET",
            ],
            obj=net_sdk.NexthopType,
            required=True,
        ),
        nexthop_reference=dict(type="str"),
        nexthop_ip_address=dict(
            type="dict", options=ip_address_spec, obj=net_sdk.IPAddress
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        vpc_reference=dict(type="str"),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
        name=dict(type="str"),
        description=dict(type="str"),
        destination=dict(type="dict", options=ip_subnet_spec, obj=net_sdk.IPSubnet),
        nexthop=dict(type="dict", options=nexthop_spec, obj=net_sdk.Nexthop),
        route_table_ext_id=dict(type="str", required=True),
        external_routing_domain_reference=dict(type="str"),
        route_type=dict(
            type="str",
            choices=["LOCAL", "STATIC"],
            obj=net_sdk.RouteType,
        ),
    )

    return module_args


def create_route_table(module, route_api_instance, result):
    sg = SpecGenerator(module)
    default_spec = net_sdk.Route()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create route spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    route_table_ext_id = module.params.get("route_table_ext_id")
    try:
        resp = route_api_instance.create_route_for_route_table(
            routeTableExtId=route_table_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module, exception=e, msg="API exception while creating route"
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ROUTE
        )
        if ext_id:
            result["ext_id"] = ext_id
            route = get_route(module, route_api_instance, ext_id, route_table_ext_id)
            result["response"] = strip_internal_attributes(route.to_dict())
    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    return current_spec == update_spec


def update_route_table(module, route_api_instance, result):
    ext_id = module.params.get("ext_id")
    route_table_ext_id = module.params.get("route_table_ext_id")
    result["ext_id"] = ext_id
    result["route_table_ext_id"] = route_table_ext_id
    current_spec = get_route(module, route_api_instance, ext_id, route_table_ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update route spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for updating route", **result)

    kwargs = {"if_match": etag}
    try:
        resp = route_api_instance.update_route_for_route_table_by_id(
            routeTableExtId=route_table_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module, exception=e, msg="API exception while updating route"
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
    route = get_route(module, route_api_instance, ext_id, route_table_ext_id)
    result["response"] = strip_internal_attributes(route.to_dict())
    result["changed"] = True


def delete_route_table(module, route_api_instance, result):
    ext_id = module.params.get("ext_id")
    route_table_ext_id = module.params.get("route_table_ext_id")
    result["ext_id"] = ext_id
    result["route_table_ext_id"] = route_table_ext_id

    if module.check_mode:
        result["msg"] = "Route table with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = route_api_instance.delete_route_for_route_table_by_id(
            routeTableExtId=route_table_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module, exception=e, msg="API exception while deleting route"
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[["state", "absent", ["ext_id"]]],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "skipped": False,
    }
    state = module.params.get("state")
    route_api_instance = get_routes_api_instance(module)
    if state == "present":
        if not module.params.get("ext_id"):
            create_route_table(module, route_api_instance, result)
        else:
            update_route_table(module, route_api_instance, result)
    elif state == "absent":
        delete_route_table(module, route_api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
