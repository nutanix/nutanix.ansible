#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_recalculate_cold_data_v2
short_description: Recalculate cold data eligible for tiering on a Nutanix Files file server
version_added: 2.7.0
description:
    - Trigger a recalculation of the storage size of cold data that is eligible for tiering on a file server.
    - This action schedules a background scan on the file server that recomputes the cold data
      statistics (number and size of files that meet the tiering eligibility criteria).
    - This action only estimates and calculates the cold data size, it does not move or tier any data.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Recalculate cold data.) -
      Required Roles: Files Administrator, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will trigger recalculation of cold data for the file server.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external ID of the file server on which to recalculate cold data.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Recalculate cold data for a file server
  nutanix.ncp.ntnx_files_recalculate_cold_data_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "b2c3d4e5-6789-4abc-9def-0123456789ab"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for recalculating cold data on the file server.
        - Returns the application messages returned by the recalculate cold data action.
    returned: always
    type: dict
    sample:
        [
            {
                "code": "FILES-10000",
                "locale": "en_US",
                "message": "Recalculate cold data request has been accepted.",
                "severity": "INFO"
            }
        ]

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode
    type: str
    sample: "File server with ext_id:b2c3d4e5-6789-4abc-9def-0123456789ab will be triggered to recalculate cold data."

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
    sample: "Api Exception raised while recalculating cold data for file server"

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task, if the operation created a task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the file server
    returned: always
    type: str
    sample: "b2c3d4e5-6789-4abc-9def-0123456789ab"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import get_tier_api_instance  # noqa: E402
from ..module_utils.v4.files.helpers import normalize_response_data  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )

    return module_args


def recalculate_cold_data(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "File server with ext_id:{0} will be triggered to recalculate cold data.".format(
                ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.recalculate_cold_data(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while recalculating cold data for file server",
        )

    data = getattr(resp, "data", None)
    result["response"] = strip_internal_attributes(normalize_response_data(data))

    task_ext_id = getattr(data, "ext_id", None)
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
        if module.params.get("wait"):
            task = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_tier_api_instance(module)
    recalculate_cold_data(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
