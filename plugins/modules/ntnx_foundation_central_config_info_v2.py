#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_config_info_v2
short_description: Fetch Foundation Central configuration from FCVM/Foundation
description:
    - This module fetches Foundation Central configuration.
    - Foundation Central config is a singleton Get API with no list, filter,
      or get-by-ID parameters.
    - This module talks to B(Foundation Central / FCVM), not Prism Central.
      Set C(nutanix_host) / C(nutanix_port) to the FCVM endpoint
      (for example C(FOUNDATION_ENDPOINT) / C(FOUNDATION_PORT)).
version_added: 2.6.0
notes:
    - >-
      This module requires Viewer or Admin role on Foundation Central / FCVM
      for the user performing the operation.
    - >-
      Target host is Foundation Central / FCVM (lifecycle Foundation Central
      Config API), not Prism Central.
    - Filter, limit, page, orderby, and select are not supported by this API.
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
options: {}
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Get Foundation Central config from FCVM
  nutanix.ncp.ntnx_foundation_central_config_info_v2:
    nutanix_host: "<foundation_central_ip>"
    nutanix_port: 9440
    nutanix_username: "<user>"
    nutanix_password: "<pass>"
    validate_certs: false
  register: fcc_config_info
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix foundation central config info v4 API
          (host is FCVM/Foundation, not Prism Central).
        - Always a single foundation central config object (singleton GET).
        - List/filter/limit are not supported by this API.
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
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
error:
    description: Error details
    type: str
    returned: always
    sample: null
failed:
    description: Whether the module failed
    type: bool
    returned: when something fails
    sample: false
msg:
    description: Status or error message
    type: str
    returned: when applicable
    sample: "Api Exception raised while fetching Foundation Central config"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_foundation_central_config_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_foundation_central_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as lifecycle_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as lifecycle_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    return dict()


def get_foundation_central_config_info(module, api_instance, result):
    """
    Fetch the singleton Foundation Central configuration.
    """
    resp = get_foundation_central_config(module, api_instance)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    if SDK_IMP_ERROR:
        module.fail_json(
            msg="Missing required library ntnx_lifecycle_py_client",
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "error": None,
    }

    # Ensure SDK import is retained for sdk_mock fallback / import sanity.
    if lifecycle_sdk is None:
        module.fail_json(msg="Lifecycle SDK is unavailable")

    api_instance = get_foundation_central_config_api_instance(module)
    get_foundation_central_config_info(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
