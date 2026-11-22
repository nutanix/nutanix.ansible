#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_oidc_clients_v2
short_description: Create and Delete OIDC clients in Nutanix Prism Central
version_added: 2.7.0
description:
  - Create and Delete OIDC clients in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Create an OIDC client) -
    Required Roles: Prism Admin, Super Admin
  - >-
    B(Delete an OIDC client) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  state:
    description:
      - If C(state) is set to C(present) then the operation will be create OIDC client.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete OIDC client.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the OIDC client.
      - Required for delete operation.
    type: str
    required: false
  client_name:
    description:
      - Name of OIDC client.
    type: str
    required: false
  application_type:
    description:
      - Application type for OIDC client.
    type: str
    required: false
  redirect_uris:
    description:
      - Redirect URIs for OIDC client.
    type: list
    elements: str
    required: false
  sha256_thumbprint_list:
    description:
      - SHA256 of a certificate public key.
    type: list
    elements: str
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
- name: Create OIDC client
  nutanix.ncp.ntnx_oidc_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    client_name: "test-oidc-client"
    redirect_uris:
      - "https://example.com/callback"
      - "https://example.com/callback2"
    application_type: "web"
    sha256_thumbprint_list:
      - "abc123thumbprint"
  register: result
  ignore_errors: true

- name: Delete OIDC client
  nutanix.ncp.ntnx_oidc_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "00000000-0000-0000-0000-000000000000"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting OIDC client.
    - If the operation is create, it will contain the OIDC client details.
    - If the operation is delete, it will be null.
  returned: always
  type: dict
  sample:
    {
      "application_type": "web",
      "client_id": "oidc-client-uuid-1234",
      "client_name": "test-oidc-client",
      "client_secret": "secret-value-xyz",
      "created_time": "2026-07-01T06:00:00.000000+00:00",
      "last_updated_time": "2026-07-01T06:00:00.000000+00:00",
      "redirect_uris": [
        "https://example.com/callback"
      ],
      "sha256_thumbprint_list": [
        "abc123thumbprint"
      ]
    }

ext_id:
  description:
    - The external ID of the OIDC client.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"

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
  sample: "Api Exception raised while creating OIDC client"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
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
    module_args = dict(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        ext_id=dict(type="str"),
        client_name=dict(type="str"),
        application_type=dict(type="str"),
        redirect_uris=dict(type="list", elements="str"),
        sha256_thumbprint_list=dict(type="list", elements="str"),
    )
    return module_args


def create_oidc_client(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.OidcClient()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create OIDC client spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_oidc_client(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating OIDC client",
        )
    # Response is OidcClient directly
    result["response"] = strip_internal_attributes(resp.to_dict())
    # Try to set ext_id from client_id
    if hasattr(resp, "client_id") and resp.client_id:
        result["ext_id"] = resp.client_id
    elif isinstance(resp.to_dict(), dict) and resp.to_dict().get("client_id"):
        result["ext_id"] = resp.to_dict().get("client_id")
    result["changed"] = True


def delete_oidc_client(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "OIDC client with ext_id:{0} will be deleted.".format(ext_id)
        return

    try:
        resp = api_instance.delete_oidc_client_by_id(extId=ext_id)
        # Some SDK versions return dict or None
        if resp is not None and hasattr(resp, "to_dict"):
            result["response"] = strip_internal_attributes(resp.to_dict())
        elif isinstance(resp, dict):
            result["response"] = strip_internal_attributes(resp)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting OIDC client",
        )
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
    result = {"changed": False, "failed": False, "response": None}
    api_instance = get_oidc_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_oidc_client(module, result, api_instance)
    else:
        delete_oidc_client(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
