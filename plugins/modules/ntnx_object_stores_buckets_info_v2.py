#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_object_stores_buckets_info_v2
short_description: Get Object Store buckets info
version_added: "2.7.0"
description:
    - Fetch details of a specific bucket in an Object store when C(bucket_name) is provided.
    - Fetch a list of the buckets in an Object store when C(bucket_name) is not provided.
    - If C(object_store_namespace) is provided with a valid federated namespace value,
      the buckets in the federated namespace are returned. Otherwise, the buckets in the
      local namespace are returned.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(View Buckets Object Store) -
      Required Roles: Objects Admin, Objects Editor, Objects Viewer, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=objects)"
options:
    object_store_ext_id:
        description:
            - The External ID of the Object Store.
        type: str
        required: true
    bucket_name:
        description:
            - The name of the bucket.
            - It must contain only lowercase letters, numbers, hyphens and dots.
            - It must start with a letter or number and end with a letter or number.
            - If provided, fetches the specific bucket; otherwise lists buckets.
        type: str
        required: false
    object_store_namespace:
        description:
            - Name of the federated namespace that this Object store belongs to.
            - It must contain only letters, numbers and hyphens but not consecutive hyphens.
            - It must start with a letter and end with a letter or number.
            - If not provided, local namespace is used.
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
- name: Get details of a specific bucket
  nutanix.ncp.ntnx_object_stores_buckets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    bucket_name: "bucket-1"
  register: result

- name: Get details of a specific bucket with namespace
  nutanix.ncp.ntnx_object_stores_buckets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    bucket_name: "bucket-1"
    object_store_namespace: "namespace-1"
  register: result

- name: List all buckets for an object store
  nutanix.ncp.ntnx_object_stores_buckets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result

- name: List buckets with filter
  nutanix.ncp.ntnx_object_stores_buckets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    filter: "name eq 'bucket-1'"
  register: result

- name: List buckets with limit
  nutanix.ncp.ntnx_object_stores_buckets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    limit: 1
  register: result

- name: List all buckets with fetch_all
  nutanix.ncp.ntnx_object_stores_buckets_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching object store buckets info.
        - Bucket details if C(bucket_name) is provided.
        - List of buckets if C(bucket_name) is not provided.
    type: dict
    returned: always
    sample:
        {
            "name": "bucket-1",
            "owner_name": "user1@example.com",
            "versioning_state": "ENABLED",
            "state": "NORMAL",
            "is_object_lock_enabled": false,
            "object_lock_retention_secs": 3600,
            "object_lock_enabled_time": "2009-09-23T14:30:00-07:00",
            "is_multi_protocol_access_enabled": true,
            "is_static_website_enabled": true,
            "is_cors_enabled": true,
            "object_count": 15000,
            "storage_usage_bytes": 5497558138880,
            "tiered_usage_bytes": 824633720832,
            "tiered_garbage_bytes": 219902325555,
            "pending_tiered_usage_bytes": 879609302220,
            "outbound_replication_status": "UNCONFIGURED",
            "inbound_replication_status": "UNCONFIGURED",
            "replication_relations": [
                {
                    "ext_id": "22262664-c65f-f854-65af-7cc25581f458",
                    "is_replication_source": false,
                    "peer": {
                        "bucket_name": "bucket-1",
                        "fqdn": "objectstore.example.com"
                    },
                    "pending_object_count": 10,
                    "pending_object_size_bytes": 1099500,
                    "last_sync_time_usecs": 1764604700000000,
                    "full_sync_pending_object_count": 10,
                    "full_sync_pending_object_size_bytes": 1099500,
                    "full_sync_progress_percentage": 50
                }
            ]
        }

bucket_name:
    description: The name of the bucket.
    returned: when C(bucket_name) is provided
    type: str
    sample: "bucket-1"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching object store buckets info"

error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false

total_available_results:
    description: The total number of available buckets for the given object store
    type: int
    returned: when buckets are listed
    sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.api_client import get_buckets_api_instance  # noqa: E402
from ..module_utils.v4.objects.helpers import get_bucket  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        object_store_ext_id=dict(type="str", required=True),
        bucket_name=dict(type="str"),
        object_store_namespace=dict(type="str"),
    )
    return module_args


def _namespace_kwargs(module):
    namespace = module.params.get("object_store_namespace")
    if namespace:
        return {"x_ntnx_objects_namespace": namespace}
    return {}


def get_bucket_by_name(module, buckets_api, result):
    object_store_ext_id = module.params.get("object_store_ext_id")
    bucket_name = module.params.get("bucket_name")
    result["bucket_name"] = bucket_name
    resp = get_bucket(
        module,
        buckets_api,
        object_store_ext_id,
        bucket_name,
        **_namespace_kwargs(module),
    )
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_buckets(module, buckets_api, result):
    object_store_ext_id = module.params.get("object_store_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object store buckets info Spec", **result
        )
    try:
        resp = list_entities(
            buckets_api.list_buckets_by_objectstore_id,
            kwargs=kwargs,
            objectStoreExtId=object_store_ext_id,
            **_namespace_kwargs(module),
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store buckets info",
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
        mutually_exclusive=[
            ("bucket_name", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    buckets_api = get_buckets_api_instance(module)
    if module.params.get("bucket_name"):
        get_bucket_by_name(module, buckets_api, result)
    else:
        list_buckets(module, buckets_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
