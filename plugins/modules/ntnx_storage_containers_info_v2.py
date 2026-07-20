#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_containers_info_v2
short_description: Retrieve information about Nutanix AllStorageContainer entities from PC
version_added: 2.5.0
description:
  - This module allows you to fetch information about AllStorageContainer in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific AllStorageContainer.
  - If C(ext_id) is not provided, list multiple AllStorageContainer optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs (ntnx_storage_py_client).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get storage container by ext_id) -
    Required Roles: Backup Admin, Consumer, Developer, Operator, Prism Admin, Prism Viewer,
    Project Admin, Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(List Storage Containers) -
    Required Roles: Backup Admin, Consumer, Developer, Operator, Prism Admin, Prism Viewer,
    Project Admin, Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external ID of the AllStorageContainer.
      - If not provided, multiple AllStorageContainer will be fetched (with optional filter/limit/pagination).
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
- name: Fetch storage container using external ID
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
  register: result

- name: Fetch all storage containers
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch storage containers with filter
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'ansible_all_sc'"
  register: result

- name: Fetch first 3 storage containers
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 3
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC AllStorageContainer info v4 API.
    - It can be a single AllStorageContainer if external ID is provided.
    - List of multiple AllStorageContainer if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "advertised_capacity_bytes": null,
      "affinity_host_ext_id": null,
      "cache_deduplication": "OFF",
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "cluster_name": "auto_cluster_prod_36acf9b012ca",
      "compression_delay_secs": 0,
      "container_ext_id": "08a07de0-78d4-4a94-9bfe-8162017726fd",
      "erasure_code": "OFF",
      "ext_id": null,
      "has_higher_ec_fault_domain_preference": false,
      "is_compression_enabled": false,
      "is_encrypted": null,
      "is_inline_ec_enabled": false,
      "is_internal": false,
      "is_marked_for_removal": false,
      "is_nfs_whitelist_inherited": true,
      "is_software_encryption_enabled": false,
      "max_capacity_bytes": 4404802450302,
      "name": "objectsm4fcfc2cab9c149024297e51c16b5d841",
      "on_disk_dedup": "OFF",
      "owner_ext_id": null,
      "replication_factor": 1,
      "storage_pool_ext_id": "df233a93-0480-4f15-a500-1269696fc4b2",
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the AllStorageContainer if provided in input.
  returned: when a single AllStorageContainer is fetched
  type: str
  sample: "57516342-7d8e-470f-91b8-ae310737ff8c"

total_available_results:
  description:
    - The total number of available AllStorageContainer entities in PC.
  returned: when all AllStorageContainer are fetched
  type: int
  sample: 12

changed:
  description: This indicates whether the task resulted in any changes (always false for info).
  returned: always
  type: bool
  sample: false

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

error:
  description: The error message if an error occurs.
  returned: when an error occurs
  type: str

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching storage container info"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_storage_container_api_instance,
)
from ..module_utils.v4.storage.helpers import get_storage_container  # noqa: E402
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


def get_storage_container_by_ext_id(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    resp = get_storage_container(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_storage_containers(module, result, api_instance):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json(
            msg="Failed generating query parameters for fetching storage containers info",
            **result,
        )
    resp = None
    try:
        resp = api_instance.get_all_storage_containers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage containers info",
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
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_storage_container_api_instance(module)
    if module.params.get("ext_id"):
        get_storage_container_by_ext_id(module, result, api_instance)
    else:
        get_storage_containers(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
