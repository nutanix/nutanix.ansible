#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_network_segments_info_v2
short_description: Get cluster network segments info
version_added: "2.7.0"
description:
    - Fetch a specific network segment using external ID, or list network
      segments for a cluster when C(ext_id) is not provided.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get Cluster Network Segment) -
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
      - Network Segment UUID used to fetch a specific network segment.
    type: str
  filter:
    description:
      - A URL query parameter that allows clients to filter a collection of
        resources.
      - The filter can be applied to the following fields - name, serviceName
    type: str
  page:
    description:
      - A URL query parameter that specifies the page number of the result set.
    type: int
  limit:
    description:
      - A URL query parameter that specifies the total number of records
        returned in the result set.
    type: int
  orderby:
    description:
      - A URL query parameter that allows clients to specify the sort criteria
        for the returned list of objects.
    type: str
  select:
    description:
      - A URL query parameter that allows clients to request a specific set of
        properties for each entity.
    type: str
  expand:
    description:
      - A URL query parameter that allows clients to request related resources
        when a resource that satisfies a particular request is retrieved.
      - Supported expand value is C(ipPool).
    type: str
  fetch_all:
    description:
      - When C(true), paginate through the list API until all available entities
        are returned. C(page) and C(limit) are ignored; each request uses the
        maximum page size (100).
      - When C(false), return a single page (API default limit).
      - Does not apply when fetching a single entity by C(ext_id).
    type: bool
    required: false
    default: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get network segment by ext_id
  nutanix.ncp.ntnx_cluster_network_segments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "63311404-8b2e-4dbf-9e33-7848cc88d330"
  register: result

- name: List all network segments for a cluster
  nutanix.ncp.ntnx_cluster_network_segments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result

- name: List network segments with filter
  nutanix.ncp.ntnx_cluster_network_segments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    filter: "name eq 'ansible-backplane-segment'"
  register: result

- name: List network segments with expand
  nutanix.ncp.ntnx_cluster_network_segments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    expand: "ipPool"
  register: result

- name: List network segments with limit
  nutanix.ncp.ntnx_cluster_network_segments_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    limit: 1
  register: result

- name: List all network segments with fetch_all
  nutanix.ncp.ntnx_cluster_network_segments_info_v2:
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
    - Response for fetching network segments info.
    - One network segment if C(ext_id) is provided.
    - List of network segments if C(ext_id) is not provided.
  returned: always
  type: dict
  sample: {}
ext_id:
  description:
    - The external ID of the network segment.
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
  sample: "Failed generating network segments info Spec"
total_available_results:
  description: The total number of available network segments in PC.
  returned: when all network segments are fetched
  type: int
  sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_network_segments_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_network_segment  # noqa: E402
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
        filter=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
        orderby=dict(type="str"),
        select=dict(type="str"),
        expand=dict(type="str"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def get_network_segment_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_network_segment(module, api_instance, cluster_ext_id, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_network_segments(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating network segments info Spec", **result)

    try:
        resp = list_entities(
            api_instance.list_network_segments_by_cluster_id,
            kwargs=kwargs,
            clusterExtId=cluster_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching network segments info",
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
        skip_info_args=True,
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
        get_network_segment_using_ext_id(module, api_instance, result)
    else:
        get_network_segments(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
