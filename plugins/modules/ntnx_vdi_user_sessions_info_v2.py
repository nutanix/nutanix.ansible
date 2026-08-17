#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vdi_user_sessions_info_v2
short_description: Fetch Nutanix Files VDI synchronization user sessions
version_added: 2.7.0
description:
  - This module allows you to fetch information about VDI synchronization
    user sessions belonging to a VDI-sync replication policy.
  - If C(ext_id) is provided, fetch details of the specific VDI user session.
  - If C(ext_id) is not provided, list multiple VDI user sessions optionally
    filtered / paginated.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get / List VDI user sessions) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - External ID of the file server owning the replication policy.
    type: str
    required: true
  replication_policy_ext_id:
    description:
      - External ID of the VDI sync replication policy.
    type: str
    required: true
  ext_id:
    description:
      - External ID of the VDI synchronization user session to fetch.
      - If not provided, list of user sessions is returned.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get VDI user session by ext_id
  nutanix.ncp.ntnx_vdi_user_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
    replication_policy_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    ext_id: "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11"
  register: result
  ignore_errors: true

- name: List all VDI user sessions in a policy
  nutanix.ncp.ntnx_vdi_user_sessions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11"
    replication_policy_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VDI user sessions v4 API.
    - Single VdiUserSession if external ID is provided.
    - List of VdiUserSession if external ID is not provided.
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
  description: Whether the module made any change (always False for info modules).
  returned: always
  type: bool
  sample: false

msg:
  description: Message set when there is an error.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VDI user sessions info"

error:
  description: Error details.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VDI user session (only when fetching by ID).
  type: str
  returned: when external ID is provided
  sample: "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11"

total_available_results:
  description: Total number of VDI user sessions in the policy.
  type: int
  returned: when listing all sessions
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_replication_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_vdi_user_session  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        replication_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_vdi_user_session_using_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    replication_policy_ext_id = module.params.get("replication_policy_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_vdi_user_session(
        module,
        api_instance,
        file_server_ext_id,
        replication_policy_ext_id,
        ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_vdi_user_sessions(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    replication_policy_ext_id = module.params.get("replication_policy_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VDI user sessions info spec", **result)

    try:
        resp = api_instance.list_vdi_user_sessions(
            fileServerExtId=file_server_ext_id,
            replicationPolicyExtId=replication_policy_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VDI user sessions info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_replication_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_vdi_user_session_using_ext_id(module, api_instance, result)
    else:
        get_vdi_user_sessions(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
