#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_protected_resources_v2
short_description: Module to promote or restore a protected resource in Nutanix Prism Central.
description:
  - This module can be used to promote or restore a protected resource in Nutanix Prism Central.
options:
  ext_id:
    description:
      - The external identifier of a protected VM or volume group used to retrieve the protected resource.
    type: str
    required: true
  cluster_ext_id:
    description:
      - The external identifier of the cluster on which the entity has valid restorable time ranges.
      - The restored entity is created on the same cluster.
    type: str
    required: false
  restore_time:
    description:
      - UTC date and time in ISO 8601 format representing the time from when the state of the entity should be restored.
      - This must be a valid time within the restorable time range(s) for the protected resource.
    type: str
    required: false
  wait:
    description:
      - Wait for the task to complete.
    type: bool
    required: false
    default: True
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import traceback  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_protected_resource_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_dataprotection_py_client as data_protection_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as data_protection_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str", required=False),
        restore_time=dict(type="str", required=False),
        wait=dict(type="bool", required=False, default=True),
    )
    return module_args


def restore_protected_resource(module, result):
    protected_resource = get_protected_resource_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    sg = SpecGenerator(module)
    default_spec = data_protection_sdk.ProtectedResourceRestoreSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating restore protected resource Spec", **result
        )
    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = protected_resource.restore_protected_resource(extId=ext_id, body=spec)

    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while restoring protected resource",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def promote_protected_resource(module, result):
    protected_resource = get_protected_resource_api_instance(module)
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    resp = None
    try:
        resp = protected_resource.promote_protected_resource(extId=ext_id)

    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while promoting protected resource",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
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
    }
    cluster_ext_id = module.params.get("cluster_ext_id")
    if cluster_ext_id:
        restore_protected_resource(module, result)
    else:
        promote_protected_resource(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
