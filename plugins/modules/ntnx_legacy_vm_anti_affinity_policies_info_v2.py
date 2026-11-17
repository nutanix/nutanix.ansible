#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_legacy_vm_anti_affinity_policies_info_v2
short_description: Fetch legacy VM-VM anti-affinity policies info from Nutanix Prism Central.
version_added: "2.7.0"
description:
    - This module fetches information about legacy VM-VM anti-affinity policies in Nutanix Prism Central.
    - It supports listing all legacy policies with optional filter, page, and limit.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List Legacy VM Anti-Affinity Policies) -
      Required Roles: Prism Admin, Prism Viewer, Project Admin, Project Manager,
      Self-Service Admin (Deprecated), Super Admin, Tenant Admin, Tenant Consumer,
      Virtual Machine Admin, Virtual Machine Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
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
- name: List all legacy VM-VM anti-affinity policies
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List legacy VM-VM anti-affinity policies with filter
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my_legacy_policy'"
  register: result

- name: List legacy VM-VM anti-affinity policies with limit
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all legacy VM-VM anti-affinity policies with fetch_all
  nutanix.ncp.ntnx_legacy_vm_anti_affinity_policies_info_v2:
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
        - Response for fetching legacy VM-VM anti-affinity policy list.
        - List of legacy VM-VM anti-affinity policies.
    type: list
    returned: always
    sample:
        [
            {
                "cluster": {
                    "ext_id": "0005cfe0-7f26-5e6a-0000-000000013179"
                },
                "ext_id": "00060a2b-5c99-5a52-ebd2-ac1f6b02d3e0",
                "links": null,
                "name": "legacy_anti_affinity_test",
                "tenant_id": null,
                "vms": [
                    {
                        "ext_id": "2f54419e-596d-4b34-aa8f-1a1e944ee7d7"
                    },
                    {
                        "ext_id": "8811743f-f3ea-463c-539a-8d6a7f69b8f5"
                    }
                ]
            }
        ]
changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when there is an error
    type: str
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching legacy VM-VM anti-affinity policies info"
total_available_results:
    description: The total number of available legacy VM-VM anti-affinity policies in PC.
    type: int
    returned: when all legacy VM-VM anti-affinity policies are fetched
    sample: 5
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
    get_vm_anti_affinity_policies_api_instance,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        filter=dict(type="str"),
        page=dict(type="int"),
        limit=dict(type="int"),
        fetch_all=dict(type="bool", required=False, default=False),
    )
    return module_args


def get_legacy_policies(module, api_instance, result):
    """List legacy VM-VM anti-affinity policies with pagination and filter support."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating legacy VM-VM anti-affinity policies info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_legacy_vm_anti_affinity_policies,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching legacy VM-VM anti-affinity policies info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_vm_anti_affinity_policies_api_instance(module)
    get_legacy_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
