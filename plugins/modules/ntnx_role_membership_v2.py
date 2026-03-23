#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_role_membership_v2
short_description: Manage role memberships in Nutanix Prism Central using v4 APIs
version_added: "2.6.0"
description:
    - Create and delete role memberships in Nutanix Prism Central.
    - Role memberships bind a role to an identity (user or user group) within a scope.
    - The IAM Role Membership API does not support update operations.
    - This module uses PC v4 APIs based SDKs.
options:
    state:
        description:
            - Specify state.
            - If C(state) is set to C(present), the module will create a role membership.
            - If C(state) is set to C(absent) with C(ext_id), the module will delete the role membership.
            - Update is not supported by the Role Membership API.
        choices:
            - present
            - absent
        type: str
        default: present
    ext_id:
        description:
            - The external ID of the role membership.
            - Required for C(state)=absent for delete.
        type: str
    role_ext_id:
        description:
            - The external ID of the role to assign.
            - Required for create operations.
        type: str
    identity_type:
        description:
            - The type of identity to which the role is being assigned.
        type: str
        choices:
            - USER
            - GROUP
    identity_ext_id:
        description:
            - The external ID of the identity (user or user group) to which the role is assigned.
        type: str
    scope_template_name:
        description:
            - The name of the scope template to use for the role membership.
        type: str
    scope_template_name_values:
        description:
            - Name-value pairs to substitute in the scope template variables
              referenced by the role membership.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The key of the key-value pair.
                type: str
            value:
                description:
                    - The value associated with the key.
                type: raw
    idp_ext_id:
        description:
            - The external ID of the identity provider.
        type: str
    project_ext_id:
        description:
            - The external ID of the project for scoped role membership.
            - Defaults to C(00000000-0000-0000-0000-000000000000) if not provided.
        type: str
    authorization_policy_ext_id:
        description:
            - The external ID of the authorization policy.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create a role membership for a user
  nutanix.ncp.ntnx_role_membership_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    role_ext_id: "{{ role_ext_id }}"
    identity_type: "USER"
    identity_ext_id: "{{ user_ext_id }}"
    scope_template_name: "ProjectsScopeTemplate"
    idp_ext_id: "{{ idp_ext_id }}"
    project_ext_id: "{{ project_ext_id }}"
  register: result

- name: Delete a role membership
  nutanix.ncp.ntnx_role_membership_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "{{ role_membership_ext_id }}"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Role Membership v4 API.
        - It will contain the role membership details after create.
    returned: always
    type: dict
    sample: "<Need to add sample>"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the role membership.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"

task_ext_id:
    description: The external ID of the task created for the operation.
    returned: always
    type: str
    sample: null

skipped:
    description: Whether the operation was skipped due to no changes (idempotency).
    returned: When module is idempotent
    type: bool
    sample: true

msg:
    description: Additional message about the operation.
    returned: When there is an error, module is idempotent or check mode (in delete operation)
    type: str
    sample: "Nothing to change."

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_role_membership_api_instance,
)
from ..module_utils.v4.iam.helpers import get_role_membership  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
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
    kv_pair_spec = dict(
        name=dict(type="str"),
        value=dict(type="raw"),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        role_ext_id=dict(type="str"),
        identity_type=dict(type="str", choices=["USER", "GROUP"]),
        identity_ext_id=dict(type="str"),
        scope_template_name=dict(type="str"),
        scope_template_name_values=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            obj=iam_sdk.KVPair,
        ),
        idp_ext_id=dict(type="str"),
        project_ext_id=dict(type="str"),
        authorization_policy_ext_id=dict(type="str"),
    )
    return module_args


def create_role_membership(module, role_memberships, result):
    """
    Create a new role membership.
    Args:
        module: Ansible module object
        role_memberships: RoleMembershipApi instance
        result: Result dict to populate
    """
    validate_required_params(
        module, ["role_ext_id", "identity_type", "identity_ext_id", "idp_ext_id"]
    )

    sg = SpecGenerator(module)
    default_spec = iam_sdk.RoleMembership()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create role membership spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = role_memberships.create_role_membership(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating role membership",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_role_membership_idempotency(old_spec, update_spec):
    """
    Check if the role membership spec has changed.
    Args:
        old_spec (dict): Current role membership spec
        update_spec (dict): Updated role membership spec
    Returns:
        bool: True if specs are identical (no change needed)
    """
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False
    return True


def delete_role_membership(module, role_memberships, result):
    """
    Delete a role membership by its external ID.
    Args:
        module: Ansible module object
        role_memberships: RoleMembershipApi instance
        result: Result dict to populate
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Role membership with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_role_membership(module, role_memberships, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting role membership", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = role_memberships.delete_role_membership_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting role membership",
        )

    result["changed"] = True
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "present",
                ("role_ext_id", "identity_type", "identity_ext_id", "idp_ext_id"),
            ),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }

    role_memberships = get_role_membership_api_instance(module)

    state = module.params["state"]
    if state == "present":
        create_role_membership(module, role_memberships, result)
    else:
        delete_role_membership(module, role_memberships, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
