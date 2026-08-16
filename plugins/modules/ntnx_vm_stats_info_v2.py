#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_stats_info_v2
short_description: Fetch information about ESXi VM stats in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about VmStat (ESXi Virtual
    Machine statistics) in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VmStat.
  - If C(ext_id) is not provided, list VM stats across all ESXi Virtual
    Machines, optionally filtered / paginated / ordered.
  - Only ESXi Virtual Machines are supported by this API. A vCenter instance
    must be registered with the cluster; the corresponding endpoints will
    fail for VMs hosted on AHV.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get ESXi VM Stats by ext_id / List ESXi VM Stats) -
      Required Roles: Prism Admin, Prism Viewer, Project Manager,
      Self-Service Admin (deprecated), Super Admin.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - External ID of an ESXi Virtual Machine. When set, only stats for
        this VM are returned.
    type: str
    required: false
  start_time:
    description:
      - The start time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format, for example
        C(2026-07-21T00:00:00.000Z).
    type: str
    required: true
  end_time:
    description:
      - The end time of the period for which stats should be reported.
      - The value should be in extended ISO-8601 format, for example
        C(2026-07-21T01:00:00.000Z).
    type: str
    required: true
  sampling_interval:
    description:
      - The sampling interval, in seconds, at which statistical data should
        be collected.
    type: int
    required: false
  stat_type:
    description:
      - The down-sampling / aggregation operator to apply while returning
        stats.
    type: str
    required: false
    choices:
      - SUM
      - MIN
      - MAX
      - AVG
      - COUNT
      - LAST
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all ESXi VM stats within a time window
  nutanix.ncp.ntnx_vm_stats_info_v2:
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
  register: all_vm_stats

- name: List first 10 ESXi VM stats sorted with AVG aggregation
  nutanix.ncp.ntnx_vm_stats_info_v2:
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 60
    stat_type: AVG
    limit: 10
    orderby: extId

- name: Get ESXi VM stats using ext_id
  nutanix.ncp.ntnx_vm_stats_info_v2:
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 30
    stat_type: AVG
  register: single_vm_stats

- name: List ESXi VM stats with $select projection
  nutanix.ncp.ntnx_vm_stats_info_v2:
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    select: "extId,stats/hypervisorCpuUsagePpm"
    limit: 5
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VmStat info v4 API.
    - It can be a single VmStat if external ID is provided.
    - List of multiple VmStat if external ID is not provided, with optional
      filter, limit, orderby and select.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "tenant_id": null,
      "stats": [
        {
          "timestamp": "2026-07-21T00:00:00+00:00",
          "hypervisor_cpu_usage_ppm": 12345,
          "hypervisor_memory_usage_ppm": 67890
        }
      ]
    }

total_available_results:
  description: Total number of matching VmStat resources returned by the
    list API.
  type: int
  returned: when C(ext_id) is not provided
  sample: 5

changed:
  description: This indicates whether the task resulted in any changes. Info
    modules never make changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the ESXi Virtual Machine.
  returned: when external ID is provided
  type: str
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

msg:
  description: Status/error message emitted by the module.
  returned: When there is an error.
  type: str
  sample: "Api Exception raised while fetching ESXi VM stats info"

error:
  description: The error message if an error occurred.
  type: str
  returned: When an error occurs

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_esxi_vm_stats  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=False),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int", required=False),
        stat_type=dict(
            type="str",
            required=False,
            choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"],
        ),
    )

    return module_args


def get_vm_stats_by_ext_id(module, api_instance, result):
    """Fetch VM stats for a specific VM via get_vm_stats_by_id."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    resp = get_esxi_vm_stats(
        module,
        api_instance,
        ext_id=ext_id,
        start_time=module.params.get("start_time"),
        end_time=module.params.get("end_time"),
        sampling_interval=module.params.get("sampling_interval"),
        stat_type=module.params.get("stat_type"),
        select=module.params.get("select"),
    )
    if resp is None or getattr(resp, "data", None) is None:
        module.fail_json(msg="Failed fetching ESXi VM stats info", **result)
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def list_vm_stats(module, api_instance, result):
    """Fetch stats across all ESXi VMs via list_vm_stats."""
    sg = SpecGenerator(module)

    info_kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM stats info spec", **result)

    stats_kwargs, err = sg.get_stats_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VM stats info spec", **result)

    kwargs = {}
    kwargs.update(stats_kwargs)
    kwargs.update(info_kwargs)

    try:
        resp = api_instance.list_vm_stats(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM stats info",
        )

    total_available_results = None
    if getattr(resp, "metadata", None) is not None:
        total_available_results = getattr(
            resp.metadata, "total_available_results", None
        )
    if total_available_results is not None:
        result["total_available_results"] = total_available_results

    data = strip_internal_attributes(resp.to_dict()).get("data")
    if not data:
        data = []
    result["response"] = data


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[("ext_id", "filter")],
    )
    remove_param_with_none_value(module.params)
    validate_required_params(module, ["start_time", "end_time"])
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "failed": False,
    }
    api_instance = get_esxi_stats_api_instance(module)
    if module.params.get("ext_id"):
        get_vm_stats_by_ext_id(module, api_instance, result)
    else:
        list_vm_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
