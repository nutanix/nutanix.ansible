#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_point_stores_info_v2
short_description: Fetch recovery point stores info in Nutanix Prism Central
version_added: 2.7.0
description:
    - This module allows you to fetch recovery point stores info in Nutanix Prism Central.
    - A recovery point store references object storage used to hold recovery points with
      Multicloud Snapshot Technology (MST). It can use any S3-compatible backend, including
      Nutanix Objects and hyperscaler offerings such as Amazon S3 and Microsoft Azure Blob Storage.
    - If C(ext_id) is provided, fetch a particular recovery point store info using external ID.
    - If C(ext_id) is not provided, fetch multiple recovery point stores info with/without using
      filters, limit, etc.
    - This module uses PC v4 APIs based SDKs.
notes:
    - This module talks to Prism Central (PC), not to FCVM/Foundation.
    - >-
      This module requires the appropriate Nutanix IAM roles/permissions to be assigned to the
      user performing the operation. Refer to the SDK/API documentation for the exact roles
      required to read recovery point stores on Prism Central.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
    ext_id:
        description:
            - External identifier of the recovery point store.
            - If provided, a single recovery point store is fetched using this external ID.
        type: str
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
- name: Fetch recovery point store using external id
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
  register: result

- name: List all recovery point stores
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
  register: result

- name: List recovery point stores with filter
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    filter: "name eq 'recovery_point_store_name'"
  register: result

- name: List recovery point stores with limit
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    limit: 1
  register: result
"""
RETURN = r"""
response:
    description:
        - The response from the Nutanix recovery point stores info v4 API. This module talks to
          Prism Central (PC).
        - It can be a single recovery point store if external ID is provided.
        - List of multiple recovery point stores if external ID is not provided with optional
          filter or limit.
    returned: always
    type: dict
    sample:
        {
            "bucket": {
                "bucket_name": "recovery-point-store-bucket",
                "provider": "NUTANIX_OBJECTS",
                "provider_config": {
                    "auth_credentials": null,
                    "bucket_name": "recovery-point-store-bucket",
                    "end_point": "https://10.1.2.100"
                }
            },
            "current_logical_usage_bytes": 0,
            "ext_id": "1ca2963d-77b6-453a-ae23-2c19e7a954a3",
            "is_healthy": true,
            "links": null,
            "name": "recovery_point_store_ansible",
            "owner_ext_id": "00000000-0000-0000-0000-000000000000",
            "tenant_id": null
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
    sample: "Api Exception raised while fetching recovery point stores info"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution.
    type: str
    returned: when an error occurs
    sample: null

failed:
    description: This field typically holds information about if the task have failed.
    returned: when something fails
    type: bool
    sample: false

ext_id:
    description: External ID of the recovery point store.
    type: str
    returned: when external ID is provided
    sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"

total_available_results:
    description: The total number of available recovery point stores in PC.
    type: int
    returned: when all recovery point stores are fetched
    sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_stores_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_recovery_point_store,
)
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


def get_recovery_point_store_using_ext_id(module, recovery_point_stores, result):
    ext_id = module.params.get("ext_id")
    resp = get_recovery_point_store(module, recovery_point_stores, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_recovery_point_stores(module, recovery_point_stores, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating recovery point stores info spec", **result
        )

    try:
        resp = recovery_point_stores.list_recovery_point_stores(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching recovery point stores info",
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
    result = {"changed": False, "error": None, "response": None}
    recovery_point_stores = get_recovery_point_stores_api_instance(module)
    if module.params.get("ext_id"):
        get_recovery_point_store_using_ext_id(module, recovery_point_stores, result)
    else:
        get_recovery_point_stores(module, recovery_point_stores, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
