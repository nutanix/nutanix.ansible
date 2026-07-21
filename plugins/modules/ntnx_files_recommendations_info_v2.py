#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_recommendations_info_v2
short_description: Fetch file server recommendations info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Recommendation in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Recommendation.
  - If C(ext_id) is not provided, list multiple Recommendation optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - The external identifier of the recommendation.
      - If provided, the specific recommendation is fetched.
    type: str
    required: false
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the recommendation(s).
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get a specific file server recommendation using ext_id
  nutanix.ncp.ntnx_files_recommendations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "38dc16f4-90b6-4b1c-8b8c-1f0fdc7b3a2e"
    ext_id: "b1c2d3e4-90b6-4b1c-8b8c-1f0fdc7b3a2e"
  register: result
  ignore_errors: true

- name: List all recommendations for a file server
  nutanix.ncp.ntnx_files_recommendations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "38dc16f4-90b6-4b1c-8b8c-1f0fdc7b3a2e"
  register: result
  ignore_errors: true

- name: List recommendations for a file server with a filter
  nutanix.ncp.ntnx_files_recommendations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "38dc16f4-90b6-4b1c-8b8c-1f0fdc7b3a2e"
    filter: "recommendationType eq Files.Config.RecommendationType'SCALE_UP'"
  register: result
  ignore_errors: true

- name: List recommendations for a file server with a limit
  nutanix.ncp.ntnx_files_recommendations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "38dc16f4-90b6-4b1c-8b8c-1f0fdc7b3a2e"
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Recommendation info v4 API.
    - It can be a single Recommendation if external ID is provided.
    - List of multiple Recommendation if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "b1c2d3e4-90b6-4b1c-8b8c-1f0fdc7b3a2e",
      "links": null,
      "recommendation_type": "SCALE_UP",
      "recommended_vm_count": 3,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - The external identifier of the recommendation.
    - Returned only when a single recommendation is fetched using its external ID.
  returned: when external ID is provided
  type: str
  sample: "b1c2d3e4-90b6-4b1c-8b8c-1f0fdc7b3a2e"

total_available_results:
  description: The total number of available recommendations for the file server.
  returned: when all recommendations are fetched
  type: int
  sample: 5

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching recommendations info"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_recommendations_api_instance,
)
from ..module_utils.v4.files.helpers import get_recommendation  # noqa: E402
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
        file_server_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_recommendation_using_ext_id(module, recommendations_api, result):
    ext_id = module.params.get("ext_id")
    file_server_ext_id = module.params.get("file_server_ext_id")
    resp = get_recommendation(module, recommendations_api, file_server_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_recommendations(module, recommendations_api, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating recommendations info spec", **result)

    try:
        resp = recommendations_api.list_recommendations(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recommendations info",
        )

    total_available_results = getattr(
        getattr(resp, "metadata", None), "total_available_results", None
    )
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
    recommendations_api = get_recommendations_api_instance(module)
    if module.params.get("ext_id"):
        get_recommendation_using_ext_id(module, recommendations_api, result)
    else:
        get_recommendations(module, recommendations_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
