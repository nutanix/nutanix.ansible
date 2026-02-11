#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_certificate_auth_providers_info_v2
short_description: Fetch information about certificate-based authentication provider(s)
version_added: "2.5.0"
description:
  - This module fetches information about Nutanix certificate-based authentication provider(s).
  - Fetch specific certificate authentication provider using external ID.
  - Fetch list containing only one certificate authentication provider if external ID is not provided.
  - This module uses PC v4 APIs based SDKs.
options:
  ext_id:
    description:
      - The external ID of the certificate authentication provider.
      - If provided, returns single certificate authentication provider.
      - If not provided, returns list containing only one certificate authentication provider.
    type: str
    required: false
  page:
    description:
      - The number of page
    type: int
  limit:
    description:
      - The number of records
    type: int
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
- name: Get details of a specific certificate authentication provider
  nutanix.ncp.ntnx_certificate_auth_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
  register: result

- name: List all certificate authentication providers
  nutanix.ncp.ntnx_certificate_auth_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: List all certificate authentication providers with page and limit
  nutanix.ncp.ntnx_certificate_auth_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    page: 0
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response for fetching certificate authentication provider(s).
    - Single certificate authentication provider if external ID is provided.
    - List containing only one certificate authentication provider if external ID is provided.
  type: dict
  returned: always
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
      "client_ca_chain": "-----BEGIN CERTIFICATE-----\nMIIGuzCCBKOgIBAgICEAEwDQYDVEK0/s84n\n-----END CERTIFICATE-----\n",
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
  type: bool
  returned: always
  sample: false
failed:
  description: Indicates if the operation failed.
  type: bool
  returned: always
  sample: false
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching certificate authentication provider info"
error:
  description: Error message if something goes wrong.
  type: str
  returned: always
ext_id:
  description: The external ID of the certificate authentication provider that was fetched.
  type: str
  returned: when fetching a specific certificate authentication provider
  sample: "a3265671-de53-41be-af9b-f06241b95356"
total_available_results:
  description: The total number of available certificate authentication providers in PC.
  type: int
  returned: when all certificate authentication providers are fetched
  sample: 5
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_certificate_auth_provider_api_instance,
)
from ..module_utils.v4.iam.helpers import get_certificate_auth_provider  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        limit=dict(type="int"),
        page=dict(type="int"),
    )
    return module_args


def get_certificate_auth_provider_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")

    resp = get_certificate_auth_provider(
        module=module,
        api_instance=api_instance,
        ext_id=ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_certificate_auth_providers(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        result[
            "msg"
        ] = "Failed generating certificate authentication provider info Spec"
        module.fail_json(**result)

    try:
        resp = api_instance.list_cert_auth_providers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching certificate authentication provider info",
        )
    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        skip_info_args=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_certificate_auth_provider_api_instance(module)
    if module.params.get("ext_id"):
        get_certificate_auth_provider_using_ext_id(module, api_instance, result)
    else:
        get_certificate_auth_providers(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
