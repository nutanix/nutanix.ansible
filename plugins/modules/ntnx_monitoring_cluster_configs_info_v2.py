#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_monitoring_cluster_configs_info_v2
short_description: Fetch cluster-specific configurations of a System-Defined Alert Policy in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ClusterConfigsBySdaId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ClusterConfigsBySdaId.
  - If C(ext_id) is not provided, list multiple ClusterConfigsBySdaId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get cluster config by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
  - >-
    B(List cluster configs of an SDA policy) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - Cluster UUID for which the SDA policy per-cluster configuration is being fetched.
      - When provided, the module returns a single ClusterConfig entry.
    type: str
    required: false
  system_defined_policy_ext_id:
    description:
      - Unique ID of the System-Defined Alert Policy whose per-cluster configurations
        are being fetched.
      - Required for both get-by-id (single) and list operations, since the underlying
        API only exposes cluster configurations scoped to a specific SDA policy.
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
- name: Fetch cluster config of an SDA policy for a specific cluster
  nutanix.ncp.ntnx_monitoring_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "5a8b7f2c-4ce3-9212-2ca4-e4b4d258bde7"
    ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: List all cluster configs of a System-Defined Alert Policy
  nutanix.ncp.ntnx_monitoring_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "5a8b7f2c-4ce3-9212-2ca4-e4b4d258bde7"
  register: result
  ignore_errors: true

- name: List first 5 cluster configs of a System-Defined Alert Policy
  nutanix.ncp.ntnx_monitoring_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "5a8b7f2c-4ce3-9212-2ca4-e4b4d258bde7"
    limit: 5
  register: result
  ignore_errors: true

- name: List cluster configs filtered by cluster ext_id
  nutanix.ncp.ntnx_monitoring_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "5a8b7f2c-4ce3-9212-2ca4-e4b4d258bde7"
    filter: "extId eq 'bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258'"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ClusterConfigsBySdaId info v4 API.
    - It can be a single ClusterConfigsBySdaId if external ID is provided.
    - List of multiple ClusterConfigsBySdaId if external ID is not provided
      with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
        "alert_config": {
            "auto_resolve": "ENABLED",
            "critical_severity": {
                "state": "ENABLED",
                "threshold_parameters": null
            },
            "info_severity": {
                "state": "DISABLED",
                "threshold_parameters": null
            },
            "warning_severity": {
                "state": "ENABLED",
                "threshold_parameters": null
            }
        },
        "configurable_parameters": null,
        "ext_id": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
        "is_enabled": true,
        "last_modified_by_user": "admin",
        "last_modified_time": "2026-07-20T12:30:00Z",
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
  sample: "Api Exception raised while fetching ClusterConfigsBySdaId info"

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
  description: Cluster UUID of the fetched SDA policy cluster configuration.
  type: str
  returned: when external ID is provided
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

total_available_results:
  description: The total number of available cluster configs for the SDA policy in PC.
  type: int
  returned: when list of ClusterConfigsBySdaId is fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_system_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import (  # noqa: E402
    get_cluster_config_by_sda_id,
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
        system_defined_policy_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_cluster_config_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    system_defined_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    resp = get_cluster_config_by_sda_id(
        module, api_instance, system_defined_policy_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cluster_configs(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating ClusterConfigsBySdaId info spec", **result
        )

    system_defined_policy_ext_id = module.params.get("system_defined_policy_ext_id")

    try:
        resp = api_instance.list_cluster_configs_by_sda_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching ClusterConfigsBySdaId info "
                "for SDA policy ext_id: {0}".format(system_defined_policy_ext_id)
            ),
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
