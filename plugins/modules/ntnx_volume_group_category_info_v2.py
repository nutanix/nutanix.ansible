#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_category_info_v2
short_description: Fetch the categories associated with a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about CategoryAssociationsByVolumeGroupId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific CategoryAssociationsByVolumeGroupId.
  - If C(ext_id) is not provided, list multiple CategoryAssociationsByVolumeGroupId optionally paginated using C(page) and C(limit).
  - The underlying List Category Associations By Volume Group Id v4 API is deprecated on newer PC releases; use the
    C(ntnx_volume_groups_info_v2) module with expand=metadata instead to get category IDs.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List Category Associations by Volume Group Id) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin,
      Prism Viewer, Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    volume_group_ext_id:
        description:
            - The external identifier of the Volume Group whose category associations are to be fetched.
        required: true
        type: str
    ext_id:
        description:
            - The external identifier of a specific category association to fetch.
            - When provided, the module attempts to return the matching category association from the list.
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
- name: List all categories associated with a Volume Group
  nutanix.ncp.ntnx_volume_group_category_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
  register: result

- name: Fetch a specific category association for a Volume Group by ext_id
  nutanix.ncp.ntnx_volume_group_category_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result

- name: List category associations with pagination (limit)
  nutanix.ncp.ntnx_volume_group_category_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    limit: 1
  register: result

- name: List category associations with pagination (page)
  nutanix.ncp.ntnx_volume_group_category_info_v2:
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    page: 0
    limit: 10
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC CategoryAssociationsByVolumeGroupId info v4 API.
        - It can be a single CategoryAssociationsByVolumeGroupId if external ID is provided.
        - List of multiple CategoryAssociationsByVolumeGroupId if external ID is not provided with optional limit.
    returned: always
    type: dict
    sample:
        [
            {
                "entity_type": "CATEGORY",
                "ext_id": "566b844b-d245-4894-a8b5-eeef1ec4b638",
                "name": "OSType/Linux",
                "uris": null
            }
        ]

ext_id:
    description:
        - The external identifier of the specific category association fetched, if provided.
    returned: when ext_id is provided
    type: str
    sample: "566b844b-d245-4894-a8b5-eeef1ec4b638"

volume_group_ext_id:
    description:
        - The external identifier of the Volume Group for which category associations are fetched.
    returned: always
    type: str
    sample: "68e4c68e-1acf-4c05-7792-e062119acb68"

total_available_results:
    description:
        - The total number of available category associations for the Volume Group in PC.
    returned: when a list is fetched
    type: int
    sample: 3

changed:
    description: Always false for info modules.
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching category associations for Volume Group"

error:
    description: This field typically holds information about any errors that occurred while fetching info.
    returned: when an error occurs
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
    """Return the Ansible argument spec for the info module."""
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def _fetch_category_associations(module, api_instance, volume_group_ext_id):
    """Call the SDK to list category associations for the given Volume Group.

    Returns the raw SDK response object. The caller is responsible for
    stripping internal attributes and shaping the response.
    """
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
            msg="Api Exception raised while fetching category associations for Volume Group",
        )


def get_category_association_by_ext_id(module, api_instance, result):
    """Fetch the categories associated with a Volume Group and filter by category ext_id."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    resp = _fetch_category_associations(module, api_instance, volume_group_ext_id)

    data = strip_internal_attributes(resp.to_dict()).get("data") or []
    matched = None
    for entry in data:
        if entry.get("ext_id") == ext_id:
            matched = entry
            break
    if matched is None:
        module.fail_json(
            msg=(
                "Category association with ext_id '{0}' was not found on "
                "Volume Group '{1}'.".format(ext_id, volume_group_ext_id)
            ),
            **result,
        )
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id
    result["response"] = matched


def list_category_associations(module, api_instance, result):
    """List all categories associated with a Volume Group."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    resp = _fetch_category_associations(module, api_instance, volume_group_ext_id)

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
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_category_association_by_ext_id(module, api_instance, result)
    else:
        list_category_associations(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
