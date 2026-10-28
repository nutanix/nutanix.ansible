#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_guest_reboot_policies_info_v2
short_description: Fetch Guest Reboot Policies info
version_added: "2.7.0"
description:
    - Fetch a Guest Reboot Policy using its external ID or list all the Guest Reboot Policies
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - The external ID of the Guest Reboot Policy.
            - If provided, fetches a single Guest Reboot Policy.
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Guest Reboot Policy by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Self-Service Admin (deprecated),
      Super Admin, Virtual Machine Admin, Virtual Machine Operator
    - >-
      B(List all the Guest Reboot Policies) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager, Self-Service Admin (deprecated),
      Super Admin, Virtual Machine Admin, Virtual Machine Operator
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get a Guest Reboot Policy using ext_id
  nutanix.ncp.ntnx_guest_reboot_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "54fe0ed5-02d8-4588-b10b-3b9736bf3d06"
  register: result

- name: List all Guest Reboot Policies
  nutanix.ncp.ntnx_guest_reboot_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List Guest Reboot Policies using filter
  nutanix.ncp.ntnx_guest_reboot_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'guest-reboot-policy-later'"
  register: result

- name: List Guest Reboot Policies with limit
  nutanix.ncp.ntnx_guest_reboot_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all Guest Reboot Policies with fetch_all
  nutanix.ncp.ntnx_guest_reboot_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching Guest Reboot Policy info.
        - One Guest Reboot Policy if C(ext_id) is provided.
        - List of multiple Guest Reboot Policies if C(ext_id) is not provided.
    returned: always
    type: dict
    sample:
        {
            "categories": [
                {
                    "ext_id": "2530b04f-3203-47e7-ae20-a3d617024688"
                }
            ],
            "create_time": "2027-01-12T07:13:51.724117+00:00",
            "created_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            },
            "description": "Reboot the guest at the given time",
            "ext_id": "c673c650-4afe-419c-59b0-441a645df9e9",
            "links": null,
            "name": "guest-reboot-policy-later",
            "project_ext_id": null,
            "reboot_schedule": {
                "day_of_week": "SUNDAY",
                "time_of_day": "02:30"
            },
            "tenant_id": null,
            "update_time": "2027-01-12T07:13:52.055646+00:00",
            "updated_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000"
            }
        }
ext_id:
    description:
        - The external ID of the Guest Reboot Policy.
    returned: when C(ext_id) is provided
    type: str
    sample: "c673c650-4afe-419c-59b0-441a645df9e9"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Failed generating Guest Reboot Policies info Spec"
total_available_results:
    description: The total number of available Guest Reboot Policies in PC.
    returned: when Guest Reboot Policies are listed
    type: int
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_guest_reboot_policies_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_guest_reboot_policy  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_guest_reboot_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_guest_reboot_policy(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_guest_reboot_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Guest Reboot Policies info Spec", **result)

    try:
        resp = list_entities(
            api_instance.list_guest_reboot_policies,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Guest Reboot Policies info",
        )

    result["total_available_results"] = resp.metadata.total_available_results
    resp_data = strip_internal_attributes(resp.to_dict()).get("data")
    result["response"] = resp_data if resp_data else []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_guest_reboot_policies_api_instance(module)

    if module.params.get("ext_id"):
        get_guest_reboot_policy_using_ext_id(module, api_instance, result)
    else:
        get_guest_reboot_policies(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
