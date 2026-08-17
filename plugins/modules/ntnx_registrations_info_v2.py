#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_registrations_info_v2
short_description: Fetch information about registrations of a Prism Central (domain manager).
version_added: 2.5.0
description:
  - This module allows you to fetch information about Registration in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Registration.
  - If C(ext_id) is not provided, list multiple Registration optionally filtered / paginated.
  - The v4 RegistrationApi is read-only and returns the clusters that have been
    registered to the domain manager (Prism Central) - other Prism Centrals,
    AOS Prism Elements, or Witness VMs.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get registration by ext_id) -
      Required Roles: Prism Admin, Super Admin, Prism Viewer
    - >-
      B(List registrations) -
      Required Roles: Prism Admin, Super Admin, Prism Viewer
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
  domain_manager_ext_id:
    description:
      - The external identifier of the domain manager (Prism Central) resource
        whose registrations are being queried.
      - This value is required by the underlying v4 Registration API.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of a specific Registration under the given
        domain manager. When provided, only that registration is fetched.
      - When omitted, all registrations under the domain manager are listed
        (subject to filter / paging).
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch a single registration by ext_id
  nutanix.ncp.ntnx_registrations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "18553f0f-7b41-4115-b25e-e5b45f414d6f"
    ext_id: "d2f9994f-44fb-4d4c-ad3c-92055316444f"
  register: single_registration

- name: List all registrations under a domain manager
  nutanix.ncp.ntnx_registrations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "18553f0f-7b41-4115-b25e-e5b45f414d6f"
  register: all_registrations

- name: List registrations with a filter (only DOMAIN_MANAGER cluster type)
  nutanix.ncp.ntnx_registrations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "18553f0f-7b41-4115-b25e-e5b45f414d6f"
    filter: "remoteClusterDetails/clusterType eq Prism.Config.ClusterType'DOMAIN_MANAGER'"
  register: dm_only_registrations

- name: List registrations with paging + limit
  nutanix.ncp.ntnx_registrations_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "18553f0f-7b41-4115-b25e-e5b45f414d6f"
    page: 0
    limit: 1
  register: first_registration_only
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Registration info v4 API.
    - It can be a single Registration if external ID is provided.
    - List of multiple Registrations if external ID is not provided,
      with optional filter / limit / paging / orderby / select.
  returned: always
  type: dict
  sample:
    {
      "connectivity_status": "CONNECTED",
      "ext_id": "d2f9994f-44fb-4d4c-ad3c-92055316444f",
      "links": null,
      "metadata": null,
      "remote_cluster_details": {
          "cluster_type": "DOMAIN_MANAGER",
          "cluster_version": "master",
          "ext_id": "d2f9994f-44fb-4d4c-ad3c-92055316444f",
          "external_address": {
              "fqdn": null,
              "ipv4": {"prefix_length": 32, "value": "10.44.76.49"},
              "ipv6": null
          },
          "links": null,
          "name": "PC_10.44.76.49",
          "node_ip_addresses": [
              {"fqdn": null, "ipv4": {"prefix_length": 32, "value": "10.44.76.49"}, "ipv6": null}
          ],
          "tenant_id": null
      },
      "remote_cluster_ext_id": "d2f9994f-44fb-4d4c-ad3c-92055316444f",
      "tenant_id": null
    }

changed:
  description: Whether the module made any change. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status / error message emitted by the module (only on error).
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching registrations info"

error:
  description:
    - Error details from the SDK / API when the module fails to fetch data.
  returned: When an error occurs
  type: str

failed:
  description: Whether the module failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the registration (only when C(ext_id) is provided).
  type: str
  returned: when external ID is provided
  sample: "d2f9994f-44fb-4d4c-ad3c-92055316444f"

total_available_results:
  description: Total number of registrations available on the domain manager.
  type: int
  returned: when all registrations are listed (no C(ext_id) supplied)
  sample: 2
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_registration  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_registration_api_instance,
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
        domain_manager_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )

    return module_args


def get_registration_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    resp = get_registration(module, api_instance, domain_manager_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_registrations(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating registrations info spec", **result)

    domain_manager_ext_id = module.params.get("domain_manager_ext_id")

    try:
        resp = api_instance.list_registrations(
            domainManagerExtId=domain_manager_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching registrations info",
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_registration_api_instance(module)
    if module.params.get("ext_id"):
        get_registration_using_ext_id(module, api_instance, result)
    else:
        list_registrations(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
