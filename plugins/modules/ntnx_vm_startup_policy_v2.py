#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_startup_policy_v2
short_description: Create, Update, Delete VM startup policies in Nutanix Prism Central
version_added: "2.6.0"
description:
    - This module allows you to create, update, and delete VM startup policies in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a new VM startup policy.
            - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update that policy.
            - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete that policy.
        type: str
        required: false
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external ID of the VM startup policy.
            - Required for update and delete operations.
        type: str
        required: false
    name:
        description:
            - Name of the VM startup policy.
            - Required for create operation.
        type: str
        required: false
    description:
        description:
            - Description of the VM startup policy.
        type: str
        required: false
    groups:
        description:
            - Ordered list of groups configured for the VM startup policy.
            - Each group is represented by one or more categories which VMs are expected to be associated with.
            - The list should be ordered in the sequence in which VMs are to be started in
              an HA event or cluster restart event.
            - Required for create operation.
        type: list
        elements: dict
        required: false
        suboptions:
            categories:
                description:
                    - Categories configured for the group.
                type: list
                elements: dict
                required: true
                suboptions:
                    ext_id:
                        description:
                            - The external ID (UUID) of the category.
                        type: str
                        required: true
    start_conditions:
        description:
            - Ordered list of start conditions for the VM startup policy.
            - Required for create operation.
        type: list
        elements: dict
        required: false
        suboptions:
            power_state_criteria:
                description:
                    - The power state criteria that the VMs in the group must attain before the dependent VMs are started.
                    - Exactly one of C(power_on) or C(guest_bootup) must be supplied
                type: dict
                required: true
                suboptions:
                    power_on:
                        description:
                            - The VM must be powered on before the dependent VMs are started.
                            - This branch has no fields; supply it as an empty mapping (for example C(power_on:) which is YAML null, or an explicit empty dict).
                        type: dict
                        required: false
                    guest_bootup:
                        description:
                            - The VM's Guest OS must be booted up before the dependent VMs are started.
                            - Guest bootup is detected via Nutanix Guest Tools (NGT).
                        type: dict
                        required: false
                        suboptions:
                            timeout_duration_secs:
                                description:
                                    - Timeout in seconds in which the VM's Guest OS bootup must be detected successfully.
                                type: int
                                required: false
            delay_duration_secs:
                description:
                    - Delay in seconds after the power state criteria is met before the dependent VMs are started.
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
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a VM Startup Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Update a VM Startup Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Self Service Admin (deprecated)
    - >-
      B(Delete a VM Startup Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Super Admin, Self Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
"""

EXAMPLES = r"""
- name: Create a VM startup policy with guest bootup criteria
  nutanix.ncp.ntnx_vm_startup_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: my_startup_policy
    description: My VM startup policy
    groups:
      - categories:
          - ext_id: "f8a21952-306f-409a-975e-1021c3827860"
      - categories:
          - ext_id: "6b1f7792-1297-4f4f-85b4-729b50333906"
    start_conditions:
      - power_state_criteria:
          guest_bootup:
            timeout_duration_secs: 300
        delay_duration_secs: 60
  register: result

- name: Create a VM startup policy with power-on criteria
  nutanix.ncp.ntnx_vm_startup_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: power_on_policy
    groups:
      - categories:
          - ext_id: "f8a21952-306f-409a-975e-1021c3827860"
    start_conditions:
      - power_state_criteria:
          power_on: {}
        delay_duration_secs: 30
  register: result

- name: Update a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "605a0cf9-d04e-3be7-911b-1e6f193f6eb9"
    name: my_startup_policy_updated
    description: Updated description
    groups:
      - categories:
          - ext_id: "f8a21952-306f-409a-975e-1021c3827860"
    start_conditions:
      - power_state_criteria:
          power_on: {}
        delay_duration_secs: 30
  register: result

- name: Delete a VM startup policy
  nutanix.ncp.ntnx_vm_startup_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "605a0cf9-d04e-3be7-911b-1e6f193f6eb9"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting VM startup policy
    - If the operation is create or update and C(wait) is true, it will return the VM startup policy details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
        "create_time": "2026-05-25T09:52:40.341137+00:00",
        "created_by": {
            "ext_id": "00000000-0000-0000-0000-000000000000"
        },
        "description": "VM startup policy created by Ansible integration tests with all attributes",
        "ext_id": "58b9a9e4-567a-4cc1-73dc-4926331c8eb1",
        "groups": [
            {
                "categories": [
                    {
                        "ext_id": "4d552748-e119-540a-b06c-3c6f0d213fa2"
                    }
                ]
            },
            {
                "categories": [
                    {
                        "ext_id": "0e7eee83-4313-5066-bd39-3834ac350f81"
                    }
                ]
            }
        ],
        "links": null,
        "name": "policy_ansible_hVQRuZXyBtrn_all",
        "num_compliant_vms": 0,
        "num_dependency_conflicts": 0,
        "num_non_compliant_vms": 0,
        "num_pending_vms": 0,
        "num_start_condition_conflicts": 0,
        "start_conditions": [
            {
                "delay_duration_secs": 60,
                "power_state_criteria": {
                    "timeout_duration_secs": 300
                }
            }
        ],
        "tenant_id": null,
        "update_time": "2026-05-25T09:52:40.340182+00:00",
        "updated_by": {
            "ext_id": "00000000-0000-0000-0000-000000000000"
        }
    }

task_ext_id:
  description:
    - The external id of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external id of the VM startup policy.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_vm_startup_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_startup_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    category_ref_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    dependency_group_spec = dict(
        categories=dict(
            type="list",
            elements="dict",
            options=category_ref_spec,
            required=True,
            obj=vmm_sdk.AhvPoliciesCategoryReference,
        ),
    )

    power_state_criteria_spec = dict(
        power_on=dict(type="dict", options=dict(), required=False),
        guest_bootup=dict(
            type="dict",
            options=dict(timeout_duration_secs=dict(type="int", required=False)),
            required=False,
        ),
    )

    start_condition_spec = dict(
        power_state_criteria=dict(
            type="dict",
            options=power_state_criteria_spec,
            required=True,
            obj={
                "power_on": vmm_sdk.PowerStateCriteriaPowerOn,
                "guest_bootup": vmm_sdk.PowerStateCriteriaGuestBootup,
            },
            mutually_exclusive=[("power_on", "guest_bootup")],
        ),
        delay_duration_secs=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        groups=dict(
            type="list",
            elements="dict",
            options=dependency_group_spec,
            obj=vmm_sdk.DependencyGroup,
        ),
        start_conditions=dict(
            type="list",
            elements="dict",
            options=start_condition_spec,
            obj=vmm_sdk.StartCondition,
        ),
    )
    return module_args


def create_vm_startup_policy(module, api_instance, result):
    validate_required_params(module, ["name", "groups", "start_conditions"])

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.VmStartupPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create VM startup policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_vm_startup_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating VM startup policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.VM_STARTUP_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_vm_startup_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for VM startup policy"
                ),
                msg="Failed to get entity ext_id from task for VM startup policy",
            )

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    strip_internal_attributes(current_spec)
    strip_internal_attributes(update_spec)
    if current_spec == update_spec:
        return True
    return False


def update_vm_startup_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_vm_startup_policy(module, api_instance, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating VM startup policy", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update VM startup policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_vm_startup_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM startup policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        policy = get_vm_startup_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(policy.to_dict())

    result["changed"] = True


def delete_vm_startup_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "VM startup policy with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_vm_startup_policy(module, api_instance, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for deleting VM startup policy", **result
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.delete_vm_startup_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting VM startup policy",
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
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    # Treat `power_on:` (YAML null) as a shorthand for `power_on: {}`.
    # mutually_exclusive on the arg-spec guarantees guest_bootup isn't also set.
    for sc in module.params.get("start_conditions") or []:
        psc = sc.setdefault("power_state_criteria", {})
        if "guest_bootup" not in psc:
            psc["power_on"] = {}

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }

    api_instance = get_vm_startup_policies_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_vm_startup_policy(module, api_instance, result)
        else:
            create_vm_startup_policy(module, api_instance, result)
    else:
        delete_vm_startup_policy(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
