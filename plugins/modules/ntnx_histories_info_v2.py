#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_histories_info_v2
short_description: Fetch LCM history information from Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to fetch information about History in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific History.
    - If C(ext_id) is not provided, list multiple History optionally filtered / paginated.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get details about an LCM history entry by external ID.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
      Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - >-
      B(List LCM history entries.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
      Security Dashboard Admin, Security Dashboard Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    ext_id:
        description:
            - The external ID (UUID) of the LCM history entry.
            - When provided, the module returns a single history entry.
            - When omitted, the module returns a list of history entries.
        type: str
        required: false
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
- name: List all LCM history entries
  nutanix.ncp.ntnx_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: histories

- name: List LCM history entries with limit
  nutanix.ncp.ntnx_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 2
  register: histories_limited

- name: List LCM history entries filtered by operation status
  nutanix.ncp.ntnx_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "operationStatus eq 'FAILED'"
  register: failed_histories

- name: Fetch a specific LCM history entry by external ID
  nutanix.ncp.ntnx_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d1e17f4d-9f9c-4a4b-8ff5-9c1f8e8b1c1b"
  register: history_detail
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC History info v4 API.
        - It can be a single History if external ID is provided.
        - List of multiple History if external ID is not provided with optional filter or limit.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_id": "1e9a1996-50e2-485f-a67c-22355cb43055",
            "cluster_name": "PC-cluster",
            "end_time": "2026-07-20T13:45:00.000000+00:00",
            "ext_id": "d1e17f4d-9f9c-4a4b-8ff5-9c1f8e8b1c1b",
            "framework_version": "3.1.0",
            "links": null,
            "operation_info": {
                "component_details": [
                    {
                        "entity_class": "PC CORE CLUSTER",
                        "entity_model": "Calm Policy Engine",
                        "from_version": "3.7.0",
                        "to_version": "4.0.0"
                    }
                ]
            },
            "operation_status": "SUCCEEDED",
            "operation_type": "UPGRADE",
            "start_time": "2026-07-20T13:30:00.000000+00:00",
            "tenant_id": null,
            "user_info": {
                "user_name": "admin",
                "user_uuid": "00000000-0000-0000-0000-000000000000"
            }
        }

changed:
    description: Whether the module made any changes. Always false for info modules.
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the LCM history entry.
    returned: when external ID is provided
    type: str
    sample: "d1e17f4d-9f9c-4a4b-8ff5-9c1f8e8b1c1b"

msg:
    description: This indicates the message if any message occurred.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching LCM histories info"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    returned: When an error occurs
    type: str
    sample: "Failed generating info spec for LCM histories"

failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false

total_available_results:
    description: The total number of available LCM history entries in PC.
    returned: when all LCM histories are fetched
    type: int
    sample: 12
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_lcm_histories_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_lcm_history  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_history_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_history(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_histories(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating info spec for LCM histories", **result)

    try:
        resp = api_instance.list_lcm_histories(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching LCM histories info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_lcm_histories_api_instance(module)
    if module.params.get("ext_id"):
        get_history_using_ext_id(module, api_instance, result)
    else:
        get_histories(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
