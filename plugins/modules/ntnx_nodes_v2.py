#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nodes_v2
short_description: Onboard, update and delete nodes managed by Foundation Central
version_added: 2.7.0
description:
  - This module allows you to onboard (create), update and delete nodes managed by Foundation Central.
  - A node represents a physical server managed by Foundation Central, including its hardware, network and lifecycle state.
  - This module uses the Life Cycle Management v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central) (FCVM/Foundation), NOT to Prism Central.
    Set C(nutanix_host) to the Foundation Central endpoint.
  - >-
    B(Onboard a Node) - Requires the appropriate Foundation Central administrator role
    on the FCVM.
  - >-
    B(Update a Node) - Requires the appropriate Foundation Central administrator role
    on the FCVM.
  - >-
    B(Delete a Node) - Requires the appropriate Foundation Central administrator role
    on the FCVM.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will onboard (create) a node.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the node.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the node.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the node.
      - Required for update and delete operations.
    type: str
    required: false
  manufacturer:
    description:
      - Manufacturer of the node.
    type: str
    required: false
  identifiers:
    description:
      - List of unique identifiers for the node.
    type: list
    elements: dict
    required: false
    suboptions:
      type:
        description:
          - Type of the node identifier.
        type: str
        required: true
        choices:
          - SERIAL_NUMBER
      value:
        description:
          - Value of the node identifier.
        type: str
        required: false
  host_type:
    description:
      - Type of the hypervisor installed on the node's host.
    type: str
    required: false
    choices:
      - AHV
      - ESX
  host_version:
    description:
      - Version of the hypervisor installed on the node's host.
    type: str
    required: false
  aos_version:
    description:
      - Version of AOS installed on the node.
    type: str
    required: false
  model:
    description:
      - Hardware model of the node.
    type: str
    required: false
  memory_gb:
    description:
      - Total memory of the node in GB.
    type: int
    required: false
  custom_attributes:
    description:
      - List of custom attributes associated with the node.
    type: list
    elements: str
    required: false
  owner_ext_id:
    description:
      - External ID of the owner of the node.
    type: str
    required: false
  hostname:
    description:
      - Hostname of the node.
    type: str
    required: false
  block_serial_number:
    description:
      - Block serial number of the node.
    type: str
    required: false
  provider_ext_id:
    description:
      - External ID of the hardware provider that manages this node.
    type: str
    required: false
  provider_connection_ext_id:
    description:
      - External ID of the hardware provider connection used to discover this node.
    type: str
    required: false
  cpu_info:
    description:
      - CPU information of the node.
    type: dict
    required: false
    suboptions:
      manufacturer:
        description:
          - Manufacturer of the CPU.
        type: str
        required: false
      model:
        description:
          - Model of the CPU.
        type: str
        required: false
      capacity_g_hz:
        description:
          - CPU capacity in GHz.
        type: float
        required: false
      logical_core_count:
        description:
          - Number of logical cores.
        type: int
        required: false
      socket_count:
        description:
          - Number of CPU sockets.
        type: int
        required: false
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
- name: Onboard a node with all attributes
  nutanix.ncp.ntnx_nodes_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    manufacturer: "Nutanix"
    model: "NX-3060-G7"
    host_type: "AHV"
    host_version: "10.0"
    aos_version: "7.0"
    memory_gb: 512
    hostname: "node-ansible"
    block_serial_number: "20SM6M420001"
    custom_attributes:
      - "rack=1"
    identifiers:
      - type: "SERIAL_NUMBER"
        value: "ZM204S000001"
    cpu_info:
      manufacturer: "Intel"
      model: "Xeon Gold 6248"
      capacity_g_hz: 2.5
      logical_core_count: 40
      socket_count: 2
  register: result
  ignore_errors: true

- name: Update a node with all attributes
  nutanix.ncp.ntnx_nodes_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    manufacturer: "Nutanix"
    model: "NX-3060-G8"
    host_type: "AHV"
    host_version: "10.0.1"
    aos_version: "7.0.1"
    memory_gb: 1024
    hostname: "node-ansible-updated"
    block_serial_number: "20SM6M420001"
    custom_attributes:
      - "rack=2"
    identifiers:
      - type: "SERIAL_NUMBER"
        value: "ZM204S000001"
    cpu_info:
      manufacturer: "Intel"
      model: "Xeon Gold 6348"
      capacity_g_hz: 2.6
      logical_core_count: 56
      socket_count: 2
  register: result
  ignore_errors: true

- name: Delete a node
  nutanix.ncp.ntnx_nodes_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for onboarding, updating or deleting a node.
    - For create or update, when C(wait) is true it returns the node details, otherwise the task details.
    - For delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "aos_version": "7.0",
      "block_serial_number": "20SM6M420001",
      "cpu_info": {
        "capacity_g_hz": 2.5,
        "logical_core_count": 40,
        "manufacturer": "Intel",
        "model": "Xeon Gold 6248",
        "socket_count": 2
      },
      "custom_attributes": ["rack=1"],
      "cvm_connectivity_status": null,
      "ext_id": "d1a1a1a1-1111-2222-3333-444455556666",
      "host_connectivity_status": null,
      "host_type": "AHV",
      "host_version": "10.0",
      "hostname": "node-ansible",
      "identifiers": [{"type": "SERIAL_NUMBER", "value": "ZM204S000001"}],
      "links": null,
      "manufacturer": "Nutanix",
      "memory_gb": 512,
      "model": "NX-3060-G7",
      "network_details": null,
      "owner_ext_id": null,
      "provider_connection_ext_id": null,
      "provider_data": null,
      "provider_ext_id": null,
      "state": "ONBOARDED",
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
    - The external ID of the node.
  returned: always
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped due to idempotency.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: contextual
  type: str
  sample: "Node with ext_id:d1a1a1a1-1111-2222-3333-444455556666 will be deleted."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_etag,
    get_nodes_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_node  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    node_identifier_spec = dict(
        type=dict(type="str", required=True, choices=["SERIAL_NUMBER"]),
        value=dict(type="str", required=False),
    )

    cpu_info_spec = dict(
        manufacturer=dict(type="str", required=False),
        model=dict(type="str", required=False),
        capacity_g_hz=dict(type="float", required=False),
        logical_core_count=dict(type="int", required=False),
        socket_count=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        manufacturer=dict(type="str"),
        identifiers=dict(
            type="list",
            elements="dict",
            options=node_identifier_spec,
            obj=lifecycle_sdk.NodeIdentifier,
        ),
        host_type=dict(type="str", choices=["AHV", "ESX"]),
        host_version=dict(type="str"),
        aos_version=dict(type="str"),
        model=dict(type="str"),
        memory_gb=dict(type="int"),
        custom_attributes=dict(type="list", elements="str"),
        owner_ext_id=dict(type="str"),
        hostname=dict(type="str"),
        block_serial_number=dict(type="str"),
        provider_ext_id=dict(type="str"),
        provider_connection_ext_id=dict(type="str"),
        cpu_info=dict(
            type="dict",
            options=cpu_info_spec,
            obj=lifecycle_sdk.CpuInfo,
        ),
    )
    return module_args


def _spec_attrs(module):
    """Return module params without the Ansible control params that collide with
    SDK ``Node`` fields (for example the Ansible ``state`` param collides with
    the read-only ``Node.state`` field)."""
    attrs = deepcopy(module.params)
    attrs.pop("state", None)
    return attrs


def create_nodes(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.Node()
    spec, err = sg.generate_spec(obj=default_spec, attr=_spec_attrs(module))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for onboarding node", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_node(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while onboarding node",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_nodes_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_nodes(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current = get_node(module, api_instance, ext_id)
    etag = get_etag(data=current)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating node with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(
        obj=deepcopy(current.data), attr=_spec_attrs(module)
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for updating node", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_nodes_idempotency(current.data.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(
            msg="Nothing to change. Node with ext_id: {0} is already in the desired state.".format(
                ext_id
            ),
            **result,
        )

    resp = None
    try:
        resp = api_instance.update_node_by_id(extId=ext_id, body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating node with ext_id: {0}".format(
                ext_id
            ),
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_node(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_nodes(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Node with ext_id:{0} will be deleted.".format(ext_id)
        return

    current = get_node(module, api_instance, ext_id)
    etag = get_etag(data=current)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.delete_node_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting node with ext_id: {0}".format(
                ext_id
            ),
        )
    if resp is not None and getattr(resp, "data", None) is not None:
        task_ext_id = resp.data.ext_id
        result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_nodes_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_nodes(module, result, api_instance)
        else:
            create_nodes(module, result, api_instance)
    else:
        delete_nodes(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
