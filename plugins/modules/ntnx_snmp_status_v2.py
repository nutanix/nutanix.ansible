#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_status_v2
short_description: Enable or disable SNMP on a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to enable or disable SNMP on a Nutanix cluster via Prism Central.
  - SNMP status is a cluster-scoped flag; this module invokes the
    C(UpdateSnmpStatus) action on the target cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Update SNMP status) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported; the SNMP status flag can only be updated (there is no create/delete).
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - External ID (UUID) of the cluster on which to update the SNMP status.
    type: str
    required: true
  is_enabled:
    description:
      - Desired SNMP status.
      - Set to C(true) to enable SNMP on the cluster, C(false) to disable it.
    type: bool
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
- name: Enable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_status_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    is_enabled: true
  register: result
  ignore_errors: true

- name: Disable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_status_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    is_enabled: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the SNMP status of a cluster.
    - If C(wait) is true, response will contain the completed task details.
    - If C(wait) is false, response will contain the submitted task details.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": [
          "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
      ],
      "completed_time": "2026-07-21T12:47:04.895394+00:00",
      "completion_details": null,
      "created_time": "2026-07-21T12:47:04.267024+00:00",
      "entities_affected": [
          {
              "ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
              "name": null,
              "rel": "clustermgmt:config:cluster"
          }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0807f744-c937-4201-7d61-a3557f2bd218",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-07-21T12:47:04.895393+00:00",
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
      "root_task": null,
      "started_time": "2026-07-21T12:47:04.299115+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": [
          {
              "ext_id": "ZXJnb24=:51ed22db-3671-47f0-7525-e471069df05f",
              "href": "https://pc-endpoint:9440/api/prism/v4.3/config/tasks/ZXJnb24=:51ed22db-3671-47f0-7525-e471069df05f",
              "rel": "subtask"
          }
      ],
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task created for updating the SNMP status.
  returned: always
  type: str
  sample: "ZXJnb24=:0807f744-c937-4201-7d61-a3557f2bd218"

cluster_ext_id:
  description:
    - The external ID of the cluster whose SNMP status was updated.
  returned: always
  type: str
  sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message when applicable.
  returned: When there is an error or in check mode
  type: str
  sample: "Api Exception raised while updating SNMP status of a cluster"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        is_enabled=dict(type="bool", required=True),
    )
    return module_args


def update_snmp_status(module, result, clusters):
    """Invoke the UpdateSnmpStatus action on the cluster identified by ``cluster_ext_id``."""
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.SnmpStatusParam()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating SNMP status update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = clusters.update_snmp_status(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SNMP status of a cluster",
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
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "cluster_ext_id": None,
        "task_ext_id": None,
    }
    clusters = get_clusters_api_instance(module)
    update_snmp_status(module, result, clusters)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
