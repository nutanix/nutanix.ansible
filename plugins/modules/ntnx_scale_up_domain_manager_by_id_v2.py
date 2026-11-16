#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scale_up_domain_manager_by_id_v2
short_description: Scale up a Domain Manager (Prism Central) cluster to a higher size
version_added: "2.7.0"
description:
    - Scale up a Domain Manager (Prism Central) cluster to a higher
      configuration by specifying the desired C(size).
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to
      the user performing the operation.
    - >-
      B(Scale up a Domain Manager) -
      Required Roles: Cluster Admin, Domain Manager Admin, Internal Super Admin,
      Prism Admin, Super Admin
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
        type: str
        required: true
    size:
        description:
            - The desired size for the Domain Manager cluster after the scale-up operation. The value should be greater than or equal to current size.
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
    returned: always
    type: dict
    sample:
        {
            "ext_id": "ZXJnb24=:7f8d3f3c-91b1-4b5b-8117-91c54b7bdd92",
            "operation": "kPrismCentralScaleUpRequest",
            "operation_description": "Scale up Prism Central",
            "progress_percentage": 100,
            "status": "SUCCEEDED"
        }

task_ext_id:
    description:
        - The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:7f8d3f3c-91b1-4b5b-8117-91c54b7bdd92"
ext_id:
    description:
        - The external ID of the domain manager.
    returned: always
    type: str
    sample: "cfddac63-ffdb-4d9c-9a8c-54abf89ce234"
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
failed:
    description: This indicates whether the task failed
    returned: always
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Api Exception raised while scaling up domain manager"
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
    """Trigger the ScaleUpDomainManagerById action on the given PC."""
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
        return

    # Confirm the target Prism Central exists before issuing the scale-up POST.
    get_pc_config(module, api_instance, ext_id)

    kwargs = {}
    if module.params.get("dryrun") is not None:
        kwargs["_dryrun"] = module.params.get("dryrun")

    try:
        resp = api_instance.scale_up_domain_manager_by_id(
            extId=ext_id, body=spec, **kwargs
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
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_domain_manager_api_instance(module)
    scale_up_domain_manager(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
