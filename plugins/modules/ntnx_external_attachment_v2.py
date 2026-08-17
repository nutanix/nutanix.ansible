#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_external_attachment_v2
short_description: Attach or detach an iSCSI external attachment on a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to attach an iSCSI client to a Volume Group as an external attachment,
    and to detach an existing external attachment from a Volume Group in Nutanix Prism Central.
  - When C(state) is C(present) and C(ext_id) is not provided, a new iSCSI external attachment is created (attached).
  - When C(state) is C(present) and C(ext_id) is provided, the module verifies that the referenced
    external attachment already exists on the given Volume Group; the fields of an existing
    attachment (iSCSI initiator identity, virtual targets, CHAP secret, attachment site) are
    immutable, so this path is idempotent.
  - When C(state) is C(absent), the referenced external attachment is detached from the Volume Group.
  - This module uses the PC v4 storage APIs (ntnx_storage_py_client).
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, an iSCSI external
        attachment is created for the given Volume Group.
      - If C(state) is set to C(present) and C(ext_id) is provided, the module confirms
        the external attachment exists (no server-side update is supported).
      - If C(state) is set to C(absent) and C(ext_id) is provided, the external attachment
        is detached from the given Volume Group.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the external (iSCSI) attachment.
      - Required for update (idempotency check) and delete (detach) operations.
    type: str
    required: false
  volume_group_ext_id:
    description:
      - The external ID of the parent Volume Group.
      - Required for every operation on an external attachment.
    type: str
    required: true
  iscsi_initiator_name:
    description:
      - iSCSI initiator name (IQN) of the client to attach.
      - Exactly one of C(iscsi_initiator_name) or C(iscsi_initiator_network_id) must be
        specified when creating an attachment.
      - This field is used for create only; iSCSI initiator identity is immutable after attach.
      - Maximum 64 characters.
    type: str
    required: false
  iscsi_initiator_network_id:
    description:
      - The network identifier of the iSCSI initiator, expressed as an IPv4 address,
        IPv6 address, or Fully Qualified Domain Name.
      - Mutually exclusive with C(iscsi_initiator_name).
      - This field is used for create only; iSCSI initiator identity is immutable after attach.
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the iSCSI initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv4 address value.
            type: str
            required: true
      ipv6:
        description:
          - IPv6 address of the iSCSI initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The IPv6 address value.
            type: str
            required: true
      fqdn:
        description:
          - Fully qualified domain name of the iSCSI initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The FQDN value.
            type: str
            required: true
  client_secret:
    description:
      - iSCSI initiator client secret used when CHAP authentication is enabled.
      - This field must only be provided when C(enabled_authentications) is set to C(CHAP).
    type: str
    required: false
  enabled_authentications:
    description:
      - Authentication type enabled for the Volume Group attachment.
      - If set to C(CHAP), C(client_secret) must be provided.
      - If omitted, no client authentication is configured.
    type: str
    required: false
    choices:
      - CHAP
      - NONE
    default: NONE
  target_params:
    description:
      - List of iSCSI target parameters that will be visible and accessible to the iSCSI client.
    type: list
    elements: dict
    required: false
    suboptions:
      num_virtual_targets:
        description:
          - Number of virtual targets generated for the iSCSI target.
          - This field is immutable after attach.
        type: int
        required: false
  num_virtual_targets:
    description:
      - Convenience alias for C(target_params[0].num_virtual_targets).
      - Sets the number of virtual targets generated for the iSCSI target.
      - Ignored if C(target_params) is also provided.
      - This field is immutable after attach.
    type: int
    required: false
  cluster_reference:
    description:
      - UUID of the cluster that will host the iSCSI client attachment.
      - Format is a standard UUID (8-4-4-4-12).
    type: str
    required: false
  attachment_site:
    description:
      - The site where the Volume Group attach operation should be processed.
      - This field may only be set if Metro DR / Synchronous Replication has been
        configured for the Volume Group.
    type: str
    required: false
    choices:
      - PRIMARY
      - SECONDARY
  iscsi_target_names:
    description:
      - List of iSCSI target names that will be visible and accessible to the iSCSI client.
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
- name: Attach an iSCSI external attachment to a Volume Group using initiator IQN
  nutanix.ncp.ntnx_external_attachment_v2:
    state: present
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
    iscsi_initiator_name: "iqn.1991-05.com.microsoft:ansible-host-01"
    num_virtual_targets: 32
    enabled_authentications: NONE
    attachment_site: PRIMARY
  register: attach_result

- name: Attach an iSCSI external attachment to a Volume Group using initiator IPv4
  nutanix.ncp.ntnx_external_attachment_v2:
    state: present
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
    iscsi_initiator_network_id:
      ipv4:
        value: "10.0.0.10"
    num_virtual_targets: 32
    enabled_authentications: CHAP
    client_secret: "Nutanix.1234567"
    attachment_site: PRIMARY

- name: Detach an existing iSCSI external attachment from a Volume Group
  nutanix.ncp.ntnx_external_attachment_v2:
    state: absent
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting an iSCSI external attachment on a Volume Group.
    - If the operation is create and C(wait) is true, this contains the completed task details.
    - If the operation is create and C(wait) is false, this contains the initial task metadata.
    - If the operation is delete, this contains the task details.
    - If C(state) is C(present) with an C(ext_id) that already exists, this contains the
      external attachment record fetched from the Volume Group (idempotent path).
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-20T15:19:00.229645+00:00",
      "created_time": "2026-07-20T15:19:00.095273+00:00",
      "entities_affected": [
        {
          "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
          "rel": "storage:config:iscsi-client"
        },
        {
          "ext_id": "11ac5593-c9cf-403d-641c-3bf76eff2193",
          "rel": "storage:config:volume-group"
        }
      ],
      "ext_id": "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T15:19:00.229642+00:00",
      "operation": "VolumeGroupAttachExternal",
      "operation_description": "Volume group attach to iSCSI Client",
      "progress_percentage": 100,
      "started_time": "2026-07-20T15:19:00.122260+00:00",
      "status": "SUCCEEDED"
    }

task_ext_id:
  description:
    - The external ID of the async task tracking the attach or detach action.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the iSCSI external attachment.
    - Populated on successful create when the task's ``entities_affected`` includes the
      attachment. Populated as input on update/delete.
  returned: always
  type: str
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

changed:
  description: Indicates whether the module made any changes on the cluster.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - True when the operation was a no-op idempotency path (e.g. update on an already
      existing external attachment whose fields are immutable).
  returned: When applicable
  type: bool
  sample: false

error:
  description: Error message returned by the API (if any).
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description:
    - Status or error message. Populated on error, on idempotent skips, and on
      check-mode delete paths.
  returned: When there is an error, module is idempotent, or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while attaching iSCSI client to Volume Group"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.storage.helpers import (  # noqa: E402
    get_external_attachment_by_ext_id,
    get_volume_group,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    address_spec = dict(
        value=dict(type="str", required=True),
    )

    iscsi_initiator_network_id_spec = dict(
        ipv4=dict(type="dict", options=address_spec, obj=storage_sdk.IPv4Address),
        ipv6=dict(type="dict", options=address_spec, obj=storage_sdk.IPv6Address),
        fqdn=dict(type="dict", options=address_spec, obj=storage_sdk.FQDN),
    )

    target_params_spec = dict(
        num_virtual_targets=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        volume_group_ext_id=dict(type="str", required=True),
        iscsi_initiator_name=dict(type="str", required=False),
        iscsi_initiator_network_id=dict(
            type="dict",
            options=iscsi_initiator_network_id_spec,
            required=False,
            obj=storage_sdk.IPAddressOrFQDN,
        ),
        client_secret=dict(type="str", required=False, no_log=True),
        enabled_authentications=dict(
            type="str",
            required=False,
            choices=["CHAP", "NONE"],
            default="NONE",
        ),
        target_params=dict(
            type="list",
            elements="dict",
            options=target_params_spec,
            required=False,
            obj=storage_sdk.TargetParam,
        ),
        num_virtual_targets=dict(type="int", required=False),
        cluster_reference=dict(type="str", required=False),
        attachment_site=dict(
            type="str",
            required=False,
            choices=["PRIMARY", "SECONDARY"],
        ),
        iscsi_target_names=dict(
            type="list",
            elements="str",
            required=False,
        ),
    )

    return module_args


def _apply_num_virtual_targets_alias(module):
    """
    If the caller passed ``num_virtual_targets`` but not ``target_params``,
    synthesise a single-element ``target_params`` list so SpecGenerator
    can populate the SDK object. If the caller passed both, ``target_params``
    wins and the alias is ignored.
    """
    if module.params.get("target_params"):
        return
    num_virtual_targets = module.params.get("num_virtual_targets")
    if num_virtual_targets is None:
        return
    module.params["target_params"] = [{"num_virtual_targets": num_virtual_targets}]


def create_external_attachment(module, result, api_instance):
    """
    Attach an iSCSI client to the referenced Volume Group.

    Validates required create-only inputs, generates the SDK ``IscsiClient``
    spec, and calls ``VolumeGroupApi.attach_iscsi_client``. On success (and
    when ``wait`` is truthy) it waits for the ergon task to complete and
    extracts the attachment's ``ext_id`` from the task's ``entities_affected``.
    """
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    validate_required_params(module, ["volume_group_ext_id"])
    if not module.params.get("iscsi_initiator_name") and not module.params.get(
        "iscsi_initiator_network_id"
    ):
        module.fail_json(
            msg=(
                "Either 'iscsi_initiator_name' or 'iscsi_initiator_network_id' "
                "must be specified when creating an iSCSI external attachment."
            ),
            **result,
        )

    _apply_num_virtual_targets_alias(module)

    sg = SpecGenerator(module)
    default_spec = storage_sdk.IscsiClient()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating attach iSCSI client to Volume Group spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    volume_group = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(volume_group)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.attach_iscsi_client(
            extId=volume_group_ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while attaching iSCSI client to Volume Group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.EXTERNAL_ATTACHMENT
        )
        if ext_id is None:
            ext_id = get_entity_ext_id_from_task(
                task_status, rel=TASK_CONSTANTS.RelEntityType.ISCSI_CLIENT
            )
        if ext_id:
            result["ext_id"] = ext_id
            existing = get_external_attachment_by_ext_id(
                module, api_instance, volume_group_ext_id, ext_id
            )
            if existing is not None:
                result["response"] = strip_internal_attributes(existing.to_dict())
    result["changed"] = True


def update_external_attachment(module, result, api_instance):
    """
    Verify an existing iSCSI external attachment on the Volume Group.

    The storage v4 API does not expose an update operation for external
    attachments (initiator identity, virtual targets, CHAP secret, and
    attachment site are all immutable). This path is therefore idempotent:
    it fetches the current attachment by ``ext_id`` and, if present,
    reports the module as skipped/unchanged. When the referenced
    attachment does not exist, the module fails with a descriptive error.
    """
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    existing = get_external_attachment_by_ext_id(
        module, api_instance, volume_group_ext_id, ext_id
    )

    if existing is None:
        module.fail_json(
            msg=(
                "External attachment with ext_id '{0}' does not exist on Volume Group "
                "'{1}'. Cannot update.".format(ext_id, volume_group_ext_id)
            ),
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["msg"] = (
            "External attachment with ext_id '{0}' already exists on Volume Group "
            "'{1}'. No update is supported by the API.".format(
                ext_id, volume_group_ext_id
            )
        )
        return

    result["response"] = strip_internal_attributes(existing.to_dict())
    result["skipped"] = True
    result["changed"] = False
    module.exit_json(
        msg=(
            "External attachment with ext_id '{0}' already exists on Volume Group "
            "'{1}'. Nothing to change (iSCSI external attachment fields are immutable).".format(
                ext_id, volume_group_ext_id
            )
        ),
        **result,
    )


def delete_external_attachment(module, result, api_instance):
    """
    Detach an existing iSCSI external attachment from the Volume Group.

    Uses the ``detach_iscsi_client_internal`` variant of the SDK, which
    targets the attachment by ``(volumeGroupExtId, extId)`` and matches the
    ``ntnx_external_attachment_v2`` module's contract of taking an
    attachment ``ext_id`` rather than a full ``IscsiClient`` body.
    """
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    validate_required_params(module, ["ext_id", "volume_group_ext_id"])

    if module.check_mode:
        result["msg"] = (
            "External attachment with ext_id:{0} on Volume Group ext_id:{1} "
            "will be detached.".format(ext_id, volume_group_ext_id)
        )
        return

    volume_group = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(volume_group)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.detach_iscsi_client_internal(
            volumeGroupExtId=volume_group_ext_id, extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while detaching iSCSI client from Volume Group",
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
        mutually_exclusive=[
            ("iscsi_initiator_name", "iscsi_initiator_network_id"),
        ],
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "volume_group_ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_external_attachment(module, result, api_instance)
        else:
            create_external_attachment(module, result, api_instance)
    else:
        delete_external_attachment(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
