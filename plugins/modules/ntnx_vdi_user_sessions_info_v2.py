#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vdi_user_sessions_info_v2
short_description: Fetch VDI synchronization user sessions info in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to fetch information about VDI synchronization user
    sessions in Nutanix Files.
  - If C(ext_id) is provided, fetch details of the specific VDI user session.
  - If C(ext_id) is not provided, list all VDI user sessions belonging to the
    supplied file server and VDI-sync replication policy, optionally filtered,
    ordered, projected, paginated or limited.
  - This module uses Prism Central v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get VDI user session by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, File Server Admin,
    File Server Viewer
  - >-
    B(List VDI user sessions) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, File Server Admin,
    File Server Viewer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external identifier of the VDI synchronization user session.
      - If provided, only that single user session is fetched (get-by-ID).
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that hosts the VDI-sync
        replication policy.
    type: str
    required: true
  replication_policy_ext_id:
    description:
      - The external identifier of the VDI-sync replication policy that owns the
        VDI user sessions.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch a VDI user session using ext_id
  nutanix.ncp.ntnx_vdi_user_sessions_info_v2:
    file_server_ext_id: "b1c9d6a2-1234-4c22-8d41-000000000001"
    replication_policy_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "e5d3f0a1-4444-4222-8d41-000000000010"
  register: result
  ignore_errors: true

- name: List all VDI user sessions for a replication policy
  nutanix.ncp.ntnx_vdi_user_sessions_info_v2:
    file_server_ext_id: "b1c9d6a2-1234-4c22-8d41-000000000001"
    replication_policy_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true

- name: List VDI user sessions with a filter
  nutanix.ncp.ntnx_vdi_user_sessions_info_v2:
    file_server_ext_id: "b1c9d6a2-1234-4c22-8d41-000000000001"
    replication_policy_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    filter: "userName eq 'EXAMPLE\\\\alice'"
  register: result
  ignore_errors: true

- name: List VDI user sessions with a limit
  nutanix.ncp.ntnx_vdi_user_sessions_info_v2:
    file_server_ext_id: "b1c9d6a2-1234-4c22-8d41-000000000001"
    replication_policy_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VdiUserSession info v4 API.
    - It can be a single VdiUserSession if external ID is provided.
    - List of multiple VdiUserSession if external ID is not provided with optional
      filter, orderby, select, page or limit.
  returned: always
  type: dict
  sample:
    {
      "current_session": {
          "failure_reason": null,
          "file_server_ext_id": "5f7b26f9-aaaa-4c22-8d41-000000000002",
          "login_time": "2026-05-06T11:50:01.000000+00:00",
          "logout_time": null,
          "status": "SUCCEEDED"
      },
      "ext_id": "e5d3f0a1-4444-4222-8d41-000000000010",
      "links": null,
      "owner_file_server_ext_id": "5f7b26f9-aaaa-4c22-8d41-000000000002",
      "tenant_id": null,
      "user_name": "EXAMPLE\\alice"
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VDI user sessions info"

error:
  description:
    - This field typically holds information about errors that occurred during
      the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the VDI user session.
  type: str
  returned: when external ID is provided
  sample: "e5d3f0a1-4444-4222-8d41-000000000010"

total_available_results:
  description: The total number of available VDI user sessions in the referenced replication policy.
  type: int
  returned: when all VDI user sessions are fetched
  sample: 5
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
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        replication_policy_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_vdi_user_session_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_vdi_user_session(
        module,
        api_instance,
        module.params.get("file_server_ext_id"),
        module.params.get("replication_policy_ext_id"),
        ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def get_vdi_user_sessions(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VDI user sessions info spec", **result)

    try:
        resp = api_instance.list_vdi_user_sessions(
            fileServerExtId=module.params.get("file_server_ext_id"),
            replicationPolicyExtId=module.params.get("replication_policy_ext_id"),
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
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
