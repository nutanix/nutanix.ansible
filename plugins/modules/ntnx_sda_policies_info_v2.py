#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_sda_policies_info_v2
short_description: Fetch System-Defined Alert Policies and their cluster configurations in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about System-Defined Alert (SDA) Policies in Nutanix Prism Central.
  - If C(ext_id) is provided and C(sda_policy_ext_id) is not provided, fetch details of the specific
    SDA policy identified by C(ext_id).
  - If C(sda_policy_ext_id) is provided and C(ext_id) is also provided, fetch the cluster-specific
    configuration of the SDA policy on that cluster.
  - If C(sda_policy_ext_id) is provided and C(ext_id) is not provided, list all cluster-specific
    configurations for the SDA policy (optionally paginated / filtered / sorted / projected).
  - If neither C(ext_id) nor C(sda_policy_ext_id) is provided, list all SDA policies
    (optionally paginated / filtered / sorted / projected).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get / List SDA policies or cluster configurations) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin,
      Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - When C(sda_policy_ext_id) is not provided, this is the external ID of an SDA policy to fetch.
      - When C(sda_policy_ext_id) is provided, this is the Prism Element cluster UUID and the module
        fetches the ClusterConfig for that policy on that cluster.
    type: str
    required: false
  sda_policy_ext_id:
    description:
      - The external ID of the System-Defined Alert Policy whose cluster configurations are queried.
      - When provided, the module targets the C(cluster-configs) subresource of the policy.
    type: str
    required: false
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
- name: List all SDA policies
  nutanix.ncp.ntnx_sda_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List SDA policies with filter and limit
  nutanix.ncp.ntnx_sda_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "startswith(name, 'A')"
    limit: 5
  register: result
  ignore_errors: true

- name: Get a specific SDA policy by ext_id
  nutanix.ncp.ntnx_sda_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"
  register: result
  ignore_errors: true

- name: List all cluster-specific configurations for an SDA policy
  nutanix.ncp.ntnx_sda_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    sda_policy_ext_id: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"
  register: result
  ignore_errors: true

- name: Get cluster-specific configuration of an SDA policy for a cluster
  nutanix.ncp.ntnx_sda_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    sda_policy_ext_id: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"
    ext_id: "00062e83-7dd7-51d9-2ebe-ac1f6b7a7ba0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SdaPolicy info v4 API.
    - It can be a single SdaPolicy dict if C(ext_id) is provided (and C(sda_policy_ext_id) is not).
    - A single ClusterConfig dict if both C(sda_policy_ext_id) and C(ext_id) are provided.
    - A list of SdaPolicy dicts if neither is provided (with optional filter / limit).
    - A list of ClusterConfig dicts if only C(sda_policy_ext_id) is provided (with optional filter / limit).
  returned: always
  type: dict
  sample:
    {
      "classifications": ["Availability", "Configuration"],
      "cluster_configs": [
          {
              "alert_config": {
                  "auto_resolve": "ENABLED",
                  "critical_severity": {"state": "ENABLED", "threshold_parameters": null},
                  "info_severity": {"state": "DISABLED", "threshold_parameters": null},
                  "warning_severity": {"state": "ENABLED", "threshold_parameters": null}
              },
              "configurable_parameters": null,
              "ext_id": "00062e83-7dd7-51d9-2ebe-ac1f6b7a7ba0",
              "is_enabled": true,
              "last_modified_by_user": "Nutanix",
              "last_modified_time": "2026-06-11T09:14:22.517000+00:00",
              "schedule_interval_seconds": 300
          }
      ],
      "description": "Detects Cassandra Service down state.",
      "entity_type": "CLUSTER",
      "ext_id": "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de",
      "impact_types": ["AVAILABILITY"],
      "kb_articles": ["KB-1234"],
      "name": "Cassandra Service Down",
      "policy_id": "A1055",
      "publisher": "Nutanix",
      "scope": "CLUSTER",
      "sub_type": "SCHEDULED",
      "target_clusters": ["PE"],
      "title": "Cassandra Service Down Check",
      "type": "HEALTH_CHECK"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching SDA policies info"

error:
  description: Holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: True on failure, False otherwise.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the SDA policy (or ClusterConfig) that was requested.
  type: str
  returned: when external ID is provided
  sample: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"

sda_policy_ext_id:
  description: External ID of the SDA policy whose cluster configurations were queried.
  type: str
  returned: when sda_policy_ext_id is provided
  sample: "3f47bbcd-6912-5b0f-bee6-8b45a0d1b1de"

total_available_results:
  description:
    - The total number of available SDA policies (or cluster configurations) on Prism Central.
  type: int
  returned: when a list is fetched
  sample: 250
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_system_defined_policies_api_instance,
)
from ..module_utils.v4.monitoring.helpers import (  # noqa: E402
    get_cluster_config,
    get_sda_policy,
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
        sda_policy_ext_id=dict(type="str"),
    )
    return module_args


def get_sda_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_sda_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cluster_config_using_ext_id(module, api_instance, result):
    sda_policy_ext_id = module.params.get("sda_policy_ext_id")
    cluster_ext_id = module.params.get("ext_id")
    resp = get_cluster_config(module, api_instance, sda_policy_ext_id, cluster_ext_id)
    result["ext_id"] = cluster_ext_id
    result["sda_policy_ext_id"] = sda_policy_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_sda_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SDA policies info spec", **result)

    try:
        resp = api_instance.list_sda_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SDA policies info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def get_cluster_configs(module, api_instance, result):
    sda_policy_ext_id = module.params.get("sda_policy_ext_id")
    result["sda_policy_ext_id"] = sda_policy_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating SDA policy cluster configs info spec",
            **result,
        )

    try:
        resp = api_instance.list_cluster_configs_by_sda_id(
            systemDefinedPolicyExtId=sda_policy_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SDA policy cluster configs info",
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

    sda_policy_ext_id = module.params.get("sda_policy_ext_id")
    ext_id = module.params.get("ext_id")

    if sda_policy_ext_id and ext_id:
        get_cluster_config_using_ext_id(module, api_instance, result)
    elif sda_policy_ext_id:
        get_cluster_configs(module, api_instance, result)
    elif ext_id:
        get_sda_policy_using_ext_id(module, api_instance, result)
    else:
        get_sda_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
