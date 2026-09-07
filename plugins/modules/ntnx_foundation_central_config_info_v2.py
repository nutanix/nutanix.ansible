#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_config_info_v2
short_description: Fetch Foundation Central configuration
description:
    - This module fetches the Foundation Central (FC) service configuration.
    - The Foundation Central configuration is a singleton resource, so this module
      always returns the single configuration object.
version_added: 2.6.0
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
notes:
    - This module talks to the Foundation Central VM (FCVM)/Foundation endpoint,
      B(not) Prism Central. Set C(nutanix_host)/C(nutanix_port) to the
      FCVM/Foundation endpoint (default port C(9440)).
    - >-
      B(Get the Foundation Central configuration.) -
      Requires an Admin/Viewer role on the Foundation Central VM (FCVM).
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options: {}
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get Foundation Central configuration
  nutanix.ncp.ntnx_foundation_central_config_info_v2:
    nutanix_host: <fcvm_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: fc_config_info
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix Foundation Central config info v4 API (served by FCVM/Foundation).
        - Foundation Central configuration is a singleton, so a single configuration dict is returned.
    type: dict
    returned: always
    sample:
        {
            "ahv_installation_timeout_minutes": 50,
            "aos_download_timeout_minutes": 60,
            "commit_id": "8701b044",
            "tls_certificate_fingerprint": "0789169a1c913336750712ad51ce22a27abcb6ba3a1bbce8a3155decf53c8757",
            "version": "2.2"
        }
changed:
    description: Whether the module made any changes. Always false for info modules.
    type: bool
    returned: always
    sample: false
msg:
    description: A status or informational message.
    returned: When applicable
    type: str
    sample: "Foundation Central config fetched successfully"
error:
    description: Error details, if any error occurred during the task execution.
    type: str
    returned: When an error occurs
    sample: "Api Exception raised while fetching Foundation Central config info"
failed:
    description: Indicates whether the task failed.
    type: bool
    returned: When something fails
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_foundation_central_config_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_foundation_central_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict()
    return module_args


def get_foundation_central_config_info(module, api_instance, result):
    """Fetch the singleton Foundation Central configuration."""
    resp = get_foundation_central_config(module, api_instance)
    result["response"] = strip_internal_attributes(resp.data.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
    }

    api_instance = get_foundation_central_config_api_instance(module)
    get_foundation_central_config_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
