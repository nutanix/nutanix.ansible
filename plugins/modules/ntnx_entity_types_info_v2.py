#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_types_info_v2
short_description: Fetch AIOps stats entity types for a source in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about AIOps EntityTypesV4 in Nutanix Prism Central.
  - EntityTypesV4 lists the entity types (e.g. C(vm), C(cluster), C(node), C(container), C(virtual_disk), etc.)
    for which the AIOps stats gateway can serve config and stats data for a given source.
  - The parent AIOps source (for example the built-in C(nutanix) source) is looked up via the sources API
    and its external ID is passed as C(source_ext_id).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get list of Entity Types for a source) -
    Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin,
    Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  source_ext_id:
    description:
      - The external ID (UUID) of the AIOps stats source.
      - Use C(ntnx_entity_types_info_v2) only with a source that has been returned by the AIOps
        sources list API. On a standard Prism Central the built-in source is named C(nutanix).
    type: str
    required: true
  read_timeout:
    description:
      - Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all entity types supported by an AIOps source
  nutanix.ncp.ntnx_entity_types_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    source_ext_id: "db293e8a-5770-c3c7-4213-85dbbc1d3679"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC EntityTypesV4 info v4 API.
    - It is a list of entity types (dicts) exposed by the given AIOps stats C(source_ext_id).
    - Each entity type exposes an C(entity_type_name) (e.g. C(vm), C(cluster)) and the corresponding
      C(ext_id) that can then be used with the AIOps stats/config APIs.
  returned: always
  type: dict
  sample:
    [
      {
        "entity_type_name": "vm",
        "ext_id": "686c821a-8091-4aef-8224-65b48019cd34",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "virtual_disk",
        "ext_id": "d9eb3ca3-5e7b-4d02-8327-5ba58e9cd407",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "cluster",
        "ext_id": "06b2d4b9-1b5c-9eaa-8c20-a1c270f95b3c",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "storagecontainerstats",
        "ext_id": "3f06ebab-4d62-a2ca-7e83-2592f9e8051e",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "virtual_nic",
        "ext_id": "45ef8942-694d-6cf5-8333-a711c0be4b2b",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "volume_group_config",
        "ext_id": "f149d727-ae8b-1abe-1656-2ff59fe06c13",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "node",
        "ext_id": "36c45369-96ca-5615-dcf9-911f068786dc",
        "links": null,
        "tenant_id": null
      },
      {
        "entity_type_name": "container",
        "ext_id": "5f0b6ebc-4bea-1028-5ba2-b8a6ce78b863",
        "links": null,
        "tenant_id": null
      }
    ]

source_ext_id:
  description: External ID of the AIOps stats source whose entity types were fetched.
  returned: always
  type: str
  sample: "db293e8a-5770-c3c7-4213-85dbbc1d3679"

total_available_results:
  description: Total number of entity types available for the given source in PC.
  returned: when entity types are fetched successfully
  type: int
  sample: 8

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching entity types for source ext_id: db293e8a-5770-c3c7-4213-85dbbc1d3679"

error:
  description: This field typically holds information about errors that occurred during task execution
  returned: when an error occurs
  type: str

failed:
  description: This field indicates whether the task failed
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_stats_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_entity_types  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        source_ext_id=dict(type="str", required=True),
    )
    return module_args


def list_entity_types(module, stats_api, result):
    source_ext_id = module.params.get("source_ext_id")
    result["source_ext_id"] = source_ext_id

    resp = get_entity_types(module, stats_api, source_ext_id)

    resp_dict = strip_internal_attributes(resp.to_dict())
    metadata = resp_dict.get("metadata") or {}
    result["total_available_results"] = metadata.get("total_available_results")

    data = resp_dict.get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "source_ext_id": None,
    }
    stats_api = get_stats_api_instance(module)
    list_entity_types(module, stats_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
