#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_protected_resources_info_v2
short_description: Module to fetch protected resource in Nutanix Prism Central.
description:
  - This module can be used to fetch protected resources in Nutanix Prism Central.
options:
  ext_id:
    description:
      - The external identifier of a protected VM or volume group used to retrieve the protected resource.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get a protected resource
    nutanix.ncp.ntnx_protected_resources_info_v2:
        nutanix_host: "{{ ip }}"
        nutanix_username: "{{ username }}"
        nutanix_password: "{{ password }}"
        ext_id: "8951bad7-1f37-4d3c-98e1-abb7faed05ed"
    register: result
    ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Protected resource details
        - It could be a VM or volume group details.
    returned: always
    type: dict
    sample:
        {
            "category_fq_names": [
                "KAJeMdivRayTansible-categorykey3/KAJeMdivRayTansible-categoryvalue3"
            ],
            "consistency_group_ext_id": null,
            "entity_ext_id": "f215097c-bbc4-4e13-4d7d-9e59c81a25f6",
            "entity_type": "VM",
            "ext_id": null,
            "links": null,
            "replication_states": [
                {
                    "protection_policy_ext_id": null,
                    "recovery_point_objective_seconds": 0,
                    "replication_status": "IN_SYNC",
                    "target_site_reference": {
                        "cluster_ext_id": "00062db4-a450-e685-0fda-cdf9ca935bfd",
                        "mgmt_cluster_ext_id": "1e9a1996-50e2-485f-a67c-22355cb43055"
                    }
                }
            ],
            "site_protection_info": [
                {
                    "location_reference": {
                        "cluster_ext_id": "00062e78-6aad-7a5a-0000-00000000b717",
                        "mgmt_cluster_ext_id": "6fb777a0-14b4-4dec-9216-a8e0153a18ee"
                    },
                    "recovery_info": null,
                    "synchronous_replication_role": "PRIMARY"
                }
            ],
            "source_site_reference": {
                "cluster_ext_id": "00062e78-6aad-7a5a-0000-00000000b717",
                "mgmt_cluster_ext_id": "6fb777a0-14b4-4dec-9216-a8e0153a18ee"
        }

ext_id:
    description: The external identifier of a protected VM or volume group.
    returned: always
    type: str
    sample: "8951bad7-1f37-4d3c-98e1-abb7faed05ed"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str
    sample: false

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
"""

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protected_resource_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_protected_resource,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_protected_resource_by_id(module, result):
    protected_resource = get_protected_resource_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_protected_resource(module, protected_resource, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    ext_id = module.params.get("ext_id")
    if ext_id:
        get_protected_resource_by_id(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
