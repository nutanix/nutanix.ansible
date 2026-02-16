#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_password_managers_info_v2
short_description: Lists password status of system user accounts.
version_added: 2.3.0
description:
    - This module retrieves the password status of system user accounts in Nutanix Clusters.
    - It uses the Nutanix Clusters Management API to fetch the password status of system users.
    - This module uses PC v4 APIs based SDKs.
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List password status of all system users
  nutanix.ncp.ntnx_password_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
  register: password_status

- name: List password status of system users with filter
  nutanix.ncp.ntnx_password_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    filter: "username eq 'admin'"
  register: list_passwords

- name: List password status of system users with limit
  nutanix.ncp.ntnx_password_managers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    limit: 1
  register: limited_passwords
"""

RETURN = r"""
response:
    description: List of system user accounts with their password status.
    returned: always
    type: list
    elements: dict
    sample: [
            {
                "cluster_ext_id": "9e0ea08a-131e-446c-80f7-5c3f30cac3a8",
                "expiry_time": "2025-08-15T00:00:00+00:00",
                "ext_id": "4f8c3c0a-35e4-4756-8c5e-9626e286fba3",
                "has_hsp_in_use": false,
                "host_ip": null,
                "last_update_time": "2025-06-16T00:00:00+00:00",
                "links": null,
                "status": "SECURE",
                "system_type": "PC",
                "tenant_id": null,
                "username": "admin"
            },
            {
                "cluster_ext_id": "0006361c-7362-d20d-0686-aa2b410069e0",
                "expiry_time": "2025-07-26T00:00:00+00:00",
                "ext_id": "91bf4349-9bc6-43c8-9062-7ea3b71e644c",
                "has_hsp_in_use": false,
                "host_ip": null,
                "last_update_time": "2025-05-27T00:00:00+00:00",
                "links": null,
                "status": "DEFAULT",
                "system_type": "AOS",
                "tenant_id": null,
                "username": "admin"
            },
            {
                "cluster_ext_id": "0006361c-7362-d20d-0686-aa2b410069e0",
                "expiry_time": "2038-01-19T03:14:07+00:00",
                "ext_id": "11dd35d6-788f-44c4-926b-4c90f484f85e",
                "has_hsp_in_use": false,
                "host_ip": null,
                "last_update_time": "2025-05-27T00:00:00+00:00",
                "links": null,
                "status": "SECURE",
                "system_type": "AOS",
                "tenant_id": null,
                "username": "nutanix"
            },
            {
                "cluster_ext_id": "9e0ea08a-131e-446c-80f7-5c3f30cac3a8",
                "expiry_time": "2038-01-19T03:14:07+00:00",
                "ext_id": "6f822a04-fa06-44a7-9785-23f52e9e3a72",
                "has_hsp_in_use": false,
                "host_ip": null,
                "last_update_time": "2025-05-01T00:00:00+00:00",
                "links": null,
                "status": "DEFAULT",
                "system_type": "PC",
                "tenant_id": null,
                "username": "nutanix"
            },
            {
                "cluster_ext_id": "0006361c-7362-d20d-0686-aa2b410069e0",
                "expiry_time": "2038-01-19T00:00:00+00:00",
                "ext_id": "009438ea-1863-4795-6dfc-28fbcf90122f",
                "has_hsp_in_use": false,
                "host_ip": {
                    "prefix_length": null,
                    "value": "10.97.99.55"
                },
                "last_update_time": "2025-05-27T00:00:00+00:00",
                "links": null,
                "status": "SECURE",
                "system_type": "AHV",
                "tenant_id": null,
                "username": "root"
            }
        ]
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching password status of system users info"
error:
    description: The error message if an error occurs.
    type: str
    returned: always
changed:
    description: Indicates whether the module made any changes.
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_password_manager_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_password_status_system_users(module, result):
    password_manager_api = get_password_manager_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        result["error"] = err
        module.fail_json(
            "Failed creating query parameters for password status of system user info"
        )
    resp = None
    try:
        resp = password_manager_api.list_system_user_passwords(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching password status of system users info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        support_proxy=True,
        argument_spec=dict(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    get_password_status_system_users(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
