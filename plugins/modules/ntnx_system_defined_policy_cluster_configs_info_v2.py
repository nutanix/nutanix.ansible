#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_system_defined_policy_cluster_configs_info_v2
short_description: Fetch System-Defined Alert Policy cluster configs info in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetch cluster-specific configuration for a System-Defined Alert Policy.
  - List all cluster specific configurations associated with a System-Defined Alert Policy
    when C(ext_id) is not provided.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get System Defined Alert Policy Cluster Configs by ext_id) -
      Required Roles: Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - >-
      B(List all the System Defined Alert Policy Cluster Configs) -
      Required Roles: Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  system_defined_policy_ext_id:
    description:
      - Unique ID of the System-Defined Alert Policy.
    type: str
    required: true
  ext_id:
    description:
      - Cluster UUID.
      - When set, only the referenced cluster configuration is returned.
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
- name: Get System-Defined Alert Policy cluster config using ext_id
  nutanix.ncp.ntnx_system_defined_policy_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "111053"
    ext_id: "15e5a7d0-c007-42ac-82c0-7d1a6d542678"
  register: result

- name: List System-Defined Alert Policy cluster configs
  nutanix.ncp.ntnx_system_defined_policy_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "111053"
  register: result

- name: List System-Defined Alert Policy cluster configs with filter
  nutanix.ncp.ntnx_system_defined_policy_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "111053"
    filter: "extId eq '15e5a7d0-c007-42ac-82c0-7d1a6d542678'"
  register: result

- name: List System-Defined Alert Policy cluster configs with limit
  nutanix.ncp.ntnx_system_defined_policy_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "111053"
    limit: 1
  register: result

- name: List all System-Defined Alert Policy cluster configs with fetch_all
  nutanix.ncp.ntnx_system_defined_policy_cluster_configs_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    system_defined_policy_ext_id: "111053"
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC System-Defined Alert Policy cluster config info v4 API.
    - It can be a single cluster config if external ID is provided.
    - List of multiple cluster configs if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "alert_config": {
        "auto_resolve": "ENABLED",
        "critical_severity": {"state": "NOT_SUPPORTED"},
        "warning_severity": {"state": "ENABLED"}
      },
      "configurable_parameters": null,
      "ext_id": "00065ea6-bab3-6489-0000-000000028f57",
      "is_enabled": true,
      "schedule_interval_seconds": null
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
  sample: "Api Exception raised while fetching system-defined policy cluster configs info"

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
  description: External ID of the cluster configuration.
  type: str
  returned: when external ID is provided
  sample: "15e5a7d0-c007-42ac-82c0-7d1a6d542678"

system_defined_policy_ext_id:
  description: Unique ID of the System-Defined Alert Policy.
  type: str
  returned: always
  sample: "111053"

total_available_results:
  description: The total number of available cluster configs for the System-Defined Alert Policy.
  type: int
  returned: when all cluster configs are fetched
  sample: 5
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
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        system_defined_policy_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_cluster_config_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    system_defined_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    resp = get_cluster_config(
        module, api_instance, system_defined_policy_ext_id, ext_id
    )
    result["ext_id"] = ext_id
    result["system_defined_policy_ext_id"] = system_defined_policy_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cluster_configs(module, api_instance, result):
    system_defined_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    result["system_defined_policy_ext_id"] = system_defined_policy_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating system-defined policy cluster configs info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_cluster_configs_by_sda_id,
            kwargs=kwargs,
            systemDefinedPolicyExtId=system_defined_policy_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system-defined policy cluster configs info",
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
