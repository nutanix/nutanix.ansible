#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_configure_tenant_v2
short_description: Configure tenant in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Configure a tenant in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Configure Tenant) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will configure the tenant.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    tenant_name:
        description:
            - Name of tenant for which configuration is being set up.
        type: str
        required: true
    tenant_description:
        description:
            - Description of the tenant.
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
- name: Configure tenant
  nutanix.ncp.ntnx_configure_tenant_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    tenant_name: "test-tenant"
    tenant_description: "Tenant for testing"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for configuring tenant.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "data": {
                "tenant_name": "test-tenant",
                "tenant_description": "Tenant for testing",
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "tenant_id": "00000000-0000-0000-0000-000000000000"
            },
            "metadata": {
                "flags": [],
                "links": [],
                "total_available_results": 1,
                "messages": [],
                "extra_info": []
            }
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while configuring tenant"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Failed generating spec for configure tenant"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the tenant
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_tenants_api_instance  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        tenant_name=dict(type="str", required=True),
        tenant_description=dict(type="str", required=False),
    )
    return module_args


def _get_tenant_spec():
    """Return Tenant SDK object, handling different SDK versions."""
    # SDK exposes AuthzTenant for TenantsApi
    if hasattr(iam_sdk, "AuthzTenant"):
        return iam_sdk.AuthzTenant()
    if hasattr(iam_sdk, "Tenant"):
        return iam_sdk.Tenant()
    # Fallback to direct import
    try:
        from ntnx_iam_py_client.models.iam.v4.authz.Tenant import Tenant

        return Tenant()
    except ImportError:
        return iam_sdk.AuthzTenant()


def configure_tenant(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = _get_tenant_spec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for configure tenant", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.configure_tenant(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while configuring tenant",
        )

    resp_dict = strip_internal_attributes(resp.to_dict())
    result["response"] = resp_dict

    # Try to extract ext_id and task_ext_id if present in response
    data = resp_dict.get("data") if isinstance(resp_dict, dict) else None
    if isinstance(data, dict):
        if data.get("ext_id"):
            result["ext_id"] = data.get("ext_id")
        elif resp.data and hasattr(resp.data, "ext_id"):
            result["ext_id"] = resp.data.ext_id
        # Handle task-like response
        if data.get("extId"):
            result["task_ext_id"] = data.get("extId")
    # Fallback: check if response itself has ext_id at top level
    if isinstance(resp_dict, dict) and resp_dict.get("ext_id"):
        result["ext_id"] = resp_dict.get("ext_id")

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    api_instance = get_tenants_api_instance(module)
    configure_tenant(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
