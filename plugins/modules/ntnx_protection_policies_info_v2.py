#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_protection_policies_info_v2
short_description: Fetch protection policies info in Nutanix Prism Central
description:
    - This module allows you to fetch protection policies info in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - The external identifier of the protection policy.
        type: str
extends_documentation_fragment:
        - nutanix.ncp.ntnx_credentials
        - nutanix.ncp.ntnx_info_v2
author:
    - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Fetch details for a protection policy using External ID
  nutanix.ncp.ntnx_protection_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
  register: result

- name: List all protection policies
  nutanix.ncp.ntnx_protection_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
  register: result

- name: Fetch details for a protection policy using filter
  nutanix.ncp.ntnx_protection_policies_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    filter: extId eq '840c6c3f-2b01-47d5-81fb-b285e45e89ba'
  register: result
  ignore_errors: true
"""
RETURN = r"""
response:
    description:
        - Response for fetching protection policies info
        - One protection policy info if External ID is provided
        - List of multiple protection policies info if External ID is not provided
    returned: always
    type: dict

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: when an error occurs
    sample: null

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

ext_id:
    description: External ID of the protection policy
    type: str
    returned: when external ID is provided
    sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protection_policies_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_protection_policy,
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


def get_protection_policy_using_ext_id(module, protection_policies, result):
    ext_id = module.params.get("ext_id")
    resp = get_protection_policy(module, protection_policies, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_protection_policies(module, protection_policies, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating protection policies info Spec", **result
        )

    try:
        resp = protection_policies.list_protection_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching protection policies info",
        )

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
    protection_policies = get_protection_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_protection_policy_using_ext_id(module, protection_policies, result)
    else:
        get_protection_policies(module, protection_policies, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
