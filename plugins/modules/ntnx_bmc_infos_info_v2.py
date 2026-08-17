#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_bmc_infos_info_v2
short_description: Fetch BMC (Baseboard Management Controller) info of a host in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about the BMC (Baseboard Management Controller)
    of a host that belongs to a cluster registered with Nutanix Prism Central.
  - The v4.2 clustermgmt API only exposes a Get-by-host endpoint for BMC info (there is no
    list endpoint), so both C(cluster_ext_id) and C(ext_id) are required.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get BMC info of a host) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the host whose BMC info should be fetched.
    type: str
    required: true
  cluster_ext_id:
    description:
      - The external ID of the cluster that owns the host.
    type: str
    required: true
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
"""

EXAMPLES = r"""
- name: Fetch BMC info of a host
  nutanix.ncp.ntnx_bmc_infos_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: bmc_info
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC BmcInfo info v4 API.
    - Always a single BMC info entity for the given (cluster_ext_id, ext_id).
  returned: always
  type: dict
  sample:
    {
        "credential": {
            "password": null,
            "username": "ADMIN"
        },
        "ip_address": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.60.10"
            },
            "ipv6": null
        },
        "status": "VALID"
    }

ext_id:
  description:
    - The external ID of the host whose BMC info was fetched.
  returned: always
  type: str
  sample: "8300384a-56ee-4750-aeb8-3d1c42908bee"

cluster_ext_id:
  description:
    - The external ID of the cluster that owns the host.
  returned: always
  type: str
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

changed:
  description: Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching BMC info using cluster and host ext_id"

error:
  description: Error details if any.
  returned: When an error occurs
  type: str

failed:
  description: True on failure.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_bmc_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_bmc_info  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_bmc_info_by_ids(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("ext_id")
    resp = get_bmc_info(module, api_instance, cluster_ext_id, host_ext_id)
    result["ext_id"] = host_ext_id
    result["cluster_ext_id"] = cluster_ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "cluster_ext_id": None,
    }
    api_instance = get_bmc_api_instance(module)
    get_bmc_info_by_ids(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
