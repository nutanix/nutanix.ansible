#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_hosts_info
short_description: host  info module
version_added: 1.4.0
description: 'Get host info'
options:
      kind:
        description:
          - The kind name
        type: str
        default: host
      host_uuid:
        description:
            - host UUID
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
  - name: List hosts using priority filter criteria
    ntnx_hosts_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        priority: 2
      kind: host
    register: result

  - name: List hosts using length, offset, sort order and priority sort attribute
    ntnx_hosts_info:
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
  description: Metadata for hosts list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "host",
            "length": 6,
            "offset": 0,
            "sort_attribute": "",
            "sort_order": "",
            "total_matches": 6
        }
        }
entities:
  description: host intent response
  returned: always
  type: list
  sample: {
    "entities": [
            {
                "metadata": {
                    "categories": {},
                    "categories_mapping": {},
                    "creation_time": "",
                    "kind": "host",
                    "last_update_time": "",
                    "spec_hash": "",
                    "spec_version": 0,
                    "uuid": ""
                },
                "spec": {
                    "resources": {
                        "controller_vm": {
                            "ip": "",
                            "oplog_usage": {
                                "oplog_disk_pct": "",
                                "oplog_disk_size": ""
                            }
                        }
                    }
                },
                "status": {
                    "cluster_reference": {
                        "kind": "cluster",
                        "uuid": ""
                    },
                    "resources": {
                        "block": {
                            "block_model": "null",
                            "block_serial_number": "null"
                        },
                        "controller_vm": {
                            "ip": "",
                            "oplog_usage": {
                                "oplog_disk_pct": "",
                                "oplog_disk_size": ""
                            }
                        },
                        "gpu_list": [],
                        "host_disks_reference_list": [
                            {
                                "kind": "disk",
                                "uuid": ""
                            },
                            {
                                "kind": "disk",
                                "uuid": ""
                            },
                            {
                                "kind": "disk",
                                "uuid": ""
                            },
                            {
                                "kind": "disk",
                                "uuid": ""
                            }
                        ],
                        "host_nics_id_list": [],
                        "host_type": "HYPER_CONVERGED",
                        "rackable_unit_reference": {
                            "kind": "rackable_unit",
                            "uuid": ""
                        },
                        "serial_number": ""
                    },
                    "state": "COMPLETE"
                }
            }
            ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.hosts import Host  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        host_uuid=dict(type="str"),
        kind=dict(type="str", default="host"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_host(module, result):
    host = Host(module)
    host_uuid = module.params.get("host_uuid")
    resp = host.read(host_uuid)

    result["response"] = resp


def get_hosts(module, result):
    host = Host(module)
    spec, error = host.get_info_spec()

    resp = host.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("host_uuid"):
        get_host(module, result)
    else:
        get_hosts(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
