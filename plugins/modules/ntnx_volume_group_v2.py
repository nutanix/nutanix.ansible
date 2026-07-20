#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_v2
short_description: Create, Update, Delete Volume Groups in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Volume Groups in Nutanix Prism Central.
  - A Volume Group is a collection of one or more Volume Disks that can be attached to iSCSI or NVMe-TCP clients, or to AHV VMs.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a Volume Group) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin, Super Admin,
    Self-Service Admin (deprecated)
  - >-
    B(Delete a Volume Group) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Project Manager, Storage Admin, Super Admin,
    Self-Service Admin (deprecated)
  - >-
    B(Update a Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create a Volume Group.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update the Volume Group.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete the Volume Group.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the Volume Group.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the Volume Group.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the Volume Group.
    type: str
    required: false
  should_load_balance_vm_attachments:
    description:
      - Indicates whether to enable Volume Group load balancing for VM attachments.
    type: bool
    required: false
  sharing_status:
    description:
      - Indicates whether the Volume Group can be shared across multiple iSCSI initiators.
      - The mode cannot be changed from SHARED to NOT_SHARED on a Volume Group with multiple attachments.
      - A Volume Group cannot be associated with more than one attachment as long as it is in exclusive mode.
    type: str
    required: false
    choices:
      - SHARED
      - NOT_SHARED
  target_prefix:
    description:
      - The specifications contain the target prefix for external clients as the value.
      - Mutually exclusive with C(target_name).
    type: str
    required: false
  target_name:
    description:
      - Name of the external client target that will be visible and accessible to the client.
      - Mutually exclusive with C(target_prefix).
    type: str
    required: false
  enabled_authentications:
    description:
      - The authentication type enabled for the Volume Group.
      - If omitted, authentication is not configured for the Volume Group.
      - If this is set to CHAP, the target/client secret must be provided.
    type: str
    required: false
    choices:
      - CHAP
      - NONE
  cluster_reference:
    description:
      - Cluster reference (external identifier of the cluster) for the Volume Group.
      - Required for create operation.
    type: str
    required: false
  usage_type:
    description:
      - Expected usage type for the Volume Group.
      - This is an indicative hint on how the caller will consume the Volume Group.
    type: str
    required: false
    choices:
      - BACKUP_TARGET
      - INTERNAL
      - TEMPORARY
      - USER
  is_hidden:
    description:
      - Indicates whether the Volume Group is hidden.
    type: bool
    required: false
  storage_features:
    description:
      - Storage optimization features which must be enabled on the Volume Group.
    type: dict
    required: false
    suboptions:
      flash_mode:
        description:
          - Enable flash mode on the Volume Group.
        type: dict
        required: true
        suboptions:
          is_enabled:
            description:
              - Indicates whether flash mode is enabled on the Volume Group.
            type: bool
            required: true
  iscsi_features:
    description:
      - iSCSI specific settings for the Volume Group.
    type: dict
    required: false
    suboptions:
      target_secret:
        description:
          - Target secret in case of a CHAP authentication.
          - This is a sensitive value and is never logged.
        type: str
        required: true
      enabled_authentications:
        description:
          - The authentication type enabled for the Volume Group.
          - If omitted, authentication is not configured for the Volume Group.
          - If this is set to CHAP, the target/client secret must be provided.
        type: str
        required: false
        choices:
          - CHAP
          - NONE
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
- name: Create Volume Group with minimum required fields
  nutanix.ncp.ntnx_volume_group_v2:
    state: present
    name: "volume_group_ansible"
    description: "Volume Group created by Ansible"
    cluster_reference: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
  register: result
  ignore_errors: true

- name: Create Volume Group with all attributes and CHAP auth
  nutanix.ncp.ntnx_volume_group_v2:
    state: present
    name: "volume_group_ansible_full"
    description: "Volume Group with all attributes"
    cluster_reference: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    should_load_balance_vm_attachments: true
    sharing_status: "SHARED"
    target_prefix: "vg_prefix"
    usage_type: "USER"
    is_hidden: false
    storage_features:
      flash_mode:
        is_enabled: true
    iscsi_features:
      target_secret: "Secret1234567"
      enabled_authentications: "CHAP"
  register: result
  ignore_errors: true

- name: Update Volume Group
  nutanix.ncp.ntnx_volume_group_v2:
    state: present
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b67"
    name: "volume_group_ansible_updated"
    description: "Volume Group updated by Ansible"
    should_load_balance_vm_attachments: false
    sharing_status: "NOT_SHARED"
    is_hidden: true
  register: result
  ignore_errors: true

- name: Delete Volume Group
  nutanix.ncp.ntnx_volume_group_v2:
    state: absent
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b67"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting the Volume Group.
    - If the operation is create or update and C(wait) is true, it will return the Volume Group details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "attachment_type": null,
      "attachments": null,
      "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
      "created_by": null,
      "description": "Volume Group created by Ansible",
      "disks": null,
      "enabled_authentications": null,
      "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
      "hydration_status": null,
      "is_hidden": false,
      "iscsi_features": {
        "enabled_authentications": "CHAP",
        "target_secret": null
      },
      "links": null,
      "name": "volume_group_ansible_full",
      "protocol": null,
      "sharing_status": "SHARED",
      "should_load_balance_vm_attachments": true,
      "storage_features": {
        "flash_mode": {
          "is_enabled": true
        }
      },
      "target_name": "vg_prefix-792cd764-37b5-4da3-7ef1-ea3f618c1648",
      "target_prefix": null,
      "tenant_id": null,
      "usage_type": "USER"
    }

task_ext_id:
  description:
    - The external identifier of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external identifier of the Volume Group.
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
    - This indicates whether the task was skipped due to idempotency.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
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
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

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
    validate_required_params,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_etag,
    get_vg_api_instance,
)
from ..module_utils.v4.volumes.helpers import get_volume_group  # noqa: E402
from ..module_utils.v4.volumes.spec.volume_group import (  # noqa: E402
    VGSpecs as vg_specs,
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
    module_args = vg_specs.get_volume_group_spec()
    return module_args


def create_volume_group(module, api_instance, result):
    validate_required_params(module, ["name", "cluster_reference"])

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.VolumeGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Volume Group spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_volume_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Volume Group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VOLUME_GROUP
        )
        if ext_id:
            result["ext_id"] = ext_id
            entity = get_volume_group(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(entity.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Volume Group"
                ),
                msg="Failed to get entity ext_id from task for Volume Group",
            )
    result["changed"] = True


def check_for_idempotency(current_spec, update_spec):
    return current_spec == update_spec


def update_volume_group(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating Volume Group", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update Volume Group spec", **result)

    # Build request body only from user-specified fields (default_spec + user attrs).
    # This avoids echoing back read-only/auto-generated fields (cluster_reference,
    # auto-generated target_name, hydration_status, etc.) which the API rejects.
    default_spec = volumes_sdk.VolumeGroup()
    request_body, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update Volume Group spec", **result)

    if check_for_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_volume_group_by_id(
            extId=ext_id, body=request_body, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Volume Group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        entity = get_volume_group(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(entity.to_dict())
    result["changed"] = True


def delete_volume_group(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Volume Group with ext_id:{0} will be deleted.".format(ext_id)
        return

    current = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(data=current)
    kwargs = {"if_match": etag} if etag else {}
    resp = None
    try:
        resp = api_instance.delete_volume_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Volume Group",
        )
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
        mutually_exclusive=[
            ("target_name", "target_prefix"),
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
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_volume_group(module, api_instance, result)
        else:
            create_volume_group(module, api_instance, result)
    else:
        delete_volume_group(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
