#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scenario_v2
short_description: Create, update or delete a Capacity Planning What-if scenario in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete a Capacity Planning ("What-if") Scenario in Nutanix Prism Central.
  - A Scenario models a target Prism Element cluster plus a list of prospective workloads and asks
    the AIOps service to predict runway, recommend node additions and (optionally) generate a report.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create/Update/Delete a Scenario) -
      Required Roles: Prism Admin, Super Admin, Self Service Admin, Internal Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create a scenario.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will update the scenario.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will delete the scenario.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - External ID of the capacity planning scenario.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the capacity planning scenario.
      - Required for create operation.
      - Minimum 1 character, maximum 256 characters.
    type: str
    required: false
  cluster_ext_id:
    description:
      - UUID of the Prism Element cluster for which the What-if analysis is being performed.
      - Required for create operation.
    type: str
    required: false
  target_runway_days:
    description:
      - Number of days a cluster is expected to sustain the workload in the capacity planning scenario.
      - Minimum 30, maximum 360.
    type: int
    required: false
  vendors:
    description:
      - List of allowed hardware vendors whose models can be recommended to sustain the workload.
      - Required in the create operation only.
    type: list
    elements: str
    choices:
      - AWS
      - AZURE
      - CISCO
      - DELL
      - FUJITSU
      - HPE_DX
      - IBM
      - LENOVO
      - NUTANIX
    required: false
  runway:
    description:
      - Existing runway details for the scenario.
      - This is normally computed by the platform. Provide it only when replaying / seeding a scenario.
    type: dict
    required: false
    suboptions:
      minimum_runway_days:
        description:
          - Number of days the cluster will be able to sustain the existing and added workloads.
        type: int
      cpu_runway_days:
        description:
          - Number of days the cluster can sustain CPU demand.
        type: int
      memory_runway_days:
        description:
          - Number of days the cluster can sustain memory demand.
        type: int
      storage_runway_days:
        description:
          - Number of days the cluster can sustain storage demand.
        type: int
      runway_start_time:
        description:
          - Timestamp (ISO-8601) marking the start of the runway calculation.
        type: str
  cluster_config:
    description:
      - Cluster specification override used when the scenario is being modeled on a hypothetical
        cluster topology (e.g. adding new nodes).
    type: dict
    required: false
    suboptions:
      data_store_config:
        description:
          - Data store configuration for the cluster (replication factor, savings, over-commit ratios).
        type: dict
        required: true
        suboptions:
          replication_factor:
            description:
              - Cluster replication factor.
            type: str
            choices:
              - RF_2
              - RF_3
            required: true
          compression_saving_percent:
            description:
              - Estimated compression saving percentage.
            type: float
          dedup_saving_percent:
            description:
              - Estimated deduplication saving percentage.
            type: float
          erasure_coding_saving_percent:
            description:
              - Estimated erasure-coding saving percentage.
            type: float
          overall_saving_percent:
            description:
              - Overall storage saving percentage.
            type: float
          cpu_over_commit_ratio:
            description:
              - CPU over-commit ratio.
            type: float
          ram_over_commit_ratio:
            description:
              - RAM over-commit ratio.
            type: float
          cpu_reservation_percentage:
            description:
              - CPU reservation percentage.
            type: float
          ram_reservation_percentage:
            description:
              - RAM reservation percentage.
            type: float
          storage_reservation_percentage:
            description:
              - Storage reservation percentage.
            type: float
      node_configs:
        description:
          - List describing the nodes (existing, user-added or recommended) that make up the modelled cluster.
        type: list
        elements: dict
        suboptions:
          model:
            description:
              - Model name of the node.
            type: str
            required: true
          node_count:
            description:
              - Number of nodes of this model. Minimum 1, maximum 500.
            type: int
            required: true
          target_online_time:
            description:
              - Recommended time (ISO-8601 timestamp) when the node should be live in the cluster.
            type: str
          is_enabled:
            description:
              - Flag indicating if this node group is included in the scenario analysis.
            type: bool
            default: false
          node_source:
            description:
              - Source of the node in the scenario.
            type: str
            choices:
              - EXISTING
              - RECOMMENDED
              - USER_ADDED
            required: true
          node_resource_capacity:
            description:
              - Optional explicit resource capacity for the node (CPU GHz, RAM/HDD/SSD/NVMe GB).
            type: dict
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
      - List of workloads to add to the What-if analysis.
      - Each entry must supply exactly one workload variant under C(workload_properties).
    type: list
    elements: dict
    required: false
    suboptions:
      schedule_date:
        description:
          - Date when the workload is scheduled to run on the cluster in C(yyyy-MM-dd) format
            (e.g. C(2026-02-01)).
        type: str
        required: true
      is_enabled:
        description:
          - Flag indicating whether the workload participates in this What-if analysis.
        type: bool
        default: false
      projected_resource_requirement:
        description:
          - Optional pre-computed resource requirement for this workload.
        type: dict
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
      workload_properties:
        description:
          - Discriminated union describing the workload variant.
          - Provide exactly one of C(vm), C(vm_category), C(sql), C(vdi), C(splunk),
            C(citrix_xen), C(microsoft_xen) or C(capacity_update).
        type: dict
        required: true
        suboptions:
          vm:
            description:
              - Plain VM workload backed by a Simulation template.
            type: dict
            suboptions:
              vm_count:
                description:
                  - Number of VMs added by this workload.
                type: int
                required: true
              simulation_ext_id:
                description:
                  - External ID of the Simulation resource that describes each VM.
                type: str
                required: true
          vm_category:
            description:
              - Workload based on scaling the VMs belonging to a category.
            type: dict
            suboptions:
              category_ext_id:
                description:
                  - External ID of the category to scale.
                type: str
                required: true
              current_vm_count:
                description:
                  - Current number of VMs in the category.
                type: int
                required: true
              target_vm_count:
                description:
                  - Target number of VMs in the category after the change.
                type: int
                required: true
          sql:
            description:
              - SQL workload description.
            type: dict
            suboptions:
              db_count:
                description:
                  - Number of SQL databases to model.
                type: int
                required: true
              profile_type:
                description:
                  - Sizing profile.
                type: str
                choices:
                  - SMALL
                  - MEDIUM
                  - LARGE
                required: true
              transaction_type:
                description:
                  - Transaction workload type.
                type: str
                choices:
                  - OLTP
                  - OLAP
                required: true
              is_business_critical:
                description:
                  - Flag marking the workload as business critical.
                type: bool
                default: false
          vdi:
            description:
              - VDI workload description.
            type: dict
            suboptions:
              vendor:
                description:
                  - VDI vendor.
                type: str
                choices:
                  - VIEW
                  - XEN_DESKTOP
                required: true
              user_type:
                description:
                  - Type of end user.
                type: str
                choices:
                  - TASK_WORKER
                  - KNOWLEDGE_WORKER
                  - POWER_USER
                  - DEVELOPER
                required: true
              provision_type:
                description:
                  - Provisioning type.
                type: str
                choices:
                  - FULL_CLONES
                  - LINKED_CLONES
                  - MACHINE_CREATION_SERVICES
                  - PROVISIONING_SERVICES
                  - V2V_P2V
                required: true
              user_count:
                description:
                  - Number of VDI end users to model.
                type: int
                required: true
          splunk:
            description:
              - Splunk workload description.
            type: dict
            suboptions:
              daily_average_indexing_rate_gb:
                description:
                  - Daily average indexing rate in GB.
                type: int
                required: true
              hot_retention_days:
                description:
                  - Hot data retention in days.
                type: int
                required: true
              cold_retention_days:
                description:
                  - Cold data retention in days.
                type: int
                required: true
              user_count:
                description:
                  - Number of Splunk users.
                type: int
                required: true
          citrix_xen:
            description:
              - Citrix Xen workload description.
            type: dict
            suboptions:
              vendor:
                description:
                  - Citrix Xen vendor variant.
                type: str
                choices:
                  - XEN_APP
                required: true
              provision_type:
                description:
                  - Provisioning type used for the Xen deployment.
                type: str
                choices:
                  - MCS
                  - PVS
              operating_system:
                description:
                  - Guest operating system.
                type: str
                choices:
                  - WINDOWS_2008R2
                  - WINDOWS_2012R2
              system_data_gb:
                description:
                  - Space consumed by each Xen Server image (minimum 20, maximum 62000).
                type: int
              user_count:
                description:
                  - Number of Xen users (minimum 1, maximum 100000).
                type: int
              mcs_diff_size_gb:
                description:
                  - Size in GB for the MCS diff disk per VM (minimum 10, maximum 50).
                type: int
              user_profile_data_mb:
                description:
                  - Size per user profile data in MB (minimum 20, maximum 100).
                type: int
              pvs_write_cache_size_gb:
                description:
                  - Size of PVS write cache per VM in GB (minimum 10, maximum 50).
                type: int
          microsoft_xen:
            description:
              - Microsoft RDSH / Xen workload description.
            type: dict
            suboptions:
              vendor:
                description:
                  - Microsoft Xen vendor.
                type: str
                choices:
                  - MICROSOFT_RDSH
                required: true
              provision_type:
                description:
                  - Provisioning type.
                type: str
                choices:
                  - VM_CLONE
              operating_system:
                description:
                  - Guest operating system.
                type: str
                choices:
                  - WINDOWS_2008R2
                  - WINDOWS_2012R2
              system_data_gb:
                description:
                  - Space consumed by each Xen Server image.
                type: int
              user_count:
                description:
                  - Number of users.
                type: int
              mcs_diff_size_gb:
                description:
                  - Size in GB for the MCS diff disk per VM.
                type: int
              user_profile_data_mb:
                description:
                  - Size per user profile data in MB.
                type: int
              pvs_write_cache_size_gb:
                description:
                  - Size of PVS write cache per VM in GB.
                type: int
          capacity_update:
            description:
              - Capacity update workload representing a percentage change in demand.
            type: dict
            suboptions:
              percentage_change:
                description:
                  - Percentage change in demand.
                type: int
                required: true
              change_type:
                description:
                  - Direction of the demand change.
                type: str
                choices:
                  - INCREASE
                  - DECREASE
                required: true
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
- name: Create a capacity planning scenario
  nutanix.ncp.ntnx_scenario_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_scenario_demo"
    cluster_ext_id: "0005f6f4-1c1c-6b3f-0000-0000000abcde"
    target_runway_days: 90
    vendors:
      - NUTANIX
      - DELL
    workloads:
      - schedule_date: "2026-02-01"
        is_enabled: true
        workload_properties:
          capacity_update:
            percentage_change: 20
            change_type: INCREASE
  register: created_scenario
  ignore_errors: true

- name: Update an existing scenario
  nutanix.ncp.ntnx_scenario_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f"
    name: "ansible_scenario_demo_updated"
    cluster_ext_id: "0005f6f4-1c1c-6b3f-0000-0000000abcde"
    target_runway_days: 180
    vendors:
      - NUTANIX
    workloads:
      - schedule_date: "2026-03-01"
        is_enabled: true
        workload_properties:
          sql:
            db_count: 4
            profile_type: MEDIUM
            transaction_type: OLTP
            is_business_critical: true
  register: updated_scenario
  ignore_errors: true

- name: Delete the scenario
  nutanix.ncp.ntnx_scenario_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f"
  register: deleted_scenario
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
      "cluster_config": null,
      "cluster_ext_id": "0005f6f4-1c1c-6b3f-0000-0000000abcde",
      "ext_id": "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f",
      "links": null,
      "name": "ansible_scenario_demo",
      "runway": null,
      "target_runway_days": 90,
      "tenant_id": null,
      "updated_time": "2026-02-01T12:00:00Z",
      "vendors": ["NUTANIX", "DELL"],
      "workloads": [
        {
          "is_enabled": true,
          "projected_resource_requirement": null,
          "schedule_date": "2026-02-01",
          "workload_properties": {
            "change_type": "INCREASE",
            "percentage_change": 20
          }
        }
      ]
    }

task_ext_id:
  description:
    - The external ID of the task associated with the operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the scenario.
  returned: always
  type: str
  sample: "b1e5a5b7-1234-4d3e-b0dc-1a2b3c4d5e6f"

changed:
  description: Indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: Indicates whether the operation was skipped (e.g. idempotency).
  returned: when applicable
  type: bool
  sample: false

error:
  description: Error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: Contextual status/error message.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Scenario with name 'ansible_scenario_demo' already exists. Skipping creation."
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
from ..module_utils.v4.aiops.helpers import (  # noqa: E402
    get_scenario,
    get_scenario_by_name,
)
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
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
    resource_capacity_spec = dict(
        cpu_ghz=dict(type="float", required=True),
        ram_gb=dict(type="float", required=True),
        hdd_gb=dict(type="float", required=True),
        ssd_gb=dict(type="float", required=True),
        nvme_gb=dict(type="float", required=True),
    )

    vm_workload_spec = dict(
        vm_count=dict(type="int", required=True),
        simulation_ext_id=dict(type="str", required=True),
    )

    vm_category_workload_spec = dict(
        category_ext_id=dict(type="str", required=True),
        current_vm_count=dict(type="int", required=True),
        target_vm_count=dict(type="int", required=True),
    )

    sql_workload_spec = dict(
        db_count=dict(type="int", required=True),
        profile_type=dict(
            type="str",
            choices=["SMALL", "MEDIUM", "LARGE"],
            required=True,
            obj=aiops_sdk.SqlProfileType,
        ),
        transaction_type=dict(
            type="str",
            choices=["OLTP", "OLAP"],
            required=True,
            obj=aiops_sdk.SqlTransactionType,
        ),
        is_business_critical=dict(type="bool", default=False),
    )

    vdi_workload_spec = dict(
        vendor=dict(
            type="str",
            choices=["VIEW", "XEN_DESKTOP"],
            required=True,
            obj=aiops_sdk.VdiVendor,
        ),
        user_type=dict(
            type="str",
            choices=["TASK_WORKER", "KNOWLEDGE_WORKER", "POWER_USER", "DEVELOPER"],
            required=True,
            obj=aiops_sdk.VdiUserType,
        ),
        provision_type=dict(
            type="str",
            choices=[
                "FULL_CLONES",
                "LINKED_CLONES",
                "MACHINE_CREATION_SERVICES",
                "PROVISIONING_SERVICES",
                "V2V_P2V",
            ],
            required=True,
            obj=aiops_sdk.VdiProvisionType,
        ),
        user_count=dict(type="int", required=True),
    )

    splunk_workload_spec = dict(
        daily_average_indexing_rate_gb=dict(type="int", required=True),
        hot_retention_days=dict(type="int", required=True),
        cold_retention_days=dict(type="int", required=True),
        user_count=dict(type="int", required=True),
    )

    citrix_xen_workload_spec = dict(
        vendor=dict(
            type="str",
            choices=["XEN_APP"],
            required=True,
            obj=aiops_sdk.CitrixXenWorkloadVendor,
        ),
        provision_type=dict(
            type="str",
            choices=["MCS", "PVS"],
            obj=aiops_sdk.CitrixXenProvisionType,
        ),
        operating_system=dict(
            type="str",
            choices=["WINDOWS_2008R2", "WINDOWS_2012R2"],
            obj=aiops_sdk.XenOperatingSystem,
        ),
        system_data_gb=dict(type="int"),
        user_count=dict(type="int"),
        mcs_diff_size_gb=dict(type="int"),
        user_profile_data_mb=dict(type="int"),
        pvs_write_cache_size_gb=dict(type="int"),
    )

    microsoft_xen_workload_spec = dict(
        vendor=dict(
            type="str",
            choices=["MICROSOFT_RDSH"],
            required=True,
            obj=aiops_sdk.MicrosoftXenWorkloadVendor,
        ),
        provision_type=dict(
            type="str",
            choices=["VM_CLONE"],
            obj=aiops_sdk.MicrosoftXenProvisionType,
        ),
        operating_system=dict(
            type="str",
            choices=["WINDOWS_2008R2", "WINDOWS_2012R2"],
            obj=aiops_sdk.XenOperatingSystem,
        ),
        system_data_gb=dict(type="int"),
        user_count=dict(type="int"),
        mcs_diff_size_gb=dict(type="int"),
        user_profile_data_mb=dict(type="int"),
        pvs_write_cache_size_gb=dict(type="int"),
    )

    capacity_update_workload_spec = dict(
        percentage_change=dict(type="int", required=True),
        change_type=dict(
            type="str",
            choices=["INCREASE", "DECREASE"],
            required=True,
            obj=aiops_sdk.CapacityUpdateType,
        ),
    )

    workload_properties_spec = dict(
        vm=dict(type="dict", options=vm_workload_spec, obj=aiops_sdk.VmWorkload),
        vm_category=dict(
            type="dict",
            options=vm_category_workload_spec,
            obj=aiops_sdk.VmCategoryWorkload,
        ),
        sql=dict(type="dict", options=sql_workload_spec, obj=aiops_sdk.SqlWorkload),
        vdi=dict(type="dict", options=vdi_workload_spec, obj=aiops_sdk.VdiWorkload),
        splunk=dict(
            type="dict", options=splunk_workload_spec, obj=aiops_sdk.SplunkWorkload
        ),
        citrix_xen=dict(
            type="dict",
            options=citrix_xen_workload_spec,
            obj=aiops_sdk.CitrixXenWorkload,
        ),
        microsoft_xen=dict(
            type="dict",
            options=microsoft_xen_workload_spec,
            obj=aiops_sdk.MicrosoftXenWorkload,
        ),
        capacity_update=dict(
            type="dict",
            options=capacity_update_workload_spec,
            obj=aiops_sdk.CapacityUpdateConfig,
        ),
    )

    workload_spec = dict(
        schedule_date=dict(type="str", required=True),
        is_enabled=dict(type="bool", default=False),
        projected_resource_requirement=dict(
            type="dict",
            options=resource_capacity_spec,
            obj=aiops_sdk.ResourceCapacity,
        ),
        workload_properties=dict(
            type="dict",
            options=workload_properties_spec,
            required=True,
            mutually_exclusive=[
                (
                    "vm",
                    "vm_category",
                    "sql",
                    "vdi",
                    "splunk",
                    "citrix_xen",
                    "microsoft_xen",
                    "capacity_update",
                )
            ],
            required_one_of=[
                (
                    "vm",
                    "vm_category",
                    "sql",
                    "vdi",
                    "splunk",
                    "citrix_xen",
                    "microsoft_xen",
                    "capacity_update",
                )
            ],
            obj={
                "vm": aiops_sdk.VmWorkload,
                "vm_category": aiops_sdk.VmCategoryWorkload,
                "sql": aiops_sdk.SqlWorkload,
                "vdi": aiops_sdk.VdiWorkload,
                "splunk": aiops_sdk.SplunkWorkload,
                "citrix_xen": aiops_sdk.CitrixXenWorkload,
                "microsoft_xen": aiops_sdk.MicrosoftXenWorkload,
                "capacity_update": aiops_sdk.CapacityUpdateConfig,
            },
        ),
    )

    node_config_spec = dict(
        model=dict(type="str", required=True),
        node_count=dict(type="int", required=True),
        target_online_time=dict(type="str"),
        is_enabled=dict(type="bool", default=False),
        node_source=dict(
            type="str",
            choices=["EXISTING", "RECOMMENDED", "USER_ADDED"],
            required=True,
            obj=aiops_sdk.NodeSource,
        ),
        node_resource_capacity=dict(
            type="dict",
            options=resource_capacity_spec,
            obj=aiops_sdk.ResourceCapacity,
        ),
    )

    data_store_config_spec = dict(
        replication_factor=dict(
            type="str",
            choices=["RF_2", "RF_3"],
            required=True,
            obj=aiops_sdk.ReplicationFactor,
        ),
        compression_saving_percent=dict(type="float"),
        dedup_saving_percent=dict(type="float"),
        erasure_coding_saving_percent=dict(type="float"),
        overall_saving_percent=dict(type="float"),
        cpu_over_commit_ratio=dict(type="float"),
        ram_over_commit_ratio=dict(type="float"),
        cpu_reservation_percentage=dict(type="float"),
        ram_reservation_percentage=dict(type="float"),
        storage_reservation_percentage=dict(type="float"),
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
            obj=aiops_sdk.NodeConfig,
        ),
    )

    runway_spec = dict(
        minimum_runway_days=dict(type="int"),
        cpu_runway_days=dict(type="int"),
        memory_runway_days=dict(type="int"),
        storage_runway_days=dict(type="int"),
        runway_start_time=dict(type="str"),
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
                "AWS",
                "AZURE",
                "CISCO",
                "DELL",
                "FUJITSU",
                "HPE_DX",
                "IBM",
                "LENOVO",
                "NUTANIX",
            ],
        ),
        runway=dict(
            type="dict",
            options=runway_spec,
            obj=aiops_sdk.ConfigRunway,
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


def create_scenario(module, api_instance, result):
    validate_required_params(module, ["name", "cluster_ext_id", "vendors"])

    name = module.params.get("name")
    existing = get_scenario_by_name(module, api_instance, name)
    if existing is not None:
        result["ext_id"] = existing.ext_id
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["skipped"] = True
        result["changed"] = False
        result["msg"] = (
            "Scenario with name '{0}' already exists. Skipping creation.".format(name)
        )
        module.exit_json(**result)

    sg = SpecGenerator(module)
    default_spec = aiops_sdk.Scenario()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create scenario spec", **result)

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
            msg="Api Exception raised while creating scenario",
        )
    if resp is None or resp.data is None:
        module.fail_json(msg="Create scenario returned an empty response", **result)

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.SCENARIO
        )
        if not ext_id:
            ext_id = get_entity_ext_id_from_task(task_status)
        if ext_id:
            result["ext_id"] = ext_id
            fetched = get_scenario(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(fetched.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Scenario"
                ),
                msg="Failed to get entity ext_id from task for Scenario",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    for key in ("updated_time", "runway"):
        old.pop(key, None)
        new.pop(key, None)
    return old == new


def update_scenario(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_scenario(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update scenario spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["msg"] = "Nothing to change."
        module.exit_json(**result)

    resp = None
    try:
        resp = api_instance.update_scenario_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating scenario",
        )

    if resp is not None and resp.data is not None:
        task_ext_id = resp.data.ext_id
        result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if task_ext_id and module.params.get("wait"):
            wait_for_completion(module, task_ext_id)
            fetched = get_scenario(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(fetched.to_dict())
    result["changed"] = True


def delete_scenario(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Scenario with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.delete_scenario_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting scenario",
        )

    if resp is not None and getattr(resp, "data", None) is not None:
        task_ext_id = resp.data.ext_id
        result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if task_ext_id and module.params.get("wait"):
            task_status = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task_status.to_dict())
    result["msg"] = "Scenario with ext_id:{0} has been deleted.".format(ext_id)
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
    }
    api_instance = get_scenarios_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_scenario(module, api_instance, result)
        else:
            create_scenario(module, api_instance, result)
    else:
        delete_scenario(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
