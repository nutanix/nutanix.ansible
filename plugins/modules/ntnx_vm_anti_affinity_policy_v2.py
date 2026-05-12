#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_anti_affinity_policy_v2
short_description: Manage VM-VM anti-affinity policy in Nutanix Prism Central
description:
    - This module allows you to create, update, and delete VM-VM anti-affinity policy in Nutanix Prism Central.
    - VM-VM anti-affinity policy ensures that specified VMs are placed on different hosts.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.6.0"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
options:
    ext_id:
        description:
            - The unique identifier of the VM anti-affinity policy.
            - This parameter is required for update and delete operations.
        required: false
        type: str
    name:
        description:
            - The name of the VM anti-affinity policy.
        required: false
        type: str
    description:
        description:
            - The description of the VM anti-affinity policy.
        required: false
        type: str
    categories:
        description:
            - List of category references associated with the VM anti-affinity policy.
            - Each entry specifies a category by its external ID.
            - VMs with the same category will be placed on different hosts.
        required: false
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - The external ID of the category.
                required: true
                type: str
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present) then the operation will be to create the anti-affinity policy.
            - If C(state) is set to C(present) and C(ext_id) is given then it will update the anti-affinity policy.
            - If C(state) is set to C(absent) and C(ext_id) is given then the anti-affinity policy will be deleted.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the CRUD operation to complete.
        type: bool
        required: false
        default: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create VM Anti-Affinity Policy) -
      Operation Name: Create VM Anti-Affinity Policy -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
    - >-
      B(Update VM Anti-Affinity Policy) -
      Operation Name: Update VM Anti-Affinity Policy -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
    - >-
      B(Delete VM Anti-Affinity Policy) -
      Operation Name: Delete VM Anti-Affinity Policy -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Virtual Machine Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
"""

EXAMPLES = r"""
- name: Create a VM anti-affinity policy
  nutanix.ncp.ntnx_vm_anti_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: my_anti_affinity_policy
    description: Policy to separate critical VMs
    categories:
      - ext_id: "2f54419e-596d-4b34-aa8f-1a1e944ee7d7"
      - ext_id: "8811743f-f3ea-463c-539a-8d6a7f69b8f5"
    state: present
    wait: true

- name: Update a VM anti-affinity policy
  nutanix.ncp.ntnx_vm_anti_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    name: updated_anti_affinity_policy
    description: Updated description
    categories:
      - ext_id: "9811743f-f3ea-463c-539a-8d6a7f69b8f5"
    state: present
    wait: true

- name: Delete a VM anti-affinity policy
  nutanix.ncp.ntnx_vm_anti_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "605a0cf9-d04e-3be7-911b-1e6f193f6eb9"
    state: absent
    wait: true
"""


RETURN = r"""
response:
    description:
        - Response for creating, updating, or deleting VM anti-affinity policy.
        - VM anti-affinity policy details if the operation is create or update and C(wait) is true.
        - Task details if the operation is delete or C(wait) is false.
    type: dict
    returned: always
    sample:
        {
            "categories": [
                {
                    "ext_id": "e4bda88f-e5da-5eb1-a031-2c0bb00d923d"
                },
                {
                    "ext_id": "4d552748-e119-540a-b06c-3c6f0d213fa2"
                },
                {
                    "ext_id": "0e7eee83-4313-5066-bd39-3834ac350f81"
                }
            ],
            "create_time": "2026-05-12T07:13:51.724117+00:00",
            "created_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            },
            "description": "ansible_lBrqyhPVeYWw_anti_affinity_test_3_description",
            "ext_id": "c673c650-4afe-419c-59b0-441a645df9e9",
            "links": null,
            "name": "ansible_lBrqyhPVeYWw_anti_affinity_test_3",
            "num_compliant_vms": 0,
            "num_non_compliant_vms": 0,
            "num_pending_vms": 0,
            "tenant_id": null,
            "update_time": "2026-05-12T07:13:52.055646+00:00",
            "updated_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            }
        }
task_ext_id:
    description: The external ID of the task associated with the operation.
    type: str
    returned: when a task is created
    sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
ext_id:
    description: The external ID of the VM anti-affinity policy.
    type: str
    returned: always
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs
skipped:
    description: Indicates whether the operation was skipped due to idempotency.
    type: bool
    returned: when the operation is skipped
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: on error, idempotency, or check mode
    sample: "Api Exception raised while creating VM anti-affinity policy"
failed:
    description: This field typically holds information about if the task have failed
    type: bool
    returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_vm_anti_affinity_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_anti_affinity_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Returns the module argument specification for VM anti-affinity policy.
    """
    category_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        categories=dict(
            type="list",
            required=False,
            elements="dict",
            options=category_spec,
            obj=vmm_sdk.AhvPoliciesCategoryReference,
        ),
    )
    return module_args


def create_policy(module, api_instance, result):
    """Create a new VM anti-affinity policy."""
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmAntiAffinityPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create VM anti-affinity policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_vm_anti_affinity_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VM anti-affinity policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=Tasks.RelEntityType.VM_ANTI_AFFINITY_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_vm_anti_affinity_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    strip_internal_attributes(current_spec)
    strip_internal_attributes(update_spec)
    if current_spec != update_spec:
        return False
    return True


def update_policy(module, api_instance, result):
    """Update an existing VM anti-affinity policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vm_anti_affinity_policy(module, api_instance, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM anti-affinity policy update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating VM anti-affinity policy", **result
        )

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.update_vm_anti_affinity_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM anti-affinity policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)

    updated_policy = get_vm_anti_affinity_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(updated_policy.to_dict())
    result["changed"] = True


def delete_policy(module, api_instance, result):
    """Delete an existing VM anti-affinity policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Policy with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_vm_anti_affinity_policy(module, api_instance, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting VM anti-affinity policy", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_vm_anti_affinity_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VM anti-affinity policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
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
    }

    api_instance = get_vm_anti_affinity_policies_api_instance(module)

    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_policy(module, api_instance, result)
        else:
            create_policy(module, api_instance, result)
    else:
        delete_policy(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
