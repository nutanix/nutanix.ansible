#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_migrate_v2
short_description: Migrate a Volume Group across sites in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to trigger the migrate action on a Volume Group
    identified by C(ext_id) in Nutanix Prism Central.
  - The migrate action moves the Volume Group ownership to the target
    Availability Zone (and optionally the target Prism Element cluster) as
    part of the Volume Group synchronous replication / cross-cluster live
    migration workflow.
  - The Volume Group must already have a synchronous replication relationship
    established with the target site before it can be migrated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation. The required roles depend on the operation
    being performed.
  - >-
    B(Migrate a Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin,
    Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external identifier of the Volume Group to migrate.
    type: str
    required: true
  target_availability_zone_id:
    description:
      - The external identifier of the target availability zone where the
        Volume Group must be migrated.
      - This field is required for the migrate action.
    type: str
    required: true
  target_cluster_id:
    description:
      - The external identifier of the target Prism Element cluster where the
        Volume Group must be migrated.
      - Optional; when omitted, the target PE cluster is determined by the
        synchronous replication relationship on the target availability zone.
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
- name: Migrate a Volume Group to the target availability zone
  nutanix.ncp.ntnx_volume_group_migrate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "792cd764-37b5-4da3-7ef1-ea3f618c1648"
    target_availability_zone_id: "17838034-1111-2222-3333-e0c44b868efa"
    target_cluster_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the migrate action on the Volume Group.
    - If C(wait) is true, the response contains the completed task details.
    - If C(wait) is false, the response contains the initial task reference
      returned by the migrate API.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-20T15:55:32.123456+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T15:55:12.123456+00:00",
      "entities_affected": [
        {
          "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
          "name": "ansible-vg-migrate",
          "rel": "volumes:config:volume-group"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T15:55:32.123456+00:00",
      "legacy_error_message": null,
      "number_of_subtasks": 0,
      "operation": "MigrateVolumeGroup",
      "operation_description": "Migrate Volume Group",
      "owned_by": null,
      "parent_task": null,
      "progress_percentage": 100,
      "root_task": null,
      "started_time": "2026-07-20T15:55:12.123456+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the migrate task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the Volume Group that was migrated.
  returned: always
  type: str
  sample: "792cd764-37b5-4da3-7ef1-ea3f618c1648"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: When applicable
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
  returned: When there is an error or in check mode.
  type: str
  sample: "Api Exception raised while migrating Volume Group"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_volume_group_api_instance,
)
from ..module_utils.v4.storage.helpers import get_volume_group  # noqa: E402
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
    module_args = dict(
        ext_id=dict(type="str", required=True),
        target_availability_zone_id=dict(type="str", required=True),
        target_cluster_id=dict(type="str", required=False),
    )
    return module_args


def migrate_volume_group(module, api_instance, result):
    """Trigger the migrate action on the target Volume Group."""
    validate_required_params(module, ["ext_id", "target_availability_zone_id"])

    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = storage_sdk.VolumeGroupMigrationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating migrate Volume Group spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Volume Group with ext_id:{0} will be migrated to availability zone:"
            "{1}.".format(ext_id, module.params.get("target_availability_zone_id"))
        )
        return

    vg = get_volume_group(module, api_instance, ext_id)
    etag = get_etag(vg)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.migrate_volume_group(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating Volume Group",
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
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_volume_group_api_instance(module)
    migrate_volume_group(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
