#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_volume_groups_info_v2
short_description: Fetch information about Nutanix PC Volume groups.
description:
  - This module fetches information about Nutanix PC Volume groups.
  - The module can fetch information about all Volume groups or a specific Volume group.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Get a Volume Group) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin, Prism Viewer,
      Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(List all the Volume Groups) -
      Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin, Prism Viewer,
      Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
    ext_id:
        description:
            - The external ID of the Volume Group.
        type: str
        required: false
    expand:
        description:
            - Expand related resources when listing or getting a Volume Group.
            - Use C(volumeGroupStats) to include volume group statistics.
            - When C(expand) is C(volumeGroupStats), C(start_time) and C(end_time)
              are required. Optional C(sampling_interval) and C(stat_type) are also
              supported with C(volumeGroupStats).
            - The module builds the API expand value as
              C(volumeGroupStats($startTime=...;$endTime=...)).
        type: str
        required: false
    start_time:
        description:
            - Start of the time window for which stats should be reported.
            - Supported with C(expand=volumeGroupStats). Required when C(expand)
              is C(volumeGroupStats).
            - Value must be in extended ISO-8601 format.
            - For example, C(2022-04-23T01:23:45.678Z).
        type: str
        required: false
    end_time:
        description:
            - End of the time window for which stats should be reported.
            - Supported with C(expand=volumeGroupStats). Required when C(expand)
              is C(volumeGroupStats).
            - Value must be in extended ISO-8601 format.
            - For example, C(2022-04-23T02:23:45.678Z).
        type: str
        required: false
    sampling_interval:
        description:
            - Sampling interval in seconds at which statistical data should be collected.
            - Supported with C(expand=volumeGroupStats).
            - For example, use C(30) for performance statistics every 30 seconds.
        type: int
        required: false
    stat_type:
        description:
            - Downsample operator applied to the statistical data.
            - Supported with C(expand=volumeGroupStats).
        type: str
        required: false
        choices: ["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"]
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Fetch information about all VGs
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Fetch information about a specific VG
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653

- name: List volume groups with stats expanded
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    expand: volumeGroupStats
    start_time: "2024-01-01T00:00:00.000Z"
    end_time: "2024-01-31T23:59:59.999Z"
    sampling_interval: 30
    stat_type: AVG
"""

RETURN = r"""
response:
    description:
        - Volume group details if C(ext_id) is provided.
        - List of Volume groups if C(ext_id) is not provided.
    type: dict
    returned: always
    sample: {
            "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
            "created_by": null,
            "created_time": null,
            "description": "Volume group 2",
            "enabled_authentications": null,
            "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
            "is_hidden": null,
            "iscsi_features": {
                "enabled_authentications": "CHAP",
                "iscsi_target_name": null,
                "target_secret": null
            },
            "iscsi_target_name": null,
            "iscsi_target_prefix": null,
            "links": null,
            "load_balance_vm_attachments": null,
            "name": "ansible-vgs-KjRMtTRxhrww2",
            "sharing_status": "SHARED",
            "should_load_balance_vm_attachments": true,
            "storage_features": {
                "flash_mode": {
                    "is_enabled": true
                }
            },
            "target_name": "vg1-792cd764-37b5-4da3-7ef1-ea3f618c1648",
            "target_prefix": null,
            "target_secret": null,
            "tenant_id": null,
        }
ext_id:
    description: Volume group external ID.
    type: str
    returned: When C(ext_id) is provided.
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching volume group info"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Failed generating volume groups info Spec"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
total_available_results:
    description:
        - The total number of available Volume groups in PC.
    type: int
    returned: when all volume groups are fetched
    sample: 125
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
        start_time=dict(type="str"),
        end_time=dict(type="str"),
        sampling_interval=dict(type="int"),
        stat_type=dict(
            type="str", choices=["SUM", "MIN", "MAX", "AVG", "COUNT", "LAST"]
        ),
    )
    return module_args


def _build_stats_expand(module, result):
    """Build volumeGroupStats(...) expand string with required/optional params."""
    expand = module.params.get("expand")
    if expand != "volumeGroupStats":
        return expand

    start_time = module.params.get("start_time")
    end_time = module.params.get("end_time")
    if not start_time or not end_time:
        module.fail_json(
            msg="start_time and end_time are required when expand is volumeGroupStats",
            **result,
        )

    params_list = [
        "$startTime={0}".format(start_time),
        "$endTime={0}".format(end_time),
    ]

    sampling_interval = module.params.get("sampling_interval")
    if sampling_interval is not None:
        params_list.append("$samplingInterval={0}".format(sampling_interval))

    stat_type = module.params.get("stat_type")
    if stat_type:
        params_list.append("$statType={0}".format(stat_type))

    return "volumeGroupStats({0})".format(";".join(params_list))


def get_vg(module, result):
    vgs = get_vg_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = vgs.get_volume_group_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume group info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vgs(module, result):
    vgs = get_vg_api_instance(module)

    expand = _build_stats_expand(module, result)
    if expand is not None:
        module.params["expand"] = expand

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume groups info Spec", **result)

    try:
        resp = vgs.list_volume_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume groups info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
        required_if=[
            ("expand", "volumeGroupStats", ("start_time", "end_time")),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_vg(module, result)
    else:
        get_vgs(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
