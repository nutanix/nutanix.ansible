#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_pbrs_info
short_description: PBR  info module
version_added: 1.0.0
description: 'Get pbr info'
options:
      kind:
        description:
          - The kind name
        type: str
        default: routing_policy
      pbr_uuid:
        description:
            - PBR UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
 - Dina AbuHijleh (@dina-abuhijleh)
"""
EXAMPLES = r"""
  - name: List pbrs using priority filter criteria
    ntnx_pbrs_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        priority: "2"
      kind: routing_policy
    register: result

  - name: List pbrs using length, offset, sort order and priority sort attribute
    ntnx_pbrs_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 2
      offset: 0
      sort_order: "ASCENDING"
      sort_attribute: "priority"
    register: result

"""
RETURN = r"""
api_version:
  description: API Version of the Nutanix v3 API framework.
  returned: always
  type: str
  sample: "3.1"
metadata:
  description: Metadata for pbrs list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "routing_policy",
            "length": 6,
            "offset": 0,
            "sort_attribute": "priority",
            "sort_order": "ASCENDING",
            "total_matches": 6
        }
        }
entities:
  description: PBR intent response
  returned: always
  type: list
  sample: {
    "entities": [
            {
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "2022-03-09T08:37:16Z",
                    "kind": "routing_policy",
                    "last_update_time": "2022-03-09T08:41:37Z",
                    "owner_reference": {
                        "kind": "user",
                        "name": "admin",
                        "uuid": "00000000-0000-0000-0000-000000000000"
                    },
                    "spec_version": 0,
                    "uuid": "11a80bee-2bca-4ce8-8662-6a4e4b44b4f3"
                },
                "spec": {
                    "name": "virtual-network-deny-all",
                    "resources": {
                        "action": {
                            "action": "DENY"
                        },
                        "destination": {
                            "address_type": "ALL"
                        },
                        "priority": 1,
                        "protocol_type": "ALL",
                        "source": {
                            "address_type": "ALL"
                        },
                        "vpc_reference": {
                            "kind": "vpc",
                            "uuid": "7ee05b9d-4021-4f57-8a03-df9503adea9d"
                        }
                    }
                },
                "status": {
                    "name": "virtual-network-deny-all",
                    "resources": {
                        "action": {
                            "action": "DENY"
                        },
                        "destination": {
                            "address_type": "ALL"
                        },
                        "priority": 1,
                        "protocol_type": "ALL",
                        "routing_policy_counters": {
                            "byte_count": 0,
                            "packet_count": 0
                        },
                        "source": {
                            "address_type": "ALL"
                        },
                        "vpc_reference": {
                            "kind": "vpc",
                            "name": "integration_test_vpc",
                            "uuid": "7ee05b9d-4021-4f57-8a03-df9503adea9d"
                        }
                    },
                    "state": "COMPLETE"
                }
            }
        ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.pbrs import Pbr  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        pbr_uuid=dict(type="str"),
        kind=dict(type="str", default="routing_policy"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_pbr(module, result):
    pbr = Pbr(module)
    pbr_uuid = module.params.get("pbr_uuid")
    resp = pbr.read(pbr_uuid)

    result["response"] = resp


def get_pbrs(module, result):
    pbr = Pbr(module)
    spec, error = pbr.get_info_spec()

    resp = pbr.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("pbr_uuid"):
        get_pbr(module, result)
    else:
        get_pbrs(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
