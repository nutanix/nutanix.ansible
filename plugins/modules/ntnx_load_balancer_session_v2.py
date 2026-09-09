#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_load_balancer_session_v2
short_description: Create, Update, Delete load balancer sessions in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to create, update, and delete load balancer sessions in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Load Balancer Session) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Update a Load Balancer Session) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, VPC Admin
    - >-
      B(Delete a Load Balancer Session) -
      Required Roles: Account Owner, Administrator, Prism Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create load balancer session.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update load balancer session.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete load balancer session.
    type: str
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the load balancer session.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the load balancer session.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the load balancer session.
      - Required for create operation.
    type: str
    required: false
  type:
    description:
      - Type of load balancer session.
      - C(NETWORK_LOAD_BALANCER) - Network (layer-4) load balancer session.
    type: str
    choices:
      - NETWORK_LOAD_BALANCER
    required: false
  vpc_reference:
    description:
      - UUID of the Virtual Private Cloud this load balancer session belongs to.
      - Required for create operation.
    type: str
    required: false
  listener:
    description:
      - Listener configuration of the load balancer session.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      virtual_ip:
        description:
          - Virtual IP configuration for the load balancer session listener.
        type: dict
        required: true
        suboptions:
          subnet_reference:
            description:
              - UUID of the subnet from which virtual IP address is allocated.
              - This field is immutable after creation and cannot be updated.
            type: str
            required: true
          assignment_type:
            description:
              - Assignment method for load balancer Virtual IP.
              - C(DYNAMIC) - Virtual IP is dynamically assigned by the system.
              - C(STATIC) - Virtual IP is statically assigned by the user.
            type: str
            choices:
              - DYNAMIC
              - STATIC
            required: true
          ip_address:
            description:
              - IP address of the virtual IP.
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
                      - The IPv4 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the network to which this host IPv4 address belongs.
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
                      - The IPv6 address of the host.
                    type: str
                    required: true
                  prefix_length:
                    description:
                      - The prefix length of the network to which this host IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
      protocol:
        description:
          - L3/L4 protocol.
          - C(TCP) - Transmission Control Protocol.
          - C(UDP) - User Datagram Protocol.
        type: str
        choices:
          - TCP
          - UDP
        required: true
      port_ranges:
        description:
          - List of port ranges the listener listens on.
        type: list
        elements: dict
        required: true
        suboptions:
          start_port:
            description:
              - Start port of TCP/UDP port range.
            type: int
            required: true
          end_port:
            description:
              - End port of TCP/UDP port range.
            type: int
            required: true
  algorithm:
    description:
      - Load balancing algorithm configured for the load balancer session.
      - >-
        C(FIVE_TUPLE_HASH) - Five Tuple hash algorithm for load balancing. Hash is calculated based on source IP address,
        destination IP address, source TCP/UDP port, destination TCP/UDP port and protocol fields of the packet.
    type: str
    choices:
      - FIVE_TUPLE_HASH
    required: false
  targets_config:
    description:
      - Targets configuration of the load balancer session.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      nic_targets:
        description:
          - List of virtual NIC targets configured as load balancer session targets.
        type: list
        elements: dict
        required: false
        suboptions:
          virtual_nic_reference:
            description:
              - UUID of the virtual NIC of the load balancer session target.
            type: str
            required: false
          port:
            description:
              - port value of the load balancer session target.
            type: int
            required: false
      category_targets:
        description:
          - List of category based targets used to derive the load balancer session's targets.
        type: list
        elements: dict
        required: false
        suboptions:
          match_all:
            description:
              - List of category vNIC selectors. The targets are derived from the entities that match all the specified categories.
            type: list
            elements: dict
            required: true
            suboptions:
              scope:
                description:
                  - The scope of the category. The scope of the category will be used to filter out the type of entities
                    that will be derived from the category to determine the final load balancer virtual NIC targets.
                  - >-
                    C(VM) - All VM(s) associated with the load balancer session's category are used to determine the
                    load balancer session's targets.
                type: str
                choices:
                  - VM
                required: false
              ext_id:
                description:
                  - External ID of the category.
                type: str
                required: false
          port:
            description:
              - port value of the load balancer session target.
            type: int
            required: true
  health_check_config:
    description:
      - Health check configuration for the load balancer session.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      interval_secs:
        description:
          - The interval, in seconds, between health checks.
          - The API default is 5.
        default: 5
        type: int
        required: false
      timeout_secs:
        description:
          - The time, in seconds, after which a health check times out.
          - The API default is 2.
        default: 2
        type: int
        required: false
      success_threshold:
        description:
          - The number of successful checks after which the target is considered healthy.
          - The API default is 3.
        default: 3
        type: int
        required: false
      failure_threshold:
        description:
          - The number of failure checks after which the target is considered unhealthy.
          - The API default is 3.
        default: 3
        type: int
        required: false
  metadata:
    description:
      - Metadata associated with this resource.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - The userName of the owner of this resource.
        type: str
        required: false
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
        required: false
      project_name:
        description:
          - The name of the project this resource belongs to.
        type: str
        required: false
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str
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
- name: Create load balancer session
  nutanix.ncp.ntnx_load_balancer_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "load_balancer_name"
    description: "ansible test full spec"
    type: "NETWORK_LOAD_BALANCER"
    vpc_reference: "b1a7c9d2-3f4e-4a6b-8c9d-0e1f2a3b4c5d"
    algorithm: "FIVE_TUPLE_HASH"
    listener:
      protocol: "TCP"
      port_ranges:
        - start_port: 80
          end_port: 80
      virtual_ip:
        subnet_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
        assignment_type: "STATIC"
        ip_address:
          ipv4:
            value: "192.168.1.100"
    targets_config:
      nic_targets:
        - virtual_nic_reference: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
          port: 80
    health_check_config:
      interval_secs: 10
      timeout_secs: 5
      success_threshold: 4
      failure_threshold: 6
  register: result
  ignore_errors: true

- name: Update load balancer session
  nutanix.ncp.ntnx_load_balancer_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "d1a36642-962e-4b45-9b52-150165100494"
    name: "load_balancer_name_updated"
    description: "ansible test updated"
    listener:
      protocol: "TCP"
      port_ranges:
        - start_port: 100
          end_port: 105
      virtual_ip:
        subnet_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
        assignment_type: "DYNAMIC"
    targets_config:
      nic_targets:
        - virtual_nic_reference: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
          port: 1080
    health_check_config:
      interval_secs: 13
      timeout_secs: 14
      success_threshold: 10
      failure_threshold: 12
  register: result
  ignore_errors: true

- name: Delete load balancer session
  nutanix.ncp.ntnx_load_balancer_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting load balancer session
    - If the operation is create or update and C(wait) is true, it will return the load balancer session details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "algorithm": "FIVE_TUPLE_HASH",
      "description": "ansible test full spec",
      "ext_id": "b83e9fc6-dfba-48d1-8319-fe208be30238",
      "health_check_config": {
          "failure_threshold": 6,
          "interval_secs": 10,
          "success_threshold": 4,
          "timeout_secs": 5
      },
      "links": null,
      "listener": {
          "port_ranges": [
              {
                  "end_port": 80,
                  "start_port": 80
              }
          ],
          "protocol": "TCP",
          "virtual_ip": {
              "assignment_type": "STATIC",
              "ip_address": {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "192.168.1.100"
                  },
                  "ipv6": null
              },
              "subnet_reference": "a40c3403-9f4c-4205-8506-64f524545be4"
          }
      },
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": null,
          "project_reference_id": null
      },
      "name": "YHjdsObUDrBeansible-lbs_2",
      "targets_config": {
          "category_targets": null,
          "nic_targets": [
              {
                  "health": "UNHEALTHY",
                  "port": 80,
                  "virtual_nic_reference": "34ed7568-8d2d-40a6-a702-0d27fe33c536",
                  "vm_reference": "6238f063-fda8-461f-5ed2-ad6b7f32875f"
              }
          ]
      },
      "tenant_id": null,
      "type": "NETWORK_LOAD_BALANCER",
      "vpc_reference": "ff1c27f0-1f10-42f6-8ffc-45f3179c4bff"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the load balancer session.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: when the task is idempotent
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
  sample: "Api Exception raised while creating load balancer session"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_load_balancer_sessions_api_instance,
)
from ..module_utils.v4.network.helpers import get_load_balancer_session  # noqa: E402
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
            obj=networking_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=networking_sdk.IPv6Address,
        ),
    )

    virtual_ip_spec = dict(
        subnet_reference=dict(type="str", required=True),
        assignment_type=dict(
            type="str",
            choices=["DYNAMIC", "STATIC"],
            required=True,
            obj=networking_sdk.AssignmentType,
        ),
        ip_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=networking_sdk.IPAddress,
        ),
    )

    port_range_spec = dict(
        start_port=dict(type="int", required=True),
        end_port=dict(type="int", required=True),
    )

    listener_spec = dict(
        virtual_ip=dict(
            type="dict",
            options=virtual_ip_spec,
            required=True,
            obj=networking_sdk.VirtualIP,
        ),
        protocol=dict(
            type="str",
            choices=["TCP", "UDP"],
            required=True,
            obj=networking_sdk.Protocol,
        ),
        port_ranges=dict(
            type="list",
            elements="dict",
            options=port_range_spec,
            required=True,
            obj=networking_sdk.PortRange,
        ),
    )

    nic_target_spec = dict(
        virtual_nic_reference=dict(type="str"),
        port=dict(type="int"),
    )

    category_vnic_selector_spec = dict(
        scope=dict(type="str", choices=["VM"], obj=networking_sdk.CategoryScope),
        ext_id=dict(type="str"),
    )

    category_target_spec = dict(
        match_all=dict(
            type="list",
            elements="dict",
            options=category_vnic_selector_spec,
            required=True,
            obj=networking_sdk.CategoryVnicSelector,
        ),
        port=dict(type="int", required=True),
    )

    targets_config_spec = dict(
        nic_targets=dict(
            type="list",
            elements="dict",
            options=nic_target_spec,
            obj=networking_sdk.NicTarget,
        ),
        category_targets=dict(
            type="list",
            elements="dict",
            options=category_target_spec,
            obj=networking_sdk.CategoryTarget,
        ),
    )

    health_check_config_spec = dict(
        interval_secs=dict(type="int", default=5),
        timeout_secs=dict(type="int", default=2),
        success_threshold=dict(type="int", default=3),
        failure_threshold=dict(type="int", default=3),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str", required=False),
        owner_user_name=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        project_name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        type=dict(
            type="str",
            choices=["NETWORK_LOAD_BALANCER"],
            obj=networking_sdk.LoadBalancerSessionType,
        ),
        vpc_reference=dict(type="str"),
        listener=dict(
            type="dict",
            options=listener_spec,
            obj=networking_sdk.Listener,
        ),
        algorithm=dict(
            type="str",
            choices=["FIVE_TUPLE_HASH"],
            obj=networking_sdk.Algorithm,
        ),
        targets_config=dict(
            type="dict",
            options=targets_config_spec,
            obj=networking_sdk.Target,
        ),
        health_check_config=dict(
            type="dict",
            options=health_check_config_spec,
            obj=networking_sdk.HealthCheck,
        ),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            obj=networking_sdk.Metadata,
        ),
    )
    return module_args


def create_load_balancer_session(module, load_balancer_sessions, result):
    validate_required_params(
        module,
        [
            "name",
            "description",
            "vpc_reference",
            "listener",
            "targets_config",
            "health_check_config",
        ],
    )
    sg = SpecGenerator(module)
    default_spec = networking_sdk.LoadBalancerSession()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create load balancer session spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = load_balancer_sessions.create_load_balancer_session(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating load balancer session",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.LOAD_BALANCER_SESSION
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_load_balancer_session(module, load_balancer_sessions, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Load Balancer Session"
                ),
                msg="Failed to get entity ext_id from task for Load Balancer Session",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec = strip_internal_attributes(old_spec_dict)
    update_spec = strip_internal_attributes(update_spec_dict)
    # Remove read-only attributes from both specs to check for idempotency
    for spec in (old_spec, update_spec):
        nic_targets = (spec.get("targets_config") or {}).get("nic_targets") or []
        for nic_target in nic_targets:
            nic_target.pop("health", None)
            nic_target.pop("vm_reference", None)

    if old_spec == update_spec:
        return True
    return False


def update_load_balancer_session(module, load_balancer_sessions, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_load_balancer_session(module, load_balancer_sessions, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating load balancer session", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update load balancer session spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = None
    try:
        resp = load_balancer_sessions.update_load_balancer_session_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating load balancer session",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_load_balancer_session(module, load_balancer_sessions, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_load_balancer_session(module, load_balancer_sessions, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Load balancer session with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = load_balancer_sessions.delete_load_balancer_session_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting load balancer session",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
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
    load_balancer_sessions = get_load_balancer_sessions_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_load_balancer_session(module, load_balancer_sessions, result)
        else:
            create_load_balancer_session(module, load_balancer_sessions, result)
    else:
        delete_load_balancer_session(module, load_balancer_sessions, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
