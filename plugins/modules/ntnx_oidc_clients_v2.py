#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_oidc_clients_v2
short_description: Manage OIDC clients in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Create and Delete OIDC clients in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned
      to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create OIDC Client) -
      Required Roles: Super Admin
    - >-
      B(Delete OIDC Client) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam&version=v4.1.b4#tag/OIDC)"
options:
    ext_id:
        description:
            - The External ID of the OIDC client.
            - Required for deleting the OIDC client.
        type: str
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
    state:
        description:
            - Specify state
            - If C(state) is set to C(present) then module will create OIDC client.
            - If C(state) is set to C(absent) with C(ext_id), then module will delete OIDC client.
        choices:
            - present
            - absent
        type: str
        default: present
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create OIDC client
  nutanix.ncp.ntnx_oidc_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    client_name: "test-oidc-client"
    application_type: "Backend application"
    redirect_uris:
      - "https://example.com/callback"
      - "https://example.com/callback2"
    sha256_thumbprint_list:
      - "3BCbFA2eeDF0F6bf9E8Fc41ccA8eFAafBF1dCe1B3cEAB51De4fF0E2EB7B52E4d"
    state: present
  register: result

- name: Delete OIDC client
  nutanix.ncp.ntnx_oidc_clients_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "0e820dbd-aa56-4257-9f99-2b9930a406bf"
    state: absent
  register: result
"""

RETURN = r"""
response:
  description:
      - Response for creating or deleting OIDC client.
      - It will contain the OIDC client details.
  returned: always
  type: dict
   sample:
    {
                "application_type": "Backend application",
                "client_id": "83704d9f-82e4-538c-a36d-faf668a3c838",
                "client_name": "oidc-sample-gt8f6w",
                "client_secret": "",
                "created_time": "2026-11-19T08:39:53.942972+00:00",
                "last_updated_time": "2026-11-19T08:39:53.942972+00:00",
                "redirect_uris": [
                    "https://example.com/callback",
                    "https://example.com/callback2"
                ],
                "sha256_thumbprint_list": [
                    "3BCbFA2eeDF0F6bf9E8Fc41ccA8eFAafBF1dCe1B3cEAB51De4fF0E2EB7B52E4d"
                ]
            }
changed:
  description:
    - This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
ext_id:
  description:
    - The external ID of the OIDC client.
  returned: always
  type: str
  sample: "0e820dbd-aa56-4257-9f99-2b9930a406bf"
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error or in check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating OIDC client"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str
  sample: false
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_oidc_api_instance  # noqa: E402
from ..module_utils.v4.iam.helpers import get_oidc_client  # noqa: E402
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
        ext_id=dict(type="str"),
        client_name=dict(type="str"),
        application_type=dict(type="str"),
        redirect_uris=dict(type="list", elements="str"),
        sha256_thumbprint_list=dict(type="list", elements="str"),
    )
    return module_args


def create_oidc_client(module, api_instance, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.OidcClient()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create OIDC client spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_oidc_client(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating OIDC client",
        )

    # OIDC client response contains client_id as identifier
    # ext_id path param maps to client_id
    ext_id = getattr(resp, "client_id", None)
    if not ext_id:
        ext_id = getattr(resp, "ext_id", None)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_oidc_client(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "OIDC client with ext_id:{0} will be deleted.".format(ext_id)
        return

    # Verify existence before delete
    get_oidc_client(module, api_instance, ext_id=ext_id)

    try:
        resp = api_instance.delete_oidc_client_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting OIDC client",
        )
    result["changed"] = True
    if resp is None:
        result["msg"] = "OIDC client with ext_id: {} deleted successfully".format(
            ext_id
        )
    else:
        # delete may return dict or empty
        try:
            result["response"] = strip_internal_attributes(resp.to_dict())
        except Exception:
            result["response"] = resp


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("client_name",)),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    state = module.params["state"]
    api_instance = get_oidc_api_instance(module)
    if state == "present":
        create_oidc_client(module, api_instance, result)
    else:
        delete_oidc_client(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
