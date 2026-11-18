#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_point_stores_info_v2
short_description: Fetch recovery point stores info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about recovery point stores in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific recovery point store.
  - If C(ext_id) is not provided, list multiple recovery point stores optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get recovery point store by ext_id) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List recovery point stores) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  ext_id:
    description:
      - The external ID of the recovery point store.
      - When provided, only the recovery point store with the matching external ID is returned.
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
- name: Get recovery point store using ext_id
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2bb43b2f-488c-4422-8e56-4f4866bf768c"
  register: result
  ignore_errors: true

- name: List all recovery point stores
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List recovery point stores with filter on name
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'MyRecoveryPointStore_1'"
  register: result
  ignore_errors: true

- name: List recovery point stores with limit
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List all recovery point stores with fetch_all
  nutanix.ncp.ntnx_recovery_point_stores_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Recovery Point Store info v4 API.
    - It can be a single recovery point store if external ID is provided.
    - List of multiple recovery point stores if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "bucket": {
        "bucket_name": "my-bucket",
        "provider": "AWS_S3",
        "provider_config": {
          "$objectType": "common.v1.config.AmazonS3Bucket",
          "bucket_url": "https://s3.amazonaws.com/my-bucket",
          "region": "us-west-2"
        }
      },
      "current_logical_usage_bytes": 71,
      "ext_id": "2bb43b2f-488c-4422-8e56-4f4866bf768c",
      "is_healthy": false,
      "links": null,
      "name": "MyRecoveryPointStore_1",
      "owner_ext_id": "c29b0a9e-64db-4cbd-848c-a2bd02fe6b3f",
      "tenant_id": null
    }

ext_id:
  description: External ID of the recovery point store.
  type: str
  returned: when external ID is provided
  sample: "2bb43b2f-488c-4422-8e56-4f4866bf768c"

total_available_results:
  description: The total number of available recovery point stores in PC.
  type: int
  returned: when listing all recovery point stores
  sample: 5

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching recovery point stores info"

error:
  description: This field typically holds information about if the task has errors that occurred during execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false
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
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_recovery_point_store_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_recovery_point_store(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_recovery_point_stores(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating recovery point stores info spec", **result
        )

    try:
        resp = list_entities(
            api_instance.list_recovery_point_stores,
            kwargs=kwargs,
        )
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_recovery_point_stores_api_instance(module)
    if module.params.get("ext_id"):
        get_recovery_point_store_using_ext_id(module, api_instance, result)
    else:
        list_recovery_point_stores(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
