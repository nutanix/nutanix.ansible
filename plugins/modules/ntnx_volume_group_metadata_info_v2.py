#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_metadata_info_v2
short_description: Fetch Volume Group Metadata Info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VolumeGroupMetadataInfo in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VolumeGroupMetadataInfo.
  - The underlying storage v4 API only supports fetching metadata info for a
    given Volume Group's external identifier, so this info module always
    requires C(ext_id) and returns a single dict rather than a list.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Volume Group Metadata Info by ext_id) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Project Manager,
      Storage Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external identifier of the Volume Group whose metadata information
        is to be fetched.
      - Required for this info module.
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
- name: Fetch Volume Group Metadata Info by Volume Group ext_id
  nutanix.ncp.ntnx_volume_group_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VolumeGroupMetadataInfo info v4 API.
    - It is a single VolumeGroupMetadataInfo dict for the requested Volume Group
      external identifier (the underlying storage v4 API does not expose a
      list-all operation for this sub-resource).
  returned: always
  type: dict
  sample:
    {
      "category_ids": [
        "566b844b-d245-4894-a8b5-eeef1ec4b638"
      ],
      "owner_reference_id": "00000000-0000-0000-0000-000000000000",
      "owner_user_name": "admin",
      "project_name": "ansible-project",
      "project_reference_id": "11111111-1111-1111-1111-111111111111"
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
  sample: "Api Exception raised while fetching Volume Group Metadata Info using ext_id"

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
  description: External ID of the Volume Group whose metadata info was fetched.
  type: str
  returned: when external ID is provided
  sample: "68e4c68e-1acf-4c05-7792-e062119acb68"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.storage.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.storage.helpers import (  # noqa: E402
    get_volume_group_metadata_info,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_volume_group_metadata_info_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_volume_group_metadata_info(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    data = resp.data.to_dict() if resp is not None and resp.data is not None else {}
    result["response"] = strip_internal_attributes(data)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vg_api_instance(module)
    get_volume_group_metadata_info_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
