#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
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
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_vg_api_instance,
)

SDK_IMP_ERROR = None
try:
    import ntnx_volumes_py_client as volumes_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as volumes_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    categories_spec = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        uris=dict(type="list", elements="str"),
        entity_type=dict(
            type="str",
            choices=[
                "VOLUME_GROUP",
                "ROUTING_POLICY",
                "DIRECT_CONNECT_VIF",
                "AVAILABILITY_ZONE",
                "STORAGE_CONTAINER",
                "VPC",
                "VPN_CONNECTION",
                "VOLUME_DISK",
                "VPN_GATEWAY",
                "IMAGE",
                "CATEGORY",
                "RECOVERY_PLAN",
                "CLUSTER",
                "DISK_RECOVERY_POINT",
                "CONSISTENCY_GROUP",
                "VIRTUAL_NIC",
                "TASK",
                "VIRTUAL_SWITCH",
                "VIRTUAL_NETWORK",
                "NODE",
                "FLOATING_IP",
                "SUBNET",
                "VM_DISK",
                "VTEP_GATEWAY",
                "VM",
                "DIRECT_CONNECT",
                "SUBNET_EXTENSION",
            ],
        ),
    )
    module_args = dict(
        ext_id=dict(type="str", required=True),
        categories=dict(
            type="list",
            elements="dict",
            options=categories_spec,
            obj=volumes_sdk.EntityReference,
        ),
    )

    return module_args


def associate_categories(module, vgs, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume group category spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vgs.associate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def disassociate_categories(module, vgs, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = volumes_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume group category spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = vgs.disassociate_category(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_volumes_py_client"), exception=SDK_IMP_ERROR
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
    vgs = get_vg_api_instance(module)
    if state == "present":
        associate_categories(module, vgs, result)
    else:
        disassociate_categories(module, vgs, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
