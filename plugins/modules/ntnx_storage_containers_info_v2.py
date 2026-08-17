#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_containers_info_v2
short_description: Fetch StorageContainer info from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about StorageContainer in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific StorageContainer.
  - If C(ext_id) is not provided, list multiple StorageContainer optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs (C(ntnx_storage_py_client)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get Storage Container by ext_id) -
      Required Roles: Backup Admin, Consumer, CSI System, Developer, Kubernetes Data Services System, NCM Connector, Operator, Prism Admin, Prism Viewer,
      Project Admin, Project Manager, Storage Admin, Storage Viewer, Super Admin
    - >-
      B(List Storage Containers) -
      Required Roles: Backup Admin, Consumer, CSI System, Developer, Kubernetes Data Services System, NCM Connector, Operator, Prism Admin, Prism Viewer,
      Project Admin, Project Manager, Storage Admin, Storage Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  ext_id:
    description:
      - The external ID of the Storage Container.
      - If not provided, multiple Storage Container info entries will be fetched.
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
- name: Fetch a specific Storage Container using its external ID
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6"
  register: result
  ignore_errors: true

- name: List all Storage Containers
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Storage Containers with filter
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'sc_ansible_full_updated'"
  register: result
  ignore_errors: true

- name: List Storage Containers with limit
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC StorageContainer info v4 API.
    - It can be a single StorageContainer if external ID is provided.
    - List of multiple StorageContainer if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "advertised_capacity_bytes": null,
      "affinity_host_ext_id": null,
      "cache_deduplication": "OFF",
      "cluster_ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
      "cluster_name": "auto-cluster-prod",
      "compression_delay_secs": 0,
      "container_ext_id": "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6",
      "erasure_code": "OFF",
      "erasure_code_delay_secs": null,
      "explicit_reserved_capacity_bytes": 0,
      "ext_id": "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6",
      "has_higher_ec_fault_domain_preference": false,
      "implicit_reserved_capacity_bytes": 0,
      "is_compression_enabled": false,
      "is_encrypted": null,
      "is_inline_ec_enabled": false,
      "is_internal": false,
      "is_marked_for_removal": false,
      "is_nfs_whitelist_inherited": true,
      "is_software_encryption_enabled": false,
      "links": null,
      "max_capacity_bytes": 4291605771923,
      "name": "sc_ansible_full",
      "nfs_whitelist_address": null,
      "on_disk_dedup": "OFF",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "replication_factor": 2,
      "storage_pool_ext_id": "487c142e-6c41-4b10-9585-4feac6bd3c68",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the Storage Container.
  returned: when external ID is provided
  type: str
  sample: "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6"

total_available_results:
  description: The total number of available Storage Containers in PC.
  returned: when all Storage Containers are fetched
  type: int
  sample: 5

msg:
  description: Status or error message set on specific code paths.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching storage containers info"

error:
  description: The error message if an error occurs.
  returned: when an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false
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


def get_storage_container_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_storage_container(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_storage_containers(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating storage containers info spec", **result)

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
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_storage_container_api_instance(module)
    if module.params.get("ext_id"):
        get_storage_container_by_ext_id(module, api_instance, result)
    else:
        get_storage_containers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
