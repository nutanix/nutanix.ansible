#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_volume_groups_disks_info_v2
short_description: Fetch information about Nutanix PC Volume group disks.
description:
  - This module fetches information about Nutanix PC Volume groups disks.
  - The module can fetch information about all Volume groups or a specific Volume group disk.
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of the Volume Group disk.
        type: str
        required: false
    volume_group_ext_id:
        description:
            - The external ID of the Volume Group.
        type: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch information about all Disks of VG
  nutanix.ncp.ntnx_volume_groups_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    volume_group_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653
    validate_certs: false

- name: Fetch information about all Disks of VG using page and limits
  nutanix.ncp.ntnx_volume_groups_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    volume_group_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653
    page: 1
    limit: 50
    validate_certs: false

- name: Fetch information about a specific VG Disk
  nutanix.ncp.ntnx_volume_groups_disks_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1654
    volume_group_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653
"""

RETURN = r"""
response:
    description:
        - List of disks if C(ext_id) is not provided.
        - Specific disk details if C(ext_id) is provided. Below example is of same case.
    type: dict
    returned: always
    sample: {
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
    description: Disk external ID. When C(ext_id) is provided.
    type: str
    returned: When c(wait) if true
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Api Exception raised while fetching volume group disk info"
"""


from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        volume_group_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_vg_disk(module, result):
    vgs = get_vg_api_instance(module)
    ext_id = module.params.get("ext_id")
    volume_group_ext_id = module.params.get("volume_group_ext_id")

    try:
        resp = vgs.get_volume_disk_by_id(
            extId=ext_id, volumeGroupExtId=volume_group_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume group disk info",
        )

    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vg_disks(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("volume_group_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume group disks info Spec", **result)

    try:
        resp = vgs.list_volume_disks_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume group disks info",
        )

    result["volume_group_ext_id"] = volume_group_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    if not result["response"]:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_vg_disk(module, result)
    else:
        get_vg_disks(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
