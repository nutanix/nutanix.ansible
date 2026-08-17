#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_notification_policy_v2
short_description: Create, Update, Delete notification policies on a Nutanix Files server
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete notification policies for a file server in Nutanix Prism Central.
  - A notification policy defines the file operations, protocols and mount targets for which notifications are sent to a partner server.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create notification policy.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update notification policy.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete notification policy.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the notification policy.
      - Required for update and delete operations.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the notification policy.
      - Required for all operations.
    type: str
    required: true
  name:
    description:
      - Notification policy name.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - A description of the notification policy.
    type: str
    required: false
  has_secured_connection:
    description:
      - Setting this flag ensures that a secure connection is established between AFS and the partner server.
    type: bool
    required: false
  protocol_types:
    description:
      - List of mount target protocol types associated with the notification policy.
      - Required for create operation.
    type: list
    elements: str
    required: false
    choices:
      - NFS
      - NONE
      - SMB
      - SMB_NFS
  should_include_all_mount_targets:
    description:
      - Setting this flag ensures that a notification policy is applicable to all the mount targets.
    type: bool
    required: false
  file_blocking_mode:
    description:
      - The file blocking mode for the notification policy.
    type: str
    required: false
    choices:
      - ALLOW_LIST
      - BLOCK_LIST
  operations:
    description:
      - Defines the list of operations on the files for which notifications are generated.
      - Required for create operation.
    type: list
    elements: str
    required: false
    choices:
      - DIRECTORY_CREATE
      - DIRECTORY_DELETE
      - FILE_CLOSE
      - FILE_CREATE
      - FILE_DELETE
      - FILE_OPEN
      - FILE_READ
      - FILE_WRITE
      - INLINE_READ
      - LINK_CREATE
      - RECALL
      - RENAME
      - SECURITY
      - SETATTR
      - SYMLINK_CREATE
      - TIER
  file_extensions:
    description:
      - List of file blocking extensions. For example C(*.mp3).
    type: list
    elements: str
    required: false
  mount_target_ext_ids:
    description:
      - A list of mount target external identifiers to which the notification policy applies.
    type: list
    elements: str
    required: false
  partner_server_ext_ids:
    description:
      - A list of partner server external identifiers.
    type: list
    elements: str
    required: false
  blocked_clients:
    description:
      - A list of users and client IPs whose notifications need to be blocked for a partner server.
    type: list
    elements: dict
    required: false
    suboptions:
      client_details:
        description:
          - Details of the client that is blocked from notifications.
        type: dict
        required: false
        suboptions:
          address:
            description:
              - The IP address or FQDN of the client.
            type: dict
            required: false
            suboptions:
              ipv4:
                description:
                  - The IPv4 address of the client.
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
                      - The prefix length of the network to which the IPv4 address belongs.
                    type: int
                    required: false
                    default: 32
              ipv6:
                description:
                  - The IPv6 address of the client.
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
                      - The prefix length of the network to which the IPv6 address belongs.
                    type: int
                    required: false
                    default: 128
              fqdn:
                description:
                  - The fully qualified domain name of the client.
                type: dict
                required: false
                suboptions:
                  value:
                    description:
                      - The fully qualified domain name value.
                    type: str
                    required: false
          port:
            description:
              - The port of the blocked client.
            type: int
            required: false
          is_backup:
            description:
              - Indicates whether the client is a backup client.
            type: bool
            required: false
            default: false
      user:
        description:
          - The user definition for a notification policy. The user can be either SID, UID or username.
        type: dict
        required: false
        suboptions:
          name:
            description:
              - Notification policy user name.
            type: str
            required: false
          sid:
            description:
              - The security identifier (SID) of the user.
            type: str
            required: false
          uid:
            description:
              - The unique identifier (UID) of the user.
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
- name: Create notification policy
  nutanix.ncp.ntnx_files_notification_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    name: "notification_policy_ansible"
    description: "Notification policy created by Ansible"
    protocol_types:
      - SMB
    operations:
      - FILE_CREATE
      - FILE_DELETE
    should_include_all_mount_targets: true
    has_secured_connection: false
    partner_server_ext_ids:
      - "3c9a1f3b-3ddb-4585-9159-26d2318269e3"
  register: result
  ignore_errors: true

- name: Update notification policy
  nutanix.ncp.ntnx_files_notification_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b"
    name: "notification_policy_ansible_updated"
    description: "Notification policy updated by Ansible"
    protocol_types:
      - SMB_NFS
    operations:
      - FILE_CREATE
      - FILE_DELETE
      - FILE_READ
    should_include_all_mount_targets: false
    file_blocking_mode: "BLOCK_LIST"
    file_extensions:
      - "*.mp3"
    partner_server_ext_ids:
      - "3c9a1f3b-3ddb-4585-9159-26d2318269e3"
  register: result
  ignore_errors: true

- name: Delete notification policy
  nutanix.ncp.ntnx_files_notification_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    file_server_ext_id: "18f78959-14a6-4c47-b5db-920460c4b668"
    ext_id: "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting notification policy
    - If the operation is create or update and C(wait) is true, it will return the notification policy details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "blocked_clients": null,
      "description": "Notification policy created by Ansible",
      "ext_id": "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b",
      "file_blocking_mode": null,
      "file_extensions": null,
      "has_secured_connection": false,
      "links": null,
      "mount_target_ext_ids": null,
      "name": "notification_policy_ansible",
      "operations": [
          "FILE_CREATE",
          "FILE_DELETE"
      ],
      "partner_server_ext_ids": [
          "3c9a1f3b-3ddb-4585-9159-26d2318269e3"
      ],
      "protocol_types": [
          "SMB"
      ],
      "should_include_all_mount_targets": true,
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
    - The external ID of the notification policy.
  returned: always
  type: str
  sample: "d1f6a9c0-3f1e-4b2a-8f0a-1c2d3e4f5a6b"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
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
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_notification_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_notification_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Read-only attributes populated by the platform that must not be sent in an update body.
READ_ONLY_FIELDS = ["ext_id", "links", "tenant_id"]


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=False),
    )

    address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=files_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=files_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=files_sdk.FQDN,
        ),
    )

    client_details_spec = dict(
        address=dict(
            type="dict",
            options=address_spec,
            required=False,
            obj=files_sdk.IPAddressOrFQDN,
        ),
        port=dict(type="int", required=False),
        is_backup=dict(type="bool", required=False, default=False),
    )

    user_spec = dict(
        name=dict(type="str", required=False),
        sid=dict(type="str", required=False),
        uid=dict(type="int", required=False),
    )

    blocked_client_spec = dict(
        client_details=dict(
            type="dict",
            options=client_details_spec,
            required=False,
            obj=files_sdk.ClientDetails,
        ),
        user=dict(
            type="dict",
            options=user_spec,
            required=False,
            obj=files_sdk.NotificationPolicyUser,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        name=dict(type="str"),
        description=dict(type="str"),
        has_secured_connection=dict(type="bool"),
        protocol_types=dict(
            type="list",
            elements="str",
            choices=["NFS", "NONE", "SMB", "SMB_NFS"],
        ),
        should_include_all_mount_targets=dict(type="bool"),
        file_blocking_mode=dict(
            type="str",
            choices=["ALLOW_LIST", "BLOCK_LIST"],
        ),
        operations=dict(
            type="list",
            elements="str",
            choices=[
                "DIRECTORY_CREATE",
                "DIRECTORY_DELETE",
                "FILE_CLOSE",
                "FILE_CREATE",
                "FILE_DELETE",
                "FILE_OPEN",
                "FILE_READ",
                "FILE_WRITE",
                "INLINE_READ",
                "LINK_CREATE",
                "RECALL",
                "RENAME",
                "SECURITY",
                "SETATTR",
                "SYMLINK_CREATE",
                "TIER",
            ],
        ),
        file_extensions=dict(type="list", elements="str"),
        mount_target_ext_ids=dict(type="list", elements="str"),
        partner_server_ext_ids=dict(type="list", elements="str"),
        blocked_clients=dict(
            type="list",
            elements="dict",
            options=blocked_client_spec,
            obj=files_sdk.BlockedNotificationClient,
        ),
    )
    return module_args


def create_notification_policy(module, result, api_instance):
    file_server_ext_id = module.params.get("file_server_ext_id")
    validate_required_params(module, ["name", "protocol_types", "operations"])
    sg = SpecGenerator(module)
    default_spec = files_sdk.NotificationPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create notification policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_notification_policy(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating notification policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.NOTIFICATION_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_notification_policy(
                module, api_instance, ext_id, file_server_ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Notification Policy"
                ),
                msg="Failed to get entity ext_id from task for Notification Policy",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    return old_spec_dict == update_spec_dict


def update_notification_policy(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    old_spec = get_notification_policy(module, api_instance, ext_id, file_server_ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating notification policy", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update notification policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_notification_policy_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating notification policy",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_notification_policy(module, api_instance, ext_id, file_server_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_notification_policy(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Notification policy with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_notification_policy_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting notification policy",
        )
    task_ext_id = getattr(getattr(resp, "data", None), "ext_id", None)
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
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_notification_policies_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_notification_policy(module, result, api_instance)
        else:
            create_notification_policy(module, result, api_instance)
    else:
        delete_notification_policy(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
