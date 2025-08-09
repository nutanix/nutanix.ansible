#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_floating_ips_info_v2
short_description: floating_ip info module
version_added: 2.0.0
description:
    - Get floating_ips info
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - floating_ip external ID
        type: str
    expand:
        description:
            - flag to expand related resources for the floating IP
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: List Floating_ips
  nutanix.ncp.ntnx_floating_ips_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Get floating_ips using ext_id
  nutanix.ncp.ntnx_floating_ips_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
"""
RETURN = r"""
response:
  description:
      - The response from the floating ips v4 API.
      - it can be floating ip or list of floating ips as per spec.
  returned: always
  type: dict
  sample: {
    "data": [
        {
            "extId": "00000000-0000-0000-0000-000000000000",
            "metadata": {
                "ownerReferenceId": "00000000-0000-0000-0000-000000000000",
                "ownerUserName": "admin"
            },
            "floatingIp": {
                "ipv4": {
                    "value": "192.168.1.69"
                }
            },
            "externalSubnetReference": "00000000-0000-0000-0000-000000000000"
        }
    ],
    "metadata": {
        "flags": [
            {
                "name": "hasError",
                "value": false
            },
            {
                "name": "isPaginated",
                "value": false
            }
        ],
        "totalAvailableResults": 1
    }
}

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false

ext_id:
    description:
        - The external ID of the floating ip when specific floating ip is fetched.
    type: str
    returned: always
    sample: "33dba56c-f123-4ec6-8b38-901e1cf716c2"
total_available_results:
    description:
        - The total number of available floating IPs in PC.
    type: int
    returned: when all floating IPs are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_floating_ip_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
    )

    return module_args


def get_floating_ips(module, result):
    floating_ips = get_floating_ip_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating floating_ips info Spec", **result)

    try:
        resp = floating_ips.list_floating_ips(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching floating_ips info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    if not resp or not getattr(resp, "data", []):
        result["response"] = []
    else:
        result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_floating_ip(module, result):
    floating_ips = get_floating_ip_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = floating_ips.get_floating_ip_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching floating IP info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_floating_ip(module, result)
    else:
        get_floating_ips(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
