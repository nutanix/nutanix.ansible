#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_histories_info_v2
short_description: Fetch information about LCM histories from Nutanix Prism Central
version_added: 2.5.0
description:
    - This module allows you to fetch information about LcmHistory in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific LcmHistory.
    - If C(ext_id) is not provided, list multiple LcmHistory optionally filtered / paginated.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get details about a particular LCM history entry.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List summary of the queried LCM histories.) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    ext_id:
        description:
            - The external ID of the LCM history entry to fetch.
            - If provided, only the specific LCM history entry is returned.
            - If omitted, a list of LCM history entries is returned (subject to
              the optional filter / limit / page / orderby / select parameters).
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all LCM histories
  nutanix.ncp.ntnx_lcm_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: lcm_histories

- name: List LCM histories with pagination and limit
  nutanix.ncp.ntnx_lcm_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    page: 0
    limit: 5
  register: lcm_histories_page

- name: List LCM histories filtered by operation type
  nutanix.ncp.ntnx_lcm_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "operationType eq Lcm.Common.OperationType'INVENTORY'"
  register: lcm_histories_filtered

- name: List LCM histories sorted by startTime descending
  nutanix.ncp.ntnx_lcm_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "startTime desc"
    limit: 10
  register: lcm_histories_sorted

- name: Fetch a particular LCM history entry using external ID
  nutanix.ncp.ntnx_lcm_histories_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "3c196eac-e1d5-4c8a-9b01-c133f6907ca2"
  register: lcm_history_entry
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC LcmHistory info v4 API.
        - It can be a single LcmHistory if external ID is provided.
        - List of multiple LcmHistory if external ID is not provided with optional filter or limit.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_id": "cae459ec-08db-475e-a5e5-151e390c9484",
            "cluster_name": "PC_10.44.76.29",
            "end_time": "2026-07-20T14:22:30.494290+00:00",
            "ext_id": "623e010a-b8ad-5d14-aad9-5ff7ce4177ff",
            "framework_version": "3.4.86535",
            "links": null,
            "operation_info": null,
            "operation_status": "FAILED",
            "operation_type": "INVENTORY",
            "start_time": "2026-07-20T14:20:30.741951+00:00",
            "tenant_id": null,
            "user_info": {
                "user_name": "admin",
                "user_uuid": "00000000-0000-0000-0000-000000000000"
            }
        }
ext_id:
    description: The external ID of the LCM history entry.
    type: str
    returned: when a single entity is fetched
    sample: "623e010a-b8ad-5d14-aad9-5ff7ce4177ff"
total_available_results:
    description: The total number of available LCM history entries in PC.
    type: int
    returned: when all LCM history entries are fetched
    sample: 32
changed:
    description: Whether the module made any changes. Always false for info modules.
    type: bool
    returned: always
    sample: false
failed:
    description: Whether the module failed.
    type: bool
    returned: always
    sample: false
msg:
    description: Status/error message.
    type: str
    returned: When there is an error
    sample: "Api Exception raised while fetching LCM histories info"
error:
    description: Error details if any error occurred.
    type: str
    returned: When an error occurs
    sample: "Failed to generate info spec for LCM histories"
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_lcm_history_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_lcm_history(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_lcm_histories(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed to generate info spec for LCM histories", **result)

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
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }

    api_instance = get_lcm_histories_api_instance(module)
    if module.params.get("ext_id"):
        get_lcm_history_using_ext_id(module, api_instance, result)
    else:
        get_lcm_histories(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
