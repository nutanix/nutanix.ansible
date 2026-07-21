#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_simulation_v2
short_description: Create, Update, Delete AIOps capacity planning simulations in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete AIOps capacity
    planning simulations in Nutanix Prism Central.
  - A simulation captures a "what-if" resource specification for a VM
    workload (vCPU, RAM, HDD, SSD) that is later referenced from capacity
    planning scenarios to project runway and generate hardware
    recommendations.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the Nutanix IAM roles that grant read/write access
      to the AIOps capacity planning APIs (typically Prism Admin or Super
      Admin) for the user performing the operation.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a simulation.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the simulation.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the simulation.
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
      - Name of the simulation.
      - Required for create operation.
    type: str
    required: false
  simulation_spec:
    description:
      - Simulated resource specification for a VM workload.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      vcpu_count:
        description:
          - Number of vCPUs for each simulated VM.
        type: int
        required: false
      ram_gb:
        description:
          - RAM in GB for each simulated VM.
        type: float
        required: false
      hdd_gb:
        description:
          - HDD storage in GB for each simulated VM.
        type: float
        required: false
      ssd_gb:
        description:
          - SSD storage in GB for each simulated VM.
        type: float
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
- name: Create simulation with all attributes
  nutanix.ncp.ntnx_simulation_v2:
    state: present
    name: "simulation_ansible"
    simulation_spec:
      vcpu_count: 4
      ram_gb: 16.0
      hdd_gb: 200.0
      ssd_gb: 100.0
  register: result
  ignore_errors: true

- name: Update simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "simulation_ansible_updated"
    simulation_spec:
      vcpu_count: 8
      ram_gb: 32.0
      hdd_gb: 400.0
      ssd_gb: 200.0
  register: result
  ignore_errors: true

- name: Delete simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a simulation.
    - For create and update, the response is the full simulation entity (re-fetched from Get after mutation).
    - For delete, the module returns a success message dict since the aiops Delete API returns no body.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "name": "simulation_ansible",
      "simulation_spec": {
        "hdd_gb": 200.0,
        "ram_gb": 16.0,
        "ssd_gb": 100.0,
        "vcpu_count": 4
      },
      "tenant_id": null
    }

ext_id:
  description:
    - The external ID of the simulation.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

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
  sample: "Api Exception raised while creating simulation"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import (  # noqa: E402
    get_etag,
    get_scenarios_api_instance,
)
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


def create_simulation(module, api_instance, result):
    """Create a Simulation. The aiops Create API is synchronous and returns
    the created entity directly (there is no task workflow), so we simply
    read the ``ext_id`` from ``resp.data`` and re-fetch the entity to
    normalize the response shape.
    """
    validate_required_params(module, ["name", "simulation_spec"])

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

    created = getattr(resp, "data", None) if resp else None
    if not created or not getattr(created, "ext_id", None):
        module.fail_json(
            msg="Simulation create returned no entity ext_id",
            response=strip_internal_attributes(resp.to_dict()) if resp else None,
            **result,
        )

    ext_id = created.ext_id
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(created.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    """Return True when the update payload matches the existing simulation."""
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def update_simulation(module, api_instance, result):
    """Update a Simulation. The aiops Update API is synchronous and requires
    an ``If-Match`` etag, and the response body is a list of AppMessage
    entries (not the updated entity), so we re-fetch the simulation after
    the update to return its current state.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_simulation(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating simulation with ext_id: {0}".format(
                ext_id
            ),
            **result,
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update simulation spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    try:
        api_instance.update_simulation_by_id(
            extId=ext_id, body=update_spec, if_match=etag
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating simulation",
        )

    simulation = get_simulation(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(simulation.to_dict())
    result["changed"] = True


def delete_simulation(module, api_instance, result):
    """Delete a Simulation. The aiops Delete API is synchronous and returns
    an empty body on success, so we surface a status message instead.
    """
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
            ("state", "present", ("name", "ext_id"), True),
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
        "skipped": False,
    }
    api_instance = get_scenarios_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_simulation(module, api_instance, result)
        else:
            create_simulation(module, api_instance, result)
    else:
        delete_simulation(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
