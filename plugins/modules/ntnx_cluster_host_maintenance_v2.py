#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_maintenance_v2
short_description: Exit a Nutanix cluster host from maintenance mode
version_added: 2.7.0
description:
  - This module allows you to transition a Nutanix cluster host out of maintenance mode.
  - Once the host successfully exits maintenance mode the previously migrated user VMs
    are migrated back to restore VM locality, any pinned VMs that were shut down during
    entry into maintenance mode are powered back on, and the cluster-wide shutdown
    token acquired at entry time is released.
  - For ESXi hypervisors, vCenter address and credentials must be supplied so that
    the exit operation is coordinated with the vSphere management plane.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Exit host from maintenance mode) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported for this action.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster that owns the host.
    type: str
    required: true
  ext_id:
    description:
      - The external ID (UUID) of the host that must exit maintenance mode.
    type: str
    required: true
  vcenter_info:
    description:
      - vCenter Server information for the ESX cluster.
      - Required when the target host is an ESXi host so the exit maintenance
        workflow can coordinate with vSphere.
    type: dict
    required: false
    suboptions:
      address:
        description:
          - IP address or fully-qualified domain name of the vCenter Server.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - IPv4 address of the vCenter Server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The IPv4 prefix length (0-32).
                type: int
                required: false
                default: 32
          ipv6:
            description:
              - IPv6 address of the vCenter Server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - The IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - The IPv6 prefix length (0-128).
                type: int
                required: false
                default: 128
          fqdn:
            description:
              - Fully-qualified domain name of the vCenter Server.
            type: dict
            required: false
            suboptions:
              value:
                description:
                  - FQDN string of the vCenter Server.
                type: str
                required: true
      credentials:
        description:
          - Credentials for the vCenter Server used to coordinate the ESXi
            host maintenance exit workflow.
        type: dict
        required: false
        suboptions:
          username:
            description:
              - Username for vCenter Server authentication.
            type: str
            required: true
          password:
            description:
              - Password for the vCenter Server user.
            type: str
            required: true
          port:
            description:
              - Port to connect to the vCenter Server on.
            type: int
            required: false
  timeout_seconds:
    description:
      - Timeout in seconds for the exit host maintenance operation on the server
        side. When not provided, the platform default is used.
    type: int
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
- name: Exit AHV host from maintenance mode
  nutanix.ncp.ntnx_cluster_host_maintenance_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "0006250e-1e01-2222-0000-abcdef012345"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    timeout_seconds: 600
  register: result
  ignore_errors: true

- name: Exit ESXi host from maintenance mode with vCenter credentials
  nutanix.ncp.ntnx_cluster_host_maintenance_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "0006250e-1e01-2222-0000-abcdef012345"
    ext_id: "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    timeout_seconds: 900
    vcenter_info:
      address:
        ipv4:
          value: "10.44.100.10"
          prefix_length: 32
      credentials:
        username: "administrator@vsphere.local"
        password: "vC3nt3rP@ss!"
        port: 443
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the exit host from maintenance mode operation.
    - Task details when C(wait) is true.
    - Task acknowledgement returned by the API when C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0006250e-1e01-2222-0000-abcdef012345"
      ],
      "completed_time": "2026-07-20T13:15:47.123456+00:00",
      "completion_details": null,
      "created_time": "2026-07-20T13:15:20.000000+00:00",
      "entities_affected": [
        {
          "ext_id": "8300384a-56ee-4750-aeb8-3d1c42908bee",
          "name": null,
          "rel": "clustermgmt:config:host"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T13:15:47.123456+00:00",
      "legacy_error_message": null,
      "operation": "ExitHostMaintenance",
      "operation_description": "Exit host maintenance mode",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T13:15:20.100000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: The status/error message returned by the module.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while exiting host from maintenance mode"

error:
  description: The error details returned by the platform when the exit host maintenance operation fails.
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the underlying async task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the host that was requested to exit maintenance mode.
  returned: always
  type: str
  sample: "8300384a-56ee-4750-aeb8-3d1c42908bee"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=cluster_management_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=cluster_management_sdk.IPv6Address,
            required=False,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            obj=cluster_management_sdk.FQDN,
            required=False,
        ),
    )

    vcenter_credentials_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        port=dict(type="int", required=False),
    )

    vcenter_info_spec = dict(
        address=dict(
            type="dict",
            options=ip_address_or_fqdn_spec,
            obj=cluster_management_sdk.IPAddressOrFQDN,
            required=True,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
        ),
        credentials=dict(
            type="dict",
            options=vcenter_credentials_spec,
            obj=cluster_management_sdk.VcenterCredentials,
            required=False,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        vcenter_info=dict(
            type="dict",
            options=vcenter_info_spec,
            obj=cluster_management_sdk.VcenterInfo,
            required=False,
        ),
        timeout_seconds=dict(type="int", required=False),
    )
    return module_args


def exit_host_maintenance(module, result, clusters_api):
    """Trigger the ExitHostMaintenance action on the given host."""
    validate_required_params(module, ["cluster_ext_id", "ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.HostMaintenanceCommonSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating exit host maintenance spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = clusters_api.exit_host_maintenance(
            clusterExtId=cluster_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while exiting host from maintenance mode",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
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
    clusters_api = get_clusters_api_instance(module)
    exit_host_maintenance(module, result, clusters_api)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
