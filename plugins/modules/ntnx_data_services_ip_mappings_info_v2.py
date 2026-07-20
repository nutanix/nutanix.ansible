#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_services_ip_mappings_info_v2
short_description: Fetch Data Services IP Mappings of a Recovery Plan in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about DataServicesIpMapping in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific DataServicesIpMapping.
  - If C(ext_id) is not provided, list multiple DataServicesIpMapping optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Data Services IP Mapping by ext_id) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List Data Services IP Mappings) -
      Required Roles: Account Owner, Administrator, Disaster Recovery Admin, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  ext_id:
    description:
      - The external ID of the Data Services IP Mapping.
    type: str
    required: false
  recovery_plan_ext_id:
    description:
      - External identifier of the recovery plan under which the Data Services IP Mapping exists.
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
- name: Fetch a specific Data Services IP Mapping using ext_id
  nutanix.ncp.ntnx_data_services_ip_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
  register: result

- name: List all Data Services IP Mappings for a Recovery Plan
  nutanix.ncp.ntnx_data_services_ip_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
  register: result

- name: List Data Services IP Mappings with limit
  nutanix.ncp.ntnx_data_services_ip_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
    limit: 1
  register: result

- name: List Data Services IP Mappings with filter
  nutanix.ncp.ntnx_data_services_ip_mappings_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_plan_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
    filter: "primaryCluster/extId eq '0005f7bf-3e2b-4a41-0000-000000029d0e'"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC DataServicesIpMapping info v4 API.
    - It can be a single DataServicesIpMapping if external ID is provided.
    - List of multiple DataServicesIpMapping if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "e7ae4b0d-726d-410d-87c2-af46f8bea264",
        "links": null,
        "primary_cluster": {
            "ext_id": "0005f7bf-3e2b-4a41-0000-000000029d0e",
            "name": null
        },
        "primary_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.76.55"
            },
            "ipv6": null
        },
        "primary_test_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.76.56"
            },
            "ipv6": null
        },
        "recovery_cluster": {
            "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57",
            "name": null
        },
        "recovery_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.77.55"
            },
            "ipv6": null
        },
        "recovery_test_data_services_ip": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.77.56"
            },
            "ipv6": null
        },
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
  sample: "Api Exception raised while fetching Data Services IP Mapping info"

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
  description: External ID of the Data Services IP Mapping.
  type: str
  returned: when external ID is provided
  sample: "e7ae4b0d-726d-410d-87c2-af46f8bea264"

total_available_results:
  description: The total number of available Data Services IP Mappings in PC for the recovery plan.
  type: int
  returned: when Data Services IP Mappings are listed
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import (  # noqa: E402
    get_data_services_ip_mapping,
)
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
        recovery_plan_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_data_services_ip_mapping_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    resp = get_data_services_ip_mapping(
        module, api_instance, recovery_plan_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_data_services_ip_mappings(module, api_instance, result):
    recovery_plan_ext_id = module.params.get("recovery_plan_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Data Services IP Mappings info spec", **result
        )

    try:
        resp = api_instance.list_data_services_ip_mappings(
            recoveryPlanExtId=recovery_plan_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Data Services IP Mappings info",
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
    api_instance = get_recovery_plans_api_instance(module)
    if module.params.get("ext_id"):
        get_data_services_ip_mapping_using_ext_id(module, api_instance, result)
    else:
        get_data_services_ip_mappings(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
