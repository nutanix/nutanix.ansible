#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_prepare_encryption_keys_backup_v2
short_description: Prepare an encryption keys backup for cluster(s) in Nutanix Prism Central
description:
  - This module prepares the encryption key backup for the specified cluster(s) in Nutanix Prism Central.
  - This is an action module that triggers a task-based operation.
  - The prepared backup can later be downloaded using M(nutanix.ncp.ntnx_download_encryption_keys_backup_v2).
  - This module uses PC v4 APIs based SDKs.
version_added: 2.7.0
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Prepare encryption keys backup) -
    Required Roles: Prism Admin, Super Admin.
  - The referenced cluster(s) must exist and have software encryption enabled before preparing a backup.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  backup_password:
    description:
      - Password used to encrypt the encryption keys backup.
      - Required for the prepare backup operation.
    type: str
    required: false
  cluster_ext_ids:
    description:
      - List of cluster external IDs for which the encryption keys backup is prepared.
    type: list
    elements: str
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
- name: Prepare encryption keys backup for clusters
  nutanix.ncp.ntnx_prepare_encryption_keys_backup_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    backup_password: "Backup.Password.123"
    cluster_ext_ids:
      - "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for preparing the encryption keys backup.
    - Task details of the prepare backup operation.
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
      "operation": "PrepareEncryptionKeysBackup",
      "status": "SUCCEEDED"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: when applicable
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

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
  sample: "Api Exception raised while preparing encryption keys backup"
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
        backup_password=dict(type="str", required=False, no_log=True),
        cluster_ext_ids=dict(type="list", elements="str", required=False),
    )
    return module_args


def prepare_encryption_keys_backup(module, result, api_instance):
    validate_required_params(module, ["backup_password"])
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.EncryptionBackupSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating prepare encryption keys backup spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = True
        result["msg"] = "Encryption keys backup would be prepared. Check mode."
        return

    resp = None
    try:
        resp = api_instance.prepare_encryption_keys_backup(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while preparing encryption keys backup",
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
        "task_ext_id": None,
    }
    api_instance = get_encryption_api_instance(module)
    prepare_encryption_keys_backup(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
