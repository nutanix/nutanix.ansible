#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_simulation_v2
short_description: Create, Update, Delete VM Simulations for AIOps Capacity Planning in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete VM Simulations in Nutanix Prism Central.
  - A Simulation defines a hypothetical VM sizing profile (vCPU/RAM/HDD/SSD) that can be reused
    across What-If capacity planning scenarios.
  - Simulations are used by AIOps capacity planning to model the impact of adding new workloads
    on cluster runway and hardware recommendations.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create a VM Simulation) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Update a VM Simulation) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete a VM Simulation) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create simulation.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update simulation.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete simulation.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the simulation.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - User-visible name of the VM simulation.
      - Required for create operation.
    type: str
    required: false
  simulation_spec:
    description:
      - The hypothetical VM resource specification used by capacity planning simulations.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      vcpu_count:
        description:
          - Number of virtual CPUs for the simulated VM.
        type: int
        required: false
      ram_gb:
        description:
          - Memory (RAM) in GiB for the simulated VM.
        type: float
        required: false
      hdd_gb:
        description:
          - HDD storage size in GiB for the simulated VM.
        type: float
        required: false
      ssd_gb:
        description:
          - SSD storage size in GiB for the simulated VM.
        type: float
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create a VM simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: present
    name: "vdi_medium_workload"
    simulation_spec:
      vcpu_count: 4
      ram_gb: 8.0
      hdd_gb: 100.0
      ssd_gb: 200.0
  register: result

- name: Update a VM simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "vdi_large_workload"
    simulation_spec:
      vcpu_count: 8
      ram_gb: 16.0
      hdd_gb: 200.0
      ssd_gb: 400.0
  register: result

- name: Delete a VM simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a VM simulation.
    - For create and update, this contains the current simulation details fetched after the API call.
    - For delete, this contains a status message indicating the simulation was removed.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "8e2b45a3-15cf-4a2e-b40c-3d1c42908b12",
      "name": "vdi_medium_workload",
      "simulation_spec": {
        "vcpu_count": 4,
        "ram_gb": 8.0,
        "hdd_gb": 100.0,
        "ssd_gb": 200.0
      },
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
    - The AIOps simulation APIs are synchronous, so this field is not populated by the platform.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the simulation.
  returned: always
  type: str
  sample: "8e2b45a3-15cf-4a2e-b40c-3d1c42908b12"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped.
  returned: always
  type: bool
  sample: false

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
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Simulation with name 'vdi_medium_workload' already exists. Skipping creation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_scenarios_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_simulation  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_aiops_py_client as aiops_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as aiops_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    simulation_spec = dict(
        vcpu_count=dict(type="int", required=False),
        ram_gb=dict(type="float", required=False),
        hdd_gb=dict(type="float", required=False),
        ssd_gb=dict(type="float", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        simulation_spec=dict(
            type="dict",
            options=simulation_spec,
            obj=aiops_sdk.SimulatedVmResourceSpec,
        ),
    )
    return module_args


def _find_simulation_by_name(module, api_instance, name):
    """Return an existing Simulation object with the given name, or None."""
    try:
        resp = api_instance.list_simulations(_filter="name eq '{0}'".format(name))
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while looking up simulation by name",
        )
    entities = resp.data if resp and resp.data else []
    for entity in entities:
        if entity.name == name:
            return entity
    return None


def create_simulation(module, result, api_instance):
    validate_required_params(module, ["name", "simulation_spec"])

    existing = _find_simulation_by_name(module, api_instance, module.params.get("name"))
    if existing is not None:
        result["ext_id"] = existing.ext_id
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["skipped"] = True
        result["changed"] = False
        module.exit_json(
            msg="Simulation with name '{0}' already exists. Skipping creation.".format(
                module.params.get("name")
            ),
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = aiops_sdk.Simulation()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create simulation spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_simulation(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating simulation",
        )

    entity = resp.data
    result["response"] = strip_internal_attributes(entity.to_dict())
    result["ext_id"] = getattr(entity, "ext_id", None)
    result["changed"] = True


def _simulation_spec_equal(current_spec, desired_spec):
    """Compare the mutable fields on two Simulation objects."""
    if current_spec.name != desired_spec.name:
        return False
    current_res = current_spec.simulation_spec
    desired_res = desired_spec.simulation_spec
    if current_res is None and desired_res is None:
        return True
    if current_res is None or desired_res is None:
        return False
    for field in ("vcpu_count", "ram_gb", "hdd_gb", "ssd_gb"):
        if getattr(current_res, field, None) != getattr(desired_res, field, None):
            return False
    return True


def update_simulation(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_simulation(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update simulation spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _simulation_spec_equal(current_spec, update_spec):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_spec.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    try:
        api_instance.update_simulation_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating simulation",
        )

    refreshed = get_simulation(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def delete_simulation(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Simulation with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        api_instance.delete_simulation_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting simulation",
        )

    result["response"] = {
        "status": "SUCCEEDED",
        "message": "Simulation with ext_id:{0} deleted successfully.".format(ext_id),
    }
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_aiops_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_scenarios_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_simulation(module, result, api_instance)
        else:
            create_simulation(module, result, api_instance)
    else:
        delete_simulation(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
