#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_esxi_vms_assign_owner_v2
short_description: Assign owner of an ESXi VM in Nutanix Prism Central
description:
  - Assign the owner of an ESXi virtual machine.
  - This module uses PC v4 APIs based SDKs
version_added: "2.7.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Assign ESXi Virtual Machine Owner) -
      Required Roles: Prism Admin, Project Manager, Self-Service Admin (deprecated), Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
options:
  ext_id:
    description:
      - The external ID of the ESXi VM.
    type: str
    required: true
  owner:
    description:
      - Owner reference.
    type: dict
    required: true
    suboptions:
      entity_type:
        description:
          - Type of the entity that the owner reference is pointing to.
        type: str
        choices:
          - USER
      ext_id:
        description:
          - The globally unique identifier of an instance of type UUID.
        type: str
        required: true
  wait:
    description:
      - Wait for the assign-owner task to complete before returning.
    type: bool
    required: false
    default: true
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Assign owner of an ESXi VM
  nutanix.ncp.ntnx_esxi_vms_assign_owner_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "530567f3-abda-4913-b5d0-0ab6758ec165"
    owner:
      entity_type: USER
      ext_id: "00000000-0000-0000-0000-000000000000"
"""

RETURN = r"""
response:
  description:
    - Response details of the assign-owner operation.
    - When C(wait) is true the response is the VM info after owner assignment.
    - When C(wait) is false the response is the initial task reference returned by the assign-owner API.
  type: dict
  returned: always
  sample: {
            "ext_id": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
            "ownership_info": {
                "owner": {
                    "entity_type": "USER",
                    "ext_id": "00000000-0000-0000-0000-000000000000"
                }
            }
        }
ext_id:
  description: The external ID of the ESXi VM.
  type: str
  returned: always
  sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
task_ext_id:
  description: The external ID of the task.
  type: str
  returned: always
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
changed:
  description: This indicates whether the task resulted in any changes
  type: bool
  returned: always
  sample: true
skipped:
  description: This indicates whether the task was skipped
  type: bool
  returned: when the module is idempotent
  sample: true
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while assigning ESXi VM owner"
error:
  description: This indicates the error message if any error occurred
  type: str
  returned: when an error occurs
failed:
  description: This indicates whether the task failed
  type: bool
  returned: always
  sample: false
"""

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
from ..module_utils.v4.vmm.api_client import get_esxi_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    owner_reference_spec = dict(
        entity_type=dict(type="str", choices=["USER"]),
        ext_id=dict(type="str", required=True),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        owner=dict(
            type="dict",
            options=owner_reference_spec,
            obj=vmm_sdk.EsxiConfigOwnerReference,
            required=True,
        ),
    )
    return module_args


def _is_owner_change_needed(current_spec, module):
    """Check if the ESXi VM owner needs to be changed."""
    requested_owner_ext_id = module.params["owner"]["ext_id"]
    current_ownership = getattr(
        getattr(current_spec, "ownership_info", None), "owner", None
    )
    current_ext_id = getattr(current_ownership, "ext_id", None)
    return current_ext_id != requested_owner_ext_id


def assign_vm_owner(module, api_instance, result):
    """Assign a new owner to the ESXi VM."""
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.EsxiConfigOwnershipInfo()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ESXi VM assign owner spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "ESXi VM with ext_id:{0} will have owner assigned.".format(
            ext_id
        )
        return

    current_spec = get_vm(module, api_instance, ext_id)
    if not _is_owner_change_needed(current_spec, module):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    try:
        resp = api_instance.assign_vm_owner(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while assigning ESXi VM owner",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_vm(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

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
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "failed": False,
    }

    api_instance = get_esxi_vm_api_instance(module)
    assign_vm_owner(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
