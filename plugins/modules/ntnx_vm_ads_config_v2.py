#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_ads_config_v2
short_description: Update ADS configuration of a VM
version_added: "2.7.0"
description:
    - Update the ADS configuration of a virtual machine.
    - Controls how Acropolis Dynamic Scheduler treats the VM with respect to automatic migrations.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update the ADS configuration of a Virtual Machine) -
      Required Roles: Prism Admin, Project Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the ADS configuration of the VM.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    vm_ext_id:
        description:
            - A globally unique identifier of a VM of type UUID.
        type: str
        required: true
    auto_migration:
        description:
            - Whether the Acropolis Dynamic Scheduler is allowed to automatically migrate this VM.
        type: str
        choices:
            - INCLUDE
            - EXCLUDE
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
- name: Update VM ADS config
  nutanix.ncp.ntnx_vm_ads_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    auto_migration: "INCLUDE"
  register: result

- name: Update VM ADS config to exclude from auto migration
  nutanix.ncp.ntnx_vm_ads_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: "00000000-0000-0000-0000-000000000001"
    auto_migration: "EXCLUDE"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating VM ADS configuration.
        - If C(wait) is true, it will contain the ADS config details after completion.
        - If C(wait) is false, it will contain the task details.
    returned: always
    type: dict
    sample:
        {
            "auto_migration": "INCLUDE",
            "ext_id": "00000000-0000-0000-0000-000000000001",
            "links": null,
            "tenant_id": null
        }
task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:05b0b0c4-c1a2-5630-9db5-460e5239eef5"
ext_id:
    description: The external ID of the VM
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000001"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
skipped:
    description: This indicates whether the task was skipped
    returned: when module is idempotent
    type: bool
    sample: false
error:
    description: This indicates the error message if any error occurred
    returned: when an error occurs
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

import copy  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm_ads_config  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

READ_ONLY_FIELDS = ["ext_id", "links", "tenant_id"]

def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        vm_ext_id=dict(type="str", required=True),
        auto_migration=dict(
            type="str",
            choices=["INCLUDE", "EXCLUDE", "UNKNOWN", "REDACTED"],
            obj=vmm_sdk.AutoMigration,
        ),
    )
    return module_args


def check_vm_ads_config_idempotency(current_spec, update_spec):
    current_dict = strip_internal_attributes(current_spec.to_dict())
    update_dict = strip_internal_attributes(update_spec.to_dict())
    # Remove read-only fields before comparison
    for key in READ_ONLY_FIELDS:
        current_dict.pop(key, None)
        update_dict.pop(key, None)
    return current_dict == update_dict


def update_vm_ads_config(module, result, api_instance):
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = vm_ext_id

    current_spec = get_vm_ads_config(module, api_instance, vm_ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=copy.deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update VM ADS config spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_vm_ads_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag_value = get_etag(data=current_spec)
    kwargs = {}
    if etag_value:
        kwargs["if_match"] = etag_value

    resp = None
    try:
        resp = api_instance.update_vm_ads_config(
            vmExtId=vm_ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating VM ADS config",
        )

    task_ext_id = None
    if resp and resp.data:
        task_ext_id = getattr(resp.data, "ext_id", None)
        result["task_ext_id"] = task_ext_id
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated = get_vm_ads_config(module, api_instance, vm_ext_id)
        result["response"] = strip_internal_attributes(updated.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vm_api_instance(module)
    update_vm_ads_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
