#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_approval_policies_associate_v2
short_description: Associate secured policies with an approval policy
version_added: "2.7.0"
description:
    - Update the list of secured policies associated with an approval policy.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Associate Protection Policy) -
      Required Roles: Disaster Recovery Admin, Prism Admin, Secure Policy Disaster Recovery Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will associate secured policies with the approval policy.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID of the approval policy.
        type: str
        required: true
    secured_policies:
        description:
            - Specification of the configured approval policy.
            - List of secured policies to associate.
        type: list
        elements: dict
        required: true
        suboptions:
            policy_ext_id:
                description:
                    - External identifier of the policy associated with an approval policy.
                type: str
                required: true
            policy_type:
                description:
                    - Type of the policy to be protected by the approval policy.
                type: str
                choices:
                    - PROTECTION_POLICY
                required: true
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        default: true
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
- name: Associate protection policies with an approval policy
  nutanix.ncp.ntnx_approval_policies_associate_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "f19af988-ea11-46ca-8958-e8158d87383b"
    secured_policies:
      - policy_ext_id: "0985aafc-8cb8-4e22-b863-3ff5f91c911e"
        policy_type: PROTECTION_POLICY
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for associating secured policies.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    type: dict
    returned: always
    sample:
        {
            "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
            "status": "SUCCEEDED"
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
ext_id:
    description: The external ID of the approval policy.
    type: str
    returned: always
    sample: "f19af988-ea11-46ca-8958-e8158d87383b"
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode operation
    type: str
    sample: "Secured policies will be associated with the approval policy."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
"""

import traceback  # noqa: E402
import uuid  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_approval_policies_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_security_py_client as security_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as security_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    secured_policy_spec = dict(
        policy_ext_id=dict(type="str", required=True),
        policy_type=dict(type="str", required=True, choices=["PROTECTION_POLICY"]),
    )
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        secured_policies=dict(
            type="list",
            elements="dict",
            required=True,
            options=secured_policy_spec,
            obj=security_sdk.SecuredPolicy,
        ),
    )
    return module_args


def associate_policies(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = security_sdk.AssociatePoliciesSpec()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating associate policies Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = "Secured policies will be associated with the approval policy."
        return

    kwargs = {"NTNX-Request-Id": str(uuid.uuid4())}
    resp = None
    try:
        resp = api_instance.associate_policies(extId=ext_id, body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating secured policies",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    if SDK_IMP_ERROR:
        module = BaseModuleV4(
            argument_spec=get_module_spec(),
            supports_check_mode=True,
        )
        module.fail_json(
            msg=missing_required_lib("ntnx_security_py_client"),
            exception=SDK_IMP_ERROR,
        )

    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    api_instance = get_approval_policies_api_instance(module)
    associate_policies(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
