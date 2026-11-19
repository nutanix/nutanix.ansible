#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_federation_v2
short_description: Create and Delete federation in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create and delete federation with an OIDC provider in Nutanix Prism Central.
  - This module uses PC v4 APIs based SDKs
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
  state:
    description:
      - If C(state) is set to C(present), the module will create federation.
      - If C(state) is set to C(absent), the module will delete federation.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  well_known_config:
    description:
      - Well known URL of the OIDC provider.
    type: str
    required: false
  idp_id:
    description:
      - IDP attached to the users of the OIDC provider.
    type: str
    required: false
  cloud_tenant:
    description:
      - Provider side tenant that is registering domain.
    type: str
    required: false
  cloud_api_key:
    description:
      - API key for authenticating to the OIDC provider.
    type: str
    required: false
  claim_map:
    description:
      - Mapping of claims from IAM to the OIDC provider.
    type: dict
    required: false
    suboptions:
      name:
        description:
          - Name of the federation claim.
        type: str
        required: false
      email:
        description:
          - Email of the federation claim.
        type: str
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
- name: Create federation with well known config
  nutanix.ncp.ntnx_federation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    well_known_config: "https://example.okta.com/.well-known/openid-configuration"
    idp_id: "00000000-0000-0000-0000-000000000000"
    cloud_api_key: "test-api-key"
    claim_map:
      name: "name"
      email: "email"
  register: result
  ignore_errors: true

- name: Delete federation
  nutanix.ncp.ntnx_federation_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating or deleting federation.
    - If C(wait) is true and the operation is Create, it will contain the federation details.
    - If C(wait) is false or the operation is Delete, it will contain the task details.
  returned: always
  type: dict
  sample:
    {
      "cloud_api_key": null,
      "cloud_tenant": null,
      "claim_map": {
        "email": "email",
        "name": "name"
      },
      "created_by": "admin",
      "created_time": "2026-07-21T06:36:56.065999+00:00",
      "ext_id": "00000000-0000-0000-0000-000000000001",
      "idp_id": "00000000-0000-0000-0000-000000000000",
      "last_updated_time": "2026-07-21T06:36:56.065999+00:00",
      "tenant_id": null,
      "well_known_config": "https://example.okta.com/.well-known/openid-configuration"
    }

ext_id:
  description:
    - The external ID of the federation.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000001"

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

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
  sample: "Api Exception raised while creating federation"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import get_federations_api_instance  # noqa: E402
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    claim_map_spec = dict(
        name=dict(type="str", required=False),
        email=dict(type="str", required=False),
    )

    module_args = dict(
        state=dict(type="str", choices=["present", "absent"], default="present"),
        well_known_config=dict(type="str", required=False),
        idp_id=dict(type="str", required=False),
        cloud_tenant=dict(type="str", required=False),
        cloud_api_key=dict(type="str", required=False, no_log=True),
        claim_map=dict(
            type="dict",
            options=claim_map_spec,
            required=False,
            obj=identity_and_access_management_sdk.FederationClaims,
        ),
    )
    return module_args


def create_federation(module, result, api_instance):
    sg = SpecGenerator(module)
    default_spec = identity_and_access_management_sdk.Federation()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create federation spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = api_instance.create_federation(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating federation",
        )

    if resp and getattr(resp, "data", None):
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        data_dict = result["response"]
        if isinstance(data_dict, dict) and data_dict.get("ext_id"):
            result["ext_id"] = data_dict.get("ext_id")
    elif resp:
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_federation(module, result, api_instance):
    if module.check_mode:
        result["msg"] = "Federation will be deleted."
        return

    try:
        resp = api_instance.delete_federation()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting federation",
        )

    if resp and resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
        if hasattr(resp.data, "ext_id") and resp.data.ext_id:
            result["task_ext_id"] = resp.data.ext_id
    elif resp:
        try:
            result["response"] = strip_internal_attributes(resp.to_dict())
        except Exception:
            result["response"] = {}

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}

    api_instance = get_federations_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        create_federation(module, result, api_instance)
    else:
        delete_federation(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
