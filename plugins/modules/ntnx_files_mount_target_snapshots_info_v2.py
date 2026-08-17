#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_mount_target_snapshots_info_v2
short_description: Fetch mount target snapshots info in Nutanix Files
version_added: 2.7.0
description:
  - This module allows you to fetch information about MountTargetSnapshot in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific MountTargetSnapshot.
  - If C(ext_id) is not provided, list multiple MountTargetSnapshot optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
options:
  ext_id:
    description:
      - The external ID of the mount target snapshot.
      - If provided, fetch the specific mount target snapshot.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external ID of the file server that owns the mount target.
    type: str
    required: true
  mount_target_ext_id:
    description:
      - The external ID of the mount target (share/export).
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
- name: Get mount target snapshot using ext_id
  nutanix.ncp.ntnx_files_mount_target_snapshots_info_v2:
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "48f78959-14a6-4c47-b5db-920460c4b668"
  register: result
  ignore_errors: true

- name: List all mount target snapshots
  nutanix.ncp.ntnx_files_mount_target_snapshots_info_v2:
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true

- name: List mount target snapshots with filter
  nutanix.ncp.ntnx_files_mount_target_snapshots_info_v2:
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    filter: "name eq 'mount_target_snapshot_ansible'"
  register: result
  ignore_errors: true

- name: List mount target snapshots with limit
  nutanix.ncp.ntnx_files_mount_target_snapshots_info_v2:
    file_server_ext_id: "5f1b7b3e-1234-4c47-b5db-920460c4b668"
    mount_target_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC MountTargetSnapshot info v4 API.
    - It can be a single MountTargetSnapshot if external ID is provided.
    - List of multiple MountTargetSnapshot if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "create_time": "2026-07-21T07:36:00.000000+00:00",
      "ext_id": "48f78959-14a6-4c47-b5db-920460c4b668",
      "links": null,
      "name": "mount_target_snapshot_ansible",
      "reclaimable_space_bytes": 0,
      "tenant_id": null,
      "total_space_bytes": 0,
      "type": "USER_SNAPSHOT"
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching mount target snapshots info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the mount target snapshot
  type: str
  returned: when external ID is provided
  sample: "48f78959-14a6-4c47-b5db-920460c4b668"

total_available_results:
  description: The total number of available mount target snapshots.
  type: int
  returned: when all mount target snapshots are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_snapshots_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import get_mount_target_snapshot  # noqa: E402
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
        mount_target_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_mount_target_snapshot_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    resp = get_mount_target_snapshot(
        module, api_instance, ext_id, file_server_ext_id, mount_target_ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_mount_target_snapshots(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    mount_target_ext_id = module.params.get("mount_target_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating mount target snapshots info spec", **result
        )

    try:
        resp = api_instance.list_mount_target_snapshots(
            fileServerExtId=file_server_ext_id,
            mountTargetExtId=mount_target_ext_id,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching mount target snapshots info",
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
    api_instance = get_snapshots_api_instance(module)
    if module.params.get("ext_id"):
        get_mount_target_snapshot_using_ext_id(module, api_instance, result)
    else:
        get_mount_target_snapshots(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
