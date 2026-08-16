#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_recovery_plan_v2
short_description: Create, Update, Delete recovery plans in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete a recovery plan in Nutanix Prism Central.
  - A recovery plan orchestrates disaster recovery of protected VMs and volume groups
    on primary Nutanix clusters to secondary Nutanix clusters registered to the same
    or different Domain manager.
  - This module uses PC v4 APIs based SDKs (namespace C(datapolicies)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - >-
      B(Update a Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - >-
      B(Delete a Recovery Plan) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=datapolicies)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create recovery plan.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update recovery plan.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete recovery plan.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the recovery plan.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - User-visible recovery plan name.
      - Required for create operation.
    type: str
    required: false
  description:
    description:
      - Description of the recovery plan.
    type: str
    required: false
  primary_location:
    description:
      - Primary disaster recovery location for the recovery plan.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      domain_manager_ext_id:
        description:
          - External identifier of the primary Domain manager (Prism Central).
        type: str
        required: true
      clusters:
        description:
          - Prism Element cluster external identifiers whose associated VMs and volume
            groups are protected.
          - Only the primary location can have multiple clusters configured, while the
            other locations can specify only one cluster.
          - Clusters must be specified for replication within the same Prism Central and
            cannot be specified for an MST type location.
          - All clusters are considered if the list is empty.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the cluster.
            type: str
            required: true
  recovery_location:
    description:
      - Recovery (secondary) disaster recovery location for the recovery plan.
    type: dict
    required: false
    suboptions:
      domain_manager_ext_id:
        description:
          - External identifier of the recovery Domain manager (Prism Central).
        type: str
        required: true
      clusters:
        description:
          - Prism Element cluster external identifier for the recovery location.
          - Only one cluster can be specified for the recovery location.
        type: list
        elements: dict
        required: false
        suboptions:
          ext_id:
            description:
              - External identifier of the cluster.
            type: str
            required: true
  witness:
    description:
      - Witness location and failover configuration.
      - Used for cross-cluster / cross-AZ failover arbitration.
    type: dict
    required: false
    suboptions:
      ext_id:
        description:
          - External identifier of the witness service.
        type: str
        required: true
      timeout_secs:
        description:
          - Timeout, in seconds, before the witness declares the primary site as
            unreachable and permits an automated failover to proceed.
        type: int
        required: false
  owner_ext_id:
    description:
      - External identifier of the user who owns the recovery plan.
      - Populated by the system on create; may be updated by an administrator.
    type: str
    required: false
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
- name: Create recovery plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "recovery_plan_ansible"
    description: "Recovery plan created by Ansible"
    primary_location:
      domain_manager_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
      clusters:
        - ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    recovery_location:
      domain_manager_ext_id: "425cd2d4-32e0-4c2d-a026-31d81fa4c805"
      clusters:
        - ext_id: "000649c4-1a2b-1234-5678-000000012345"
  register: result

- name: Update recovery plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
    name: "recovery_plan_ansible_updated"
    description: "Updated recovery plan description"
    primary_location:
      domain_manager_ext_id: "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f"
      clusters:
        - ext_id: "000647b8-ddb3-6bbb-0000-000000028f57"
    recovery_location:
      domain_manager_ext_id: "425cd2d4-32e0-4c2d-a026-31d81fa4c805"
      clusters:
        - ext_id: "000649c4-1a2b-1234-5678-000000012345"
  register: result

- name: Delete recovery plan
  nutanix.ncp.ntnx_recovery_plan_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "e7ae4b0d-726d-410d-87c2-af46f8bea264"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a recovery plan.
    - If the operation is create or update and C(wait) is true, it will return the recovery plan details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "description": "Recovery plan created by Ansible",
      "ext_id": "e7ae4b0d-726d-410d-87c2-af46f8bea264",
      "is_protection_paused_post_failover": null,
      "links": null,
      "name": "recovery_plan_ansible",
      "num_network_mappings": 0,
      "num_stages": 0,
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "primary_location":
        {
          "clusters":
            [
              { "ext_id": "000647b8-ddb3-6bbb-0000-000000028f57", "name": null }
            ],
          "domain_manager_ext_id": "b3a6932b-f64e-49ee-924d-c5a5b8ce2f3f",
          "project_ext_id": null
        },
      "project_ext_id": null,
      "recovery_location":
        {
          "clusters":
            [
              { "ext_id": "000649c4-1a2b-1234-5678-000000012345", "name": null }
            ],
          "domain_manager_ext_id": "425cd2d4-32e0-4c2d-a026-31d81fa4c805",
          "project_ext_id": null
        },
      "tenant_id": null,
      "witness": null,
      "witness_configuration": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the recovery plan.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

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
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating recovery plan"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.data_policies.api_client import (  # noqa: E402
    get_etag,
    get_recovery_plans_api_instance,
)
from ..module_utils.v4.data_policies.helpers import get_recovery_plan  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_datapolicies_py_client as data_policies_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_policies_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Read-only fields returned by the API but not accepted on update.
_READ_ONLY_FIELDS = ("num_stages", "num_network_mappings")

# Rel type reported by ergon for RecoveryPlan entities. Kept module-local
# because the constants file does not (yet) expose data-policies rels.
_RECOVERY_PLAN_REL = "datapolicies:config:recovery-plan"


def get_module_spec():

    entity_reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )

    disaster_recovery_location_spec = dict(
        domain_manager_ext_id=dict(type="str", required=True),
        clusters=dict(
            type="list",
            elements="dict",
            options=entity_reference_spec,
            obj=data_policies_sdk.EntityReference,
        ),
    )

    witness_spec = dict(
        ext_id=dict(type="str", required=True),
        timeout_secs=dict(type="int", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        primary_location=dict(
            type="dict",
            options=disaster_recovery_location_spec,
            obj=data_policies_sdk.DisasterRecoveryLocation,
        ),
        recovery_location=dict(
            type="dict",
            options=disaster_recovery_location_spec,
            obj=data_policies_sdk.DisasterRecoveryLocation,
        ),
        witness=dict(
            type="dict",
            options=witness_spec,
            obj=data_policies_sdk.WitnessConfiguration,
        ),
        owner_ext_id=dict(type="str"),
    )
    return module_args


def create_RecoveryPlan(module, result, api_instance):
    validate_required_params(module, ["name", "primary_location"])

    sg = SpecGenerator(module)
    default_spec = data_policies_sdk.RecoveryPlan()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create recovery plan spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_recovery_plan(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating recovery plan",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(resp, rel=_RECOVERY_PLAN_REL)
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_recovery_plan(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Recovery Plan"
                ),
                msg="Failed to get entity ext_id from task for Recovery Plan",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    # Read-only counters populated by the API — irrelevant for idempotency.
    for field in _READ_ONLY_FIELDS:
        old_spec_dict.pop(field, None)
        update_spec_dict.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_RecoveryPlan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_recovery_plan(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating recovery plan", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update recovery plan spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    strip_read_only_fields(update_spec, fields=_READ_ONLY_FIELDS)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_recovery_plan_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating recovery plan",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_recovery_plan(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_RecoveryPlan(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Recovery plan with ext_id:{0} will be deleted.".format(ext_id)
        return

    # Fetch current etag; some deployments enforce optimistic concurrency on DELETE.
    current = get_recovery_plan(module, api_instance, ext_id)
    etag = get_etag(data=current)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.delete_recovery_plan_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting recovery plan",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=False)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_datapolicies_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_recovery_plans_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_RecoveryPlan(module, result, api_instance)
        else:
            create_RecoveryPlan(module, result, api_instance)
    else:
        delete_RecoveryPlan(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
