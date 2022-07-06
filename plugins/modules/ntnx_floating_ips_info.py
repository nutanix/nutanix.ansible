#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_floating_ips_info
short_description: Floting ips info module
version_added: 1.0.0
description: 'Get floating_ip info'
options:
      kind:
        description:
          - The kind name
        type: str
        default: floating_ip
      fip_uuid:
        description:
            - Floting ip UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List Floating ip using ip starts with 10 filter criteria
    ntnx_floating_ips_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        floating_ip: "10."
      kind: floating_ip
    register: result

  - name: List Floating ip using length, offset, sort order and floating_ip sort attribute
    ntnx_floating_ips_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 3
      offset: 0
      sort_order: "DESCENDING"
      sort_attribute: "floating_ip"
    register: result

"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for floating_ip list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "filter": "floating_ip==10.*",
            "kind": "floating_ip",
            "length": 1,
            "offset": 0,
            "total_matches": 1
        }
        }
entities:
  description: Floating_ip intent response
  returned: always
  type: list
  sample: {
    "entities": [
            {
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-03-09T10:13:58Z",
                    "kind": "floating_ip",
                    "last_update_time": "2022-03-09T10:14:00Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec_version": 0,
                    "uuid": "d578ce7a-7610-4581-b815-f44476b3613e"
                },
                "spec": {
                    "resources": {
                        "external_subnet_reference": {
                            "kind": "subnet",
                            "uuid": "946d59d1-65fe-48cc-9882-e93439404e89"
                        }
                    }
                },
                "status": {
                    "execution_context": {
                        "task_uuids": [
                            "739eb335-db26-472c-a27f-d9dd10de8241"
                        ]
                    },
                    "name": "",
                    "resources": {
                        "external_subnet_reference": {
                            "kind": "subnet",
                            "uuid": "946d59d1-65fe-48cc-9882-e93439404e89"
                        },
                        "floating_ip": "10.44.3.203"
                    },
                    "state": "COMPLETE"
                }
            }
        ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.floating_ips import FloatingIP  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        fip_uuid=dict(type="str"),
        kind=dict(type="str", default="floating_ip"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_fip(module, result):
    floating_ip = FloatingIP(module)
    floating_ip_uuid = module.params.get("fip_uuid")
    resp = floating_ip.read(floating_ip_uuid)

    result["response"] = resp


def get_fips(module, result):
    floating_ip = FloatingIP(module)
    spec, error = floating_ip.get_info_spec()

    resp = floating_ip.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("fip_uuid"):
        get_fip(module, result)
    else:
        get_fips(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
