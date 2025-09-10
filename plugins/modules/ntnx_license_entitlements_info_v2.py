#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_license_entitlements_info_v2
short_description: Shows the effective license entitlements
description: 
    - Shows the effective license entitlements.
    - This module uses PC v4 APIs based SDKs.
version_added: "2.4.0"
author:
  - Abhinav Bansal (@abhinavbansal29)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix List license entitlements API.
  type: dict
  returned: always
  sample:
changed:
    description:
        - Indicates whether the module has made any changes.
    type: bool
    returned: always
    sample: false
total_available_results:
    description:
        - The total number of available license entitlements.
    type: int
    returned: when all license entitlements are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.licensing.api_client import (  # noqa: E402
    get_licensing_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def license_entitlements_info(module, licensing_api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating license entitlements info Spec", **result
        )
    try:
        resp = licensing_api_instance.list_entitlements(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching license entitlements info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=dict(),
        supports_check_mode=False,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
    }

    licensing_api_instance = get_licensing_api_instance(module)

    license_entitlements_info(module, licensing_api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
