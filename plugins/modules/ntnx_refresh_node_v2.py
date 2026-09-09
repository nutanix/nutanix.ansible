#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_refresh_node_v2
short_description: Refresh a node managed by Foundation Central
version_added: 2.7.0
description:
  - This module triggers a refresh of a node managed by Foundation Central.
  - Refreshing a node re-syncs its hardware, network and lifecycle state from the hardware provider.
  - This is an action module and does not implement Create/Update/Delete state machines.
  - This module uses the Life Cycle Management v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central) (FCVM/Foundation), NOT to Prism Central.
    Set C(nutanix_host) to the Foundation Central endpoint.
  - >-
    B(Refresh a Node) - Requires the appropriate Foundation Central administrator role on the FCVM.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will refresh the node.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID of the node to refresh.
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
    ext_id: "d1a1a1a1-1111-2222-3333-444455556666"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for refreshing a node.
    - Task details when C(wait) is true.
  returned: always
  type: dict
  sample:
    {
      "completed_time": "2026-09-09T06:26:51.524581+00:00",
      "created_time": "2026-09-09T06:26:47.167906+00:00",
      "entities_affected": [
        {"ext_id": "d1a1a1a1-1111-2222-3333-444455556666", "rel": "lifecycle:config:node"}
      ],
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "operation": "RefreshNode",
      "operation_description": "Refresh node",
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
  returned: when applicable
  type: str
  sample: "d1a1a1a1-1111-2222-3333-444455556666"

skipped:
  description: This indicates whether the action was skipped (e.g. in check mode).
  returned: when applicable
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: contextual
  type: str
  sample: "Node with ext_id:d1a1a1a1-1111-2222-3333-444455556666 will be refreshed."

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


def run_action(module, result, api_instance):
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_nodes_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
