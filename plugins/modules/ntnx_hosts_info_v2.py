#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_hosts_info_v2
short_description: Retrieve information about Nutanix hosts from PC
version_added: "2.7.0"
description:
  - List all host entities across clusters registered to Prism Central.
  - Fetch particular host info using external ID and cluster external ID.
  - Fetch hosts associated with a cluster using C(cluster_ext_id).
  - Supports optional filter, limit, page, orderby, select, and fetch_all.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Host) -
    Required Roles: Cluster Admin, Cluster Viewer, NCM Connector,
    Network Infra Admin, Prism Admin, Prism Viewer, Storage Admin, Super Admin,
    Tenant Admin, Tenant Consumer, Virtual Machine Admin,
    Virtual Machine Operator, VPC Admin
  - >-
    B(View Cluster Host) -
    Required Roles: Backup Admin, Cluster Admin, Cluster Viewer,
    LocalAccountManager Admin, LocalAccountManager Viewer, NCM Connector,
    Network Infra Admin, Prism Admin, Prism Viewer, Project Manager,
    Super Admin, VPC Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the host.
      - If not provided, multiple hosts info will be fetched.
    type: str
  cluster_ext_id:
    description:
      - The external ID of the cluster to filter hosts by.
      - Required together with C(ext_id) when fetching a single host.
      - If provided without C(ext_id), hosts for the specified cluster are listed.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
  - Pradeepsingh Bhati (@bhati-pradeep)
"""

EXAMPLES = r"""
- name: List all hosts
  nutanix.ncp.ntnx_hosts_info_v2:
  register: result
  ignore_errors: true

- name: List hosts with filter
  nutanix.ncp.ntnx_hosts_info_v2:
    filter: "hostName eq 'host1'"
  register: result
  ignore_errors: true

- name: List hosts with limit
  nutanix.ncp.ntnx_hosts_info_v2:
    limit: 5
  register: result
  ignore_errors: true

- name: List hosts by cluster external ID
  nutanix.ncp.ntnx_hosts_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true

- name: Get host by external ID
  nutanix.ncp.ntnx_hosts_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
  register: result
  ignore_errors: true

- name: List all hosts with fetch_all
  nutanix.ncp.ntnx_hosts_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC hosts info v4 API.
    - A single host when C(ext_id) is provided.
    - List of hosts when C(ext_id) is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
      "host_name": "ansible_ag",
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
  sample: "Api Exception raised while fetching hosts info"

error:
  description: This indicates the error message if any error occurred
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the host when requested via C(ext_id).
  type: str
  returned: When external ID is provided
  sample: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"

total_available_results:
  description: The total number of available hosts matching the query.
  type: int
  returned: When a list call is made
  sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_host  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
    )


def get_host_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = get_host(module, api_instance, ext_id, cluster_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_hosts(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating hosts info spec", **result)

    cluster_ext_id = module.params.get("cluster_ext_id")
    try:
        if cluster_ext_id:
            resp = list_entities(
                api_instance.list_hosts_by_cluster_id,
                kwargs=kwargs,
                clusterExtId=cluster_ext_id,
            )
        else:
            resp = list_entities(api_instance.list_hosts, kwargs=kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching hosts info",
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
        mutually_exclusive=[("ext_id", "filter")],
        required_by={"ext_id": ["cluster_ext_id"]},
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    if module.params.get("ext_id"):
        get_host_by_ext_id(module, api_instance, result)
    else:
        get_hosts(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
