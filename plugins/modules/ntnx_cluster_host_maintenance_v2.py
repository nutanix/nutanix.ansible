#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_maintenance_v2
short_description: Put a Nutanix cluster host into or out of maintenance mode
version_added: 2.7.0
description:
  - Put a Nutanix cluster host into maintenance mode (C(state=present)) or take
    it out of maintenance mode (C(state=absent)) using the v4 clustermgmt
    Planned Outage Manager (POM) API.
  - When C(state) is C(present), workloads are migrated, non-migratable UVMs may
    be shut down when consented, and the CVM is shut down safely.
  - When C(state) is C(absent), VM locality is restored, pinned VMs are powered
    back on, and the cluster-wide shutdown token is released.
  - The operation is orchestrated asynchronously; the SDK returns a task
    external ID that the module tracks until completion when C(wait) is C(true).
  - Requires the cluster external ID and the host external ID.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Enter Cluster Host Maintenance) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - >-
    B(Exit Cluster Host Maintenance) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present), the host identified by C(ext_id) is put
        into maintenance mode.
      - If C(state) is set to C(absent), the host identified by C(ext_id) is taken
        out of maintenance mode.
      - C(should_rollback_on_failure) and C(should_shutdown_non_migratable_uvms)
        are only valid when C(state) is C(present).
    type: str
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - External ID (UUID) of the cluster that owns the target host.
    type: str
    required: true
  ext_id:
    description:
      - External ID (UUID) of the host to put into or take out of maintenance
        mode.
    type: str
    required: true
  should_rollback_on_failure:
    description:
      - Whether the Planned Outage Manager workflow must roll back state
        changes (e.g. power the CVM back on, restart previously stopped pinned
        VMs) if the maintenance workflow fails.
      - Defaults to C(true) on the server if left unset.
      - Only applicable when C(state) is C(present).
    type: bool
    required: false
  should_shutdown_non_migratable_uvms:
    description:
      - Whether to power off UVMs that cannot be migrated off the host (e.g.
        pinned VMs or RF1 VMs) so the enter-maintenance workflow can proceed.
      - Callers usually query the C(compute-non-migratable-vms) API first and
        set this to C(true) to grant consent for the shutdown.
      - Defaults to C(false) on the server if left unset.
      - Only applicable when C(state) is C(present).
    type: bool
    required: false
  timeout_seconds:
    description:
      - Server-side timeout in seconds for the maintenance workflow.
      - Minimum value is 1.
    type: int
    required: false
  vcenter_info:
    description:
      - vCenter connection information required for ESXi hosts so that Prism
        can coordinate putting the host into or out of maintenance mode with
        vSphere.
      - Not required for AHV hosts.
      - When set, both C(address) and C(credentials) are required.
    type: dict
    required: false
    suboptions:
      address:
        description:
          - vCenter IP address or FQDN. Exactly one of C(ipv4), C(ipv6) or
            C(fqdn) must be provided.
        type: dict
        required: true
        suboptions:
          ipv4:
            description:
              - IPv4 address of the vCenter server.
            type: dict
            suboptions:
              value:
                description:
                  - IPv4 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the IPv4 address.
                  - Defaults to 32 on the server if left unset.
                type: int
                required: false
          ipv6:
            description:
              - IPv6 address of the vCenter server.
            type: dict
            suboptions:
              value:
                description:
                  - IPv6 address value.
                type: str
                required: true
              prefix_length:
                description:
                  - Prefix length of the IPv6 address.
                  - Defaults to 128 on the server if left unset.
                type: int
                required: false
          fqdn:
            description:
              - Fully qualified domain name of the vCenter server.
            type: dict
            suboptions:
              value:
                description:
                  - FQDN value.
                type: str
                required: true
      credentials:
        description:
          - Credentials used by Prism to authenticate with vCenter.
        type: dict
        required: true
        suboptions:
          username:
            description:
              - vCenter username.
            type: str
            required: true
          password:
            description:
              - vCenter password. It is marked C(no_log) so its value is never
                logged.
            type: str
            required: true
          port:
            description:
              - vCenter port used to connect.
              - Defaults to 443 on the server if left unset.
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
- name: Put an AHV host into maintenance mode
  nutanix.ncp.ntnx_cluster_host_maintenance_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    should_rollback_on_failure: true
    should_shutdown_non_migratable_uvms: false
    timeout_seconds: 3600
  register: result
  ignore_errors: true

- name: Put an ESXi host into maintenance mode with vCenter info
  nutanix.ncp.ntnx_cluster_host_maintenance_v2:
    state: present
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    should_rollback_on_failure: true
    should_shutdown_non_migratable_uvms: true
    timeout_seconds: 3600
    vcenter_info:
      address:
        ipv4:
          value: "10.44.76.29"
      credentials:
        username: "administrator@vsphere.local"
        password: "vcenter-password"
        port: 443
  register: result
  ignore_errors: true

- name: Take an AHV host out of maintenance mode
  nutanix.ncp.ntnx_cluster_host_maintenance_v2:
    state: absent
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    timeout_seconds: 600
  register: result
  ignore_errors: true

- name: Take an ESXi host out of maintenance mode with vCenter credentials
  nutanix.ncp.ntnx_cluster_host_maintenance_v2:
    state: absent
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    timeout_seconds: 900
    vcenter_info:
      address:
        ipv4:
          value: "10.44.100.10"
          prefix_length: 32
      credentials:
        username: "administrator@vsphere.local"
        password: "vcenter-password"
        port: 443
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for putting the host into or taking it out of maintenance mode.
    - Task details when C(wait) is true (task run to completion).
    - Task reference details when C(wait) is false.
    - In check mode, the generated request body for the selected state.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
        "0006361b-6855-3644-7458-2268f8ffb2bd"
      ],
      "completed_time": "2026-07-20T12:20:41.524581+00:00",
      "created_time": "2026-07-20T12:19:47.167906+00:00",
      "entities_affected": [
        {
          "ext_id": "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9",
          "rel": "clustermgmt:config:host"
        },
        {
          "ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
          "rel": "clustermgmt:config:cluster"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T12:20:41.524581+00:00",
      "legacy_error_message": null,
      "operation": "HostEnterMaintenance",
      "operation_description": "Enter host into maintenance mode",
      "owned_by": {
        "ext_id": "00000000-0000-0000-0000-000000000000",
        "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "started_time": "2026-07-20T12:19:47.185754+00:00",
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
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while putting host into maintenance mode"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: when an error occurs
  type: str
  sample: "Not Found"

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
  description: The external ID of the host that was put into or taken out of maintenance mode.
  returned: always
  type: str
  sample: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"

cluster_ext_id:
  description: The external ID of the cluster that owns the host.
  returned: always
  type: str
  sample: "0006361b-6855-3644-7458-2268f8ffb2bd"
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
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as cluster_management_sdk  # noqa: E402  # fmt: skip

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    ip_address_or_fqdn_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            obj=cluster_management_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
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
            required=True,
            options=ip_address_or_fqdn_spec,
            obj=cluster_management_sdk.IPAddressOrFQDN,
            mutually_exclusive=[("ipv4", "ipv6", "fqdn")],
            required_one_of=[("ipv4", "ipv6", "fqdn")],
        ),
        credentials=dict(
            type="dict",
            required=True,
            options=vcenter_credentials_spec,
            obj=cluster_management_sdk.VcenterCredentials,
        ),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present", "absent"]),
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        should_rollback_on_failure=dict(type="bool", required=False),
        should_shutdown_non_migratable_uvms=dict(type="bool", required=False),
        timeout_seconds=dict(type="int", required=False),
        vcenter_info=dict(
            type="dict",
            required=False,
            options=vcenter_info_spec,
            obj=cluster_management_sdk.VcenterInfo,
        ),
    )
    return module_args


def validate_state_params(module, result):
    """Reject enter-only params when taking a host out of maintenance."""
    if module.params.get("state") != "absent":
        return
    enter_only = []
    if module.params.get("should_rollback_on_failure") is not None:
        enter_only.append("should_rollback_on_failure")
    if module.params.get("should_shutdown_non_migratable_uvms") is not None:
        enter_only.append("should_shutdown_non_migratable_uvms")
    if enter_only:
        module.fail_json(
            msg=(
                "Parameters {0} are only valid when state is present "
                "(putting a host into maintenance mode)"
            ).format(", ".join(enter_only)),
            **result,
        )


def enter_host_maintenance(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.EnterHostMaintenanceSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for entering host maintenance mode",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.enter_host_maintenance(
            clusterExtId=cluster_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while putting host into maintenance mode",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def exit_host_maintenance(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    result["cluster_ext_id"] = cluster_ext_id
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

    resp = None
    try:
        resp = api_instance.exit_host_maintenance(
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
        "failed": False,
        "ext_id": None,
        "cluster_ext_id": None,
        "task_ext_id": None,
    }
    validate_state_params(module, result)
    api_instance = get_clusters_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        enter_host_maintenance(module, result, api_instance)
    else:
        exit_host_maintenance(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
