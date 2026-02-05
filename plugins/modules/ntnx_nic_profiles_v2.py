#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nic_profiles_v2
short_description: Create, Update, Delete NIC profiles in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete NIC profiles in Nutanix Prism Central.
  - Use ntnx_nic_profiles_association_v2 module to associate or disassociate host NICs.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - If C(state) is set to C(present) and ext_id is not provided then the operation will create the NIC profile.
      - If C(state) is set to C(present) and ext_id is provided then the operation will update the NIC profile.
      - If C(state) is set to C(absent) and ext_id is provided then the operation will delete the NIC profile.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External ID of the NIC profile.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the NIC profile.
      - Required for create and update operations.
    type: str
    required: false
  description:
    description:
      - Description of the NIC profile.
    type: str
    required: false
  capability_config:
    description:
      - Capability specification of the NIC profile.
      - Required for create and update operations.
    type: dict
    required: false
    suboptions:
      capability_type:
        description:
          - Capability type for the NIC profile.
        type: str
        choices:
          - SRIOV
          - DP_OFFLOAD
        required: true
  nic_family:
    description:
      - Specification for a specific device family of Host NIC.
      - The given string must be in the format vendor_id:device_id.
      - Required for create and update operations.
    type: str
    required: false
  metadata:
    description:
      - Metadata associated with the NIC profile resource.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - The userName of the owner of this resource.
        type: str
        required: false
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
        required: false
      project_name:
        description:
          - The name of the project this resource belongs to.
        type: str
        required: false
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create NIC profile
  nutanix.ncp.ntnx_nic_profiles_v2:
    state: present
    name: "nic_profile_sriov"
    description: "SRIOV profile for host NICs"
    capability_config:
      capability_type: "SRIOV"
    nic_family: "15b3:101d"
  register: result
  ignore_errors: true

- name: Update NIC profile
  nutanix.ncp.ntnx_nic_profiles_v2:
    state: present
    ext_id: "ad2c7c4e-4694-4c95-82f4-eadc761a4d17"
    name: "nic_profile_sriov_updated"
    description: "Updated NIC profile description"
  register: result
  ignore_errors: true

- name: Delete NIC profile
  nutanix.ncp.ntnx_nic_profiles_v2:
    state: absent
    ext_id: "ad2c7c4e-4694-4c95-82f4-eadc761a4d17"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting NIC profiles.
    - If the operation is create or update and C(wait) is true, it will return the NIC profile details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "capability_config": {
          "capability_type": "SRIOV"
      },
      "description": "First NIC profile created by ansible",
      "ext_id": "f98bdee4-fa0d-4b8b-a68e-f020d5a7fcfb",
      "host_nic_references": null,
      "links": null,
      "metadata": {
          "category_ids": null,
          "owner_reference_id": "00000000-0000-0000-0000-000000000000",
          "owner_user_name": "admin",
          "project_name": null,
          "project_reference_id": null
      },
      "name": "nic_profile_ansible_GSPVxekSKefu_first",
      "nic_family": "15b3:101d",
      "tenant_id": null
    }
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:15cb540e-df8d-41d7-807c-d39fdd253e81"
ext_id:
  description:
    - The external ID of the NIC profile.
  returned: always
  type: str
  sample: "3adb2f67-8ba3-49a8-b907-7c865671f744"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false
skipped:
  description: This indicates whether the operation was skipped
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Nothing to change."
error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
failed:
  description: Indicates if the operation failed.
  type: bool
  returned: always
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_nic_profiles_api_instance,
)
from ..module_utils.v4.network.helpers import get_nic_profile  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    capability_config_spec = dict(
        capability_type=dict(
            type="str",
            choices=["SRIOV", "DP_OFFLOAD"],
            obj=networking_sdk.CapabilityType,
            required=True,
        ),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str", required=False),
        owner_user_name=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        project_name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        capability_config=dict(
            type="dict",
            options=capability_config_spec,
            obj=networking_sdk.CapabilityConfig,
            required=False,
        ),
        nic_family=dict(type="str", required=False),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            obj=networking_sdk.Metadata,
            required=False,
        ),
    )
    return module_args


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    return old_spec_dict == update_spec_dict


def create_nic_profile(module, nic_profiles, result):
    sg = SpecGenerator(module)
    default_spec = networking_sdk.NicProfile()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create NIC profile Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = nic_profiles.create_nic_profile(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating NIC profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.NIC_PROFILE
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_nic_profile(module, nic_profiles, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def update_nic_profile(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_nic_profile(module, nic_profiles, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating NIC profile", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update NIC profile Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = nic_profiles.update_nic_profile_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating NIC profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_nic_profile(module, nic_profiles, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_nic_profile(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "NIC profile with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = nic_profiles.delete_nic_profile_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting NIC profile",
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
            ("state", "present", ("ext_id", "name"), True),
            ("state", "present", ("ext_id", "capability_config"), True),
            ("state", "present", ("ext_id", "nic_family"), True),
            ("state", "absent", ("ext_id",)),
        ],
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
    state = module.params.get("state")
    nic_profiles = get_nic_profiles_api_instance(module)

    if state == "absent":
        delete_nic_profile(module, nic_profiles, result)
        module.exit_json(**result)

    if module.params.get("ext_id"):
        update_nic_profile(module, nic_profiles, result)
    else:
        create_nic_profile(module, nic_profiles, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
