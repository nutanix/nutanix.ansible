#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_refresh_node_v2
short_description: Refreshes a node's information by fetching the latest data from the hardware provider
version_added: "2.7.0"
description:
  - Refreshes a node's information by fetching the latest data from the hardware provider.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Refresh Node) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will refresh the node.
      - If C(state) is C(absent), the module will fail.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - External ID of the node.
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
- name: Refresh a node
  nutanix.ncp.ntnx_refresh_node_v2:
    nutanix_host: "{{ foundation_central_ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "7eee1613-ac19-4a32-8d6a-c8ed93c5cf06"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for refreshing a node.
    - If C(wait) is true, the response will contain the final task details.
    - If C(wait) is false, the response will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "operation": "RefreshNode",
      "status": "SUCCEEDED"
    }

changed:
  description: This indicates whether the action was executed.
  returned: always
  type: bool
  sample: true

task_ext_id:
  description: The external ID of the task.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the node.
  returned: always
  type: str
  sample: "7eee1613-ac19-4a32-8d6a-c8ed93c5cf06"

msg:
  description: This indicates the status or error message.
  returned: when applicable
  type: str
  sample: "Node with ext_id:7eee1613-ac19-4a32-8d6a-c8ed93c5cf06 will be refreshed."

error:
  description: This field holds the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_nodes_api_instance  # noqa: E402
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


def refresh_node(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Node with ext_id:{0} will be refreshed.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.refresh_node(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while refreshing node with ext_id: {0}".format(
                ext_id
            ),
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
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
        "failed": False,
    }
    api_instance = get_nodes_api_instance(module)
    refresh_node(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
