#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_associate_host_nic_to_nic_profile_v2
short_description: Associate or disassociate a Host NIC with a NIC Profile in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to associate or disassociate a Host NIC with a NIC Profile in Nutanix Prism Central.
  - When C(state) is C(present), the module associates the specified Host NIC with the NIC Profile
    identified by C(ext_id). Associating a Host NIC configures Virtual Functions (VFs) on the physical NIC
    according to the NIC Profile capability (for example SR-IOV or DP_OFFLOAD).
  - When C(state) is C(absent), the module disassociates the specified Host NIC from the NIC Profile
    identified by C(ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Associate a Host NIC to a NIC Profile) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - >-
      B(Disassociate a Host NIC from a NIC Profile) -
      Required Roles: Network Infra Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module will associate the given Host NIC with the NIC Profile.
      - If C(state) is set to C(absent) the module will disassociate the given Host NIC from the NIC Profile.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the NIC Profile.
      - Required for both associate and disassociate operations.
    type: str
    required: true
  host_nic_ext_id:
    description:
      - The external ID (UUID) of the Host NIC to associate with or disassociate from the NIC Profile.
      - Required for both associate and disassociate operations.
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
- name: Associate Host NIC to NIC Profile
  nutanix.ncp.ntnx_associate_host_nic_to_nic_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    host_nic_ext_id: "c1f27ed6-e6dd-4c34-9fda-1acdb1234567"
  register: result
  ignore_errors: true

- name: Disassociate Host NIC from NIC Profile
  nutanix.ncp.ntnx_associate_host_nic_to_nic_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    host_nic_ext_id: "c1f27ed6-e6dd-4c34-9fda-1acdb1234567"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for associating or disassociating a Host NIC with a NIC Profile.
    - If C(wait) is true, contains the completed task details.
    - If C(wait) is false, contains the submitted task reference.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "000642d8-a2e0-e442-0b82-606eab989991"
      ],
      "completed_time": "2026-07-20T13:23:32.384983+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T13:21:50.094877+00:00",
      "entities_affected": [
          {
              "ext_id": "68e4c68e-1acf-4c05-7792-e062119acb68",
              "name": "nic_profile_ansible",
              "rel": "networking:config:nic-profile"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:2bf53fdd-309b-5971-9f4b-436c86e8f92f",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T13:23:32.384982+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 0,
      "operation": "AssociateHostNicToNicProfile",
      "operation_description": "Associate Host NIC to NIC Profile",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-07-20T13:21:50.525912+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task submitted to the platform.
  returned: always
  type: str
  sample: "ZXJnb24=:2bf53fdd-309b-5971-9f4b-436c86e8f92f"

ext_id:
  description:
    - The external ID of the NIC Profile that the Host NIC was associated with / disassociated from.
  returned: always
  type: str
  sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

changed:
  description: Indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: Error details when an error occurs.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message describing the module outcome.
  returned: When there is an error or a contextual message
  type: str
  sample: "Api Exception raised while associating Host NIC to NIC Profile"
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


def _build_host_nic_spec(module, result, action):
    """
    Build the HostNic body used by both associate and disassociate operations.
    """
    sg = SpecGenerator(module)
    default_spec = networking_sdk.HostNic()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Host NIC spec for {0} operation".format(action),
            **result,
        )
    if not getattr(spec, "host_nic_ext_id", None):
        spec.host_nic_ext_id = module.params.get("host_nic_ext_id")
    return spec


def associate_host_nic_to_nic_profile(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_host_nic_spec(module, result, action="associate")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = nic_profiles.associate_host_nic_to_nic_profile(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating Host NIC to NIC Profile",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def disassociate_host_nic_from_nic_profile(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_host_nic_spec(module, result, action="disassociate")

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = nic_profiles.disassociate_host_nic_from_nic_profile(
            extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating Host NIC from NIC Profile",
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
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "error": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    nic_profiles = get_nic_profiles_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        associate_host_nic_to_nic_profile(module, nic_profiles, result)
    else:
        disassociate_host_nic_from_nic_profile(module, nic_profiles, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
