#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_groups_v2
short_description: Create and Delete user groups
description:
    - Create and Delete user groups in Nutanix PC
    - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
    state:
        description:
            - State of the user group, whether to create or delete.
            - When C(state) is present, it will create user group.
            - When C(state) is absent, it will delete user group.
        type: str
        choices: ['present', 'absent']
    ext_id:
        description:
            - User Group External ID.
            - Required for deleting a user group.
        type: str
    name:
        description:
            - Common Name of the User Group.
            - Mandatory for SAML User Group.
        type: str
    distinguished_name:
        description:
            - Identifier for the User Group in the form of a distinguished name.
            - Mandatory for LDAP User Group.
        type: str
    idp_id:
        description:
            - Identifier of the IDP for the User Group.
        type: str
    group_type:
        description:
            - Type of the User Group.
        type: str
        choices: ['SAML', 'LDAP']
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false
        default: true
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create LDAP user group
  nutanix.ncp.ntnx_user_groups_v2:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      group_type: "LDAP"
      distinguished_name: "test_distinguished_name"
      idp_id: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"

- name: Create SAML user group
  nutanix.ncp.ntnx_user_groups_v2:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      group_type: "SAML"
      idp_id: "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a"
      name: group_name_test

- name: Delete user group
  nutanix.ncp.ntnx_user_groups_v2:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: false
      state: absent
      ext_id: "ext_id"
"""

RETURN = r"""
response:
    description:
        - Response of user group operation.
        - User group details if C(wait) is True.
        - Task details if C(wait) is False.
    type: dict
    returned: always
    sample:
        {
        "created_by": "00000000-0000-0000-0000-000000000000",
        "created_time": "2024-06-26T22:56:55.763219-07:00",
        "distinguished_name": null,
        "ext_id": "b94694bd-cd7f-5ba1-88f7-ca96306da024",
        "group_type": "SAML",
        "idp_id": "40fe7aeb-f420-5aee-ba42-cfc2369bc1ec",
        "last_updated_time": "2024-06-26T22:56:55.763219-07:00",
        "links": null,
        "name": "group_name2_wtkhkeqsivby",
        "tenant_id": null
        }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error or in delete operation
  type: str
  sample: "Api Exception raised while creating user group"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

ext_id:
  description: The created user group external ID
  returned: always
  type: str
  sample: "b94694bd-cd7f-5ba1-88f7-ca96306da024"

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_user_group_api_instance,
)
from ..module_utils.v4.iam.helpers import get_user_group  # noqa: E402
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
        name=dict(type="str"),
        distinguished_name=dict(type="str"),
        idp_id=dict(type="str"),
        group_type=dict(type="str", choices=["SAML", "LDAP"]),
    )
    return module_args


def create_user_group(module, user_groups, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.UserGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create user groups spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = user_groups.create_user_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating user group",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_user_group(module, user_groups, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "User group with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_user_group(module, user_groups, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for deleting user groups", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = user_groups.delete_user_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting user group",
        )

    result["changed"] = True
    if resp is None:
        result["msg"] = "User group with ext_id: {} deleted successfully".format(ext_id)
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "distinguished_name", "ext_id"), True),
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
    user_groups = get_user_group_api_instance(module)
    if state == "present":
        create_user_group(module, user_groups, result)
    else:
        delete_user_group(module, user_groups, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
