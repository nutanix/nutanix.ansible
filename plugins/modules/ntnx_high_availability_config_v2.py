#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_high_availability_config_v2
short_description: Enable or disable high availability configuration for a cluster
version_added: "2.7.0"
description:
    - Enable or disable compute high availability on a cluster.
    - When enabling, specifies the desired number of host failures to tolerate.
    - This is an action module that triggers a task-based operation.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Enable High Availability Config) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Disable High Availability Config) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - This module talks to B(Prism Central) (PC).
    - The referenced cluster must exist before enabling or disabling high availability.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
    state:
        description:
            - Specify state.
            - If C(state) is C(present), enable high availability on the cluster.
            - If C(state) is C(absent), disable high availability on the cluster.
        type: str
        choices:
            - present
            - absent
        default: present
    cluster_ext_id:
        description:
            - The external ID of the cluster.
        type: str
        required: true
    host_failures_to_tolerate_count:
        description:
            - Number of host failures the cluster is configured to tolerate.
            - Required when C(state) is C(present).
        type: int
        required: false
    dryrun:
        description:
            - Allows long running operations to execute in a dry-run mode providing ability
              to identify trouble spots and system failures without performing the actual
              operation.
            - The operation runs in dry-run mode only if the provided value is true.
            - Only applicable when C(state) is C(present).
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
- name: Enable high availability on a cluster
  nutanix.ncp.ntnx_high_availability_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    host_failures_to_tolerate_count: 1
  register: result
  ignore_errors: true

- name: Enable high availability with dryrun validation
  nutanix.ncp.ntnx_high_availability_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    host_failures_to_tolerate_count: 2
    dryrun: true
  register: result
  ignore_errors: true

- name: Disable high availability on a cluster
  nutanix.ncp.ntnx_high_availability_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for enabling or disabling high availability configuration.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-07-20T12:20:41.524581+00:00",
            "created_time": "2026-07-20T12:19:47.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2",
                    "rel": "clustermgmt:config:cluster"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T12:20:41.524581+00:00",
            "legacy_error_message": null,
            "operation": "EnableHighAvailabilityConfig",
            "operation_description": "Enable high availability config",
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
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode
    type: str
    sample: "High availability will be disabled."

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description: The external ID of the cluster
    returned: always
    type: str
    sample: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_high_availability_config_api_instance,
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

    from ..module_utils.v4.sdk_mock import mock_sdk as cluster_management_sdk  # noqa: E402  # fmt: skip

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(
            type="str",
            choices=["present", "absent"],
            default="present",
        ),
        cluster_ext_id=dict(type="str", required=True),
        host_failures_to_tolerate_count=dict(type="int"),
        dryrun=dict(type="bool"),
    )
    return module_args


def enable_high_availability_config(module, result, api_instance):
    validate_required_params(module, ["host_failures_to_tolerate_count"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.HighAvailabilityConfigEnableParams()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating enable high availability config spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "High availability will be enabled."
        return

    kwargs = {}
    dryrun = module.params.get("dryrun")
    if dryrun is not None:
        kwargs["_dryrun"] = dryrun

    try:
        resp = api_instance.enable_high_availability_config(
            clusterExtId=cluster_ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while enabling high availability config for cluster with ext_id: {0}".format(
                cluster_ext_id
            ),
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def disable_high_availability_config(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    if module.check_mode:
        result["response"] = {"cluster_ext_id": cluster_ext_id}
        result["msg"] = "High availability will be disabled."
        return

    resp = None
    try:
        resp = api_instance.disable_high_availability_config(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disabling high availability config for cluster with ext_id: {0}".format(
                cluster_ext_id
            ),
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
    result = {"changed": False, "failed": False, "response": None}

    api_instance = get_high_availability_config_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        enable_high_availability_config(module, result, api_instance)
    else:
        disable_high_availability_config(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
