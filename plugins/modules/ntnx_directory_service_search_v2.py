#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_directory_service_search_v2
short_description: Search users and groups in a directory service in Nutanix PC.
version_added: "2.6.0"
description:
    - This module is used to search a user or group in a directory service in Nutanix PC.
    - The directory service to search in is identified by its external ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Search user/group in directory service) -
      Required Roles: Flow Admin, Flow Viewer, Nutanix Central Admin, Prism Admin,
      Project Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will search a user or group in the directory service.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID of the directory service to search in.
        type: str
        required: true
    query:
        description:
            - The string to search for in the directory service.
        type: str
        required: true
    searched_attributes:
        description:
            - Attributes for search operation. By default, the search will be performed with a common name.
        type: list
        elements: str
    returned_attributes:
        description:
            - Attributes returned by the search operation.
        type: list
        elements: str
    is_wildcard_search:
        description:
            - Flag indicating whether the search should be a wildcard search or not.
        type: bool
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Search directory service for a group
  nutanix.ncp.ntnx_directory_service_search_v2:
    ext_id: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
    query: "test_query"
    searched_attributes:
      - name
      - sAMAccountName
      - cn
    returned_attributes:
      - name
      - objectGUID
  register: ad_object_search_result
"""

RETURN = r"""
response:
    description:
        - Response for searching users and groups in the directory service.
        - Contains the search results.
    type: dict
    returned: always
    sample:
        {
            "domain_name": "systest.nutanix.com",
            "search_results": [
                {
                    "attributes": [
                        {
                            "name": "member",
                            "values": [
                                "test_cac_98@systest.nutanix.com"
                            ]
                        },
                        {
                            "name": "memberDN",
                            "values": [
                                "CN=test_cac_98,OU=cac_ou,DC=systest,DC=nutanix,DC=com"
                            ]
                        },
                        {
                            "name": "memberSAM",
                            "values": [
                                "test_cac_98"
                            ]
                        },
                        {
                            "name": "name",
                            "values": [
                                "test_cac_g98"
                            ]
                        },
                        {
                            "name": "objectGUID",
                            "values": [
                                "9316163d-6a31-9542-bb71-3f2105d840d6"
                            ]
                        },
                        {
                            "name": "objectCategory",
                            "values": [
                                "CN=Group,CN=Schema,CN=Configuration,DC=systest,DC=nutanix,DC=com"
                            ]
                        }
                    ],
                    "entity_type": "Group",
                    "name": "CN=test_cac_g98,OU=cac_ou,DC=systest,DC=nutanix,DC=com"
                }
            ]
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
    description: This field indicates if the task execution failed
    returned: always
    type: bool
    sample: false

ext_id:
  description: External ID of the directory service that was searched.
  returned: always
  type: str
  sample: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_directory_service_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        query=dict(type="str", required=True),
        searched_attributes=dict(type="list", elements="str"),
        returned_attributes=dict(type="list", elements="str"),
        is_wildcard_search=dict(type="bool", default=True),
    )
    return module_args


def search_directory_service(module, directory_services, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = iam_sdk.DirectoryServiceSearchQuery()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating directory service search spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = directory_services.search_directory_service(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while searching directory service",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "ext_id": None,
    }
    directory_services = get_directory_service_api_instance(module)
    search_directory_service(module, directory_services, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
