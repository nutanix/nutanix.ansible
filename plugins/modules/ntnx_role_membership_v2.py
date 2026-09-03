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
            - If C(state) is set to C(absent) and C(ext_id) is provided, the module will delete the role membership.
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
            - Type of identity associated with the role membership.
        type: str
        choices:
            - USER
            - GROUP
    identity_ext_id:
        description:
            - External identifier of the identity (user or group) associated with the role membership.
        type: str
    scope_template_name:
        description:
            - Display name of the scope template for the authorization policy created via the role membership.
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
            - External Identifier of the identity provider associated with the role membership.
        type: str
    project_ext_id:
        description:
            - External identifier of the project associated with the role membership.
            - Defaults to C(00000000-0000-0000-0000-000000000000) if not provided.
        type: str
        default: 00000000-0000-0000-0000-000000000000
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
    role_ext_id: "93939393-9393-9393-9393-939393939393"
    identity_type: "USER"
    identity_ext_id: "90909090-9090-9090-9090-909090909090"
    scope_template_name: "ProjectsScopeTemplate"
    scope_template_name_values:
      - name: "projectExtId"
        value: "44444444-4444-4444-4444-444444444444"
    idp_ext_id: "99999999-9999-9999-9999-999999999999"
    project_ext_id: "44444444-4444-4444-4444-444444444444"
  register: result

- name: Delete a role membership
  nutanix.ncp.ntnx_role_membership_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "12345678-1234-1234-1234-123456789012"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for creating or deleting role memberships.
        - Role membership details if the operation is create.
        - Delete success message if the operation is delete.
    returned: always
    type: dict
    sample: {
        "authorization_policy_ext_id": "a313661d-b127-5446-bd18-31366273637e",
        "created_by": "00000000-0000-0000-0000-000000000000",
        "created_time": "2026-06-02T08:32:09.680175+00:00",
        "ext_id": "44844104-873b-5a14-a89c-ea6fb67d6055",
        "identity_ext_id": "f6dbbd12-cecd-5a54-88bb-bc1abc7468d4",
        "identity_type": "USER",
        "identity_value": "f6dbbd12-cecd-5a54-88bb-bc1abc7468d4",
        "idp_ext_id": "0572e531-4c2c-57ef-92a6-b33aabe61806",
        "key_value_pairs": [
            {
                "key": "projectExtId",
                "value": "00000000-0000-0000-0000-000000000000"
            }
        ],
        "last_updated_time": "2026-06-02T08:32:09.680175+00:00",
        "project_ext_id": "00000000-0000-0000-0000-000000000000",
        "role_ext_id": "468c1fe7-d986-5788-af71-72c3031bc98d",
        "scope_template_name": "ProjectsScopeTemplate",
        "scope_template_name_values": [
            {
                "name": "projectExtId",
                "value": "00000000-0000-0000-0000-000000000000"
            }
        ],
        "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df"
    }

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: true

ext_id:
    description: The external ID of the role membership.
    returned: always
    type: str
    sample: "44844104-873b-5a14-a89c-ea6fb67d6055"

msg:
    description: Additional message about the operation.
    returned: When there is an error or delete operation.
    type: str
    sample: "Role membership with ext_id:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee will be deleted."

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: always
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
        project_ext_id=dict(type="str", default="00000000-0000-0000-0000-000000000000"),
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
        module,
        [
            "role_ext_id",
            "identity_type",
            "identity_ext_id",
            "idp_ext_id",
            "scope_template_name",
        ],
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

    resp_data = strip_internal_attributes(resp.data.to_dict())
    ext_id = resp.data.ext_id
    result["ext_id"] = ext_id
    result["response"] = resp_data

    if ext_id and module.params.get("wait"):
        resp = get_role_membership(module, role_memberships, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


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
    if resp is None:
        result["msg"] = "Role membership with ext_id: {} deleted successfully".format(
            ext_id
        )
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
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
        "failed": False,
        "response": None,
        "ext_id": None,
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
