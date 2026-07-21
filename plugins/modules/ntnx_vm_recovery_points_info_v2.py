#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_points_info_v2
short_description: Fetch AHV VM recovery point info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about AHV VM recovery points in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific AHV VM recovery point.
  - If C(ext_id) is not provided, list multiple AHV VM recovery points optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get an AHV VM recovery point by ext_id) -
      Required Roles: Backup Admin, Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer,
      Super Admin, Self-Service Admin (deprecated)
    - >-
      B(List AHV VM recovery points) -
      Required Roles: Backup Admin, Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer,
      Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - A globally unique identifier of an AHV VM recovery point. It should be of type UUID.
      - If provided, only that recovery point is returned.
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
- name: Get AHV VM recovery point by external ID
  nutanix.ncp.ntnx_vm_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
  register: result

- name: List all AHV VM recovery points
  nutanix.ncp.ntnx_vm_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List AHV VM recovery points with filter
  nutanix.ncp.ntnx_vm_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'ansible-vm-rp'"
  register: result

- name: List AHV VM recovery points with limit
  nutanix.ncp.ntnx_vm_recovery_points_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AHV VM recovery point info v4 API.
    - It can be a single AHV VM recovery point if external ID is provided.
    - List of multiple AHV VM recovery points if external ID is not provided
      with optional filter, limit or pagination.
  returned: always
  type: dict
  sample:
    {
      "application_consistent_properties": null,
      "consistency_group_ext_id": null,
      "creation_time": "2026-07-21T05:12:31.912+00:00",
      "disk_recovery_points": [
        {
          "disk_ext_id": "839feff9-bac0-4a70-9523-82ea9e431517",
          "disk_recovery_point_ext_id": "21d467f0-ccef-4733-91cc-f04db58a92eb"
        }
      ],
      "expiration_time": "2027-01-01T00:00:00+00:00",
      "ext_id": "b387359d-fa5c-4d58-9eb2-3af1a4976319",
      "links": null,
      "location_agnostic_id": "51264897-07a8-4292-831b-ae28a37135e5",
      "name": "ansible-vm-rp",
      "recovery_point_type": "CRASH_CONSISTENT",
      "status": "COMPLETE",
      "tenant_id": null,
      "total_exclusive_usage_bytes": 0,
      "vm": null,
      "vm_categories": null,
      "vm_ext_id": "ac5aff0c-6c68-4948-9088-b903e2be0ce7"
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching AHV VM recovery points info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the AHV VM recovery point.
  type: str
  returned: when external ID is provided
  sample: "b387359d-fa5c-4d58-9eb2-3af1a4976319"

total_available_results:
  description: The total number of available AHV VM recovery points on Prism Central.
  type: int
  returned: when AHV VM recovery points are listed
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_vm_recovery_points_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm_recovery_point  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_vm_recovery_point_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    entity = get_vm_recovery_point(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(entity.to_dict())


def list_vm_recovery_points(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating AHV VM recovery points info spec", **result
        )

    try:
        resp = api_instance.list_vm_recovery_points(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching AHV VM recovery points info",
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
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_recovery_points_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_recovery_point_by_ext_id(module, api_instance, result)
    else:
        list_vm_recovery_points(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
