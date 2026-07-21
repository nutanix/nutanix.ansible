#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_simulation_v2
short_description: Create, Update, Delete a Simulation in Nutanix Prism Central (aiops)
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete a Simulation in Nutanix Prism Central.
  - A Simulation captures a projected VM workload (vCPU, RAM, storage) that can be
    referenced from a capacity planning Scenario.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Simulation) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Update a Simulation) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete a Simulation) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create Simulation.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update Simulation.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete Simulation.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Simulation.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the resource used in a scenario.
      - Required for create operation.
      - Minimum 1 character, maximum 256 characters.
    type: str
    required: false
  simulation_spec:
    description:
      - Simulated resource specification for the VM workload used in the Simulation.
    type: dict
    required: false
    suboptions:
      vcpu_count:
        description:
          - Number of vCPUs for the simulated VM workload.
        type: int
        required: false
      ram_gb:
        description:
          - Amount of RAM in GB for the simulated VM workload.
        type: float
        required: false
      hdd_gb:
        description:
          - Amount of HDD storage in GB for the simulated VM workload.
        type: float
        required: false
      ssd_gb:
        description:
          - Amount of SSD storage in GB for the simulated VM workload.
        type: float
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: present
    name: "simulation_ansible"
    simulation_spec:
      vcpu_count: 4
      ram_gb: 8.0
      hdd_gb: 100.0
      ssd_gb: 50.0
  register: result
  ignore_errors: true

- name: Update simulation
  nutanix.ncp.ntnx_simulation_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "simulation_ansible_updated"
    simulation_spec:
      vcpu_count: 8
      ram_gb: 16.0
      hdd_gb: 200.0
      ssd_gb: 100.0
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
    - Response for creating, updating, or deleting a Simulation.
    - For create and update operations it returns the Simulation details.
    - For delete operations it returns a status dict indicating SUCCEEDED.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "3236a842-f0c6-42a6-a6da-4cff299d219b",
      "links": null,
      "name": "simulation_ansible_example_updated",
      "simulation_spec": {
          "hdd_gb": 200.0,
          "ram_gb": 16.0,
          "ssd_gb": 100.0,
          "vcpu_count": 8
      },
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
    - The aiops Simulation APIs are synchronous, so this is C(None) for a successful call.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the Simulation.
  returned: always
  type: str
  sample: "3236a842-f0c6-42a6-a6da-4cff299d219b"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. idempotency)
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
  description:
    - Status/error message.
    - "Sample: Simulation with name 'simulation_ansible' already exists. Skipping creation."
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
    """
    Return the first Simulation whose name matches ``name`` (used for idempotency
    on create). Returns None when nothing matches or the API rejects the filter.
    """
    try:
        resp = api_instance.list_simulations(
            _filter="name eq '{0}'".format(name), _limit=1
        )
    except Exception:
        return None
    data = getattr(resp, "data", None)
    if not data:
        return None
    if isinstance(data, list):
        return data[0]
    return None


def create_simulation(module, api_instance, result):
    validate_required_params(module, ["name", "simulation_spec"])
    name = module.params.get("name")

    existing = _find_simulation_by_name(module, api_instance, name)
    if existing is not None:
        result["ext_id"] = getattr(existing, "ext_id", None)
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["skipped"] = True
        result["changed"] = False
        result["msg"] = (
            "Simulation with name '{0}' already exists. Skipping creation.".format(name)
        )
        return

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

    data = getattr(resp, "data", None)
    if data is not None and hasattr(data, "ext_id"):
        result["ext_id"] = data.ext_id
        result["response"] = strip_internal_attributes(data.to_dict())
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    return old_spec_dict == update_spec_dict


def _reset_read_only_attributes(spec):
    """
    Reset server-populated read-only attributes on the Simulation spec before
    sending it back as an update body. The SDK model does not permit deletion of
    these attributes (no `deleter` on the properties), so we clear them to None.
    """
    for field in ("links", "tenant_id"):
        try:
            setattr(spec, field, None)
        except AttributeError:
            pass


def update_simulation(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_simulation(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

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
        result["changed"] = False
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    _reset_read_only_attributes(update_spec)

    try:
        resp = api_instance.update_simulation_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating simulation",
        )

    data = getattr(resp, "data", None)
    if data is not None and hasattr(data, "ext_id"):
        result["ext_id"] = data.ext_id
        result["response"] = strip_internal_attributes(data.to_dict())
    else:
        try:
            refreshed = get_simulation(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(refreshed.to_dict())
        except Exception:
            result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_simulation(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Simulation with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = api_instance.delete_simulation_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting simulation",
        )

    if resp is not None and hasattr(resp, "to_dict"):
        result["response"] = strip_internal_attributes(resp.to_dict())
    else:
        result["response"] = {"status": "SUCCEEDED"}
    result["msg"] = "Simulation with ext_id:{0} deleted successfully.".format(ext_id)
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
        "task_ext_id": None,
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
