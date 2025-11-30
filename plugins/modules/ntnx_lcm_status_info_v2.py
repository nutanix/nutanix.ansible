#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_lcm_status_info_v2
short_description: Get the LCM framework status.
description: Get the LCM framework status.
version_added: "2.1.0"
author:
  - George Ghawali (@george-ghawali)
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster.
      - It is used to fetch the LCM status on a particular cluster, it gives Prism Central's LCM status if nothing passed.
      - If we give PE cluster's external ID, it will give PE cluster's LCM status.
      - We can get the external ID of the cluster using ntnx_clusters_info_v2 module.
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
- name: Get LCM status
  nutanix.ncp.ntnx_lcm_status_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00062e00-87eb-ef15-0000-00000000b71a"
  register: lcm_status
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LCM Status API.
    - It contains details like the ongoing operations on the LCM.
  type: dict
  returned: always
  sample:
    {
      "ext_id": null,
      "framework_version": {
          "available_version": "3.1.56788",
          "current_version": "3.1.56788",
          "is_update_needed": false
      },
      "in_progress_operation": {
          "operation_id": null,
          "operation_type": null
      },
      "is_cancel_intent_set": false,
      "links": null,
      "tenant_id": null,
      "upload_task_uuid": null
    }
changed:
    description:
        - Indicates whether the module has made any changes.
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_status_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_lcm_status  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=False),
    )

    return module_args


def lcm_status(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = get_lcm_status(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():

    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("cluster_ext_id", "filter"),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
    }

    api_instance = get_status_api_instance(module)

    lcm_status(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
