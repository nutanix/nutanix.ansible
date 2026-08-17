#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_sync_policies_info_v2
short_description: Fetch entity sync policies info in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about EntitySyncPolicy in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific EntitySyncPolicy.
  - If C(ext_id) is not provided, list multiple EntitySyncPolicy optionally filtered / paginated /
    ordered / projected.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get an Entity Sync Policy by ext_id) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Flow Admin, Flow Viewer,
    Prism Admin, Prism Viewer, Project Manager, Super Admin
  - >-
    B(List Entity Sync Policies) -
    Required Roles: Disaster Recovery Admin, Disaster Recovery Viewer, Flow Admin, Flow Viewer,
    Prism Admin, Prism Viewer, Project Manager, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  ext_id:
    description:
      - The external identifier of the entity sync policy.
      - When provided, a single entity sync policy is fetched by ID.
      - When omitted, a list of entity sync policies is returned (optionally filtered / paginated).
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch a single entity sync policy using external ID
  nutanix.ncp.ntnx_entity_sync_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List all entity sync policies
  nutanix.ncp.ntnx_entity_sync_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List entity sync policies with a filter
  nutanix.ncp.ntnx_entity_sync_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "entityType eq Datapolicies.Config.SyncedEntityType'SECURITY_POLICY'"
  register: result
  ignore_errors: true

- name: List entity sync policies with a limit
  nutanix.ncp.ntnx_entity_sync_policies_info_v2:
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
    - The response from the Nutanix PC EntitySyncPolicy info v4 API.
    - It can be a single EntitySyncPolicy if external ID is provided.
    - List of multiple EntitySyncPolicy if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    {
      "entity_ext_id": "3f7d6c02-8a2f-4f27-9c1e-1c99b5aef1a2",
      "entity_name": "nsp-example",
      "entity_type": "SECURITY_POLICY",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "project_ext_id": null,
      "recovery_config_store_ext_id": null,
      "remote_domain_manager_ext_id": "bd32fb09-8005-4655-a3a8-086b8ec1b1ea",
      "status": "IN_SYNC",
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the entity sync policy.
  returned: when external ID is provided
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

msg:
  description: Human readable message when an error occurs.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching entity sync policies info"

error:
  description: Error message if any error occurred while fetching info.
  returned: when an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

total_available_results:
  description: The total number of available entity sync policies in PC.
  returned: when all entity sync policies are fetched
  type: int
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_entity_sync_policies_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_entity_sync_policy  # noqa: E402
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


def get_entity_sync_policy_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_entity_sync_policy(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_entity_sync_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating entity sync policies info spec", **result
        )

    try:
        resp = api_instance.list_entity_sync_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching entity sync policies info",
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
    api_instance = get_entity_sync_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_entity_sync_policy_using_ext_id(module, api_instance, result)
    else:
        get_entity_sync_policies(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
