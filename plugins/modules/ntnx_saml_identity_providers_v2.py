#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_saml_identity_providers_v2
short_description: Manage SAML identity providers in Nutanix PC
version_added: "2.0.0"
description:
  - Create, Update, Delete SAML identity providers in Nutanix PC
  - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
            - External ID of the Identity provider.
            - Required for updating or deleting the Identity provider.
    type: str
  name:
    description:
      - Unique name of the IDP.
    required: false
    type: str
  username_attribute:
    description:
      - SAML assertion Username attribute element.
    required: false
    type: str
  email_attribute:
    description:
      - SAML assertion email attribute element.
    required: false
    type: str
  groups_attribute:
    description:
      - SAML assertion groups attribute element.
    required: false
    type: str
  groups_delim:
    description:
      - Delimiter is used to split the value of attribute into multiple groups.
    required: false
    type: str
  idp_metadata_url:
    description:
      - Metadata url that provides IDP details.
    required: false
    type: str
  idp_metadata_xml:
    description:
      - Base64 encoded metadata in XML format with IDP details.
    required: false
    type: str
  idp_metadata:
    description:
      - Information of the IDP.
    required: false
    type: dict
    suboptions:
        entity_id:
          description:
            - Entity Identifier of Identity provider.
          required: false
          type: str
        login_url:
          description:
            - Login URL of the Identity provider.
          required: false
          type: str
        logout_url:
          description:
            - Logout URL of the Identity provider.
          required: false
          type: str
        error_url:
          description:
            - Error URL of the Identity provider.
          required: false
          type: str
        certificate:
          description:
            - Certificate for verification.
          required: false
          type: str
        name_id_policy_format:
          description:
            - Name ID Policy format.
          required: false
          type: str
          choices: ["EMAILADDRESS","UNSPECIFIED","X509SUBJECTNAME","WINDOWSDOMAINQUALIFIEDNAME","ENCRYPTED","ENTITY","KERBEROS","PERSISTENT","TRANSIENT",]
  custom_attributes:
    description:
      - SAML assertions for list of custom attribute elements.
    required: false
    type: list
    elements: str
  entity_issuer:
    description:
      - It will be used as Issuer in SAML authnRequest.
    required: false
    type: str
  is_signed_authn_req_enabled:
    description:
      - Flag indicating signing of SAML authnRequests.
    required: false
    type: bool
  state:
    description:
        - Specify state
        - If C(state) is set to C(present) then module will create Identity provider.
        - if C(state) is set to C(present) and C(ext_id) is given, then module will update Identity provider.
        - If C(state) is set to C(absent) with C(ext_id), then module will delete Identity provider.
    choices:
        - present
        - absent
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
  - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
  - Alaa Bishtawi (@alaa-bish)
"""


EXAMPLES = r"""
- name: Create identity provider
  nutanix.ncp.ntnx_saml_identity_providers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    name: "ansible-saml"
    username_attribute: "test_name"
    email_attribute: "email"
    groups_attribute: "groups"
    groups_delim: ","
    idp_metadata_xml: "https://samltest.id/saml/idp"
    is_signed_authn_req_enabled: true
    state: present
  register: result
  ignore_errors: true
- name: Update identity provider
  nutanix.ncp.ntnx_saml_identity_providers_v2:
    ext_id: "59d5de78-a964-5746-8c6e-677c4c7a79df"
    name: "ansible-saml"
    username_attribute: "new_name2"
    email_attribute: "email"
    groups_attribute: "groups"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
- name: Delete identity provider
  nutanix.ncp.ntnx_saml_identity_providers_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "59d5de78-a964-5746-8c6e-677c4c7a79df"
  register: result
"""

RETURN = r"""
response:
  description:
        - Response for the Identity provider operations.
        - Identity provider details if C(wait) is true.
        - Task details if C(wait) is false.
  returned: always
  type: dict
  sample:
    {
                "created_by": "00000000-0000-0000-0000-000000000000",
                "created_time": "2024-07-01T05:20:48.365380+00:00",
                "custom_attributes": null,
                "email_attribute": "email",
                "entity_issuer": "https://000.000.000.000:9440/api/iam/authn",
                "ext_id": "5fa927db-dcf1-5fee-ad3f-dc2ee9e80915",
                "groups_attribute": "groups",
                "groups_delim": ",",
                "idp_metadata": {
                    "certificate": null,
                    "entity_id": "http://test.test.com/adfs/services/trust",
                    "error_url": null,
                    "login_url": "https://test.test.com/adfs/ls/",
                    "logout_url": "https://test.test.com/adfs/ls/IdpInitiatedSignOn.asp",
                    "name_id_policy_format": "emailAddress"
                },
                "idp_metadata_url": null,
                "idp_metadata_xml": null,
                "is_signed_authn_req_enabled": false,
                "last_updated_time": "2024-07-01T05:20:48.365380+00:00",
                "links": null,
                "name": "ansible-saml",
                "tenant_id": "59d5de78-a964-5746-8c6e-677c4c7a79df",
                "username_attribute": "DibnCPQWWtZtansible-agvm1"
            }
changed:
  description:
    - Whether the identity provider is changed or not.
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
ext_id:
  description:
          - External ID of the Identity provider.
  returned: always
  type: str
  sample: "00000000-0000-0000-0000-000000000000"
skipped:
    description:
        - Whether the operation is skipped or not.
        - Will be returned if operation is skipped.
    type: bool
    returned: always
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_identity_provider_api_instance,
)
from ..module_utils.v4.iam.helpers import get_identity_provider  # noqa: E402
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
    idp_metadata_spec = dict(
        entity_id=dict(type="str"),
        login_url=dict(type="str"),
        logout_url=dict(type="str"),
        error_url=dict(type="str"),
        certificate=dict(type="str"),
        name_id_policy_format=dict(
            type="str",
            choices=[
                "EMAILADDRESS",
                "UNSPECIFIED",
                "X509SUBJECTNAME",
                "WINDOWSDOMAINQUALIFIEDNAME",
                "ENCRYPTED",
                "ENTITY",
                "KERBEROS",
                "PERSISTENT",
                "TRANSIENT",
            ],
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        username_attribute=dict(type="str"),
        email_attribute=dict(type="str"),
        groups_attribute=dict(type="str"),
        groups_delim=dict(type="str"),
        idp_metadata_url=dict(type="str"),
        idp_metadata_xml=dict(type="str"),
        idp_metadata=dict(
            type="dict", options=idp_metadata_spec, obj=iam_sdk.IdpMetadata
        ),
        custom_attributes=dict(type="list", elements="str"),
        entity_issuer=dict(type="str"),
        is_signed_authn_req_enabled=dict(type="bool"),
    )
    return module_args


def create_identity_provider(module, identity_providers, result):
    sg = SpecGenerator(module)
    default_spec = iam_sdk.SamlIdentityProvider()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create identity providers spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = identity_providers.create_saml_identity_provider(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating identity provider",
        )

    result["ext_id"] = resp.data.ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def check_identity_providers_idempotency(old_spec, update_spec):
    if old_spec != update_spec:
        return False

    return True


def update_identity_provider(module, identity_providers, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_identity_provider(module, identity_providers, ext_id=ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating identity providers update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_identity_providers_idempotency(
        current_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = identity_providers.update_saml_identity_provider_by_id(
            extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating identity provider",
        )

    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def delete_identity_provider(module, identity_providers, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Identity provider with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    current_spec = get_identity_provider(module, identity_providers, ext_id=ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for deleting identity provider", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = identity_providers.delete_saml_identity_provider_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting identity provider",
        )
    result["changed"] = True
    if resp is None:
        result["msg"] = "Identity Provider with ext_id: {} deleted successfully".format(
            ext_id
        )
    else:
        result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseModule(
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
    }
    state = module.params["state"]
    identity_providers = get_identity_provider_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_identity_provider(module, identity_providers, result)
        else:
            create_identity_provider(module, identity_providers, result)
    else:
        delete_identity_provider(module, identity_providers, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
