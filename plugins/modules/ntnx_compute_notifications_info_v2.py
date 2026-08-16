#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_compute_notifications_info_v2
short_description: Fetch a LCM compute-notification resource details from Nutanix Prism Central.
version_added: 2.7.0
description:
    - This module allows you to fetch information about a LCM compute-notification resource
      created by the C(ntnx_lcm_compute_notification_v2) module.
    - If C(ext_id) is provided, fetch details of the specific compute-notification resource.
    - The LCM notifications API only exposes a get-by-id endpoint; a list endpoint is not
      available, so C(ext_id) is mandatory for this module.
    - The compute-notification resource is server-managed and remains valid for one hour after
      it is created by the compute-notifications action.
    - This module uses PC v4 APIs based SDKs.
options:
    ext_id:
        description:
            - The external ID of the LCM compute-notification resource.
            - Obtained from the C(ext_id) return value of C(ntnx_lcm_compute_notification_v2)
              or from the C(completion_details) of the corresponding LCM task.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Fetch a LCM compute-notification resource.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch LCM compute-notification resource using external ID
  nutanix.ncp.ntnx_compute_notifications_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: notification_info
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC LCM compute-notification info v4 API.
        - Returns the details of a single compute-notification resource identified by
          C(ext_id).
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_id": "00062db4-a450-e685-0fda-cdf9ca935bfd",
            "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
            "links": null,
            "notifications": [
                {
                    "details": [
                        {
                            "message": "Some hosts will be rebooted during the upgrade.",
                            "severity_level": "WARNING"
                        }
                    ],
                    "entity_class": "PC CORE CLUSTER",
                    "entity_model": "Calm Policy Engine",
                    "entity_type": "SOFTWARE",
                    "entity_version": "4.0.0",
                    "ext_id": "3c196eac-e1d5-4c8a-9b01-c133f6907ca2",
                    "hardware_family": null,
                    "hypervisor_type": null,
                    "location_info": {
                        "location_name": null,
                        "location_type": "PC",
                        "uuid": "1e9a1996-50e2-485f-a67c-22355cb43055"
                    },
                    "notification_type": "ENTITY",
                    "to_version": "4.1.0"
                }
            ],
            "tenant_id": null
        }

ext_id:
    description: The external ID of the LCM compute-notification resource.
    returned: always
    type: str
    sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
    description: Whether the module made any changes. Always false for info modules.
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching LCM compute-notification info using external identifier of the resource"

error:
    description: This field holds the error details if an error occurred during the API call.
    returned: When an error occurs
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
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_notifications_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_notification  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the argument spec for the compute-notifications info module."""

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )

    return module_args


def get_notification_using_ext_id(module, api_instance, result):
    """Fetch a single LCM compute-notification resource by external ID."""
    ext_id = module.params.get("ext_id")
    resp = get_lcm_notification(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    """Ansible entry point for the compute-notifications info module."""
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "ext_id": None, "failed": False}

    api_instance = get_notifications_api_instance(module)
    get_notification_using_ext_id(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
