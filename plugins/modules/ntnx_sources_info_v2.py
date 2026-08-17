#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_sources_info_v2
short_description: Fetch aiops SourcesV4 info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about SourcesV4 in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific SourcesV4.
  - If C(ext_id) is not provided, list multiple SourcesV4.
  - The aiops SDK exposes only a singleton listing endpoint for SourcesV4 —
    server-side filter, limit, page, orderby and select are NOT supported and
    are intentionally omitted from this module.
  - This module uses PC v4 APIs based SDKs (namespace C(aiops)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get list of aiops SourcesV4) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  ext_id:
    description:
      - The external ID of the aiops SourcesV4.
      - When provided, filter the sources listing client-side and return the
        matching single Source object.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get aiops source using ext_id
  nutanix.ncp.ntnx_sources_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d2c1a3a4-0000-0000-0000-000000000001"
  register: result
  ignore_errors: true

- name: List all aiops sources
  nutanix.ncp.ntnx_sources_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SourcesV4 info v4 API.
    - It can be a single SourcesV4 if external ID is provided.
    - List of multiple SourcesV4 if external ID is not provided.
    - The aiops SDK does not accept filter/limit query params for this endpoint.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "db293e8a-5770-c3c7-4213-85dbbc1d3679",
      "links": null,
      "source_name": "nutanix",
      "tenant_id": null
    }

total_available_results:
  description: The total number of available aiops sources returned by PC.
  type: int
  returned: when all sources are fetched
  sample: 1

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching sources v4 list"

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
  description: External ID of the aiops SourcesV4
  type: str
  returned: when external ID is provided
  sample: "db293e8a-5770-c3c7-4213-85dbbc1d3679"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_stats_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import (  # noqa: E402
    get_source_by_ext_id,
    list_sources,
)
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_aiops_py_client as aiops_sdk  # noqa: F401,E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as aiops_sdk  # noqa: F401,E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_source_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    source = get_source_by_ext_id(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(source.to_dict())


def get_sources(module, api_instance, result):
    resp = list_sources(module, api_instance)
    resp_dict = strip_internal_attributes(resp.to_dict())
    metadata = resp_dict.get("metadata") or {}
    result["total_available_results"] = metadata.get("total_available_results")
    data = resp_dict.get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_aiops_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_stats_api_instance(module)
    if module.params.get("ext_id"):
        get_source_using_ext_id(module, api_instance, result)
    else:
        get_sources(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
