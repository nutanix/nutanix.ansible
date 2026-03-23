#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_role_memberships_info_v2
short_description: Fetch role membership information using Nutanix v4 APIs
version_added: "2.6.0"
description:
    - Fetch information about role memberships from Nutanix Prism Central.
    - Retrieve a single role membership by external ID or list all role memberships with optional filters.
    - This module uses PC v4 APIs based SDKs.
options:
    ext_id:
        description:
            - The external ID (UUID) of the role membership to retrieve.
            - Mutually exclusive with C(filter).
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Get all role memberships
  nutanix.ncp.ntnx_role_memberships_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Get role membership by ext_id
  nutanix.ncp.ntnx_role_memberships_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ role_membership_ext_id }}"
  register: result

- name: List role memberships with filter
  nutanix.ncp.ntnx_role_memberships_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "roleExtId eq '{{ role_ext_id }}'"
  register: result

- name: List role memberships with limit
  nutanix.ncp.ntnx_role_memberships_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Role Memberships info v4 API.
        - It can be a single role membership if external ID is provided.
        - List of multiple role memberships if external ID is not provided.
    returned: always
    type: dict
    sample: "<Need to add sample>"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

ext_id:
    description: The external ID of the role membership.
    returned: When single entity is fetched
    type: str
    sample: "00000000-0000-0000-0000-000000000000"

total_available_results:
    description: Total number of available results when listing role memberships.
    returned: When listing role memberships
    type: int
    sample: 5

msg:
    description: Additional message about the operation.
    returned: When there is an error
    type: str

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
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_role_membership_api_instance,
)
from ..module_utils.v4.iam.helpers import get_role_membership  # noqa: E402
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
    )
    return module_args


def get_role_membership_by_ext_id(module, role_memberships, result):
    """
    Fetch a single role membership by its external ID.
    Args:
        module: Ansible module object
        role_memberships: RoleMembershipApi instance
        result: Result dict to populate
    """
    ext_id = module.params.get("ext_id")
    resp = get_role_membership(module, role_memberships, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_role_memberships_list(module, role_memberships, result):
    """
    List role memberships with optional filters and pagination.
    Args:
        module: Ansible module object
        role_memberships: RoleMembershipApi instance
        result: Result dict to populate
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list role memberships spec", **result)

    try:
        resp = role_memberships.list_role_memberships(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing role memberships",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib(iam_sdk.__name__),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}

    role_memberships = get_role_membership_api_instance(module)

    if module.params.get("ext_id"):
        get_role_membership_by_ext_id(module, role_memberships, result)
    else:
        get_role_memberships_list(module, role_memberships, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
