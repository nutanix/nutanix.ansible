#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_object_store_profile_v2
short_description: Create and update object store profiles for a Nutanix Files file server
version_added: 2.6.0
description:
  - This module allows you to create and update object store profiles (tiering profiles) for a Nutanix Files file server in Nutanix Prism Central.
  - An object store profile defines the S3/Azure object store backend used by Nutanix Files Smart Tiering.
  - If C(ext_id) is not provided, a new object store profile is created.
  - If C(ext_id) is provided, the existing object store profile is updated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module does not support deletion because the Nutanix Files v4 API does not expose a delete operation for object store profiles.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the object store profile.
      - If C(state) is C(present) and C(ext_id) is not provided, a new object store profile is created.
      - If C(state) is C(present) and C(ext_id) is provided, the existing object store profile is updated.
    type: str
    choices:
      - present
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server that owns the object store profile.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - The external identifier of the object store profile.
      - Required for the update operation.
    type: str
    required: false
  name:
    description:
      - Object store cloud profile name.
      - Required for the create operation.
      - Maximum 80 characters.
    type: str
    required: false
  object_store_type:
    description:
      - Type of the object store backend used for tiering.
      - Required for the create operation.
    type: str
    required: false
    choices:
      - AWS
      - AWS_GLACIER_IR
      - AWS_STANDARD_IA
      - AZURE
      - AZURE_COOL
      - GCP
      - NUTANIX
      - OTHER
  mount_target_ext_ids:
    description:
      - List of mount target (share) external identifiers that should be included in the tiering profile.
    type: list
    elements: str
    required: false
  mount_targets_enablement_type:
    description:
      - Controls which mount targets of the file server are enabled for tiering with this profile.
    type: str
    required: false
    choices:
      - ALL_CURRENT_FUTURE_MOUNT_TARGETS
      - ALL_CURRENT_MOUNT_TARGETS
      - ALL_FUTURE_MOUNT_TARGETS
      - NONE
  retention_period_days:
    description:
      - Indicates time in days for which the data will be maintained in the cloud after it is deleted from the local storage on the file server.
      - Minimum value is 0. The API default is 1825 days.
    type: int
    required: false
  is_ssl_peer_verfication_enabled:
    description:
      - Enable SSL verify peer certificate for the object store connection.
    type: bool
    required: false
  object_store_config:
    description:
      - Object store connection and credential configuration for the tiering profile.
      - Required for the create operation.
    type: dict
    required: false
    suboptions:
      base_url:
        description:
          - Base URL of the object store endpoint.
          - Required when C(object_store_config) is provided.
        type: str
        required: false
      ca_cert_content:
        description:
          - CA certificate content used to validate the object store endpoint.
        type: str
        required: false
      proxy_server:
        description:
          - HTTP proxy server configuration used to reach the object store.
        type: dict
        required: false
        suboptions:
          url:
            description:
              - HTTP proxy server URL.
            type: str
            required: false
          credential:
            description:
              - Credentials used to authenticate with the proxy server.
            type: dict
            required: false
            suboptions:
              username:
                description:
                  - Name of the user for the proxy server.
                  - Maximum 256 characters.
                type: str
                required: false
              password:
                description:
                  - Password of the user for the proxy server.
                type: str
                required: false
      configuration:
        description:
          - AWS/Azure configuration for the tiering profile.
          - Provide C(aws) for AWS/NUTANIX/GCP/OTHER object store types and C(azure) for Azure object store types.
          - Required when C(object_store_config) is provided.
        type: dict
        required: false
        suboptions:
          aws:
            description:
              - AWS (or S3-compatible) configuration for the tiering profile.
            type: dict
            required: false
            suboptions:
              access_key:
                description:
                  - Access key for the object store.
                  - Required when C(aws) is provided.
                  - Maximum 1024 characters.
                type: str
                required: false
              secret_key:
                description:
                  - Secret key for the object store.
                  - Maximum 1024 characters.
                type: str
                required: false
              bucket_name:
                description:
                  - Bucket name.
                  - Minimum 3 and maximum 63 characters.
                type: str
                required: false
              bucket_location:
                description:
                  - Bucket location (region).
                  - Maximum 2048 characters.
                type: str
                required: false
          azure:
            description:
              - Azure configuration for the tiering profile.
            type: dict
            required: false
            suboptions:
              storage_account_name:
                description:
                  - Storage account name for Azure.
                  - Required when C(azure) is provided.
                  - Minimum 3 and maximum 24 characters.
                type: str
                required: false
              storage_account_key:
                description:
                  - Storage account key for Azure.
                  - Maximum 1024 characters.
                type: str
                required: false
              container_name:
                description:
                  - Container name for Azure.
                  - Minimum 3 and maximum 63 characters.
                type: str
                required: false
  recovery_object_store_config:
    description:
      - Recovery object store connection and credential configuration for the tiering profile.
      - This has the same structure as C(object_store_config).
    type: dict
    required: false
    suboptions:
      base_url:
        description:
          - Base URL of the recovery object store endpoint.
          - Required when C(recovery_object_store_config) is provided.
        type: str
        required: false
      ca_cert_content:
        description:
          - CA certificate content used to validate the recovery object store endpoint.
        type: str
        required: false
      proxy_server:
        description:
          - HTTP proxy server configuration used to reach the recovery object store.
        type: dict
        required: false
        suboptions:
          url:
            description:
              - HTTP proxy server URL.
            type: str
            required: false
          credential:
            description:
              - Credentials used to authenticate with the proxy server.
            type: dict
            required: false
            suboptions:
              username:
                description:
                  - Name of the user for the proxy server.
                  - Maximum 256 characters.
                type: str
                required: false
              password:
                description:
                  - Password of the user for the proxy server.
                type: str
                required: false
      configuration:
        description:
          - AWS/Azure configuration for the recovery object store.
          - Provide C(aws) for AWS/NUTANIX/GCP/OTHER object store types and C(azure) for Azure object store types.
          - Required when C(recovery_object_store_config) is provided.
        type: dict
        required: false
        suboptions:
          aws:
            description:
              - AWS (or S3-compatible) configuration for the recovery object store.
            type: dict
            required: false
            suboptions:
              access_key:
                description:
                  - Access key for the recovery object store.
                  - Required when C(aws) is provided.
                  - Maximum 1024 characters.
                type: str
                required: false
              secret_key:
                description:
                  - Secret key for the recovery object store.
                  - Maximum 1024 characters.
                type: str
                required: false
              bucket_name:
                description:
                  - Bucket name.
                  - Minimum 3 and maximum 63 characters.
                type: str
                required: false
              bucket_location:
                description:
                  - Bucket location (region).
                  - Maximum 2048 characters.
                type: str
                required: false
          azure:
            description:
              - Azure configuration for the recovery object store.
            type: dict
            required: false
            suboptions:
              storage_account_name:
                description:
                  - Storage account name for Azure.
                  - Required when C(azure) is provided.
                  - Minimum 3 and maximum 24 characters.
                type: str
                required: false
              storage_account_key:
                description:
                  - Storage account key for Azure.
                  - Maximum 1024 characters.
                type: str
                required: false
              container_name:
                description:
                  - Container name for Azure.
                  - Minimum 3 and maximum 63 characters.
                type: str
                required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Create AWS object store profile
  nutanix.ncp.ntnx_files_object_store_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "0006abcd-1111-2222-3333-444455556666"
    name: "tiering_profile_ansible"
    object_store_type: "AWS"
    mount_targets_enablement_type: "ALL_CURRENT_MOUNT_TARGETS"
    mount_target_ext_ids:
      - "b0df3e22-a3a3-4b86-8f09-ec9e1f3e8dc2"
    retention_period_days: 1825
    is_ssl_peer_verfication_enabled: true
    object_store_config:
      base_url: "https://s3.us-east-1.amazonaws.com/"
      configuration:
        aws:
          access_key: "AKIAEXAMPLEACCESSKEY"
          secret_key: "wJalrXUtnFEMIEXAMPLESECRETKEY"
          bucket_name: "files-tiering-bucket"
          bucket_location: "us-east-1"
  register: result
  ignore_errors: true

- name: Update object store profile
  nutanix.ncp.ntnx_files_object_store_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    file_server_ext_id: "0006abcd-1111-2222-3333-444455556666"
    ext_id: "1e4e557e-a53e-4d2f-b2d6-a1da4ccf2430"
    name: "tiering_profile_ansible_updated"
    object_store_type: "AWS"
    mount_targets_enablement_type: "ALL_CURRENT_FUTURE_MOUNT_TARGETS"
    retention_period_days: 3650
    is_ssl_peer_verfication_enabled: false
    object_store_config:
      base_url: "https://s3.us-east-1.amazonaws.com/"
      configuration:
        aws:
          access_key: "AKIAEXAMPLEACCESSKEY"
          secret_key: "wJalrXUtnFEMIEXAMPLESECRETKEY"
          bucket_name: "files-tiering-bucket"
          bucket_location: "us-east-1"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or updating the object store profile.
    - If the operation is create or update and C(wait) is true, it will return the object store profile details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "1e4e557e-a53e-4d2f-b2d6-a1da4ccf2430",
      "name": "tiering_profile_ansible",
      "object_store_type": "AWS",
      "mount_targets_enablement_type": "ALL_CURRENT_MOUNT_TARGETS",
      "mount_target_ext_ids": ["b0df3e22-a3a3-4b86-8f09-ec9e1f3e8dc2"],
      "retention_period_days": 1825,
      "is_ssl_peer_verfication_enabled": true,
      "object_store_config": {
          "base_url": "https://s3.us-east-1.amazonaws.com/",
          "ca_cert_content": null,
          "configuration": {
              "access_key": "AKIAEXAMPLEACCESSKEY",
              "bucket_location": "us-east-1",
              "bucket_name": "files-tiering-bucket"
          },
          "proxy_server": null
      },
      "recovery_object_store_config": null,
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the object store profile.
  returned: always
  type: str
  sample: "1e4e557e-a53e-4d2f-b2d6-a1da4ccf2430"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency
  returned: always
  type: bool
  sample: false

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
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_etag,
    get_tier_api_instance,
)
from ..module_utils.v4.files.helpers import get_object_store_profile  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as files_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Read-only attributes populated by the platform that must not be sent back on update.
READ_ONLY_FIELDS = ["ext_id", "links", "tenant_id"]


def get_object_store_config_spec():
    """Build the argument spec for an object store configuration block."""

    credential_spec = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
    )

    proxy_server_spec = dict(
        url=dict(type="str"),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=files_sdk.Credential,
        ),
    )

    aws_config_spec = dict(
        access_key=dict(type="str", no_log=True),
        secret_key=dict(type="str", no_log=True),
        bucket_name=dict(type="str"),
        bucket_location=dict(type="str"),
    )

    azure_config_spec = dict(
        storage_account_name=dict(type="str"),
        storage_account_key=dict(type="str", no_log=True),
        container_name=dict(type="str"),
    )

    configuration_obj_map = {
        "aws": files_sdk.AWSConfig,
        "azure": files_sdk.AzureConfig,
    }

    configuration_spec = dict(
        aws=dict(type="dict", options=aws_config_spec),
        azure=dict(type="dict", options=azure_config_spec),
    )

    object_store_config_spec = dict(
        base_url=dict(type="str"),
        ca_cert_content=dict(type="str"),
        proxy_server=dict(
            type="dict",
            options=proxy_server_spec,
            obj=files_sdk.ProxyServer,
        ),
        configuration=dict(
            type="dict",
            options=configuration_spec,
            obj=configuration_obj_map,
            mutually_exclusive=[("aws", "azure")],
        ),
    )
    return object_store_config_spec


def get_module_spec():
    object_store_config_spec = get_object_store_config_spec()

    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
        name=dict(type="str"),
        object_store_type=dict(
            type="str",
            choices=[
                "AWS",
                "AWS_GLACIER_IR",
                "AWS_STANDARD_IA",
                "AZURE",
                "AZURE_COOL",
                "GCP",
                "NUTANIX",
                "OTHER",
            ],
            obj=files_sdk.ObjectStoreType,
        ),
        mount_target_ext_ids=dict(type="list", elements="str"),
        mount_targets_enablement_type=dict(
            type="str",
            choices=[
                "ALL_CURRENT_FUTURE_MOUNT_TARGETS",
                "ALL_CURRENT_MOUNT_TARGETS",
                "ALL_FUTURE_MOUNT_TARGETS",
                "NONE",
            ],
            obj=files_sdk.MountTargetsEnablementType,
        ),
        retention_period_days=dict(type="int"),
        is_ssl_peer_verfication_enabled=dict(type="bool"),
        object_store_config=dict(
            type="dict",
            options=object_store_config_spec,
            obj=files_sdk.ObjectStoreConfig,
        ),
        recovery_object_store_config=dict(
            type="dict",
            options=deepcopy(object_store_config_spec),
            obj=files_sdk.ObjectStoreConfig,
        ),
    )
    return module_args


def create_object_store_profile(module, result, tier_api):
    file_server_ext_id = module.params.get("file_server_ext_id")
    validate_required_params(
        module, ["name", "object_store_type", "object_store_config"]
    )

    sg = SpecGenerator(module)
    default_spec = files_sdk.ObjectStoreProfile()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create object store profile spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = tier_api.create_object_store_profile(
            fileServerExtId=file_server_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating object store profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.OBJECT_STORE_PROFILE
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_object_store_profile(
                module, tier_api, file_server_ext_id, ext_id
            )
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get object store profile ext_id from task"
                ),
                msg="Failed to get object store profile ext_id from task",
            )
    result["changed"] = True


def check_object_store_profile_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    return old_spec == update_spec


def update_object_store_profile(module, result, tier_api):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_object_store_profile(module, tier_api, file_server_ext_id, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating object store profile", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update object store profile spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_object_store_profile_idempotency(
        old_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = tier_api.update_object_store_profile_by_id(
            fileServerExtId=file_server_ext_id, extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating object store profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_object_store_profile(module, tier_api, file_server_ext_id, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"),
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
    tier_api = get_tier_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_object_store_profile(module, result, tier_api)
        else:
            create_object_store_profile(module, result, tier_api)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
