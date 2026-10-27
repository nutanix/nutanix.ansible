#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_to_host_migration_v2
short_description: Migrate a VM to another host within the same cluster
version_added: "2.7.0"
description:
    - Migrate a VM to another host within the same cluster.
    - This module uses PC v4 APIs based SDKs
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Host to host VM migration) -
      Required Roles: Account Owner, Administrator, Consumer, Developer, Operator, Prism Admin, Project Admin,
      Project Manager, Self-Service Admin (deprecated), Super Admin, User, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present), the VM is migrated to the specified destination host.
            - No other choices are supported for this module.
        choices:
            - present
        type: str
        default: present
    ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    host:
        description:
            - The destination host to which the VM is migrated.
        type: dict
        required: true
        suboptions:
            ext_id:
                description:
                    - The globally unique identifier of a host type UUID.
                type: str
                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Migrate a VM to a destination host
  nutanix.ncp.ntnx_vm_to_host_migration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    host:
      ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
"""

RETURN = r"""
response:
    description:
        - Task details for the VM to host migration.
        - When C(wait) is true, the final task payload after completion; otherwise the initial task acknowledgement.
    type: dict
    returned: always
    sample:
        {
            "app_name": null,
            "batch_summary": null,
            "cluster_ext_ids": [
                "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-21T05:31:44.875612+00:00",
            "completion_details": null,
            "created_time": "2026-07-21T05:31:44.382175+00:00",
            "entities_affected": [
                {
                    "ext_id": "16023bcc-c1e2-4131-76eb-6bad6e0ddb66",
                    "name": "ansible-example-vm-to-host",
                    "rel": "vmm:ahv:config:vm"
                },
                {
                    "ext_id": "adf0c9e0-4051-4cd2-9f6f-ca9f962e941b",
                    "name": "goku-4",
                    "rel": "clustermgmt:config:host"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:f1e19e35-8c51-53f5-a699-70dd11f8724d",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-21T05:31:44.875611+00:00",
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
            "started_time": "2026-07-21T05:31:44.389846+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:f1e19e35-8c51-53f5-a699-70dd11f8724d"
ext_id:
    description: The external ID of the VM.
    type: str
    returned: always
    sample: "16023bcc-c1e2-4131-76eb-6bad6e0ddb66"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: when an error occurs
    sample: "Failed to get etag for VM"
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Api Exception raised while migrating VM to host"
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    host_reference = dict(
        ext_id=dict(type="str", required=True),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        host=dict(
            type="dict",
            required=True,
            options=host_reference,
            obj=vmm_sdk.AhvConfigHostReference,
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
        "response": None,
        "failed": False,
        "ext_id": None,
    }

    api_instance = get_vm_api_instance(module)
    migrate_vm_to_host(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
