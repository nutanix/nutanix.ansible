#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_pc_backup_target_v2
short_description: Create, Update and Delete a PC backup target.
version_added: 2.1.0
description:
    - Create, Update and Delete a cluster or object store as the backup target.
    - For a given Prism Central, there can be up to 3 clusters as backup targets and 1 object store as backup target.
options:
    state:
        description:
            - State of the backup target whether to create, update or delete.
            - If C(state) is present, it will create or update the backup target.
            - If C(state) is set to C(present) and ext_id is not provided then it will create a new backup target.
            - If C(state) is set to C(present) and ext_id is provided then it will update the backup target.
            - If C(state) is absent, it will delete the backup target.
        choices: ['present', 'absent']
        type: str
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false
    domain_manager_ext_id:
        description: 
            - Domain manager means the PC.
            - A external identifier for the domain manager (PC).
        type: str
        required: true
    ext_id:
        description: A unique identifier for the backup target.
        type: str
        required: false
    location:
        description:
            - Location of the backup target.
            - For example, a cluster or an object store endpoint.
        type: dict
        required: false
        suboptions:
            cluster_location:
                description: Location of the cluster.
                type: dict
                suboptions:
                    config:
                        description: Configuration of the Cluster reference of the remote cluster to be connected.
                        type: dict
                        required: true
                        suboptions:
                            ext_id:
                                description: External ID of the remote cluster.
                                type: str
                                required: true
            object_store_location:
                description: Location of the object store.
                type: dict
                suboptions:
                    provider_config:
                        description: The base model of S3 object store endpoint where domain manager needs to be backed up.
                        type: dict
                        required: true
                        suboptions:
                            bucket_name:
                                description: The bucket name of the object store endpoint where backup data of domain manager is to be stored.
                                type: str
                                required: true
                            region:
                                description: The region name of the object store endpoint where backup data of domain manager is stored.
                                type: str
                                default: us-east-1
                            credentials:
                                description: Secret credentials model for the object store containing access key ID and secret access key.
                                type: dict
                                required: false
                                suboptions:
                                    access_key_id:
                                        description: Access key Id for the object store provided for backup target.
                                        type: str
                                        required: true
                                    secret_access_key:
                                        description: Secret access key for the object store provided for backup target.
                                        type: str
                                        required: true
                    backup_policy:
                        description: Backup policy for the object store provided.
                        type: dict
                        suboptions:
                            rpo_in_minutes:
                                description: RPO interval in minutes at which the backup will be taken
                                type: int
                                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create backup target cluster
  nutanix.ncp.ntnx_pc_backup_target_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    domain_manager_ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
    location:
      cluster_location:
        config:
          ext_id: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"
  register: result

- name: Update backup target object store
  nutanix.ncp.ntnx_pc_backup_target_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"
    domain_manager_ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
    location:
      object_store_location:
        provider_config:
          bucket_name: "mybucket"
          region: "us-east-1"
          credentials:
            access_key_id: "access_key_id"
            secret_access_key: "secret_access_key"
        backup_policy:
          rpo_in_minutes: 120
  register: result

- name: Delete backup target cluster
  nutanix.ncp.ntnx_pc_backup_target_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"
    domain_manager_ext_id: "18553f0f-8547-4115-9696-2f698fbe7117"
    state: absent
  register: result
"""

RETURN = r"""
response:
    description: Task status for the backup target operation.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": [
                "00062c47-ac15-ee40-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2025-01-29T07:35:54.109510+00:00",
            "completion_details": null,
            "created_time": "2025-01-29T07:35:49.556281+00:00",
            "entities_affected": [
                {
                    "ext_id": "18553f0f-7b41-4115-bf42-2f698fbe7117",
                    "name": "prism_central",
                    "rel": "prism:config:domain_manager"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:5f63a855-6b6e-4aca-4efb-159a35ce0e52",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2025-01-29T07:35:54.109509+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "kCreateBackupTarget",
            "operation_description": "Create Backup Target",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2025-01-29T07:35:49.569607+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description: Task ID for the backup target operation.
    type: str
    returned: always
    sample: "ZXJnb24=:5f63a855-6b6e-4aca-4efb-159a35ce0e52"

ext_id:
    description: External ID of the backup target.
    type: str
    returned: always
    sample: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.helpers import get_backup_target  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
    get_etag,
)
from ..module_utils.v4.prism.spec.pc import PrismSpecs as prism_specs  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        domain_manager_ext_id=dict(type="str", required=True),
    )
    module_args.update(prism_specs.get_location_backup_spec())
    return module_args


def create_backup_target(module, domain_manager_backups_api, result):
    """
    This method will create backup target.
    Args:
        module (object): Ansible module object
        domain_manager_backups_api (object): DomainManagerBackupApi instance
        result (dict): Result object
    """
    sg = SpecGenerator(module)
    default_spec = prism_sdk.BackupTarget()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating backup target create Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    try:
        resp = domain_manager_backups_api.create_backup_target(
            domainManagerExtId=domain_manager_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to create backup target",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_backup_target(module, domain_manager_backups_api, result):
    """
    This method will update backup target.
    Args:
        module (object): Ansible module object
        domain_manager_backups_api (object): DomainManagerBackupApi instance
        result (dict): Result object
    """
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")

    sg = SpecGenerator(module)
    default_spec = prism_sdk.BackupTarget()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update backup target spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_backup_target(module, domain_manager_backups_api, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for Updating Backing Target", **result
        )
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating backup target update Spec", **result)

    skip_idempotency = False
    if module.params.get("location", {}).get("cluster_location") or module.params.get(
        "location", {}
    ).get("object_store_location", {}).get("provider_config", {}).get("credentials"):
        skip_idempotency = True

    if not skip_idempotency:
        if check_idempotency(current_spec, update_spec):
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = domain_manager_backups_api.update_backup_target_by_id(
            domainManagerExtId=domain_manager_ext_id,
            extId=ext_id,
            body=update_spec,
            if_match=etag_value,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to update backup target",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_backup_target(module, domain_manager_backups_api, result):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    result["ext_id"] = ext_id
    current_spec = get_backup_target(module, domain_manager_backups_api, ext_id)

    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for deleting Backing Target", **result
        )

    resp = None
    try:
        resp = domain_manager_backups_api.delete_backup_target_by_id(
            domainManagerExtId=domain_manager_ext_id, extId=ext_id, if_match=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting backup target",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["location"]),
            ("state", "absent", ["ext_id"]),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    state = module.params.get("state")
    domain_manager_backups_api = get_domain_manager_backup_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_backup_target(module, domain_manager_backups_api, result)
        else:
            create_backup_target(module, domain_manager_backups_api, result)
    else:
        delete_backup_target(module, domain_manager_backups_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
