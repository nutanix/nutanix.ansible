#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_nic_stats_info_v2
short_description: Fetch VM NIC stats info (ESXi hypervisor) from Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about NicStat in Nutanix Prism Central.
  - Only one lookup mode is supported by the v4 ESXi stats API — fetching NIC
    stats for a specific VM NIC by its external ID and the owning VM external ID
    over a given time window.
  - C(ext_id) and C(vm_ext_id) are always required — the SDK does not expose a
    list-all endpoint for NIC stats.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Get NIC stats for a VM on ESXi) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin, Virtual Machine
      Admin, Virtual Machine Operator, Virtual Machine Viewer.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    ext_id:
        description:
            - External ID of the VM NIC.
        type: str
        required: true
    vm_ext_id:
        description:
            - External ID of the VM that owns the NIC.
        type: str
        required: true
    start_time:
        description:
            - Start of the reporting window (ISO-8601 / RFC-3339 timestamp).
            - Sample input C(2024-07-31T12:41:56.955Z).
        type: str
        required: true
    end_time:
        description:
            - End of the reporting window (ISO-8601 / RFC-3339 timestamp).
            - Sample input C(2025-07-31T12:41:56.955Z).
        type: str
        required: true
    sampling_interval:
        description:
            - Sampling interval in seconds at which statistical data should be
              collected.
        type: int
        required: false
    stat_type:
        description:
            - Down-sampling operator applied to the stat time series
              (C(_statType) query parameter).
        type: str
        required: false
        choices:
            - SUM
            - MIN
            - MAX
            - AVG
            - COUNT
            - LAST
    read_timeout:
        description: Read timeout in milliseconds for API calls.
        type: int
        required: false
        default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
 - Nutanix (@nutanix)
 - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch VM NIC stats for a specific NIC
  nutanix.ncp.ntnx_vm_nic_stats_info_v2:
    vm_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec16e
    ext_id: 4a67ce54-dd9c-4c71-9d91-2a19d512dc7d
    start_time: 2024-07-31T12:41:56.955Z
    end_time: 2025-07-31T12:41:56.955Z
  register: nic_stats_info

- name: Fetch VM NIC stats with sampling and average down-sampling
  nutanix.ncp.ntnx_vm_nic_stats_info_v2:
    vm_ext_id: 530567f3-abda-4913-b5d0-0ab6758ec16e
    ext_id: 4a67ce54-dd9c-4c71-9d91-2a19d512dc7d
    start_time: 2024-07-31T12:41:56.955Z
    end_time: 2025-07-31T12:41:56.955Z
    sampling_interval: 30
    stat_type: AVG
  register: nic_stats_info_avg
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC NicStat info v4 API.
    - Always a single NicStat (with a C(stats) time series) — no list mode is
      supported for this entity.
  type: dict
  returned: always
  sample:
    {
        "ext_id": "4a67ce54-dd9c-4c71-9d91-2a19d512dc7d",
        "vm_ext_id": "530567f3-abda-4913-b5d0-0ab6758ec16e",
        "links": null,
        "tenant_id": null,
        "stats": [
            {
                "timestamp": "2024-07-31T12:41:56.955000+00:00",
                "network_dropped_received_packets": 0,
                "network_dropped_transmitted_packets": 0
            }
        ]
    }
ext_id:
    description:
        - External ID of the VM NIC whose stats were retrieved.
    type: str
    returned: always
    sample: "4a67ce54-dd9c-4c71-9d91-2a19d512dc7d"
vm_ext_id:
    description:
        - External ID of the VM that owns the NIC.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec16e"
changed:
    description: Always C(false) — info modules do not mutate any state.
    type: bool
    returned: always
    sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VM NIC stats info"
error:
  description: The error details when an error occurs.
  type: str
  returned: when an error occurs
failed:
  description: Whether the module invocation failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.vmm.api_client import get_esxi_stats_api_instance  # noqa: E402

SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    import ntnx_vmm_py_client as virtual_machine_management_sdk  # noqa: E402, F401
except ImportError:
    # pylint: disable=unused-import
    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401
        mock_sdk as virtual_machine_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        vm_ext_id=dict(type="str", required=True),
        start_time=dict(type="str", required=True),
        end_time=dict(type="str", required=True),
        sampling_interval=dict(type="int", required=False),
        stat_type=dict(
            type="str",
            required=False,
            choices=[
                "SUM",
                "MIN",
                "MAX",
                "AVG",
                "COUNT",
                "LAST",
            ],
        ),
    )
    return module_args


def get_vm_nic_stats(module, api_instance, result):
    """Fetch NIC stats for a given VM NIC using the ESXi Stats API.

    Populates ``result["response"]`` with the sanitized ``data`` block from
    :meth:`ntnx_vmm_py_client.EsxiStatsApi.get_nic_stats_by_id`.
    """
    validate_required_params(module, ["ext_id", "vm_ext_id", "start_time", "end_time"])

    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    sampling_interval = module.params.get("sampling_interval")
    stat_type = module.params.get("stat_type")

    resp = None
    try:
        resp = api_instance.get_nic_stats_by_id(
            vmExtId=vm_ext_id,
            extId=ext_id,
            _startTime=start_time,
            _endTime=end_time,
            _samplingInterval=sampling_interval,
            _statType=stat_type,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VM NIC stats info",
        )

    if getattr(resp, "data", None) is not None:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    else:
        result["response"] = None
        module.fail_json(msg="Failed fetching VM NIC stats info", **result)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "vm_ext_id": None,
        "failed": False,
    }
    api_instance = get_esxi_stats_api_instance(module)
    get_vm_nic_stats(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
