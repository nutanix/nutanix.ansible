#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_saml_sp_metadata_v2
short_description: Download SAML Service Provider (SP) metadata from Nutanix Prism Central
version_added: 2.5.0
description:
  - This module downloads the SAML Service Provider (SP) metadata XML from a
    Nutanix Prism Central so that an administrator can import it into an
    external SAML Identity Provider (IDP) such as ADFS, Okta or Ping Identity.
  - When C(ext_id) is provided, the newer per-IDP endpoint is used
    (C(GET /api/iam/v4.x/authn/saml-identity-providers/{extId}/sp-metadata)).
    The response reflects the IDP's own configured redirect URL and entity
    issuer, and honours the C(is_signed_authn_req_enabled) flag on that IDP.
  - When C(ext_id) is not provided, the legacy cluster-wide endpoint is used
    (C(GET /api/iam/v4.x/authn/saml-sp-metadata)). This endpoint has been
    deprecated by ENG-729426 in favour of the per-IDP endpoint.
  - The SP metadata is returned as an XML document. Optionally, the module
    can persist the XML to a file on the Ansible controller via C(dest).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to
    the user performing the operation.
  - >-
    B(Download SAML SP metadata) -
    Required Roles: Nutanix Central Admin, Prism Admin, Prism Viewer,
    Project Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - External ID of an existing SAML identity provider whose SP metadata
        must be downloaded.
      - When provided, the newer per-IDP endpoint is used so that per-IDP
        configuration (reverse-proxy redirect URL, signed authn requests)
        is honoured.
      - When omitted, the legacy cluster-wide SP metadata endpoint is used.
    type: str
    required: false
  dest:
    description:
      - Optional absolute path on the Ansible controller where the fetched
        SP metadata XML should be written.
      - When provided, the module writes the XML content to this file after
        a successful fetch and reports the path back under C(response.path).
      - The parent directory must already exist.
    type: path
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix Ansible Codegen (@nutanix)
"""

EXAMPLES = r"""
- name: Download SAML SP metadata for a specific identity provider
  nutanix.ncp.ntnx_saml_sp_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "368169cc-5293-543e-901d-4ba26874967a"
  register: sp_metadata

- name: Download legacy cluster-wide SAML SP metadata
  nutanix.ncp.ntnx_saml_sp_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: legacy_sp_metadata

- name: Download SAML SP metadata for a specific IDP and save it to a file
  nutanix.ncp.ntnx_saml_sp_metadata_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "368169cc-5293-543e-901d-4ba26874967a"
    dest: "/tmp/adfs19-sp-metadata.xml"
  register: saved_sp_metadata
"""

RETURN = r"""
response:
  description:
    - Details of the fetched SAML SP metadata.
    - Contains the raw XML metadata document under C(content) and, when a
      destination path was provided, the file path where the XML was saved
      under C(path).
    - The C(ext_id) sub-field echoes the SAML IDP external ID used for the
      request (``null`` when the legacy endpoint was called).
  returned: always
  type: dict
  sample:
    ext_id: "368169cc-5293-543e-901d-4ba26874967a"
    path: "/tmp/adfs19-sp-metadata.xml"
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
    - External ID of the SAML identity provider whose SP metadata was
      downloaded.
    - Returned as ``null`` when the legacy cluster-wide endpoint was used.
  returned: always
  type: str
  sample: "368169cc-5293-543e-901d-4ba26874967a"
task_ext_id:
  description:
    - Placeholder for parity with other v4 modules. The SP metadata endpoints
      are synchronous and do not create a task, so this is always ``null``.
  returned: always
  type: str
  sample: null
changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true
skipped:
  description:
    - Whether the operation was skipped. Set when the module was invoked in
      check mode.
  returned: when applicable
  type: bool
  sample: false
msg:
  description: Status / error message.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "SAML SP metadata for ext_id:368169cc-5293-543e-901d-4ba26874967a will be downloaded."
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

import os  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
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
        dest=dict(type="path"),
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


def _write_metadata_to_file(module, result, xml_content, dest):
    """Persist the SP metadata XML to a file on the controller."""
    parent = os.path.dirname(os.path.abspath(dest))
    if not os.path.isdir(parent):
        result["failed"] = True
        module.fail_json(
            msg="Destination directory does not exist: {0}".format(parent), **result
        )
    try:
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(xml_content or "")
    except (OSError, IOError) as e:
        result["failed"] = True
        module.fail_json(
            msg="Failed to write SAML SP metadata to {0}: {1}".format(dest, str(e)),
            **result,
        )


def download_saml_sp_metadata(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = ext_id

    if module.check_mode:
        if ext_id:
            result["msg"] = (
                "SAML SP metadata for ext_id:{0} will be downloaded.".format(ext_id)
            )
        else:
            result["msg"] = "Legacy cluster-wide SAML SP metadata will be downloaded."
        return

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

    response = {
        "ext_id": ext_id,
        "content": xml_content,
        "path": None,
    }

    if dest:
        _write_metadata_to_file(module, result, xml_content, dest)
        response["path"] = dest

    result["response"] = response
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
        "error": None,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
        "failed": False,
    }

    api_instance = get_identity_provider_api_instance(module)
    download_saml_sp_metadata(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
