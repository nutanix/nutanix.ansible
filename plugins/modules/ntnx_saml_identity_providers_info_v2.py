#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_saml_identity_providers_info_v2
short_description: Fetch SAML identity providers from Nutanix PC
version_added: 2.0.0
description:
    - Fetch a single or list of multiple identity providers
    - if external id is provided, it will return the identity provider info
    - if external id is not provided, it will return multiple identity providers
options:
  ext_id:
    description:
            - Identity provider external ID
    required: false
    type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List identity providers
  nutanix.ncp.ntnx_saml_identity_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List identity provider using name filter criteria
  nutanix.ncp.ntnx_saml_identity_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'test_idp'"
  register: result

- name: List identity provider using ext_id
  nutanix.ncp.ntnx_saml_identity_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
  register: result
"""
RETURN = r"""
response:
  description:
      - The response from the identity provider v4 API.
      - it can be identity provider or  multiple identity providers as per spec.
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
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_identity_provider_api_instance,
)
from ..module_utils.v4.iam.helpers import get_identity_provider  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )

    return module_args


def get_identity_provider_by_ext_id(module, identity_providers, result):
    ext_id = module.params.get("ext_id")
    resp = get_identity_provider(module, identity_providers, ext_id=ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_identity_providers(module, identity_providers, result):

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating identity providers info Spec", **result)

    try:
        resp = identity_providers.list_saml_identity_providers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching identity providers info",
        )

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    identity_providers = get_identity_provider_api_instance(module)
    if module.params.get("ext_id"):
        get_identity_provider_by_ext_id(module, identity_providers, result)
    else:
        get_identity_providers(module, identity_providers, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
