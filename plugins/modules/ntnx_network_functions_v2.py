#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_network_functions_v2
short_description: Manage network functions in Nutanix Prism Central
version_added: 2.5.0
description:
  - Create, Update, Delete network functions
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - If C(state) is present, it will create or update the network function.
      - If C(state) is set to C(present) and ext_id is not provided, the operation will create the network function.
      - If C(state) is set to C(present) and ext_id is provided, the operation will update the network function.
      - If C(state) is set to C(absent) and ext_id is provided, the operation will delete the network function.
    type: str
    choices: ['present', 'absent']
  ext_id:
    description:
      - Network function external ID.
      - Required for updating or deleting the network function.
    type: str
  name:
    description:
      - A required, user-friendly name for the network function (up to 128 characters).
    type: str
  description:
    description:
      - An optional, longer text field (up to 1000 characters) to describe the network function's purpose.
    type: str
  nic_pairs:
    description:
      - List of all NIC pairs part of this network function.
      - Minimum 1, maximum 2 items.
    type: list
    elements: dict
    suboptions:
      ingress_nic_reference:
        description:
          - The required UUID of the virtual NIC on the NFVM where traffic enters.
          - You must create a VM with a special "Network Function NIC" type and provide the UUID of that NIC here.
          - This tells the Nutanix platform which vNIC on your firewall VM to send the redirected traffic to.
        type: str
        required: true
      egress_nic_reference:
        description:
          - The optional UUID of the virtual NIC from which traffic exits the NFVM.
          - Specify the UUID of another Network Function NIC on the same VM.
          - In an inline model, traffic enters the ingressNic, is processed by the NFVM, and then sent out through the egressNic to its final destination.
          - This is not used in VTAP mode.
        type: str
      vm_reference:
        description:
          - The UUID of the VM that hosts the ingress and egress NICs.
        type: str
      is_enabled:
        description:
          - A boolean flag to control the administrative state of the NIC pair.
          - Set to C(false) to administratively disable this NIC pair, for instance, during a maintenance window.
          - If set to C(false), this NIC pair will not be considered for traffic redirection, even if it's healthy.
          - This provides a way to gracefully take a specific NFVM out of service without deleting the configuration.
        type: bool
        default: true
  high_availability_mode:
    description:
      - A required setting that defines the HA configuration. Currently, only C(ACTIVE_PASSIVE) is supported.
      - Set this to C(ACTIVE_PASSIVE) and define two nicPairs in your configuration, one for each NFVM in the HA pair.
      - This enables high availability. The system will designate one NIC pair as ACTIVE and the other as PASSIVE.
      - If the active one fails its health check, the system automatically fails over to the passive one, ensuring service continuity.
    type: str
    choices: ['ACTIVE_PASSIVE']
  failure_handling:
    description:
      - Defines what happens to traffic if all NFVMs in the chain are unhealthy.
      - This is a critical security and availability decision.
      - C(FAIL_CLOSE) blocks all traffic. This is the secure option, preventing uninspected traffic from passing.
      - C(FAIL_OPEN) allows traffic to bypass the NFVM and go directly to the destination.
        Use this if connectivity is more critical than inspection.
      - C(NO_ACTION) when network function is unhealthy, no action is taken and traffic is black-holed.
        This value is deprecated and will automatically be converted to FAIL_CLOSE.
    type: str
    choices: ['FAIL_OPEN', 'FAIL_CLOSE', 'NO_ACTION']
  traffic_forwarding_mode:
    description:
      - Specifies how traffic is delivered to the NFVM. This determines the fundamental behavior of your service insertion.
      - C(INLINE) redirects traffic through the NFVM. The NFVM inspects, and possibly modifies or blocks, the traffic before forwarding it.
        Requires both ingress_nic_reference and egress_nic_reference. Use for active enforcement (like a firewall).
      - C(VTAP) mirrors a copy of the traffic to the NFVM for passive monitoring (e.g., for an Intrusion Detection System).
        The original traffic flow is unaffected. egress_nic_reference is not used in this mode. Use for passive monitoring.
    type: str
    choices: ['VTAP', 'INLINE']
  data_plane_health_check_config:
    description:
      - Data Plane Health check configuration applied for the network function.
      - These settings control how the system monitors the health of your NFVMs and determines when to trigger failover.
    type: dict
    suboptions:
      interval_secs:
        description:
          - The time in seconds between each health check probe.
          - Adjust based on how quickly you need to detect a failure.
          - A lower value means faster detection but higher monitoring overhead.
          - Range 1-65535.
        type: int
        default: 5
      timeout_secs:
        description:
          - The time in seconds before a health check probe is considered to have failed.
          - Set a value that gives your NFVM enough time to respond to a probe under normal load.
          - Prevents the system from waiting indefinitely for a response from an unresponsive NFVM.
          - Range 1-65535.
        type: int
        default: 1
      success_threshold:
        description:
          - The number of consecutive successful checks required to mark an unhealthy NFVM as healthy again.
          - Keep the default or increase it to be more certain the NFVM has recovered before sending production traffic to it again.
          - Prevents flapping, where an NFVM is repeatedly marked healthy and unhealthy in rapid succession.
          - Range 1-64.
        type: int
        default: 3
      failure_threshold:
        description:
          - The number of consecutive failed checks required to mark a healthy NFVM as unhealthy.
          - Keep the default or adjust as needed.
          - A lower value means faster failover, but a higher value protects against transient network blips causing an unnecessary failover.
          - This ensures the system doesn't trigger a failover due to a single dropped packet or a temporary issue.
          - Range 1-64.
        type: int
        default: 3
  metadata:
    description:
      - An object containing standard resource metadata.
      - This includes ownership, project association, and categorization details.
    type: dict
    suboptions:
      owner_reference_id:
        description:
          - The unique identifier (UUID) of the user who owns this resource.
          - Set this to the UUID of the user or service account responsible for this network function.
          - It establishes clear ownership for accountability and resource management.
        type: str
      owner_user_name:
        description:
          - The username corresponding to the owner_reference_id.
          - This offers a human-readable identifier for the owner, complementing the UUID.
        type: str
      project_reference_id:
        description:
          - The unique identifier (UUID) for the project this network function belongs to.
          - If you are using Nutanix Projects for resource segmentation, specify the project's UUID here.
          - This associates the network function with a specific project, allowing for project-based resource tracking, billing, and access control.
        type: str
      project_name:
        description:
          - The name of the project corresponding to the project_reference_id.
          - This makes it easy to identify the associated project in logs and UIs.
        type: str
      category_ids:
        description:
          - A list of UUIDs representing the categories associated with this resource.
          - Assign one or more category UUIDs (e.g., categories for "Environment Production" or "Service Firewall").
          - Categories are crucial for creating dynamic security policies.
          - For instance, a policy can be defined to apply to all VMs in a certain category, and this network function can be part of that policy.
        type: list
        elements: str
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
author:
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create network function with single NIC pair
  nutanix.ncp.ntnx_network_functions_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "my-network-function"
    description: "Network function for traffic inspection"
    high_availability_mode: ACTIVE_PASSIVE
    failure_handling: FAIL_OPEN
    traffic_forwarding_mode: INLINE
    nic_pairs:
      - ingress_nic_reference: "a3265671-de53-41be-af9b-f06241b95356"
        egress_nic_reference: "b4376782-ef64-52cf-bg0c-g17352ca6467"
        vm_reference: "c5487893-fg75-63dg-ch1d-h28463db7578"
        is_enabled: true
    data_plane_health_check_config:
      interval_secs: 5
      timeout_secs: 1
      success_threshold: 3
      failure_threshold: 3

- name: Create network function with VTAP mode
  nutanix.ncp.ntnx_network_functions_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "vtap-network-function"
    description: "VTAP mode for passive monitoring"
    high_availability_mode: ACTIVE_PASSIVE
    traffic_forwarding_mode: VTAP
    nic_pairs:
      - ingress_nic_reference: "a3265671-de53-41be-af9b-f06241b95356"
        is_enabled: true

- name: Create network function with two NIC pairs for HA
  nutanix.ncp.ntnx_network_functions_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    name: "ha-network-function"
    high_availability_mode: ACTIVE_PASSIVE
    failure_handling: FAIL_CLOSE
    traffic_forwarding_mode: INLINE
    nic_pairs:
      - ingress_nic_reference: "a3265671-de53-41be-af9b-f06241b95356"
        egress_nic_reference: "b4376782-ef64-52cf-bg0c-g17352ca6467"
        vm_reference: "c5487893-fg75-63dg-ch1d-h28463db7578"
        is_enabled: true
      - ingress_nic_reference: "d6598904-gh86-74eh-di2e-i39574ec8689"
        egress_nic_reference: "e7609015-hi97-85fi-ej3f-j40685fd979a"
        vm_reference: "f8710126-ij08-96gj-fk4g-k51796ge080b"
        is_enabled: true

- name: Update network function
  nutanix.ncp.ntnx_network_functions_v2:
    state: present
    nutanix_host: "{{ ip }}"
    validate_certs: false
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
    name: "updated-network-function"
    description: "Updated description"
    failure_handling: FAIL_CLOSE

- name: Delete network function
  nutanix.ncp.ntnx_network_functions_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
"""

RETURN = r"""
response:
    description:
      - Response for creating, updating, or deleting network functions.
      - Network function details if C(wait) is true and the operation is create or update.
      - Task details if C(wait) is false or the operation is delete.
    type: dict
    returned: always

ext_id:
    description:
        - External ID of the network function.
    type: str
    returned: always
task_ext_id:
    description: Task External ID
    returned: always
    type: str
    sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Api Exception raised while creating network function"
error:
    description: Error message if any
    returned: always
    type: str
changed:
    description: Indicates if the module made any changes
    returned: always
    type: bool
    sample: true
failed:
    description: Indicates if the module failed
    returned: when failed
    type: bool
    sample: false
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
    get_network_function_api_instance,
)
from ..module_utils.v4.network.helpers import get_network_function  # noqa: E402
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

    nic_pair_spec = dict(
        ingress_nic_reference=dict(type="str", required=True),
        egress_nic_reference=dict(type="str"),
        vm_reference=dict(type="str"),
        is_enabled=dict(type="bool", default=True),
    )

    data_plane_health_check_config_spec = dict(
        interval_secs=dict(type="int", default=5),
        timeout_secs=dict(type="int", default=1),
        success_threshold=dict(type="int", default=3),
        failure_threshold=dict(type="int", default=3),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        nic_pairs=dict(
            type="list",
            elements="dict",
            options=nic_pair_spec,
            obj=net_sdk.NicPair,
        ),
        high_availability_mode=dict(type="str", choices=["ACTIVE_PASSIVE"]),
        failure_handling=dict(
            type="str", choices=["FAIL_OPEN", "FAIL_CLOSE", "NO_ACTION"]
        ),
        traffic_forwarding_mode=dict(type="str", choices=["VTAP", "INLINE"]),
        data_plane_health_check_config=dict(
            type="dict",
            options=data_plane_health_check_config_spec,
            obj=net_sdk.DataPlaneHealthCheckConfig,
        ),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
    )

    return module_args


def create_network_function(module, result, network_functions):
    sg = SpecGenerator(module)
    default_spec = net_sdk.NetworkFunction()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create network function spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = network_functions.create_network_function(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating network function",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.NETWORK_FUNCTION
        )
        if ext_id:
            resp = get_network_function(module, network_functions, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_network_function_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec.to_dict())
    update_spec = strip_internal_attributes(update_spec.to_dict())
    old_spec_nic_pairs = old_spec.get("nic_pairs") or []
    update_spec_nic_pairs = update_spec.get("nic_pairs") or []
    if len(old_spec_nic_pairs) != len(update_spec_nic_pairs):
        return False
    for old_nic_pair, update_nic_pair in zip(old_spec_nic_pairs, update_spec_nic_pairs):
        old_nic_pair.pop("data_plane_health_status")
        old_nic_pair.pop("high_availability_state")
        update_nic_pair.pop("data_plane_health_status")
        update_nic_pair.pop("high_availability_state")
        if old_nic_pair != update_nic_pair:
            return False
    if old_spec != update_spec:
        return False
    return True


def update_network_function(module, result, network_functions):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_network_function(module, network_functions, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating network function", **result
        )

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating network function update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    result["current_spec"] = strip_internal_attributes(current_spec.to_dict())
    result["update_spec"] = strip_internal_attributes(update_spec.to_dict())
    if check_network_function_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = network_functions.update_network_function_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating network function",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_network_function(module, network_functions, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_network_function(module, result, network_functions):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Network function with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    try:
        resp = network_functions.delete_network_function_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting network function",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
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
        "error": None,
        "response": None,
        "ext_id": None,
    }
    network_functions = get_network_function_api_instance(module)
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_network_function(module, result, network_functions)
        else:
            create_network_function(module, result, network_functions)
    else:
        delete_network_function(module, result, network_functions)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
