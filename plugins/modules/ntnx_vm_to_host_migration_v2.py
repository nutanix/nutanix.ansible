#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_to_host_migration_v2
short_description: Migrate an AHV VM from one host to another within a cluster
version_added: 2.7.0
description:
    - Migrate an AHV VM (Virtual Machine) live from its current host to a
      target host within the same cluster.
    - The destination host must belong to the same cluster as the VM.
    - This is a stateless action module - each invocation triggers a
      one-shot host to host VM migration task.
    - This module uses PC v4 APIs based SDKs.
options:
    ext_id:
        description:
            - The external ID (UUID) of the AHV VM that has to be migrated.
        type: str
        required: true
    host:
        description:
            - The destination host to which the VM will be migrated.
        type: dict
        required: true
        suboptions:
            ext_id:
                description:
                    - The external ID (UUID) of the destination host.
                    - The destination host MUST belong to the same cluster as
                      the source host on which the VM is currently running.
                type: str
                required: true
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Host to host VM migration) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, Project Admin, Project Manager, Super Admin, User,
      Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
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
- name: Migrate a VM to a target host within the same cluster
  nutanix.ncp.ntnx_vm_to_host_migration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    host:
      ext_id: "3b6e2e77-f4a5-45f9-8fce-c11e04e4dd4b"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for the host to host VM migration operation.
        - Task details when the operation completes.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T23:09:23.817715+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T23:09:23.317879+00:00",
            "entities_affected": [
                {
                    "ext_id": "3bdc57e5-9ecb-4c99-49e1-2294e7c1eeac",
                    "name": "ansible-testZMLgXDFRvm-to-host",
                    "rel": "vmm:ahv:config:vm"
                },
                {
                    "ext_id": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
                    "name": "goku-4",
                    "rel": "clustermgmt:config:host"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:99ffcca6-5c76-52de-8126-6f6f61e07e3c",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T23:09:23.817714+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 2,
            "number_of_subtasks": 0,
            "operation": "VmMigrateToHost",
            "operation_description": "VM migrate to host",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T23:09:23.325814+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while migrating VM to host"

error:
    description: This field typically holds information about the error that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed to get etag for VM"

failed:
    description: This field typically holds information about if the task has failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task associated with the operation.
    returned: always
    type: str
    sample: "ZXJnb24=:99ffcca6-5c76-52de-8126-6f6f61e07e3c"

ext_id:
    description: The external ID of the VM being migrated.
    returned: always
    type: str
    sample: "3bdc57e5-9ecb-4c99-49e1-2294e7c1eeac"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    host_ref_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        host=dict(
            type="dict",
            options=host_ref_spec,
            obj=vmm_sdk.AhvConfigHostReference,
            required=True,
        ),
    )
    return module_args


def migrate_vm_to_host(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmMigrateToHostParams()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for VM to host migration", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    vm = get_vm(module, api_instance, ext_id)
    etag = get_etag(vm)
    if not etag:
        module.fail_json(msg="Failed to get etag for VM", **result)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.migrate_vm_to_host(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating VM to host",
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
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_vm_api_instance(module)
    migrate_vm_to_host(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
