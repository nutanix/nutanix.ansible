#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_sync_policy_v2
short_description: Synchronize an entity sync policy in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module triggers a manual synchronization for an existing entity sync policy in Nutanix Prism Central.
  - Entity Sync Policies replicate infrastructure entities (e.g. Security Policies, Storage Policies,
    Categories, Subnets, Protection Policies, Recovery Plans) from a local domain manager to a remote
    domain manager to keep multisite / DR configurations consistent.
  - Only an action operation (sync-entity) is exposed by the API; there is no create / update /
    delete API for this entity because sync policies are managed implicitly by the system when the
    underlying entity is protected. Use the info module M(nutanix.ncp.ntnx_entity_sync_policies_info_v2)
    to discover an existing sync policy and its C(ext_id), then use this module to trigger a re-sync.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Sync an Entity Sync Policy) -
    Required Roles: Disaster Recovery Admin, Flow Admin, Prism Admin, Project Manager, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported because the API only exposes a sync action.
      - When C(state=present), the module will trigger a synchronization of the entity to the remote domain manager.
    type: str
    choices:
      - present
    default: present
    required: false
  ext_id:
    description:
      - The external identifier of the entity sync policy to synchronize.
      - This is required for the sync action.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Trigger sync for an entity sync policy
  nutanix.ncp.ntnx_entity_sync_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the sync entity operation on an entity sync policy.
    - If C(wait) is true, this holds the completed task details.
    - If C(wait) is false, this holds the accepted task reference.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": null,
      "completed_time": "2026-07-20T13:31:52.187903+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T13:31:50.821001+00:00",
      "entities_affected": [
        {
          "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
          "name": "entity_sync_policy",
          "rel": "datapolicies:config:entity-sync-policy"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T13:31:52.187902+00:00",
      "legacy_error_message": null,
      "operation": "SyncEntitySyncPolicy",
      "operation_description": "Sync entity identified by its identifier to a remote domain manager",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T13:31:50.833212+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the sync task.
  returned: always
  type: str
  sample: "ZXJnb24=:c3f6cc70-fda6-4133-a97c-58802d58186a"

ext_id:
  description:
    - The external ID of the entity sync policy that was synchronized.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
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
  description: Human readable status / error message.
  returned: When there is an error or in check mode
  type: str
  sample: "Api Exception raised while syncing entity sync policy with ext_id: 2e40ff57-20aa-4d2b-b179-298db969c20d"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_entity_sync_policies_api_instance,
    get_etag,
)
from ..module_utils.v4.data_policies.helpers import get_entity_sync_policy  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402, F401
except ImportError:

    # pylint: disable=unused-import
    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401
        mock_sdk as data_policies_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def sync_entity_sync_policy(module, api_instance, result):
    """Trigger a sync-entity action on the given entity sync policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Entity sync policy with ext_id:{0} will be synchronized to the remote"
            " domain manager.".format(ext_id)
        )
        return

    current_spec = get_entity_sync_policy(module, api_instance, ext_id)

    kwargs = {}
    etag = get_etag(data=current_spec)
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.sync_entity_sync_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while syncing entity sync policy with ext_id: {0}".format(
                ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
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
    api_instance = get_entity_sync_policies_api_instance(module)
    sync_entity_sync_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
