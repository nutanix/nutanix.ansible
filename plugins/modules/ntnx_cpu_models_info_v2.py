#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cpu_models_info_v2
short_description: Fetch CPU models info in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch information about cpu models in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific cpu model.
    - If C(ext_id) is not provided, list multiple cpu models optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get CPU model by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer,
      Project Admin, Project Manager, Self-Service Admin (Deprecated), Super Admin
    - >-
      B(List CPU models) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Admin,
      Project Manager, Self-Service Admin (Deprecated), Super Admin, Virtual Machine Admin,
      Virtual Machine Operator, Virtual Machine Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
    ext_id:
        description:
            - The external ID of the CPU model.
        type: str
        required: false
    apply:
    description:
      - A URL query parameter that allows clients to specify a sequence of transformations to the
        entity set, such as groupby, orderby, aggregate etc.
      - For example C(groupby((property))) will get the entity set grouped by "property".
      - The sequence must start with groupby, which may include multiple nested aggregates.
        It may optionally be followed by orderby and/or pagination parameters.
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
- name: Get CPU model using ext_id
  nutanix.ncp.ntnx_cpu_models_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true

- name: List all CPU models
  nutanix.ncp.ntnx_cpu_models_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List CPU models with filter
  nutanix.ncp.ntnx_cpu_models_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "isDefault eq true"
  register: result
  ignore_errors: true

- name: List CPU models with limit
  nutanix.ncp.ntnx_cpu_models_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List all CPU models with fetch_all
  nutanix.ncp.ntnx_cpu_models_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
  ignore_errors: true

- name: List CPU models with apply
  nutanix.ncp.ntnx_cpu_models_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    apply: "groupby((isDefault))"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix CPU models info v4 API.
        - It can be a single CPU model if External ID is provided.
        - List of multiple CPU models if External ID is not provided with optional filter or limit.
    returned: always
    type: dict
    sample:
        {
            "apc_cluster_ext_ids": [
                "0005b3c2-2a6d-3a1c-0000-00000000b3f8"
            ],
            "cluster_ext_ids": [
                "0005b3c2-2a6d-3a1c-0000-00000000b3f8"
            ],
            "configuration": {
                "architecture": "X86_64",
                "cpu_generation_config": {
                    "name": "Sapphire Rapids",
                    "vendor_name": "Intel"
                }
            },
            "ext_id": "550e8400-e29b-41d4-a716-446655440000",
            "is_default": true,
            "links": null,
            "tenant_id": null
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching cpu models info"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the CPU model
    type: str
    returned: when external ID is provided
    sample: "550e8400-e29b-41d4-a716-446655440000"

total_available_results:
    description: The total number of available CPU models in PC.
    type: int
    returned: when all CPU models are fetched
    sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cpu_models_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cpu_model  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        apply=dict(type="str"),
    )

    return module_args


def get_cpu_model_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_cpu_model(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cpu_models(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["apply"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cpu models info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_cpu_models,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cpu models info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
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
            ("ext_id", "apply"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_cpu_models_api_instance(module)
    if module.params.get("ext_id"):
        get_cpu_model_using_ext_id(module, api_instance, result)
    else:
        get_cpu_models(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
