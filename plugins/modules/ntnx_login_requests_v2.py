#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_login_requests_v2
short_description: Create, update, and delete login requests in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete login requests in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create login request) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Update login request) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete login request) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create login request.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update login request.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete login request.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the login request.
      - Required for update and delete operations.
    type: str
    required: false
  client_id:
    description:
      - Client identifier for the login request.
    type: str
    required: false
  response_type:
    description:
      - Response type for the login request.
    type: str
    required: false
    choices:
      - ID_TOKEN
      - CODE
      - TOKEN
  scope:
    description:
      - Supported scope values for the login request. The supported values are OPENID, PROFILE, EMAIL, OFFLINE_ACCESS and GROUPS. OPENID is a mandatory field.
    type: list
    elements: str
    required: false
    choices:
      - OPENID
      - PROFILE
      - EMAIL
      - OFFLINE_ACCESS
      - GROUPS
  redirect_uri:
    description:
      - Redirect URI for the login request.
    type: str
    required: false
  nonce:
    description:
      - Nonce value for the login request.
    type: str
    required: false
  oauth_state:
    description:
      - State value for the login request (OAuth state parameter).
    type: str
    required: false
  audience:
    description:
      - Audience value for the login request.
    type: str
    required: false
  approval_prompt:
    description:
      - Approval prompt value for the login request.
    type: str
    required: false
  login_provider_id:
    description:
      - Identifier for the login provider to be updated in the login request.
    type: str
    required: false
  is_user_logged_in:
    description:
      - Flag to determine if the user is logged in or not.
    type: bool
    required: false
  is_service_provider_enabled:
    description:
      - Flag to determine if service provider is enabled or not.
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
- name: Create login request
  nutanix.ncp.ntnx_login_requests_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    client_id: "9a53c903-ba26-588b-ac0f-f8ab26f5a6b0"
    response_type: "CODE"
    scope:
      - OPENID
    redirect_uri: "https://10.44.76.17:9440"
    nonce: "test-nonce"
    oauth_state: "test-state"
    audience: "test-audience"
    approval_prompt: "auto"
    is_user_logged_in: false
    is_service_provider_enabled: false
  register: result
  ignore_errors: true

- name: Update login request
  nutanix.ncp.ntnx_login_requests_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "22222222-2222-2222-2222-222222222222"
    login_provider_id: "37f30135-455b-5ebd-995f-b47e817a59f2"
  register: result
  ignore_errors: true

- name: Delete login request
  nutanix.ncp.ntnx_login_requests_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "22222222-2222-2222-2222-222222222222"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting login request
    - If the operation is create or update and C(wait) is true, it will return the login request details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "approval_prompt": null,
      "audience": null,
      "client_id": "9a53c903-ba26-588b-ac0f-f8ab26f5a6b0",
      "ext_id": "fc8b3c56-e66c-5e7c-9988-2e45bfe85569",
      "is_service_provider_enabled": false,
      "is_user_logged_in": false,
      "links": null,
      "login_provider_id": "37f30135-455b-5ebd-995f-b47e817a59f2",
      "nonce": null,
      "redirect_uri": "https://10.44.76.17:9440",
      "response_type": "CODE",
      "scope": [
        "OPENID"
      ],
      "state": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the login request.
  returned: always
  type: str
  sample: "22222222-2222-2222-2222-222222222222"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: when module is idempotent
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: always
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while creating login request"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_login_requests_api_instance,
)
from ..module_utils.v4.iam.helpers import get_login_request  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as identity_and_access_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as identity_and_access_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        client_id=dict(type="str"),
        response_type=dict(
            type="str",
            choices=["ID_TOKEN", "CODE", "TOKEN"],
        ),
        scope=dict(
            type="list",
            elements="str",
            choices=["OPENID", "PROFILE", "EMAIL", "OFFLINE_ACCESS", "GROUPS"],
        ),
        redirect_uri=dict(type="str"),
        nonce=dict(type="str"),
        oauth_state=dict(type="str"),
        audience=dict(type="str"),
        approval_prompt=dict(type="str"),
        login_provider_id=dict(type="str"),
        is_user_logged_in=dict(type="bool"),
        is_service_provider_enabled=dict(type="bool"),
    )
    return module_args


def create_login_request(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = identity_and_access_management_sdk.LoginRequest()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create login request spec", **result)

    # Manual mapping for oauth_state -> state due to collision with module operation state
    # SpecGenerator would incorrectly map operation state (present/absent) to LoginRequest.state
    if module.params.get("oauth_state") is not None:
        spec.state = module.params.get("oauth_state")
    elif getattr(spec, "state", None) in ["present", "absent"]:
        spec.state = None

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_login_request(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating login request",
        )
    if resp and resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if hasattr(resp.data, "ext_id") and resp.data.ext_id:
            result["ext_id"] = resp.data.ext_id
        # handle task case if response is task
        if hasattr(resp.data, "ext_id") and resp.data.ext_id:
            # check if task
            ext_id_val = resp.data.ext_id
            if ext_id_val and ext_id_val.startswith("ZXJnb24"):
                result["task_ext_id"] = ext_id_val
    result["changed"] = True


def check_login_request_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    # Remove read-only and server-populated fields
    for key in [
        "ext_id",
        "links",
        "tenant_id",
        "_reserved",
        "_object_type",
        "_unknown_fields",
    ]:
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_login_request(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    old_spec = get_login_request(module, api_instance, ext_id)
    # Sanitize empty string login_provider_id from old_spec (API returns "" but expects UUID or null)
    if getattr(old_spec, "login_provider_id", None) == "":
        old_spec.login_provider_id = None
    etag = get_etag(data=old_spec)
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update login request spec", **result)

    # Manual mapping for oauth_state -> state
    if module.params.get("oauth_state") is not None:
        update_spec.state = module.params.get("oauth_state")
    elif getattr(update_spec, "state", None) in ["present", "absent"]:
        # retain original state if not intended to change
        update_spec.state = getattr(old_spec, "state", None)

    # Sanitize login_provider_id: empty string fails regex validation
    if getattr(update_spec, "login_provider_id", None) == "":
        update_spec.login_provider_id = None

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_login_request_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_login_request_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating login request",
        )
    if resp and resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if hasattr(resp.data, "ext_id") and resp.data.ext_id:
            # update returns login request, keep ext_id
            result["ext_id"] = resp.data.ext_id
    else:
        # fallback to fetching updated entity
        updated = get_login_request(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(updated.to_dict())
    result["changed"] = True


def delete_login_request(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Login request with ext_id:{0} will be deleted.".format(ext_id)
        return

    # Fetch ETag for If-Match header
    try:
        old_spec = get_login_request(module, api_instance, ext_id)
        etag = get_etag(data=old_spec)
    except Exception:
        old_spec = None
        etag = None
    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.delete_login_request_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting login request",
        )
    if resp and hasattr(resp, "data") and resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if hasattr(resp.data, "ext_id") and resp.data.ext_id:
            result["task_ext_id"] = resp.data.ext_id
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_login_requests_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_login_request(module, result, api_instance)
        else:
            create_login_request(module, result, api_instance)
    else:
        delete_login_request(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
