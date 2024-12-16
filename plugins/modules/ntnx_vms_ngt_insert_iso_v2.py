#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Pradeepsingh Bhati
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_vms_ngt_insert_iso_v2
short_description: Insert Nutanix Guest Tools (NGT) ISO into a virtual machine.
description:
    - This module allows you to insert the Nutanix Guest Tools (NGT) ISO into a virtual machine's available CD-ROM in Nutanix PC.
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of the virtual machine where the NGT ISO should be inserted.
        type: str
        required: true
    capabilities:
        description:
            - List of capabilities to enable for the NGT ISO.
            - Valid choices are "SELF_SERVICE_RESTORE" and "VSS_SNAPSHOT".
        type: list
        elements: str
        choices:
            - SELF_SERVICE_RESTORE
            - VSS_SNAPSHOT
    is_config_only:
        description:
            - Indicates that the Nutanix Guest Tools are already installed on the guest VM,
              and the ISO is being inserted to update the configuration of these tools.
        type: bool
        default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
- name: Insert NGT ISO into virtual machine
  ntnx_vm_ngt_insert_iso_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "98b9dc89-be08-3c56-b554-692b8b676fd1"
    capabilities:
      - SELF_SERVICE_RESTORE
      - VSS_SNAPSHOT
    is_config_only: false
"""

RETURNS = r"""
changed:
    description: Indicates whether the state of the system has changed.
    returned: always
    type: bool
error:
    description: Error message if an error occurred during the module execution.
    returned: on error
    type: str
response:
    description:
        - If C(wait) is true, It will show NGT configuration of VM after operation.
        - If C(wait) is false, It will show task status of NGT operation.
    returned: always
    type: dict
    sample: {
            "available_version": "4.1",
            "capabilities": [
                "SELF_SERVICE_RESTORE"
            ],
            "guest_os_version": "linux:64:CentOS Linux-7.3.1611",
            "is_enabled": true,
            "is_installed": true,
            "is_iso_inserted": true,
            "is_reachable": true,
            "is_vm_mobility_drivers_installed": null,
            "is_vss_snapshot_capable": null,
            "version": "4.1"
        }
ext_id:
    description: The external ID of the virtual machine.
    returned: always
    type: str
task_ext_id:
    description: The external ID of the task created for inserting the NGT ISO.
    returned: when the task is created
    type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

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
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        capabilities=dict(
            type="list",
            elements="str",
            choices=["SELF_SERVICE_RESTORE", "VSS_SNAPSHOT"],
        ),
        is_config_only=dict(type="bool", default=False),
    )
    return module_args


def insert_ngt_iso(module, result):
    vmm = get_vm_api_instance(module)
    ext_id = module.params.get("ext_id")
    if not ext_id:
        return module.fail_json(
            msg="vm ext_id is required to inserting NGT iso", **result
        )

    result["ext_id"] = ext_id

    status = vmm.get_guest_tools_by_id(extId=ext_id)
    etag = get_etag(status)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.GuestToolsInsertConfig()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating insert NGT iso spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = vmm.insert_vm_guest_tools(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while inserting NGT iso in vm",
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
    insert_ngt_iso(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
