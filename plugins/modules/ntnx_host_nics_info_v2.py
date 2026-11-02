#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_host_nics_info_v2
short_description: List host NICs across Nutanix Prism Central
version_added: "2.7.0"
description:
  - List all host NICs for all clusters attached to Prism Central.
  - Supports optional filter, limit, page, orderby, select, and fetch_all.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Host Nic) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin,
    Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options: {}
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
- name: List all host NICs
  nutanix.ncp.ntnx_host_nics_info_v2:
  register: result
  ignore_errors: true

- name: List host NICs with filter
  nutanix.ncp.ntnx_host_nics_info_v2:
    filter: "name eq 'eth0'"
  register: result
  ignore_errors: true

- name: List host NICs with limit
  nutanix.ncp.ntnx_host_nics_info_v2:
    limit: 5
  register: result
  ignore_errors: true

- name: List host NICs with ordering
  nutanix.ncp.ntnx_host_nics_info_v2:
    orderby: "name desc"
  register: result
  ignore_errors: true

- name: List host NICs with selection
  nutanix.ncp.ntnx_host_nics_info_v2:
    select: "name,extId,macAddress"
  register: result
  ignore_errors: true

- name: List all host NICs with fetch_all
  nutanix.ncp.ntnx_host_nics_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC host NICs info v4 API.
    - List of host NICs with optional filter, limit, orderby, or select.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "084af8fb-87f8-46e6-a2f4-cabeffc81850",
      "name": "eth1",
      "mac_address": "ac:1f:6b:6f:9e:49",
      "link_capacity_in_mbps": 1000
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
  sample: "Api Exception raised while fetching host NICs info"

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
  description: The total number of available host NICs matching the query.
  type: int
  returned: always
  sample: 4
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
    return dict()


def get_host_nics(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating host NICs info spec", **result)

    try:
        resp = list_entities(api_instance.list_host_nics, kwargs=kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching host NICs info",
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
    get_host_nics(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
