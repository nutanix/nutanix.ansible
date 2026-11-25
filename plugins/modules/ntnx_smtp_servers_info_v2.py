#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_smtp_servers_info_v2
short_description: Fetch SMTP servers info in Nutanix Prism Central
version_added: "2.7.0"
description:
    - This module allows you to fetch information about SMTP servers in Nutanix Prism Central.
    - If C(ext_id) is provided, fetch details of the specific SMTP server.
    - If C(ext_id) is not provided, list multiple SMTP servers optionally filtered or paginated.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get SMTP server by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin, Domain Manager Viewer, Flow Admin, Flow Policy Author,
      Flow Viewer, Internal Super Admin, NCM Connector, Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List SMTP servers) -
      Required Roles: Cluster Admin, Cluster Viewer, Domain Manager Admin, Domain Manager Viewer, Flow Admin, Flow Policy Author,
      Flow Viewer, Internal Super Admin, NCM Connector, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    ext_id:
        description:
            - The external ID of the SMTP server configuration.
        type: str
        required: false
    domain_manager_ext_id:
        description:
            - The external identifier of the domain manager (Prism Central) resource.
            - Required for all operations.
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
- name: Get SMTP server using ext_id
  nutanix.ncp.ntnx_smtp_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    ext_id: "11111111-1111-1111-1111-111111111111"
  register: result
  ignore_errors: true

- name: List all SMTP servers
  nutanix.ncp.ntnx_smtp_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true

- name: List SMTP servers with filter
  nutanix.ncp.ntnx_smtp_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    filter: "isActive eq true"
  register: result
  ignore_errors: true

- name: List SMTP servers with limit
  nutanix.ncp.ntnx_smtp_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    limit: 1
  register: result
  ignore_errors: true

- name: List all SMTP servers with fetch_all
  nutanix.ncp.ntnx_smtp_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    domain_manager_ext_id: "00000000-0000-0000-0000-000000000000"
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - The response from the Nutanix SMTP server info v4 API (host is PC).
      - It can be a single SMTP server if External ID is provided.
      - List of multiple SMTP servers if External ID is not provided with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    {
        "config": {
            "config_details": {
                "email_address": "nutanix@example.com",
                "host": {
                    "fqdn": {
                        "value": "smtp.example.com"
                    },
                    "ipv4": null,
                    "ipv6": null
                },
                "password": null,
                "port": 25,
                "security_mode": "NONE",
                "username": "smtp_user"
            }
        },
        "email_notification_status": null,
        "ext_id": "11111111-1111-1111-1111-111111111111",
        "is_active": true,
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
  sample: "Api Exception raised while fetching SMTP servers info"

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
  description: External ID of the SMTP server
  returned: when external ID is provided
  type: str
  sample: "11111111-1111-1111-1111-111111111111"

total_available_results:
  description: The total number of available SMTP servers in PC.
  returned: when all SMTP servers are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_smtp_server  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_smtp_server_api_instance,
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
        ext_id=dict(type="str"),
        domain_manager_ext_id=dict(type="str", required=True),
    )

    return module_args


def get_smtp_server_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    resp = get_smtp_server(module, api_instance, domain_manager_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_smtp_servers(module, api_instance, result):
    domain_manager_ext_id = module.params.get("domain_manager_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SMTP servers info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_smtp_servers,
            kwargs=kwargs,
            domainManagerExtId=domain_manager_ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SMTP servers info",
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
    api_instance = get_smtp_server_api_instance(module)
    if module.params.get("ext_id"):
        get_smtp_server_using_ext_id(module, api_instance, result)
    else:
        get_smtp_servers(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
