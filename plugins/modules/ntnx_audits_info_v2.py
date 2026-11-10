#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_audits_info_v2
short_description: Fetch audits info in Nutanix Prism Central
version_added: 2.7.0
description:
  - Fetch details of an audit identified by external ID.
  - List audits optionally filtered or paginated when C(ext_id) is not provided.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get audit by ext_id) -
      Required Roles: Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin
    - >-
      B(List all the audits) -
      Required Roles: Monitoring Admin, Monitoring Viewer, Prism Admin, Prism Viewer, Project Admin, Project Manager, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - UUID of the generated audit.
      - When set, only the referenced audit is returned.
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
- name: Get audit using ext_id
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "f92b961e-6f0e-4c1c-b6de-36e328396c9e"
  register: result

- name: List all audits
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List audits with filter
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "auditType eq 'CategoryAudit'"
  register: result

- name: List audits with limit
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result

- name: List all audits with fetch_all
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC audits info v4 API.
    - It can be a single audit if external ID is provided.
    - List of multiple audits if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "affected_entities": null,
      "audit_type": "IAMAdministrationEventAudit",
      "cluster_reference": {
          "ext_id": "cae459ec-08db-475e-a5e5-151e390c9484",
          "name": "PC_10.44.76.29",
          "type": null
      },
      "creation_time": "2026-07-20T14:40:12.123456+00:00",
      "ext_id": "15d110e1-5ca5-4603-4412-8d87fd1bad03",
      "links": null,
      "message": "Token for user admin from 10.100.0.23 has been created",
      "operation_end_time": null,
      "operation_start_time": null,
      "operation_type": "CREATE",
      "parameters": null,
      "service_name": null,
      "source_entity": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin",
          "type": "Token"
      },
      "status": "SUCCEEDED",
      "tenant_id": null,
      "user_reference": {
          "ext_id": null,
          "ip_address": "10.100.0.23",
          "name": "admin"
      }
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching audits info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the audit.
  type: str
  returned: when external ID is provided
  sample: "f92b961e-6f0e-4c1c-b6de-36e328396c9e"

total_available_results:
  description: The total number of available audits in PC.
  type: int
  returned: when all audits are fetched
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_audits_api_instance,
)
from ..module_utils.v4.monitoring.helpers import get_audit  # noqa: E402
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
    )

    return module_args


def get_audit_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_audit(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_audits(module, api_instance, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating audits info spec", **result)

    try:
        resp = list_entities(
            api_instance.list_audits,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching audits info",
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
    api_instance = get_audits_api_instance(module)
    if module.params.get("ext_id"):
        get_audit_using_ext_id(module, api_instance, result)
    else:
        get_audits(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
