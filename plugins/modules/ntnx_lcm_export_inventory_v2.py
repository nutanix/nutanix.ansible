#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_export_inventory_v2
short_description: Export the entity inventory information of connected clusters as a downloadable file.
description:
    - Export the entity inventory information of connected clusters as a downloadable file.
    - The exported file contains the full list of LCM entities (software and firmware) discovered across one or more clusters,
      including their versions, locations, and available updates.
    - This module uses PC v4 APIs based SDKs
version_added: "2.7.0"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Export Inventory) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will export the entity inventory information of connected clusters as a downloadable file.
            - If C(state) is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    file_format:
        description:
            - The format of the exported file.
        type: str
        choices:
            - CSV
        default: CSV
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Export entity inventory information of connected clusters as a downloadable file in CSV format
  nutanix.ncp.ntnx_lcm_export_inventory_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    file_format: CSV
  register: inventory_export
"""

RETURN = r"""
response:
    description:
        - Task response returned by the LCM inventory action.
        - If C(wait) is false, this will contain only the initial task reference.
        - If C(wait) is true, this will contain the path to the exported file.
    type: dict
    returned: always
    sample:
    {
        "path": "<path_to_exported_file>"
    }
task_ext_id:
    description: The external identifier of the LCM export inventory task completion.
    type: str
    returned: always
    sample: "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720"
changed:
    description: Whether the module made any changes on the target system.
    type: bool
    returned: always
    sample: true
failed:
    description: Whether the module failed.
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When an error occurs or an informational message is set
    type: str
    sample: "Api Exception raised while performing LCM inventory"
error:
    description: Error details if any error occurred.
    type: str
    returned: When an error occurs
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_inventory_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_ext_id_from_task_completion_details,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_format=dict(type="str", default="CSV", choices=["CSV"], required=True),
    )

    return module_args


def export_lcm_inventory(module, api_instance, result):
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.ExportInventorySpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create LCM export inventory Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.export_inventory(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing LCM inventory",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        downloaded_path = get_ext_id_from_task_completion_details(
            task_resp, name=TASK_CONSTANTS.CompletetionDetailsName.EXPORT_INVENTORY
        )
        if downloaded_path:
            result["path"] = downloaded_path
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get path from task for LCM Upgrade Selection"
                ),
                msg="Failed to get path from task for LCM Upgrade Selection",
            )

    result["changed"] = True


def run_module():

    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }

    api_instance = get_inventory_api_instance(module)

    export_lcm_inventory(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
