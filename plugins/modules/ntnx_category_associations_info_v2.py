#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_category_associations_info_v2
short_description: Fetch categories associated with a Volume Group in Nutanix Prism Central.
version_added: 2.5.0
description:
  - This module allows you to fetch information about CategoryAssociation in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific CategoryAssociation.
  - If C(ext_id) is not provided, list multiple CategoryAssociation optionally filtered / paginated.
  - The C(volume_group_ext_id) parameter is required in every invocation - category
    associations always belong to a specific Volume Group in the storage namespace.
  - This module uses PC v4 APIs based SDKs (ntnx_storage_py_client).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(List category associations for a Volume Group) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin,
    Storage Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  volume_group_ext_id:
    description:
      - The external identifier of the Volume Group whose category associations should be listed.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of a specific associated Category.
      - When provided, only that category association is returned (filtered client-side)
        because the storage v4 API only exposes list semantics for category associations.
    type: str
    required: false
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
- name: List all categories associated with a Volume Group
  nutanix.ncp.ntnx_category_associations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
  register: result

- name: Get a specific category associated with a Volume Group
  nutanix.ncp.ntnx_category_associations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result

- name: List categories associated with a Volume Group with limit
  nutanix.ncp.ntnx_category_associations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    volume_group_ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC CategoryAssociation info v4 API.
    - It can be a single CategoryAssociation entry if external ID is provided.
    - It can be a list of multiple CategoryAssociation entries if external ID is not
      provided with an optional page/limit.
  returned: always
  type: dict
  sample:
    [
      {
        "entity_type": "CATEGORY",
        "ext_id": "566b844b-d245-4894-a8b5-eeef1ec4b638",
        "name": "AppFamily/Databases",
        "uris": [
          "/api/prism/v4.0/config/categories/566b844b-d245-4894-a8b5-eeef1ec4b638"
        ]
      }
    ]

total_available_results:
  description: Total number of category associations available for the Volume Group.
  type: int
  returned: when listing (no C(ext_id) provided)
  sample: 2

ext_id:
  description:
    - External ID of the Category whose association was fetched.
  type: str
  returned: when C(ext_id) is provided
  sample: "566b844b-d245-4894-a8b5-eeef1ec4b638"

changed:
  description: Always False for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Human readable status/error message.
  returned: contextual
  type: str
  sample: "Api Exception raised while fetching category associations for Volume Group"

error:
  description: Error details, if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )
    return module_args


def _fetch_category_associations(module, api_instance, kwargs):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    try:
        return api_instance.get_category_associations(
            extId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching category associations for Volume Group",
        )


def get_category_association_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = _fetch_category_associations(module, api_instance, {"_limit": 100})
    resp = strip_internal_attributes(resp.to_dict())
    data = resp.get("data") or []
    match = next((item for item in data if item.get("ext_id") == ext_id), None)
    if not match:
        module.fail_json(
            msg="Category with ext_id '{0}' is not associated with Volume Group '{1}'".format(
                ext_id, module.params.get("volume_group_ext_id")
            ),
            failed=True,
        )
    result["ext_id"] = ext_id
    result["response"] = match


def get_category_associations(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating category associations info spec", **result
        )

    resp = _fetch_category_associations(module, api_instance, kwargs)
    resp = strip_internal_attributes(resp.to_dict())
    metadata = resp.get("metadata") or {}
    result["total_available_results"] = metadata.get("total_available_results")
    data = resp.get("data")
    if not data:
        data = []
    result["response"] = data


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
        get_category_associations(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
