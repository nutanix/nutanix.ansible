#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_recovery_info_v2
short_description: Fetch cluster recovery information
version_added: 2.6.0
description:
  - Fetch the recovery information for a given cluster.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get cluster recovery information) -
    Required Roles: Cluster Admin, Cluster Viewer, Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - External ID of the cluster whose recovery info is requested.
    type: str
    required: true
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get recovery info for a cluster
  nutanix.ncp.ntnx_clusters_recovery_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0006b8c9-1c1c-5c4c-1111-111111111111"
  register: result
"""

RETURN = r"""
response:
  description:
    - Cluster recovery information.
  type: dict
  returned: always
  sample:
    {
      "recovery_status": "RECOVERING",
      "subnets": []
    }
ext_id:
  description: External ID of the cluster whose info was fetched.
  type: str
  returned: always
msg:
  description: Message if an error occurred while fetching the info.
  type: str
  returned: when an error occurs
error:
  description: Error message if any.
  type: str
  returned: when an error occurs
changed:
  description: Indicates if any change was made.
  type: bool
  returned: always
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_protection_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_cluster_recovery_info,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def fetch_cluster_recovery_info(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_cluster_recovery_info(
        module=module,
        api_instance=api_instance,
        ext_id=ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_cluster_protection_api_instance(module)
    fetch_cluster_recovery_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
