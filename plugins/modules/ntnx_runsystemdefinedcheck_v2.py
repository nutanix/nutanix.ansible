#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_runsystemdefinedcheck_v2
short_description: Run system-defined checks and manage SDA policy cluster configs in Nutanix Prism Central
version_added: "2.6.0"
description:
    - Run system-defined checks on a cluster using the Nutanix monitoring API.
    - Update cluster-specific configuration for a system-defined alert policy.
    - Delete is not supported for system-defined policies; state=absent will fail with an appropriate message.
    - This module uses PC v4 APIs based SDKs.
options:
  ext_id:
    description:
      - The external ID of the cluster config entry to update.
      - Required for update operations (state=present with system_defined_policy_ext_id).
    required: false
    type: str
  cluster_ext_id:
    description:
      - The external ID of the cluster on which to run system-defined checks.
      - Required for create (run checks) operations.
    required: false
    type: str
  system_defined_policy_ext_id:
    description:
      - The external ID of the system-defined alert policy.
      - Required for update operations.
    required: false
    type: str
  sda_ext_ids:
    description:
      - List of check IDs to be executed.
      - Mutually exclusive with should_run_all_checks.
    required: false
    type: list
    elements: str
  should_anonymize:
    description:
      - Whether to mask sensitive data in the check run summary.
    required: false
    type: bool
    default: true
  should_send_report_to_configured_recipients:
    description:
      - Whether to send the run summary to the configured email address.
    required: false
    type: bool
    default: true
  additional_recipients:
    description:
      - Additional email addresses for sending the run summary.
    required: false
    type: list
    elements: str
  node_ips:
    description:
      - List of node IP addresses where the check will run.
      - Ignored if the check scope is a cluster.
    required: false
    type: list
    elements: dict
    suboptions:
      value:
        description:
          - The IPv4 address of the node.
        type: str
        required: true
      prefix_length:
        description:
          - The prefix length of the IPv4 address.
        type: int
        required: false
  should_run_all_checks:
    description:
      - Whether to run all system-defined checks applicable to the cluster.
      - Mutually exclusive with sda_ext_ids.
    required: false
    type: bool
    default: false
  is_enabled:
    description:
      - Whether the SDA policy is enabled on the cluster.
      - Used during update operations.
    required: false
    type: bool
  schedule_interval_seconds:
    description:
      - Interval in seconds for periodically executing the SDA policy.
      - Used during update operations.
    required: false
    type: int
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Run specific system-defined checks on a cluster
  nutanix.ncp.ntnx_runsystemdefinedcheck_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    sda_ext_ids:
      - "check-ext-id-1"
    should_anonymize: true
    should_send_report_to_configured_recipients: false
  register: result

- name: Run all system-defined checks on a cluster
  nutanix.ncp.ntnx_runsystemdefinedcheck_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    should_run_all_checks: true
  register: result

- name: Update cluster config for an SDA policy
  nutanix.ncp.ntnx_runsystemdefinedcheck_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    system_defined_policy_ext_id: "policy-ext-id"
    ext_id: "cluster-config-ext-id"
    is_enabled: true
    schedule_interval_seconds: 3600
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix monitoring API.
    - For create operations, this will be the task reference.
    - For update operations, this will be the updated cluster config.
  type: dict
  returned: always
changed:
  description: Whether the resource was changed.
  type: bool
  returned: always
  sample: true
ext_id:
  description: The external ID of the resource.
  type: str
  returned: when applicable
task_ext_id:
  description: The task external ID for async operations (run checks).
  type: str
  returned: when a task is created
skipped:
  description: Whether the operation was skipped due to idempotency.
  type: bool
  returned: when applicable
msg:
  description: Informational message about the operation.
  type: str
  returned: when applicable
error:
  description: Error message if an error occurs.
  type: str
  returned: when an error occurs
failed:
  description: Whether the module execution failed.
  type: bool
  returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.monitoring.api_client import (  # noqa: E402
    get_etag,
    get_system_defined_checks_api_instance,
    get_system_defined_policies_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_monitoring_py_client as monitoring_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as monitoring_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        system_defined_policy_ext_id=dict(type="str"),
        sda_ext_ids=dict(type="list", elements="str"),
        should_anonymize=dict(type="bool", default=True),
        should_send_report_to_configured_recipients=dict(type="bool", default=True),
        additional_recipients=dict(type="list", elements="str"),
        node_ips=dict(
            type="list",
            elements="dict",
            options=ipv4_spec,
            obj=monitoring_sdk.IPv4Address,
        ),
        should_run_all_checks=dict(type="bool", default=False),
        is_enabled=dict(type="bool"),
        schedule_interval_seconds=dict(type="int"),
    )

    return module_args


def create_run_checks(module, checks_api, result):
    """Run system-defined checks on a cluster."""
    sg = SpecGenerator(module)
    default_spec = monitoring_sdk.RunSystemDefinedChecksSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for running system-defined checks", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = None
    try:
        resp = checks_api.run_system_defined_checks(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while running system-defined checks",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())


def get_cluster_config(module, policies_api, system_defined_policy_ext_id, ext_id):
    """Fetch a cluster config entry for an SDA policy."""
    try:
        return policies_api.get_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id,
            extId=ext_id,
        ).data
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster config",
        )


def check_cluster_config_idempotency(old_spec, update_spec):
    """Compare two cluster config specs for idempotency."""
    old = deepcopy(old_spec)
    new = deepcopy(update_spec)
    strip_internal_attributes(old)
    strip_internal_attributes(new)
    return old == new


def update_cluster_config(module, policies_api, result):
    """Update cluster-specific configuration for an SDA policy."""
    ext_id = module.params.get("ext_id")
    system_defined_policy_ext_id = module.params.get("system_defined_policy_ext_id")
    result["ext_id"] = ext_id

    current_spec = get_cluster_config(
        module, policies_api, system_defined_policy_ext_id, ext_id
    )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating cluster config update spec", **result)

    if check_cluster_config_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    etag = get_etag(data=current_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = policies_api.update_cluster_config_by_id(
            systemDefinedPolicyExtId=system_defined_policy_ext_id,
            extId=ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating cluster config",
        )

    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_run_checks(module, result):
    """Handle delete operation — not supported for system-defined policies."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Delete is not supported for system-defined checks/policies."
        return

    module.fail_json(
        msg="Delete is not supported for system-defined checks/policies.", **result
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            (
                "state",
                "present",
                ("cluster_ext_id", "system_defined_policy_ext_id"),
                True,
            ),
            ("state", "absent", ("ext_id",)),
        ],
        mutually_exclusive=[
            ("sda_ext_ids", "should_run_all_checks"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_monitoring_py_client"),
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
    state = module.params["state"]
    if state == "present":
        if module.params.get("system_defined_policy_ext_id") and module.params.get(
            "ext_id"
        ):
            policies_api = get_system_defined_policies_api_instance(module)
            update_cluster_config(module, policies_api, result)
        else:
            checks_api = get_system_defined_checks_api_instance(module)
            create_run_checks(module, checks_api, result)
    else:
        delete_run_checks(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
