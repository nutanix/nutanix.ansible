#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_object_stores_storage_backends_info_v2
short_description: Get Object Store storage backends info
version_added: "2.7.0"
description:
    - Fetch details of a storage backend when C(ext_id) is provided.
    - Fetch a list of the storage backends configured in an Object store when
      C(ext_id) is not provided.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation.
    - >-
      B(Get a list of the storage backends configured in an Object store) -
      Required Roles: Objects Admin, Objects Editor, Objects Viewer, Prism Admin, Super Admin
    - >-
      B(Get the details of a storage backend) -
      Required Roles: Objects Admin, Objects Editor, Objects Viewer, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=objects)"
options:
    object_store_ext_id:
        description:
            - The UUID of the Object store.
        type: str
        required: true
    ext_id:
        description:
            - The UUID of the storage backend in the Object store.
            - If provided, fetches the specific storage backend; otherwise lists
              storage backends.
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
- name: List all storage backends for an object store
  nutanix.ncp.ntnx_object_stores_storage_backends_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result

- name: List storage backends with filter
  nutanix.ncp.ntnx_object_stores_storage_backends_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    filter: "isPrimary eq true"
  register: result

- name: List all storage backends with fetch_all
  nutanix.ncp.ntnx_object_stores_storage_backends_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    fetch_all: true
  register: result

- name: Get details of a storage backend
  nutanix.ncp.ntnx_object_stores_storage_backends_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    ext_id: "f3197423-f486-4037-6037-95442e58484e"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching object store storage backends info.
        - Storage backend details if C(ext_id) is provided.
        - List of storage backends if C(ext_id) is not provided.
    type: dict
    returned: always
    sample:
        {
            "tenant_id": "4cf559d1-4510-4f5f-ab44-008b4600f2b1",
            "ext_id": "8e36bec3-b4a4-427a-b54f-600604fd1e4c",
            "links": [
                {
                    "href": "string",
                    "rel": "string"
                }
            ],
            "name": "cluster-1",
            "cluster_ext_id": "00062664-c65f-f854-65af-7cc25581f458",
            "max_usage_pct": 75,
            "total_capacity_bytes": 1073741824,
            "container_name": "container-1",
            "physical_used_capacity_bytes": 536870912,
            "logical_used_capacity_bytes": 536870912,
            "available_capacity_bytes": 536870912,
            "is_primary": false
        }

ext_id:
    description: The external ID of the storage backend.
    returned: when C(ext_id) is provided
    type: str
    sample: "f3197423-f486-4037-6037-95442e58484e"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching object store storage backends info"

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
    description: The total number of available storage backends for the given object store
    type: int
    returned: when storage backends are listed
    sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_storage_backends_api_instance,
)
from ..module_utils.v4.objects.helpers import get_storage_backend  # noqa: E402
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
        ext_id=dict(type="str"),
    )
    return module_args


def get_storage_backend_by_ext_id(module, storage_backends_api, result):
    object_store_ext_id = module.params.get("object_store_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_storage_backend(
        module, storage_backends_api, object_store_ext_id, ext_id
    )
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_storage_backends(module, storage_backends_api, result):
    object_store_ext_id = module.params.get("object_store_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating object store storage backends info Spec", **result
        )
    try:
        resp = list_entities(
            storage_backends_api.list_storage_backends,
            kwargs=kwargs,
            objectStoreExtId=object_store_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching object store storage backends info",
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
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    storage_backends_api = get_storage_backends_api_instance(module)
    if module.params.get("ext_id"):
        get_storage_backend_by_ext_id(module, storage_backends_api, result)
    else:
        list_storage_backends(module, storage_backends_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
