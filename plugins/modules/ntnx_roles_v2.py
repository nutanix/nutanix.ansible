#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_roles_v2
short_description: Create, update, and delete roles.
description:
    - This module allows you to create, update, and delete roles.
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
    state:
        description:
            - State of the role. Whether to create, update, or delete.
            - If C(state) is C(present) and C(ext_id) is not provided, create a new role.
            - If C(state) is C(present) and C(ext_id) is provided, update the role.
            - If C(state) is C(absent), it will delete the role with the given External ID.
        type: str
        choices: ['present', 'absent']
    ext_id:
        description:
            - Role External ID.
            - Required for updating or deleting the role.
        type: str
        required: false
    display_name:
        description:
            - The display name for the Role.
        type: str
        required: false
    description:
        description:
            - Description of the Role.
        type: str
        required: false
    client_name:
        description:
            - Client that created the entity.
        type: str
        required: false
    operations:
        description:
            - List of Operations external IDs for the Role.
            - During update operation, all given operations will override the existing operations.
        type: list
        elements: str
        required: false
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
      - nutanix.ncp.ntnx_logger_v2
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create roles with operations
  nutanix.ncp.ntnx_roles_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    display_name: "Display_Name_Test"
    description: test-ansible-role-1-desc
    operations:
      - "251d4a4f-244f-4c84-70a9-8c8f68f9dff0"
      - "0194fbfd-a5d1-49f8-46f4-e4b01d0abe47"

- name: Update all fields
  nutanix.ncp.ntnx_roles_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
    display_name: "Display_Name_Test_Updated"
    description: test-ansible-role-3-desc-updated
    operations:
      - "0194fbfd-a5d1-49f8-46f4-e4b01d0abe47"

- name: delete role
  nutanix.ncp.ntnx_roles_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
"""

RETURN = r"""
response:
    description:
        - Response of roles operations.
        - Roles details if C(wait) is True
        - Task details if C(wait) is False
    returned: always
    type: dict
    sample:
        {
                "accessible_clients": [
                    "FilesManagerService"
                ],
                "accessible_entity_types": [
                    "Files"
                ],
                "assigned_user_groups_count": 0,
                "assigned_users_count": 0,
                "client_name": "IAM",
                "created_by": "00000000-0000-0000-0000-000000000000",
                "created_time": "2024-06-24T12:59:39.966377+00:00",
                "description": "test-ansible-role-1-desc",
                "display_name": "role_name_iUPLDmxsGfOr",
                "ext_id": "13a6657d-fa96-49e3-7307-87e93a1fec3d",
                "is_system_defined": false,
                "last_updated_time": "2024-06-24T12:59:39.966377+00:00",
                "links": null,
                "operations": [
                    "251d4a4f-244f-4c84-70a9-8c8f68f9dff0",
                    "0194fbfd-a5d1-49f8-46f4-e4b01d0abe47"
                ],
                "tenant_id": null
            }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

ext_id:
  description: The created role's External ID
  returned: always
  type: str
  sample: "13a6657d-fa96-49e3-7307-87e93a1fec3d"

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

"""


import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_role_api_instance,
)
from ..module_utils.v4.iam.helpers import get_role  # noqa: E402
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
        ext_id=dict(type="str"),
        display_name=dict(type="str"),
        description=dict(type="str"),
        client_name=dict(type="str"),
        operations=dict(type="list", elements="str"),
    )
    return module_args


def create_role(module, result):
    roles = get_role_api_instance(module)
    sg = SpecGenerator(module)
    default_spec = iam_sdk.Role()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create Roles Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = roles.create_role(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating role",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_roles_idempotency(old_spec, update_spec):
    old_operations = old_spec.pop("operations")
    new_operations = update_spec.pop("operations")
    if old_spec != update_spec:
        return False
    if set(old_operations) != set(new_operations):
        return False
    return True


def update_role(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    roles = get_role_api_instance(module)
    current_spec = get_role(module, roles, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating roles update spec", **result)

    # check for idempotency
    if check_roles_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = roles.update_role_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating role",
        )

    resp = get_role(module, roles, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_role(module, result):
    roles = get_role_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Role with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_role(module, roles, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("unable to fetch etag for deleting role", **result)

    kwargs = {"if_match": etag}

    try:
        resp = roles.delete_role_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting role",
        )

    result["changed"] = True
    result["response"] = resp


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("display_name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
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
    if state == "present":
        if module.params.get("ext_id"):
            update_role(module, result)
        else:
            create_role(module, result)
    else:
        delete_role(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
