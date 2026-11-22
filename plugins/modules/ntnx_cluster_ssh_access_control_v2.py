#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_ssh_access_control_v2
short_description: Update external SSH access control for a cluster
version_added: "2.7.0"
description:
  - This module allows you to update the external SSH access control
    settings of a cluster in Nutanix Prism Central.
  - External SSH access control is a singleton resource per cluster,
    identified by the cluster external ID.
  - There is no create or delete operation for this resource; only
    update is supported.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned
    to the user performing the operation.
  - >-
    B(Update External SSH Access Control) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - The cluster referenced by C(cluster_ext_id) must exist before
    updating SSH access control.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - Specify state.
      - If C(state) is set to C(present), the module will update the
        external SSH access control.
      - C(absent) is not supported because SSH access control cannot be
        deleted.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - The external ID of the cluster to update SSH access control for.
    type: str
    required: true
  is_ssh_enabled:
    description:
      - Indicates whether SSH is currently enabled on the cluster.
    type: bool
    required: false
  is_password_login_enabled:
    description:
      - Indicates whether password-based SSH login is enabled on the
        cluster.
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
- name: Update external SSH access control - enable SSH
  nutanix.ncp.ntnx_cluster_ssh_access_control_v2:
    cluster_ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
    is_ssh_enabled: true
    is_password_login_enabled: false
  register: result
  ignore_errors: true

- name: Update external SSH access control - disable SSH
  nutanix.ncp.ntnx_cluster_ssh_access_control_v2:
    cluster_ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
    is_ssh_enabled: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating external SSH access control for a cluster.
    - If C(wait) is true, it will contain the task details after
      completion.
    - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
      "app_name": null,
      "cluster_ext_ids": [
        "00065ffe-0266-379f-0000-000000028f57"
      ],
      "completed_time": "2026-11-22T09:42:59.639680+00:00",
      "created_time": "2026-11-22T09:42:44.043226+00:00",
      "entities_affected": [
        {
          "ext_id": "7488b33a-b7d0-43cf-59aa-d4ecad2b6bdb",
          "name": "Enable SSH Protocol Access",
          "rel": "EnableSSHProtocolAccessTask"
        }
      ],
      "ext_id": "ZXJnb24=:bdd07ab4-889b-4617-723f-ccedfb0416ad",
      "operation": "EnableSSHProtocolAccessOp",
      "operation_description": "Enable SSH Protocol Access",
      "progress_percentage": 100,
      "started_time": "2026-11-22T09:42:44.220454+00:00",
      "status": "SUCCEEDED"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:bdd07ab4-889b-4617-723f-ccedfb0416ad"

ext_id:
  description:
    - The external ID of the cluster whose SSH access control was
      updated.
  returned: always
  type: str
  sample: "00065ffe-0266-379f-0000-000000028f57"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped due to idempotency.
  returned: when module is idempotent
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any occurred.
  returned: When there is an error or when module is idempotent
  type: str
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_ssh_control_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_external_ssh_access_control,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        is_ssh_enabled=dict(type="bool", required=False),
        is_password_login_enabled=dict(type="bool", required=False),
    )
    return module_args


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    for key in ("ssh_access_inconsistency_details",):
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_external_ssh_access_control(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    if module.check_mode:
        sg = SpecGenerator(module)
        spec, err = sg.generate_spec(obj=clustermgmt_sdk.ExternalSshAccessControl())
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed generating update external SSH access control spec",
                **result,
            )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_external_ssh_access_control(module, api_instance, cluster_ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update external SSH access control spec",
            **result,
        )

    if check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating external SSH access control",
            **result,
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.update_external_ssh_access_control_by_cluster_id(
            clusterExtId=cluster_ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating external SSH access control",
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
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_ssh_control_api_instance(module)
    update_external_ssh_access_control(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
