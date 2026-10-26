#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scale_up_domain_manager_by_id_v2
short_description: Scale up a domain manager (Prism Central) cluster to a higher configuration
version_added: 2.7.0
description:
    - Scale up a domain manager (Prism Central) cluster to a higher configuration.
    - A size change is a task-driven async operation that resizes the domain
      manager (Prism Central) cluster to the requested size (STARTER, SMALL,
      LARGE or EXTRALARGE).
    - This module targets the domain manager (Prism Central) itself; use
      C(nutanix_host) with a PC endpoint.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Scale up a domain manager (Prism Central) cluster to a higher configuration) -
      Required Roles: Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - The target endpoint for this module is the domain manager (Prism Central), not Prism Element / FCVM.
    - The target size MUST be strictly larger than the currently deployed size;
      scaling down is not supported by the API. Supplying the same size the
      cluster is already running at will be surfaced as an API error by the
      backend.
    - Scaling is an async, long-running operation. The returned C(task_ext_id)
      can be polled with M(nutanix.ncp.ntnx_pc_tasks_info_v2).
    - The target domain manager extId can be discovered using
      M(nutanix.ncp.ntnx_pc_config_info_v2).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    state:
        description:
            - State of the module.
            - If state is C(present), the module will trigger the scale-up action.
            - This module does not support state C(absent).
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the domain manager (Prism Central)
              resource to scale up.
            - Can be fetched with M(nutanix.ncp.ntnx_pc_config_info_v2).
        type: str
        required: true
    size:
        description:
            - Target domain manager (Prism Central) size.
            - Must be strictly larger than the currently deployed size.
        type: str
        required: true
        choices:
            - STARTER
            - SMALL
            - LARGE
            - EXTRALARGE
    dryrun:
        description:
            - When set to C(true) the request is executed in dry-run mode.
            - In dry-run mode the backend validates the request and returns a
              summary snapshot of the resultant system without actually
              performing the scale-up.
        type: bool
        required: false
        default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Scale up a domain manager (Prism Central) cluster to SMALL
  nutanix.ncp.ntnx_scale_up_domain_manager_by_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    size: SMALL
  register: scale_up_result

- name: Scale up a domain manager (Prism Central) cluster to LARGE in dry-run mode
  nutanix.ncp.ntnx_scale_up_domain_manager_by_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    size: LARGE
    dryrun: true
  register: scale_up_dryrun_result
"""

RETURN = r"""
response:
    description:
        - Response for the scale-up domain manager (Prism Central) operation.
        - Task details if C(wait) is true (default).
        - Submitted task reference payload if C(wait) is false.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00062cd6-e034-fd28-185b-ac1f6b6f97e2"
            ],
            "completed_time": "2026-02-14T04:36:21.321654+00:00",
            "completion_details": null,
            "created_time": "2026-02-14T04:21:03.144201+00:00",
            "entities_affected": [
                {
                    "ext_id": "cfddac63-ffdb-4d9c-9a8c-54abf89ce234",
                    "name": "PC_10.44.76.25",
                    "rel": "prism:config:domain_manager"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:7f12d1b0-19c6-4e8e-86b2-6f1d4a4d0b19",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-02-14T04:36:21.321648+00:00",
            "legacy_error_message": null,
            "number_of_entities_affected": 1,
            "number_of_subtasks": 0,
            "operation": "kDomainManagerScaleUp",
            "operation_description": "Scale up Prism Central",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "root_task": null,
            "started_time": "2026-02-14T04:21:03.158772+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

changed:
    description: Whether the scale-up action was executed and resulted in any changes.
    returned: always
    type: bool
    sample: true

task_ext_id:
    description: External ID of the async task created by the scale-up operation.
    returned: when the API accepts the request
    type: str
    sample: "ZXJnb24=:7f12d1b0-19c6-4e8e-86b2-6f1d4a4d0b19"

ext_id:
    description: External ID of the domain manager (Prism Central) that was scaled up.
    returned: always
    type: str
    sample: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"

skipped:
    description: Reason the action was skipped (e.g., when running in check_mode).
    returned: when the action is skipped
    type: str
    sample: "scale-up skipped because the module is running in check_mode."

msg:
    description: Status / error message surfaced to the user.
    returned: When applicable
    type: str
    sample: "Api Exception raised while scaling up domain manager with ext_id: cfddac63-ffdb-4d9c-9a8c-54abf89ce234"

error:
    description: Error details when the task fails.
    returned: always
    type: str
    sample: null

failed:
    description: Indicates whether the task failed.
    returned: when the task fails
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_prism_py_client as prism_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as prism_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Return the Ansible argument spec for the scale-up domain manager
    (Prism Central) action module.

    The spec mirrors the ``ScaleUpDomainManagerSpec`` request body documented in
    the Prism v4 SDK plus the ``extId`` path parameter and the optional
    ``_dryrun`` query parameter exposed by ``ScaleUpDomainManagerById``.
    """
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        size=dict(
            type="str",
            required=True,
            choices=["STARTER", "SMALL", "LARGE", "EXTRALARGE"],
        ),
        dryrun=dict(type="bool", required=False, default=False),
    )
    return module_args


def _build_scale_up_spec(module, result):
    """
    Build the ``ScaleUpDomainManagerSpec`` request body from the module params.

    Args:
        module: Ansible module instance.
        result: Running result dict (populated with the generated error, if any).

    Returns:
        The SDK ``ScaleUpDomainManagerSpec`` instance ready to be sent to the
        API, or ``None`` if spec generation failed (``module.fail_json`` is
        called inside this helper on failure).
    """
    sg = SpecGenerator(module)
    default_spec = prism_sdk.ScaleUpDomainManagerSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating scale up domain manager spec", **result)
    return spec


def scale_up_domain_manager(module, result, api_instance):
    """
    Trigger the ``ScaleUpDomainManagerById`` SDK call for the configured
    domain manager (Prism Central) and record the resulting task metadata on
    ``result``.

    Supports ``check_mode`` by returning the generated spec without hitting
    the API, and supports the ``_dryrun`` query parameter via the module
    option ``dryrun``.
    """
    ext_id = module.params.get("ext_id")
    dryrun = module.params.get("dryrun")
    result["ext_id"] = ext_id

    spec = _build_scale_up_spec(module, result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = (
            "scale-up skipped because the module is running in check_mode."
        )
        return

    resp = None
    try:
        resp = api_instance.scale_up_domain_manager_by_id(
            extId=ext_id,
            body=spec,
            _dryrun=dryrun,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while scaling up domain manager with "
                "ext_id: {0}".format(ext_id)
            ),
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_prism_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_domain_manager_api_instance(module)
    scale_up_domain_manager(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
