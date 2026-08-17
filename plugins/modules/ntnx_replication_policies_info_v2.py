#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_replication_policies_info_v2
short_description: Fetch Nutanix Files replication policies info in Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ReplicationPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ReplicationPolicy.
  - If C(ext_id) is not provided, list multiple ReplicationPolicy optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get / List Replication Policies) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  ext_id:
    description:
      - External ID of the replication policy to fetch.
      - If not provided, list of replication policies is returned.
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
- name: Get replication policy by ext_id
  nutanix.ncp.ntnx_replication_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all replication policies
  nutanix.ncp.ntnx_replication_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List replication policies with filter
  nutanix.ncp.ntnx_replication_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "type eq Files.Config.ReplicationPolicyType'SMART_DR'"
  register: result
  ignore_errors: true

- name: List replication policies with limit
  nutanix.ncp.ntnx_replication_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ReplicationPolicy info v4 API.
    - It can be a single ReplicationPolicy if external ID is provided.
    - List of multiple ReplicationPolicy if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "change_user_session_ownership_spec": null,
      "description": "Smart DR replication policy created by Ansible",
      "exclude_file_patterns": null,
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "is_reverse": false,
      "links": null,
      "name": "smartdr_policy_ansible",
      "replication_configurations": [
          {
              "primary_domain_manager_ext_id": "1c2d3e4f-1234-4c1b-9d0b-6bdf7bf67e11",
              "primary_file_server_ext_id": "a4b02ea9-6a56-4c1b-9d0b-6bdf7bf67e11",
              "replication_entities": null,
              "replication_summary": null,
              "schedule": {
                  "frequency": 1,
                  "schedule_interval": {"frequency": 1},
                  "start_time": null
              },
              "secondary_domain_manager_ext_id": "2b3c4d5e-5678-4c1b-9d0b-6bdf7bf67e11",
              "secondary_file_server_ext_id": "b7d84e21-3a45-47dc-a1c8-4bcf6a24fa19",
              "should_cancel_ongoing_replication_jobs": null,
              "status": "ENABLED"
          }
      ],
      "should_include_new_mount_targets": true,
      "should_keep_deleted_files": null,
      "status": "ENABLED",
      "tenant_id": null,
      "type": "SMART_DR"
    }

changed:
  description: Whether the module made any change on the cluster (always False).
  returned: always
  type: bool
  sample: false

msg:
  description: Message set when there is an error.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching replication policies info"

error:
  description: Error details if any error occurred.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the replication policy (only when fetching by ID).
  type: str
  returned: when external ID is provided
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: Total number of replication policies in Prism Central.
  type: int
  returned: when listing all replication policies
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_replication_policies_api_instance,
)
from ..module_utils.v4.files.helpers import get_replication_policy  # noqa: E402
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
    )
    return module_args


def get_replication_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_replication_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_replication_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating replication policies info spec", **result
        )

    try:
        resp = api_instance.list_replication_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching replication policies info",
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
    api_instance = get_replication_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_replication_policy_using_ext_id(module, api_instance, result)
    else:
        get_replication_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
