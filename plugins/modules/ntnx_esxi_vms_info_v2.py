#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_esxi_vms_info_v2
short_description: Fetch information about Nutanix ESXi based PC VMs
description:
  - This module fetches information about Nutanix ESXi based PC VMs.
  - The module can fetch information about all ESXi VMs or a specific ESXi VM.
  - This module uses PC v4 APIs based SDKs
version_added: "2.7.0"
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(View ESXi Virtual Machine) -
      Required Roles: Prism Admin, Prism Viewer, Project Manager, Self-Service Admin (deprecated),
      Super Admin, Storage Admin, Disaster Recovery Admin, Disaster Recovery Viewer, Backup Admin
    - >-
      B(View ESXi Virtual Machine) (List) -
      Required Roles: Prism Admin, Prism Viewer, Project Manager, Self-Service Admin (deprecated),
      Super Admin, Storage Admin, Backup Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=vmm)"
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
options:
    ext_id:
        description:
          - The external ID of the ESXi VM.
        type: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Fetch information about all ESXi VMs
  nutanix.ncp.ntnx_esxi_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Fetch information about a specific ESXi VM
  nutanix.ncp.ntnx_esxi_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "530567f3-abda-4913-b5d0-0ab6758ec165"

- name: List all ESXi VMs with fetch_all
  nutanix.ncp.ntnx_esxi_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    fetch_all: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching ESXi VMs info
    - Specific ESXi VM info if External ID is provided
    - List of multiple ESXi VMs info if External ID is not provided
  type: dict
  returned: always
  sample: {
            "ext_id": "9d199d16-1c8e-4ddf-40f5-20a2d78aa918",
            "name": "esxi-vm-1",
            "power_state": "OFF",
            "cluster": {
                "ext_id": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
            },
            "ownership_info": {
                "owner": {
                    "ext_id": "00000000-0000-0000-0000-000000000000"
                }
            },
            "categories": null,
            "links": null,
            "tenant_id": null
        }
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching ESXi VMs info"
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
changed:
  description: This indicates whether the task resulted in any changes
  type: bool
  returned: always
  sample: false
failed:
  description: This indicates whether the task failed
  type: bool
  returned: always
  sample: false
ext_id:
    description:
        - The external ID of the ESXi VM when a specific VM is fetched.
    type: str
    returned: when fetching a single VM
    sample: "530567f3-abda-4913-b5d0-0ab6758ec168"
total_available_results:
    description:
        - The total number of available ESXi VMs in PC.
    type: int
    returned: when all VMs are fetched
    sample: 125
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_esxi_vm_api_instance  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_vm(module, result):
    vmm = get_esxi_vm_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = vmm.get_vm_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VM info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vms(module, result):
    vmm = get_esxi_vm_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ESXi VMs info Spec", **result)

    try:
        resp = list_entities(
            vmm.list_vms,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ESXi VMs info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    if resp is None or getattr(resp, "data", None) is None:
        result["response"] = []
    else:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    if module.params.get("ext_id"):
        get_vm(module, result)
    else:
        get_vms(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
