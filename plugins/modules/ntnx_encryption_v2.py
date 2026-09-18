#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_encryption_v2
short_description: Configure data-at-rest encryption for a cluster in Nutanix Prism Central
description:
  - This module allows you to configure (update) the data-at-rest encryption configuration of a cluster in Nutanix Prism Central.
  - Encryption is configured per cluster and is identified by the cluster external ID.
  - This module uses PC v4 APIs based SDKs.
version_added: 2.7.0
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Update the encryption configuration of a cluster) -
    Required Roles: Prism Admin, Super Admin.
  - The cluster referenced by C(ext_id) must exist before configuring encryption.
  - Software encryption cannot be disabled once enabled on a cluster.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  ext_id:
    description:
      - The external ID of the cluster to configure encryption for.
      - Required for the update operation.
    type: str
    required: true
  type:
    description:
      - List of encryption types to enable on the cluster.
      - Required for update operation.
    type: list
    elements: str
    choices:
      - SOFTWARE
    required: false
  scope:
    description:
      - Scope at which the encryption is applied on the cluster.
    type: str
    choices:
      - CLUSTER
      - ENTITY
    required: false
  kms_spec:
    description:
      - Key Management Server (KMS) specification used for encryption.
    type: dict
    required: false
    suboptions:
      kms_type:
        description:
          - Type of the Key Management Server.
        type: str
        choices:
          - CLOUD
          - KMIP
          - NATIVE_LOCAL
          - NATIVE_REMOTE
        required: true
      external_kms_ext_ids:
        description:
          - List of external Key Management Server external IDs.
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
- name: Update encryption configuration of a cluster with all fields
  nutanix.ncp.ntnx_encryption_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
    type:
      - SOFTWARE
    scope: CLUSTER
    kms_spec:
      kms_type: NATIVE_LOCAL
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for configuring encryption for a cluster.
    - Encryption configuration details if C(wait) is true.
    - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
      "kms_spec": {
          "external_kms_ext_ids": null,
          "kms_type": "NATIVE_LOCAL"
      },
      "last_key_backup_time": null,
      "last_key_gen_time": "2026-09-18T06:26:47.167906+00:00",
      "scope": "CLUSTER",
      "type": [
          "SOFTWARE"
      ]
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the cluster whose encryption configuration was updated.
  returned: always
  type: str
  sample: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped due to idempotency.
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
  returned: When there is an error, the module is idempotent, or in check mode.
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
    get_encryption_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_encryption_config  # noqa: E402
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

    kms_spec = dict(
        kms_type=dict(
            type="str",
            required=True,
            choices=["CLOUD", "KMIP", "NATIVE_LOCAL", "NATIVE_REMOTE"],
            obj=clustermgmt_sdk.KmsType,
        ),
        external_kms_ext_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        type=dict(
            type="list",
            elements="str",
            choices=["SOFTWARE"],
            obj=clustermgmt_sdk.EncryptionType,
        ),
        scope=dict(
            type="str",
            choices=["CLUSTER", "ENTITY"],
            obj=clustermgmt_sdk.EncryptionScope,
        ),
        kms_spec=dict(
            type="dict",
            options=kms_spec,
            obj=clustermgmt_sdk.KmsSpec,
        ),
    )
    return module_args


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    # Read-only attributes that must not participate in idempotency check
    for key in ("last_key_gen_time", "last_key_backup_time"):
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_encryption(module, result, api_instance):
    cluster_ext_id = module.params.get("ext_id")
    result["ext_id"] = cluster_ext_id
    validate_required_params(module, ["type"])

    # In check mode, build the spec from a fresh object and return without any
    # API call (do not require the encryption config to already exist).
    if module.check_mode:
        sg = SpecGenerator(module)
        spec, err = sg.generate_spec(obj=clustermgmt_sdk.EncryptionConfig())
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed generating update encryption config spec", **result
            )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    old_spec = get_encryption_config(module, api_instance, cluster_ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating encryption config", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update encryption config spec", **result
        )

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_encryption_config(
            clusterExtId=cluster_ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating encryption config",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_encryption_config(module, api_instance, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("ext_id",)),
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
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_encryption_api_instance(module)
    update_encryption(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
