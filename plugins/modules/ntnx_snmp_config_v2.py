#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_config_v2
short_description: Update SNMP configuration on a Nutanix cluster
version_added: 2.6.0
description:
  - Update SNMP configuration on a Nutanix cluster.
  - Update SNMP status (enable/disable) when C(is_enabled) is provided.
  - Add SNMP transport ports and protocol details when C(state) is C(present), C(transports) and C(port) are provided.
  - Remove SNMP transport ports and protocol details when C(state) is C(absent), C(transports) and C(port) are provided.
  - This module uses PC v4 APIs based SDKs.
options:
  state:
    description:
      - If C(state) is C(present), it will add the specified SNMP transport.
      - If C(state) is C(absent), it will remove the specified SNMP transport.
      - State is only used for transport operations. It is ignored when C(is_enabled) is provided.
    type: str
    choices: ['present', 'absent']
  cluster_ext_id:
    description:
      - The external ID of the cluster.
    type: str
    required: true
  is_enabled:
    description:
      - SNMP status. Set to C(true) to enable SNMP, C(false) to disable.
      - When provided, the module will update SNMP status instead of managing transports.
    type: bool
  protocol:
    description:
      - SNMP transport protocol.
      - Required when adding or removing SNMP transport.
    type: str
    choices: ['UDP', 'UDP6', 'TCP', 'TCP6']
  port:
    description:
      - SNMP port number.
      - Required when adding or removing SNMP transport.
    type: int
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Enable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    is_enabled: true
  register: result

- name: Disable SNMP on a cluster
  nutanix.ncp.ntnx_snmp_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    is_enabled: false
  register: result

- name: Add SNMP transport
  nutanix.ncp.ntnx_snmp_config_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    protocol: UDP
    port: 162
  register: result

- name: Remove SNMP transport
  nutanix.ncp.ntnx_snmp_config_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    protocol: UDP
    port: 162
  register: result
"""

RETURN = r"""
response:
  description:
    - Task details for SNMP config operations.
  type: dict
  returned: always
  sample:
    {
      "app_name": null,
      "batch_summary": null,
      "cluster_ext_ids": null,
      "completed_time": "2026-03-12T12:06:25.726843+00:00",
      "completion_details": null,
      "created_time": "2026-03-12T12:06:25.540060+00:00",
      "entities_affected": null,
      "error_messages": null,
      "ext_id": "ZXJnb24=:54a506dc-6d4f-4344-43e4-41205eba32f4",
      "is_background_task": false,
      "is_cancelable": false,
      "last_updated_time": "2026-03-12T12:06:25.726842+00:00",
      "legacy_error_message": null,
      "number_of_entities_affected": 0,
      "number_of_subtasks": 0,
      "operation": "UpdateSnmpStatus",
      "operation_description": "Update snmp status",
      "owned_by": {
          "ext_id": "00000000-0000-0000-0000-000000000000",
          "name": "admin"
      },
      "parent_task": null,
      "progress_percentage": 100,
      "resource_links": null,
      "root_task": null,
      "started_time": "2026-03-12T12:06:25.604235+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description: Task External ID
  returned: always
  type: str
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
error:
  description: Error message if any
  returned: always
  type: str
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

cluster_ext_id:
  description: The external ID of the cluster.
  returned: always
  type: str
  sample: "913fa076-d385-4dd8-b549-0e628e645569"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_snmp_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        is_enabled=dict(type="bool"),
        protocol=dict(type="str", choices=["UDP", "UDP6", "TCP", "TCP6"], obj=clusters_sdk.SnmpProtocol),
        port=dict(type="int"),
    )

    return module_args


def update_snmp_status(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    is_enabled = module.params.get("is_enabled")
    result["cluster_ext_id"] = cluster_ext_id

    spec = clusters_sdk.SnmpStatusParam(is_enabled=is_enabled)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.update_snmp_status(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating SNMP status",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def add_snmp_transport(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.SnmpTransport()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating add SNMP transport spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.add_snmp_transport(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while adding SNMP transport",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def remove_snmp_transport(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.SnmpTransport()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating remove SNMP transport spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.remove_snmp_transport(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while removing SNMP transport",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

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
        "task_ext_id": None,
    }
    api_instance = get_snmp_api_instance(module)

    if module.params.get("is_enabled") is not None:
        update_snmp_status(module, result, api_instance)
    else:
        if not module.params.get("protocol") or not module.params.get("port"):
            module.fail_json(
                msg="protocol and port are required when adding or removing SNMP transport",
                **result
            )
        state = module.params["state"]
        if state == "present":
            add_snmp_transport(module, result, api_instance)
        else:
            remove_snmp_transport(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
