#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_ransomware_configs_info_v2
short_description: Fetch ransomware configuration info of a file server in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about RansomwareConfig in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific RansomwareConfig.
  - If C(ext_id) is not provided, list multiple RansomwareConfig optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs
notes:
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server on which the ransomware configurations are managed.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the ransomware configuration.
      - If provided, the specific ransomware configuration is fetched.
    type: str
    required: false
  filter:
    description:
      - The filter in OData syntax used to filter the results.
      - The filter can be applied on the C(fileExtensions) field.
    type: str
    required: false
  limit:
    description:
      - The maximum number of records to return in the result set.
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
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get ransomware config using ext_id
  nutanix.ncp.ntnx_files_ransomware_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
  register: result
  ignore_errors: true

- name: List all ransomware configs of a file server
  nutanix.ncp.ntnx_files_ransomware_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
  register: result
  ignore_errors: true

- name: List ransomware configs with filter
  nutanix.ncp.ntnx_files_ransomware_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    filter: "fileExtensions eq '*.crypto'"
  register: result
  ignore_errors: true

- name: List ransomware configs with limit
  nutanix.ncp.ntnx_files_ransomware_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC RansomwareConfig info v4 API.
    - It can be a single RansomwareConfig if external ID is provided.
    - List of multiple RansomwareConfig if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "b1c2d3e4-f5a6-4789-90ab-cdef01234567",
      "excluded_mount_target_ext_ids": [
          "5f0d1c2b-3a4e-4d5c-8b7a-9e0f1a2b3c4d"
      ],
      "file_extensions": [
          "*.crypto",
          "*.locked",
          "?.enc"
      ],
      "links": null,
      "tenant_id": null
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
  sample: "Api Exception raised while fetching ransomware config info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the ransomware configuration
  type: str
  returned: when external ID is provided
  sample: "b1c2d3e4-f5a6-4789-90ab-cdef01234567"

total_available_results:
  description: The total number of available ransomware configurations for the file server.
  type: int
  returned: when all ransomware configurations are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_ransomware_configs_api_instance,
)
from ..module_utils.v4.files.helpers import get_ransomware_config  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        filter=dict(type="str"),
        limit=dict(type="int"),
    )

    return module_args


def get_ransomware_config_using_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_ransomware_config(module, api_instance, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_ransomware_configs(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ransomware configs info spec", **result)

    try:
        resp = api_instance.list_ransomware_configs(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ransomware configs info",
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
        skip_info_args=True,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_ransomware_configs_api_instance(module)
    if module.params.get("ext_id"):
        get_ransomware_config_using_ext_id(module, api_instance, result)
    else:
        get_ransomware_configs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
