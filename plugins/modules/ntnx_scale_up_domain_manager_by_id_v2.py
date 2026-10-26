#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scale_up_domain_manager_by_id_v2
short_description: Scale up a Domain Manager (Prism Central) cluster to a higher size
version_added: 2.7.0
description:
    - Scale up a Domain Manager (Prism Central) cluster to a higher
      configuration by specifying the desired C(size).
    - This is an action module backed by the PC v4
      C(POST /api/prism/v4.4/management/domain-managers/{extId}/$actions/scale-up)
      SDK call C(DomainManagerApi.scale_up_domain_manager_by_id).
    - This module uses PC v4 APIs based SDKs.
notes:
    - The module talks to the Domain Manager (Prism Central) itself and must
      be pointed at the PC endpoint, not a Prism Element.
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Scale up a Domain Manager) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin, Prism Admin, Super Admin
    - Scale up is a one-way operation; the target C(size) must be strictly
      larger than the current Prism Central size (for example
      C(SMALL) -> C(LARGE) -> C(EXTRALARGE)).
    - When C(dryrun) is set to C(true), the API only validates the request
      and reports a summary of the resulting system without actually scaling
      up the cluster.
    - When C(wait) is C(true) (default), the module blocks until the
      underlying async task finishes; set C(wait) to C(false) to return the
      C(task_ext_id) immediately.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=prism)"
options:
    state:
        description:
            - State of the module.
            - Only C(present) is supported — this action module triggers a
              one-shot scale-up operation.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - The external identifier of the domain manager (Prism Central)
              resource to scale up.
            - Can be discovered using M(nutanix.ncp.ntnx_domain_managers_info_v2)
              or M(nutanix.ncp.ntnx_pc_config_info_v2).
        type: str
        required: true
    size:
        description:
            - The desired Prism Central size to scale up to.
            - Must be a strictly larger size than the current PC size.
        type: str
        required: true
        choices:
            - SMALL
            - LARGE
            - EXTRALARGE
            - STARTER
    dryrun:
        description:
            - When C(true), the API executes in dry-run mode — it validates
              the request and reports what the resulting system would look
              like without actually scaling up the Prism Central.
            - When C(false) or omitted, the real scale-up operation is
              performed.
        type: bool
        required: false
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
- name: Scale up a Prism Central from SMALL to LARGE
  nutanix.ncp.ntnx_scale_up_domain_manager_by_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    size: "LARGE"
  register: scale_up_result

- name: Dry-run a Prism Central scale up to EXTRALARGE
  nutanix.ncp.ntnx_scale_up_domain_manager_by_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    size: "EXTRALARGE"
    dryrun: true
  register: scale_up_dryrun_result

- name: Trigger scale up without waiting for the task to complete
  nutanix.ncp.ntnx_scale_up_domain_manager_by_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
    size: "LARGE"
    wait: false
  register: scale_up_async_result
"""

RETURN = r"""
response:
    description:
        - Response for the Prism Central scale-up operation.
        - When C(wait) is C(true), it contains the final task details.
        - When C(wait) is C(false), it contains the initial task response.
        - In C(check_mode) or when C(dryrun) is C(true), it contains the
          scale-up request body / dry-run summary rather than a real task.
    returned: always
    type: dict
    sample:
        {
            "cluster_ext_ids": [
                "00062db6-57d1-7642-0000-00000000b71a"
            ],
            "completed_time": "2026-05-14T11:08:33.512544+00:00",
            "completion_details": null,
            "created_time": "2026-05-14T10:52:12.874110+00:00",
            "entities_affected": [
                {
                    "ext_id": "cfddac63-ffdb-4d9c-9a8c-54abf89ce234",
                    "name": "PC_10.44.76.25",
                    "rel": "prism:config:domain-manager"
                }
            ],
            "error_messages": null,
            "ext_id": "ZXJnb24=:7f8d3f3c-91b1-4b5b-8117-91c54b7bdd92",
            "is_background_task": false,
            "is_cancelable": false,
            "last_updated_time": "2026-05-14T11:08:33.512541+00:00",
            "legacy_error_message": null,
            "operation": "kPrismCentralScaleUpRequest",
            "operation_description": "Scale up Prism Central",
            "owned_by": {
                "ext_id": "00000000-0000-0000-0000-000000000000",
                "name": "admin"
            },
            "parent_task": null,
            "progress_percentage": 100,
            "started_time": "2026-05-14T10:52:13.001823+00:00",
            "status": "SUCCEEDED",
            "sub_steps": null,
            "sub_tasks": null,
            "warnings": null
        }

task_ext_id:
    description:
        - External ID of the task triggered by the scale-up action.
        - Not populated when the module runs in C(check_mode) because no
          API call is made.
    returned: when applicable
    type: str
    sample: "ZXJnb24=:7f8d3f3c-91b1-4b5b-8117-91c54b7bdd92"

ext_id:
    description: External ID of the Prism Central resource that was scaled up.
    returned: always
    type: str
    sample: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"

changed:
    description: Whether the scale-up action was executed on the cluster.
    returned: always
    type: bool
    sample: true

skipped:
    description:
        - Reason the action was skipped (for example when C(check_mode) is
          enabled, no actual API call is made).
    returned: when applicable
    type: str
    sample: "Scale up operation skipped in check_mode"

msg:
    description: Status or error message produced by the module.
    returned: When there is an error or a status needs to be surfaced
    type: str
    sample: "Api Exception raised while scaling up domain manager with ext_id: cfddac63-ffdb-4d9c-9a8c-54abf89ce234"

error:
    description:
        - Error details when the task fails.
        - C(None) on success.
    returned: always
    type: str
    sample: null

failed:
    description: Whether the module execution failed.
    returned: when something fails
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
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
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        size=dict(
            type="str",
            required=True,
            choices=["SMALL", "LARGE", "EXTRALARGE", "STARTER"],
            obj=prism_sdk.ManagementSize,
        ),
        dryrun=dict(type="bool", required=False),
    )
    return module_args


def scale_up_domain_manager(module, result, api_instance):
    """Trigger the ScaleUpDomainManagerById action on the given PC.

    Args:
        module: AnsibleModule instance.
        result: Result dict populated in-place.
        api_instance: DomainManagerApi SDK instance.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = prism_sdk.ScaleUpDomainManagerSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating scale up domain manager spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["skipped"] = "Scale up operation skipped in check_mode"
        return

    # Confirm the target Prism Central actually exists before issuing the
    # scale-up POST; this surfaces a clean "not found" error instead of a
    # confusing 4xx from the action endpoint when a bad ext_id is passed.
    get_pc_config(module, api_instance, ext_id)

    extra_kwargs = {}
    if module.params.get("dryrun") is not None:
        extra_kwargs["_dryrun"] = module.params.get("dryrun")

    try:
        resp = api_instance.scale_up_domain_manager_by_id(
            extId=ext_id, body=spec, **extra_kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while scaling up domain manager with ext_id: {0}".format(
                ext_id
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
