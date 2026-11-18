#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_node_schedulable_status_info_v2
short_description: Fetch Node Schedulable Status info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch Node Schedulable Status info in Nutanix Prism Central.
  - Each entry indicates whether an AHV node in the cluster is a storage-only
    ("never schedulable") node or a regular schedulable node.
  - Fetch multiple Node Schedulable Status entries with/without using filters, limit, etc.
  - The Nutanix v4 API exposes only a list endpoint for Node Schedulable Status
    (no Get-by-ID).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View Node Schedulable Status) -
      Required Roles: Network Infra Admin, Prism Admin, Project Manager, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - Prism Element cluster UUID (maps to the C(X-Cluster-Id) header).
      - Optional. When supplied, the API scopes the listing to the given PE cluster.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all node schedulable statuses
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
  register: result
  ignore_errors: true

- name: List node schedulable statuses for a specific PE cluster
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: List only never-schedulable (storage-only) nodes
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    filter: "isNeverSchedulable eq true"
  register: result
  ignore_errors: true

- name: List only regular (schedulable) nodes
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    filter: "isNeverSchedulable eq false"
  register: result
  ignore_errors: true

- name: List node schedulable statuses with a limit
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: Sort node schedulable statuses in ascending order of isNeverSchedulable
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    orderby: "isNeverSchedulable asc"
  register: result
  ignore_errors: true

- name: List all node schedulable statuses with fetch_all
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - List of Node Schedulable Status entries from the Nutanix PC
      list Node Schedulable Status v4 API.
    - Optionally filtered, limited, or ordered using C(filter), C(limit),
      C(page), or C(orderby).
  returned: always
  type: list
  sample:
    [
      {
        "ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e",
        "is_never_schedulable": false,
        "links": null,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching node schedulable statuses info"

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available Node Schedulable Status entries in PC.
  type: int
  returned: When all node schedulable statuses are fetched
  sample: 4
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_virtual_switch_nodes_info_api_instance,
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
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def get_node_schedulable_statuses(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating node schedulable statuses info spec", **result
        )

    if module.params.get("cluster_ext_id"):
        kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")

    try:
        resp = list_entities(
            api_instance.list_node_schedulable_status,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching node schedulable statuses info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_virtual_switch_nodes_info_api_instance(module)
    get_node_schedulable_statuses(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
