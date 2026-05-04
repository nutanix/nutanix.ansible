#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_runsystemdefinedchecks_info_v2
short_description: Get system-defined alert policies info from Nutanix Prism Central
version_added: "2.6.0"
description:
    - Retrieve system-defined alert policies information.
    - Fetch a single policy by ext_id or list all policies with pagination support.
    - This module uses PC v4 APIs based SDKs.
options:
    ext_id:
        description:
            - The external ID of the system-defined alert policy.
            - If provided, fetches a single policy.
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
- name: List all system-defined alert policies
  nutanix.ncp.ntnx_runsystemdefinedchecks_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
  register: result

- name: List system-defined alert policies with pagination
  nutanix.ncp.ntnx_runsystemdefinedchecks_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    page: 0
    limit: 10
  register: result

- name: Get a specific system-defined alert policy by ext_id
  nutanix.ncp.ntnx_runsystemdefinedchecks_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    ext_id: "<policy_ext_id>"
  register: result
"""

RETURN = r"""
response:
  description:
    - A single policy dict when ext_id is provided.
    - A list of policy dicts when listing all policies.
  type: dict
  returned: always
changed:
  description: Always false for info modules.
  type: bool
  returned: always
  sample: false
ext_id:
  description: The external ID of the policy when fetched by ext_id.
  type: str
  returned: when ext_id is provided
msg:
  description: Informational or error message.
  type: str
  returned: when an error occurs
error:
  description: Error message if an error occurs.
  type: str
  returned: when an error occurs
failed:
  description: Whether the module execution failed.
  type: bool
  returned: always
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_system_defined_policies_api_instance,
)
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


def get_policy(module, policies_api, result):
    """Fetch a single system-defined alert policy by ext_id."""
    ext_id = module.params.get("ext_id")

    try:
        resp = policies_api.get_sda_policy_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system defined policy info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def list_policies(module, policies_api, result):
    """List all system-defined alert policies with pagination."""
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating system defined policies info spec", **result
        )

    try:
        resp = policies_api.list_sda_policies(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching system defined policies info",
        )

    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")

    if resp.metadata:
        result["total_available_results"] = resp.metadata.total_available_results


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
    policies_api = get_system_defined_policies_api_instance(module)
    if module.params.get("ext_id"):
        get_policy(module, policies_api, result)
    else:
        list_policies(module, policies_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
