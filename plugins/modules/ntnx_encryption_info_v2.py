#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_encryption_info_v2
short_description: Fetch encryption configuration of a cluster in Nutanix Prism Central
description:
  - This module allows you to fetch the data-at-rest encryption configuration of a cluster in Nutanix Prism Central.
  - The encryption configuration is fetched using the external ID of the cluster.
  - This module uses PC v4 APIs based SDKs.
version_added: 2.7.0
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get the encryption configuration of a cluster) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the cluster whose encryption configuration is to be fetched.
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
- name: Get encryption configuration of a cluster using cluster ext_id
  nutanix.ncp.ntnx_encryption_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix encryption info v4 API.
    - This module talks to Prism Central (PC).
    - It returns the encryption configuration of a single cluster identified by the external ID provided.
    - The encryption configuration is fetched per cluster; there is no list operation for this entity.
  returned: always
  type: dict
  sample:
    {
      "kms_spec": {
          "external_kms_ext_ids": null,
          "kms_type": "NATIVE_LOCAL"
      },
      "last_key_backup_time": null,
      "last_key_gen_time": "2026-09-18T06:26:47.167906+00:00",
      "scope": "CLUSTER",
      "type": [
          "SOFTWARE"
      ]
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the cluster whose encryption configuration was fetched.
  returned: when external ID is provided
  type: str
  sample: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any occurred.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching encryption config using cluster ext_id"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_encryption_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_encryption_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_encryption_config_info(module, api_instance, result):
    cluster_ext_id = module.params.get("ext_id")
    result["ext_id"] = cluster_ext_id
    resp = get_encryption_config(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_encryption_api_instance(module)
    get_encryption_config_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
