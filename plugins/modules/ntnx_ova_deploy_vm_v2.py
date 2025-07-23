#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ova_deploy_vm_v2
short_description: "Deploy VM from an ova"
version_added: 2.2.1
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
 - Abhinav Bansal (@abhinavbansal29)
"""
EXAMPLES = r"""

"""
RETURN = r"""

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
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import ( # noqa: E402
    get_ova_api_instance,
    get_vm_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_vm  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402

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
        ext_id=dict(type="str"),
    )
    override_vm_config_spec = dict(
        name=dict(type="str"),
        num_sockets=dict(type="int"),
        num_cores_per_socket=dict(type="int"),
        num_threads_per_core=dict(type="int"),
        memory_size_bytes=dict(type="int"),
        nics=dict(
            type="list",
            elements="dict",
            options=vm_specs.get_nic_spec(),
            obj=vmm_sdk.AhvConfigNic,
            required=True,
        ),
        cd_roms=dict(
            type="list", elements="dict", options=vm_specs.get_cd_rom_spec(), obj=vmm_sdk.AhvConfigCdRom
        ),
        categories=dict(
            type="list",
            elements="dict",
            options=reference_spec,
            obj=vmm_sdk.AhvConfigCategoryReference,
        ),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        override_vm_config=dict(
            type="dict",
            options=override_vm_config_spec,
            obj=vmm_sdk.OvaVmConfigOverrideSpec,
            required=True,
        ),
        cluster_location_ext_id=dict(type="str", required=True),
    )

    return module_args


def deploy_vm_using_ova(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    ova = get_ova_api_instance(module)
    vm = get_vm_api_instance(module)

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.OvaDeploymentSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating deploy vm using ova spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = ova.deploy_ova(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deploying vm using ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        vm_ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.VM
        )
        if vm_ext_id:
            resp = get_vm(module, vm, vm_ext_id)
            result["vm_ext_id"] = vm_ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

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
        "task_ext_id": None,
    }
    deploy_vm_using_ova(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
