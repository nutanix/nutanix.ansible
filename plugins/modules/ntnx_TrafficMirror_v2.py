#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_TrafficMirror_v2
short_description: Create, Update and Delete Traffic mirror sessions in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update and delete Traffic mirror sessions in Nutanix Prism Central.
  - A Traffic mirror session mirrors network traffic from a set of source ports to a set of destination ports for monitoring or inspection.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Traffic mirror session) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin.
    - >-
      B(Update a Traffic mirror session) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin.
    - >-
      B(Delete a Traffic mirror session) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin.
    - Requires the referenced virtual switch, clusters, hosts and NICs to exist before creating the Traffic mirror session.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create the Traffic mirror session.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the Traffic mirror session.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the Traffic mirror session.
    type: str
    choices:
      - present
      - absent
  ext_id:
    description:
      - The external ID (UUID) of the Traffic mirror session.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the Traffic mirror session.
      - Required for the create operation.
    type: str
    required: false
  description:
    description:
      - Description of the Traffic mirror session.
    type: str
    required: false
  source_list:
    description:
      - List of source ports to mirror traffic from.
      - Required for the create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      direction:
        description:
          - Direction of the traffic to mirror from the source port.
        type: str
        choices:
          - INGRESS
          - EGRESS
          - BIDIRECTIONAL
        required: true
      nic_type:
        description:
          - Type of the source NIC.
        type: str
        choices:
          - HOST_NIC
          - VIRTUAL_NIC
        required: false
      nic_uuid:
        description:
          - UUID of the source NIC (host NIC or virtual NIC) to mirror traffic from.
        type: str
        required: false
      is_up:
        description:
          - Whether the source NIC is up.
          - This attribute is read-only and populated by the server.
        type: bool
        required: false
  destination_list:
    description:
      - List of destination ports where mirrored traffic will be sent.
      - Required for the create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      nic_type:
        description:
          - Type of the destination NIC.
        type: str
        choices:
          - HOST_NIC
          - VIRTUAL_NIC
        required: true
      nic_uuid:
        description:
          - UUID of the destination NIC (host NIC or virtual NIC) where mirrored traffic is sent.
        type: str
        required: false
      is_up:
        description:
          - Whether the destination NIC is up.
          - This attribute is read-only and populated by the server.
        type: bool
        required: false
  is_enabled:
    description:
      - Whether the Traffic mirror session is enabled.
    type: bool
    required: false
    default: true
  cluster_reference_list:
    description:
      - List of cluster UUIDs that the Traffic mirror session applies to.
    type: list
    elements: str
    required: false
  host_reference_list:
    description:
      - List of host UUIDs that the Traffic mirror session applies to.
    type: list
    elements: str
    required: false
  virtual_switch_reference:
    description:
      - UUID of the virtual switch that the Traffic mirror session applies to.
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
- name: Create Traffic mirror session
  nutanix.ncp.ntnx_TrafficMirror_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "traffic_mirror_ansible"
    description: "Traffic mirror session created by Ansible"
    is_enabled: true
    source_list:
      - direction: "BIDIRECTIONAL"
        nic_type: "VIRTUAL_NIC"
        nic_uuid: "a3265671-de53-41be-af9b-f06241b95356"
    destination_list:
      - nic_type: "VIRTUAL_NIC"
        nic_uuid: "b4376782-ef64-52cf-bc0c-a17352ca6467"
    virtual_switch_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    cluster_reference_list:
      - "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Update Traffic mirror session
  nutanix.ncp.ntnx_TrafficMirror_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d"
    name: "traffic_mirror_ansible_updated"
    description: "Updated Traffic mirror session"
    is_enabled: false
    source_list:
      - direction: "INGRESS"
        nic_type: "VIRTUAL_NIC"
        nic_uuid: "a3265671-de53-41be-af9b-f06241b95356"
    destination_list:
      - nic_type: "VIRTUAL_NIC"
        nic_uuid: "b4376782-ef64-52cf-bc0c-a17352ca6467"
    virtual_switch_reference: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    cluster_reference_list:
      - "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: Delete Traffic mirror session
  nutanix.ncp.ntnx_TrafficMirror_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating or deleting a Traffic mirror session.
    - Traffic mirror session details if C(wait) is true and the operation is create or update.
    - Task details if C(wait) is false or the operation is delete.
  returned: always
  type: dict
  sample:
    {
      "cluster_reference_list": ["bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"],
      "description": "Traffic mirror session created by Ansible",
      "destination_list": [
          {
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "b4376782-ef64-52cf-bc0c-a17352ca6467"
          }
      ],
      "ext_id": "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d",
      "host_reference_list": null,
      "is_enabled": true,
      "links": null,
      "metadata": null,
      "name": "traffic_mirror_ansible",
      "source_list": [
          {
              "direction": "BIDIRECTIONAL",
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "a3265671-de53-41be-af9b-f06241b95356"
          }
      ],
      "state": "ACTIVE",
      "state_message": null,
      "tenant_id": null,
      "virtual_switch_reference": "2e40ff57-20aa-4d2b-b179-298db969c20d"
    }

ext_id:
  description:
    - External ID of the Traffic mirror session.
  returned: always
  type: str
  sample: "3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d"

task_ext_id:
  description:
    - Task External ID.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Message explaining why the operation was skipped when the module is idempotent.
  returned: when the operation is skipped
  type: str
  sample: "TrafficMirror with name 'traffic_mirror_ansible' already exists. Skipping creation."

error:
  description: Error message if any error occurred during the operation.
  returned: when an error occurs
  type: str

failed:
  description: Indicates whether the module operation failed.
  returned: when the operation fails
  type: bool
  sample: false

msg:
  description: Status message describing the outcome of the operation.
  returned: when there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Traffic mirror session with ext_id:3f8b1c2d-2e3f-4a5b-6c7d-8e9f0a1b2c3d will be deleted."
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
    get_traffic_mirrors_api_instance,
)
from ..module_utils.v4.network.helpers import get_traffic_mirror  # noqa: E402
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

    source_port_spec = dict(
        direction=dict(
            type="str",
            choices=["INGRESS", "EGRESS", "BIDIRECTIONAL"],
            required=True,
            obj=networking_sdk.TrafficMirrorSourcePortDirection,
        ),
        nic_type=dict(
            type="str",
            choices=["HOST_NIC", "VIRTUAL_NIC"],
            required=False,
            obj=networking_sdk.TrafficMirrorPortNicType,
        ),
        nic_uuid=dict(type="str", required=False),
        is_up=dict(type="bool", required=False),
    )

    destination_port_spec = dict(
        nic_type=dict(
            type="str",
            choices=["HOST_NIC", "VIRTUAL_NIC"],
            required=True,
            obj=networking_sdk.TrafficMirrorPortNicType,
        ),
        nic_uuid=dict(type="str", required=False),
        is_up=dict(type="bool", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        source_list=dict(
            type="list",
            elements="dict",
            options=source_port_spec,
            obj=networking_sdk.TrafficMirrorSourcePort,
        ),
        destination_list=dict(
            type="list",
            elements="dict",
            options=destination_port_spec,
            obj=networking_sdk.TrafficMirrorPort,
        ),
        is_enabled=dict(type="bool", default=True),
        cluster_reference_list=dict(type="list", elements="str"),
        host_reference_list=dict(type="list", elements="str"),
        virtual_switch_reference=dict(type="str"),
    )

    return module_args


def _check_for_idempotency(old_spec, update_spec):
    old_dict = strip_internal_attributes(old_spec.to_dict())
    update_dict = strip_internal_attributes(update_spec.to_dict())
    for key in ("state", "state_message"):
        old_dict.pop(key, None)
        update_dict.pop(key, None)
    return old_dict == update_dict


def _remove_read_only_attributes(spec):
    """Remove read-only attributes populated by the server before an update."""
    for attr in ("state", "state_message"):
        if hasattr(spec, attr):
            setattr(spec, attr, None)
    if getattr(spec, "source_list", None):
        for port in spec.source_list:
            port.is_up = None
    if getattr(spec, "destination_list", None):
        for port in spec.destination_list:
            port.is_up = None


def create_TrafficMirror(module, result, api_instance):
    validate_required_params(module, ["name", "source_list", "destination_list"])
    sg = SpecGenerator(module)
    default_spec = networking_sdk.TrafficMirror()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Traffic mirror session spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_traffic_mirror(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Traffic mirror session",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.TRAFFIC_MIRROR
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_traffic_mirror(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def update_TrafficMirror(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_traffic_mirror(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating Traffic mirror session", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update Traffic mirror session spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _check_for_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    _remove_read_only_attributes(update_spec)

    resp = None
    try:
        resp = api_instance.update_traffic_mirror_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Traffic mirror session",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_traffic_mirror(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_TrafficMirror(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Traffic mirror session with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_traffic_mirror_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Traffic mirror session",
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
        "response": None,
        "error": None,
        "ext_id": None,
    }
    api_instance = get_traffic_mirrors_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_TrafficMirror(module, result, api_instance)
        else:
            create_TrafficMirror(module, result, api_instance)
    else:
        delete_TrafficMirror(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
