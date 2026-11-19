#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_install_external_storage_driver_by_cluster_id_v2
short_description: Install external storage driver on a cluster
version_added: "2.7.0"
description:
    - Install external storage driver on a Nutanix cluster using the cluster external ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the
      user performing the operation.
    - >-
      B(Install External Storage Driver) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster.
    type: str
    required: true
  key:
    description:
      - Object storage key of the driver package.
    type: str
    required: true
  version:
    description:
      - Version of the external storage driver.
    type: str
  provider_type:
    description:
      - Provider type for external storage.
    type: str
    choices: ['DELL_POWERFLEX', 'EVERPURE_FLASHARRAY', 'DELL_POWERSTORE', 'NETAPP_STORAGE', 'LENOVO_STORAGE', 'BLOCK_STORAGE_NVME']
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    default: true
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
- name: Install external storage driver on a cluster
  nutanix.ncp.ntnx_install_external_storage_driver_by_cluster_id_v2:
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    key: "my-driver-key"
    version: "1.0.0"
    provider_type: "DELL_POWERFLEX"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for install external storage driver on a nutanix cluster using the cluster external id.
    - If C(wait) is true, it will contain the final task payload after completion.
    - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
        "ext_id": "ZXJnb24=:fc0f5074-4da9-5593-bfdc-a08c13df963d",
        "status": "SUCCEEDED"
    }
task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
ext_id:
  description:
    - The external ID of the resource.
  returned: always
  type: str
  sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while performing operation"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_config_api_instance,
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
    from ..module_utils.v4.sdk_mock import mock_sdk as cluster_management_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        key=dict(type="str", required=True, no_log=False),
        version=dict(type="str"),
        provider_type=dict(
            type="str",
            choices=[
                "DELL_POWERFLEX",
                "EVERPURE_FLASHARRAY",
                "DELL_POWERSTORE",
                "NETAPP_STORAGE",
                "LENOVO_STORAGE",
                "BLOCK_STORAGE_NVME",
            ],
        ),
    )
    return module_args


def run_action(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.ExternalStorageDriverSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for Install External Storage Driver", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict()) if spec else {}
        return

    try:
        resp = api_instance.install_external_storage_driver_by_cluster_id(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing install external storage driver",
        )

    task_ext_id = resp.data.ext_id if resp.data else None
    if task_ext_id:
        result["task_ext_id"] = task_ext_id
    result["response"] = (
        strip_internal_attributes(resp.data.to_dict()) if resp.data else {}
    )
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True
    for key in ["ext_id", "cluster_ext_id", "host_ext_id"]:
        if module.params.get(key):
            result["ext_id"] = module.params.get(key)
            break


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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_cluster_config_api_instance(module)
    run_action(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
