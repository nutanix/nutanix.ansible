#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_non_migratable_vms_info_v2
short_description: Get non-migratable VMs result by ID
version_added: "2.7.0"
description:
    - Get the details of non-migratable VMs for a cluster using the result
      external ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get Cluster Non Migratable Vms Result) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
    type: str
    required: true
  ext_id:
    description:
      - UUID of the result storing the non-migratable VMs.
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
- name: Get non-migratable VMs result by ID
  nutanix.ncp.ntnx_non_migratable_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "63311404-8b2e-4dbf-9e33-7848cc88d330"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for fetching non-migratable VMs result info.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "cc8edc49-3282-40d8-b17f-7880c7722a61",
        "links": null,
        "tenant_id": null,
        "vms": [
            {
                "host_ip": {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "180.178.15.134"
                    },
                    "ipv6": null
                },
                "non_migratable_vm_reason": "Test reason for non-migratable VM",
                "vm_name": "Test VM Name",
                "vm_uuid": "7d460c38-b100-4897-9140-ca7348abbd0b"
            }
        ]
    }
ext_id:
  description:
    - The external ID of the non-migratable VMs result.
  returned: always
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: >-
    Api Exception raised while fetching non-migratable VMs result using
    ext_id
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_non_migratable_vms_result,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_non_migratable_vms_result_using_ext_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_non_migratable_vms_result(module, api_instance, cluster_ext_id, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_clusters_api_instance(module)
    get_non_migratable_vms_result_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
