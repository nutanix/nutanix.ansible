#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_categories_v2
short_description: Associate or disassociate categories to a VM in AHV Nutanix.
description:
  - This module allows you to associate or disassociate categories to a AHV VM in Nutanix.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
options:
  categories:
    description:
      - List of categories to associate or disassociate with the VM.
      - For associating, module will only send categories which are not already associated with the VM.
      - For disassociating, module will only send categories which are already associated with the VM.
    type: list
    elements: dict
    suboptions:
      ext_id:
        description:
          - The external ID of the category.
        type: str
        required: true
    required: true
  vm_ext_id:
    description:
      - The external ID of the VM.
    type: str
    required: true
  state:
    description:
      - If set to "present", the categories will be associated with the VM.
      - If set to "absent", the categories will be disassociated from the VM.
    type: str
    choices: [present, absent]
    default: present
  wait:
    description:
      - Whether to wait for the operation to complete before returning.
    type: bool
    default: true
author:
    - Pradeepsingh Bhati (@bhati-pradeep)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Associate categories with a VM
  nutanix.ncp.ntnx_vms_categories_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    categories:
      - ext_id: bbc3555a-133b-5348-9764-bfff196e84e4
      - ext_id: e4bda88f-e5da-5eb1-a031-2c0bb00d923d
      - ext_id: 7bb4b92a-e6bd-5866-8ad4-8f3ab5886c33
    vm_ext_id: 8bb4b92a-e6bd-5866-8ad4-8f3ab5886c33
    state: present
    wait: true

- name: Disassociate categories from a VM
  nutanix.ncp.ntnx_vms_categories_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    categories:
      - ext_id: bbc3555a-133b-5348-9764-bfff196e84e4
      - ext_id: e4bda88f-e5da-5eb1-a031-2c0bb00d923d
    vm_ext_id: 8bb4b92a-e6bd-5866-8ad4-8f3ab5886c33
    state: absent
    wait: true
"""

RETURNS = r"""
response:
  description:
    - For wait=true, the response will be the list of categories associated with the VM.
    - For wait=false, the response will be the task response when triggered.
  type: list
  elements: str
  returned: always
  sample:[
            "eb8b4155-b3d1-5772-8d2f-d566d43d8e46",
            "4d552748-e119-540a-b06c-3c6f0d213fa2",
            "46f433d5-016d-5b11-a75f-5d0f44da7fd5",
            "cee7a9cc-3032-54bb-9eaf-a8205af52b7c"
        ],
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or module is idempotent
    type: str
    sample: "Api Exception raised while associating vm disk"
error:
    description: The error message if an error occurred.
    type: str
    returned: on error
    sample: "failed to associate categories with vm"
changed:
    description: Whether the state of the vm has changed.
    type: bool
    returned: always
    sample: true
skipped:
    description: Whether the operation is skipped due to no state change
    type: bool
    returned: on skipping
    sample: true
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
vm_ext_id:
    description: The external ID of the vm.
    type: str
    returned: always
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
"""


import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    reference_spec = dict(
        ext_id=dict(type="str", required=True),
    )
    module_args = dict(
        categories=dict(
            type="list",
            elements="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigCategoryReference,
            required=True,
        ),
        vm_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_vm_categories_uuid_list(module, api_instance, vm_ext_id):
    vm = get_vm(module, api_instance, vm_ext_id)
    categories = []
    if vm.categories is not None:
        for item in vm.categories:
            categories.append(item.ext_id)

    return categories


def associate_categories(module, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    # Remove already existing categories from list and create specs
    # create list of categories not associated in vm
    current_categories = get_vm_categories_uuid_list(module, vmm, vm_ext_id)
    add_categories = []
    for category in module.params.get("categories", []):
        ext_id = category.get("ext_id")
        if ext_id and ext_id not in current_categories:
            add_categories.append(vmm_sdk.AhvConfigCategoryReference(ext_id=ext_id))

    spec = vmm_sdk.AhvConfigAssociateVmCategoriesParams(categories=add_categories)

    if not spec.categories:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of vm current state
    vm = get_vm(module, vmm, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.associate_categories(extId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating vm disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        vm = get_vm(module, vmm, vm_ext_id)
        categories = vm.categories
        categories = [item.ext_id for item in categories]
        result["response"] = categories
    result["changed"] = True


def disassociate_categories(module, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    # Send categories from list which are actually associated to vm
    # this is to avoid failures from API due to non associated categories
    current_categories = get_vm_categories_uuid_list(module, vmm, vm_ext_id)
    remove_categories = []
    for category in module.params.get("categories", []):
        ext_id = category.get("ext_id")
        if ext_id and ext_id in current_categories:
            remove_categories.append(vmm_sdk.AhvConfigCategoryReference(ext_id=ext_id))

    spec = vmm_sdk.AhvConfigDisassociateVmCategoriesParams(categories=remove_categories)

    if not spec.categories:
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of vm current state
    vm = get_vm(module, vmm, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.disassociate_categories(extId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating vm disk",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        vm = get_vm(module, vmm, vm_ext_id)
        categories = vm.categories
        if categories is not None:
            categories = [item.ext_id for item in categories]
            result["response"] = categories
    result["changed"] = True


def run_module():
    module = BaseModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_vmm_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "vm_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        associate_categories(module, result)
    else:
        disassociate_categories(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
