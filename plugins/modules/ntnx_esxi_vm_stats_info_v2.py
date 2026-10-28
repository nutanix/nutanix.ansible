#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_esxi_vm_stats_info_v2
short_description: Fetch information about ESXi VM stats
version_added: "2.7.0"
description:
    - Fetch information about ESXi Virtual Machine statistics in Nutanix Prism
      Central.
    - If C(ext_id) is provided, fetch stats for that ESXi VM.
    - If C(ext_id) is not provided, list VM stats across ESXi Virtual Machines,
      optionally filtered, paginated, or ordered.
    - Only ESXi Virtual Machines are supported. A vCenter instance must be
      registered with the cluster; the endpoints fail for AHV VMs.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(List VM stats for all VMs / Get VM stats for a given VM) -
      Required Roles: Prism Admin, Prism Viewer, Project Manager,
      Self-Service Admin (deprecated), Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - Retrieve statistics for the VM with the specified external ID.
            - When set, only stats for this VM are returned.
        type: str
        required: false
    start_time:
        description:
            - The start time of the period for which stats should be reported.
            - The value should be in extended ISO-8601 format.
            - >-
              For example, start time of C(2022-04-23T01:23:45.678+09:00) would
              consider all stats starting at 1:23:45.678 on the 23rd of April
              2022.
        type: str
        required: true
    end_time:
        description:
            - The end time of the period for which stats should be reported.
            - The value should be in extended ISO-8601 format.
            - >-
              For example, end time of C(2022-04-23T13:23:45.678+09:00) would
              consider all stats till 13:23:45.678 on the 23rd of April 2022.
        type: str
        required: true
    sampling_interval:
        description:
            - The sampling interval in seconds at which statistical data should
              be collected.
            - For example, if you want performance statistics every 30 seconds,
              then provide the value as 30.
        type: int
        required: false
    stat_type:
        description:
            - The operator to use while performing down-sampling on stats data.
            - Allowed values are SUM, MIN, MAX, AVG, COUNT and LAST.
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
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all ESXi VM stats within a time window
  nutanix.ncp.ntnx_esxi_vm_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
  register: all_vm_stats

- name: List all ESXi VM stats with fetch_all
  nutanix.ncp.ntnx_esxi_vm_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    fetch_all: true
  register: all_vm_stats_fetch_all

- name: List ESXi VM stats with sampling, aggregation, and paging
  nutanix.ncp.ntnx_esxi_vm_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 60
    stat_type: AVG
    limit: 10
    orderby: stats/hypervisorCpuUsagePpm
  register: paged_vm_stats

- name: List ESXi VM stats filtered by hypervisor CPU usage
  nutanix.ncp.ntnx_esxi_vm_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    filter: "stats/any(a:a/hypervisorCpuUsagePpm gt 0)"
  register: filtered_vm_stats

- name: Get ESXi VM stats using ext_id
  nutanix.ncp.ntnx_esxi_vm_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    sampling_interval: 30
    stat_type: AVG
  register: single_vm_stats

- name: List ESXi VM stats with $select projection
  nutanix.ncp.ntnx_esxi_vm_stats_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    start_time: "2026-07-21T00:00:00.000Z"
    end_time: "2026-07-21T01:00:00.000Z"
    select: "extId,stats/hypervisorCpuUsagePpm"
    limit: 5
  register: projected_vm_stats
"""

RETURN = r"""
response:
    description:
        - The response from the ESXi VM stats info API.
        - It can be a single VmStat if C(ext_id) is provided.
        - List of VmStat entities when C(ext_id) is not provided.
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
    description: Total number of matching VmStat resources returned by the list API.
    type: int
    returned: when C(ext_id) is not provided
    sample: 5
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: false
ext_id:
    description: The external ID of the ESXi Virtual Machine.
    type: str
    returned: when C(ext_id) is provided
    sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"
msg:
    description: This indicates the message if any message occurred
    type: str
    returned: When there is an error
    sample: "Api Exception raised while fetching ESXi VM stats info"
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: when an error occurs
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_esxi_vm_stats  # noqa: E402

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
        resp = list_entities(
            api_instance.list_vm_stats,
            kwargs=kwargs,
        )
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
    result = {
        "changed": False,
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
