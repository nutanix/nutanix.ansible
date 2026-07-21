#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_external_iscsi_attachments_by_volume_group_id_v2
short_description: Manage external iSCSI attachments (iSCSI clients) of a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to attach and detach external iSCSI clients to/from a Volume Group in Nutanix Prism Central.
  - An external iSCSI attachment represents an iSCSI client (initiator) that is associated with a Volume Group as an external attachment.
  - If C(state) is C(present) and C(ext_id) is not provided, the module attaches a new iSCSI client to the Volume Group.
  - If C(state) is C(present) and C(ext_id) is provided, the module attaches an already existing iSCSI client (by external ID) to the Volume Group.
  - If C(state) is C(absent) and C(ext_id) is provided, the module detaches the iSCSI client from the Volume Group.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Attach an iSCSI client to the given Volume Group) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin, Super Admin,
    Self-Service Admin (deprecated)
  - >-
    B(Detach an iSCSI client from the given Volume Group) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin, Super Admin,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will attach a new iSCSI client to the Volume Group.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will
        attach an already existing iSCSI client (by ext_id) to the Volume Group.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will detach the iSCSI client from the Volume Group.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the iSCSI client (external iSCSI attachment).
      - Required for detach (delete) operation.
      - When provided with C(state=present) the attach is performed by referencing an existing iSCSI client by its external ID.
    type: str
    required: false
  volume_group_ext_id:
    description:
      - The external ID of the Volume Group the iSCSI client is being attached to or detached from.
    type: str
    required: true
  iscsi_initiator_name:
    description:
      - iSCSI initiator name (IQN).
      - Exactly one of C(iscsi_initiator_name) and C(iscsi_initiator_network_id) must be specified during the attach operation.
      - This field is immutable once the attachment is created.
    type: str
    required: false
  iscsi_initiator_network_id:
    description:
      - IPv4 / IPv6 address or FQDN identifying the iSCSI initiator on the network.
      - Mutually exclusive with C(iscsi_initiator_name).
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The value of the IPv4 address.
            type: str
            required: true
      ipv6:
        description:
          - IPv6 address of the initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The value of the IPv6 address.
            type: str
            required: true
      fqdn:
        description:
          - Fully qualified domain name of the initiator.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - The value of the FQDN address.
            type: str
            required: true
  client_secret:
    description:
      - iSCSI initiator client secret used for CHAP authentication.
      - This must only be provided when C(enabled_authentications) is set to C(CHAP).
    type: str
    required: false
  enabled_authentications:
    description:
      - The authentication type enabled for the external iSCSI attachment.
      - When set to C(CHAP) the C(client_secret) must be provided.
    type: str
    required: false
    choices:
      - CHAP
      - NONE
    default: NONE
  num_virtual_targets:
    description:
      - Number of virtual targets generated for the iSCSI target.
      - This field is immutable once the attachment is created.
    type: int
    required: false
  attachment_site:
    description:
      - The site where the Volume Group attach operation should be processed.
      - This field may only be set if Metro DR (Volume Group synchronous replication) has been configured for this Volume Group.
    type: str
    required: false
    choices:
      - SECONDARY
      - PRIMARY
  cluster_reference:
    description:
      - The external identifier of the cluster on which the iSCSI client is registered.
      - Used together with C(ext_id) when attaching an already existing iSCSI client to the Volume Group.
    type: str
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
- name: Attach a new iSCSI client to a Volume Group using IQN
  nutanix.ncp.ntnx_external_iscsi_attachments_by_volume_group_id_v2:
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    iscsi_initiator_name: "iqn.1991-05.com.microsoft:ansible-client"
    num_virtual_targets: 32
    enabled_authentications: CHAP
    client_secret: "Nutanix.1234455"
    attachment_site: "PRIMARY"
  register: attach_by_iqn

- name: Attach a new iSCSI client to a Volume Group using an IPv4 initiator network id
  nutanix.ncp.ntnx_external_iscsi_attachments_by_volume_group_id_v2:
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    iscsi_initiator_network_id:
      ipv4:
        value: "10.44.76.100"
    num_virtual_targets: 32
    enabled_authentications: NONE
  register: attach_by_ipv4

- name: Attach an existing iSCSI client (by ext_id) to a Volume Group
  nutanix.ncp.ntnx_external_iscsi_attachments_by_volume_group_id_v2:
    state: present
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
  register: attach_by_ext_id

- name: Detach an iSCSI client from a Volume Group
  nutanix.ncp.ntnx_external_iscsi_attachments_by_volume_group_id_v2:
    state: absent
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
  register: detach_result
"""

RETURN = r"""
response:
  description:
    - Response for attaching or detaching an external iSCSI client to/from a Volume Group.
    - If the operation is attach and C(wait) is true, it will return the task details after completion (including status).
    - If the operation is attach and C(wait) is false, it will return the task submission details.
    - If the operation is detach, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T05:19:00.229645+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T05:19:00.095273+00:00",
      "entities_affected": [
          {
              "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
              "rel": "volumes:config:iscsi-client"
          },
          {
              "ext_id": "11ac5593-c9cf-403d-641c-3bf76eff2193",
              "rel": "volumes:config:volume-group"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7",
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T05:19:00.229642+00:00",
      "legacy_error_message": null,
      "operation": "VolumeGroupAttachExternal",
      "operation_description": "Volume group attach to iSCSI Client",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-21T05:19:00.122260+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:e7b6ff28-e5f1-4316-82e8-96368cc851d7"

ext_id:
  description:
    - The external ID of the iSCSI client (external iSCSI attachment).
  returned: always
  type: str
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

volume_group_ext_id:
  description:
    - The external ID of the Volume Group the operation acted on.
  returned: always
  type: str
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
  returned: When applicable
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
  returned: When there is an error, module is idempotent or check mode
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
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.volumes.helpers import (  # noqa: E402
    get_external_iscsi_attachment_by_ext_id,
    get_volume_group,
)

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    address_spec = dict(
        value=dict(type="str", required=True),
    )
    iscsi_initiator_network_id_spec = dict(
        ipv4=dict(type="dict", options=address_spec, obj=volumes_sdk.IPv4Address),
        ipv6=dict(type="dict", options=address_spec, obj=volumes_sdk.IPv6Address),
        fqdn=dict(type="dict", options=address_spec, obj=volumes_sdk.FQDN),
    )
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        iscsi_initiator_name=dict(type="str", required=False),
        iscsi_initiator_network_id=dict(
            type="dict",
            options=iscsi_initiator_network_id_spec,
            obj=volumes_sdk.IPAddressOrFQDN,
        ),
        client_secret=dict(type="str", no_log=True, required=False),
        enabled_authentications=dict(
            type="str",
            choices=["CHAP", "NONE"],
            default="NONE",
        ),
        num_virtual_targets=dict(type="int", required=False),
        attachment_site=dict(
            type="str",
            choices=["SECONDARY", "PRIMARY"],
            required=False,
        ),
        cluster_reference=dict(type="str", required=False),
    )
    return module_args


def _external_attachment_exists(module, api_instance, volume_group_ext_id, ext_id):
    """Check whether an external iSCSI attachment with the given ext_id already exists on the VG.

    Returns True if the attachment is present, False otherwise.
    """
    return (
        get_external_iscsi_attachment_by_ext_id(
            module, api_instance, volume_group_ext_id, ext_id
        )
        is not None
    )


def create_ExternalIscsiAttachmentsByVolumeGroupId(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.IscsiClient()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating attach external iSCSI attachment spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.attach_iscsi_client(
            body=spec, extId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while attaching iSCSI client to "
                "Volume Group {0}"
            ).format(volume_group_ext_id),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ISCSI_CLIENT
        )
        if ext_id:
            result["ext_id"] = ext_id
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for external iSCSI attachment"
                ),
                msg=(
                    "Failed to get external iSCSI attachment ext_id from task "
                    "for Volume Group {0}"
                ).format(volume_group_ext_id),
            )
    result["changed"] = True


def update_ExternalIscsiAttachmentsByVolumeGroupId(module, result, api_instance):
    """Attach an already existing iSCSI client (by ext_id) to the Volume Group.

    The Nutanix Volumes v4 API does not expose a dedicated update operation for
    external iSCSI attachments. When C(state=present) is combined with an
    C(ext_id), we treat it as an attach-existing-by-id request. If the client is
    already attached to the Volume Group we short-circuit with an idempotent
    skip. Otherwise, we call the attach API with the minimal reference body.
    """

    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    if _external_attachment_exists(module, api_instance, volume_group_ext_id, ext_id):
        result["skipped"] = True
        result["changed"] = False
        result["msg"] = (
            "External iSCSI attachment with ext_id '{0}' is already attached "
            "to Volume Group '{1}'. Skipping attach.".format(
                ext_id, volume_group_ext_id
            )
        )
        module.exit_json(**result)

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.IscsiClient()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating attach external iSCSI attachment spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vg = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.attach_iscsi_client(
            body=spec, extId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while attaching existing iSCSI client "
                "'{0}' to Volume Group '{1}'"
            ).format(ext_id, volume_group_ext_id),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        task_ext_id_entity = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ISCSI_CLIENT
        )
        if task_ext_id_entity:
            result["ext_id"] = task_ext_id_entity
    result["changed"] = True


def delete_ExternalIscsiAttachmentsByVolumeGroupId(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.IscsiClientAttachment()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating detach external iSCSI attachment spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "External iSCSI attachment with ext_id '{0}' will be detached "
            "from Volume Group '{1}'.".format(ext_id, volume_group_ext_id)
        )
        return

    vg = get_volume_group(module, api_instance, volume_group_ext_id)
    etag = get_etag(vg)
    kwargs = {"if_match": etag} if etag else {}

    resp = None
    try:
        resp = api_instance.detach_iscsi_client(
            body=spec, extId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while detaching iSCSI client '{0}' from "
                "Volume Group '{1}'"
            ).format(ext_id, volume_group_ext_id),
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
        mutually_exclusive=[
            ("iscsi_initiator_name", "iscsi_initiator_network_id"),
        ],
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "volume_group_ext_id": None,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ExternalIscsiAttachmentsByVolumeGroupId(module, result, api_instance)
        else:
            create_ExternalIscsiAttachmentsByVolumeGroupId(module, result, api_instance)
    else:
        delete_ExternalIscsiAttachmentsByVolumeGroupId(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
