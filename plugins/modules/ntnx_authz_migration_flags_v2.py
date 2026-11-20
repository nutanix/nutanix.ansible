#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_authz_migration_flags_v2
short_description: List Authz migration flags using v4 APIs
version_added: "2.7.0"
description:
    - List migration flags for AuthZ migration in Nutanix Prism Central.
    - This module fetches the list of migration flags used to control
      AuthZ migration behavior.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned
      to the user performing the operation.
    - >-
      B(List migration flags) -
      Required Roles: Prism Admin, Super Admin, Nutanix Central Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    filter:
        description:
            - A URL query parameter that allows clients to filter a
              collection of resources.
            - Expression specified with C($filter) must conform to the
              OData V4.01 URL conventions.
            - For example, C(flagName eq 'some_flag') would filter on
              migration flag name.
        type: str
        required: false
    orderby:
        description:
            - A URL query parameter that allows clients to specify the
              sort criteria for the returned list of objects.
            - Resources can be sorted in ascending order using C(asc)
              or descending order using C(desc).
        type: str
        required: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all Authz migration flags
  nutanix.ncp.ntnx_authz_migration_flags_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true

- name: List Authz migration flags with filter
  nutanix.ncp.ntnx_authz_migration_flags_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "flagName eq 'test_flag'"
  register: result
  ignore_errors: true

- name: List Authz migration flags with orderby
  nutanix.ncp.ntnx_authz_migration_flags_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "flagName asc"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for listing AuthZ migration flags.
        - It contains list of migration flags with flag name and value.
    returned: always
    type: dict
    sample:
        {
            "data": [
                {
                    "flag_name": "test_flag",
                    "flag_value": "true",
                    "ext_id": "00000000-0000-0000-0000-000000000000",
                    "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df"
                }
            ],
            "metadata": {
                "total_available_results": 1
            }
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: false

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "List of Authz migration flags fetched successfully"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Api Exception raised while listing Authz migration flags"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_authz_migration_api_instance,
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
        filter=dict(type="str", required=False),
        orderby=dict(type="str", required=False),
    )
    return module_args


def list_authz_migration_flags(module, result, api_instance):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating list authz migration flags spec", **result
        )

    if module.check_mode:
        result["msg"] = "List of Authz migration flags will be fetched."
        result["response"] = []
        return

    resp = None
    try:
        resp = api_instance.authz_migration_flags(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing Authz migration flags",
        )

    # Handle response - data may be list of flags or empty
    resp_dict = strip_internal_attributes(resp.to_dict())
    result["response"] = resp_dict
    result["changed"] = False


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_authz_migration_api_instance(module)
    list_authz_migration_flags(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
