#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_containers_info_v2
short_description: Retrieve information about Nutanix storage continer from PC
version_added: 2.0.0
description:
    - This module retrieves information about Nutanix storage continer from PC.
    - Fetch particular storage continer info using external ID
    - Fetch multiple storage continers info with/without using filters, limit, etc.
options:
  ext_id:
    description:
      - The external ID of the storage continer.
      - If not provided, multiple storage continer info will be fetched.
    type: str
    required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: fetch storage continer info using external ID
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
  register: result

- name: fetch all storage continer info
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: fetch all storage continer info with filter
  nutanix.ncp.ntnx_storage_containers_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: "name eq 'storage_container_name'"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching storage container info.
        - Returns storage container info if ext_id is provided or list of multiple storage containers.
    type: dict
    returned: always
    sample:
     {
                "affinity_host_ext_id": null,
                "cache_deduplication": "OFF",
                "cluster_ext_id": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1",
                "cluster_name": "auto-cluster-prod-f30accd2eec1",
                "compression_delay_secs": 0,
                "container_ext_id": "547c01c4-19c2-4293-8a9c-43441c18d0c7",
                "erasure_code": "OFF",
                "erasure_code_delay_secs": null,
                "ext_id": null,
                "has_higher_ec_fault_domain_preference": false,
                "is_compression_enabled": false,
                "is_encrypted": null,
                "is_inline_ec_enabled": false,
                "is_internal": false,
                "is_marked_for_removal": false,
                "is_nfs_whitelist_inherited": true,
                "is_software_encryption_enabled": false,
                "links": [
                    {
                        "href": "https://000.000.000.000:9440/api/clustermgmt/v4.0.b2/config/storage-containers/547c01c4-19c2-4293-8a9c-43441c18d0c7",
                        "rel": "storage-container"
                    },
                    {
                        "href": "https://000.000.000.000:9440/api/clustermgmt/v4.0.b2/stats/storage-containers/547c01c4-19c2-4293-8a9c-43441c18d0c7",
                        "rel": "storage-container-stats"
                    }
                ],
                "logical_advertised_capacity_bytes": null,
                "logical_explicit_reserved_capacity_bytes": 0,
                "logical_implicit_reserved_capacity_bytes": 0,
                "max_capacity_bytes": 4365702025514,
                "name": "SelfServiceContainer",
                "nfs_whitelist_address": null,
                "on_disk_dedup": "OFF",
                "owner_ext_id": "00000000-0000-0000-0000-000000000000",
                "replication_factor": 1,
                "storage_pool_ext_id": "487c142e-6c41-4b10-9585-4feac6bd3c68",
                "tenant_id": null
            }
error:
    description: The error message if an error occurs.
    type: str
    returned: when an error occurs
ext_id:
    description:
        - The external ID of the storage container if given in input.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_storage_containers_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_storage_container  # noqa: E402
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


def get_storage_container_by_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    storage_containers = get_storage_containers_api_instance(module)
    resp = get_storage_container(module, storage_containers, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_storage_containers(module, result):
    storage_containers = get_storage_containers_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json(
            "Failed creating query parameters for fetching storage containers info"
        )
    resp = None
    try:
        resp = storage_containers.list_storage_containers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching storage containers info",
        )

    if getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = []


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_storage_container_by_ext_id(module, result)
    else:
        get_storage_containers(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
