#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_mount_targets_info_v2
short_description: Fetch Nutanix Files mount target(s) information
version_added: 2.5.0
description:
  - This module allows you to fetch information about MountTarget in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific MountTarget.
  - If C(ext_id) is not provided, list multiple MountTarget optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get MountTarget by ext_id) -
      Required Roles: Files Admin, Files Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List MountTargets) -
      Required Roles: Files Admin, Files Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external ID of the parent file server.
      - Required for both get-by-id and list operations.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the mount target to fetch.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Get mount target using ext_id
  nutanix.ncp.ntnx_files_mount_targets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    ext_id: "b8f1cc23-1111-2222-3333-4441c4d5aa11"
  register: result

- name: List all mount targets on a file server
  nutanix.ncp.ntnx_files_mount_targets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result

- name: List mount targets with filter
  nutanix.ncp.ntnx_files_mount_targets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    filter: "name eq 'ansible_smb_share'"
  register: result

- name: List mount targets with limit
  nutanix.ncp.ntnx_files_mount_targets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
    limit: 5
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC MountTarget info v4 API.
    - It can be a single MountTarget if external ID is provided.
    - List of multiple MountTarget if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "blocked_clients": null,
      "blocked_file_extensions": null,
      "connected_mount_target_path": null,
      "description": "SMB share created by Ansible",
      "ext_id": "b8f1cc23-1111-2222-3333-4441c4d5aa11",
      "is_compression_enabled": true,
      "is_long_name_enabled": null,
      "is_previous_version_enabled": null,
      "is_snapshot_paused": null,
      "links": null,
      "max_size_gb": 100,
      "multi_protocol_properties": null,
      "name": "ansible_smb_share",
      "nfs_properties": null,
      "parent_mount_target_ext_id": null,
      "path": null,
      "protocol": "SMB",
      "secondary_protocol": null,
      "smb_properties": {
          "is_access_based_enumeration_enabled": true,
          "is_ca_enabled": false,
          "is_smb3_encryption_enabled": true,
          "share_acl": null
      },
      "state": "ONLINE",
      "status_type": null,
      "tenant_id": null,
      "type": "GENERAL",
      "workload_type": null,
      "worm_spec": null
    }

changed:
  description: Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual message when applicable.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching mount targets info"

error:
  description: Error details when the module fails.
  type: str
  returned: when an error occurs

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the mount target.
  type: str
  returned: when external ID is provided
  sample: "b8f1cc23-1111-2222-3333-4441c4d5aa11"

total_available_results:
  description: The total number of available mount targets on the file server.
  type: int
  returned: when listing mount targets
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_mount_targets_api_instance,
)
from ..module_utils.v4.files.helpers import get_mount_target  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def get_mount_target_using_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_mount_target(module, api_instance, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_mount_targets(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating mount targets info spec", **result)

    try:
        resp = api_instance.list_mount_targets(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching mount targets info",
        )

    total_available_results = (
        resp.metadata.total_available_results if resp.metadata else None
    )
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
    api_instance = get_mount_targets_api_instance(module)
    if module.params.get("ext_id"):
        get_mount_target_using_ext_id(module, api_instance, result)
    else:
        get_mount_targets(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
