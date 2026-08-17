#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_notifications_info_v2
short_description: Fetch LCM upgrade notification details in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about an LCM (Life Cycle Manager)
    upgrade notification resource in Nutanix Prism Central.
  - The notification resource is created by M(nutanix.ncp.ntnx_notification_v2)
    (the compute-notifications API). Its external ID must be supplied to this
    module.
  - The LCM notifications API does not expose a list endpoint; C(ext_id) is
    required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Get LCM upgrade notification by ext_id) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  ext_id:
    description:
      - External ID of the LCM upgrade notification resource.
      - Typically obtained from the C(ext_id) returned by
        M(nutanix.ncp.ntnx_notification_v2).
    type: str
    required: true
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
- name: Get LCM upgrade notification details using ext_id
  nutanix.ncp.ntnx_lcm_notifications_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5"
  register: notification_info
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LCM Notifications info v4 API.
    - It contains the computed LCM upgrade notification for the supplied external
      ID, including all per-entity notification items with severity, target
      version, hypervisor type, and location information.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_id": null,
        "ext_id": "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5",
        "links": null,
        "notifications": [
            {
                "details": [
                    {
                        "message": "Host will enter maintenance mode during upgrade.",
                        "severity_level": "WARNING"
                    }
                ],
                "entity_class": "PC CORE CLUSTER",
                "entity_model": "Calm Policy Engine",
                "entity_type": "SOFTWARE",
                "entity_version": "3.8.0",
                "ext_id": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
                "hardware_family": null,
                "hypervisor_type": null,
                "location_info": null,
                "notification_type": "ENTITY",
                "to_version": "4.1.0"
            }
        ],
        "tenant_id": null
    }

ext_id:
  description: External ID of the LCM upgrade notification resource that was fetched.
  returned: when external ID is provided
  type: str
  sample: "b9c1a8a0-1e5f-4e07-9c9e-90a1c2d3e4f5"

changed:
  description: This indicates whether the module made any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status/error message emitted by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching LCM notification info using external identifier of the notification"

error:
  description: Error details if the module failed.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the module failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_notifications_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_notification  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_notification_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_notification(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    if resp is None:
        result["response"] = None
    else:
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
        "response": None,
        "failed": False,
    }

    api_instance = get_notifications_api_instance(module)
    get_notification_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
