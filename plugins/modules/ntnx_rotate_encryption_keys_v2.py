#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_rotate_encryption_keys_v2
short_description: Rotate the encryption keys of a cluster in Nutanix Prism Central
description:
  - This module rotates the data-at-rest encryption keys on a cluster in Nutanix Prism Central.
  - This is an action module that triggers a task-based operation.
  - Key rotation can only be performed for the C(SOFTWARE) encryption type.
  - This module uses PC v4 APIs based SDKs.
version_added: 2.7.0
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Rotate encryption keys) -
    Required Roles: Prism Admin, Super Admin.
  - The referenced cluster must exist and have software encryption enabled before rotating keys.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the cluster whose encryption keys are to be rotated.
    type: str
    required: true
  encryption_types:
    description:
      - List of encryption types for which the keys are rotated.
      - Key rotation can be performed only for the C(SOFTWARE) encryption type.
      - Required for the rotate operation.
    type: list
    elements: str
    choices:
      - SOFTWARE
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
- name: Rotate encryption keys for a cluster
  nutanix.ncp.ntnx_rotate_encryption_keys_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
    encryption_types:
      - SOFTWARE
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for rotating the encryption keys of a cluster.
    - Task details of the rotate encryption keys operation.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": [
          "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
      ],
      "completed_time": "2026-09-18T06:26:51.524581+00:00",
      "created_time": "2026-09-18T06:26:47.167906+00:00",
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "operation": "RotateEncryptionKeys",
      "status": "SUCCEEDED"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the cluster whose encryption keys were rotated.
  returned: when applicable
  type: str
  sample: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"

changed:
  description: This indicates whether the action resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the action was skipped (e.g. in check mode).
  returned: when applicable
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
  returned: When there is an error or in check mode.
  type: str
  sample: "Api Exception raised while rotating encryption keys"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_encryption_api_instance,
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
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        encryption_types=dict(
            type="list",
            elements="str",
            choices=["SOFTWARE"],
            obj=clustermgmt_sdk.EncryptionType,
        ),
    )
    return module_args


def rotate_encryption_keys(module, result, api_instance):
    cluster_ext_id = module.params.get("ext_id")
    result["ext_id"] = cluster_ext_id
    validate_required_params(module, ["encryption_types"])

    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.EncryptionKeyRotationSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating rotate encryption keys spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = True
        result["msg"] = (
            "Encryption keys for cluster with ext_id:{0} would be rotated. "
            "Check mode.".format(cluster_ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.rotate_encryption_keys(
            clusterExtId=cluster_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while rotating encryption keys",
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
    api_instance = get_encryption_api_instance(module)
    rotate_encryption_keys(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
