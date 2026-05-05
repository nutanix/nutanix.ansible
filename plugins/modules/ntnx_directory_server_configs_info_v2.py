#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_directory_server_configs_info_v2
short_description: Get directory server configs info
version_added: 2.6.0
description:
    - Fetch specific directory server config info using external ID
    - Fetch list of all directory server configs if external ID is not provided
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get directory server config by ext_id) -
      Operation Name: View Directory Server Config -
      Required Roles: Flow Admin, Flow Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List all the Directory Servers) -
      Operation Name: View Directory Server Config -
      Required Roles: Flow Admin, Flow Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=microseg)"
options:
    ext_id:
        description:
            - External ID to fetch specific directory server config info
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
- name: List all directory server configs
  nutanix.ncp.ntnx_directory_server_configs_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: Get directory server config using ext_id
  nutanix.ncp.ntnx_directory_server_configs_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    ext_id: "b215708c-252f-400c-bc90-2f36242d3d3c"
  register: result
"""

RETURN = r"""
response:
  description:
      - Response for fetching directory server configs info
      - One directory server config info if External ID is provided
      - List of multiple directory server configs info if External ID is not provided
  returned: always
  type: dict
  sample:
    {
        "directory_service_reference": "00062ffc-95ad-19e9-185b-ac1f6b6f97a3",
        "domain_controllers": null,
        "ext_id": "b215708c-252f-400c-bc90-2f36242d3d3c",
        "is_default_category_enabled": true,
        "links": null,
        "matching_criterias": [
            {
                "criteria": "test",
                "match_entity": "VM",
                "match_field": "NAME",
                "match_type": "CONTAINS"
            }
        ],
        "should_keep_default_category_on_login": false,
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

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
    sample: "Api Exception raised while fetching directory server configs info"

ext_id:
    description: The external ID of the directory server config
    returned: when ext_id is provided
    type: str
    sample: "b215708c-252f-400c-bc90-2f36242d3d3c"

total_available_results:
    description: The total number of available directory server configs in PC.
    type: int
    returned: when all directory server configs are fetched
    sample: 5
"""
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_directory_server_configs_api_instance,
)
from ..module_utils.v4.flow.helpers import get_directory_server_config  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_directory_server_config_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_directory_server_config(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_directory_server_configs(module, api_instance, result):

    kwargs = {}
    if module.params.get("select"):
        kwargs["_select"] = module.params["select"]

    try:
        resp = api_instance.list_directory_server_configs(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching directory server configs info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_directory_server_configs_api_instance(module)
    if module.params.get("ext_id"):
        get_directory_server_config_using_ext_id(module, api_instance, result)
    else:
        get_directory_server_configs(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
