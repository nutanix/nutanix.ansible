#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_protection_info_v2
short_description: Fetch protection status for a Nutanix cluster
version_added: 2.6.0
description:
  - Fetch the protection status of a given cluster.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Get protection status for a cluster) -
    Required Roles: Cluster Admin, Cluster Viewer, Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - External ID of the cluster whose protection info is requested.
    type: str
    required: true
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get protection info for a cluster
  nutanix.ncp.ntnx_clusters_protection_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
  register: result
"""

RETURN = r"""
response:
  description:
    - Cluster protection information.
  type: dict
  returned: always
  sample:
    {
      "cluster_ext_id": "00064ff3-8bf0-8ab9-2afa-525400a07915",
      "failure_reason": null,
      "protected_entities": [
          {
              "entity_type": "vm",
              "protected_count": 1,
              "unprotected_count": 0
          },
          {
              "entity_type": "volume",
              "protected_count": 0,
              "unprotected_count": 0
          }
      ],
      "protection_rpo_minutes": 60,
      "protection_state": "PROTECTED",
      "protection_target": "LOCAL",
      "target_protection_state": "PROTECTED"
    }
changed:
    description:
        - Indicates if any changes were made during the operation.
    type: bool
    returned: always
    sample: true
failed:
    description: Indicates if the protection info operation failed.
    type: bool
    returned: always
    sample: false
ext_id:
    description:
        - The external ID of the cluster whose protection info is requested.
    type: str
    returned: always
    sample: "00064ff3-8bf0-8ab9-2afa-525400a07915"
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_protection_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_cluster_protection_info,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def fetch_cluster_protection_info(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_cluster_protection_info(
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
    result = {"changed": False, "response": None}
    api_instance = get_cluster_protection_api_instance(module)
    fetch_cluster_protection_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
