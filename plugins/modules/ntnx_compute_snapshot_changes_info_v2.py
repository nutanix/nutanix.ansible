#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_compute_snapshot_changes_info_v2
short_description: Fetch information about Nutanix Files compute-snapshot-change resources
version_added: 2.5.0
description:
  - This module allows you to fetch information about ComputeSnapshotChange in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ComputeSnapshotChange.
  - If C(ext_id) is not provided, list multiple ComputeSnapshotChange optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs (I(ntnx_files_py_client)).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get compute snapshot change by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, File Server Admin, File Server Viewer.
  - >-
    B(List compute snapshot changes) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin, File Server Admin, File Server Viewer.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the SnapshotChangedContent resource.
      - When set, the module performs a get-by-ID call and returns a single entity.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the file server hosting the mount target.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - The external ID of the mount target that the SnapshotChangedContent belongs to.
    type: str
    required: true
  x_next_page_token:
    description:
      - Pagination token forwarded to the SDK's C(X-Next-Page-Token) header when fetching
        a specific SnapshotChangedContent by external ID.
      - The Files v4 API returns the changed-content page-by-page (maximum 300 entries per
        page) and provides a token for the next page; pass that token here on subsequent
        calls.
      - Only applies when C(ext_id) is provided (single-entity fetch).
    type: str
    required: false
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
- name: Get snapshot changed content using ext_id
  nutanix.ncp.ntnx_compute_snapshot_changes_info_v2:
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: Get next page of an existing snapshot changed content
  nutanix.ncp.ntnx_compute_snapshot_changes_info_v2:
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
    x_next_page_token: "eyJvZmZzZXQiOjMwMH0="
  register: result
  ignore_errors: true

- name: List all snapshot changed contents for a mount target
  nutanix.ncp.ntnx_compute_snapshot_changes_info_v2:
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true

- name: List snapshot changed contents with filter
  nutanix.ncp.ntnx_compute_snapshot_changes_info_v2:
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    filter: "snapshotExtId eq '3e2d5fbb-0000-0000-0000-000000000002'"
  register: result
  ignore_errors: true

- name: List snapshot changed contents with pagination
  nutanix.ncp.ntnx_compute_snapshot_changes_info_v2:
    file_server_ext_id: "6c6f6f6b-1234-4321-9abc-abcdef012345"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    limit: 10
    page: 0
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ComputeSnapshotChange info v4 API.
    - It can be a single ComputeSnapshotChange if external ID is provided.
    - List of multiple ComputeSnapshotChange if external ID is not provided with optional
      filter or limit.
  returned: always
  type: dict
  sample:
    {
      "base_snapshot_ext_id": "3e2d5fbb-0000-0000-0000-000000000001",
      "changed_contents": [
          {
              "access_time": null,
              "change_time": "2026-07-21T05:00:00Z",
              "creation_time": "2026-07-21T05:00:00Z",
              "inode_number": 42,
              "object_type": "FILE",
              "old_path": null,
              "operation_type": "CREATED",
              "path": "/share/dir1/file1.txt",
              "size_bytes": 1024
          }
      ],
      "ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "has_more_content": false,
      "links": null,
      "snapshot_ext_id": "3e2d5fbb-0000-0000-0000-000000000002",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/info message emitted by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching compute snapshot changes info"

error:
  description: Error message if any error occurred.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the SnapshotChangedContent (single-entity fetch only).
  type: str
  returned: when external ID is provided
  sample: "48f78959-14a6-4c47-b5db-920460c4b668"

total_available_results:
  description: The total number of available SnapshotChangedContent entries returned by the list API.
  type: int
  returned: when all compute snapshot changes are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_snapshot_changed_contents_api_instance,
)
from ..module_utils.v4.files.helpers import get_snapshot_changed_content  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        file_server_ext_id=dict(type="str", required=True),
        mount_target_ext_id=dict(type="str", required=True),
        x_next_page_token=dict(type="str", no_log=False),
    )
    return module_args


def get_snapshot_changed_content_using_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    ext_id = module.params.get("ext_id")
    entity = get_snapshot_changed_content(
        module,
        api_instance,
        file_server_ext_id,
        mount_target_ext_id,
        ext_id,
        x_next_page_token=module.params.get("x_next_page_token"),
    )
    result["ext_id"] = ext_id
    if entity is not None:
        result["response"] = strip_internal_attributes(entity.to_dict())
    else:
        result["response"] = {}


def list_snapshot_changed_contents(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating compute snapshot changes info spec", **result
        )

    try:
        resp = api_instance.list_snapshot_changed_contents(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching compute snapshot changes info "
                "for mount target '{0}' on file server '{1}'"
            ).format(mount_target_ext_id, file_server_ext_id),
        )

    total_available_results = None
    metadata = getattr(resp, "metadata", None)
    if metadata is not None:
        total_available_results = getattr(metadata, "total_available_results", None)
    if total_available_results is not None:
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_snapshot_changed_contents_api_instance(module)
    if module.params.get("ext_id"):
        get_snapshot_changed_content_using_ext_id(module, api_instance, result)
    else:
        list_snapshot_changed_contents(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
