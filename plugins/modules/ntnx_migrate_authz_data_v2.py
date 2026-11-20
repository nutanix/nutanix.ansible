#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_migrate_authz_data_v2
short_description: Migrate AuthZ data using v4 APIs
version_added: "2.7.0"
description:
    - Migrate the IAM AuthZ data from IAM V1 or transform IAM V2 AuthZ data.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned
      to the user performing the operation.
    - >-
      B(Migrate AuthZ data) -
      Required Roles: Prism Admin, Super Admin, Nutanix Central Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will migrate AuthZ data.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    migration_type:
        description:
            - The type of AuthZ migration.
        type: str
        required: true
        choices:
            - REMOVE_AP_TENANT_ID_FILTERS
            - NC_USER_AP_TO_USER_DEFINED
            - ASSIGN_BASIC_USER_AP_TO_NC_USER_AP_USERS_USERGROUPS
            - REMOVE_CLIENT_FOUNDATION_CENTRAL
            - MOVE_ROLES_APS_FROM_PRISM_CLOUD_IAM
            - REMOVE_DUPLICATE_APS_AFTER_NAMESPACE_MIGRATION
            - SYNC_AP_TO_AUTHZ_FILTER_SEARCH_TABLE
            - MIGRATE_PROJECT_AP_TO_ROLE_MEMBERSHIP
            - POPULATE_USER_ROLE_PRODUCTS
            - MIGRATE_SELF_SERVICE_ADMIN_AP_TO_PROJECT_MANAGER
    project_ap_migration_data:
        description:
            - Input payload for the migrate-project-ap-to-role-membership migration.
            - Required only when the migration type is C(MIGRATE_PROJECT_AP_TO_ROLE_MEMBERSHIP).
        type: dict
        required: false
        suboptions:
            project_ext_id:
                description:
                    - External identifier of the project.
                    - All role memberships created during this migration are
                      scoped to this project.
                type: str
                required: true
            ap_ext_ids:
                description:
                    - List of external identifiers of authorization policies
                      to migrate to role memberships.
                type: list
                elements: str
                required: true
            user_idp_mappings:
                description:
                    - List of mappings from user external identifier to
                      identity provider external identifier.
                    - Used while creating role memberships for users
                      referenced by the migrated authorization policies.
                type: list
                elements: dict
                required: false
                suboptions:
                    identity_ext_id:
                        description:
                            - External identifier of the identity
                              (user or user group).
                        type: str
                        required: true
                    idp_ext_id:
                        description:
                            - External identifier of the identity provider
                              that the identity belongs to.
                        type: str
                        required: true
            user_group_idp_mappings:
                description:
                    - List of mappings from user group external identifier
                      to identity provider external identifier.
                    - Used while creating role memberships for user groups
                      referenced by the migrated authorization policies.
                type: list
                elements: dict
                required: false
                suboptions:
                    identity_ext_id:
                        description:
                            - External identifier of the identity
                              (user or user group).
                        type: str
                        required: true
                    idp_ext_id:
                        description:
                            - External identifier of the identity provider
                              that the identity belongs to.
                        type: str
                        required: true
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
- name: Migrate AuthZ data - remove AP tenant ID filters
  nutanix.ncp.ntnx_migrate_authz_data_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    migration_type: "REMOVE_AP_TENANT_ID_FILTERS"
  register: result
  ignore_errors: true

- name: Migrate AuthZ data with project AP migration
  nutanix.ncp.ntnx_migrate_authz_data_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    migration_type: "MIGRATE_PROJECT_AP_TO_ROLE_MEMBERSHIP"
    project_ap_migration_data:
      project_ext_id: "12345678-1234-1234-1234-123456789012"
      ap_ext_ids:
        - "87654321-4321-4321-4321-210987654321"
      user_idp_mappings:
        - identity_ext_id: "11111111-1111-1111-1111-111111111111"
          idp_ext_id: "22222222-2222-2222-2222-222222222222"
      user_group_idp_mappings:
        - identity_ext_id: "33333333-3333-3333-3333-333333333333"
          idp_ext_id: "44444444-4444-4444-4444-444444444444"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for migrating AuthZ data.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "data": [
                {
                    "code": "200",
                    "message": "Migration completed successfully"
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
    sample: true

task_ext_id:
    description: The external ID of the task
    returned: when applicable
    type: str
    sample: "ZXJnb24=:a0d8956a-4cc4-43aa-9715-897b5468dd57"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Api Exception raised while migrating AuthZ data"

failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while migrating AuthZ data"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

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

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    identity_idp_mapping_spec = dict(
        identity_ext_id=dict(type="str", required=True),
        idp_ext_id=dict(type="str", required=True),
    )

    project_ap_migration_data_spec = dict(
        project_ext_id=dict(type="str", required=True),
        ap_ext_ids=dict(type="list", elements="str", required=True),
        user_idp_mappings=dict(
            type="list",
            elements="dict",
            options=identity_idp_mapping_spec,
            required=False,
            obj=iam_sdk.IdentityIdpMapping,
        ),
        user_group_idp_mappings=dict(
            type="list",
            elements="dict",
            options=identity_idp_mapping_spec,
            required=False,
            obj=iam_sdk.IdentityIdpMapping,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        migration_type=dict(
            type="str",
            required=True,
            choices=[
                "REMOVE_AP_TENANT_ID_FILTERS",
                "NC_USER_AP_TO_USER_DEFINED",
                "ASSIGN_BASIC_USER_AP_TO_NC_USER_AP_USERS_USERGROUPS",
                "REMOVE_CLIENT_FOUNDATION_CENTRAL",
                "MOVE_ROLES_APS_FROM_PRISM_CLOUD_IAM",
                "REMOVE_DUPLICATE_APS_AFTER_NAMESPACE_MIGRATION",
                "SYNC_AP_TO_AUTHZ_FILTER_SEARCH_TABLE",
                "MIGRATE_PROJECT_AP_TO_ROLE_MEMBERSHIP",
                "POPULATE_USER_ROLE_PRODUCTS",
                "MIGRATE_SELF_SERVICE_ADMIN_AP_TO_PROJECT_MANAGER",
            ],
            obj=iam_sdk.AuthzMigrationType,
        ),
        project_ap_migration_data=dict(
            type="dict",
            required=False,
            options=project_ap_migration_data_spec,
            obj=iam_sdk.ProjectApMigrationData,
        ),
    )
    return module_args


def migrate_authz_data(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.AuthzMigrationRequest()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating migrate AuthZ data spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "AuthZ data migration will be performed with migration_type: {0}".format(
                module.params.get("migration_type")
            )
        )
        return

    resp = None
    try:
        resp = api_instance.migrate_authz_data(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while migrating AuthZ data",
        )

    # Handle task or direct response
    if resp and getattr(resp, "data", None) is not None:
        data = resp.data
        # Check if response is a task reference
        if hasattr(data, "ext_id"):
            result["task_ext_id"] = getattr(data, "ext_id", None)
        result["response"] = strip_internal_attributes(resp.to_dict())
        # If wait is true and we have a task, wait for completion
        task_ext_id = result.get("task_ext_id")
        if task_ext_id and module.params.get("wait"):
            from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402

            task = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task.to_dict())
    else:
        result["response"] = strip_internal_attributes(resp.to_dict()) if resp else {}

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_authz_migration_api_instance(module)
    migrate_authz_data(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
