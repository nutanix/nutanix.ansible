#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snapshot_changed_contents_info_v2
short_description: Fetch mount target snapshot changed contents in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to fetch information about SnapshotChangedContent in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific SnapshotChangedContent.
  - If C(ext_id) is not provided, list multiple SnapshotChangedContent optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get / List SnapshotChangedContent) -
      Required Roles: Files Admin, Prism Admin, Super Admin, Backup Admin, Files Viewer, Prism Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - External identifier of the file server that owns the mount target.
      - Required for both get-by-ID and list operations.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - External identifier of the mount target (share) whose snapshot changed
        contents must be enumerated or fetched.
      - Required for both get-by-ID and list operations.
    type: str
    required: true
  ext_id:
    description:
      - External identifier of the SnapshotChangedContent bucket.
      - When provided the module fetches a single bucket. When omitted it lists
        all buckets for the given mount target.
    type: str
    required: false
  next_page_token:
    description:
      - Continuation token returned as the C(X-Next-Page-Token) header of a
        previous get-by-ID call. Only meaningful when C(ext_id) is provided.
      - The API returns paginated output (max 300 changes per page); use this
        token to retrieve the next page.
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
- name: Fetch a single snapshot changed content bucket by ext_id
  nutanix.ncp.ntnx_snapshot_changed_contents_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1"
  register: result
  ignore_errors: true

- name: Fetch the next page of a large snapshot changed content bucket
  nutanix.ncp.ntnx_snapshot_changed_contents_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1"
    next_page_token: "eyJvZmZzZXQiOjMwMH0="
  register: result
  ignore_errors: true

- name: List all snapshot changed content buckets for a mount target
  nutanix.ncp.ntnx_snapshot_changed_contents_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true

- name: List snapshot changed content buckets filtered by snapshotExtId
  nutanix.ncp.ntnx_snapshot_changed_contents_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    filter: "snapshotExtId eq '48f78959-14a6-4c47-b5db-920460c4b668'"
  register: result
  ignore_errors: true

- name: List snapshot changed content buckets with limit
  nutanix.ncp.ntnx_snapshot_changed_contents_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d8a37c9e-2b6a-4a17-b76f-33d6f11f61aa"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SnapshotChangedContent info v4 API.
    - It can be a single SnapshotChangedContent if external ID is provided.
    - List of multiple SnapshotChangedContent if external ID is not provided,
      optionally filtered by C(filter) / C(orderby) / C(select) or paginated
      by C(page) / C(limit).
  returned: always
  type: dict
  sample:
    {
      "base_snapshot_ext_id": "6c2c2a6c-7bd5-4e73-b74e-9fbc51c4f2e6",
      "changed_contents": [
          {
              "access_time": "2026-07-21T07:31:00.000000+00:00",
              "change_time": "2026-07-21T07:31:00.000000+00:00",
              "creation_time": "2026-07-21T07:30:59.000000+00:00",
              "inode_number": 12345,
              "object_type": "FILE",
              "old_path": null,
              "operation_type": "ADD",
              "path": "/share1/dir_a/new_file.txt",
              "size_bytes": 4096
          }
      ],
      "ext_id": "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1",
      "has_more_content": false,
      "links": null,
      "snapshot_ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual message set when there is an error.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching snapshot changed contents info"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the SnapshotChangedContent bucket.
  type: str
  returned: when external ID is provided
  sample: "3f8fd0f2-2e91-4b1e-9d21-2b0d5c56b6b1"

total_available_results:
  description: The total number of available SnapshotChangedContent buckets in Prism Central for the mount target.
  type: int
  returned: when all SnapshotChangedContent buckets are listed
  sample: 5
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        mount_target_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        next_page_token=dict(type="str", no_log=False),
    )
    return module_args


def get_snapshot_changed_content_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    next_page_token = module.params.get("next_page_token")
    resp = get_snapshot_changed_content(
        module=module,
        api_instance=api_instance,
        file_server_ext_id=file_server_ext_id,
        mount_target_ext_id=mount_target_ext_id,
        ext_id=ext_id,
        next_page_token=next_page_token,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_snapshot_changed_contents(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating snapshot changed contents info spec", **result
        )

    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")

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
            msg="Api Exception raised while fetching snapshot changed contents info",
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
    api_instance = get_snapshot_changed_contents_api_instance(module)
    if module.params.get("ext_id"):
        get_snapshot_changed_content_using_ext_id(module, api_instance, result)
    else:
        get_snapshot_changed_contents(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
