#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_roles_info_v2
short_description: Get roles info
version_added: 2.0.0
description:
    - Get roles info using roles external ID or list all roles
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - This module is used to get roles info
            - It can be used to get roles info using roles external ID or list all roles
        type: str
        required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: List roles
  nutanix.ncp.ntnx_roles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch role using uuid criteria
  nutanix.ncp.ntnx_roles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
  register: result

- name: List roles using filter
  nutanix.ncp.ntnx_roles_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "displayName eq 'Display_Name_Test'"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching roles info
        - Returns roles info using roles external ID or list all roles
    type: dict
    returned: always
    sample:
        {
            "accessible_clients": [
                "Networking",
                "License Manager",
                "AIOps",
            ],
            "accessible_entity_types": [
                "Remote Syslog Server",
                "Disk",
                "Rack",
                "Rackable Unit",
                "Host",
            ],
            "assigned_user_groups_count": 0,
            "assigned_users_count": 1,
            "client_name": "Prism",
            "created_by": "",
            "created_time": "2024-05-28T09:24:59.584696+00:00",
            "description": "View-only admin of a Nutanix deployment. Has access to all infrastructure and platform features, but cannot make any changes.",
            "display_name": "Prism Viewer",
            "ext_id": "5171e1de-ac44-422b-8d40-dd0ff2bc2b5a",
            "is_system_defined": true,
            "last_updated_time": "2024-05-28T09:25:06.642563+00:00",
            "links": null,
            "operations": [
                "10245831-6013-48de-94c7-dd2e9e298b91",
                "443c7424-86de-4ea4-8fa8-cc5fe894066b",
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

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

total_available_results:
    description: The total number of available roles in PC.
    type: int
    returned: when all roles are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import get_role_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_role  # noqa: E402
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


def get_role_by_ext_id(module, roles, result):
    ext_id = module.params.get("ext_id")
    resp = get_role(module, roles, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_roles(module, roles, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating roles info Spec", **result)

    try:
        resp = roles.list_roles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching roles info",
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
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    roles = get_role_api_instance(module)
    if module.params.get("ext_id"):
        get_role_by_ext_id(module, roles, result)
    else:
        get_roles(module, roles, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
