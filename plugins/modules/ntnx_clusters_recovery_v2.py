#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_recovery_v2
short_description: Create or finalize a cluster recovery plan
version_added: 2.6.0
description:
  - Initialize or finalize a cluster disaster-recovery (DR) plan.
  - Use operation=initialize to create a recovery plan against a brand new, empty destination cluster.
    (Requires providing the destination cluster external ID). The system connects the destination cluster to the backup storage (LTSS),
    locates the latest snapshots of the faulted source cluster, and begins hydrating (downloading and registering) the storage containers,
    networks, and VMs onto the new hardware in a staged, read-only state.
  - Use operation=finalize to commit the failover. The staged, read-only storage on the destination cluster is promoted to active (read-write),
    and the recovered VMs are powered on. The destination cluster then automatically resumes the original protection schedule.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Initialize a cluster recovery - create recovery plan) -
    Required Roles: Cluster Admin, Disaster Recovery Admin, Prism Admin, Super Admin
  - >-
    B(Finalize a cluster recovery - commit failover) -
    Required Roles: Cluster Admin, Disaster Recovery Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - Only C(present) is supported for this module.
      - The actual action is controlled by C(operation).
    type: str
    choices: ["present"]
    default: present
  operation:
    description:
      - The recovery operation to perform on the faulted cluster.
      - C(initialize) creates a new recovery plan. Requires
        C(destination_cluster_ext_id).
      - C(finalize) commits the failover on an in-progress recovery.
    type: str
    choices: ["initialize", "finalize"]
    required: true
  ext_id:
    description:
      - External ID of the original, faulted source cluster being recovered.
    type: str
    required: true
  destination_cluster_ext_id:
    description:
      - External ID of the brand new, empty destination cluster onto which
        the source cluster will be recovered.
      - Required when C(operation=initialize).
    type: str
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Initialize recovery - create a cluster recovery plan
  nutanix.ncp.ntnx_clusters_recovery_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    operation: initialize
    ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
    destination_cluster_ext_id: "0006b8c9-1c1c-5c4c-1111-111111111111"
  register: result

- name: Finalize recovery - commit the failover on the destination cluster
  nutanix.ncp.ntnx_clusters_recovery_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    operation: finalize
    ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
  register: result
"""

RETURN = r"""
response:
  description: Task details for the initialize/finalize recovery operation.
  type: dict
  returned: always
ext_id:
  description: External ID of the source cluster on which the operation was performed.
  type: str
  returned: always
task_ext_id:
  description: External ID of the task created by the recovery action.
  type: str
  returned: when a task is created
changed:
  description: Indicates if any change was made.
  type: bool
  returned: always
msg:
  description: A human readable message about the result of the action.
  type: str
  returned: when a message is emitted
error:
  description: Error message if any.
  type: str
  returned: when an error occurs
failed:
  description: Indicates if the module failed.
  type: bool
  returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_protection_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_cluster_recovery_info,
)
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
        operation=dict(
            type="str",
            choices=["initialize", "finalize"],
            required=True,
        ),
        ext_id=dict(type="str", required=True),
        destination_cluster_ext_id=dict(type="str"),
    )
    return module_args


def initialize_cluster_recovery(module, result, api_instance, ext_id):
    sg = SpecGenerator(module)
    default_spec = clusters_sdk.RecoverySpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating initialize cluster recovery spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.initialize_cluster_recovery(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while initializing cluster recovery",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, add_task_service=True)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def finalize_cluster_recovery(module, result, api_instance, ext_id):
    if module.check_mode:
        result["msg"] = (
            "Cluster recovery for cluster with ext_id:{0} will be finalized.".format(
                ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.finalize_cluster_recovery(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while finalizing cluster recovery",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, add_task_service=True)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("operation", "initialize", ("destination_cluster_ext_id",)),
        ],
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
    }
    api_instance = get_cluster_protection_api_instance(module)
    operation = module.params.get("operation")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    if operation == "initialize":
        initialize_cluster_recovery(module, result, api_instance, ext_id)
    else:
        finalize_cluster_recovery(module, result, api_instance, ext_id)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
