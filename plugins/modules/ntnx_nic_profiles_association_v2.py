#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_nic_profiles_association_v2
short_description: Associate or disassociate host NICs with a NIC profile
version_added: 2.5.0
description:
  - This module associates or disassociates a host NIC with a NIC profile in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
options:
  state:
    description:
      - The state of the NIC profile association.
      - If C(present), the module will associate the host NIC with the NIC profile.
      - If C(absent), the module will disassociate the host NIC from the NIC profile.
    type: str
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the NIC profile.
    type: str
    required: true
  host_nic_ext_id:
    description:
      - The external identifier of the host NIC to associate or disassociate.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Associate host NIC with NIC profile
  nutanix.ncp.ntnx_nic_profiles_association_v2:
    state: present
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    host_nic_ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result
  ignore_errors: true

- name: Disassociate host NIC from NIC profile
  nutanix.ncp.ntnx_nic_profiles_association_v2:
    state: absent
    ext_id: "68e4c68e-1acf-4c05-7792-e062119acb68"
    host_nic_ext_id: "566b844b-d245-4894-a8b5-eeef1ec4b638"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description: Task response for associating or disassociating host NICs with a NIC profile.
  type: dict
  returned: always
task_ext_id:
  description: The external identifier of the task.
  type: str
  returned: always
ext_id:
  description: The external identifier of the NIC profile.
  type: str
  returned: always
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: When an error occurs
  type: str
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_nic_profiles_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        host_nic_ext_id=dict(type="str", required=True),
    )

    return module_args


def associate_host_nic(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.HostNic()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating host NIC spec for associating NIC profile.", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = nic_profiles.associate_host_nic_to_nic_profile(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating host NIC with NIC profile",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def disassociate_host_nic(module, nic_profiles, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.HostNic()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating host NIC spec for disassociating NIC profile.",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = nic_profiles.disassociate_host_nic_from_nic_profile(
            extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating host NIC from NIC profile",
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
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "error": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    state = module.params.get("state")
    nic_profiles = get_nic_profiles_api_instance(module)
    if state == "present":
        associate_host_nic(module, nic_profiles, result)
    else:
        disassociate_host_nic(module, nic_profiles, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
