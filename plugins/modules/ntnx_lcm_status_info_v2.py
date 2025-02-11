#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_lcm_status_v2
short_description: Fetch LCM Status
description: Fetch LCM Status like current version, available version, etc.
version_added: "2.0.0"
author:
  - George Ghawali (@george-ghawali)
options:
  ext_id:
    description:
      - The external ID of the Nutanix PC Cluster.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC LCM Status API.
    - It contains details like current version, available version, etc.
  type: dict
  returned: always
  sample:
    {
      "frameworkVersion":
        {
          "currentVersion": "3.1.52092",
          "availableVersion": "3.0.1.1.53478",
          "isUpdateNeeded": true,
        },
      "inProgressOperation": {},
      "isCancelIntentSet": false,
    }
changed:
    description:
        - Indicates whether the module has made any changes.
    type: bool
    returned: always
    sample: false
error:
    description:
        - The error message if the module fails.
    type: str
    returned: always
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_status_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_lcm_status  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=False),
    )

    return module_args


def lcm_status(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = get_lcm_status(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():

    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }

    api_instance = get_status_api_instance(module)

    lcm_status(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
