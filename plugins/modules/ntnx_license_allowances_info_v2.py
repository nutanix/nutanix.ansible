#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_license_allowances_info_v2
short_description: Lists features allowed for use under the applied license
description:
    - Lists features allowed for use under the applied license.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.4.0"
options:
  expand:
    description:
      - The expand parameter is used to expand the response.
    type: str
author:
  - Abhinav Bansal (@abhinavbansal29)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Get license allowances info
  nutanix.ncp.ntnx_license_allowances_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: Get license allowances info using limit
  nutanix.ncp.ntnx_license_allowances_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: Get license allowances info using filter
  nutanix.ncp.ntnx_license_allowances_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: type eq Licensing.Config.ClusterType'NUTANIX'
  register: result
  ignore_errors: true

- name: Get license allowances info using expand
  nutanix.ncp.ntnx_license_allowances_info_v2:
    expand: details
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
    - The response from the Nutanix List license allowances API.
  type: dict
  returned: always
  sample:
    [
        {
            "details": [
                {
                    "feature_id": "WHAT_IF_ANALYSIS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "CAPACITY_FORECAST",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "ONE_CLICK_UPGRADES_LCM",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "CUSTOM_DASHBOARD",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "SEARCH",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "ANALYSIS_SESSION",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "ADV_ORCH_RUNBOOKS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "XDISCOVER",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "BUDGETING_CHARGEBACK",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "MAX_TRIAL_PERIOD_DAYS",
                    "scope": "PC",
                    "value": "0",
                    "value_type": "INTEGER"
                },
                {
                    "feature_id": "SQL_SERVER_MONITORING",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "XPILOT",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "SPEND_VISIBILITY_ANALYSIS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "INFRASTRUCTURE_MGMT",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "VULCAN",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "SMART_ALERTS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "MULTI_VM_APPS_BLUEPRINTS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "IAAS_SINGLE_VM_BLUEPRINTS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "ANOMALY_DETECTION",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "SELF_SERVICE_APPROVALS",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "VM_INEFFICIENCY_DETECTION",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "PC_REPORTING",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "SELF_SERVICE_SCHEDULER",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "COST_METERING",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "APP_MONITORING",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "VCENTER_MONITORING",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "SELF_SERVICE_MARKETPLACE",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                },
                {
                    "feature_id": "MONITORING_TROUBLESHOOTING",
                    "scope": "PC",
                    "value": "TRUE",
                    "value_type": "BOOLEAN"
                }
            ],
            "ext_id": "00063e5a-2715-c792-0000-000000028f57",
            "is_multicluster": false,
            "links": null,
            "name": "auto_cluster_prod_e97a5f710501",
            "tenant_id": null,
            "type": "NUTANIX"
        }
    ]
changed:
    description:
        - Indicates whether the module has made any changes.
    type: bool
    returned: always
    sample: false
total_available_results:
    description:
        - The total number of available license allowances.
    type: int
    returned: when all license allowances are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.licensing.api_client import (  # noqa: E402
    get_licensing_api_instance,
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
        expand=dict(type="str"),
    )
    return module_args


def license_allowances_info(module, licensing_api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating license allowances info Spec", **result)
    try:
        resp = licensing_api_instance.list_allowances(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching license allowances info",
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
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
    }

    licensing_api_instance = get_licensing_api_instance(module)

    license_allowances_info(module, licensing_api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
