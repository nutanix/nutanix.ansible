#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_saml_idp_sp_metadata_info_v2
short_description: Fetch SAML Service Provider (SP) metadata from Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about SamlIdpSpMetadata in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch the SP-Metadata for the specific SAML identity provider using
    the C(/saml-identity-providers/{extId}/sp-metadata) endpoint.
  - If C(ext_id) is not provided, fetch the generic (singleton) SP-Metadata for Prism Central
    using the C(/saml-sp-metadata) endpoint.
  - The response is a standard SAML 2.0 C(<md:EntityDescriptor>) XML document that
    can be uploaded to an external Identity Provider (Okta, ADFS, Keycloak, etc.)
    to establish a trust relationship with Prism Central acting as the
    Service Provider.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get SAML IdP SP-Metadata) -
    Required Roles: Nutanix Central Admin, Prism Admin, Super Admin
  - >-
    B(Get SAML SP-Metadata) -
    Required Roles: Nutanix Central Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - External ID of the SAML identity provider whose SP-Metadata should be fetched.
      - If not provided, the singleton generic SP-Metadata endpoint is called instead.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch SP-Metadata for a specific SAML identity provider
  nutanix.ncp.ntnx_saml_idp_sp_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "5fa927db-dcf1-5fee-ad3f-dc2ee9e80915"
  register: result
  ignore_errors: true

- name: Fetch generic (singleton) SP-Metadata for Prism Central
  nutanix.ncp.ntnx_saml_idp_sp_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SamlIdpSpMetadata info v4 API.
    - Returns the SP-Metadata XML document (as a string) for a single SAML
      identity provider when C(ext_id) is provided.
    - Returns the singleton SP-Metadata XML document (as a string) when
      C(ext_id) is not provided (there is no list/filter/limit variant for
      this endpoint).
  returned: always
  type: dict
  sample: >-
    <?xml version="1.0" encoding="UTF-8"?>
    <md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
        entityID="https://10.44.76.28:9440/api/iam/authn">
      <md:SPSSODescriptor AuthnRequestsSigned="false" WantAssertionsSigned="false"
          protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
        <md:AssertionConsumerService
            Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            Location="https://10.44.76.28:9440/api/iam/authn/saml_callback"
            index="1"/>
      </md:SPSSODescriptor>
    </md:EntityDescriptor>

ext_id:
  description:
    - External ID of the SAML identity provider whose SP-Metadata was fetched.
  type: str
  returned: when C(ext_id) is provided
  sample: "5fa927db-dcf1-5fee-ad3f-dc2ee9e80915"

changed:
  description: This indicates whether the operation resulted in any change on
      the cluster. Always C(false) for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching SAML IdP SP-Metadata info"

error:
  description: This field typically holds information about any error that
      occurred during execution.
  type: str
  returned: when an error occurs

failed:
  description: This indicates whether the operation failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_identity_provider_api_instance,
)
from ..module_utils.v4.utils import raise_api_exception  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as identity_and_access_management_sdk  # noqa: E402, F401 pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401 pylint: disable=unused-import
        mock_sdk as identity_and_access_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def _extract_sp_metadata(resp):
    """Extract the SP-Metadata payload from an SDK response.

    The IAM SDK models the response ``data`` as a OneOf that resolves to a
    ``str`` (the XML document) on success. Handle both flat and nested-object
    variants defensively.
    """
    data = getattr(resp, "data", None)
    if data is None:
        return None
    if isinstance(data, (str, bytes)):
        return data.decode() if isinstance(data, bytes) else data
    value = getattr(data, "value", None)
    if isinstance(value, (str, bytes)):
        return value.decode() if isinstance(value, bytes) else value
    try:
        return data.to_dict()
    except AttributeError:
        return str(data)


def get_saml_idp_sp_metadata_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    try:
        resp = api_instance.get_saml_idp_sp_metadata_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SAML IdP SP-Metadata info",
        )
    result["response"] = _extract_sp_metadata(resp)


def get_saml_sp_metadata_singleton(module, api_instance, result):
    try:
        resp = api_instance.get_saml_sp_metadata()
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching SAML SP-Metadata info",
        )
    result["response"] = _extract_sp_metadata(resp)


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_identity_provider_api_instance(module)
    if module.params.get("ext_id"):
        get_saml_idp_sp_metadata_by_ext_id(module, api_instance, result)
    else:
        get_saml_sp_metadata_singleton(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
