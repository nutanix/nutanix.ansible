#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_defined_policies_info_v2
short_description: Fetch User-Defined Alert policies info in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetch details of a User-Defined Alert policy identified by external ID.
  - List User-Defined Alert policies optionally filtered or paginated when C(ext_id) is not provided.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get User-Defined Alert policy by ext_id) -
      Required Roles: Files Admin, Files Viewer, Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - >-
      B(List all the User-Defined Alert policies) -
      Required Roles: Files Admin, Files Viewer, Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - Entity UUID.
      - When set, only the referenced User-Defined Alert policy is returned.
    type: str
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
- name: Get User-Defined Alert policy using ext_id
  nutanix.ncp.ntnx_user_defined_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "701bcb62-de3c-4f24-aec9-dd9de450d3ac"
  register: result

- name: List all User-Defined Alert policies
  nutanix.ncp.ntnx_user_defined_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List User-Defined Alert policies with filter
  nutanix.ncp.ntnx_user_defined_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "title eq 'VM CPU Usage'"
  register: result

- name: List User-Defined Alert policies with limit
  nutanix.ncp.ntnx_user_defined_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all User-Defined Alert policies with fetch_all
  nutanix.ncp.ntnx_user_defined_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC User-Defined Alert policy info v4 API.
    - It can be a single User-Defined Alert policy if external ID is provided.
    - List of multiple User-Defined Alert policies if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "created_by": "admin",
      "description": "Trigger warning alert when cluster CPU usage exceeds 80%",
      "entity_type": "cluster",
      "ext_id": "ff30d9de-0648-427b-bf2c-646ee8ec23cb",
      "filters": [
          {"ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2", "type": "CLUSTER"}
      ],
      "impact_types": ["PERFORMANCE"],
      "is_auto_resolved": true,
      "is_enabled": true,
      "is_expected_to_error_on_conflict": null,
      "last_updated_time": "2026-07-20T15:36:58.758223+00:00",
      "links": null,
      "policies_to_override": null,
      "policyId": "Ac89aa5ad-9b13-41a5-956f-3c622c904499",
      "related_policies": null,
      "tenant_id": null,
      "title": "vm_high_cpu_uda_policy_ansible_updated",
      "trigger_conditions": [
          {
              "condition": {
                  "metric_name": "hypervisor_cpu_usage_ppm",
                  "operator": "GREATER_THAN",
                  "threshold_value": {"int_value": 800000}
              },
              "condition_type": "STATIC_THRESHOLD",
              "severity_level": "WARNING"
          }
      ],
      "trigger_wait_period": 900
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
  sample: "Api Exception raised while fetching user-defined policies info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the User-Defined Alert policy.
  type: str
  returned: when external ID is provided
  sample: "701bcb62-de3c-4f24-aec9-dd9de450d3ac"

total_available_results:
  description: The total number of available User-Defined Alert policies in PC.
  type: int
  returned: when all User-Defined Alert policies are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_user_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_uda_policy  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
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


def get_uda_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_uda_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_uda_policies(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating user-defined policies info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_uda_policies,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user-defined policies info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

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
    api_instance = get_user_defined_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_uda_policy_using_ext_id(module, api_instance, result)
    else:
        get_uda_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
