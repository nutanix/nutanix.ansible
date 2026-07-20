#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_disks_info_v2
short_description: Fetch information about Nutanix PC Volume Disks
version_added: 2.7.0
description:
  - This module allows you to fetch information about VolumeDisk in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VolumeDisk.
  - If C(ext_id) is not provided, list multiple VolumeDisk optionally filtered / paginated.
  - This module uses the Nutanix PC v4 storage APIs based SDK (C(ntnx_storage_py_client)).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Get the details of a Volume Disk or list Volume Disks) -
    Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer,
    Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager,
    Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external identifier of the Volume Disk.
      - If provided, the module fetches a single Volume Disk.
    type: str
    required: false
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group that owns the Volume Disks.
    type: str
    required: true
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
- name: Fetch information about all Volume Disks of a Volume Group
  nutanix.ncp.ntnx_volume_disks_info_v2:
    volume_group_ext_id: "530567f3-abda-4913-b5d0-0ab6758ec1653"
  register: result

- name: Fetch information about all Volume Disks of a Volume Group with pagination
  nutanix.ncp.ntnx_volume_disks_info_v2:
    volume_group_ext_id: "530567f3-abda-4913-b5d0-0ab6758ec1653"
    page: 0
    limit: 50
  register: result

- name: Fetch a specific Volume Disk of a Volume Group
  nutanix.ncp.ntnx_volume_disks_info_v2:
    volume_group_ext_id: "530567f3-abda-4913-b5d0-0ab6758ec1653"
    ext_id: "530567f3-abda-4913-b5d0-0ab6758ec1654"
  register: result

- name: Fetch Volume Disks with filter
  nutanix.ncp.ntnx_volume_disks_info_v2:
    volume_group_ext_id: "530567f3-abda-4913-b5d0-0ab6758ec1653"
    filter: "storageContainerId eq '10eb150f-e8b8-4d69-a828-6f23771d3723'"
  register: result
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
      "created_time": null,
      "description": null,
      "disk_data_source_reference": null,
      "disk_size_bytes": 21474836480,
      "disk_storage_features": {
        "flash_mode": {
          "is_enabled": true
        }
      },
      "ext_id": "4e00e28d-4d93-4587-a8f0-4502d72224c8",
      "index": 0,
      "links": null,
      "storage_container_id": "10eb150f-e8b8-4d69-a828-6f23771d3723",
      "tenant_id": null
    }

volume_group_ext_id:
  description: Volume Group external ID.
  type: str
  returned: always
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"

ext_id:
  description: Volume Disk external ID. Only returned when a single Volume Disk is fetched.
  type: str
  returned: when single entity
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"

total_available_results:
  description: The total number of available Volume Disks when listing.
  type: int
  returned: when listing Volume Disks
  sample: 3

changed:
  description: Always False for info modules.
  returned: always
  type: bool
  sample: false

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Volume Disk info using ext_id"

error:
  description: The error message if any.
  type: str
  returned: When an error occurs
  sample: "Api Exception raised while fetching Volume Disk info"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        volume_group_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_volume_disk(module, result, api_instance):
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
            msg="Api Exception raised while fetching Volume Disk info using ext_id",
        )

    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_volume_disks(module, result, api_instance):
    volume_group_ext_id = module.params.get("volume_group_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Volume Disks info spec", **result)

    try:
        resp = api_instance.get_volume_disks(
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
    result["volume_group_ext_id"] = volume_group_ext_id
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
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_volume_disk(module, result, api_instance)
    else:
        get_volume_disks(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
