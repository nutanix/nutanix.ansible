#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_config_info_v2
short_description: Fetch LCM Configurations
description:
    - This module fetches LCM configurations.
    - Fetch LCM configurations using cluster external ID.
version_added: 2.0.0
author:
    - Abhinav Bansal (@abhinavbansal29)
options:
    ext_id:
        description:
            - The external ID of the cluster.
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
    description: The response from the LCM config API
    type: dict
    returned: always
    sample:
        {}
ext_id:
    description: The external ID of the cluster
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: bool
    returned: always
    sample: false
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.lcm.api_client import get_config_api_instance  # noqa: E402
from ..module_utils.v4.lcm.helpers import get_lcm_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )

    return module_args


def lcm_config(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = get_lcm_config(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
    }

    api_instance = get_config_api_instance(module)

    lcm_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
