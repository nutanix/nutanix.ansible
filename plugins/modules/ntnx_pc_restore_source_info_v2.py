#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_restore_source_info_v2
short_description: Get PC restore source info
version_added: 2.1.0
description:
    - Fetch specific restore source info using external ID
    - Please provide Prism Element IP address here in C(nutanix_host)
options:
    ext_id:
        description: External ID to fetch specific restore source info
        type: str
        required: True
    nutanix_host:
        description: The Nutanix Prism Element IP address
        type: str
        required: True
    nutanix_username:
        description: The username to authenticate with the Nutanix Prism Element
        type: str
        required: True
    nutanix_password:
        description: The password to authenticate with the Nutanix Prism Element
        type: str
        required: True
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get restore source cluster
  nutanix.ncp.ntnx_pc_restore_source_info_v2:
    nutanix_host: <pe_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for fetching restore source info
    type: dict
    returned: always
    sample:
        {
            "ext_id": "11bc64e2-8547-9632-6584-8b39fc2015f3",
            "links": null,
            "location": {
                "config": {
                    "ext_id": "00062cd6-1232-1122-5433-ac1f6b6f97e2",
                    "name": null
                }
            },
        }
ext_id:
    description:
        - External ID of the restore source
    type: str
    returned: always
    sample: "11bc64e2-8547-9632-6584-8b39fc2015f3"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str
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
from ..module_utils.v4.prism.helpers import get_restore_source  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(ext_id=dict(type="str", required=True))
    return module_args


def get_restore_source_with_ext_id(module, prism, result):
    ext_id = module.params.get("ext_id")
    resp = get_restore_source(module, prism, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    prism = get_domain_manager_backup_api_instance(module)
    get_restore_source_with_ext_id(module, prism, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
