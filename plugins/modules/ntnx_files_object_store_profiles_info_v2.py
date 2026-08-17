#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_object_store_profiles_info_v2
short_description: Fetch object store profiles for a Nutanix Files file server
version_added: 2.6.0
description:
  - This module allows you to fetch information about ObjectStoreProfile in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ObjectStoreProfile.
  - If C(ext_id) is not provided, list multiple ObjectStoreProfile optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the object store profiles.
      - Required for both get-by-id and list operations.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the object store profile.
      - If provided, fetch the specific object store profile.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Fetch object store profile using ext_id
  nutanix.ncp.ntnx_files_object_store_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "0006abcd-1111-2222-3333-444455556666"
    ext_id: "1e4e557e-a53e-4d2f-b2d6-a1da4ccf2430"
  register: result
  ignore_errors: true

- name: List all object store profiles for a file server
  nutanix.ncp.ntnx_files_object_store_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "0006abcd-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true

- name: List object store profiles with filter
  nutanix.ncp.ntnx_files_object_store_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "0006abcd-1111-2222-3333-444455556666"
    filter: "name eq 'tiering_profile_ansible'"
  register: result
  ignore_errors: true

- name: List object store profiles with limit
  nutanix.ncp.ntnx_files_object_store_profiles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "0006abcd-1111-2222-3333-444455556666"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ObjectStoreProfile info v4 API.
    - It can be a single ObjectStoreProfile if external ID is provided.
    - List of multiple ObjectStoreProfile if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "1e4e557e-a53e-4d2f-b2d6-a1da4ccf2430",
      "name": "tiering_profile_ansible",
      "object_store_type": "AWS",
      "mount_targets_enablement_type": "ALL_CURRENT_MOUNT_TARGETS",
      "mount_target_ext_ids": ["b0df3e22-a3a3-4b86-8f09-ec9e1f3e8dc2"],
      "retention_period_days": 1825,
      "is_ssl_peer_verfication_enabled": true,
      "object_store_config": {
          "base_url": "https://s3.us-east-1.amazonaws.com/",
          "ca_cert_content": null,
          "configuration": {
              "access_key": "AKIAEXAMPLEACCESSKEY",
              "bucket_location": "us-east-1",
              "bucket_name": "files-tiering-bucket"
          },
          "proxy_server": null
      },
      "recovery_object_store_config": null,
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the object store profile.
  returned: when external ID is provided
  type: str
  sample: "1e4e557e-a53e-4d2f-b2d6-a1da4ccf2430"

total_available_results:
  description: The total number of available object store profiles for the file server.
  returned: when all object store profiles are fetched
  type: int
  sample: 1

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching object store profiles info"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import get_tier_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import get_object_store_profile  # noqa: E402
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
    )
    return module_args


def get_object_store_profile_using_ext_id(module, tier_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_object_store_profile(module, tier_api, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_object_store_profiles(module, tier_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object store profiles info spec", **result
        )

    try:
        resp = tier_api.list_object_store_profiles(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store profiles info",
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
    result = {"changed": False, "response": None, "failed": False}
    tier_api = get_tier_api_instance(module)
    if module.params.get("ext_id"):
        get_object_store_profile_using_ext_id(module, tier_api, result)
    else:
        get_object_store_profiles(module, tier_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
