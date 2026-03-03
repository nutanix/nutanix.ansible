#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_categories_info_v2
short_description: Nutanix PC categories info module
version_added: 2.0.0
description:
    - Get categories info
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - category UUID
        type: str
    expand:
        description:
            - Additional query param to expand the response with more details
            - detailedAssociations is supported only when ext_id is provided
        type: str
        choices: ['associations', 'detailedAssociations']
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: list all categories
  nutanix.ncp.ntnx_categories_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>

- name: List all categories with keyname & expand associations
  nutanix.ncp.ntnx_categories_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    expand: associations
    filter: "key eq '{{category_name}}'"
"""
RETURN = r"""
response:
  description:
    - By default, List of category key values.
    - If ext_id is provided then it will have dictionary consisting category key value info.
  type: dict
  returned: always
  sample:
    {
                "associations": [
                    {
                        "category_id": null,
                        "count": 18,
                        "resource_group": "ENTITY",
                        "resource_type": "VM"
                    }
                ],
                "description": "Created by CALM",
                "detailed_associations": null,
                "ext_id": "cc16efb4-6591-4b89-a643-8c835f035393",
                "key": "OSType",
                "links": [
                    {
                        "href": "https://00.00.00.00:9440/api/prism/v4.0.b1/config/categories/cc16efb4-6591-4b89-a643-8c835f035393",
                        "rel": "self"
                    }
                ],
                "owner_uuid": null,
                "tenant_id": null,
                "type": "USER",
                "value": "Linux"
            }
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching categories info"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
ext_id:
    description:
        - The external ID of the category if given in input.
    type: str
    returned: always
    sample: "dded1b87-e566-419a-aac0-fb282792fb83"
total_available_results:
    description:
        - The total number of available categories in PC.
    type: int
    returned: when all categories are fetched
    sample: 125
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import get_pc_api_client  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str", choices=["associations", "detailedAssociations"]),
    )

    return module_args


def get_category_api_instance(module):
    api_client = get_pc_api_client(module)
    return prism_sdk.CategoriesApi(api_client=api_client)


def get_category(module, result):
    categories = get_category_api_instance(module)
    ext_id = module.params.get("ext_id")
    expand = module.params.get("expand")

    try:
        resp = categories.get_category_by_id(ext_id, expand)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching category info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_categories(module, result):
    categories = get_category_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating categories info Spec", **result)

    try:
        resp = categories.list_categories(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching categories info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_category(module, result)
    else:
        get_categories(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
