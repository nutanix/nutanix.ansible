#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_groups_info_v2
short_description: Fetch user groups
version_added: 2.0.0
description:
    - This module is used to get user_group information.
    - Fetch a specific user group using ext_id or multiple user groups
options:
    ext_id:
        description:
            - user_group external ID
            - If used, specific user group information will be fetched. Else, all user groups will be fetched.
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List all user groups
  ntnx_user_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: user_groups

- name: List user_groups using user_group uuid criteria
  ntnx_user_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "119e6031-93e3-40b8-bd2e-2537522d629f"
  register: result

- name: List user_groups using filter criteria
  ntnx_user_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'test_user_group_name'"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching user group information.
        - User group info if ext_id is provided.
        - List of user groups if ext_id is not provided.
    type: dict
    returned: always
    sample:
        {
        "created_by": "00000000-0000-0000-0000-000000000000",
        "created_time": "2024-05-29T08:52:41.075478+00:00",
        "distinguished_name": "cn=sspgroupqa1,cn=users,dc=qa,dc=nucalm,dc=io",
        "ext_id": "119e6031-93e3-40b8-bd2e-2537522d629f",
        "group_type": "LDAP",
        "idp_id": "6863c60b-ae9d-5c32-b8c1-2d45b9ba343a",
        "last_updated_time": "2024-05-29T08:52:41.075478+00:00",
        "links": null,
        "name": "sspgroupqa1",
        "tenant_id": null
        }

ext_id:
    description:
        - user_group external ID when specific user group is fetched
    type: str
    returned: always
    sample: "119e6031-93e3-40b8-bd2e-2537522d629f"

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

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_user_group_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_user_group  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_user_group_by_ext_id(module, user_groups, result):
    ext_id = module.params.get("ext_id")
    resp = get_user_group(module, user_groups, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_user_groups(module, user_groups, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating user groups info Spec", **result)

    try:
        resp = user_groups.list_user_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching user groups info",
        )

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
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    user_groups = get_user_group_api_instance(module)
    if module.params.get("ext_id"):
        get_user_group_by_ext_id(module, user_groups, result)
    else:
        get_user_groups(module, user_groups, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
