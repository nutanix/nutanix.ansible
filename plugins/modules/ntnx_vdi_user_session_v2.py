#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vdi_user_session_v2
short_description: Update Nutanix Files VDI synchronization user session
version_added: 2.7.0
description:
    - Update the owner file server for a specific VDI synchronization user
      session under a VDI-sync replication policy.
    - Used to resolve conflicted situations where two file servers claim to
      own the same VDI user profile.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Update VDI user session) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported (update only).
        type: str
        choices:
            - present
        default: present
    file_server_ext_id:
        description:
            - External ID of the file server that owns the replication policy.
        type: str
        required: true
    replication_policy_ext_id:
        description:
            - External ID of the VDI sync replication policy.
        type: str
        required: true
    ext_id:
        description:
            - External ID of the VDI synchronization user session to update.
        type: str
        required: true
    user_name:
        description:
            - Username the session belongs to.
        type: str
        required: false
    owner_file_server_ext_id:
        description:
            - External ID of the file server that should become the new
              owner of the user session.
        type: str
        required: false
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
- name: Change the owner file server for a VDI user session
  nutanix.ncp.ntnx_vdi_user_session_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
    replication_policy_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    ext_id: "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11"
    user_name: "vdiuser1"
    owner_file_server_ext_id: "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description: Updated VDI user session details, or task details for the update.
    returned: always
    type: dict
    sample:
        {
            "current_session": null,
            "ext_id": "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11",
            "links": null,
            "owner_file_server_ext_id": "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19",
            "tenant_id": null,
            "user_name": "vdiuser1"
        }

changed:
    description: Whether the module made any change.
    returned: always
    type: bool
    sample: true

msg:
    description: Status/error message.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while updating VDI user session"

error:
    description: Error details.
    returned: when an error occurs
    type: str

failed:
    description: Whether the module failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: External ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: External ID of the updated VDI user session.
    returned: always
    type: str
    sample: "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_replication_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_vdi_user_session  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    # The Files SDK is required at runtime even though we do not build any
    # SDK spec objects directly in this module; SpecGenerator mutates the
    # ``old_spec`` returned by the GET call.
    import ntnx_files_py_client  # noqa: E402,F401 # pylint: disable=unused-import
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        replication_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        user_name=dict(type="str", required=False),
        owner_file_server_ext_id=dict(type="str", required=False),
    )
    return module_args


def update_vdi_user_session(module, api_instance, result):
    """Update the owner file server for the VDI user session."""
    file_server_ext_id = module.params.get("file_server_ext_id")
    replication_policy_ext_id = module.params.get("replication_policy_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_vdi_user_session(
        module,
        api_instance,
        file_server_ext_id,
        replication_policy_ext_id,
        ext_id,
    )
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating VDI user session", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VDI user session update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.update_vdi_user_session_by_id(
            fileServerExtId=file_server_ext_id,
            replicationPolicyExtId=replication_policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VDI user session",
        )

    task_ext_id = resp.data.ext_id if resp and resp.data else None
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        latest = get_vdi_user_session(
            module,
            api_instance,
            file_server_ext_id,
            replication_policy_ext_id,
            ext_id,
        )
        result["response"] = strip_internal_attributes(latest.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_replication_policies_api_instance(module)
    update_vdi_user_session(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
