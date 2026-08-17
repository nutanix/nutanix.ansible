#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_configs_info_v2
short_description: Fetch ClusterConfig info of a System-Defined Alert Policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ClusterConfig in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ClusterConfig (single entity).
  - If C(ext_id) is not provided, list all ClusterConfig entries for the given
    System-Defined Alert (SDA) Policy - optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get / List ClusterConfig) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - The Cluster UUID (ClusterConfig external ID).
      - When provided, a single ClusterConfig entry is fetched.
    type: str
    required: false
  system_defined_policy_ext_id:
    description:
      - The unique external ID of the parent System-Defined Alert (SDA) Policy.
      - Required for both single-fetch and list operations.
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
- name: Get ClusterConfig using ext_id
  nutanix.ncp.ntnx_cluster_configs_info_v2:
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
    ext_id: "0005f36a-b46f-8d0e-0000-000000000000"
  register: result
  ignore_errors: true

- name: List all ClusterConfigs for an SDA policy
  nutanix.ncp.ntnx_cluster_configs_info_v2:
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
  register: result
  ignore_errors: true

- name: List ClusterConfigs with limit and pagination
  nutanix.ncp.ntnx_cluster_configs_info_v2:
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
    limit: 5
    page: 0
  register: result
  ignore_errors: true

- name: List ClusterConfigs sorted by extId
  nutanix.ncp.ntnx_cluster_configs_info_v2:
    system_defined_policy_ext_id: "6c3f96e8-4d63-4a91-a2b4-4f6ce7de7f22"
    orderby: "extId asc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ClusterConfig info v4 API.
    - It can be a single ClusterConfig if external ID is provided.
    - List of multiple ClusterConfig if external ID is not provided
      (optionally paginated by C(limit) / C(page) or ordered by C(orderby)).
    - The C(filter) parameter is not supported for this endpoint.
  returned: always
  type: dict
  sample:
    {
      "alert_config": {
        "auto_resolve": "ENABLED",
        "critical_severity": {"state": "ENABLED", "threshold_parameters": null},
        "info_severity": {"state": "DISABLED", "threshold_parameters": null},
        "warning_severity": {"state": "ENABLED", "threshold_parameters": null}
      },
      "configurable_parameters": null,
      "ext_id": "0005f36a-b46f-8d0e-0000-000000000000",
      "is_enabled": true,
      "last_modified_by_user": "admin",
      "last_modified_time": "2026-07-21T10:15:22.123456+00:00",
      "links": null,
      "schedule_interval_seconds": 600,
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
  sample: "Api Exception raised while fetching ClusterConfig info"

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
  description: External ID of the ClusterConfig (Cluster UUID)
  type: str
  returned: when external ID is provided
  sample: "0005f36a-b46f-8d0e-0000-000000000000"

total_available_results:
  description: The total number of available ClusterConfig entries for the SDA policy in PC.
  type: int
  returned: when ClusterConfigs are listed
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_system_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_cluster_config  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=False),
        system_defined_policy_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_cluster_config_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    sda_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    resp = get_cluster_config(module, api_instance, sda_policy_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def get_cluster_configs(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ClusterConfig info spec", **result)

    sda_policy_ext_id = module.params.get("system_defined_policy_ext_id")

    try:
        resp = api_instance.list_cluster_configs_by_sda_id(
            systemDefinedPolicyExtId=sda_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ClusterConfig info",
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_system_defined_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_cluster_config_using_ext_id(module, api_instance, result)
    else:
        get_cluster_configs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
