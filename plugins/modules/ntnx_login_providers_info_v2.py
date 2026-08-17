#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_login_providers_info_v2
short_description: Fetch login providers info in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about LoginProvider in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific LoginProvider.
  - If C(ext_id) is not provided, list multiple LoginProvider optionally filtered / paginated.
  - LoginProvider is a read-only IAM v4 resource. It lists every authentication
    back-end configured on Prism Central - built-in local users, service
    accounts, and any directory service, SAML identity provider or certificate
    auth provider registered on the cluster.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get login provider by ext_id) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - >-
      B(List login providers) -
      Required Roles: Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  ext_id:
    description:
      - The external ID of the login provider.
      - When provided the module fetches a single login provider by resolving
        the ext_id server-side via the list API with an C(extId eq '...') filter.
      - This is because the LoginProviders API surface is read-only and does
        not expose a GetById endpoint.
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
- name: List all login providers configured on Prism Central
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: providers

- name: Get a single login provider by ext_id
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000000"
  register: provider

- name: Filter login providers by name (the built-in local provider is called 'local')
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'local'"
  register: local_providers

- name: List login providers with a pagination limit
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 2
  register: limited_providers

- name: List login providers sorted by createdTime ascending
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    orderby: "createdTime asc"
  register: sorted_providers

- name: List login providers returning only a subset of properties
  nutanix.ncp.ntnx_login_providers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    select: "name,type,extId"
  register: partial_providers
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LoginProvider info v4 API.
    - It can be a single LoginProvider if external ID is provided.
    - List of multiple LoginProvider if external ID is not provided with optional filter or limit.
    - The C(type) field is serialised as a lowercase string
      (C(local), C(saml), C(ldap), C(cert), C(service_account)); the SDK
      may also surface C($UNKNOWN) for provider types it does not yet know
      about (e.g. C(oidc) on newer PC builds).
    - Newer PC builds add multi-project scoping attributes
      (C(isSharedWithAllProjects), C(projectExtId), C(sharedWithProjects))
      that are surfaced verbatim as they are not part of the SDK model.
  returned: always
  type: dict
  sample:
    {
        "created_time": "2026-06-29T07:18:36.283028+00:00",
        "ext_id": "d607d664-cc19-559f-a95c-4e8b4b7f6606",
        "isSharedWithAllProjects": true,
        "is_browser_login_supported": true,
        "last_updated_time": "2026-06-29T07:18:36.283028+00:00",
        "links": null,
        "name": "local",
        "projectExtId": "00000000-0000-0000-0000-000000000000",
        "tenant_id": null,
        "type": "local"
    }

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching login providers info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the login provider
  type: str
  returned: when external ID is provided
  sample: "00000000-0000-0000-0000-000000000000"

total_available_results:
  description: The total number of available login providers in PC.
  type: int
  returned: when all login providers are fetched
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_login_providers_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def _fetch_login_provider_by_ext_id(module, login_providers_api, ext_id):
    """Fetch a single login provider by ext_id using the list API with a filter.

    The LoginProviders API surface only exposes a list endpoint - there is no
    GetById route. To keep parity with other v4 info modules we implement
    ext_id lookup by asking the list API to filter on extId server-side.
    """
    try:
        resp = login_providers_api.list_login_providers(
            _filter="extId eq '{0}'".format(ext_id)
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching login provider using ext_id {0}".format(
                ext_id
            ),
        )
    data = getattr(resp, "data", None) or []
    if not data:
        module.fail_json(
            msg="Login provider with ext_id '{0}' not found.".format(ext_id),
            failed=True,
            error="Not Found",
        )
    return data[0]


def get_login_provider_by_ext_id(module, login_providers_api, result):
    ext_id = module.params.get("ext_id")
    provider = _fetch_login_provider_by_ext_id(module, login_providers_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(provider.to_dict())


def get_login_providers(module, login_providers_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating login providers info spec", **result)

    try:
        resp = login_providers_api.list_login_providers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching login providers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
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
    result = {"changed": False, "response": None, "failed": False}
    login_providers_api = get_login_providers_api_instance(module)
    if module.params.get("ext_id"):
        get_login_provider_by_ext_id(module, login_providers_api, result)
    else:
        get_login_providers(module, login_providers_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
