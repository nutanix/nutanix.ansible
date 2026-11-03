#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_ip_pools_info_v2
short_description: Get cluster IP pools info
version_added: "2.7.0"
description:
    - Fetch a specific IP pool using external ID, or list IP pools for a
      cluster when C(ext_id) is not provided.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get Cluster IP Pool) -
      Required Roles: Backup Admin, Cluster Admin, Cluster Viewer, Prism Admin,
      Prism Viewer, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
    type: str
    required: true
  ext_id:
    description:
      - IP Pool UUID used to fetch a specific IP pool.
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
- name: Get IP pool by ext_id
  nutanix.ncp.ntnx_cluster_ip_pools_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "63311404-8b2e-4dbf-9e33-7848cc88d330"
  register: result

- name: List all IP pools for a cluster
  nutanix.ncp.ntnx_cluster_ip_pools_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result

- name: List IP pools with filter
  nutanix.ncp.ntnx_cluster_ip_pools_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    filter: "name eq 'ansible-ip-pool'"
  register: result

- name: List IP pools with limit
  nutanix.ncp.ntnx_cluster_ip_pools_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    limit: 1
  register: result

- name: List all IP pools with fetch_all
  nutanix.ncp.ntnx_cluster_ip_pools_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching IP pools info.
    - One IP pool if C(ext_id) is provided.
    - List of IP pools if C(ext_id) is not provided.
  returned: always
  type: dict
  sample:
    [
        {
            "ext_id": "f8832e28-0bb5-4a5e-af73-ed65711b7522",
            "is_in_use": false,
            "links": null,
            "name": "ansible-ip-pool-updated",
            "netmask": {
                "ipv4": {
                    "prefix_length": null,
                    "value": "255.255.255.0"
                },
                "ipv6": null
            },
            "ranges": [
                {
                    "end_address": {
                        "ipv4": {
                            "prefix_length": null,
                            "value": "10.77.88.40"
                        },
                        "ipv6": null
                    },
                    "start_address": {
                        "ipv4": {
                            "prefix_length": null,
                            "value": "10.77.88.30"
                        },
                        "ipv6": null
                    }
                }
            ],
            "tenant_id": null,
            "type": "PE_IP_POOL"
        }
    ]
ext_id:
  description:
    - The external ID of the IP pool.
  returned: when C(ext_id) is provided
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false
error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "f8832e28-0bb5-4a5e-af73-ed65711b7522"
total_available_results:
  description: The total number of available IP pools in PC.
  returned: when all IP pools are fetched
  type: int
  sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_network_segments_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_ip_pool  # noqa: E402
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


def get_ip_pool_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_ip_pool(module, api_instance, cluster_ext_id, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_ip_pools(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating IP pools info Spec", **result)

    try:
        resp = list_entities(
            api_instance.list_ip_pools_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching IP pools info",
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
    api_instance = get_network_segments_api_instance(module)
    if module.params.get("ext_id"):
        get_ip_pool_using_ext_id(module, api_instance, result)
    else:
        get_ip_pools(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
