#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vcenter_extension_v2
short_description: Register or unregister vCenter server extension in Nutanix Prism Central
description:
  - This module allows you to register or unregister a vCenter server extension.
  - Nutanix Prism requires registering vCenter Server extension keys to be able to perform VM Management and other operations.
  - This module uses PC v4 APIs based SDKs
version_added: "2.6.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Register vCenter server extension) -
      Operation Name: Register VCenter Extension -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Unregister vCenter server extension) -
      Operation Name: Unregister VCenter Extension -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - Specify state.
      - If C(state) is set to C(present) then the operation will register the vCenter extension.
      - If C(state) is set to C(absent) then the operation will unregister the vCenter extension.
    choices:
      - present
      - absent
    type: str
    default: present
  ext_id:
    description:
      - The globally unique identifier of vCenter Server extension instance. It should be of type UUID.
    type: str
    required: true
  username:
    description:
      - Username for vCenter Server extension registration/unregistration.
    type: str
    required: false
  password:
    description:
      - Password for vCenter Server extension registration/unregistration.
    type: str
    required: false
  port:
    description:
      - Port for vCenter Server extension registration/unregistration.
    type: int
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Register vCenter server extension
  nutanix.ncp.ntnx_vcenter_extension_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "<vcenter_extension_ext_id>"
    username: "<vcenter_username>"
    password: "<vcenter_password>"
    port: 443
    state: present

- name: Unregister vCenter server extension
  nutanix.ncp.ntnx_vcenter_extension_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "<vcenter_extension_ext_id>"
    username: "<vcenter_username>"
    password: "<vcenter_password>"
    port: 443
    state: absent
"""

RETURN = r"""
response:
  description:
    - The full API response for the vCenter extension operation.
    - Task details if C(wait) is false.
    - VCenter extension details if C(wait) is true.
  type: dict
  returned: always
  sample:
    {
      "cluster_ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
      "ext_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "ip_address": "10.0.0.1",
      "is_registered": true
    }
task_ext_id:
  description:
    - The external ID of the task.
  type: str
  returned: always
  sample: "ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1"
ext_id:
  description:
    - The external ID of the vCenter extension.
  type: str
  returned: always
  sample: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  returned: always
  type: str
  sample: null
msg:
  description: Status or error message.
  returned: contextual
  type: str
  sample: "vCenter extension registered successfully."
skipped:
  description: Message explaining why operation was skipped (e.g. idempotency).
  returned: when applicable
  type: str
  sample: "vCenter extension is already registered. Nothing to change."
failed:
  description: True on failure.
  returned: when something fails
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_vcenter_extensions_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_vcenter_extension  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
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
        ext_id=dict(type="str", required=True),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        port=dict(type="int", required=False),
    )
    return module_args


def _build_vcenter_credentials_spec(module):
    """
    Build VcenterCredentials spec from module params.
    Args:
        module: AnsibleModule instance
    Returns:
        VcenterCredentials spec object
    """
    cred = cluster_management_sdk.VcenterCredentials()
    if module.params.get("username"):
        cred.username = module.params["username"]
    if module.params.get("password"):
        cred.password = module.params["password"]
    if module.params.get("port") is not None:
        cred.port = module.params["port"]
    return cred


def _check_vcenter_extension_registered(module, api_instance, ext_id):
    """
    Check if the vCenter extension is already registered.
    Args:
        module: AnsibleModule instance
        api_instance: VcenterExtensionsApi instance
        ext_id (str): vCenter extension external ID
    Returns:
        bool: True if registered, False otherwise
        object: vCenter extension data if found, None otherwise
    """
    try:
        resp = api_instance.get_vcenter_extension_by_id(extId=ext_id)
        if resp and resp.data:
            data = resp.data
            if hasattr(data, "is_registered") and data.is_registered:
                return True, data
            return False, data
    except Exception:
        return False, None
    return False, None


def create_VcenterExtension(module, result, api_instance):
    """
    Register a vCenter server extension.
    Args:
        module: AnsibleModule instance
        result (dict): Module result dict
        api_instance: VcenterExtensionsApi instance
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_vcenter_credentials_spec(module)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    is_registered, current_data = _check_vcenter_extension_registered(
        module, api_instance, ext_id
    )
    if is_registered:
        result["skipped"] = (
            "vCenter extension is already registered. Nothing to change."
        )
        result["response"] = strip_internal_attributes(current_data.to_dict())
        module.exit_json(
            msg="vCenter extension is already registered. Nothing to change.", **result
        )

    resp = None
    try:
        resp = api_instance.register_vcenter_extension(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while registering vCenter extension",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp_data = get_vcenter_extension(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp_data.to_dict())

    result["changed"] = True


def delete_VcenterExtension(module, result, api_instance):
    """
    Unregister a vCenter server extension.
    Args:
        module: AnsibleModule instance
        result (dict): Module result dict
        api_instance: VcenterExtensionsApi instance
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    spec = _build_vcenter_credentials_spec(module)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "vCenter extension with ext_id '{0}' will be unregistered.".format(ext_id)
        )
        return

    is_registered, current_data = _check_vcenter_extension_registered(
        module, api_instance, ext_id
    )
    if not is_registered:
        result["skipped"] = "vCenter extension is not registered. Nothing to change."
        if current_data:
            result["response"] = strip_internal_attributes(current_data.to_dict())
        module.exit_json(
            msg="vCenter extension is not registered. Nothing to change.", **result
        )

    resp = None
    try:
        resp = api_instance.unregister_vcenter_extension(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unregistering vCenter extension",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp_data = get_vcenter_extension(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp_data.to_dict())

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
        "task_ext_id": None,
    }

    api_instance = get_vcenter_extensions_api_instance(module)

    state = module.params["state"]
    if state == "present":
        create_VcenterExtension(module, result, api_instance)
    else:
        delete_VcenterExtension(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
