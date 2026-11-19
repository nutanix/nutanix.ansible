#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_authn_migration_v2
short_description: Migrate IAM AuthN data from IAMv1 or transform data in IAMv2
version_added: "2.7.0"
description:
    - Migrate the IAM AuthN data from IAMv1 or transform data in IAMv2
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Migrate the IAM AuthN data) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will migrate the IAM AuthN data.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    migration_type:
        description:
            - The type of authn migration.
            - Indicates the migration operation to perform.
        type: str
        required: true
        choices:
            - HASH_OIDC_CLIENT_SECRET
            - MIGRATE_LDAP_BIND_PASSWORDS
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
- name: Migrate AuthN data to hash OIDC client secret
  nutanix.ncp.ntnx_authn_migration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    migration_type: HASH_OIDC_CLIENT_SECRET
  register: result
  ignore_errors: true

- name: Migrate LDAP bind passwords
  nutanix.ncp.ntnx_authn_migration_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    migration_type: MIGRATE_LDAP_BIND_PASSWORDS
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for migrating IAM AuthN data.
        - Contains the API response including metadata and data.
    returned: always
    type: dict
    sample:
        {
            "data": [
                {
                    "arguments_map": {},
                    "code": "IAM-1000",
                    "error_group": null,
                    "locale": "en_US",
                    "message": "AuthN migration completed successfully.",
                    "severity": "INFO"
                }
            ],
            "metadata": {
                "flags": [],
                "kind": "iam.v4.authn.AuthnMigrationApiResponse",
                "messages": null,
                "total_available_results": 1
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
    sample: "Api Exception raised while migrating authn data"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str

failed:
    description: This field indicates if the task execution failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_authn_migration_api_instance,
)
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
        migration_type=dict(
            type="str",
            required=True,
            choices=["HASH_OIDC_CLIENT_SECRET", "MIGRATE_LDAP_BIND_PASSWORDS"],
            obj=iam_sdk.AuthnMigrationType,
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.AuthnMigrationRequest()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating authn migration spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.migrate(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating authn data",
        )

    result["response"] = strip_internal_attributes(resp.to_dict())
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
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_authn_migration_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
