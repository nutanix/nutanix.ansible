#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_saml_idp_sp_metadata_v2
short_description: Download SAML Service Provider (SP) metadata for a configured SAML identity provider in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module downloads the Service Provider (SP) metadata XML document for a
    specific SAML identity provider (IdP) that has been configured in Nutanix
    Prism Central.
  - The returned SP metadata is a standard SAML 2.0 C(<md:EntityDescriptor>)
    document that can be uploaded to an external Identity Provider (Okta, ADFS,
    Keycloak, etc.) to establish trust with Prism Central acting as the
    Service Provider.
  - This is a read-only download operation. It does not create, update, or
    delete any resources on the cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Download SAML IdP SP-Metadata) -
    Required Roles: Nutanix Central Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  state:
    description:
      - State of the module.
      - If C(state) is set to C(present) the module will download the
        SP-Metadata for the SAML identity provider identified by C(ext_id).
      - Only C(present) is supported for this read-only download operation.
    type: str
    choices:
      - present
    default: present
    required: false
  ext_id:
    description:
      - External ID of the SAML identity provider whose SP-Metadata should be
        downloaded.
      - Required for the download operation.
    type: str
    required: true
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
- name: Download SP-Metadata for a SAML identity provider
  nutanix.ncp.ntnx_saml_idp_sp_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "5fa927db-dcf1-5fee-ad3f-dc2ee9e80915"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The SP-Metadata XML document for the requested SAML identity provider.
    - Returned as a string that contains a standard SAML 2.0
      C(<md:EntityDescriptor>) element and its descendants
      (SPSSODescriptor, AssertionConsumerService, etc.).
  returned: always
  type: str
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
    - The external ID of the SAML identity provider whose SP-Metadata was
      downloaded.
  returned: always
  type: str
  sample: "5fa927db-dcf1-5fee-ad3f-dc2ee9e80915"

changed:
  description:
    - This indicates whether the operation resulted in any change on the cluster.
    - Always C(false) for this read-only download operation.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, or on check mode.
  type: str
  sample: "Api Exception raised while downloading SAML IdP SP-Metadata"

error:
  description: This field typically holds information about any error that
      occurred during execution.
  returned: When an error occurs
  type: str

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
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_identity_provider_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    validate_required_params,
)

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
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def _extract_sp_metadata(resp):
    """Extract the SP-Metadata payload from an SDK response.

    The IAM SDK models the response ``data`` as a OneOf that resolves to
    ``str`` on success (the XML document). Depending on SDK version the
    payload can appear either as ``resp.data`` (already a string) or nested
    inside an object with a ``value`` attribute. Normalize both shapes.
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


def download_saml_idp_sp_metadata(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    validate_required_params(module, ["ext_id"])

    if module.check_mode:
        result["msg"] = (
            "SAML IdP SP-Metadata for ext_id:{0} will be downloaded.".format(ext_id)
        )
        return

    try:
        resp = api_instance.get_saml_idp_sp_metadata_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading SAML IdP SP-Metadata",
        )

    result["response"] = _extract_sp_metadata(resp)


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
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }

    api_instance = get_identity_provider_api_instance(module)
    download_saml_idp_sp_metadata(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
