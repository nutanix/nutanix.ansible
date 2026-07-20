#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_audits_info_v2
short_description: Fetch audit information from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about Audit in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific Audit.
  - If C(ext_id) is not provided, list multiple Audit optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get audit by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List audits) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=monitoring)"
options:
  ext_id:
    description:
      - The external ID (UUID) of a specific audit to fetch.
      - When provided, the module returns a single audit record.
      - When not provided, the module lists multiple audits.
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
- name: Get audit using ext_id
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "15d110e1-5ca5-4603-4412-8d87fd1bad03"
  register: result
  ignore_errors: true

- name: List all audits (default page/limit)
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List audits filtered by user reference name
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "userReference/name eq 'admin'"
  register: result
  ignore_errors: true

- name: List audits with limit and ordering
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
    orderby: "creationTime desc"
  register: result
  ignore_errors: true

- name: List audits selecting specific fields
  nutanix.ncp.ntnx_audits_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 2
    select: "extId,auditType,operationType,creationTime,status"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC Audit info v4 API.
    - It can be a single Audit if external ID is provided.
    - List of multiple Audit if external ID is not provided with optional filter, limit, page,
      orderby, or select parameters.
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
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching audits info"

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
  description: External ID of the audit
  type: str
  returned: when external ID is provided
  sample: "15d110e1-5ca5-4603-4412-8d87fd1bad03"

total_available_results:
  description: The total number of available audits in PC.
  type: int
  returned: when audits are listed
  sample: 12333
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
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_audit_by_ext_id(module, audits_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_audit(module, audits_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_audits(module, audits_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating audits info spec", **result)

    try:
        resp = audits_api.list_audits(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching audits info",
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
    audits_api = get_audits_api_instance(module)
    if module.params.get("ext_id"):
        get_audit_by_ext_id(module, audits_api, result)
    else:
        get_audits(module, audits_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
