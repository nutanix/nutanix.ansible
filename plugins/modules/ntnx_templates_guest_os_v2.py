#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_templates_guest_os_v2
short_description: Manage guest OS updates for Nutanix AHV templates.
description:
    - This module allows you to initiate, complete, or cancel guest OS updates for Nutanix AHV templates.
version_added: "2.0.0"
options:
    state:
        description:
            - The state of the guest OS update.
        type: str
        choices: ['start', 'cancel', 'finish']
        default: start
    template_ext_id:
        description:
            - The identifier of a Template.
            - requited for all states.
        type: str
        required: true
    version_id:
        description:
            - The identifier of a Template Version.
        type: str
        required: true
    version_name:
        description:
            - The user defined name of a Template Version.
            - required for finish state to complete guest OS update.
        type: str
    version_description:
        description:
            - The user defined description of a Template Version.
            - required for finish state to complete guest OS update.
        type: str
    is_active_version:
        description:
            - Specify whether to mark the Template Version as active or not.
              The newly created Version during Template Creation, updating
              or Guest OS updating is set to Active by default unless specified otherwise.
        type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: initiate_guest_os_update
  ntnx_templates_guest_os_v2:
    template_ext_id: "{{ template1_ext_id }}"
    version_id: "{{version1_ext_id}}"
    state: start
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: cancel guest_os_update
  ntnx_templates_guest_os_v2:
    template_ext_id: "{{ template1_ext_id }}"
    version_id: "{{version1_ext_id}}"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: cancel

- name: finish guest_os_update
  ntnx_templates_guest_os_v2:
    template_ext_id: "{{ template1_ext_id }}"
    version_id: "{{version1_ext_id}}"
    state: finish
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""

RETURN = r"""
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
from ..module_utils.v4.vmm.api_client import (  # noqa: E402
    get_etag,
    get_templates_api_instance,
)
from ..module_utils.v4.vmm.helpers import get_template  # noqa: E402

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
        state=dict(type="str", choices=["start", "cancel", "finish"], default="start"),
        template_ext_id=dict(type="str", required=True),
        version_id=dict(type="str", required=True),
        version_name=dict(type="str"),
        version_description=dict(type="str"),
        is_active_version=dict(type="bool"),
    )

    return module_args


def initiate_guest_os_update(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("template_ext_id")
    result["template_ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for initiate guest os update", **result
        )

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.InitiateGuestUpdateSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating initiate guest os update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Guest OS update will be initiated"
        return

    kwargs = {"if_match": etag}

    try:
        resp = templates.initiate_guest_update(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while initiating guest os update",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def complete_guest_os_update(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("template_ext_id")
    result["template_ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for complete guest os update", **result
        )

    sg = SpecGenerator(module)
    default_spec = vmm_sdk.CompleteGuestUpdateSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating complete guest os update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Guest OS update will be completed"
        return

    kwargs = {"if_match": etag}

    try:
        resp = templates.complete_guest_update(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while completing guest os update",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())

    result["changed"] = True


def cancel_guest_os_update(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("template_ext_id")
    result["template_ext_id"] = ext_id

    current_spec = get_template(module, templates, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for initiate guest os update", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = templates.cancel_guest_update(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while initiating guest os update",
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
    if state == "start":
        initiate_guest_os_update(module, result)
    elif state == "finish":
        complete_guest_os_update(module, result)
    else:
        cancel_guest_os_update(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
