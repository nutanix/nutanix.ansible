#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_metadata_info_v2
short_description: Fetch VolumeGroupMetadata for a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VolumeGroupMetadata in Nutanix Prism Central.
  - The metadata contains the C(owner_reference) and C(category_ids) of a Volume Group.
  - It wraps the Nutanix Volumes v4 API C(GetVolumeGroupMetadataById)
    (URI C(/api/volumes/v4.2/config/volume-groups/{volumeGroupExtId}/metadata)) which is
    marked B(deprecated) upstream. Newer clients should prefer
    C(ntnx_volume_groups_info_v2) using C(GetVolumeGroupById) with the
    C($expand=metadata) OData query, but this module remains supported for
    backwards compatibility.
  - VolumeGroupMetadata does not have its own external ID; it is a singleton subresource
    of a Volume Group and is addressed by the parent Volume Group's external ID.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation. The required roles depend on the operation being performed.
    - >-
      B(Get Volume Group metadata by Volume Group ID) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer,
      Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager, Storage Admin,
      Storage Viewer, Super Admin, Self-Service Admin (deprecated).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  volume_group_ext_id:
    description:
      - The external ID of the parent Volume Group whose metadata should be fetched.
      - This is required because VolumeGroupMetadata is a singleton subresource of a Volume Group.
    type: str
    required: true
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch VolumeGroupMetadata using the parent Volume Group external ID
  nutanix.ncp.ntnx_volume_group_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
  register: metadata_result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VolumeGroupMetadata info v4 API.
    - Metadata of a Volume Group. The exact fields returned depend on the AOS/PC
      version but typically include C(category_ids), C(owner_reference_id),
      C(owner_user_name), C(project_reference_id) and C(project_name).
    - The endpoint returns a single VolumeGroupMetadata object (there is no list variant
      for this deprecated subresource endpoint).
    - C(category_ids) may be returned as C(null) when no categories are attached.
  returned: always
  type: dict
  sample:
    {
        "category_ids": null,
        "owner_reference_id": "00000000-0000-0000-0000-000000000000",
        "owner_user_name": null,
        "project_name": null,
        "project_reference_id": null
    }

volume_group_ext_id:
  description: The external ID of the parent Volume Group whose metadata was fetched.
  returned: always
  type: str
  sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Volume Group metadata for volume_group_ext_id=<uuid>"

error:
  description: This field typically holds information about errors that occurred during the task execution.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.volumes.helpers import get_volume_group_metadata  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
    )
    return module_args


def _get_volume_group_metadata(module, api_instance, result):
    """Fetch the VolumeGroupMetadata singleton for a Volume Group."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    resp = get_volume_group_metadata(module, api_instance, volume_group_ext_id)
    response = strip_internal_attributes(resp.to_dict()) if resp is not None else None
    result["response"] = response


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "volume_group_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    _get_volume_group_metadata(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
