#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_descriptors_info_v2
short_description: Fetch aiops entity and metric descriptors in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about EntityDescriptorsV4 in Nutanix Prism Central.
  - EntityDescriptorsV4 exposes metadata (dictionary/catalog) of entity types
    and the metrics/attributes that can be queried for each entity for a
    given data source (for example C(nutanix)).
  - If C(ext_id) is not provided, list multiple EntityDescriptorsV4 optionally
    filtered / paginated. This SDK endpoint is a list-only (singleton) datasource
    so a get-by-ID variant is not offered by the aiops SDK.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(List Entity Descriptors for a source) -
      Required Roles / Operations: AIOps:View_Stats_Entity_Descriptors
      (typically Prism Viewer, Prism Admin, Super Admin, or any role granting
      the AIOps stats read permission).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  ext_id:
    description:
      - Placeholder external ID field kept for interface parity with other
        C(_info_v2) modules.
      - The aiops EntityDescriptorsV4 endpoint is a singleton list operation
        and does not offer a get-by-ID variant, so this field is currently
        ignored and reserved for future SDK expansion.
    type: str
    required: false
  source_ext_id:
    description:
      - The external ID (UUID) or well-known name of the aiops data source
        (for example C(nutanix)) to fetch the entity/metric descriptors for.
      - Required for listing entity descriptors.
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
- name: List all entity descriptors for the nutanix source
  nutanix.ncp.ntnx_entity_descriptors_info_v2:
    source_ext_id: "nutanix"
  register: result
  ignore_errors: true

- name: List entity descriptors with a limit
  nutanix.ncp.ntnx_entity_descriptors_info_v2:
    source_ext_id: "nutanix"
    limit: 5
  register: result
  ignore_errors: true

- name: List entity descriptors with an OData filter
  nutanix.ncp.ntnx_entity_descriptors_info_v2:
    source_ext_id: "nutanix"
    filter: "entityType eq 'vm'"
  register: result
  ignore_errors: true

- name: List a specific page of entity descriptors
  nutanix.ncp.ntnx_entity_descriptors_info_v2:
    source_ext_id: "nutanix"
    page: 0
    limit: 10
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC EntityDescriptorsV4 info v4 API.
    - A list of multiple EntityDescriptorsV4 for the requested source,
      optionally narrowed by C(filter), C(page) or C(limit).
    - Each item describes an entity type (for example C(vm), C(cluster))
      and the metrics/attributes it exposes.
  returned: always
  type: list
  elements: dict
  sample:
    - display_name: "VM"
      entity_type: "vm"
      ext_id: "vm"
      links: null
      metrics:
        - default_value: null
          display_name: "CPU Usage (%)"
          downsampling_operator: "AVG"
          is_attribute: false
          is_attribute_persisted_as_time_series: null
          name: "hypervisor_cpu_usage_ppm"
          sampling_interval_secs: 30
          unit: "ppm"
          value_range: null
          value_type: "DOUBLE"
      parents:
        - entity_type: "cluster"
          ext_id: "cluster"
      source: "nutanix"
      tenant_id: null

total_available_results:
  description: The total number of available entity descriptors for the requested source in PC.
  returned: when all entity descriptors are fetched
  type: int
  sample: 42

ext_id:
  description:
    - The external ID echoed back when C(ext_id) is supplied. The aiops SDK
      does not currently expose a get-by-ID call so this is only populated
      when the caller sets C(ext_id).
  returned: when C(ext_id) is provided
  type: str
  sample: "vm"

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Human readable status/error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching entity descriptors for source 'nutanix'"

error:
  description: Error details if the task fails.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_stats_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_entity_descriptors  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        source_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_entity_descriptors_list(module, api_instance, result):
    """
    Fetch the list of aiops entity descriptors for the supplied source.

    Populates ``result["response"]`` with the (possibly empty) list, and
    ``result["total_available_results"]`` with the total count reported by
    the server metadata.
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating entity descriptors info spec", **result)

    source_ext_id = module.params.get("source_ext_id")
    resp = get_entity_descriptors(module, api_instance, source_ext_id, **kwargs)

    resp_dict = strip_internal_attributes(resp.to_dict())
    metadata = resp_dict.get("metadata") or {}
    total_available_results = metadata.get("total_available_results")
    result["total_available_results"] = total_available_results

    data = resp_dict.get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_stats_api_instance(module)
    if module.params.get("ext_id"):
        # The aiops SDK does not expose a "get by ID" variant for entity
        # descriptors — echo the ext_id back so callers can use it downstream
        # but still fetch the full list scoped to the source.
        result["ext_id"] = module.params.get("ext_id")
    get_entity_descriptors_list(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
