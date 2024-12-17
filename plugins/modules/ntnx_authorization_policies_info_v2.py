#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_authorization_policies_info_v2
short_description: Fetch Authorization policies info from Nutanix PC.
version_added: 2.0.0
description:
    - Get authorization policies info
    - It will fetch specific authorization policy if external ID is provided
    - It will fetch multiple authorization policies if external ID is not provided
    - Use filters to fetch specific authorization policies
options:
    ext_id:
        description:
            - authorization_policy external ID
            - if provided, it will fetch the authorization policy with the given external ID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: Get 10 auth policies
  ntnx_authorization_policies_info_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    limit: 10
  register: result
  ignore_errors: true

- name: Get specific auth policy
  ntnx_authorization_policies_info_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "ebbfbd38-794b-5529-adcc-dcb6b4177387"
  register: result
  ignore_errors: true

- name: Fetch using filters
  ntnx_authorization_policies_info_v2:
    nutanix_host: "{{ nutanix_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    filter: "displayName eq 'acp1'"
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
  description:
    - It will have specific authorization policy if external ID is provided
    - It will have list of multiple authorization policies if external ID is not provided
  returned: always
  type: dict
  sample:
       {
                "authorizationPolicyType": "PREDEFINED_READ_ONLY",
                "clientName": "",
                "createdBy": "",
                "createdTime": "2024-03-20T09:54:34.846946Z",
                "description": "",
                "displayName": "Super Admin_acp",
                "entities": [
                    {
                        "$reserved": {
                            "*": {
                                "*": {
                                    "eq": "*"
                                }
                            }
                        }
                    }
                ],
                "extId": "00000000-0000-0000-0300-000000000000",
                "identities": [
                    {
                        "$reserved": {
                            "user": {
                                "uuid": {
                                    "anyof": [
                                        "00000002-0000-0000-0000-000000000000"
                                    ]
                                }
                            }
                        }
                    }
                ],
                "isSystemDefined": true,
                "lastUpdatedTime": "2024-03-20T09:54:34.846946Z",
                "role": "00000001-0000-0000-0000-000000000000"
            }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
ext_id:
  description: External Id of the authorization policy
  returned: always
  type: bool
  sample: "00000000-0000-0000-0000-000000000000"
"""

import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_authorization_policy_api_instance,
)
from ..module_utils.v4.iam.helpers import (  # noqa: E402
    get_authorization_policy as get_authorization_policy_by_id,
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
    )

    return module_args


def format_acp_spec(spec):
    identities = strip_internal_attributes(
        deepcopy(spec.pop("identities")), ["_reserved"]
    )
    entities = strip_internal_attributes(deepcopy(spec.pop("entities")), ["_reserved"])
    spec = strip_internal_attributes(spec)

    # taking out identity and entity present under $reserved in spec
    formatted_identities = []
    if identities:
        for identity in identities:
            formatted_identities.append(identity["_reserved"])
    spec["identities"] = formatted_identities

    formatted_entities = []
    if entities:
        for entity in entities:
            formatted_entities.append(entity["_reserved"])
    spec["entities"] = formatted_entities

    return spec


def get_authorization_policies(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating authorization_policies info Spec", **result
        )

    try:
        resp = api_instance.list_authorization_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching authorization_policies info",
        )

    policies = []
    if getattr(resp, "data", []):
        policies = resp.to_dict().get("data")

    for policy in policies:
        format_acp_spec(policy)

    result["response"] = policies


def get_authorization_policy(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    policy = get_authorization_policy_by_id(module, api_instance, ext_id)
    result["response"] = format_acp_spec(policy.to_dict())


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

    authorization_policies = get_authorization_policy_api_instance(module)
    if module.params.get("ext_id"):
        get_authorization_policy(module, authorization_policies, result)
    else:
        get_authorization_policies(module, authorization_policies, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
