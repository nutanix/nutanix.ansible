#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_config_info_v2
short_description: Fetch the storage configuration of a Nutanix cluster in Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch the storage configuration of a Nutanix cluster in Prism Central.
  - Storage configuration is a singleton resource per cluster, identified by the cluster external ID.
  - The cluster external ID (C(cluster_ext_id)) is required as the storage configuration is scoped to a single cluster.
  - There is no list operation for storage configuration; it is always fetched for a specific cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get Storage Configuration) -
    Required Roles: Prism Admin, Prism Viewer, Storage Admin, Super Admin.
  - This module talks to Prism Central (PC), not to FCVM/Foundation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose storage configuration is to be fetched.
      - Required to fetch the storage configuration.
    type: str
    required: false
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
- name: Get storage configuration of a cluster
  nutanix.ncp.ntnx_storage_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix storage config info v4 API.
    - This module talks to Prism Central (PC).
    - It returns the storage configuration of the cluster identified by C(cluster_ext_id).
  returned: always
  type: dict
  sample:
    {
      "is_delayed_maintenance_resiliency_enabled": true,
      "is_rebuild_reservation_enabled": false,
      "is_rf1_enabled": false,
      "resilient_capacity_warning_threshold_percentage": 75,
      "storage_over_provisioning_caution_threshold": -1.0
    }

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: The external ID of the cluster whose storage configuration was fetched.
  returned: always
  type: str
  sample: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching storage config using cluster ext_id"

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_storage_config_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_storage_config  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=False),
    )
    return module_args


def get_storage_config_of_cluster(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    validate_required_params(module, ["cluster_ext_id"])
    resp = get_storage_config(module, api_instance, cluster_ext_id)
    result["ext_id"] = cluster_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_storage_config_api_instance(module)
    get_storage_config_of_cluster(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
