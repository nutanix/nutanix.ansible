#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_key_management_server_v2
short_description: Create, update, and delete key management servers.
description:
  - This module allows you to create, update, and delete key management servers.
  - Key management server is used to secure encryption keys when data encryption is enabled.
  - This module uses PC v4 APIs based SDKs
version_added: "2.4.0"
options:
  state:
    description:
      - State of the key management server. Whether to create, update, or delete.
      - If C(state) is C(present) and C(ext_id) is not provided, create a new key management server.
      - If C(state) is C(present) and C(ext_id) is provided, update the key management server.
      - If C(state) is C(absent), and ext_id is provided, it will delete the key management server.
    type: str
    choices: ["present", "absent"]
  ext_id:
    description:
      - Key Management Server External ID.
      - Required for updating or deleting the key management server.
    type: str
    required: false
  name:
    description:
      - Key Management Server name.
      - Required for creating or updating the key management server.
    type: str
    required: false
  access_information:
    description:
      - Key Management Server access information.
      - Required for creating the key management server.
    type: dict
    required: false
    suboptions:
      azure_key_vault:
        description: Access information for the Azure Key Vault.
        type: dict
        suboptions:
          endpoint_url:
            description: Endpoint URL for the Azure Key Vault.
            type: str
            required: true
          key_id:
            description: Master key identifier for the Azure Key Vault.
            type: str
            required: true
          tenant_id:
            description: Tenant identifier for the Azure Key Vault.
            type: str
            required: true
          client_id:
            description:
              - Client identifier for the Azure Key Vault.
              - Not supported in the idempotency check.
            type: str
            required: true
          client_secret:
            description:
              - Client secret for the Azure Key Vault.
              - Not supported in the idempotency check.
            type: str
            required: true
          credential_expiry_date:
            description: When the client secret is going to expire.
            type: str
            required: true
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    required: false
    default: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create key management server
  nutanix.ncp.ntnx_key_management_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "Key_Management_Server_1"
    access_information:
      azure_key_vault:
        endpoint_url: "https://demo-keyvault-001.vault.azure.net/"
        key_id: "key_id"
        tenant_id: "d4c8a8e5-91b3-4f7e-8c2e-77d6f4a22f11"
        client_id: "e29f9c62-3e56-41d0-b123-7f8a22c0cdef"
        client_secret: "7Z3uQ~vO4trhXk8B5M9qjwgT1pR2uC9yD1zF0wX3"
        credential_expiry_date: "2026-09-01"

- name: Update key management server
  nutanix.ncp.ntnx_key_management_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
    name: "Key_Management_Server_1_Updated"
    access_information:
      azure_key_vault:
        endpoint_url: "https://demo-keyvault-001.vault.azure.net/"
        key_id: "key_id_updated"
        tenant_id: "d4c8a8e5-91b3-4f7e-8c2e-77d6f4a22f11"
        client_id: "e29f9c62-3e56-41d0-b123-7f8a22c0cdef"
        client_secret: "7Z3uQ~vO4trhXk8B5M9qjwgT1pR2uC9yD1zF0wX3"
        credential_expiry_date: "2026-09-01"

- name: Delete key management server
  nutanix.ncp.ntnx_key_management_server_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "13a6657d-fa96-49e3-7307-87e93a1fec3d"
"""

RETURN = r"""
response:
    description:
        - Response of key management server operations.
        - Key management server details if C(wait) is True and C(state) is present
        - Task details if C(wait) is False or C(state) is absent
    returned: always
    type: dict
    sample:
      {
        "access_information": {
            "client_id": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "client_secret": null,
            "credential_expiry_date": "2026-11-01",
            "endpoint_url": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "key_id": "********:707213e0523744d9ad27bc7d58efde0e",
            "tenant_id": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
            "truncated_client_secret": "0PJ"
        },
        "ext_id": "19595599-6719-4a2f-94b1-4cde1b84ce60",
        "links": null,
        "name": "ansible_test_GFMHxYZYEhIB",
        "tenant_id": null
      }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

ext_id:
  description: The External ID of the created Key Management Server
  returned: always
  type: str
  sample: "13a6657d-fa96-49e3-7307-87e93a1fec3d"

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

task_ext_id:
  description: The External ID of the task
  returned: always
  type: str
  sample: "13a6657d-fa96-49e3-7307-87e93a1fec3d"

skipped:
  description: This indicates whether the task was skipped
  returned: When current spec and update spec are identical
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Failed generating create Key Management Server Spec."

"""


import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_etag,
    get_kms_api_instance,
)
from ..module_utils.v4.security.helpers import get_kms_by_ext_id  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_security_py_client as security_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as security_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    access_information_obj_map = {
        "azure_key_vault": security_sdk.AzureAccessInformation,
    }

    azure_key_vault_spec = dict(
        endpoint_url=dict(type="str", required=True),
        key_id=dict(type="str", required=True),
        tenant_id=dict(type="str", required=True),
        client_id=dict(type="str", required=True),
        client_secret=dict(type="str", no_log=True, required=True),
        credential_expiry_date=dict(type="str", required=True),
    )

    access_information_spec = dict(
        azure_key_vault=dict(
            type="dict",
            options=azure_key_vault_spec,
            no_log=False,
        )
    )

    module_args = dict(
        name=dict(type="str"),
        ext_id=dict(type="str"),
        access_information=dict(
            type="dict",
            options=access_information_spec,
            obj=access_information_obj_map,
        ),
    )
    return module_args


def create_kms(module, kms_api_instance, result):

    sg = SpecGenerator(module)
    default_spec = security_sdk.KeyManagementServer()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Key Management Server Spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = kms_api_instance.create_key_management_server(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Key Management Server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.KMS
        )
        if ext_id:
            resp = get_kms_by_ext_id(module, kms_api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_kms_idempotency(old_spec, update_spec):
    old_spec = strip_internal_attributes(old_spec)
    update_spec = strip_internal_attributes(update_spec)
    # removing access information credentials from the spec since they are not supported in the idempotency check
    if old_spec.get("access_information"):
        old_spec["access_information"].pop("client_secret", None)
        old_spec["access_information"].pop("key_id", None)
        old_spec["access_information"].pop("truncated_client_secret", None)
    if update_spec.get("access_information"):
        update_spec["access_information"].pop("client_secret", None)
        update_spec["access_information"].pop("key_id", None)
        update_spec["access_information"].pop("truncated_client_secret", None)
    # converting credential expiry date to string
    old_spec["access_information"]["credential_expiry_date"] = str(
        old_spec["access_information"]["credential_expiry_date"]
    )
    update_spec["access_information"]["credential_expiry_date"] = str(
        update_spec["access_information"]["credential_expiry_date"]
    )
    if old_spec != update_spec:
        return False
    return True


def update_kms(module, kms_api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_kms_by_ext_id(module, kms_api_instance, ext_id)
    sg = SpecGenerator(module)
    default_spec = security_sdk.KeyManagementServer()
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating Key Management Server update spec", **result
        )
    # check for idempotency
    if check_kms_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating Key Management Server", **result
        )

    kwargs = {"if_match": etag}
    try:
        resp = kms_api_instance.update_key_management_server_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Key Management Server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_kms_by_ext_id(module, kms_api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_kms(module, kms_api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Key Management Server with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    try:
        resp = kms_api_instance.delete_key_management_server_by_id(
            extId=ext_id,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Key Management Server",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name",)),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_security_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    kms_api_instance = get_kms_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_kms(module, kms_api_instance, result)
        else:
            if not module.params.get("access_information"):
                module.fail_json(
                    msg="access_information is required when creating a key management server."
                )
            create_kms(module, kms_api_instance, result)
    else:
        delete_kms(module, kms_api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
