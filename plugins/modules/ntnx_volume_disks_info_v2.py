#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_disks_info_v2
short_description: Fetch information about Volume Disks in a Nutanix Volume Group
version_added: 2.7.0
description:
  - This module allows you to fetch information about VolumeDisk in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VolumeDisk.
  - If C(ext_id) is not provided, list multiple VolumeDisk optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get the details of a Volume Disk) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer,
      Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager, Storage Admin,
      Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(List all the Volume Disks attached to the Volume Group) -
      Required Roles: CSI System, Disaster Recovery Admin, Disaster Recovery Viewer,
      Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager, Storage Admin,
      Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    ext_id:
        description:
            - The external ID of the Volume Disk to fetch.
            - If provided, a single Volume Disk is fetched.
        type: str
        required: false
    volume_group_ext_id:
        description:
            - The external ID of the Volume Group that owns the Volume Disks.
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
- name: Fetch a specific Volume Disk using ext_id
  nutanix.ncp.ntnx_volume_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    ext_id: "4e00e28d-4d93-4587-a8f0-4502d72224c8"
  register: result
  ignore_errors: true

- name: List all Volume Disks of a Volume Group
  nutanix.ncp.ntnx_volume_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
  register: result
  ignore_errors: true

- name: List Volume Disks with filter
  nutanix.ncp.ntnx_volume_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    filter: "index eq 1"
  register: result
  ignore_errors: true

- name: List Volume Disks with limit
  nutanix.ncp.ntnx_volume_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b34"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VolumeDisk info v4 API.
    - It can be a single VolumeDisk if external ID is provided.
    - List of multiple VolumeDisk if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "description": "ansible-updated-disk",
      "disk_data_source_reference": null,
      "disk_size_bytes": 42949672960,
      "disk_storage_features": {
          "flash_mode": {
              "is_enabled": false
          }
      },
      "ext_id": "046020bf-e7e0-419e-854c-e971967eca5c",
      "index": 1,
      "links": null,
      "storage_container_id": "44481f83-d0a1-47b3-b9b8-32b5465c622e",
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the Volume Disk.
    - Only returned when a specific Volume Disk is fetched by ext_id.
  returned: when external ID is provided
  type: str
  sample: "046020bf-e7e0-419e-854c-e971967eca5c"

volume_group_ext_id:
  description: The external ID of the Volume Group that owns the disk(s).
  returned: always
  type: str
  sample: "d32862d3-5218-4970-61e2-da2a2ce8df50"

total_available_results:
  description:
    - The total number of Volume Disks available in the Volume Group when listing.
  returned: when listing Volume Disks
  type: int
  sample: 3

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Volume Disks info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
        volume_group_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_volume_disk_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    try:
        resp = api_instance.get_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Disk info",
        )
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_volume_disks(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Volume Disks info spec", **result)

    try:
        resp = api_instance.list_volume_disks_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Disks info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["volume_group_ext_id"] = volume_group_ext_id
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
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_volume_disk_using_ext_id(module, api_instance, result)
    else:
        get_volume_disks(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
