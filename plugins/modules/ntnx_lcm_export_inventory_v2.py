#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_export_inventory_v2
short_description: Perform an LCM Inventory scan on a cluster or Prism Central
description:
    - This module performs an LCM inventory operation that identifies and scans
      entities on the cluster (or Prism Central) which can be updated through
      Life Cycle Manager (LCM).
    - The inventory operation is the first step of the LCM workflow.
      Once it completes, the LCM framework has an up-to-date view of the
      installed entities and the versions that can be deployed on the cluster.
    - Optionally the caller can pass a list of credential references from the
      Nutanix Credential Store to allow LCM to authenticate against inventory
      sources that require credentials (e.g. certain vendor management
      endpoints).
    - This is an asynchronous operation. The module returns the task
      C(ext_id) and, when C(wait=true) (the default), polls the task until it
      terminates and returns the final task response.
version_added: 2.5.0
author:
    - Abhinav Bansal (@abhinavbansal29)
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Perform an inventory operation to identify/scan entities on the cluster
      that can be updated through LCM.) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module performs an LCM inventory
              on the target scope.
            - Any other value causes the module to fail because inventory is
              an action, not a resource.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - The external ID of the cluster on which the inventory should be
              performed.
            - When omitted, LCM performs the inventory on Prism Central (PC).
            - When a Prism Element (PE) cluster external ID is passed, the
              inventory is performed on that PE cluster.
            - The cluster external ID can be discovered using the
              M(nutanix.ncp.ntnx_clusters_info_v2) module.
        type: str
        required: false
    credentials:
        description:
            - Optional list of credentials used to authenticate against
              inventory sources during the LCM scan.
            - Each entry references a pre-created credential in the Nutanix
              Credential Store by its external identifier.
        type: list
        elements: dict
        required: false
        suboptions:
            credential_ext_id:
                description:
                    - External identifier (UUID) of a credential stored in the
                      Nutanix Credential Store.
                type: str
                required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Perform LCM inventory on Prism Central
  nutanix.ncp.ntnx_lcm_export_inventory_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: pc_inventory

- name: Perform LCM inventory on a specific Prism Element cluster
  nutanix.ncp.ntnx_lcm_export_inventory_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00062e00-87eb-ef15-0000-00000000b71a"
  register: pe_inventory

- name: Perform LCM inventory with credential references
  nutanix.ncp.ntnx_lcm_export_inventory_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00062e00-87eb-ef15-0000-00000000b71a"
    credentials:
      - credential_ext_id: "d6a5a1b0-2b7f-4d8a-9d38-9f4a0f4bf001"
  register: inventory_with_creds
"""

RETURN = r"""
response:
    description:
        - Task response returned by the LCM inventory action.
        - Before C(wait_for_completion) this contains only the initial task
          reference. After C(wait=True) completes, this contains the full task
          representation (including status, subtasks, timings).
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_ids": null,
            "completed_time": "2026-07-20T14:11:12.512241+00:00",
            "completion_details": null,
            "created_time": "2026-07-20T14:08:58.314367+00:00",
            "entities_affected": null,
            "error_messages": null,
            "ext_id": "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T14:11:12.512240+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 0,
            "number_of_subtasks": 2,
            "operation": "kLcmRootTask",
            "operation_description": "Inventory Root Task",
            "owned_by": null,
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-07-20T14:08:58.314367+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": [
                {
                    "ext_id": "ZXJnb24=:302b65d2-783c-41b0-609d-3a7454e0b491",
                    "href": "https://10.44.76.28:9440/api/prism/v4.0/config/tasks/ZXJnb24=:302b65d2-783c-41b0-609d-3a7454e0b491",
                    "rel": "subtask"
                },
                {
                    "ext_id": "ZXJnb24=:30b19489-70ca-44c0-626c-a634e527ea61",
                    "href": "https://10.44.76.28:9440/api/prism/v4.0/config/tasks/ZXJnb24=:30b19489-70ca-44c0-626c-a634e527ea61",
                    "rel": "subtask"
                }
            ],
            "warnings": null
        }
task_ext_id:
    description: The external identifier of the LCM inventory task submitted to Prism.
    type: str
    returned: always
    sample: "ZXJnb24=:f26d910f-77fe-41a7-7700-fda504474720"
changed:
    description: Whether the module made any changes on the target system.
    type: bool
    returned: always
    sample: true
skipped:
    description: True if the operation was skipped (only set when applicable).
    type: bool
    returned: when applicable
    sample: false
failed:
    description: True when the module failed to perform the LCM inventory.
    type: bool
    returned: always
    sample: false
msg:
    description: Descriptive status or error message emitted by the module.
    returned: When an error occurs or an informational message is set
    type: str
    sample: "Api Exception raised while performing LCM inventory"
error:
    description:
        - Error details returned by the LCM SDK when the API call fails.
        - Contains the SDK exception reason string; empty on success.
    type: str
    returned: When an error occurs
    sample: "Failed generating LCM inventory Spec"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_inventory_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as life_cycle_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as life_cycle_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    credential_reference_spec = dict(
        credential_ext_id=dict(type="str", required=True),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str"),
        credentials=dict(
            type="list",
            elements="dict",
            options=credential_reference_spec,
            obj=life_cycle_management_sdk.CredentialReference,
        ),
    )

    return module_args


def _build_inventory_spec(module, result):
    """
    Build the InventorySpec payload from module parameters.
    Returns (spec, has_body) where has_body indicates whether the caller
    should send a body to the API (only when credentials were provided).
    """
    credentials = module.params.get("credentials")
    if not credentials:
        return None, False

    spec = life_cycle_management_sdk.InventorySpec()
    cred_objs = []
    for entry in credentials:
        cred_ref = life_cycle_management_sdk.CredentialReference()
        cred_ref.credential_ext_id = entry.get("credential_ext_id")
        cred = life_cycle_management_sdk.Credential()
        cred.credential_detail = cred_ref
        cred_objs.append(cred)
    spec.credentials = cred_objs
    return spec, True


def perform_lcm_inventory(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")

    spec, has_body = _build_inventory_spec(module, result)

    # SpecGenerator round-trip validation for the credentials sub-spec when
    # provided; this catches malformed spec-generator objects early.
    if has_body:
        sg = SpecGenerator(module)
        _spec, err = sg.generate_spec(obj=life_cycle_management_sdk.InventorySpec())
        if err:
            result["error"] = err
            module.fail_json(msg="Failed generating LCM inventory Spec", **result)

    if module.check_mode:
        preview = {"cluster_ext_id": cluster_ext_id}
        if has_body:
            preview["body"] = strip_internal_attributes(spec.to_dict())
        result["response"] = preview
        return

    resp = None
    try:
        if has_body:
            resp = api_instance.perform_inventory(
                X_Cluster_Id=cluster_ext_id, body=spec
            )
        else:
            resp = api_instance.perform_inventory(X_Cluster_Id=cluster_ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing LCM inventory",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["ext_id"] = task_ext_id
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "task_ext_id": None,
        "ext_id": None,
    }

    api_instance = get_inventory_api_instance(module)

    perform_lcm_inventory(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
