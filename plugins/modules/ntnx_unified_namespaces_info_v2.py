#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_unified_namespaces_info_v2
short_description: Fetch Files Unified Namespace info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about UnifiedNamespace in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific UnifiedNamespace.
  - If C(ext_id) is not provided, list multiple UnifiedNamespace optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get Unified Namespace by ext_id) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
  - >-
    B(Get list of Unified Namespaces) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external ID of the Unified Namespace.
      - If provided, only the specific Unified Namespace matching this external ID is returned.
    type: str
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
- name: Get Unified Namespace using ext_id
  nutanix.ncp.ntnx_unified_namespaces_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"
  register: result
  ignore_errors: true

- name: List all Unified Namespaces
  nutanix.ncp.ntnx_unified_namespaces_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Unified Namespaces with filter on namespaceMemberConfigs
  nutanix.ncp.ntnx_unified_namespaces_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "namespaceMemberConfigs/any(m:m/fileServerType eq Nutanix.Files.Config.FileServerType'NUTANIX')"
  register: result
  ignore_errors: true

- name: List Unified Namespaces with limit
  nutanix.ncp.ntnx_unified_namespaces_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC UnifiedNamespace info v4 API.
    - It can be a single UnifiedNamespace if external ID is provided.
    - List of multiple UnifiedNamespace if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "9c1e537d-6777-4c22-5d41-ddd0c3337aa9",
      "namespace_member_configs": [
        {
          "file_server_ext_id": "11111111-1111-1111-1111-111111111111",
          "is_core_member": true,
          "file_server_type": "NUTANIX",
          "should_include_all_mount_targets": true
        }
      ],
      "created_timestamp_usecs": null,
      "modified_timestamp_usecs": null,
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching unified namespaces info"

error:
  description:
    - This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Unified Namespace.
  type: str
  returned: When external ID is provided
  sample: "9c1e537d-6777-4c22-5d41-ddd0c3337aa9"

total_available_results:
  description: The total number of available Unified Namespaces in PC.
  type: int
  returned: When all Unified Namespaces are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_unified_namespaces_api_instance,
)
from ..module_utils.v4.files.helpers import get_unified_namespace  # noqa: E402
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


def get_unified_namespace_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_unified_namespace(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_unified_namespaces(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating unified namespaces info spec", **result)

    try:
        resp = api_instance.list_unified_namespaces(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching unified namespaces info",
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
            ("ext_id", "page"),
            ("ext_id", "limit"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_unified_namespaces_api_instance(module)
    if module.params.get("ext_id"):
        get_unified_namespace_using_ext_id(module, api_instance, result)
    else:
        get_unified_namespaces(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
