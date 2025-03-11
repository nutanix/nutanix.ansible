#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_address_groups_info_v2
short_description: Get address groups info
version_added: 2.0.0
description:
    - Fetch specific address group info using external ID
    - Fetch list of multiple address groups info if external ID is not provided with optional filters
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID to fetch specific address group info
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - George Ghawali (@george-ghawali)
"""
EXAMPLES = r"""
- name: Fetch address groups using external id
  nutanix.ncp.ntnx_address_groups_info_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    ext_id: "{{ test_address_groups_uuid }}"
  register: result

- name: List all address groups
  nutanix.ncp.ntnx_address_groups_info_v2:
    state: present
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
  register: result
"""
RETURN = r"""
response:
  description:
      - Response for fetching address groups info
      - One address group info if External ID is provided
      - List of multiple address groups info if External ID is not provided
  returned: always
  type: dict
  sample:
        {
            "created_by": "00000000-0000-0000-0000-000000000000",
            "description": "test-ansible-group-3-desc",
            "ext_id": "63311404-8b2e-4dbf-9e33-7848cc88d330",
            "ip_ranges": null,
            "ipv4_addresses": [
                {
                    "prefix_length": 32,
                    "value": "10.1.4.1"
                }
            ],
            "links": null,
            "name": "yclaDaQKtEGIansible-ag1",
            "policy_references": null,
            "tenant_id": null
            }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_address_groups_api_instance,
)
from ..module_utils.v4.flow.helpers import get_address_group  # noqa: E402
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
    )

    return module_args


def get_address_group_using_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    address_groups = get_address_groups_api_instance(module)
    resp = get_address_group(module, address_groups, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_address_groups(module, result):
    address_groups = get_address_groups_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating address groups info Spec", **result)

    try:
        resp = address_groups.list_address_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching address groups info",
        )

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
    result = {"changed": False, "response": None}
    if module.params.get("ext_id"):
        get_address_group_using_ext_id(module, result)
    else:
        get_address_groups(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
