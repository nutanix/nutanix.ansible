#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_category_mappings_info_v2
short_description: Get DS category mappings info
version_added: 2.6.0
description:
    - Fetch specific DS category mapping info using external ID
    - Fetch list of multiple DS category mappings info if external ID is not provided with optional filters
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get DS category mapping by ext_id) -
      Operation Name: View Category Mapping -
      Required Roles: Flow Admin, Flow Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List DS Category Mappings) -
      Operation Name: View Category Mapping -
      Required Roles: Flow Admin, Flow Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
    ext_id:
        description:
            - External ID to fetch specific DS category mapping info
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all DS category mappings
  nutanix.ncp.ntnx_category_mappings_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result
  ignore_errors: true

- name: List DS category mappings using filter
  nutanix.ncp.ntnx_category_mappings_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    filter: "name eq 'ansible-category-mapping'"
  register: result
  ignore_errors: true

- name: List DS category mappings using limit
  nutanix.ncp.ntnx_category_mappings_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: Get DS category mapping using ext_id
  nutanix.ncp.ntnx_category_mappings_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    ext_id: "b215708c-252f-400c-bc90-2f36242d3d3c"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - Response for fetching DS category mappings info
      - One DS category mapping info if External ID is provided
      - List of multiple DS category mappings info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
        "ad_info": {
            "directory_service_reference": "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a",
            "object_identifier": "S-1-5-21-123456789-123456789-123456789-1001",
            "object_path": "CN=TestGroup,DC=example,DC=com",
            "status": "USABLE"
        },
        "category_name": "AppType",
        "category_value": "Default",
        "ext_id": "b215708c-252f-400c-bc90-2f36242d3d3c",
        "links": null,
        "name": "ansible-category-mapping",
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching DS category mappings info"

ext_id:
  description: The DS category mapping ext_id
  returned: when ext_id is provided
  type: str
  sample: "b215708c-252f-400c-bc90-2f36242d3d3c"

total_available_results:
    description: The total number of available DS category mappings in PC.
    type: int
    returned: when all DS category mappings are fetched
    sample: 10
"""
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_directory_server_configs_api_instance,
)
from ..module_utils.v4.flow.helpers import get_ds_category_mapping  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_category_mapping_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_ds_category_mapping(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_category_mappings(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating DS category mappings info Spec", **result
        )

    try:
        resp = api_instance.list_category_mappings(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching DS category mappings info",
        )

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
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_directory_server_configs_api_instance(module)
    if module.params.get("ext_id"):
        get_category_mapping_using_ext_id(module, api_instance, result)
    else:
        get_category_mappings(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
