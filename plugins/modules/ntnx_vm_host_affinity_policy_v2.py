#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vm_host_affinity_policy_v2
short_description: Manage VM-host affinity policy in Nutanix Prism Central
description:
    - This module allows you to create, update, and delete VM-host affinity policy in Nutanix Prism Central.
    - VM-host affinity policy enforces that VMs matching certain categories run on hosts matching certain categories.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.6.0"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
options:
    ext_id:
        description:
            - The unique identifier of the VM host affinity policy.
            - This parameter is required for update and delete operations.
        required: false
        type: str
    name:
        description:
            - The name of the VM host affinity policy.
        required: false
        type: str
    description:
        description:
            - The description of the VM host affinity policy.
        required: false
        type: str
    vm_categories:
        description:
            - List of category references for VMs that this policy applies to.
            - Each entry specifies a category by its external ID.
            - VMs with these categories will be hosted on hosts that match C(host_categories).
        required: false
        type: list
        elements: dict
        suboptions:
            ext_id:
                description:
                    - The external ID of the category.
                required: true
                type: str
    host_categories:
        description:
            - List of category references for hosts that VMs should have affinity with.
            - Each entry specifies a category by its external ID.
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
            - If C(state) is set to C(present) then the operation will be to create the host affinity policy.
            - If C(state) is set to C(present) and C(ext_id) is given then it will update the host affinity policy.
            - If C(state) is set to C(absent) and C(ext_id) is given then the host affinity policy will be deleted.
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
      B(Create VM Host Affinity Policy) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Update VM Host Affinity Policy) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - >-
      B(Delete VM Host Affinity Policy) -
      Required Roles: Prism Admin, Super Admin, Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
"""

EXAMPLES = r"""
- name: Create a VM host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: my_host_affinity_policy
    description: Policy to keep critical VMs on specific hosts
    vm_categories:
      - ext_id: "2f54419e-596d-4b34-aa8f-1a1e944ee7d7"
    host_categories:
      - ext_id: "8811743f-f3ea-463c-539a-8d6a7f69b8f5"
    state: present
    wait: true

- name: Update a VM host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    name: updated_host_affinity_policy
    description: Updated description
    vm_categories:
      - ext_id: "9811743f-f3ea-463c-539a-8d6a7f69b8f5"
    host_categories:
      - ext_id: "1a1e944e-e7d7-2f54-419e-596d4b34aa8f"
    state: present
    wait: true

- name: Delete a VM host affinity policy
  nutanix.ncp.ntnx_vm_host_affinity_policy_v2:
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
        - The response from the VM host affinity policy operation.
        - It will be task response if C(wait) is false.
    type: dict
    returned: always
    sample: {
        "name": "my_host_affinity_policy",
        "description": "Policy to keep critical VMs on specific hosts",
        "vm_categories": [
            {"ext_id": "605a0cf9-d04e-3be7-911b-1e6f193f6ebe"}
        ],
        "host_categories": [
            {"ext_id": "98b9dc89-be08-3c56-b554-692b8b676fd1"}
        ],
        "ext_id": "54fe0ed5-02d8-4588-b10b-3b9736bf3d06",
        "create_time": "2026-01-01T00:00:00.000000+00:00",
        "update_time": "2026-01-01T00:00:00.000000+00:00"
    }
task_ext_id:
    description: The external ID of the task associated with the operation.
    type: str
    returned: when a task is created
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
ext_id:
    description: The external ID of the VM host affinity policy.
    type: str
    returned: always
    sample: "98b9dc89-be08-3c56-b554-692b8b676fd2"
changed:
    description: Indicates whether the resource was changed.
    type: bool
    returned: always
error:
    description: The error message if an error occurred.
    type: str
    returned: when an error occurs
skipped:
    description: Indicates whether the operation was skipped due to idempotency.
    type: bool
    returned: when the operation is skipped
msg:
    description: A message describing the result.
    type: str
    returned: on error, idempotency, or check mode
    sample: "VM host affinity policy created successfully"
failed:
    description: Indicates whether the operation failed.
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
    get_vm_host_affinity_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_host_affinity_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Returns the module argument specification for VM host affinity policy.
    """
    category_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        vm_categories=dict(
            type="list",
            required=False,
            elements="dict",
            options=category_spec,
            obj=vmm_sdk.AhvPoliciesCategoryReference,
        ),
        host_categories=dict(
            type="list",
            required=False,
            elements="dict",
            options=category_spec,
            obj=vmm_sdk.AhvPoliciesCategoryReference,
        ),
    )
    return module_args


def create_policy(module, api_instance, result):
    """Create a new VM host affinity policy."""
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmHostAffinityPolicy()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create VM host affinity policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_vm_host_affinity_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VM host affinity policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=Tasks.RelEntityType.VM_HOST_AFFINITY_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_vm_host_affinity_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    strip_internal_attributes(current_spec)
    strip_internal_attributes(update_spec)
    if current_spec != update_spec:
        return False
    return True


def update_policy(module, api_instance, result):
    """Update an existing VM host affinity policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vm_host_affinity_policy(module, api_instance, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating VM host affinity policy update spec", **result
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
            "Unable to fetch etag for updating VM host affinity policy", **result
        )

    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.update_vm_host_affinity_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM host affinity policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)

    updated_policy = get_vm_host_affinity_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(updated_policy.to_dict())
    result["changed"] = True


def delete_policy(module, api_instance, result):
    """Delete an existing VM host affinity policy."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Policy with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_vm_host_affinity_policy(module, api_instance, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting VM host affinity policy", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_vm_host_affinity_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VM host affinity policy",
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

    api_instance = get_vm_host_affinity_policies_api_instance(module)

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
