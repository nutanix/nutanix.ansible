#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_vm_attachment_info_v2
short_description: Fetch VmAttachmentsByVolumeGroupId info in Nutanix Prism Central.
version_added: 2.7.0
description:
  - This module allows you to fetch information about VmAttachmentsByVolumeGroupId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmAttachmentsByVolumeGroupId.
  - If C(ext_id) is not provided, list multiple VmAttachmentsByVolumeGroupId optionally filtered / paginated.
  - Uses the V4 C(ListVmAttachmentsByVolumeGroupId) API on C(VolumeGroupsApi).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(List VM attachments by Volume Group) -
    Required Roles: Backup Admin, Prism Admin, Prism Viewer, Project Manager, Storage Admin, Storage Viewer,
    Super Admin, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer,
    Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group whose VM attachments should be listed.
      - Required for both single and list operations because the API is scoped to a parent Volume Group.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier (VM ext_id) of a specific VmAttachment on the Volume Group.
      - When provided the module filters the underlying list response and returns only the
        matching VmAttachment; when omitted the full list is returned.
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
- name: List all VM attachments for a Volume Group
  nutanix.ncp.ntnx_volume_group_vm_attachment_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
  register: result

- name: List VM attachments with a limit
  nutanix.ncp.ntnx_volume_group_vm_attachment_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    limit: 5
  register: result

- name: Fetch a specific VM attachment on a Volume Group
  nutanix.ncp.ntnx_volume_group_vm_attachment_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4a5d"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmAttachmentsByVolumeGroupId info v4 API.
    - It can be a single VmAttachmentsByVolumeGroupId if external ID is provided.
    - List of multiple VmAttachmentsByVolumeGroupId if external ID is not provided
      with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "16f04294-2b2b-4b2b-7b34-9cb81195f92c",
        "index": null
      }
    ]

ext_id:
  description: External ID of the specific VmAttachment on the Volume Group.
  type: str
  returned: when C(ext_id) is provided
  sample: "16f04294-2b2b-4b2b-7b34-9cb81195f92c"

volume_group_ext_id:
  description: External ID of the parent Volume Group.
  type: str
  returned: always
  sample: "2b18feee-4502-4f73-4fa7-1216446cf8e5"

total_available_results:
  description: The total number of VmAttachment records available for the Volume Group.
  type: int
  returned: when listing all VM attachments
  sample: 1

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM attachments for volume group"

error:
  description: The error message if any error occurred.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed.
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
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def _list_vm_attachments(module, api_instance, kwargs):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    try:
        return api_instance.list_vm_attachments_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM attachments for volume group",
        )


def get_vm_attachment_by_ext_id(module, api_instance, result):
    """Return the single VmAttachment matching module.params['ext_id']."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = ext_id

    resp = _list_vm_attachments(module, api_instance, kwargs={})
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    attachments = strip_internal_attributes(resp.to_dict()).get("data") or []
    matched = next((item for item in attachments if item.get("ext_id") == ext_id), None)
    if matched is None:
        module.fail_json(
            msg=(
                "VmAttachment with ext_id: {0} was not found on Volume Group "
                "ext_id: {1}."
            ).format(ext_id, volume_group_ext_id),
            **result,
        )
    result["response"] = matched


def list_vm_attachments(module, api_instance, result):
    """List every VmAttachment for the given Volume Group, honouring filters."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM attachments info spec", **result)
    kwargs.pop("volumeGroupExtId", None)

    resp = _list_vm_attachments(module, api_instance, kwargs=kwargs)
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


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
        get_vm_attachment_by_ext_id(module, api_instance, result)
    else:
        list_vm_attachments(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
