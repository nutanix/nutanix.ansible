#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_seed_config_v2
short_description: Seed Authz configuration in IAM
version_added: "2.7.0"
description:
    - Seed Authz configuration in IAM.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Seed Authz configuration in IAM) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    config_type:
        description:
            - The type of entities which will be seeded.
        type: str
        required: true
        choices:
            - CLIENT
            - ENTITY
            - OPERATION
            - ROLE
            - AUTHORIZATION_POLICY
    client_name:
        description:
            - The name of the client for which the entities will be seeded.
        type: str
        required: true
    operation_type:
        description:
            - The type of operation to be performed on the entities.
        type: str
        required: true
        choices:
            - CREATE
            - UPDATE
    tenant_id:
        description:
            - ID of tenant for which configuration is being set up.
        type: str
        required: false
    config_list:
        description:
            - List of entities to be seeded.
        type: dict
        required: true
        suboptions:
            client_config:
                description:
                    - Client configuration to be seeded.
                type: dict
                required: false
                suboptions:
                    legacy_client_name:
                        description:
                            - Identifier for the old/legacy client name.
                        type: str
                        required: false
                    name:
                        description:
                            - Name of the client.
                        type: str
                        required: false
                    description:
                        description:
                            - Description of the client.
                        type: str
                        required: false
                    display_name:
                        description:
                            - Display name of the client.
                        type: str
                        required: false
                    deployment_list:
                        description:
                            - List of deployments for the client.
                        type: list
                        elements: str
                        required: false
            entity_list:
                description:
                    - The entities config that will be seeded.
                type: dict
                required: false
                suboptions:
                    entities:
                        description:
                            - The entities config that will be seeded.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            legacy_object_list:
                                description:
                                    - List of old displayNames of the given entity which have been consolidated or renamed.
                                type: list
                                elements: str
                                required: false
                            is_internal:
                                description:
                                    - Flag identifying if the entity is internal or not.
                                type: bool
                                required: false
                            name:
                                description:
                                    - Name of the entity.
                                type: str
                                required: false
                            description:
                                description:
                                    - Description of the entity.
                                type: str
                                required: false
                            display_name:
                                description:
                                    - Display name of the entity.
                                type: str
                                required: false
                            client_name:
                                description:
                                    - Client name associated with the entity.
                                type: str
                                required: false
                            search_url:
                                description:
                                    - Search URL for the entity.
                                type: str
                                required: false
                            attribute_list:
                                description:
                                    - List of attributes supported for access control on this entity.
                                type: list
                                elements: dict
                                required: false
                                suboptions:
                                    display_name:
                                        description:
                                            - Display name of the entity's attribute used in Authorization Policy filters.
                                        type: str
                                        required: false
                                    name:
                                        description:
                                            - Name of the entity's attribute used in Authorization Policy filters.
                                        type: str
                                        required: false
                                    search_endpoint:
                                        description:
                                            - API endpoint used to search for entities associated with this attribute.
                                        type: str
                                        required: false
                                    version:
                                        description:
                                            - API version used to invoke the search endpoint for this attribute.
                                        type: str
                                        required: false
                                    search_field:
                                        description:
                                            - API field used to filter search results for this attribute.
                                        type: str
                                        required: false
                                    operator:
                                        description:
                                            - OData operator used to build the search filter for this attribute.
                                        type: str
                                        required: false
                                    id_field:
                                        description:
                                            - API response field containing the identifier for a selected entity.
                                        type: str
                                        required: false
                                    delegate_to_entity:
                                        description:
                                            - Name of another entity whose search configuration is used for this attribute.
                                        type: str
                                        required: false
                                    additional_filters:
                                        description:
                                            - Search field or filter expression applied when search is delegated to another entity.
                                        type: str
                                        required: false
                            is_logical_and_supported_for_attributes:
                                description:
                                    - Indicates if logical AND is supported for attributes.
                                type: bool
                                required: false
                            products:
                                description:
                                    - List of products associated with the entity.
                                type: list
                                elements: str
                                required: false
                                choices:
                                    - PC
                                    - NC
                                    - NCM
            operation_list:
                description:
                    - The operation objects that will be seeded.
                type: dict
                required: false
                suboptions:
                    operations:
                        description:
                            - The operation objects that will be seeded.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            is_internal:
                                description:
                                    - Flag to denote if operation is internal or not.
                                type: bool
                                required: false
                            legacy_operation_list:
                                description:
                                    - Legacy or existing Operation name(s) which have been replaced/consolidated by the new Operation name.
                                type: list
                                elements: str
                                required: false
                            legacy_parent_operation_list:
                                description:
                                    - Existing operation name(s) which have been split into operations including the given new Operation name.
                                type: list
                                elements: str
                                required: false
                            display_name:
                                description:
                                    - Display name of the operation.
                                type: str
                                required: false
                            description:
                                description:
                                    - Description of the operation.
                                type: str
                                required: false
                            entity_type:
                                description:
                                    - Entity type associated with the operation.
                                type: str
                                required: false
                            client_name:
                                description:
                                    - Client name for the operation.
                                type: str
                                required: false
                            allow_on_shared_entity:
                                description:
                                    - Flag to allow operation on shared entity.
                                type: bool
                                required: false
                            operation_type:
                                description:
                                    - Type of operation.
                                type: str
                                required: false
                                choices:
                                    - INTERNAL
                                    - EXTERNAL
                                    - SYSTEM_DEFINED_ONLY
                            related_operation_list:
                                description:
                                    - List of related operations.
                                type: list
                                elements: str
                                required: false
                            associated_endpoint_list:
                                description:
                                    - List of associated endpoints.
                                type: list
                                elements: dict
                                required: false
                                suboptions:
                                    api_version:
                                        description:
                                            - Version of the API for the provided associated endpoint.
                                        type: str
                                        required: false
                                    endpoint_url:
                                        description:
                                            - Endpoint URL.
                                        type: str
                                        required: false
                                    http_method:
                                        description:
                                            - HTTP method for the endpoint.
                                        type: str
                                        required: false
                                        choices:
                                            - GET
                                            - POST
                                            - PUT
                                            - DELETE
                                            - PATCH
                            products:
                                description:
                                    - List of products.
                                type: list
                                elements: str
                                required: false
            role_list:
                description:
                    - The role objects that will be seeded.
                type: dict
                required: false
                suboptions:
                    roles:
                        description:
                            - The role objects that will be seeded.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            legacy_role:
                                description:
                                    - Old IUN of the role.
                                type: str
                                required: false
                            is_internal:
                                description:
                                    - Flag identifying if the role is internal or not.
                                type: bool
                                required: false
                            description:
                                description:
                                    - Description of the role.
                                type: str
                                required: false
                            operations:
                                description:
                                    - List of operations for the role.
                                type: list
                                elements: str
                                required: false
                            accessible_clients:
                                description:
                                    - List of accessible clients.
                                type: list
                                elements: str
                                required: false
                            accessible_entity_types:
                                description:
                                    - List of accessible entity types.
                                type: list
                                elements: str
                                required: false
                            project_ext_id:
                                description:
                                    - External ID of the project.
                                type: str
                                required: false
                            is_shared_with_all_projects:
                                description:
                                    - Indicates if role is shared with all projects.
                                type: bool
                                required: false
                            display_name:
                                description:
                                    - Display name of the role.
                                type: str
                                required: false
                            client_name:
                                description:
                                    - Client name for the role.
                                type: str
                                required: false
                            is_global:
                                description:
                                    - Flag to indicate if the entity is global or not.
                                type: bool
                                required: false
                            products:
                                description:
                                    - List of products.
                                type: list
                                elements: str
                                required: false
                            is_system_defined:
                                description:
                                    - Indicates if role is system defined.
                                type: bool
                                required: false
            authorization_policy_list:
                description:
                    - The authorization policies config that will be seeded.
                type: dict
                required: false
                suboptions:
                    authorization_policies:
                        description:
                            - The authorization policies config that will be seeded.
                        type: list
                        elements: dict
                        required: true
                        suboptions:
                            opaquedata:
                                description:
                                    - Opaque data refers to the legacy filters used in the authorization policy.
                                type: str
                                required: false
                            is_internal:
                                description:
                                    - Flag identifying if the authorization policy is internal or not.
                                type: bool
                                required: false
                            project_ext_id:
                                description:
                                    - External ID of the project.
                                type: str
                                required: false
                            is_shared_with_all_projects:
                                description:
                                    - Indicates if policy is shared with all projects.
                                type: bool
                                required: false
                            display_name:
                                description:
                                    - Display name of the authorization policy.
                                type: str
                                required: false
                            description:
                                description:
                                    - Description of the authorization policy.
                                type: str
                                required: false
                            client_name:
                                description:
                                    - Client name for the authorization policy.
                                type: str
                                required: false
                            role:
                                description:
                                    - Role associated with the authorization policy.
                                type: str
                                required: false
                            is_global:
                                description:
                                    - Flag to indicate if the entity is global or not.
                                type: bool
                                required: false
                            domain_ext_ids:
                                description:
                                    - List of domain external IDs.
                                type: list
                                elements: str
                                required: false
                            authorization_policy_type:
                                description:
                                    - Type of authorization policy.
                                type: str
                                required: false
                                choices:
                                    - USER_DEFINED
                                    - PREDEFINED_READ_ONLY
                            identities:
                                description:
                                    - List of identities for the policy.
                                type: list
                                elements: dict
                                required: false
                            entities:
                                description:
                                    - List of entities for the policy.
                                type: list
                                elements: dict
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
- name: Seed entity configuration
  nutanix.ncp.ntnx_seed_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    config_type: ENTITY
    client_name: test_client
    operation_type: CREATE
    config_list:
      entity_list:
        entities:
          - name: test_entity_ansible
            display_name: Test Entity Ansible
            description: Test entity created via Ansible
            client_name: test_client
  register: result
  ignore_errors: true

- name: Seed operation configuration
  nutanix.ncp.ntnx_seed_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    config_type: OPERATION
    client_name: test_client
    operation_type: CREATE
    config_list:
      operation_list:
        operations:
          - display_name: Test Operation
            description: Test operation via Ansible
            entity_type: test_entity
            client_name: test_client
  register: result
  ignore_errors: true

- name: Seed role configuration
  nutanix.ncp.ntnx_seed_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    config_type: ROLE
    client_name: test_client
    operation_type: CREATE
    config_list:
      role_list:
        roles:
          - display_name: Test Role
            description: Test role via Ansible
            client_name: test_client
            operations:
              - op1
              - op2
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for seeding configuration.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "data": {
                "seed_status": "SUCCESS"
            },
            "metadata": {
                "total_available_results": 1
            }
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while seeding configuration"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_configuration_seeding_api_instance,
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
    attribute_entity_spec = dict(
        display_name=dict(type="str", required=False),
        name=dict(type="str", required=False),
        search_endpoint=dict(type="str", required=False),
        version=dict(type="str", required=False),
        search_field=dict(type="str", required=False),
        operator=dict(type="str", required=False),
        id_field=dict(type="str", required=False),
        delegate_to_entity=dict(type="str", required=False),
        additional_filters=dict(type="str", required=False),
    )

    entity_config_spec = dict(
        legacy_object_list=dict(type="list", elements="str", required=False),
        is_internal=dict(type="bool", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        display_name=dict(type="str", required=False),
        client_name=dict(type="str", required=False),
        search_url=dict(type="str", required=False),
        attribute_list=dict(
            type="list",
            elements="dict",
            options=attribute_entity_spec,
            obj=iam_sdk.AttributeEntity,
            required=False,
        ),
        is_logical_and_supported_for_attributes=dict(type="bool", required=False),
        products=dict(
            type="list",
            elements="str",
            required=False,
            choices=["PC", "NC", "NCM"],
        ),
    )

    seed_entity_list_spec = dict(
        entities=dict(
            type="list",
            elements="dict",
            options=entity_config_spec,
            obj=iam_sdk.EntityConfig,
            required=True,
        ),
    )

    associated_endpoint_spec = dict(
        api_version=dict(type="str", required=False),
        endpoint_url=dict(type="str", required=False),
        http_method=dict(
            type="str",
            required=False,
            choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
            obj=iam_sdk.HttpMethod,
        ),
    )

    operation_config_spec = dict(
        is_internal=dict(type="bool", required=False),
        legacy_operation_list=dict(type="list", elements="str", required=False),
        legacy_parent_operation_list=dict(type="list", elements="str", required=False),
        display_name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        entity_type=dict(type="str", required=False),
        client_name=dict(type="str", required=False),
        allow_on_shared_entity=dict(type="bool", required=False),
        operation_type=dict(
            type="str",
            required=False,
            choices=["INTERNAL", "EXTERNAL", "SYSTEM_DEFINED_ONLY"],
            obj=iam_sdk.OperationType,
        ),
        related_operation_list=dict(type="list", elements="str", required=False),
        associated_endpoint_list=dict(
            type="list",
            elements="dict",
            options=associated_endpoint_spec,
            obj=iam_sdk.AssociatedEndpoint,
            required=False,
        ),
        products=dict(type="list", elements="str", required=False),
    )

    seed_operation_list_spec = dict(
        operations=dict(
            type="list",
            elements="dict",
            options=operation_config_spec,
            obj=iam_sdk.OperationConfig,
            required=True,
        ),
    )

    role_config_spec = dict(
        legacy_role=dict(type="str", required=False),
        is_internal=dict(type="bool", required=False),
        description=dict(type="str", required=False),
        operations=dict(type="list", elements="str", required=False),
        accessible_clients=dict(type="list", elements="str", required=False),
        accessible_entity_types=dict(type="list", elements="str", required=False),
        project_ext_id=dict(type="str", required=False),
        is_shared_with_all_projects=dict(type="bool", required=False),
        display_name=dict(type="str", required=False),
        client_name=dict(type="str", required=False),
        is_global=dict(type="bool", required=False),
        products=dict(type="list", elements="str", required=False),
        is_system_defined=dict(type="bool", required=False),
    )

    seed_role_list_spec = dict(
        roles=dict(
            type="list",
            elements="dict",
            options=role_config_spec,
            obj=iam_sdk.RoleConfig,
            required=True,
        ),
    )

    authorization_policy_config_spec = dict(
        opaquedata=dict(type="str", required=False),
        is_internal=dict(type="bool", required=False),
        project_ext_id=dict(type="str", required=False),
        is_shared_with_all_projects=dict(type="bool", required=False),
        display_name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        client_name=dict(type="str", required=False),
        role=dict(type="str", required=False),
        is_global=dict(type="bool", required=False),
        domain_ext_ids=dict(type="list", elements="str", required=False),
        authorization_policy_type=dict(
            type="str",
            required=False,
            choices=["USER_DEFINED", "PREDEFINED_READ_ONLY"],
            obj=iam_sdk.AuthorizationPolicyType,
        ),
        identities=dict(type="list", elements="dict", required=False),
        entities=dict(type="list", elements="dict", required=False),
    )

    seed_authz_policy_list_spec = dict(
        authorization_policies=dict(
            type="list",
            elements="dict",
            options=authorization_policy_config_spec,
            obj=iam_sdk.AuthorizationPolicyConfig,
            required=True,
        ),
    )

    client_config_spec = dict(
        legacy_client_name=dict(type="str", required=False),
        name=dict(type="str", required=False),
        description=dict(type="str", required=False),
        display_name=dict(type="str", required=False),
        deployment_list=dict(type="list", elements="str", required=False),
    )

    config_list_spec = dict(
        client_config=dict(
            type="dict",
            options=client_config_spec,
            obj=iam_sdk.ClientConfig,
            required=False,
        ),
        entity_list=dict(
            type="dict",
            options=seed_entity_list_spec,
            obj=iam_sdk.SeedConfigEntityList,
            required=False,
        ),
        operation_list=dict(
            type="dict",
            options=seed_operation_list_spec,
            obj=iam_sdk.SeedConfigOperationList,
            required=False,
        ),
        role_list=dict(
            type="dict",
            options=seed_role_list_spec,
            obj=iam_sdk.SeedConfigRoleList,
            required=False,
        ),
        authorization_policy_list=dict(
            type="dict",
            options=seed_authz_policy_list_spec,
            obj=iam_sdk.SeedConfigAuthorizationPolicyList,
            required=False,
        ),
    )

    module_args = dict(
        config_type=dict(
            type="str",
            required=True,
            choices=[
                "CLIENT",
                "ENTITY",
                "OPERATION",
                "ROLE",
                "AUTHORIZATION_POLICY",
            ],
            obj=iam_sdk.SeedConfigType,
        ),
        client_name=dict(type="str", required=True),
        operation_type=dict(
            type="str",
            required=True,
            choices=["CREATE", "UPDATE"],
            obj=iam_sdk.SeedConfigOperationType,
        ),
        tenant_id=dict(type="str", required=False),
        config_list=dict(
            type="dict",
            options=config_list_spec,
            obj={
                "client_config": iam_sdk.ClientConfig,
                "entity_list": iam_sdk.SeedConfigEntityList,
                "operation_list": iam_sdk.SeedConfigOperationList,
                "role_list": iam_sdk.SeedConfigRoleList,
                "authorization_policy_list": iam_sdk.SeedConfigAuthorizationPolicyList,
            },
            required=True,
            mutually_exclusive=[
                ("client_config", "entity_list"),
                ("client_config", "operation_list"),
                ("client_config", "role_list"),
                ("client_config", "authorization_policy_list"),
                ("entity_list", "operation_list"),
                ("entity_list", "role_list"),
                ("entity_list", "authorization_policy_list"),
                ("operation_list", "role_list"),
                ("operation_list", "authorization_policy_list"),
                ("role_list", "authorization_policy_list"),
            ],
            required_one_of=[
                (
                    "client_config",
                    "entity_list",
                    "operation_list",
                    "role_list",
                    "authorization_policy_list",
                ),
            ],
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.SeedConfigRequest()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating seed config spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.seed_config(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while seeding configuration",
        )

    # Response is SeedConfigApiResponse with metadata and data
    if resp:
        try:
            resp_dict = resp.to_dict()
            result["response"] = strip_internal_attributes(resp_dict)
        except Exception:
            result["response"] = (
                strip_internal_attributes(resp.to_dict())
                if hasattr(resp, "to_dict")
                else str(resp)
            )
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

    api_instance = get_configuration_seeding_api_instance(module)
    run_action(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
