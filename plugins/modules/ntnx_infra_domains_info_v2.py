#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_infra_domains_info_v2
short_description: Fetch infrastructure domains info in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch information about infrastructure domains in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific infrastructure domain.
    - If C(ext_id) is not provided, list multiple infrastructure domains optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get infrastructure domain by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin, Domain Manager Viewer,
      Internal Super Admin, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List all the infrastructure domains) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin, Domain Manager Viewer,
      Internal Super Admin, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    ext_id:
        description:
            - The external ID of the infrastructure domain.
        type: str
        required: false
    expand:
    description:
      - A URL query parameter that allows clients to request related resources
        when a resource that satisfies a particular request is retrieved.
      - Supported expand value is C(clusterAssociations).
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
- name: Get infra domain using ext_id
  nutanix.ncp.ntnx_infra_domains_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000001"
  register: result
  ignore_errors: true

- name: List all infra domains
  nutanix.ncp.ntnx_infra_domains_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List infra domains with filter
  nutanix.ncp.ntnx_infra_domains_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'test-infra-domain'"
  register: result
  ignore_errors: true

- name: List infra domains with limit
  nutanix.ncp.ntnx_infra_domains_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: List all infra domains with fetch_all
  nutanix.ncp.ntnx_infra_domains_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
  ignore_errors: true

- name: List infra domains with expand
  nutanix.ncp.ntnx_infra_domains_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    expand: "clusterAssociations"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - The response from the Nutanix infra domain info v4 API
      - It can be a single infra domain if external ID is provided.
      - List of multiple infra domain if external ID is not provided with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    {
      "cluster_associations": [
        {
          "cluster_ext_id": "00066101-9650-faa8-0000-000000028f57",
          "is_hosting": true
        }
      ],
      "created_by": "admin",
      "created_time": "2025-02-09T14:44:52.593544+00:00",
      "description": "Test infra domain via Ansible",
      "ext_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
      "fqdn": {
        "value": "infra.example.com"
      },
      "last_updated_by": "admin",
      "last_updated_time": "2025-02-09T14:44:52.593544+00:00",
      "links": null,
      "location": "us-west-1",
      "name": "test-infra-domain",
      "platform_config": {
        "hosting_cluster_info": {
          "hosting_cluster_details": null,
          "network_config": {
            "cluster_subnet_configs": [
              {
                "cluster_ext_id": "00066101-9650-faa8-0000-000000028f57",
                "subnet_ext_id": "b2c3d4e5-f6a7-8901-bcde-f01234567890"
              }
            ]
          }
        },
        "load_balancer_config": [
          {
            "cluster_network_config": {
              "cluster_ext_id": "00066101-9650-faa8-0000-000000028f57",
              "subnet_ext_id": "b2c3d4e5-f6a7-8901-bcde-f01234567890"
            },
            "ip_addresses": [
              {
                "ipv4": {
                  "prefix_length": 32,
                  "value": "10.0.0.20"
                }
              }
            ]
          }
        ],
        "name_server_ip": {
          "ipv4": {
            "prefix_length": 32,
            "value": "10.0.0.11"
          }
        },
        "platform_cluster_ext_id": "c3d4e5f6-a7b8-9012-cdef-012345678901",
        "virtual_ip": {
          "ipv4": {
            "prefix_length": 32,
            "value": "10.0.0.10"
          }
        }
      },
      "size": "SMALL",
      "status": "DEPLOYED",
      "tenant_id": null,
      "version": "6.10"
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
  sample: "Api Exception raised while fetching infra domains info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the infrastructure domain
  returned: when external ID is provided
  type: str
  sample: "a1b2c3d4-e5f6-7890-abcd-ef0123456789"

total_available_results:
  description: The total number of available infrastructure domains in PC.
  returned: when all infrastructure domains are fetched
  type: int
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_infra_domain  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_infra_domain_api_instance,
)
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
        ext_id=dict(type="str", required=False),
        expand=dict(type="str", required=False),
    )

    return module_args


def get_infra_domain_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_infra_domain(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_infra_domains(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating infra domains info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_infra_domains,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching infra domains info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data")

    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_infra_domain_api_instance(module)
    if module.params.get("ext_id"):
        get_infra_domain_using_ext_id(module, api_instance, result)
    else:
        get_infra_domains(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
