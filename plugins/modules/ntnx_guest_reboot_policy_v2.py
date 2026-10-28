#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_guest_reboot_policy_v2
short_description: Create, Update, Delete Guest Reboot Policy
version_added: "2.7.0"
description:
    - Create, Update, Delete Guest Reboot Policy
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present) and C(ext_id) is not given then the Guest Reboot Policy will be created.
            - If C(state) is set to C(present) and C(ext_id) is given then the Guest Reboot Policy will be updated.
            - If C(state) is set to C(absent) and C(ext_id) is given then the Guest Reboot Policy will be deleted.
        type: str
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external ID of the Guest Reboot Policy.
            - Required for updating or deleting the Guest Reboot Policy.
        type: str
        required: false
    name:
        description:
            - Name of the Guest Reboot Policy.
            - Must be between 1 and 80 characters long.
            - Required for creating the Guest Reboot Policy.
        type: str
        required: false
    description:
        description:
            - Guest Reboot Policy description.
        type: str
        required: false
    categories:
        description:
            - Categories of the Guest Reboot Policy.
            - Must contain between 1 and 20 unique categories.
            - Required for creating the Guest Reboot Policy.
        type: list
        elements: dict
        required: false
        suboptions:
            ext_id:
                description:
                    - The external ID (UUID) of the category.
                type: str
                required: true
    reboot_schedule:
        description:
            - Reboot schedule of the Guest Reboot Policy. Either immediate or later.
            - Required for creating the Guest Reboot Policy.
            - Exactly one of C(immediate) or C(later) can be provided.
        type: dict
        required: false
        suboptions:
            immediate:
                description:
                    - Immediately reboot the guest once the reboot-required flag is set.
                    - This schedule has no attributes, provide an empty dictionary C({}) to select it.
                type: dict
                required: false
            later:
                description:
                    - Reboot the guest at the specified time of the day, once the reboot-required flag is set.
                type: dict
                required: false
                suboptions:
                    day_of_week:
                        description:
                            - Day of the week to reboot, in the Guest Reboot Policy.
                        type: str
                        required: true
                        choices:
                            - SUNDAY
                            - MONDAY
                            - TUESDAY
                            - WEDNESDAY
                            - THURSDAY
                            - FRIDAY
                            - SATURDAY
                    time_of_day:
                        description:
                            - Time of the day to reboot, in the Guest Reboot Policy.
                            - Must be in 24-hour C(HH:MM) format.
                        type: str
                        required: true
    project_ext_id:
        description:
            - The external ID (UUID) of the project.
        type: str
        required: false
    wait:
        description:
            - Wait for the CRUD operation to complete.
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
      B(Create Guest Reboot Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Virtual Machine Admin
    - >-
      B(Update Guest Reboot Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Virtual Machine Admin
    - >-
      B(Delete Guest Reboot Policy) -
      Required Roles: Prism Admin, Project Admin, Project Manager, Self-Service Admin (deprecated), Super Admin,
      Virtual Machine Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create a Guest Reboot Policy with immediate reboot schedule
  nutanix.ncp.ntnx_guest_reboot_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: guest-reboot-policy-immediate
    description: Reboot the guest immediately once the reboot-required flag is set
    categories:
      - ext_id: "2530b04f-3203-47e7-ae20-a3d617024688"
    reboot_schedule:
      immediate: {}
    project_ext_id: "d6d98a71-1759-4c8e-8d12-178349a39794"
  register: result

- name: Create a Guest Reboot Policy with later reboot schedule
  nutanix.ncp.ntnx_guest_reboot_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: guest-reboot-policy-later
    categories:
      - ext_id: "2530b04f-3203-47e7-ae20-a3d617024688"
      - ext_id: "8811743f-f3ea-463c-539a-8d6a7f69b8f5"
    reboot_schedule:
      later:
        day_of_week: SUNDAY
        time_of_day: "02:30"
  register: result

- name: Update a Guest Reboot Policy
  nutanix.ncp.ntnx_guest_reboot_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
    name: guest-reboot-policy-updated
    description: Updated description
    reboot_schedule:
      later:
        day_of_week: FRIDAY
        time_of_day: "23:00"
  register: result

- name: Delete a Guest Reboot Policy
  nutanix.ncp.ntnx_guest_reboot_policy_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for Guest Reboot Policy operations.
        - Guest Reboot Policy details if C(wait) is true and the operation is create or update.
        - Task details if C(wait) is false or the operation is delete.
    returned: always
    type: dict
    sample:
        {
            "categories": [
                {
                    "ext_id": "2530b04f-3203-47e7-ae20-a3d617024688"
                }
            ],
            "create_time": "2027-01-12T07:13:51.724117+00:00",
            "created_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            },
            "description": "Reboot the guest at the given time",
            "ext_id": "c673c650-4afe-419c-59b0-441a645df9e9",
            "links": null,
            "name": "guest-reboot-policy-later",
            "project_ext_id": null,
            "reboot_schedule": {
                "day_of_week": "SUNDAY",
                "time_of_day": "02:30"
            },
            "tenant_id": null,
            "update_time": "2027-01-12T07:13:52.055646+00:00",
            "updated_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            }
        }
task_ext_id:
    description:
        - The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
ext_id:
    description:
        - The external ID of the Guest Reboot Policy.
    returned: always
    type: str
    sample: "c673c650-4afe-419c-59b0-441a645df9e9"
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
    returned: When there is an error, module is idempotent or check mode
    type: str
    sample: "Api Exception raised while creating Guest Reboot Policy"
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
    strip_read_only_fields,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_guest_reboot_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_guest_reboot_policy  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Server populated fields that must not be sent back in the update body.
_READ_ONLY_FIELDS = ("create_time", "update_time", "created_by", "updated_by")


def get_module_spec():
    category_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    later_spec = dict(
        day_of_week=dict(
            type="str",
            required=True,
            choices=[
                "SUNDAY",
                "MONDAY",
                "TUESDAY",
                "WEDNESDAY",
                "THURSDAY",
                "FRIDAY",
                "SATURDAY",
            ],
        ),
        time_of_day=dict(type="str", required=True),
    )
    reboot_schedule_spec = dict(
        immediate=dict(type="dict", options=dict(), required=False),
        later=dict(type="dict", options=later_spec, required=False),
    )
    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        categories=dict(
            type="list",
            elements="dict",
            options=category_spec,
            required=False,
            obj=vmm_sdk.AhvPoliciesCategoryReference,
        ),
        reboot_schedule=dict(
            type="dict",
            options=reboot_schedule_spec,
            required=False,
            obj={
                "immediate": vmm_sdk.RebootScheduleImmediate,
                "later": vmm_sdk.RebootScheduleLater,
            },
            mutually_exclusive=[("immediate", "later")],
        ),
        project_ext_id=dict(type="str", required=False),
    )
    return module_args


def create_guest_reboot_policy(module, api_instance, result):
    validate_required_params(module, ["name", "categories", "reboot_schedule"])

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.GuestRebootPolicy()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Guest Reboot Policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_guest_reboot_policy(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Guest Reboot Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        ext_id = get_entity_ext_id_from_task(
            task, rel=TASK_CONSTANTS.RelEntityType.GUEST_REBOOT_POLICY
        )
        if ext_id:
            result["ext_id"] = ext_id
            policy = get_guest_reboot_policy(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(policy.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Guest Reboot Policy"
                ),
                msg="Failed to get entity ext_id from task for Guest Reboot Policy",
            )

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    strip_internal_attributes(current_spec)
    strip_internal_attributes(update_spec)
    return current_spec == update_spec


def update_guest_reboot_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_guest_reboot_policy(module, api_instance, ext_id=ext_id)

    update_spec = deepcopy(current_spec)
    if module.params.get("reboot_schedule"):
        # The reboot schedule is a oneOf, so drop the current one and let the
        # spec generator build the requested schedule type from scratch.
        update_spec.reboot_schedule = None

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=update_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update Guest Reboot Policy spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating Guest Reboot Policy", **result
        )
    kwargs = {"if_match": etag}

    strip_read_only_fields(update_spec, fields=_READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_guest_reboot_policy_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Guest Reboot Policy",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        policy = get_guest_reboot_policy(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(policy.to_dict())

    result["changed"] = True


def delete_guest_reboot_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Guest Reboot Policy with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_guest_reboot_policy(module, api_instance, ext_id=ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for deleting Guest Reboot Policy", **result
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.delete_guest_reboot_policy_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Guest Reboot Policy",
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
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    # Treat `immediate:` (YAML null) as a shorthand for `immediate: {}`.
    # mutually_exclusive on the arg-spec guarantees later isn't also set.
    reboot_schedule = module.params.get("reboot_schedule")
    if reboot_schedule is not None and "later" not in reboot_schedule:
        reboot_schedule["immediate"] = {}

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }

    api_instance = get_guest_reboot_policies_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_guest_reboot_policy(module, api_instance, result)
        else:
            create_guest_reboot_policy(module, api_instance, result)
    else:
        delete_guest_reboot_policy(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
