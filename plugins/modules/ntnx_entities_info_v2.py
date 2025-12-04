#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entities_info_v2
short_description: Get entities info
version_added: 2.0.0
description:
    - Get entities info using entity external ID or list multiple entities
    - Configure and manage entities representing the resources over which permissions are defined.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID of the entity
            - It can be used to get specific entity info
        required: false
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - abhinavbansal29 (@abhinavbansal29)
"""
EXAMPLES = r"""
- name: List all entities
  nutanix.ncp.ntnx_entities_info_v2:
  nutanix_host: <pc_ip>
  nutanix_username: <user>
  nutanix_password: <pass>
  validate_certs: false
  register: result
  ignore_errors: true

- name: List entities using filter
  nutanix.ncp.ntnx_entities_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    filter: "name eq '{{ entity_name }}'"
  register: result
  ignore_errors: true

- name: List entities using limit
  nutanix.ncp.ntnx_entities_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    limit: 1
  register: result
  ignore_errors: true

- name: Fetch entity using external ID
  nutanix.ncp.ntnx_entities_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    ext_id: "{{ entity_external_id }}"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for fetching entities info
        - Returns entities info using entities external ID or list multiple entities
    type: dict
    returned: always
    sample:
        {
            "attribute_list": [
                {
                    "attribute_values": null,
                    "display_name": null,
                    "ext_id": null,
                    "links": null,
                    "supported_operators": null,
                    "tenant_id": null
                },
                {
                    "attribute_values": null,
                    "display_name": null,
                    "ext_id": null,
                    "links": null,
                    "supported_operators": null,
                    "tenant_id": null
                },
                {
                    "attribute_values": null,
                    "display_name": null,
                    "ext_id": null,
                    "links": null,
                    "supported_operators": null,
                    "tenant_id": null
                }
            ],
            "client_name": "DevOps",
            "created_by": null,
            "created_time": "2025-11-27T15:44:50.397000+00:00",
            "description": "account",
            "display_name": "Account",
            "ext_id": "dc774897-3bfa-437b-53bb-c97e192029c4",
            "is_logical_and_supported_for_attributes": false,
            "last_updated_time": "2025-11-27T15:44:50.397000+00:00",
            "links": null,
            "name": "account",
            "search_url": null,
            "tenant_id": null
        }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

msg:
    description: Message if any error occurred
    returned: when there is an error
    type: str
    sample: "Failed generating entities info Spec"

ext_id:
    description: External ID of the entity
    returned: always
    type: str
    sample: 04e7b47e-a861-5b57-a494-10ca57e6ec4a

total_available_results:
    description:
        - The total number of available entities in PC.
    type: int
    returned: when all entities are fetched
    sample: 125

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_entity_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_entity  # noqa: E402
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


def get_entity_by_ext_id(module, entities, result):
    ext_id = module.params.get("ext_id")
    resp = get_entity(module, entities, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_entities(module, entities, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating entities info Spec", **result)

    try:
        resp = entities.list_entities(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching entities info",
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
    result = {"changed": False, "error": None, "response": None}
    entities = get_entity_api_instance(module)
    if module.params.get("ext_id"):
        get_entity_by_ext_id(module, entities, result)
    else:
        get_entities(module, entities, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
