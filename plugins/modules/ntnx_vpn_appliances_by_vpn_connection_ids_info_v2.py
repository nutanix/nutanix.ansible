#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpn_appliances_by_vpn_connection_ids_info_v2
short_description: Fetch info about supported third-party VPN appliances for a Nutanix VPN connection
version_added: 2.5.0
description:
  - This module allows you to fetch information about VpnAppliancesByVpnConnectionId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VpnAppliancesByVpnConnectionId. In that case
    the raw vendor configuration payload for that appliance is returned as a string in C(response).
  - If C(ext_id) is not provided, list multiple VpnAppliancesByVpnConnectionId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List third-party VPN appliances for a VPN connection) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, VPC Admin
    - >-
      B(Get third-party VPN appliance configuration) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer,
      Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  vpn_connection_ext_id:
    description:
      - External ID of the VPN connection whose supported third-party VPN appliances should be listed.
    type: str
    required: true
  ext_id:
    description:
      - External ID of a specific third-party VPN appliance.
      - When provided, the module fetches the vendor configuration payload for that appliance
        (returned as a plain-text string in C(response)).
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: List all supported third-party VPN appliances for a VPN connection
  nutanix.ncp.ntnx_vpn_appliances_by_vpn_connection_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true

- name: List VPN appliances with a filter
  nutanix.ncp.ntnx_vpn_appliances_by_vpn_connection_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    filter: "startswith(name, 'Palo')"
  register: result
  ignore_errors: true

- name: List VPN appliances with limit and ordering
  nutanix.ncp.ntnx_vpn_appliances_by_vpn_connection_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    limit: 1
    orderby: "name asc"
  register: result
  ignore_errors: true

- name: Fetch a specific third-party VPN appliance configuration
  nutanix.ncp.ntnx_vpn_appliances_by_vpn_connection_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    vpn_connection_ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    ext_id: "9f4b3d1c-6a15-4c8b-9d12-6b6b9f13a1b2"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VpnAppliancesByVpnConnectionId info v4 API.
    - It can be a single VpnAppliancesByVpnConnectionId if external ID is provided (in that case the
      vendor configuration payload is returned as a plain-text string).
    - List of multiple VpnAppliancesByVpnConnectionId if external ID is not provided with optional
      filter or limit.
  returned: always
  type: dict
  sample:
    - ext_id: "9f4b3d1c-6a15-4c8b-9d12-6b6b9f13a1b2"
      name: "PaloAlto"
      version: "10.0"
      links: null
      metadata: null
      tenant_id: null

changed:
  description: This indicates whether the task resulted in any changes. Always false for this module.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VPN appliances info"

error:
  description: Error details when an error occurs.
  type: str
  returned: when an error occurs

failed:
  description: Whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the third-party VPN appliance whose vendor config was fetched.
  type: str
  returned: when external ID is provided
  sample: "9f4b3d1c-6a15-4c8b-9d12-6b6b9f13a1b2"

vpn_connection_ext_id:
  description: External ID of the VPN connection whose appliances were queried.
  type: str
  returned: always
  sample: "2e40ff57-20aa-4d2b-b179-298db969c20d"

total_available_results:
  description: The total number of available VPN appliances for the VPN connection.
  type: int
  returned: when appliances are listed
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpn_connections_api_instance,
)
from ..module_utils.v4.network.helpers import get_vpn_appliance_config  # noqa: E402
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
    vpn_connection_ext_id = module.params.get("vpn_connection_ext_id")
    ext_id = module.params.get("ext_id")
    result["vpn_connection_ext_id"] = vpn_connection_ext_id
    result["ext_id"] = ext_id
    resp = get_vpn_appliance_config(
        module=module,
        api_instance=api_instance,
        vpn_connection_ext_id=vpn_connection_ext_id,
        ext_id=ext_id,
    )
    result["response"] = resp


def list_vpn_appliances(module, api_instance, result):
    vpn_connection_ext_id = module.params.get("vpn_connection_ext_id")
    result["vpn_connection_ext_id"] = vpn_connection_ext_id
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating VPN appliances info spec", **result)
    try:
        resp = api_instance.list_vpn_appliances_by_vpn_connection_id(
            vpnConnectionExtId=vpn_connection_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VPN appliances info",
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
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
