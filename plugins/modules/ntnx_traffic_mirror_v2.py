#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_traffic_mirror_v2
short_description: Create, Update, Delete traffic mirror sessions in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete traffic mirror (port mirror / SPAN) sessions in Nutanix Prism Central.
  - A traffic mirror session duplicates network traffic from a set of source ports (physical host NICs or VM virtual NICs)
    to a set of destination ports for network troubleshooting, security monitoring, or packet analysis.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Traffic Mirror session) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Update a Traffic Mirror session) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Traffic Mirror session) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create traffic mirror session.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update traffic mirror session.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete traffic mirror session.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the traffic mirror session.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the traffic mirror session.
      - Required for create operation.
      - Maximum 128 characters.
    type: str
    required: false
  description:
    description:
      - Description of the traffic mirror session.
      - Maximum 1000 characters.
    type: str
    required: false
  source_list:
    description:
      - List of source ports of the session.
      - Maximum of 4 source ports are allowed per session.
      - Each session should have at least 1 source port.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      direction:
        description:
          - Direction of the traffic being mirrored on the source port.
          - C(BIDIRECTIONAL) mirrors both ingress and egress traffic.
          - C(EGRESS) mirrors only outgoing traffic.
          - C(INGRESS) mirrors only incoming traffic.
        type: str
        required: true
        choices:
          - BIDIRECTIONAL
          - EGRESS
          - INGRESS
      nic_type:
        description:
          - Type of the NIC to use as source.
          - C(HOST_NIC) mirrors a physical host NIC (a host uplink or bond).
          - C(VIRTUAL_NIC) mirrors a VM virtual NIC.
        type: str
        required: false
        choices:
          - HOST_NIC
          - VIRTUAL_NIC
      nic_uuid:
        description:
          - UUID of the NIC (host NIC or VM vNIC) to mirror traffic from.
        type: str
        required: false
      is_up:
        description:
          - Read-only. Indicates whether the port is up.
          - Set by the platform; ignored on create/update requests.
        type: bool
        required: false
  destination_list:
    description:
      - List of destination ports of the session.
      - Maximum of 2 destination ports are allowed per session.
      - Each session should have at least 1 destination port.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      nic_type:
        description:
          - Type of the NIC to use as destination.
          - C(HOST_NIC) sends mirrored traffic to a physical host NIC.
          - C(VIRTUAL_NIC) sends mirrored traffic to a VM virtual NIC.
        type: str
        required: true
        choices:
          - HOST_NIC
          - VIRTUAL_NIC
      nic_uuid:
        description:
          - UUID of the destination NIC.
        type: str
        required: false
      is_up:
        description:
          - Read-only. Indicates whether the port is up.
          - Set by the platform; ignored on create/update requests.
        type: bool
        required: false
  is_enabled:
    description:
      - Indicates whether the port mirroring session is enabled or not.
      - Defaults to true when creating a new session.
    type: bool
    required: false
  cluster_reference_list:
    description:
      - List of cluster UUIDs that are configured for this session.
      - Currently, only 1 cluster is allowed to participate in a session.
    type: list
    elements: str
    required: false
  host_reference_list:
    description:
      - List of host UUIDs that are configured for this session.
      - Currently, only 1 host is allowed to participate in a session.
    type: list
    elements: str
    required: false
  virtual_switch_reference:
    description:
      - Traffic mirror virtual switch reference to use for Remote SPAN.
      - Required when the destination VM lives on a different host than the source.
    type: str
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
- name: Create a traffic mirror session (VM to VM on the same host)
  nutanix.ncp.ntnx_traffic_mirror_v2:
    state: present
    name: "tm_ansible_local"
    description: "Traffic mirror session created by Ansible"
    is_enabled: true
    source_list:
      - direction: BIDIRECTIONAL
        nic_type: VIRTUAL_NIC
        nic_uuid: "b1f8ce4b-6c8a-4d13-9c8f-8e2d1a1f8b3e"
    destination_list:
      - nic_type: VIRTUAL_NIC
        nic_uuid: "5d2ac2b8-b60a-4de6-9345-6f34e79e7a19"
    cluster_reference_list:
      - "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    host_reference_list:
      - "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result

- name: Update a traffic mirror session
  nutanix.ncp.ntnx_traffic_mirror_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "tm_ansible_local_updated"
    description: "Updated traffic mirror session"
    is_enabled: false
    source_list:
      - direction: INGRESS
        nic_type: VIRTUAL_NIC
        nic_uuid: "b1f8ce4b-6c8a-4d13-9c8f-8e2d1a1f8b3e"
    destination_list:
      - nic_type: VIRTUAL_NIC
        nic_uuid: "5d2ac2b8-b60a-4de6-9345-6f34e79e7a19"
    cluster_reference_list:
      - "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    host_reference_list:
      - "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result

- name: Delete a traffic mirror session
  nutanix.ncp.ntnx_traffic_mirror_v2:
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a traffic mirror session.
    - If the operation is create or update and C(wait) is true, it will return the traffic mirror session details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_reference_list": [
          "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
      ],
      "description": "Traffic mirror session created by Ansible",
      "destination_list": [
          {
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "5d2ac2b8-b60a-4de6-9345-6f34e79e7a19"
          }
      ],
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "host_reference_list": [
          "8300384a-56ee-4750-aeb8-3d1c42908bee"
      ],
      "is_enabled": true,
      "links": null,
      "metadata": null,
      "name": "tm_ansible_local",
      "source_list": [
          {
              "direction": "BIDIRECTIONAL",
              "is_up": true,
              "nic_type": "VIRTUAL_NIC",
              "nic_uuid": "b1f8ce4b-6c8a-4d13-9c8f-8e2d1a1f8b3e"
          }
      ],
      "state": "ACTIVE",
      "state_message": null,
      "tenant_id": null,
      "virtual_switch_reference": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the traffic mirror session.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the operation was skipped due to idempotency.
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
  returned: When there is an error, module is idempotent, or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating traffic mirror"
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
            required=True,
            choices=["BIDIRECTIONAL", "EGRESS", "INGRESS"],
            obj=networking_sdk.TrafficMirrorSourcePortDirection,
        ),
        nic_type=dict(
            type="str",
            required=False,
            choices=["HOST_NIC", "VIRTUAL_NIC"],
            obj=networking_sdk.TrafficMirrorPortNicType,
        ),
        nic_uuid=dict(type="str", required=False),
        is_up=dict(type="bool", required=False),
    )

    destination_port_spec = dict(
        nic_type=dict(
            type="str",
            required=True,
            choices=["HOST_NIC", "VIRTUAL_NIC"],
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
        is_enabled=dict(type="bool"),
        cluster_reference_list=dict(type="list", elements="str"),
        host_reference_list=dict(type="list", elements="str"),
        virtual_switch_reference=dict(type="str"),
    )
    return module_args


def _params_without_state(module):
    """Ansible's ``state`` param collides with the SDK's ``TrafficMirror.state``
    field (ACTIVE/DISABLED/ERROR), so drop it before feeding params to the
    SpecGenerator. The state param has already been dispatched by run_module()
    at this point."""
    attr = deepcopy(module.params)
    attr.pop("state", None)
    return attr


def create_traffic_mirror(module, result, api_instance):
    validate_required_params(module, ["name", "source_list", "destination_list"])
    sg = SpecGenerator(module)
    default_spec = networking_sdk.TrafficMirror()
    spec, err = sg.generate_spec(obj=default_spec, attr=_params_without_state(module))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create traffic mirror spec", **result)

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
            msg="Api Exception raised while creating traffic mirror",
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
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Traffic Mirror"
                ),
                msg="Failed to get entity ext_id from task for Traffic Mirror",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Compare user-facing fields on old vs update spec to detect no-op updates."""
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in ("state", "state_message", "links", "tenant_id", "metadata"):
        old.pop(field, None)
        new.pop(field, None)
    for port in list(old.get("source_list") or []) + list(
        old.get("destination_list") or []
    ):
        if isinstance(port, dict):
            port.pop("is_up", None)
    for port in list(new.get("source_list") or []) + list(
        new.get("destination_list") or []
    ):
        if isinstance(port, dict):
            port.pop("is_up", None)
    return old == new


def _remove_read_only_attributes(spec):
    """Clear server-populated read-only fields before update."""
    spec.state = None
    spec.state_message = None
    spec.links = None
    spec.tenant_id = None
    if spec.source_list:
        for port in spec.source_list:
            port.is_up = None
    if spec.destination_list:
        for port in spec.destination_list:
            port.is_up = None


def update_traffic_mirror(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_traffic_mirror(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating traffic mirror", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(
        obj=deepcopy(old_spec), attr=_params_without_state(module)
    )
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update traffic mirror spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

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
            msg="Api Exception raised while updating traffic mirror",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_traffic_mirror(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_traffic_mirror(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Traffic mirror with ext_id:{0} will be deleted.".format(ext_id)
        return

    current = get_traffic_mirror(module, api_instance, ext_id)
    etag = get_etag(data=current)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.delete_traffic_mirror_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting traffic mirror",
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
    }
    api_instance = get_traffic_mirrors_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_traffic_mirror(module, result, api_instance)
        else:
            create_traffic_mirror(module, result, api_instance)
    else:
        delete_traffic_mirror(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
