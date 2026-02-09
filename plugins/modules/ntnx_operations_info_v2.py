#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_operations_info_v2
short_description: Module to fetch IAM operations info (previously `permissions`)
version_added: 2.0.0
description:
    - This module is used to get operations info
    - It can be used to get all operations info or specific permission info using external id
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - Permission external id
        type: str

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all operations
  nutanix.ncp.ntnx_operations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch permission info using external id
  nutanix.ncp.ntnx_operations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ permission_ext_id }}"
  register: result

- name: List operations using filter criteria
  nutanix.ncp.ntnx_operations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "displayName eq 'Display_Name_Test'"
"""
RETURN = r"""
response:
    description:
        - Response for fetching permissions info
        - Response will have list or single operation info as per the spec provided
    type: dict
    returned: always
    sample:
        {
                    "associated_endpoint_list": [
                        {
                            "api_version": "V4",
                            "endpoint_url": "/config/file-servers/{extId}/$actions/search-user-mapping",
                            "http_method": "POST"
                        }
                    ],
                    "client_name": "FilesManagerService",
                    "created_time": "2024-05-28T09:24:56.559305+00:00",
                    "description": "Allows to search file server user mapping",
                    "display_name": "Search_File_Server_User_Mapping",
                    "entity_type": "files",
                    "ext_id": "251d4a4f-244f-4c84-70a9-8c8f68f9dff0",
                    "last_updated_time": "2024-05-28T09:25:09.249611+00:00",
                    "links": null,
                    "operation_type": "EXTERNAL",
                    "related_operation_list": [
                        "ad8a998d-06ca-404e-5e15-e91e2de3a783"
                    ],
                    "tenant_id": null
                }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching permission info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
total_available_results:
    description:
        - The total number of available operations in PC.
    type: int
    returned: when all operations are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_permission_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_permission  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
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


def get_operation_by_ext_id(module, operations, result):
    ext_id = module.params.get("ext_id")
    resp = get_permission(module, operations, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_operations(module, operations, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating operations info Spec", **result)

    try:
        resp = operations.list_operations(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching permission info",
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
    operations = get_permission_api_instance(module)
    if module.params.get("ext_id"):
        get_operation_by_ext_id(module, operations, result)
    else:
        get_operations(module, operations, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
