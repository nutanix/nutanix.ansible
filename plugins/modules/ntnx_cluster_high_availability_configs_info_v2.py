#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_high_availability_configs_info_v2
short_description: Fetch cluster high availability configs info in Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to fetch information about cluster high availability configs in Nutanix Prism Central.
  - If C(cluster_ext_id) is provided, fetch details of the specific cluster high availability config.
  - If C(cluster_ext_id) is not provided, list multiple cluster high availability configs optionally filtered or paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get High Availability Config) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List High Availability Configs) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster to fetch high availability configuration for.
      - When provided, a single high availability config is returned for that cluster.
      - When not provided, list all high availability configs across clusters.
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
- name: Get cluster high availability config using cluster ext_id
  nutanix.ncp.ntnx_cluster_high_availability_configs_info_v2:
    cluster_ext_id: "00065dc6-9144-09c1-4862-ac1f6b35f170"
  register: result
  ignore_errors: true

- name: List all cluster high availability configs
  nutanix.ncp.ntnx_cluster_high_availability_configs_info_v2:
  register: result
  ignore_errors: true

- name: List cluster high availability configs with filter
  nutanix.ncp.ntnx_cluster_high_availability_configs_info_v2:
    filter: "clusterExtId eq '00065dc6-9144-09c1-4862-ac1f6b35f170'"
  register: result
  ignore_errors: true

- name: List cluster high availability configs with limit
  nutanix.ncp.ntnx_cluster_high_availability_configs_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List all cluster high availability configs with fetch_all
  nutanix.ncp.ntnx_cluster_high_availability_configs_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix cluster high availability configs info v4 API
    - It can be a single cluster high availability config if External ID is provided.
    - List of multiple cluster high availability configs if External ID is not provided with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    [
      {
        "cluster_ext_id": "00065dc6-9144-09c1-4862-ac1f6b35f170",
        "ext_id": null,
        "ha_config": {
          "ext_id": "00065dc6-9144-09c1-4862-ac1f6b35f170",
          "host_failures_to_tolerate_count": 1,
          "is_ha_enabled": true,
          "links": null,
          "remaining_host_failures_to_tolerate_count": 1,
          "reserved_memory_bytes": 10737418240,
          "state": "HIGHLY_AVAILABLE",
          "tenant_id": null
        },
        "links": null,
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
  sample: "Api Exception raised while fetching high availability configs info"

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
  description: External ID of the cluster whose high availability config was fetched
  type: str
  returned: when external ID is provided
  sample: "00065dc6-9144-09c1-4862-ac1f6b35f170"

total_available_results:
  description: The total number of available cluster high availability configs in PC.
  type: int
  returned: when all cluster high availability configs are fetched
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_high_availability_configs_api_instance,
    get_high_availability_config_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_high_availability_config,
)
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
        cluster_ext_id=dict(type="str", required=False),
    )

    return module_args


def get_high_availability_config_using_cluster_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id
    resp = get_high_availability_config(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cluster_high_availability_configs(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating cluster high availability configs info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_high_availability_configs,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching high availability configs info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
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
            ("cluster_ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    if module.params.get("cluster_ext_id"):
        api_instance = get_high_availability_config_api_instance(module)
        get_high_availability_config_using_cluster_ext_id(module, api_instance, result)
    else:
        api_instance = get_cluster_high_availability_configs_api_instance(module)
        get_cluster_high_availability_configs(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
