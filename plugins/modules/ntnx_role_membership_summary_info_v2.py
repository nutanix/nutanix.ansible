#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_role_membership_summary_info_v2
short_description: Fetch role membership summary information using Nutanix v4 APIs
version_added: "2.7.0"
description:
    - This module is in Beta because the underlying Nutanix SDK API is currently in Beta.
    - The module and its behavior may change in future releases as the SDK API evolves.
    - Fetch role membership summaries from Nutanix Prism Central.
    - A role membership summary aggregates, per project, the counts of distinct
      identities (users and groups) and roles that have role memberships in that
      project.
    - The underlying v4 API only supports a list operation, so this module always
      returns a list of role membership summaries, optionally narrowed with a
      filter, limit, select, orderby or page.
    - This module uses PC v4 APIs based SDKs.
notes:
    - This module talks to Prism Central (PC), not to an FCVM/Foundation endpoint.
    - >-
      B(List role membership summaries) -
      Requires an IAM role on Prism Central that grants read access to role
      memberships (for example Super Admin or Prism Admin).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options: {}
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all role membership summaries
  nutanix.ncp.ntnx_role_membership_summary_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List role membership summaries with limit
  nutanix.ncp.ntnx_role_membership_summary_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result

- name: List role membership summaries with filter
  nutanix.ncp.ntnx_role_membership_summary_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "extId eq '00000000-0000-0000-0000-000000000000'"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Role Membership Summary info v4 API.
        - The host for this module is Prism Central (PC).
        - The underlying API only supports a list operation, so this is always a
          list of role membership summaries.
        - Each summary contains the per-project counts of identities, users,
          groups and roles.
        - Returns an empty list when there are no role membership summaries.
    returned: always
    type: dict
    sample: [
        {
            "ext_id": "00000000-0000-0000-0000-000000000000",
            "groups_count": 1,
            "roles_count": 2,
            "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
            "total_identities_count": 3,
            "users_count": 2
        }
    ]

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

total_available_results:
    description: Total number of available role membership summaries.
    returned: When listing role membership summaries
    type: int
    sample: 5

msg:
    description: Additional message about the operation.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while listing role membership summaries"

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_role_membership_api_instance,
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
    module_args = dict()
    return module_args


def get_role_membership_summaries(module, role_memberships, result):
    """
    List role membership summaries with optional filters and pagination.
    Args:
        module: Ansible module object
        role_memberships: RoleMembershipApi instance
        result: Result dict to populate
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating list role membership summaries spec", **result
        )

    try:
        resp = role_memberships.list_role_membership_summary(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing role membership summaries",
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
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib(iam_sdk.__name__),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    role_memberships = get_role_membership_api_instance(module)
    get_role_membership_summaries(module, role_memberships, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
