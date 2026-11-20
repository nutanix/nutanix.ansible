#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_remote_subnets_info_v2
short_description: Fetch remote subnets info discovered under a Prism Element cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch remote subnets info discovered under a
    Prism Element cluster in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular remote subnet using its external ID.
  - If C(ext_id) is not provided, fetch multiple remote subnets with/without using
    filters, limit, etc.
  - C(cluster_ext_id) is required — the discovery endpoint is scoped to a single
    Prism Element cluster.
  - The Remote Subnet resource is a B(read-only) discovery surface; create, update
    and delete are not supported.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(View Remote Subnet) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Super Admin, Tenant Admin, VPC Admin
    - >-
      B(View Remote Subnet) (List) -
      Required Roles: Account Owner, Administrator, Network Infra Admin, Prism Admin, Super Admin, Tenant Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  cluster_ext_id:
    description:
      - External ID of the Prism Element cluster that owns the remote subnet(s).
      - Maps to the API path parameter C(clusterExtId).
      - Required for both list and get-by-id operations.
    type: str
    required: true
  ext_id:
    description:
      - External ID of a specific remote subnet to fetch.
      - Maps to the API path parameter C(extId) for get-by-id.
      - When provided, the module fetches only that remote subnet (get-by-id).
      - When omitted, the module lists remote subnets for the cluster.
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
- name: Fetch a remote subnet using its external ID
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all remote subnets discovered on a Prism Element cluster
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true

- name: List remote subnets with a filter
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    filter: "startswith(name, 'C')"
  register: result
  ignore_errors: true

- name: List remote subnets with a limit
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    limit: 1
  register: result
  ignore_errors: true

- name: List remote subnets sorted by name descending
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    orderby: "name desc"
  register: result
  ignore_errors: true

- name: List remote subnets using pagination
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    page: 0
    limit: 10
  register: result
  ignore_errors: true

- name: List all remote subnets with fetch_all
  nutanix.ncp.ntnx_cluster_remote_subnets_info_v2:
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC remote subnets info v4 API.
    - It can be a single remote subnet if external ID is provided.
    - List of multiple remote subnets if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "bridge_name": null,
      "cluster_name": "PE-01",
      "cluster_name_list": null,
      "cluster_reference": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "cluster_reference_list": null,
      "description": null,
      "dhcp_options": null,
      "dynamic_ip_addresses": null,
      "external_dhcp_servers": null,
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "hypervisor_type": "AHV",
      "ip_config": null,
      "ip_prefix": null,
      "ip_usage": null,
      "is_advanced_networking": null,
      "is_external": false,
      "is_nat_enabled": false,
      "layer2_stretch_reference": null,
      "links": null,
      "metadata": null,
      "migration_state": null,
      "name": "remote_subnet_ansible",
      "network_function_chain_reference": null,
      "network_id": 373,
      "reserved_ip_addresses": null,
      "subnet_type": "VLAN",
      "tenant_id": null,
      "virtual_switch": null,
      "virtual_switch_reference": null,
      "vpc": null,
      "vpc_name": null,
      "vpc_reference": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

msg:
  description: This indicates the message associated with the operation, primarily on error.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching remote subnets info"

ext_id:
  description: External ID of the remote subnet that was fetched (only when ext_id was provided).
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

cluster_ext_id:
  description: External ID of the Prism Element cluster used to scope the fetch/list.
  type: str
  returned: always
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

total_available_results:
  description: The total number of remote subnets discovered on the given Prism Element cluster.
  type: int
  returned: when all remote subnets are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_remote_entities_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_remote_subnet_for_cluster,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_remote_subnet_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_remote_subnet_for_cluster(module, api_instance, cluster_ext_id, ext_id)
    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_remote_subnets(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating remote subnets info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_remote_subnets_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching remote subnets info",
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
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
            ("ext_id", "fetch_all"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "cluster_ext_id": None,
    }
    api_instance = get_remote_entities_api_instance(module)
    if module.params.get("ext_id"):
        get_remote_subnet_using_ext_id(module, api_instance, result)
    else:
        get_remote_subnets(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
