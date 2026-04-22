#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_protection_v2
short_description: Protect or unprotect a Nutanix cluster
version_added: 2.6.0
description:
  - Protect a cluster by enabling periodic full-cluster snapshots and replication
    to a protection target (C(LTSS) or C(LOCAL)).
  - Unprotect a cluster by stopping the snapshot schedule, removing the stored
    backup data from the target and clearing DR tracking.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Protect a cluster) -
    Required Roles: Cluster Admin, Disaster Recovery Admin, Prism Admin, Super Admin
  - >-
    B(Unprotect a cluster) -
    Required Roles: Cluster Admin, Disaster Recovery Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is C(present), the module will protect the cluster.
      - If C(state) is C(absent), the module will unprotect the cluster.
    type: str
    choices: ["present", "absent"]
    default: present
  ext_id:
    description:
      - External ID of the cluster to protect or unprotect.
    type: str
    required: true
  protection_rpo_minutes:
    description:
      - Recovery point objective for protecting the cluster.
      - Determines the frequency (in minutes) at which full-cluster snapshots are taken.
      - Allowed range is between C(60) and C(360). Default is C(60).
      - Required when C(state=present).
    type: int
    default: 60
  local_snapshot_retention_policy:
    description:
      - Number of local snapshots that the protection service should retain.
      - Allowed range is between C(2) and C(4). Default is C(2).
      - Required when C(state=present).
    type: int
    default: 2
  protection_target:
    description:
      - Where backups are stored.
      - C(LTSS) uses Multi-cloud Snapshot Technology (for example, AWS S3).
      - C(LOCAL) is only allowed in test environments.
      - Required when C(state=present).
    type: str
    choices: ["LOCAL", "LTSS"]
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Protect a cluster with hourly snapshots replicated to LTSS
  nutanix.ncp.ntnx_clusters_protection_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
    protection_rpo_minutes: 60
    local_snapshot_retention_policy: 2
    protection_target: LTSS
  register: result

- name: Protect a cluster in a test environment using LOCAL target
  nutanix.ncp.ntnx_clusters_protection_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
    protection_rpo_minutes: 60
    local_snapshot_retention_policy: 2
    protection_target: LOCAL
  register: result

- name: Unprotect a cluster
  nutanix.ncp.ntnx_clusters_protection_v2:
    state: absent
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0005a7b8-0b0b-4b3b-0000-000000000000"
  register: result
"""

RETURN = r"""
response:
  description:
    - Task details for the protect/unprotect operation.
    - Contains the task status, progress and entities affected.
  type: dict
  returned: always
ext_id:
  description:
    - External ID of the cluster on which the operation was performed.
  type: str
  returned: always
  sample: "0005a7b8-0b0b-4b3b-0000-000000000000"
task_ext_id:
  description: External ID of the task created by the protect/unprotect action.
  type: str
  returned: when a task is created
  sample: "ZXJnb24=:350f0fd5-097d-4ece-8f44-6e5bfbe2dc08"
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
from ..module_utils.v4.clusters_mgmt.spec.cluster_protection import (  # noqa: E402
    ClusterProtectionSpecs,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)
from ..module_utils.v4.clusters_mgmt.helpers import (
    get_cluster_protection_info,
)  # noqa: E402


SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clusters_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as clusters_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
    )
    module_args.update(ClusterProtectionSpecs.get_protection_spec())
    return module_args


def protect_cluster(module, result, api_instance, ext_id):
    validate_required_params(
        module,
        ["protection_target"],
    )

    sg = SpecGenerator(module)
    default_spec = clusters_sdk.ProtectionSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating protect cluster spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.protect_cluster(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while protecting cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id, add_task_service=True)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def unprotect_cluster(module, result, api_instance, ext_id):
    if module.check_mode:
        result["msg"] = "Cluster with ext_id:{0} will be unprotected.".format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.unprotect_cluster(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unprotecting cluster",
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
    state = module.params.get("state")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    if state == "present":
        protect_cluster(module, result, api_instance, ext_id)
    else:
        unprotect_cluster(module, result, api_instance, ext_id)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
