#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nodes_v2
short_description: Create, Update, Delete Foundation Central nodes
version_added: "2.7.0"
description:
  - Create, Update, Delete Foundation Central nodes.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a Node) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Update a Node) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Delete a Node) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create node.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update node.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete node.
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
      - Manufacturer of the node
      - Required for create operation.
    type: str
    required: false
  identifiers:
    description:
      - Unique identifier array for the node (currently limited to 1 item with SERIAL_NUMBER type)
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      type:
        description:
          - Type of the unique identifier of the node
        type: str
        required: true
        choices:
          - SERIAL_NUMBER
      value:
        description:
          - Unique identifier value of the node
        type: str
        required: true
  provider_connection_ext_id:
    description:
      - External ID of the provider connection of the node
    type: str
    required: false
  custom_attributes:
    description:
      - User tags of the node
    type: list
    elements: str
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
- name: Create a node
  nutanix.ncp.ntnx_nodes_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    manufacturer: "Nutanix"
    identifiers:
      - type: "SERIAL_NUMBER"
        value: "ZM204S000001"
    provider_connection_ext_id: "0b1c8b69-8d3d-440e-b12e-bf41f89f85e7"
    custom_attributes:
      - "rack=1"
  register: result
  ignore_errors: true

- name: Update a node
  nutanix.ncp.ntnx_nodes_v2:
    nutanix_host: "{{ foundation_central_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
    manufacturer: "Nutanix"
    identifiers:
      - type: "SERIAL_NUMBER"
        value: "ZM204S000001"
    custom_attributes:
      - "rack=2"
  register: result
  ignore_errors: true

- name: Delete a node
  nutanix.ncp.ntnx_nodes_v2:
    nutanix_host: "{{ foundation_central_host }}"
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
    - Response for creating, updating, or deleting a node.
    - If the operation is create or update and C(wait) is true, it will return the node details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
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
  description: This indicates whether the task was skipped due to idempotency.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating node"
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
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    node_identifier_spec = dict(
        type=dict(type="str", required=True, choices=["SERIAL_NUMBER"]),
        value=dict(type="str", required=True),
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
        provider_connection_ext_id=dict(type="str"),
        custom_attributes=dict(type="list", elements="str"),
    )
    return module_args


def create_nodes(module, result, api_instance):
    validate_required_params(module, ["manufacturer", "identifiers"])
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.Node()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create node spec", **result)

    # SpecGenerator picks up Ansible's 'state' param ("present"/"absent")
    # and sets it on the SDK object; reset to None so the API does not
    # receive an invalid enum value.
    spec.state = None

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
            msg="Api Exception raised while creating node",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            node = get_node(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(node.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception("Failed to get entity ext_id from task for node"),
                msg="Failed to get entity ext_id from task for node",
            )
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
        return module.fail_json(msg="Unable to fetch etag for updating node", **result)

    kwargs = {"if_match": etag}

    # Preserve original state before SpecGenerator overwrites it
    original_state = current.state

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update node spec", **result)

    # Restore original state so that Ansible's "present"/"absent"
    # does not leak into the API payload.
    update_spec.state = original_state

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_nodes_idempotency(current.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_node_by_id(extId=ext_id, body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating node",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        node = get_node(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(node.to_dict())
    result["changed"] = True


def delete_nodes(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Node with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_node_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting node",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
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
        "response": None,
        "ext_id": None,
        "failed": False,
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
