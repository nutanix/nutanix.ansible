#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_effective_rate_limit_policies_info_v2
short_description: Fetch effective rate limit policy info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about EffectiveRateLimitPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific EffectiveRateLimitPolicy.
  - If C(ext_id) is not provided, list multiple EffectiveRateLimitPolicy optionally filtered / paginated.
  - The EffectiveRateLimitPolicy resource resolves the rate limit that is
    currently in effect for each Prism Element cluster after evaluating every
    matching image rate limit policy (lowest configured C(rateLimitKbps) wins).
  - This module uses PC v4 APIs based SDKs.
options:
  ext_id:
    description:
      - The external identifier of the image rate limit policy whose effective
        record on a cluster should be fetched.
      - When provided, the module resolves the effective policy by first
        loading the image rate limit policy with this external identifier and
        then filtering the effective policies to those referencing it.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(List effective rate limit policies) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all effective rate limit policies
  nutanix.ncp.ntnx_vm_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List effective rate limit policies for a specific cluster using filter
  nutanix.ncp.ntnx_vm_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "clusterExtId eq '000647b8-ddb3-6bbb-0000-000000028f57'"
  register: result
  ignore_errors: true

- name: List effective rate limit policies with a page limit
  nutanix.ncp.ntnx_vm_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: Fetch the effective rate limit policy record for a specific rate limit policy
  nutanix.ncp.ntnx_vm_effective_rate_limit_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC EffectiveRateLimitPolicy info v4 API.
    - It can be a single EffectiveRateLimitPolicy if external ID is provided.
    - List of multiple EffectiveRateLimitPolicy if external ID is not provided
      with optional filter or limit.
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
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching effective rate limit policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the image rate limit policy that was resolved.
  type: str
  returned: when external ID is provided
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

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
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_image_rate_limit_policy_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_image_rate_limit_policy  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Return the argument spec for the info module.

    The list API supports the OData query parameters ($page, $limit, $filter,
    $orderby, $select). Those are provided by C(BaseInfoModule) so we only add
    the ``ext_id`` option here.
    """

    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_effective_rate_limit_policy_using_ext_id(module, api_instance, result):
    """
    Resolve the effective rate limit policy record for a specific image rate
    limit policy identified by ``ext_id``.

    The effective policies list API does not accept a server-side filter on
    ``rateLimitExtId`` (Prism returns HTTP 400 for that expression), so we do
    the filtering client-side: fetch the source policy (fails fast on 404),
    list every effective record, and return the subset whose
    ``rate_limit_ext_id`` matches the requested policy. If no cluster
    currently matches the source policy's ``cluster_entity_filter`` the
    response is an empty list.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    # Verify the requested rate limit policy exists (raises on 404).
    get_image_rate_limit_policy(module, api_instance, ext_id)

    try:
        resp = api_instance.list_effective_rate_limit_policies()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching effective rate limit policies info using ext_id",
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
    if total_available_results is not None:
        result["total_available_results"] = total_available_results
    data = strip_internal_attributes(resp.to_dict()).get("data") or []
    matches = [record for record in data if record.get("rate_limit_ext_id") == ext_id]
    result["response"] = matches


def list_effective_rate_limit_policies(module, api_instance, result):
    """
    List all effective rate limit policies (optionally filtered / paginated).
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating effective rate limit policies info spec", **result
        )

    try:
        resp = api_instance.list_effective_rate_limit_policies(**kwargs)
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
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_image_rate_limit_policy_api_instance(module)
    if module.params.get("ext_id"):
        get_effective_rate_limit_policy_using_ext_id(module, api_instance, result)
    else:
        list_effective_rate_limit_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
