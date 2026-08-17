#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_runway_planned_capacity_v2
short_description: Create, Update, Delete capacity planning (Runway) scenarios in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete capacity planning
    scenarios (Runway) in Nutanix Prism Central.
  - Runway is the estimated number of days remaining before actual resource
    usage exceeds the cluster effective capacity for CPU, memory, or storage.
  - A capacity planning scenario models workloads and cluster configuration
    changes and exposes the resulting Runway projection.
  - This module uses PC v4 APIs based SDKs (ntnx_aiops_py_client).
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation. The required roles depend on the operation
    being performed.
  - >-
    B(Create a capacity planning scenario) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Update a capacity planning scenario) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete a capacity planning scenario) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be to create a capacity planning scenario.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be to update a capacity planning scenario.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be to delete the capacity planning scenario.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the capacity planning scenario.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the capacity planning scenario.
      - Required for create operation.
      - Minimum length 1, maximum length 256.
    type: str
    required: false
  cluster_ext_id:
    description:
      - UUID of the cluster for which the What-If capacity analysis is being performed.
      - Required for create operation.
    type: str
    required: false
  target_runway_days:
    description:
      - Target number of days a cluster is expected to sustain the workload
        in the capacity planning scenario.
      - Minimum 30, maximum 360.
    type: int
    required: false
  vendors:
    description:
      - Allowed hardware vendors whose models can be requested to sustain the
        workload in the capacity planning scenario.
    type: list
    elements: str
    choices:
      - NUTANIX
      - DELL
      - LENOVO
      - CISCO
      - IBM
      - HPE_DX
      - AWS
      - FUJITSU
      - AZURE
    required: false
  cluster_config:
    description:
      - Cluster specification for the What-If capacity analysis.
      - Required for create operation.
    type: dict
    required: false
    suboptions:
      data_store_config:
        description:
          - Data store configuration used during What-If capacity analysis
            (savings, over-commit and reservation settings).
        type: dict
        required: true
        suboptions:
          replication_factor:
            description:
              - Replication factor of the cluster resources.
            type: str
            choices:
              - RF_2
              - RF_3
            required: true
          compression_saving_percent:
            description:
              - Compression saving percentage of the cluster resources.
            type: float
            required: true
          dedup_saving_percent:
            description:
              - De-dupe saving percentage of the cluster resources.
            type: float
            required: true
          erasure_coding_saving_percent:
            description:
              - Erasure coding saving percentage of the cluster resources.
            type: float
            required: true
          overall_saving_percent:
            description:
              - Overall saving percentage of the cluster resources.
            type: float
            required: true
          cpu_over_commit_ratio:
            description:
              - CPU overcommit ratio.
            type: float
            required: true
          ram_over_commit_ratio:
            description:
              - RAM overcommit ratio.
            type: float
            required: true
          cpu_reservation_percentage:
            description:
              - CPU reservation percentage.
            type: float
            required: true
          ram_reservation_percentage:
            description:
              - RAM reservation percentage.
            type: float
            required: true
          storage_reservation_percentage:
            description:
              - Storage reservation percentage.
            type: float
            required: true
      node_configs:
        description:
          - Metadata about the nodes in a cluster. Nodes can be user added,
            existing on the cluster, or recommended by the recommendation engine.
        type: list
        elements: dict
        required: false
        suboptions:
          model:
            description:
              - Model name of a node.
            type: str
            required: true
          node_count:
            description:
              - Number of nodes of this model.
              - Minimum 1, maximum 500.
            type: int
            required: true
          target_online_time:
            description:
              - Recommended time when a node should be live in the cluster
                (ISO-8601 format, for example C(2022-02-20T00:00:00.458Z)).
            type: str
            required: false
          is_enabled:
            description:
              - Whether the node is taken into account while performing the
                capacity scenario analysis.
            type: bool
            required: false
            default: false
          node_source:
            description:
              - Source of the node added.
            type: str
            choices:
              - EXISTING
              - USER_ADDED
              - RECOMMENDED
            required: true
          node_resource_capacity:
            description:
              - Resource capacity for a node in the cluster.
            type: dict
            required: false
            suboptions:
              cpu_ghz:
                description:
                  - CPU capacity in GHz.
                type: float
                required: true
              ram_gb:
                description:
                  - RAM capacity in GB.
                type: float
                required: true
              hdd_gb:
                description:
                  - HDD capacity in GB.
                type: float
                required: true
              ssd_gb:
                description:
                  - SSD capacity in GB.
                type: float
                required: true
              nvme_gb:
                description:
                  - NVMe capacity in GB.
                type: float
                required: true
  workloads:
    description:
      - List of workloads for which the runway analysis is being done.
      - A workload can be considered an additional resource requirement to
        run a specific use case (for example, a VM workload for a SQL server).
    type: list
    elements: dict
    required: false
    suboptions:
      schedule_date:
        description:
          - Time since the workload is planned to run on the cluster
            (ISO-8601 date, for example C(2026-01-01)).
        type: str
        required: true
      is_enabled:
        description:
          - Whether the added workload in the planned capacity scenario is
            included in the What-If analysis or ignored.
        type: bool
        required: false
        default: false
      projected_resource_requirement:
        description:
          - Projected resource requirement of the workload.
        type: dict
        required: false
        suboptions:
          cpu_ghz:
            description:
              - CPU capacity in GHz.
            type: float
            required: true
          ram_gb:
            description:
              - RAM capacity in GB.
            type: float
            required: true
          hdd_gb:
            description:
              - HDD capacity in GB.
            type: float
            required: true
          ssd_gb:
            description:
              - SSD capacity in GB.
            type: float
            required: true
          nvme_gb:
            description:
              - NVMe capacity in GB.
            type: float
            required: true
      vm_workload:
        description:
          - VM workload description used as the C(workload_properties) of the
            workload. Mutually exclusive with other C(*_workload) sub-options.
        type: dict
        required: false
        suboptions:
          vm_count:
            description:
              - Number of VMs in the VM workload.
              - Minimum 1, maximum 20000.
            type: int
            required: true
          simulation_ext_id:
            description:
              - The UUID of the simulation that is created manually and used
                as the resource profile of each VM.
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
- name: Create capacity planning scenario (Runway) with minimum attributes
  nutanix.ncp.ntnx_runway_planned_capacity_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "runway_scenario_ansible"
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    target_runway_days: 90
    cluster_config:
      data_store_config:
        replication_factor: "RF_2"
        compression_saving_percent: 25.81
        dedup_saving_percent: 35.86
        erasure_coding_saving_percent: 15.17
        overall_saving_percent: 59.64
        cpu_over_commit_ratio: 1.0
        ram_over_commit_ratio: 1.0
        cpu_reservation_percentage: 0.0
        ram_reservation_percentage: 0.0
        storage_reservation_percentage: 0.0
  register: result
  ignore_errors: true

- name: Update capacity planning scenario
  nutanix.ncp.ntnx_runway_planned_capacity_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "runway_scenario_ansible_updated"
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    target_runway_days: 180
    vendors:
      - NUTANIX
    cluster_config:
      data_store_config:
        replication_factor: "RF_3"
        compression_saving_percent: 20.0
        dedup_saving_percent: 30.0
        erasure_coding_saving_percent: 15.0
        overall_saving_percent: 50.0
        cpu_over_commit_ratio: 1.5
        ram_over_commit_ratio: 1.0
        cpu_reservation_percentage: 10.0
        ram_reservation_percentage: 10.0
        storage_reservation_percentage: 5.0
  register: result
  ignore_errors: true

- name: Delete capacity planning scenario
  nutanix.ncp.ntnx_runway_planned_capacity_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a capacity planning scenario.
    - If the operation is create or update and C(wait) is true, it will return the scenario details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_config": {
        "data_store_config": {
          "compression_saving_percent": 25.81,
          "cpu_over_commit_ratio": 1.0,
          "cpu_reservation_percentage": 0.0,
          "dedup_saving_percent": 35.86,
          "erasure_coding_saving_percent": 15.17,
          "overall_saving_percent": 59.64,
          "ram_over_commit_ratio": 1.0,
          "ram_reservation_percentage": 0.0,
          "replication_factor": "RF_2",
          "storage_reservation_percentage": 0.0
        },
        "node_configs": null
      },
      "cluster_ext_id": "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "name": "runway_scenario_ansible",
      "runway": null,
      "target_runway_days": 90,
      "tenant_id": null,
      "updated_time": null,
      "vendors": null,
      "workloads": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the capacity planning scenario.
  returned: always
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

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
  sample: "Api Exception raised while creating capacity planning scenario"
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
from ..module_utils.v4.aiops.helpers import get_scenario  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
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
    import ntnx_aiops_py_client as aiops_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as aiops_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

SCENARIO_REL_TYPE = "aiops:config:scenario"
READ_ONLY_FIELDS = ("updated_time", "runway", "links", "tenant_id")


def get_module_spec():

    resource_capacity_spec = dict(
        cpu_ghz=dict(type="float", required=True),
        ram_gb=dict(type="float", required=True),
        hdd_gb=dict(type="float", required=True),
        ssd_gb=dict(type="float", required=True),
        nvme_gb=dict(type="float", required=True),
    )

    data_store_config_spec = dict(
        replication_factor=dict(
            type="str",
            required=True,
            choices=["RF_2", "RF_3"],
        ),
        compression_saving_percent=dict(type="float", required=True),
        dedup_saving_percent=dict(type="float", required=True),
        erasure_coding_saving_percent=dict(type="float", required=True),
        overall_saving_percent=dict(type="float", required=True),
        cpu_over_commit_ratio=dict(type="float", required=True),
        ram_over_commit_ratio=dict(type="float", required=True),
        cpu_reservation_percentage=dict(type="float", required=True),
        ram_reservation_percentage=dict(type="float", required=True),
        storage_reservation_percentage=dict(type="float", required=True),
    )

    node_config_spec = dict(
        model=dict(type="str", required=True),
        node_count=dict(type="int", required=True),
        target_online_time=dict(type="str", required=False),
        is_enabled=dict(type="bool", required=False, default=False),
        node_source=dict(
            type="str",
            required=True,
            choices=["EXISTING", "USER_ADDED", "RECOMMENDED"],
        ),
        node_resource_capacity=dict(
            type="dict",
            options=resource_capacity_spec,
            required=False,
            obj=aiops_sdk.ResourceCapacity,
        ),
    )

    cluster_config_spec = dict(
        data_store_config=dict(
            type="dict",
            options=data_store_config_spec,
            required=True,
            obj=aiops_sdk.DataStoreConfig,
        ),
        node_configs=dict(
            type="list",
            elements="dict",
            options=node_config_spec,
            required=False,
            obj=aiops_sdk.NodeConfig,
        ),
    )

    vm_workload_spec = dict(
        vm_count=dict(type="int", required=True),
        simulation_ext_id=dict(type="str", required=True),
    )

    workload_spec = dict(
        schedule_date=dict(type="str", required=True),
        is_enabled=dict(type="bool", required=False, default=False),
        projected_resource_requirement=dict(
            type="dict",
            options=resource_capacity_spec,
            required=False,
            obj=aiops_sdk.ResourceCapacity,
        ),
        vm_workload=dict(
            type="dict",
            options=vm_workload_spec,
            required=False,
            obj=aiops_sdk.VmWorkload,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        target_runway_days=dict(type="int"),
        vendors=dict(
            type="list",
            elements="str",
            choices=[
                "NUTANIX",
                "DELL",
                "LENOVO",
                "CISCO",
                "IBM",
                "HPE_DX",
                "AWS",
                "FUJITSU",
                "AZURE",
            ],
        ),
        cluster_config=dict(
            type="dict",
            options=cluster_config_spec,
            obj=aiops_sdk.ClusterConfig,
        ),
        workloads=dict(
            type="list",
            elements="dict",
            options=workload_spec,
            obj=aiops_sdk.Workload,
        ),
    )

    return module_args


def _build_workloads(module):
    """Build the aiops Workload SDK objects from module params.

    The SDK exposes ``workload_properties`` as a OneOf polymorphic field
    (SqlWorkload, VmWorkload, VdiWorkload, etc.). The current spec supports
    ``vm_workload`` for the VM workload type; extend here as more workload
    types are needed.
    """
    workloads_param = module.params.get("workloads") or []
    workloads = []
    for wl in workloads_param:
        vm_wl = wl.get("vm_workload")
        if not vm_wl:
            module.fail_json(
                msg="Each workload MUST provide a supported workload_properties value; "
                "currently only 'vm_workload' is supported.",
            )
        vm_workload_obj = aiops_sdk.VmWorkload(
            vm_count=vm_wl.get("vm_count"),
            simulation_ext_id=vm_wl.get("simulation_ext_id"),
        )
        projected = wl.get("projected_resource_requirement")
        projected_obj = None
        if projected:
            projected_obj = aiops_sdk.ResourceCapacity(
                cpu_ghz=projected.get("cpu_ghz"),
                ram_gb=projected.get("ram_gb"),
                hdd_gb=projected.get("hdd_gb"),
                ssd_gb=projected.get("ssd_gb"),
                nvme_gb=projected.get("nvme_gb"),
            )
        workloads.append(
            aiops_sdk.Workload(
                schedule_date=wl.get("schedule_date"),
                is_enabled=bool(wl.get("is_enabled", False)),
                projected_resource_requirement=projected_obj,
                workload_properties=vm_workload_obj,
            )
        )
    return workloads


def _finalize_spec(module, spec):
    """Attach any manually-built polymorphic sub-specs (e.g. workloads)."""
    if module.params.get("workloads"):
        spec.workloads = _build_workloads(module)


def create_Runway(module, result, api_instance):
    validate_required_params(
        module,
        ["name", "cluster_ext_id", "cluster_config", "vendors", "target_runway_days"],
    )
    sg = SpecGenerator(module)
    default_spec = aiops_sdk.Scenario()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create capacity planning scenario spec",
            **result,
        )

    _finalize_spec(module, spec)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_scenario(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating capacity planning scenario",
        )
    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        ext_id = get_entity_ext_id_from_task(task, rel=SCENARIO_REL_TYPE)
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task)
        if ext_id:
            result["ext_id"] = ext_id
            scenario = get_scenario(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(scenario.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for capacity planning scenario"
                ),
                msg="Failed to get entity ext_id from task for capacity planning scenario",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(deepcopy(old_spec_dict))
    update_spec_dict = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in READ_ONLY_FIELDS:
        old_spec_dict.pop(field, None)
        update_spec_dict.pop(field, None)
    return old_spec_dict == update_spec_dict


def update_Runway(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_scenario(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        module.fail_json(
            msg="Unable to fetch etag for updating capacity planning scenario",
            **result,
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update capacity planning scenario spec",
            **result,
        )

    _finalize_spec(module, update_spec)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_scenario_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating capacity planning scenario",
        )
    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        scenario = get_scenario(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(scenario.to_dict())
    result["changed"] = True


def delete_Runway(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Capacity planning scenario with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_scenario_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting capacity planning scenario",
        )
    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_scenarios_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_Runway(module, result, api_instance)
        else:
            create_Runway(module, result, api_instance)
    else:
        delete_Runway(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
