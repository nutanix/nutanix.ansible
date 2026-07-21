#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpn_appliance_for_vpn_connection_v2
short_description: Download third-party VPN appliance configuration for a VPN connection in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module downloads the third-party VPN appliance configuration text for a
    specific appliance under a Nutanix Prism Central VPN connection.
  - The Nutanix PC v4 networking API generates a vendor-specific
    C(text/plain) configuration script (e.g. for Cisco ASA, PaloAlto, Juniper,
    SonicWall, VyOS, CheckPoint, Fortinet) that the network administrator can
    apply directly on the on-premises third-party VPN gateway to align the
    IPSec and BGP settings with the Nutanix side of the tunnel.
  - The list of supported appliances (and their C(ext_id)s) for a given VPN
    connection can be discovered via
    M(nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get third-party VPN appliance configuration) -
      Required Roles: Consumer, Developer, Network Infra Admin, Operator, Prism Admin, Prism Viewer, Project Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module will download the
        third-party VPN appliance configuration for the given
        C(vpn_connection_ext_id) and C(ext_id).
      - Only C(present) is supported because the API is read-only for this
        entity (there is no create/update/delete operation for a
        third-party VPN appliance configuration).
    type: str
    choices:
      - present
    default: present
  vpn_connection_ext_id:
    description:
      - External ID of the parent VPN connection.
      - Obtainable via M(nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2)
        or from the Prism Central VPN connections page.
    type: str
    required: true
  ext_id:
    description:
      - External ID of the third-party VPN appliance whose configuration
        should be downloaded.
      - Discoverable via M(nutanix.ncp.ntnx_vpn_appliance_for_vpn_connections_info_v2)
        with only C(vpn_connection_ext_id) supplied.
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
- name: Download third-party VPN appliance configuration for a VPN connection
  nutanix.ncp.ntnx_vpn_appliance_for_vpn_connection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    vpn_connection_ext_id: "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0"
    ext_id: "b2037b0e-af4c-38f7-8c12-6ed629be12af"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response returned by the Nutanix PC VpnApplianceForVpnConnection v4 API.
    - Contains the raw vendor-specific configuration text under
      C(configuration) plus the C(vpn_connection_ext_id) and C(ext_id) that
      identify the appliance whose configuration was downloaded.
  returned: always
  type: dict
  sample:
    {
      "vpn_connection_ext_id": "8a938cf5-2c9a-4c9b-8f01-8c9f8e40e6c0",
      "ext_id": "b2037b0e-af4c-38f7-8c12-6ed629be12af",
      "configuration": "# Cisco ASA 9.7 and above\n# This configuration consists of IPSec VPN and BGP configuration...\n"
    }

ext_id:
  description:
    - The external ID of the third-party VPN appliance whose configuration
      was downloaded.
  returned: always
  type: str
  sample: "b2037b0e-af4c-38f7-8c12-6ed629be12af"

task_ext_id:
  description:
    - The external ID of the task.
    - The v4 API endpoint is a synchronous read; no asynchronous task is
      created, so this is C(null) for a successful download.
  returned: always
  type: str
  sample: null

changed:
  description: This indicates whether the module resulted in any changes.
  returned: always
  type: bool
  sample: false

skipped:
  description: This indicates whether the module was skipped (e.g. in check mode).
  returned: always
  type: bool
  sample: false

error:
  description: This field holds the error details if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This field indicates whether the module failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while fetching third-party VPN appliance configuration for VPN connection"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpn_connections_api_instance,
)
from ..module_utils.v4.network.helpers import (  # noqa: E402
    get_vpn_appliance_for_vpn_connection,
)

SDK_IMP_ERROR = None
try:
    # pylint: disable=unused-import
    import ntnx_networking_py_client  # noqa: E402, F401
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        vpn_connection_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def download_vpn_appliance_config(module, api_instance, result):
    """Download the third-party VPN appliance vendor config for a VPN connection.

    The Nutanix PC v4 endpoint
    ``/networking/v4.3/config/vpn-connections/{vpnConnectionExtId}/vpn-vendor-configs/{extId}``
    returns the configuration as a plain-text CLI snippet. The SDK exposes it
    through :py:meth:`VpnConnectionsApi.get_vpn_appliance_for_vpn_connection_by_id`
    with ``response_type='str'``.
    """
    vpn_connection_ext_id = module.params.get("vpn_connection_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["response"] = {
            "vpn_connection_ext_id": vpn_connection_ext_id,
            "ext_id": ext_id,
            "configuration": None,
        }
        result["msg"] = (
            "Third-party VPN appliance configuration for VPN connection "
            "'{0}' and appliance '{1}' would be downloaded.".format(
                vpn_connection_ext_id, ext_id
            )
        )
        return

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

    result["response"] = {
        "vpn_connection_ext_id": vpn_connection_ext_id,
        "ext_id": ext_id,
        "configuration": config_text,
    }


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
        "failed": False,
    }
    api_instance = get_vpn_connections_api_instance(module)
    download_vpn_appliance_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
