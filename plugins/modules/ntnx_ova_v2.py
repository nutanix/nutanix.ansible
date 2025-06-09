#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
---
module: ntnx_ova_v2
short_description: "Create, Update and Delete Ova"
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
from copy import deepcopy  # noqa: E402

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
from ..module_utils.v4.vmm.api_client import get_etag, get_ova_api_instance # noqa: E402
from ..module_utils.v4.vmm.helpers import get_ova  # noqa: E402
from ..module_utils.v4.vmm.spec.vms import VmSpecs as vm_specs  # noqa: E402
from ..module_utils.v4.iam.spec.iam import UserSpecs as user_specs  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_vmm_py_client as vmm_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as vmm_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    checksum_allowed_types = {
        "ova_sha1_checksum": vmm_sdk.OvaSha1Checksum,
        "ova_sha256_checksum": vmm_sdk.OvaSha256Checksum,
    }
    source_allowed_types = {
        "ova_url_source": vmm_sdk.OvaUrlSource,
        "ova_vm_source": vmm_sdk.OvaVmSource,
        "objects_lite_source": vmm_sdk.ObjectsLiteSource,
    }
    ova_sha_checksum_spec = dict(
        hex_digest= dict(type="str", required=True),
    )
    checksum_spec = dict(
        ova_sha1_checksum=dict(
            type="dict", options=ova_sha_checksum_spec),
        ova_sha256_checksum=dict(
            type="dict", options=ova_sha_checksum_spec),
        )
    ova_url_source_spec = dict(
        url=dict(type="str", required=True),
        should_allow_insecure_url=dict(
            type="bool",
            default=False,
        ),
        basic_auth=dict(
            type="dict",
            options=dict(
                username=dict(type="str", required=True),
                password=dict(type="str", no_log=True, required=True),
            ),
        ),
    )
    disk_format_spec = dict(
        type="str",
        choices=["VMDK", "QCOW2"],
    )
    ova_vm_source_spec = dict(
        vm_ext_id=dict(type="str", required=True),
        disk_file_format= disk_format_spec,
    )
    objects_lite_source_spec = dict(
        key=dict(type="str", required=True),
    )
    source_spec = dict(
        ova_url_source=dict(
            type="dict",
            options=ova_url_source_spec,
        ),
        ova_vm_source=dict(
            type="dict",
            options=ova_vm_source_spec,
        ),
        objects_lite_source=dict(
            type="dict",
            options=objects_lite_source_spec,
        ),
    )

    module_args = dict(
        name= dict(type="str"), #Make this required for state present
        ext_id= dict(type="str"),
        checksum=dict(
            type="dict",
            options=checksum_spec,
            obj=checksum_allowed_types,
            mutually_exclusive=[("ova_sha1_checksum", "ova_sha256_checksum")],
        ),
        source=dict( #Make this required for create
            type="dict",
            options=source_spec,
            obj=source_allowed_types,
            mutually_exclusive=[
                ("ova_url_source", "ova_vm_source", "objects_lite_source")
            ],
        ),
        created_by=dict(
            type="dict",
            options=user_specs.get_users_spec().pop("ext_id", None),
            obj=vmm_sdk.User,
        ),
        cluster_location_ext_ids= dict(
            type="list",
            elements="str",
        ),
        vm_config=dict(
            type="dict",
            options=vm_specs.get_vm_spec().pop("ext_id", None),
            obj=vmm_sdk.AhvConfigVm,
        ),
        disk_format= disk_format_spec,
    )

    return module_args


def create_ova(module, ova, result):
    sg = SpecGenerator(module)
    default_spec = vmm_sdk.Ova()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create ova spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = ova.create_ova(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.OVA
        )
        if ext_id:
            resp = get_ova(module, ova, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_ova(module, ova, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_ova(module, ova, ext_id=ext_id)

    etag_value = get_etag(current_spec)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ova update spec", **result)

    # check for idempotency
    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = ova.update_ova_by_id(extId=ext_id, body=update_spec, if_match=etag_value)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating ova",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_ova(module, ova, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_ova(module, ova, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Ova with ext_id:{0} will be deleted.".format(ext_id)
        return

    resp = None
    try:
        resp = ova.delete_ova_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting ova",
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
        required_if=[
            (
                "state",
                "absent",
                ("ext_id",),
            ),
        ],
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
    state = module.params.get("state")
    ova = get_ova_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_ova(module, ova, result)
        else:
            create_ova(module, ova, result)
    else:
        delete_ova(module, ova, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
