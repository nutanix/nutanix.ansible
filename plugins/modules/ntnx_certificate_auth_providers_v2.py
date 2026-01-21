#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_certificate_auth_providers_v2
short_description: Manage certificate-based authentication providers in Nutanix Prism Central
version_added: "2.5.0"
description:
  - Create, Update, Delete certificate-based authentication providers in Nutanix Prism Central.
  - Certificate Authentication Providers enable mutual TLS (mTLS) authentication.
  - Allows users to log in using a client certificate (e.g., Smart Card, DoD CAC, PIV card) instead of username/password.
  - This module uses PC v4 APIs based SDKs.
options:
  state:
    description:
      - Specify state of the certificate authentication provider.
      - If C(state) is set to C(present) then module will create certificate auth provider.
      - If C(state) is set to C(present) and C(ext_id) is given, then module will update certificate auth provider.
      - If C(state) is set to C(absent) with C(ext_id), then module will delete certificate auth provider.
    type: str
    choices: ["present", "absent"]
  ext_id:
    description:
      - External ID of the certificate authentication provider.
      - Required for updating or deleting the certificate auth provider.
    type: str
  name:
    description:
      - Unique name of the certificate-based authentication provider.
      - Used to identify this specific provider in the Prism Central UI or API lists.
    type: str
  client_ca_chain:
    description:
      - The full chain of Certificate Authority (CA) certificates (Root CA and Intermediate CAs).
    type: str
  is_cert_auth_enabled:
    description:
      - Flag to enable/disable certificate authentication for the current provider.
    type: bool
  is_cac_enabled:
    description:
      - Flag to enable/disable Common Access Card (CAC).
    type: bool
  dir_svc_ext_id:
    description:
      - UUID of an existing Directory Service (e.g., Active Directory) configured in Prism Central.
    type: str
  ca_cert_file_name:
    description:
      - Name of the uploaded CA chain file.
      - The original filename of the clientCaChain you uploaded.
    type: str
  is_ocsp_enabled:
    description:
      - Flag to enable/disable Online Certificate Status Protocol (OCSP) revocation check.
    type: bool
  ocsp_responder:
    description:
      - URL of the OCSP responder used to override the URL from AIA extension.
    type: str
  is_crl_enabled:
    description:
      - Flag to enable/disable Certificate Revocation List (CRL) checking.
    type: bool
  crl_dps:
    description:
      - List of CRL Distribution Points URLs where the CRL file can be downloaded.
    type: list
    elements: str
  global_crl_refresh_interval:
    description:
      - Interval in seconds at which the CRL should be fetched from the CRL Distribution Points.
    type: int
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create certificate authentication provider with CAC enabled
  nutanix.ncp.ntnx_certificate_auth_providers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "CAC"
    client_ca_chain: "<ca_cert_chain_string>"
    ca_cert_file_name: "ca_cert_chain.pem"
    is_cert_auth_enabled: true
    is_cac_enabled: true
    dir_svc_ext_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  register: result
  ignore_errors: true

- name: Update certificate authentication provider
  nutanix.ncp.ntnx_certificate_auth_providers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
    name: "CAC"
    is_cert_auth_enabled: false
  register: result
  ignore_errors: true

- name: Delete certificate authentication provider
  nutanix.ncp.ntnx_certificate_auth_providers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the certificate authentication provider operations.
    - For create and update operations, it returns the certificate auth provider details.
    - For delete operation, it returns the message indicating the certificate auth provider is deleted successfully.
  returned: always
  type: dict
  sample:
    {
      "ca_cert_file_name": "ca_cert_chain.pem",
      "cert_revocation_info": {
          "crl_dps": null,
          "global_crl_refresh_interval": 86400,
          "is_crl_enabled": false,
          "is_ocsp_enabled": true,
          "ocsp_responder": ""
      },
      "client_ca_chain": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
      "created_by": "00000000-0000-0000-0000-000000000000",
      "created_time": null,
      "dir_svc_ext_id": "6cd7a803-a0ae-5a23-92be-e7a27573b363",
      "ext_id": "10c4bab1-2d88-540e-a602-92f723b44c73",
      "is_cac_enabled": true,
      "is_cert_auth_enabled": true,
      "last_updated_time": null,
      "links": null,
      "name": "CAC",
      "tenant_id": null
    }
changed:
  description: Indicates if any changes were made during the operation.
  returned: always
  type: bool
  sample: true
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or in delete operation
  type: str
  sample: "Api Exception raised while creating certificate auth provider"
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs
  sample: "BAD REQUEST"
ext_id:
  description: External ID of the certificate authentication provider.
  type: str
  returned: always
  sample: "a3265671-de53-41be-af9b-f06241b95356"
skipped:
  description: Indicates if the operation was skipped
  type: bool
  returned: always
  sample: false
failed:
  description: Indicates if the operation failed
  type: bool
  returned: always
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_certificate_auth_provider_api_instance,
    get_etag,
)
from ..module_utils.v4.iam.helpers import (  # noqa: E402
    get_api_params_from_spec,
    get_certificate_auth_provider,
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
    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        client_ca_chain=dict(type="str", no_log=True),
        is_cert_auth_enabled=dict(type="bool"),
        is_cac_enabled=dict(type="bool"),
        dir_svc_ext_id=dict(type="str"),
        ca_cert_file_name=dict(type="str"),
        is_ocsp_enabled=dict(type="bool"),
        ocsp_responder=dict(type="str"),
        is_crl_enabled=dict(type="bool"),
        crl_dps=dict(type="list", elements="str"),
        global_crl_refresh_interval=dict(type="int"),
    )
    return module_args


# Special case mappings for snake_case to camelCase conversion
# dir_svc_ext_id -> API expects 'dirSvcExtID' (uppercase ID), not 'dirSvcExtId'
CAMEL_CASE_SPECIAL_CASES = {
    "dir_svc_ext_id": "dirSvcExtID",
}


def create_certificate_auth_provider(module, api_instance, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.CertAuthProvider()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create certificate auth provider spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    # Get API parameters dynamically from spec (exclude ext_id as it's not used in create)
    api_params = get_api_params_from_spec(
        spec,
        module_spec=get_module_spec(),
        exclude_params=["ext_id"],
        special_cases=CAMEL_CASE_SPECIAL_CASES,
    )

    resp = None
    try:
        resp = api_instance.create_cert_auth_provider(**api_params)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating certificate auth provider",
        )

    # API returns entity directly, not a task
    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_certificate_auth_provider_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_certificate_auth_provider(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_certificate_auth_provider(module, api_instance, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating certificate auth provider", **result
        )

    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating certificate auth provider update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_certificate_auth_provider_idempotency(
        strip_internal_attributes(current_spec.to_dict()),
        strip_internal_attributes(update_spec.to_dict()),
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    # Get API parameters dynamically from update spec (exclude ext_id as it's passed separately)
    api_params = get_api_params_from_spec(
        update_spec,
        module_spec=get_module_spec(),
        special_cases=CAMEL_CASE_SPECIAL_CASES,
    )
    api_params.update(kwargs)

    resp = None
    try:
        resp = api_instance.update_cert_auth_provider_by_id(**api_params)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating certificate auth provider",
        )

    # API returns entity directly, not a task
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_certificate_auth_provider(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Certificate auth provider with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    current_spec = get_certificate_auth_provider(module, api_instance, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting certificate auth provider", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_cert_auth_provider_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting certificate auth provider",
        )

    # Delete API may return None or empty response
    result["changed"] = True
    if resp is None:
        result["msg"] = (
            "Certificate auth provider with ext_id: {} deleted successfully".format(
                ext_id
            )
        )
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params["state"]
    api_instance = get_certificate_auth_provider_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_certificate_auth_provider(module, api_instance, result)
        else:
            create_certificate_auth_provider(module, api_instance, result)
    else:
        delete_certificate_auth_provider(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
