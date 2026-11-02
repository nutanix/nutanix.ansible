#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_hosts_by_cluster_id_info_v2
short_description: List hosts associated with a Nutanix cluster
version_added: "2.7.0"
description:
  - List all hosts associated with a cluster identified by cluster external ID.
  - Supports optional filter, limit, page, orderby, select, and fetch_all.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Cluster Host) -
    Required Roles: Backup Admin, Cluster Admin, Cluster Viewer,
    LocalAccountManager Admin, LocalAccountManager Viewer, NCM Connector,
    Network Infra Admin, Prism Admin, Prism Viewer, Project Manager,
    Super Admin, VPC Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
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
- name: List hosts for a cluster
  nutanix.ncp.ntnx_hosts_by_cluster_id_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: List hosts for a cluster with filter
  nutanix.ncp.ntnx_hosts_by_cluster_id_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    filter: "hostName eq 'host1'"
  register: result
  ignore_errors: true

- name: List hosts for a cluster with limit
  nutanix.ncp.ntnx_hosts_by_cluster_id_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    limit: 5
  register: result
  ignore_errors: true

- name: List all hosts for a cluster with fetch_all
  nutanix.ncp.ntnx_hosts_by_cluster_id_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC hosts by cluster ID info v4 API.
    - List of hosts for the given cluster with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
      "host_name": "host1",
      "host_type": "HYPER_CONVERGED"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching hosts by cluster id info"

error:
  description: This indicates the error message if any error occurred
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available hosts for the cluster.
  type: int
  returned: always
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict(
        cluster_ext_id=dict(type="str", required=True),
    )


def get_hosts_by_cluster_id(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating hosts by cluster id info spec", **result
        )

    cluster_ext_id = module.params.get("cluster_ext_id")

    try:
        resp = list_entities(
            api_instance.list_hosts_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching hosts by cluster id info",
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
    api_instance = get_clusters_api_instance(module)
    get_hosts_by_cluster_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
