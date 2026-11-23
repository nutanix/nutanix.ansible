#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_port_capability_info_v2
short_description: Fetch port capability info for a Nutanix cluster
version_added: "2.7.0"
description:
  - This module allows you to fetch port capability information for a Nutanix cluster.
  - It fetches the capability of all ports in a cluster including whether RDMA/iSER is supported.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(View Port Capability) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin,
    Prism Viewer, Project Manager, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
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
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch port capability for a cluster
  nutanix.ncp.ntnx_cluster_port_capability_info_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC PortCapability info v4 API.
    - Capability of all ports in a cluster.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
        "last_fetched_timestamp": "2026-07-20T12:20:41.524581+00:00",
        "links": null,
        "ports": [
            {
                "is_rdma_capable": true,
                "name": "eth0",
                "port_type": "ETHERNET"
            }
        ],
        "tenant_id": null
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
  sample: "Api Exception raised while fetching port capability info"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs
failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
ext_id:
  description: External ID of the cluster whose port capability was fetched.
  type: str
  returned: When cluster_ext_id is provided
  sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_network_segments_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_port_capability(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id
    try:
        resp = api_instance.get_port_capability_by_cluster_id(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching port capability info",
        )
    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None, "failed": False}
    api_instance = get_network_segments_api_instance(module)
    get_port_capability(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
