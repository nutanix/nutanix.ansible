#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_products_info_v2
short_description: Fetch information about portfolio Products in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about Product in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Product.
  - If C(ext_id) is not provided, list multiple Product optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Get product by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List products) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  ext_id:
    description:
      - The product ID for a given product.
    type: str
    required: false
  domain_manager_ext_id:
    description:
      - The external identifier of the domain manager (Prism Central) resource that
        owns the product.
      - Can be discovered using M(nutanix.ncp.ntnx_pc_config_info_v2).
    type: str
    required: true
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
- name: Fetch a single product using ext_id
  nutanix.ncp.ntnx_products_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    ext_id: "0081eaf6-527b-44a0-4fe9-60ee067c0e82"
  register: product
  ignore_errors: true

- name: List all portfolio products on the PC
  nutanix.ncp.ntnx_products_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
  register: products
  ignore_errors: true

- name: Attempt to filter products using an OData $filter expression
  # NOTE: The Products list endpoint currently accepts the $filter query
  # parameter but does not expose any filterable properties. The backend
  # rejects filter expressions with an "invalid property for query" error.
  nutanix.ncp.ntnx_products_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    filter: "name eq Prism.Config.ProductName'SELF_SERVICE'"
  register: filtered_products
  ignore_errors: true

- name: List products with pagination and ordering
  nutanix.ncp.ntnx_products_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "cae459ec-08db-475e-a5e5-151e390c9484"
    page: 0
    limit: 5
    orderby: "name asc"
  register: paged_products
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Product info v4 API.
    - It can be a single Product if external ID is provided.
    - List of multiple Product if external ID is not provided with optional
      filter, page, limit, orderby or select.
  returned: always
  type: dict
  sample:
    {
      "enablement_state": "ENABLED",
      "ext_id": "0081eaf6-527b-44a0-4fe9-60ee067c0e82",
      "last_modified_time": "2026-06-30T17:30:02.650540+00:00",
      "links": null,
      "metadata": null,
      "name": "SELF_SERVICE",
      "resize_time": "2026-06-30T17:11:25.349000+00:00",
      "resource_spec": {
        "cpu_count": 2,
        "memory_size_bytes": 4294967296
      },
      "service_enablement_time": null,
      "tenant_id": null,
      "version": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
    Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching products info"

error:
  description: This field typically holds information about if the task have
    errors that occurred during the task execution.
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the product.
  type: str
  returned: When external ID is provided
  sample: "0081eaf6-527b-44a0-4fe9-60ee067c0e82"

total_available_results:
  description: The total number of available products on the PC.
  type: int
  returned: When all products are fetched
  sample: 8
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_product  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
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
        domain_manager_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_product_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    resp = get_product(module, api_instance, ext_id, domain_manager_ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_products(module, api_instance, result):
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating products info spec", **result)

    try:
        resp = api_instance.list_products(
            domainManagerExtId=domain_manager_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching products info",
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
    api_instance = get_domain_manager_api_instance(module)
    if module.params.get("ext_id"):
        get_product_using_ext_id(module, api_instance, result)
    else:
        get_products(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
