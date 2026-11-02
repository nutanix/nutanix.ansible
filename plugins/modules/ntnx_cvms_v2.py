#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cvms_v2
short_description: Update a cluster CVM
version_added: "2.7.0"
description:
    - Update configuration of a specific CVM associated with a cluster.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Update Cluster Cvm) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is C(present), the module will update the CVM.
      - If C(state) is C(absent), the module will fail.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
    type: str
  ext_id:
    description:
      - External identifier for the CVM.
    type: str
  name:
    description:
      - Name of the CVM.
    type: str
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    default: true
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
- name: Update a CVM name
  nutanix.ncp.ntnx_cvms_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "6a24ee94-8c26-4d10-9c60-6c67d4c47dc2"
    name: "NTNX-ansible-example-CVM"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for updating a CVM.
    - CVM details if C(wait) is true.
    - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
        "app_name": null,
        "batch_summary": null,
        "cluster_ext_ids": null,
        "completed_time": "2026-11-02T16:39:47.793064+00:00",
        "completion_details": null,
        "created_time": "2026-11-02T16:39:47.549134+00:00",
        "entities_affected": null,
        "error_messages": [
            {
                "arguments_map": null,
                "code": "TSKS-20801",
                "error_group": "LEGACY_ERROR",
                "locale": "en_US",
                "message": "Operation failed due to legacy error and 'legacyErrorMessage' should be referred to for details",
                "severity": "ERROR"
            }
        ],
        "ext_id": "ZXJnb24=:cabde2bd-a456-5d34-be27-3bdff7a4bfcd",
        "is_background_task": false,
        "is_cancelable": false,
        "last_updated_time": "2026-11-02T16:39:47.793063+00:00",
        "legacy_error_message": "CVM name update is not supported on single and two node clusters",
        "number_of_entities_affected": 0,
        "number_of_subtasks": 1,
        "operation": "updateCvm",
        "operation_description": "Update CVM",
        "owned_by": {
            "ext_id": "00000000-0000-0000-0000-000000000000",
            "name": "admin"
        },
        "parent_task": null,
        "progress_percentage": 100,
        "project_ext_id": "00000000-0000-0000-0000-000000000000",
        "resource_links": null,
        "root_task": null,
        "started_time": "2026-11-02T16:39:47.559171+00:00",
        "status": "FAILED",
        "sub_steps": null,
        "sub_tasks": [
            {
                "ext_id": "ZXJnb24=:792f5ed9-004d-4aaa-63db-2355ffad5c54",
                "href": "https://10.44.76.16:9440/api/prism/v4.4/config/tasks/ZXJnb24=:792f5ed9-004d-4aaa-63db-2355ffad5c54",
                "rel": "subtask"
            }
        ],
        "warnings": null
    }
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
  description:
    - The external ID of the CVM.
  returned: always
  type: str
  sample: "6a24ee94-8c26-4d10-9c60-6c67d4c47dc2"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false
error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "ZXJnb24=:cabde2bd-a456-5d34-be27-3bdff7a4bfcd"
"""

import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cvms_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cvm  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_CVM_READ_ONLY_FIELDS = (
    "cluster_ext_id",
    "node_ext_id",
    "ip_address",
    "num_vcpus",
    "memory_size_bytes",
    "hypervisor_type",
    "backplane_ip_address",
    "ext_id",
    "links",
    "tenant_id",
)


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str"),
        ext_id=dict(type="str"),
        name=dict(type="str"),
    )
    return module_args


def check_cvm_idempotency(current_spec, update_spec):
    return getattr(current_spec, "name", None) == getattr(update_spec, "name", None)


def update_cvm(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "ext_id", "name"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_cvm(module, api_instance, ext_id, cluster_ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating CVM update spec", **result)

    strip_read_only_fields(update_spec, fields=_CVM_READ_ONLY_FIELDS)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_cvm_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json("Unable to fetch etag for updating CVM", **result)
    kwargs = {"if_match": etag}

    try:
        resp = api_instance.update_cvm_by_id(
            clusterExtId=cluster_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating CVM",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_cvm(module, api_instance, ext_id, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False, "ext_id": None}
    api_instance = get_cvms_api_instance(module)
    update_cvm(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
