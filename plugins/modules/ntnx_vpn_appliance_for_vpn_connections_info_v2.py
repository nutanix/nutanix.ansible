#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpn_appliance_for_vpn_connections_info_v2
short_description: Fetch third-party VPN appliance information for a VPN connection in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about VpnApplianceForVpnConnection in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VpnApplianceForVpnConnection.
  - If C(ext_id) is not provided, list multiple VpnApplianceForVpnConnection optionally filtered / paginated.
  - The Nutanix PC v4 API generates a vendor-specific configuration script
    (Cisco ASA, PaloAlto, Juniper, SonicWall, VyOS, CheckPoint, Fortinet,
    ...) for a given VPN connection so administrators can align the
    third-party VPN gateway with the Nutanix side of the tunnel.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List third-party VPN appliances for a VPN connection) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - >-
      B(Get third-party VPN appliance configuration by ext_id) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  vpn_connection_ext_id:
    description:
      - External ID of the parent VPN connection whose supported third-party
        VPN appliances are being queried.
    type: str
    required: true
  ext_id:
    description:
      - External ID of a specific third-party VPN appliance.
      - When provided, the module downloads the vendor-specific config text
        for that appliance under the given C(vpn_connection_ext_id).
      - When not provided, the module lists every third-party VPN appliance
        for which a configuration is available under the given
        C(vpn_connection_ext_id).
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
- name: List all third-party VPN appliances available for a VPN connection
  nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0"
  register: appliances
  ignore_errors: true

- name: List third-party VPN appliances filtered by name
  nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0"
    filter: "name eq 'Cisco ASA'"
  register: cisco_appliance
  ignore_errors: true

- name: Fetch third-party VPN appliance config text using ext_id
  nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0"
    ext_id: "b2037b0e-af4c-38f7-8c12-6ed629be12af"
  register: cisco_config
  ignore_errors: true

- name: List third-party VPN appliances with a page size
  nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0"
    limit: 5
  register: appliances_paginated
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VpnApplianceForVpnConnection info v4 API.
    - When C(ext_id) is provided, a dict containing the downloaded
      vendor-specific configuration text (under C(configuration)) is returned.
    - When C(ext_id) is not provided, a list of supported third-party VPN
      appliances is returned; each item is a dict describing the appliance
      (e.g. C(name), C(version), C(ext_id)).
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "b2037b0e-af4c-38f7-8c12-6ed629be12af",
        "links": null,
        "metadata": null,
        "name": "Cisco ASA",
        "tenant_id": null,
        "version": "9.7+"
      },
      {
        "ext_id": "3a271c2a-30b0-3041-af1a-45b9adeb90b8",
        "links": null,
        "metadata": null,
        "name": "PaloAlto",
        "tenant_id": null,
        "version": "8.0+"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always False for info modules.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the third-party VPN appliance whose configuration was downloaded.
  returned: when ext_id is provided
  type: str
  sample: "b2037b0e-af4c-38f7-8c12-6ed629be12af"

vpn_connection_ext_id:
  description: External ID of the parent VPN connection.
  returned: always
  type: str
  sample: "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0"

total_available_results:
  description: The total number of third-party VPN appliances available for the given VPN connection.
  type: int
  returned: when listing multiple appliances
  sample: 7

error:
  description: This field holds information about errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching third-party VPN appliance info for VPN connection"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpn_connections_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_vpn_appliance_for_vpn_connection,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        vpn_connection_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_vpn_appliance_by_ext_id(module, api_instance, result):
    """Fetch a specific third-party VPN appliance config via ext_id.

    The Nutanix PC v4 API returns the vendor config as a ``text/plain``
    payload. We normalize it into a dict so the module response shape stays
    consistent with the list path.
    """
    vpn_connection_ext_id = module.params.get("vpn_connection_ext_id")
    ext_id = module.params.get("ext_id")
    config_text = get_vpn_appliance_for_vpn_connection(
        module, api_instance, vpn_connection_ext_id, ext_id
    )

    if isinstance(config_text, bytes):
        try:
            config_text = config_text.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            config_text = str(config_text)
    elif config_text is not None and not isinstance(config_text, str):
        config_text = str(config_text)

    result["ext_id"] = ext_id
    result["vpn_connection_ext_id"] = vpn_connection_ext_id
    result["response"] = {
        "vpn_connection_ext_id": vpn_connection_ext_id,
        "ext_id": ext_id,
        "configuration": config_text,
    }


def list_vpn_appliances(module, api_instance, result):
    """List all supported third-party VPN appliances for a VPN connection."""
    vpn_connection_ext_id = module.params.get("vpn_connection_ext_id")
    result["vpn_connection_ext_id"] = vpn_connection_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating third-party VPN appliance info spec", **result
        )

    kwargs.pop("_select", None)

    try:
        resp = api_instance.list_vpn_appliances_by_vpn_connection_id(
            vpnConnectionExtId=vpn_connection_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching third-party VPN "
                "appliance info for VPN connection"
            ),
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "vpn_connection_ext_id": None,
    }
    api_instance = get_vpn_connections_api_instance(module)
    if module.params.get("ext_id"):
        get_vpn_appliance_by_ext_id(module, api_instance, result)
    else:
        list_vpn_appliances(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
