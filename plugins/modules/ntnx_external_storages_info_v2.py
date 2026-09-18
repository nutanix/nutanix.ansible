#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_external_storages_info_v2
short_description: Fetch external storages info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch external storages info or a specific external storage in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch a particular external storage info using its external ID.
  - If C(ext_id) is not provided, fetch multiple external storages info with/without using filters, limit, etc.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get an External Storage by ext_id) -
    Required Roles: Prism Admin, Prism Viewer, Storage Admin, Super Admin
  - >-
    B(Get list of External Storages) -
    Required Roles: Prism Admin, Prism Viewer, Storage Admin, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID (UUID) of the external storage.
      - If provided, a single external storage is returned.
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
- name: Get external storage using ext_id
  nutanix.ncp.ntnx_external_storages_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all external storages
  nutanix.ncp.ntnx_external_storages_info_v2:
  register: result
  ignore_errors: true

- name: List external storages with filter
  nutanix.ncp.ntnx_external_storages_info_v2:
    filter: "name eq 'external_storage_ansible'"
  register: result
  ignore_errors: true

- name: List external storages with limit
  nutanix.ncp.ntnx_external_storages_info_v2:
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix external storages info v4 API. The host is Prism Central (PC).
    - It can be a single external storage if external ID is provided.
    - It is a list of multiple external storages if external ID is not provided, with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
      "config": {
        "protection_domain_name": "pd-01",
        "storage_pool_id": "sp-id-01",
        "storage_pool_name": "sp-01",
        "system_id": "powerflex-system-01",
        "username": "admin"
      },
      "end_point_address": {
        "fqdn": null,
        "ipv4": {
          "prefix_length": 32,
          "value": "10.44.76.100"
        },
        "ipv6": null
      },
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "free_capacity_bytes": null,
      "health": null,
      "links": null,
      "name": "external_storage_ansible",
      "owner_ext_id": null,
      "provider_type": "DELL_POWERFLEX",
      "tenant_id": null,
      "total_capacity_bytes": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching external storages info"

error:
  description: This field typically holds information about any errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the external storage.
  type: str
  returned: When external ID is provided
  sample: "7bea69e9-684c-4736-7805-d658ee17c1b6"

total_available_results:
  description: The total number of available external storages in PC.
  type: int
  returned: When all external storages are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_external_storages_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_external_storage  # noqa: E402
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


def get_external_storage_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_external_storage(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_external_storages(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating external storages info spec", **result)

    try:
        resp = api_instance.list_external_storages(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching external storages info",
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
    api_instance = get_external_storages_api_instance(module)
    if module.params.get("ext_id"):
        get_external_storage_using_ext_id(module, api_instance, result)
    else:
        get_external_storages(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
