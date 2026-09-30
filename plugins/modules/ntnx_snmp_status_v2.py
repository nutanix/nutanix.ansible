#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_status_v2
short_description: Update SNMP status (enable/disable) on a Nutanix cluster
version_added: 2.6.0
description:
  - Update SNMP status (enable/disable) on a Nutanix cluster.
  - Set C(is_enabled) to C(true) to enable SNMP, C(false) to disable it.
  - This module uses PC v4 APIs based SDKs.
options:
  state:
        description:
          - state is not supported for this module.
          - It will always be present.
        type: str
        choices: ['present']
        default: present
  cluster_ext_id:
    description:
      - The external ID of the cluster.
    type: str
    required: true
  is_enabled:
    description:
      - SNMP status. Set to C(true) to enable SNMP, C(false) to disable.
    type: bool
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Enable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_status_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "913fa076-d385-4dd8-b549-0e628e645569"
    is_enabled: true
  register: result

- name: Disable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_status_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "913fa076-d385-4dd8-b549-0e628e645569"
    is_enabled: false
  register: result
"""

RETURN = r"""
response:
  description:
    - Task details for SNMP status operations.
  type: dict
  returned: always
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": [
          "0006580f-6db7-1270-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-08-05T05:55:57.373218+00:00",
      "completion_details": null,
      "created_time": "2026-08-05T05:55:56.918689+00:00",
      "entities_affected": [
          {
              "ext_id": "0006580f-6db7-1270-185b-ac1f6b6f97e2",
              "name": null,
              "rel": "clustermgmt:config:cluster"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:69c1057e-2805-4670-62d5-664d43ac4ef6",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-08-05T05:55:57.373218+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 1,
      "number_of_subtasks": 1,
      "operation": "Update Snmp Status",
      "operation_description": "Update Snmp Status",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "project_ext_id": "00000000-0000-0000-0000-000000000000",
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-08-05T05:55:56.930686+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": [
          {
              "ext_id": "ZXJnb24=:91004042-2cc6-4270-79c5-a3babf940d79",
              "href": "https://10.44.76.39:9440/api/prism/v4.4/config/tasks/ZXJnb24=:91004042-2cc6-4270-79c5-a3babf940d79",
              "rel": "subtask"
          }
      ],
      "warnings": null
    }

task_ext_id:
  description: Task External ID
  returned: always
  type: str
  sample: "ZXJnb24=:54a506dc-6d4f-4344-43e4-41205eba32f4"

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while updating SNMP status"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when there is an error
  type: str

cluster_ext_id:
  description: The external ID of the cluster.
  returned: always
  type: str
  sample: "913fa076-d385-4dd8-b549-0e628e645569"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_snmp_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        state=dict(type="str", choices=["present"], default="present"),
        is_enabled=dict(type="bool", required=True),
    )
    return module_args


def update_snmp_status(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.SnmpConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update SNMP status spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.update_snmp_status(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SNMP status",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "task_ext_id": None,
        "cluster_ext_id": None,
    }
    api_instance = get_snmp_api_instance(module)
    update_snmp_status(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
