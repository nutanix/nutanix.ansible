#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_category_associations_by_volume_group_ids_info_v2
short_description: List categories associated with a Volume Group in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about CategoryAssociationsByVolumeGroupId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific CategoryAssociationsByVolumeGroupId.
  - If C(ext_id) is not provided, list multiple CategoryAssociationsByVolumeGroupId optionally filtered / paginated.
  - The underlying SDK API is deprecated but still functional; see the note below.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List category associations for a Volume Group) -
    Required Roles: Backup Admin, CSI System, Kubernetes Data Services System, Prism Admin, Prism Viewer,
    Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group whose category associations should be listed.
      - This is required to invoke the list-category-associations-by-volume-group-id API.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of a specific associated category to fetch from the list.
      - When provided, the module lists all category associations for the Volume Group and returns the entry whose
        external identifier matches this value.
      - The v4 volumes API does not offer a dedicated get-by-id endpoint for a single category association.
    type: str
    required: false
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
      - Must be a positive integer between 0 and the maximum number of pages available for the resource.
    type: int
    required: false
  limit:
    description:
      - A URL query parameter that specifies the total number of records returned in the result set.
      - Must be a positive integer between 1 and 100. Defaults to 50 when not provided.
    type: int
    required: false
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
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all category associations for a Volume Group
  nutanix.ncp.ntnx_category_associations_by_volume_group_ids_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
  register: result

- name: List category associations for a Volume Group with pagination
  nutanix.ncp.ntnx_category_associations_by_volume_group_ids_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    page: 0
    limit: 25
  register: result

- name: Fetch a specific associated category by ext_id
  nutanix.ncp.ntnx_category_associations_by_volume_group_ids_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC CategoryAssociationsByVolumeGroupId info v4 API.
    - It can be a single CategoryAssociationsByVolumeGroupId if external ID is provided.
    - List of multiple CategoryAssociationsByVolumeGroupId if external ID is not provided
      (pagination via C(page)/C(limit) is supported by the API).
  returned: always
  type: dict
  sample:
    [
      {
        "entity_type": "CATEGORY",
        "ext_id": "f67f4fd0-dbd0-432b-7b71-58002c9f2d1f",
        "name": null,
        "uris": null
      },
      {
        "entity_type": "CATEGORY",
        "ext_id": "e72b4777-aadc-46d0-4659-3367e33e6720",
        "name": null,
        "uris": null
      }
    ]

total_available_results:
  description: The total number of category associations available in the API for the Volume Group.
  type: int
  returned: when the list API returns metadata with total_available_results
  sample: 2

ext_id:
  description: The external identifier of the specific associated category requested via C(ext_id).
  type: str
  returned: when C(ext_id) is provided
  sample: "f67f4fd0-dbd0-432b-7b71-58002c9f2d1f"

volume_group_ext_id:
  description: The external identifier of the Volume Group whose category associations were fetched.
  type: str
  returned: always
  sample: "a6165ec0-8936-405d-67bc-cc04c05e5622"

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or the entity could not be found
  type: str
  sample: "Api Exception raised while listing category associations for Volume Group"

error:
  description: This field typically holds information about the error that occurred during the task execution.
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
        page=dict(type="int", required=False),
        limit=dict(type="int", required=False),
    )

    return module_args


def _list_all_category_associations(module, api_instance, volume_group_ext_id):
    """List category associations for a Volume Group honouring page/limit."""
    kwargs = {}
    if module.params.get("page") is not None:
        kwargs["_page"] = module.params.get("page")
    if module.params.get("limit") is not None:
        kwargs["_limit"] = module.params.get("limit")
    try:
        return api_instance.list_category_associations_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing category associations for Volume Group",
        )


def get_category_association_using_ext_id(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = ext_id

    resp = _list_all_category_associations(module, api_instance, volume_group_ext_id)
    resp_dict = strip_internal_attributes(resp.to_dict())
    data = resp_dict.get("data") or []
    match = None
    for item in data:
        if item.get("ext_id") == ext_id:
            match = item
            break
    if not match:
        module.fail_json(
            msg=(
                "Category association with ext_id '{0}' was not found for Volume Group "
                "'{1}'."
            ).format(ext_id, volume_group_ext_id),
            **result,
        )
    result["response"] = match


def get_category_associations(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    resp = _list_all_category_associations(module, api_instance, volume_group_ext_id)
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
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_category_association_using_ext_id(module, api_instance, result)
    else:
        get_category_associations(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
