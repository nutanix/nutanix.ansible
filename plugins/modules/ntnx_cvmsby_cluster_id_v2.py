#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cvmsby_cluster_id_v2
short_description: Reconfigure Controller VMs (CVMs) associated with a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to reconfigure the vCPUs and memory allocated to
    the Controller VMs (CVMs) of a Nutanix cluster using Prism Central v4 APIs.
  - The reconfigure operation is applied to every CVM in the target cluster and
    is executed sequentially via a rolling task in Prism Central.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Reconfigure CVMs of a cluster) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - State of the module.
      - If state is present, the module will reconfigure the CVMs of the target cluster.
      - Delete is not supported for CVMs; C(state=absent) will fail.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose CVMs are to be reconfigured.
      - Required for the reconfigure operation.
    type: str
    required: true
  num_vcpus:
    description:
      - Target number of virtual CPUs to configure on every CVM of the cluster.
      - Must be a positive integer.
      - At least one of C(num_vcpus) or C(memory_size_bytes) must be provided.
    type: int
    required: false
  memory_size_bytes:
    description:
      - Target memory size in bytes to configure on every CVM of the cluster.
      - Must be a positive integer expressed in bytes (e.g. C(34359738368) for 32 GiB).
      - At least one of C(num_vcpus) or C(memory_size_bytes) must be provided.
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
- name: Reconfigure CVMs of a cluster - update vCPUs and memory
  nutanix.ncp.ntnx_cvmsby_cluster_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    num_vcpus: 12
    memory_size_bytes: 34359738368
  register: result
  ignore_errors: true

- name: Reconfigure CVMs of a cluster - update only vCPUs
  nutanix.ncp.ntnx_cvmsby_cluster_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    num_vcpus: 10
  register: result
  ignore_errors: true

- name: Reconfigure CVMs of a cluster - update only memory
  nutanix.ncp.ntnx_cvmsby_cluster_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    memory_size_bytes: 42949672960
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for reconfiguring CVMs in a cluster.
        - Task details if C(wait) is true.
        - Task submission details if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "0006361b-6855-3644-7458-2268f8ffb2bd"
            ],
            "completed_time": "2026-07-20T12:26:51.524581+00:00",
            "created_time": "2026-07-20T12:26:47.167906+00:00",
            "entities_affected": [
                {
                    "ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
                    "rel": "clustermgmt:config:cluster"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
            "is_cancelable": false,
            "last_updated_time": "2026-07-20T12:26:51.524581+00:00",
            "legacy_error_message": null,
            "operation": "ReconfigureCvms",
            "operation_description": "Reconfigure CVMs",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-07-20T12:26:47.185754+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: This indicates whether the reconfigure task resulted in any changes.
    returned: always
    type: bool
    sample: true

msg:
    description: Status/error message returned by the module.
    returned: When there is an error, or module is running in check mode
    type: str
    sample: "Api Exception raised while reconfiguring CVMs in cluster"

error:
    description: Error details when an API/SDK error is raised.
    returned: when an error occurs
    type: str
    sample: "Cluster ext_id is invalid"

failed:
    description: This field indicates whether the module failed.
    returned: always
    type: bool
    sample: false

task_ext_id:
    description: The external ID of the reconfigure task.
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"

ext_id:
    description:
        - The external ID (UUID) of the cluster on which the reconfigure operation was performed.
    returned: always
    type: str
    sample: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cvms_api_instance,
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
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        num_vcpus=dict(type="int", required=False),
        memory_size_bytes=dict(type="int", required=False),
    )
    return module_args


def reconfigure_cvms_by_cluster_id(module, result, api_instance):
    """Reconfigure the CVMs of a cluster using the Nutanix v4 API."""

    validate_required_params(module, ["cluster_ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    # At least one target attribute must be provided; a spec that does not
    # change anything is rejected by the platform, so guard for it up front.
    if (
        module.params.get("num_vcpus") is None
        and module.params.get("memory_size_bytes") is None
    ):
        module.fail_json(
            msg=(
                "At least one of 'num_vcpus' or 'memory_size_bytes' must be "
                "provided to reconfigure CVMs."
            ),
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.CvmReconfigurationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating CVM reconfiguration spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "CVMs of cluster ext_id:{0} will be reconfigured.".format(
            cluster_ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.reconfigure_cvms(clusterExtId=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while reconfiguring CVMs in cluster",
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
        required_one_of=[("num_vcpus", "memory_size_bytes")],
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
        "ext_id": None,
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_cvms_api_instance(module)
    reconfigure_cvms_by_cluster_id(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
