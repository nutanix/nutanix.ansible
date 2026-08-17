#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_node_schedulable_status_info_v2
short_description: Fetch Node Schedulable Status info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about NodeSchedulableStatus in Nutanix Prism Central.
  - Each entry indicates whether an AHV node in the cluster is a storage-only
    ("never schedulable") node or a regular schedulable node.
  - If C(ext_id) is not provided, list multiple NodeSchedulableStatus entries
    optionally filtered / paginated / sorted.
  - The underlying SDK endpoint C(/networking/v4/config/node-schedulable-statuses)
    is a list-only API — there is no get-by-id endpoint, so C(ext_id) is used to
    client-side filter the listed results.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get list of Node Schedulable Statuses) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, Virtual Machine Admin, Virtual Machine Operator,
      Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  ext_id:
    description:
      - The external ID (UUID) of a specific node.
      - When provided, the list is fetched from the API and the entry with a matching
        C(ext_id) is returned (the underlying SDK does not expose a get-by-id endpoint).
    type: str
    required: false
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

- name: Fetch a specific node's schedulable status by node ext_id
  nutanix.ncp.ntnx_node_schedulable_status_info_v2:
    ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC NodeSchedulableStatus info v4 API.
    - It is a single NodeSchedulableStatus entry (as a dict) when C(ext_id) is
      provided and a match is found in the listed results.
    - It is a list of multiple NodeSchedulableStatus entries when C(ext_id) is
      not provided, optionally narrowed by filter, limit, page, orderby, or
      cluster_ext_id.
    - Each entry contains C(ext_id) (the node UUID) and C(is_never_schedulable)
      (True for storage-only nodes, False for regular schedulable nodes).
  returned: always
  type: dict
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
  returned: When there is an error or a specific ext_id is not found.
  type: str
  sample: "Api Exception raised while fetching node schedulable statuses info"

error:
  description: This field typically holds information about the error that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the node whose schedulable status was fetched.
  type: str
  returned: when external ID is provided
  sample: "f28e7475-f835-42ef-ac35-ecbc48d5421e"

total_available_results:
  description: The total number of available NodeSchedulableStatus entries in PC.
  type: int
  returned: when all node schedulable statuses are fetched (no ext_id supplied)
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
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
    )

    return module_args


def _fetch_node_schedulable_statuses(module, api_instance, kwargs):
    try:
        return api_instance.list_node_schedulable_status(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching node schedulable statuses info",
        )


def get_node_schedulable_status_by_ext_id(module, api_instance, result):
    """List and locally filter by ext_id.

    The underlying SDK exposes only a list endpoint; there is no get-by-id
    for NodeSchedulableStatus. We fetch the list (optionally scoped by
    cluster_ext_id) and return the entry matching the caller-supplied ext_id.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    kwargs = {}
    if module.params.get("cluster_ext_id"):
        kwargs["X_Cluster_Id"] = module.params.get("cluster_ext_id")

    resp = _fetch_node_schedulable_statuses(module, api_instance, kwargs)

    resp = strip_internal_attributes(resp.to_dict())
    entries = resp.get("data") or []

    match = next(
        (entry for entry in entries if entry.get("ext_id") == ext_id),
        None,
    )
    if match is None:
        module.fail_json(
            msg=(
                "Node schedulable status with ext_id '{0}' not found in the "
                "listed results.".format(ext_id)
            ),
            **result,
        )

    result["response"] = match


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

    resp = _fetch_node_schedulable_statuses(module, api_instance, kwargs)

    resp = strip_internal_attributes(resp.to_dict())
    metadata = resp.get("metadata") or {}
    total_available_results = metadata.get("total_available_results")
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
    api_instance = get_virtual_switch_nodes_info_api_instance(module)
    if module.params.get("ext_id"):
        get_node_schedulable_status_by_ext_id(module, api_instance, result)
    else:
        get_node_schedulable_statuses(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
