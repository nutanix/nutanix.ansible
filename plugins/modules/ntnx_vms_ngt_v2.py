#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Pradeepsingh Bhati
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: ntnx_vms_ngt_v2
short_description: Install or uninstall Nutanix Guest Tools (NGT) on a VM.
description:
    - This module allows you to install or uninstall Nutanix Guest Tools (NGT) on a VM in a Nutanix cluster.
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
notes:
    - Module will skip if install/uninstall is not required checking the current installation status.
options:
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then module will install NGT on the VM.
            - if C(state) is set to C(absent) then module will uninstall NGT on the VM.
        choices:
            - present
            - absent
        type: str
        default: present
    wait:
        description: Wait for the operation to complete.
        type: bool
        required: false
        default: True
    ext_id:
        description:
            - The external ID of the VM on which to install or uninstall NGT.
        type: str
        required: true
    capabilities:
        description:
            - List of NGT capabilities to enable.
        type: list
        elements: str
        choices:
            - SELF_SERVICE_RESTORE
            - VSS_SNAPSHOT
    credential:
        description:
            - The credentials to authenticate with the VM.
        type: dict
        suboptions:
            username:
                description:
                    - The username for authentication.
                type: str
                required: true
            password:
                description:
                    - The password for authentication.
                type: str
                required: true
    reboot_preference:
        description:
            - The reboot preference for the VM after installing or uninstalling NGT.
        type: dict
        suboptions:
            schedule_type:
                description:
                    - The type of reboot schedule.
                type: str
                choices:
                    - IMMEDIATE
                    - SKIP
                    - LATER
                required: true
            schedule:
                description:
                    - The schedule for reboot.
                    - required when C(schedule_type) is LATER.
                type: dict
                suboptions:
                    start_time:
                        description:
                            - The start time for the reboot schedule.
                            - ISO 8601 format.
                        type: str
                        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Install NGT on a VM
  ntnx_vm_ngt_installation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    capabilities:
      - SELF_SERVICE_RESTORE
    credentials:
      username: "admin"
      password: "password"
    reboot_preference:
      schedule_type: "LATER"
      schedule:
        start_time: "2022-01-01T00:00:00Z"

- name: Uninstall NGT from a VM
  ntnx_vm_ngt_installation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    state: "absent"
"""

RETURN = r"""
response:
    description:
        - If C(wait) is true, It will show NGT configuration of VM after install or uninstall operation.
        - If C(wait) is false, It will show task status of NGT operation.
    type: dict
    returned: always
    sample:
        {
            "available_version": "4.1",
            "capabilities": [
                "VSS_SNAPSHOT"
            ],
            "guest_os_version": null,
            "is_enabled": true,
            "is_installed": false,
            "is_iso_inserted": true,
            "is_reachable": false,
            "is_vm_mobility_drivers_installed": null,
            "is_vss_snapshot_capable": null,
            "version": null
        }
task_ext_id:
    description: The external ID of the task associated with the NGT operation.
    type: str
    returned: when the task is created
changed:
    description: Indicates whether the NGT installation or uninstallation changed the state of the VM.
    type: bool
    returned: always
error:
    description: The error message, if any, encountered during the NGT operation.
    type: str
    returned: on error
ext_id:
    description: The external ID of the VM on which the NGT operation was performed.
    type: str
    returned: always
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_etag, get_vm_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_ngt_status  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    credential = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )
    schedule = dict(
        start_time=dict(type="str", required=True),
    )
    reboot_preference = dict(
        schedule_type=dict(
            type="str", choices=["IMMEDIATE", "SKIP", "LATER"], required=True
        ),
        schedule=dict(
            type="dict", options=schedule, obj=vmm_sdk.RebootPreferenceSchedule
        ),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        capabilities=dict(
            type="list",
            elements="str",
            choices=["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"],
        ),
        credential=dict(type="dict", options=credential, obj=vmm_sdk.Credential),
        reboot_preference=dict(
            type="dict", options=reboot_preference, obj=vmm_sdk.RebootPreference
        ),
    )
    return module_args


def install_ngt(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    if not ext_id:
        return module.fail_json(msg="ext_id is required to install NGT", **result)

    result["ext_id"] = ext_id

    status = get_ngt_status(module, vmm, ext_id)
    if getattr(status, "is_installed", False):
        result["skipped"] = True
        module.exit_json(msg="NGT is already installed in given vm.", **result)
    etag = get_etag(status)
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.GuestToolsInstallConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create install Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vmm.install_vm_guest_tools(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while installing NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        status = get_ngt_status(module, vmm, ext_id)
        result["response"] = strip_internal_attributes(status.to_dict())
    result["changed"] = True


def uninstall_ngt(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    if not ext_id:
        return module.fail_json(
            msg="vm ext_id is required to uninstalling NGT", **result
        )

    result["ext_id"] = ext_id

    status = get_ngt_status(module, vmm, ext_id)
    if not getattr(status, "is_installed", False):
        result["skipped"] = True
        module.exit_json(msg="NGT is already not installed in the given vm", **result)

    etag = get_etag(status)
    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.uninstall_vm_guest_tools(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uninstalling NGT",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        status = get_ngt_status(module, vmm, ext_id)
        result["response"] = strip_internal_attributes(status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
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
        "ext_id": None,
    }
    state = module.params["state"]
    if state == "present":
        install_ngt(module, result)
    else:
        uninstall_ngt(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
