#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_effective_rate_limit_policies_info_v2
short_description: Fetch effective image rate limit policies in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to list effective image rate limit policies in Nutanix Prism Central.
  - The effective rate limit for the Prism Elements. If no rate limit applies to a particular
    cluster, no entry is returned for that cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Resolve the effective rate limit for Prism Elements) -
    Required Roles: Super Admin, Prism Admin, Prism Viewer, Virtual Machine Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
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
- name: List all effective rate limit policies
  nutanix.ncp.ntnx_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List effective rate limit policies for a specific cluster using filter
  nutanix.ncp.ntnx_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "clusterExtId eq '000647b8-ddb3-6bbb-0000-000000028f57'"
  register: result
  ignore_errors: true

- name: List effective rate limit policies with a page limit
  nutanix.ncp.ntnx_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List all effective rate limit policies with fetch_all
  nutanix.ncp.ntnx_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching effective rate limit policies info.
    - List of effective rate limit policies when listing.
  returned: always
  type: dict
  sample:
    [
      {
          "cluster_ext_id": "000647b8-ddb3-6bbb-0000-000000028f57",
          "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
          "links": null,
          "rate_limit_ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
          "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching effective rate limit policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of effective rate limit policy records available in PC.
  type: int
  returned: when the list operation succeeds
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_image_rate_limit_policy_api_instance,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_effective_rate_limit_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating effective rate limit policies info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_effective_rate_limit_policies,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching effective rate limit policies info",
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
    if total_available_results is not None:
        result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=dict(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_image_rate_limit_policy_api_instance(module)
    get_effective_rate_limit_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
