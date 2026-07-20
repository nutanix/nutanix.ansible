#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_nic_from_nic_profile_v2
short_description: Associate or disassociate a Host NIC to/from a NIC Profile in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to associate a Host NIC with an existing NIC Profile
      or disassociate a Host NIC from an existing NIC Profile in Nutanix Prism Central.
    - When C(state) is C(present), the module associates the Host NIC identified by
      C(host_nic_ext_id) to the NIC Profile identified by C(ext_id).
    - When C(state) is C(absent), the module disassociates the Host NIC identified by
      C(host_nic_ext_id) from the NIC Profile identified by C(ext_id).
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Associate a Host NIC to a NIC Profile) -
      Required Roles/Permissions: Associate_Host_Nic_Nic_Profile, View_Nic_Profile, Update_Nic_Profile
      (typically granted to Prism Admin, Super Admin, Network Infra Admin).
    - >-
      B(Disassociate a Host NIC from a NIC Profile) -
      Required Roles/Permissions: Disassociate_Host_Nic_Nic_Profile, View_Nic_Profile, Update_Nic_Profile
      (typically granted to Prism Admin, Super Admin, Network Infra Admin).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
    state:
        description:
            - If C(state) is set to C(present), the module associates the Host NIC to the NIC Profile.
            - If C(state) is set to C(absent), the module disassociates the Host NIC from the NIC Profile.
        type: str
        required: false
        choices:
            - present
            - absent
        default: present
    ext_id:
        description:
            - The external ID (UUID) of the NIC Profile that the Host NIC will be
              associated to or disassociated from.
        type: str
        required: true
    host_nic_ext_id:
        description:
            - The external ID (UUID) of the Host NIC to associate or disassociate.
        type: str
        required: true
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
- name: Associate a Host NIC to a NIC Profile
  nutanix.ncp.ntnx_host_nic_from_nic_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    host_nic_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: result
  ignore_errors: true

- name: Disassociate a Host NIC from a NIC Profile
  nutanix.ncp.ntnx_host_nic_from_nic_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    host_nic_ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for associating or disassociating a Host NIC to/from a NIC Profile.
        - Task details if C(wait) is true.
        - Task reference details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T13:09:07.069647+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T13:09:06.992506+00:00",
            "entities_affected": [
                {
                    "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
                    "name": null,
                    "rel": "networking:config:nic_profile"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T13:09:07.069646+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "kNicProfileUpdateAssociation",
            "operation_description": "NIC Profile Update Association",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T13:09:07.006009+00:00",
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
    returned: When there is an error or module is running in check mode.
    type: str
    sample: "Api Exception raised while associating host NIC to NIC Profile"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: when an error occurs
    type: str
    sample: "Failed to generate spec for associating host NIC to NIC Profile"

failed:
    description: This field typically holds information about if the task have failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the NIC Profile on which the association/disassociation was performed.
    returned: always
    type: str
    sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_nic_profiles_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        host_nic_ext_id=dict(type="str", required=True),
    )
    return module_args


def _build_host_nic_spec(module, result):
    """Build a HostNic spec object from module parameters."""
    sg = SpecGenerator(module)
    default_spec = networking_sdk.HostNic()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for host NIC to NIC Profile action",
            **result,
        )
    return spec


def associate_host_nic_to_nic_profile(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_host_nic_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Host NIC '{0}' will be associated to NIC Profile '{1}'.".format(
                module.params.get("host_nic_ext_id"), ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.associate_host_nic_to_nic_profile(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating host NIC to NIC Profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def disassociate_host_nic_from_nic_profile(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_host_nic_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Host NIC '{0}' will be disassociated from NIC Profile '{1}'.".format(
                module.params.get("host_nic_ext_id"), ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.disassociate_host_nic_from_nic_profile(
            extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating host NIC from NIC Profile",
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
            msg=missing_required_lib("ntnx_networking_py_client"),
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

    api_instance = get_nic_profiles_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        associate_host_nic_to_nic_profile(module, api_instance, result)
    else:
        disassociate_host_nic_from_nic_profile(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
