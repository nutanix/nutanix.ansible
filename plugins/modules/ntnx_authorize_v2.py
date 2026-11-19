#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_authorize_v2
short_description: Authorize incoming requests
version_added: "2.7.0"
description:
    - Authorize incoming requests
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Authorize) -
      Required Roles: Super Admin, Prism Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will authorize incoming requests.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    x_ntnx_project:
        description:
            - Project header for the request.
        type: str
        required: false
    identity:
        description:
            - Object defining the attributes of Identity (who).
            - Optional when C(user_token) is supplied; if both are present, the user token takes precedence and this identity is ignored.
        type: dict
        required: false
        suboptions:
            identity_type:
                description:
                    - Type of identity object.
                type: str
                required: false
                choices:
                    - User
            attributes:
                description:
                    - Map of attributes for the Identity.
                type: dict
                required: false
    user_token:
        description:
            - Optional user JWT.
            - >-
              When present, the user UUID and group UUIDs are derived from the token claims and used as the identity
              for the authorization checks, overriding any identity supplied in the request body.
            - The token signature is not verified because this endpoint is reachable only over mTLS.
        type: str
        required: false
    request_list:
        description:
            - List of requests to be authorized.
        type: list
        elements: dict
        required: true
        suboptions:
            request_id:
                description:
                    - Unique qualifier of the request.
                type: str
                required: true
            response_type:
                description:
                    - Type of response expected.
                type: str
                required: false
                choices:
                    - BooleanResponse
                    - FilterResponse
            entity:
                description:
                    - Entity on which the action is being performed.
                type: dict
                required: true
                suboptions:
                    type:
                        description:
                            - Type of the entity.
                        type: str
                        required: true
                    operation:
                        description:
                            - Operation being performed on the entity.
                        type: str
                        required: true
                    attributes:
                        description:
                            - Map of attributes for the entity.
                        type: dict
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
- name: Authorize incoming requests
  nutanix.ncp.ntnx_authorize_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    identity:
      identity_type: User
      attributes:
        user_uuid: "00000000-0000-0000-0000-000000000001"
    request_list:
      - request_id: "req-1"
        response_type: BooleanResponse
        entity:
          type: "vm"
          operation: "view"
          attributes:
            cluster_uuid: "00000000-0000-0000-0000-000000000002"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for authorize.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "response": [
                {
                    "authorized": true,
                    "filters": null,
                    "message": null,
                    "request_id": "req-1",
                    "response_type": "BooleanResponse"
                }
            ]
        }

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while authorizing request"

task_ext_id:
    description: The external ID of the task.
    returned: always
    type: str
    sample: "ZXJnb24=:00000000-0000-0000-0000-000000000000"

ext_id:
    description: The external ID of the resource.
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_authorizations_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as iam_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as iam_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    identity_spec = dict(
        identity_type=dict(
            type="str",
            required=False,
            choices=["User"],
            obj=iam_sdk.IdentityType,
        ),
        attributes=dict(type="dict", required=False),
    )

    authorize_entity_spec = dict(
        type=dict(type="str", required=True),
        operation=dict(type="str", required=True),
        attributes=dict(type="dict", required=False),
    )

    request_object_spec = dict(
        request_id=dict(type="str", required=True),
        response_type=dict(
            type="str",
            required=False,
            choices=["BooleanResponse", "FilterResponse"],
            obj=iam_sdk.AuthzResponseType,
        ),
        entity=dict(
            type="dict",
            options=authorize_entity_spec,
            required=True,
            obj=iam_sdk.AuthorizeEntity,
        ),
    )

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        x_ntnx_project=dict(type="str", required=False),
        identity=dict(
            type="dict",
            options=identity_spec,
            required=False,
            obj=iam_sdk.IdentityObject,
        ),
        user_token=dict(type="str", required=False, no_log=True),
        request_list=dict(
            type="list",
            elements="dict",
            options=request_object_spec,
            required=True,
            obj=iam_sdk.RequestObject,
        ),
    )

    return module_args


def run_authorize(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.AuthorizationRequest()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating spec for authorize", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # Build kwargs for header
    kwargs = {}
    if module.params.get("x_ntnx_project"):
        kwargs["x_ntnx_project"] = module.params.get("x_ntnx_project")

    resp = None
    try:
        resp = api_instance.authorize(body=spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while authorizing request",
        )

    # resp is AuthorizeApiResponse, data contains AuthorizationResponse or ErrorResponse
    if resp and hasattr(resp, "data") and resp.data is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    elif resp:
        result["response"] = strip_internal_attributes(resp.to_dict())
    else:
        result["response"] = {}

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }

    api_instance = get_authorizations_api_instance(module)
    run_authorize(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
