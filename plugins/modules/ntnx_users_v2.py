#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_users_v2
short_description: Module to create, update and delete users from Nutanix PC
version_added: "2.0.0"
description:
    - This module allows you to create, update and delete users.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create user) -
      Required Roles: Nutanix Central Admin, Prism Admin, Project Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Update user) -
      Required Roles: Nutanix Central Admin, Prism Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Delete user) -
      Required Roles: Nutanix Central Admin, Prism Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
    state:
        description:
            - State of the user. Whether to create, update or delete.
            - If C(state) is C(present) and C(ext_id) is not provided, create a new user.
            - If C(state) is C(present) and C(ext_id) is provided, update the user.
            - If C(state) is C(absent) and C(ext_id) is provided, delete the user.
        type: str
        choices: ['present', 'absent']
        default: present
    ext_id:
        description:
            - External ID of the User.
            - Required for updating or deleting a User.
        required: false
        type: str
    username:
        description:
            - Identifier for the User in the form an email address.
            - Required for creating a User.
        required: false
        type: str
    user_type:
        description:
            - Type of the User.
        required: false
        type: str
        choices: ['LOCAL', 'SAML', 'LDAP', 'EXTERNAL', 'SERVICE_ACCOUNT']
    display_name:
        description:
            - Display name for the User.
        required: false
        type: str
    first_name:
        description:
            - First name for the User.
        required: false
        type: str
    middle_initial:
        description:
            - Middle name for the User.
        required: false
        type: str
    last_name:
        description:
            - Last name for the User.
        required: false
        type: str
    email_id:
        description:
            - Email Id for the User.
        required: false
        type: str
    locale:
        description:
            - Default locale for the User.
        required: false
        type: str
    region:
        description:
            - Default Region for the User.
        required: false
        type: str
    password:
        description:
            - Password for the User.
            - Use this for local user only.
        required: false
        type: str
    idp_id:
        description:
            - Identifier of the IDP for the User.
            - Mandatory for creating LDAP and SAML users.
        required: false
        type: str
    is_force_reset_password_enabled:
        description:
            - Flag to force the User to reset password.
            - Supported for local users only.
        required: false
        type: bool
        default: false
    additional_attributes:
        description:
            - Any additional attribute for the User.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: The key of this key-value pair
                type: str
            value:
                description:
                    - The value associated with the key for this key-value pair
                    - Supported for creating users only.
                type: str
    status:
        description:
            - Status of the User.
            - Supported for creating users only.
        required: false
        type: str
        choices: ['ACTIVE', 'INACTIVE']
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false
        default: true
    description:
        description:
            - Description of the User.
        required: false
        type: str
    creation_type:
        description:
            - The creation mechanism of this entity.
        required: false
        type: str
        choices: ['PREDEFINED', 'SERVICEDEFINED', 'USERDEFINED']
    soft_delete:
        description:
            - When set to true, the user/user group is soft deleted. Else it is hard deleted.
        required: false
        type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
 - Abhinav Bansal (@abhinavbansal29)
"""


EXAMPLES = r"""
- name: create local user
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    idp_id: "40fe7aeb-f420-5aee-ba42-cfc2369bc1ec"
    user_type: LOCAL
    username: "ssptest111@qa.nucalm.io"
    first_name: firstName
    last_name: lastName
    password: test.Password.123
    is_force_reset_password_enabled: true
  register: result

- name: update local user
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "27892065-1d1b-5d66-ab17-a26038088b17"
    first_name: "firstNameUpdated"
    last_name: "lastNameUpdated"
  register: result

- name: Create SAML user
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_type: SAML
    username: "user_test"
    idp_id: "40fe7aeb-f420-5aee-ba42-cfc2369bc1ec"

- name: Create LDAP user
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_type: LDAP
    username: "user_test"
    idp_id: "40fe7aeb-f420-5aee-ba42-cfc2369bc1ec"

- name: Create Service Account
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    user_type: SERVICE_ACCOUNT
    username: "service_acc_1"
    email_id: "service_acc_1@email.com"
    description: "description_1"
  register: result

- name: Update Service Account
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "87892065-1d1b-5d66-ab17-a26038488b17"
    email_id: "service_acc_1_updated@email.com"
    description: "description_1_updated"
  register: result

- name: Delete user
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "27892065-1d1b-5d66-ab17-a26038088b17"
  register: result

- name: Delete user with soft delete
  nutanix.ncp.ntnx_users_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "27892065-1d1b-5d66-ab17-a26038088b17"
    soft_delete: true
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for creating, updating, or deleting users.
        - If C(wait) is true and the operation is Create or Update, it will contain the user details.
        - If C(wait) is false or the operation is Delete, it will contain the task details.
    type: dict
    returned: always
    sample:
      {
        "additional_attributes": [
          {
            "name": "attr1",
            "value": "value1"
          }
        ],
        "buckets_access_keys": null,
        "created_by": "00000000-0000-0000-0000-000000000000",
        "created_time": "2026-11-19T13:05:25.745971+00:00",
        "creation_type": "USERDEFINED",
        "default_landing_page_path": null,
        "description": "",
        "display_name": "test-displayname",
        "email_id": "test-ansible@example.com",
        "ext_id": "7d52f697-d9fb-559d-9fc9-cae9639a4bc4",
        "external_identifier": null,
        "first_name": "test-firstname",
        "has_object_keys": null,
        "idp_id": "37f30135-455b-5ebd-995f-b47e817a59f2",
        "is_force_reset_password_enabled": true,
        "last_login_time": "2026-11-19T13:05:25.711808+00:00",
        "last_name": "test-lastname",
        "last_updated_by": "00000000-0000-0000-0000-000000000000",
        "last_updated_time": "2026-11-19T13:05:25.745971+00:00",
        "links": null,
        "locale": "en-US",
        "middle_initial": "M",
        "password": null,
        "region": "en-US",
        "status": "ACTIVE",
        "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
        "user_group_ext_ids": null,
        "user_type": "LOCAL",
        "username": "test-ansible-user-79570"
      }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str
  sample: null

task_ext_id:
  description: The external ID of the task.
  returned: when task is created
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description: The external ID of the user.
  returned: always
  type: str
  sample: "27892065-1d1b-5d66-ab17-a26038088b17"

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

skipped:
  description: This indicates whether the task was skipped
  returned: when module is idempotent
  type: bool
  sample: false

msg:
    description: This field typically holds a message that is displayed to the user
    returned: when there is an error, module is idempotent or in check mode for delete
    type: str
    sample: "User with ext_id: 27892065-1d1b-5d66-ab17-a26038088b17 deleted successfully"
"""
import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_user_api_instance,
)
from ..module_utils.v4.iam.helpers import get_user  # noqa: E402
from ..module_utils.v4.iam.spec.iam import UserSpecs as user_specs  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_users_empty_attributes,
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
    module_args = user_specs.get_users_spec()
    module_args.update(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        soft_delete=dict(type="bool", required=False),
    )
    return module_args


def create_user(module, users, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.User()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create users spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = users.create_user(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating user",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_users_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False
    return True


def update_user(module, users, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_user(module, users, ext_id=ext_id)

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating users update spec", **result)

    # check for idempotency
    if not module.params.get("password"):
        if check_users_idempotency(current_spec.to_dict(), update_spec.to_dict()):
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = users.update_user_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating user",
        )

    resp = get_user(module, users, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_user(module, users, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "User with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_user(module, users, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(msg="Unable to fetch etag for deleting user", **result)

    kwargs = {"if_match": etag}
    soft_delete = module.params.get("soft_delete")
    if soft_delete is not None:
        kwargs["Soft_Delete"] = soft_delete

    try:
        resp = users.delete_user_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting user",
        )

    result["changed"] = True
    if resp is not None and hasattr(resp, "data") and resp.data is not None:
        # Handle task-based or empty response
        try:
            result["response"] = strip_internal_attributes(resp.data.to_dict())
        except Exception:
            result["response"] = strip_internal_attributes(resp.to_dict())
        # If response contains task ext_id, capture it
        if hasattr(resp.data, "ext_id") and resp.data.ext_id:
            result["task_ext_id"] = resp.data.ext_id
    else:
        result["msg"] = "User with ext_id: {0} deleted successfully".format(ext_id)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
        mutually_exclusive=[
            ("ext_id", "username"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    users = get_user_api_instance(module)
    if state == "absent":
        delete_user(module, users, result)
    elif module.params.get("ext_id"):
        update_user(module, users, result)
    else:
        create_user(module, users, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
