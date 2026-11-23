#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_ssh_access_control_info_v2
short_description: Fetch external SSH access control of a cluster
version_added: "2.7.0"
description:
  - This module allows you to fetch the external SSH access control
    configuration of a cluster in Nutanix Prism Central.
  - SSH access control is a singleton resource per cluster, identified
    by the cluster external ID.
  - There is no list operation for external SSH access control; it is
    always fetched for a specific cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned
    to the user performing the operation.
  - >-
    B(Get External SSH Access Control) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin,
    Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster whose external SSH access control
        is to be fetched.
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
- name: Get external SSH access control of a cluster
  nutanix.ncp.ntnx_cluster_ssh_access_control_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix external SSH access control info v4
      API.
    - It returns the external SSH access control configuration of a
      single cluster identified by the external ID provided.
    - The SSH access control is fetched per cluster; there is no list
      operation for this entity.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "00065ffe-0266-379f-0000-000000028f57",
      "is_password_login_enabled": true,
      "is_ssh_enabled": true,
      "links": [],
      "ssh_access_inconsistency_details": [],
      "tenant_id": "00065ffe-0266-379f-0000-000000028f57"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the cluster whose external SSH access control was fetched.
  returned: always
  type: str
  sample: "00065ffe-0266-379f-0000-000000028f57"

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_ssh_control_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_external_ssh_access_control,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_external_ssh_access_control_info(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id
    resp = get_external_ssh_access_control(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_ssh_control_api_instance(module)
    get_external_ssh_access_control_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
