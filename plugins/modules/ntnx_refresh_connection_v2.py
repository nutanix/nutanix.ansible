#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_refresh_connection_v2
short_description: Refresh a hardware provider connection in Nutanix Foundation Central
version_added: 2.7.0
description:
  - This module refreshes a connection to a hardware provider endpoint.
  - Refreshing a connection re-discovers nodes and/or refreshes the resource pools.
  - This is an action module that triggers a task-based operation.
  - This module uses Foundation Central (FCVM) v4 APIs based SDKs.
notes:
  - This module talks to B(Foundation Central / FCVM), B(not) Prism Central.
    Set C(nutanix_host) to the Foundation Central (FCVM) endpoint.
  - >-
    B(Refresh a connection) -
    Required Roles - Admin role on Foundation Central.
  - The referenced hardware provider and connection must exist before refreshing.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  hardware_provider_ext_id:
    description:
      - External ID of the hardware provider that owns the connection.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the connection to refresh.
    type: str
    required: true
  configuration:
    description:
      - Configuration describing what to refresh.
      - The Foundation Central API requires a configuration to be provided.
      - Exactly one of the configuration types may be provided.
    type: dict
    required: false
    suboptions:
      discover_nodes:
        description:
          - Configuration to discover nodes for the given group identifiers.
        type: dict
        required: false
        suboptions:
          group_ids:
            description:
              - List of group identifiers to discover nodes for.
            type: list
            elements: str
            required: false
      refresh_resources:
        description:
          - Configuration to refresh resource pools.
        type: dict
        required: false
        suboptions:
          group_ids:
            description:
              - List of group identifiers to refresh resources for.
            type: list
            elements: str
            required: false
          should_refresh_mac_pools:
            description:
              - Whether to refresh MAC address pools.
            type: bool
            required: false
          should_refresh_ip_pools:
            description:
              - Whether to refresh IP address pools.
            type: bool
            required: false
          should_refresh_server_identity_pools:
            description:
              - Whether to refresh server identity pools.
            type: bool
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
- name: Refresh a connection to discover nodes
  nutanix.ncp.ntnx_refresh_connection_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    configuration:
      discover_nodes:
        group_ids:
          - "group-1"
          - "group-2"
  register: result
  ignore_errors: true

- name: Refresh a connection to refresh resource pools
  nutanix.ncp.ntnx_refresh_connection_v2:
    nutanix_host: "{{ foundation_host }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    hardware_provider_ext_id: "5e5a9d0b-8f3d-4c14-9f6f-6b3a3c9c6a01"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    configuration:
      refresh_resources:
        group_ids:
          - "group-1"
        should_refresh_mac_pools: true
        should_refresh_ip_pools: true
        should_refresh_server_identity_pools: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the refresh connection API.
    - If C(wait) is true, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "completed_time": "2026-09-09T04:59:56.942665+00:00",
      "ext_id": "ZXJnb24=:612b2437-166a-5a33-99e9-9f5572031a5a",
      "operation": "DiscoverNodesFromHardwareProviderConnectionTask",
      "operation_description": "Discover nodes for hardware provider connection connection_ansible_updated",
      "progress_percentage": 100,
      "status": "SUCCEEDED"
    }

task_ext_id:
  description:
    - The external ID of the task for the refresh connection action.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the connection that was refreshed.
  returned: when applicable
  type: str
  sample: "89af36d8-b9b2-4623-9406-799ee178757b"

changed:
  description: This indicates whether the action resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the action was skipped.
  returned: when applicable
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: when something fails
  type: bool
  sample: false

msg:
  description: This indicates the status or error message.
  returned: when applicable
  type: str
  sample: "Connection with ext_id:8300384a-56ee-4750-aeb8-3d1c42908bee will be refreshed."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_hardware_providers_api_instance,
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
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    discover_nodes_spec = dict(
        group_ids=dict(type="list", elements="str", required=False),
    )
    refresh_resources_spec = dict(
        group_ids=dict(type="list", elements="str", required=False),
        should_refresh_mac_pools=dict(type="bool", required=False),
        should_refresh_ip_pools=dict(type="bool", required=False),
        should_refresh_server_identity_pools=dict(type="bool", required=False),
    )
    configuration_spec = dict(
        discover_nodes=dict(
            type="dict",
            options=discover_nodes_spec,
            obj=lifecycle_sdk.DiscoverNodesSpec,
            required=False,
        ),
        refresh_resources=dict(
            type="dict",
            options=refresh_resources_spec,
            obj=lifecycle_sdk.RefreshResourcesSpec,
            required=False,
        ),
    )
    module_args = dict(
        hardware_provider_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        configuration=dict(
            type="dict",
            options=configuration_spec,
            obj=dict(
                discover_nodes=lifecycle_sdk.DiscoverNodesSpec,
                refresh_resources=lifecycle_sdk.RefreshResourcesSpec,
            ),
            required=False,
            mutually_exclusive=[("discover_nodes", "refresh_resources")],
        ),
    )
    return module_args


def run_action(module, api_instance, result):
    hardware_provider_ext_id = module.params.get("hardware_provider_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["hardware_provider_ext_id", "ext_id"])

    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.RefreshConnectionSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating refresh connection spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Connection with ext_id:{0} will be refreshed.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.refresh_connection(
            hardwareProviderExtId=hardware_provider_ext_id,
            extId=ext_id,
            body=spec,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while refreshing connection",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_hardware_providers_api_instance(module)
    run_action(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
