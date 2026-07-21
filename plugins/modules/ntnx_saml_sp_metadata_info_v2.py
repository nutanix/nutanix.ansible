#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_saml_sp_metadata_info_v2
short_description: Fetch SAML Service Provider (SP) metadata info from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to fetch information about SamlSpMetadata in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific SamlSpMetadata for
    that SAML identity provider (uses the new per-IDP endpoint).
  - If C(ext_id) is not provided, fetch the legacy cluster-wide SAML SP metadata.
  - The SP metadata is returned as an XML document.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to
    the user performing the operation.
  - >-
    B(Get SAML SP metadata) -
    Required Roles: Nutanix Central Admin, Prism Admin, Prism Viewer,
    Project Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - External ID of an existing SAML identity provider whose SP metadata
        must be fetched.
      - When provided, the newer per-IDP endpoint is used
        (C(GET /api/iam/v4.x/authn/saml-identity-providers/{extId}/sp-metadata)).
      - When omitted, the legacy cluster-wide SP metadata endpoint
        (C(GET /api/iam/v4.x/authn/saml-sp-metadata)) is used.
    type: str
    required: false
  read_timeout:
    description: Read timeout in milliseconds for API calls.
    type: int
    required: false
    default: 30000
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix Ansible Codegen (@nutanix)
"""

EXAMPLES = r"""
- name: Get SAML SP metadata for a specific identity provider
  nutanix.ncp.ntnx_saml_sp_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "368169cc-5293-543e-901d-4ba26874967a"
  register: sp_metadata_info

- name: Get legacy cluster-wide SAML SP metadata
  nutanix.ncp.ntnx_saml_sp_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: legacy_sp_metadata_info
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SamlSpMetadata info v4 API.
    - It contains the XML metadata document under C(content) along with the
      SAML IDP external ID under C(ext_id) (``null`` for the legacy endpoint).
  returned: always
  type: dict
  sample:
    ext_id: "368169cc-5293-543e-901d-4ba26874967a"
    content: |
      <?xml version="1.0"?>
      <md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
                           validUntil="2032-01-17T08:35:15Z"
                           cacheDuration="PT604800S"
                           entityID="https://10.44.76.29:9440/api/iam/authn">
        <md:SPSSODescriptor AuthnRequestsSigned="false"
                            WantAssertionsSigned="true"
                            protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
          ...
        </md:SPSSODescriptor>
      </md:EntityDescriptor>
ext_id:
  description:
    - External ID of the SAML identity provider whose SP metadata was fetched.
    - Returned as ``null`` when the legacy cluster-wide endpoint was used.
  returned: always
  type: str
  sample: "368169cc-5293-543e-901d-4ba26874967a"
changed:
  description: Always False for info modules.
  returned: always
  type: bool
  sample: false
msg:
  description: Status / error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching SAML SP metadata"
error:
  description: Error details when the operation fails.
  returned: When an error occurs
  type: str
failed:
  description: Whether the task failed.
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
from ..module_utils.v4.iam.helpers import get_saml_sp_metadata  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    import ntnx_iam_py_client  # noqa: F401
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def _decode_metadata_payload(payload):
    """Convert the SDK response payload to a Unicode XML string."""
    if payload is None:
        return None
    if isinstance(payload, bytes):
        try:
            return payload.decode("utf-8")
        except UnicodeDecodeError:
            return payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        return payload
    return str(payload)


def fetch_saml_sp_metadata(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    resp = get_saml_sp_metadata(module, api_instance, ext_id=ext_id)
    if resp is None:
        raise_api_exception(
            module=module,
            exception=Exception(
                "SDK returned an empty response while fetching SAML SP metadata"
            ),
            msg="Empty response while fetching SAML SP metadata",
        )

    try:
        resp_dict = strip_internal_attributes(resp.to_dict())
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to serialise SAML SP metadata response",
        )
        resp_dict = {}

    xml_content = _decode_metadata_payload(resp_dict.get("data"))
    if not xml_content:
        raise_api_exception(
            module=module,
            exception=Exception(
                "SAML SP metadata payload is empty for ext_id: {0}".format(ext_id)
            ),
            msg="SAML SP metadata payload is empty",
        )

    result["response"] = {
        "ext_id": ext_id,
        "content": xml_content,
    }


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
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
        "failed": False,
    }
    api_instance = get_identity_provider_api_instance(module)
    fetch_saml_sp_metadata(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
