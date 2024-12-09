#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_serial_port_v2
version_added: "2.0.0"
description:
    - This module allows you to manage serial port for Nutanix AHV VMs.
short_description: VM Serial Port module which supports VM serial port CRUD states
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then the operation will be  create the item.
            - if C(state) is set to C(present) and C(ext_id) is given then it will update that serial port.
            - if C(state) is set to C(present) then C(ext_id) or C(name) needs to be set.
            - >-
                If C(state) is set to C(absent) and if the item exists, then
                item is removed.
        choices:
            - present
            - absent
        type: str
        default: present
    ext_id:
        description:
            - The external ID of the serial port.
            - Required for updating or deleting a serial port.
        type: str
        required: false

    vm_ext_id:
        description:
            - The external ID of the VM.
        type: str
        required: true
    index:
        description:
            - Index of the serial port.
        type: int
    is_connected:
        description:
            - Indicates whether the serial port is connected or not.
        type: bool
author:
 - Prem Karat (@premkarat)
 - Alaa Bishtawi (@alaa-bish)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Create Serial Port
  ntnx_vms_serial_port_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: '{{ vm_ext_id }}'
    state: present
    index: 0
    is_connected: true

- name: Update Serial Port connection status
  ntnx_vms_serial_port_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vm_ext_id: '{{ vm_ext_id }}'
    ext_id: '{{ result.response.0.ext_id }}'
    state: present
    is_connected: false

- name: Delete Serial Port
  ntnx_vms_serial_port_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "dded1b87-e566-419a-aac0-fb282792fb83"
    vm_ext_id: "dded1b87-e566-419a-aac0-fb282792fb83"
"""

RETURN = r"""
response:
  description:
    - when wait is false, the response will be task status.
    - The response from the Nutanix PC VMM Serial Port v4 API.
    - it can be single serial port or list of serial ports as per spec.
  type: dict
  returned: always
  sample:
                {
                "ext_id": "dded1b87-e566-419a-aac0-fb282792fb83",
                "index": 0,
                "is_connected": true,
                "links": null,
                "tenant_id": null
            }
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
vm_ext_id:
    description: The external ID of the vm.
    type: str
    returned: always
    sample: "dded1b87-e566-419a-aac0-fb282792fb83"
ext_id:
    description:
        - The external ID of the Serial Port when specific serial port is fetched.
    type: str
    returned: always
    sample: "dded1b87-e566-419a-aac0-fb282792fb83"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    wait_for_completion,
    wait_for_entity_ext_id_in_task,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_serial_port, get_vm  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        is_connected=dict(type="bool"),
        index=dict(type="int"),
        vm_ext_id=dict(type="str", required=True),
    )

    return module_args


def create_serial_port(module, result):
    vmm = get_vm_api_instance(module)
    vm_ext_id = module.params["vm_ext_id"]
    result["vm_ext_id"] = vm_ext_id

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.SerialPort()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create vm serial port Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # get etag of vm current state
    vm = get_vm(module, vmm, vm_ext_id)
    etag = get_etag(vm)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.create_serial_port(vmExtId=vm_ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating vm serial port",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id, err = wait_for_entity_ext_id_in_task(
            module, task_ext_id, rel=TASK_CONSTANTS.RelEntityType.SERIAL_PORT
        )
        if err:
            result["error"] = err
            module.fail_json(msg="Failed to get serial port ID from task", **result)
        if ext_id:
            resp = get_serial_port(module, vmm, ext_id, vm_ext_id=vm_ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_serial_port(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["ext_id"] = ext_id
    result["vm_ext_id"] = vm_ext_id

    current_spec = get_serial_port(
        module, api_instance=vmm, ext_id=ext_id, vm_ext_id=vm_ext_id
    )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating vm serial port update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = vmm.update_serial_port_by_id(
            vmExtId=vm_ext_id, extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating vm serial port",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    # poll for the last unfinished task
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_serial_port(module, vmm, ext_id, vm_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_serial_port(module, result):
    ext_id = module.params.get("ext_id")
    vm_ext_id = module.params.get("vm_ext_id")
    result["vm_ext_id"] = vm_ext_id
    result["ext_id"] = ext_id

    vmm = get_vm_api_instance(module)
    serial_port = get_serial_port(module, vmm, ext_id, vm_ext_id=vm_ext_id)
    etag = get_etag(serial_port)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.delete_serial_port_by_id(vmExtId=vm_ext_id, extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting vm serial port",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[("state", "absent", ("ext_id",))],
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
        "ext_id": None,
        "vm_ext_id": None,
    }
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_serial_port(module, result)
        else:
            create_serial_port(module, result)
    else:
        delete_serial_port(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
