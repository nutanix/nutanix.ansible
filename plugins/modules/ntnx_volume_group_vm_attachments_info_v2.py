#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_vm_attachments_info_v2
short_description: Fetch VmAttachment info for a Volume Group in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmAttachment in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmAttachment for the Volume Group.
  - If C(ext_id) is not provided, list multiple VmAttachment optionally paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(List VM attachments of a Volume Group) -
    Required Roles: Backup Admin, Consumer, Developer, Operator, Prism Admin, Prism Viewer,
    Project Manager, Storage Admin, Super Admin, Virtual Machine Admin,
    Virtual Machine Viewer, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group whose VM attachments are being fetched.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the specific VmAttachment (VM ext_id) to fetch.
      - If not provided, the module lists all VM attachments for the Volume Group.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get a specific VmAttachment by VM ext_id
  nutanix.ncp.ntnx_volume_group_vm_attachments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
    ext_id: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
  register: single_result

- name: List all VmAttachments of a Volume Group
  nutanix.ncp.ntnx_volume_group_vm_attachments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
  register: list_result

- name: List VmAttachments of a Volume Group with limit
  nutanix.ncp.ntnx_volume_group_vm_attachments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
    limit: 5
  register: limited_result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmAttachment info v4 API.
    - It can be a single VmAttachment if external ID is provided.
    - List of multiple VmAttachment if external ID is not provided with optional limit.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7",
        "index": 1,
        "links": null,
        "tenant_id": null
      }
    ]
volume_group_ext_id:
  description: External ID of the Volume Group whose VM attachments were fetched.
  type: str
  returned: always
  sample: "d4a91ba0-2af7-4b40-91a4-4b40deadbeef"
ext_id:
  description: External ID of the VmAttachment (VM ext_id) when a single VmAttachment was requested.
  type: str
  returned: when a single VmAttachment is requested
  sample: "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
total_available_results:
  description: The total number of VmAttachments available for the Volume Group.
  type: int
  returned: when listing VM attachments
  sample: 2
changed:
  description: Always false for info modules.
  type: bool
  returned: always
  sample: false
failed:
  description: True on failure.
  type: bool
  returned: always
  sample: false
msg:
  description: Status/error message.
  type: str
  returned: contextual
  sample: "VmAttachment for VM 'ac5aff0c-6c68-4948-9088-b903e2be0ce7' not found in Volume Group 'd4a91ba0-...-4b40deadbeef'."
error:
  description: The error message if any.
  type: str
  returned: when an error occurs
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.storage.helpers import find_vm_attachment  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_vm_attachment_by_ext_id(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    vm_ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = vm_ext_id

    attachment = find_vm_attachment(
        module, api_instance, volume_group_ext_id, vm_ext_id
    )
    if attachment is None:
        module.fail_json(
            msg=(
                "VmAttachment for VM '{0}' not found in Volume Group '{1}'.".format(
                    vm_ext_id, volume_group_ext_id
                )
            ),
            **result,
        )

    result["response"] = strip_internal_attributes(attachment.to_dict())


def list_vm_attachments(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VmAttachment info spec", **result)

    # Only page and limit are supported for the get_vm_attachments API.
    kwargs = {k: v for k, v in kwargs.items() if k in ("_page", "_limit")}

    try:
        resp = api_instance.get_vm_attachments(extId=volume_group_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM attachments for Volume Group",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
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
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "volume_group_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_attachment_by_ext_id(module, api_instance, result)
    else:
        list_vm_attachments(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
