#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_prechecks_v2
short_description: Perform LCM Prechecks
description:
    - This module allows you to perform LCM Prechecks.
version_added: "2.0.0"
author:
 - George Ghawali (@george-ghawali)
options:
    management_server:
        description:
            - Management server details.
        type: dict
        suboptions:
            hypervisor_type:
                description:
                    - Hypervisor type.
                type: str
                required: true
                choices:
                    - ESX
                    - AHV
                    - HYPERV
            ip:
                description:
                    - Management server IP.
                type: str
                required: true
            username:
                description:
                    - Management server username.
                type: str
                required: true
            password:
                description:
                    - Management server password.
                type: str
                required: true
    entity_update_specs:
        description:
            - List of entity update specs.
        type: list
        elements: dict
        required: true
        suboptions:
            entity_uuid:
                description:
                    - Entity UUID.
                type: str
                required: true
            to_version:
                description:
                    - To version.
                type: str
                required: true
    skipped_precheck_flags:
        description:
            - List of skipped precheck flags.
        type: list
        elements: str
        choices:
            - POWER_OFF_UVMS
    cluster_ext_id:
        description:
            - Cluster external ID.
        type: str
        required: true
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
    description: Response for performing LCM prechecks.
    type: dict
    returned: always
    sample:
        {}
task_ext_id:
    description: Task external ID.
    type: str
    returned: always
    sample: ZXJnb24=:f2efc360-5377-42d3-8e69-f5e3cd7d8f83
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_prechecks_api_instance  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    hypervisor_type_spec = dict(
        type="str",
        required=True,
        choices=["ESX", "AHV", "HYPERV"],
    )

    management_server_spec = dict(
        hypervisor_type=hypervisor_type_spec,
        ip=dict(type="str", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    module_args = dict(
        management_server=dict(
            type="dict",
            options=management_server_spec,
        ),
        entity_update_specs=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            required=True,
        ),
        skipped_precheck_flags=dict(
            type="list",
            elements="str",
            choices=["POWER_OFF_UVMS"],
        ),
        cluster_ext_id=dict(type="str", required=False),
    )

    return module_args


def lcm_prechecks(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    sg = SpecGenerator(module)
    default_spec = lifecycle_sdk.PrechecksSpec()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create LCM prechecks Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.perform_prechecks(X_Cluster_Id=cluster_ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while performing LCM prechecks",
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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "task_ext_id": None,
    }

    api_instance = get_prechecks_api_instance(module)

    lcm_prechecks(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
