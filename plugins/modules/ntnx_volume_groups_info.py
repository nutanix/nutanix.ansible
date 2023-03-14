#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_info
short_description: volume_group info module
version_added: 1.9.0
description: 'Get volume_group info'
options:
    volume_group_uuid:
        description:
            - volume_group UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      # - nutanix.ncp.ntnx_info
author:
 - Prem Karat (@premkarat)
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
  - name: List volume_group using name filter criteria
    ntnx_volume_groups_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter:
        name: "{{ volume_group.name }}"
      kind: volume_group
    register: result

  - name: List volume_group using length, offset, sort order and name sort attribute
    ntnx_volume_groups_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      length: 10
      offset: 1
      sort_order: "ASCENDING"
      sort_attribute: "name"
    register: result
"""
RETURN = r"""
metadata:
  description: Metadata for volume_group list output
  returned: always
  type: dict
  sample: {}
entities:
  description: volume_group intent response
  returned: always
  type: list
  sample: {
  "entities": [
    {
      "status": {
        "description": "string",
        "state": "string",
        "message_list": [
          {
            "message": "string",
            "reason": "string",
            "details": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          }
        ],
        "cluster_reference": {
          "kind": "cluster",
          "name": "string",
          "uuid": "string"
        },
        "resources": {
          "flash_mode": "string",
          "iscsi_target_name": "string",
          "enabled_authentications": "string",
          "attachment_list": [
            {
              "iscsi_initiator_network_id": "string",
              "enabled_authentications": "string",
              "vm_reference": {
                "kind": "vm",
                "name": "string",
                "uuid": "string"
              },
              "iscsi_initiator_name": "string"
            }
          ],
          "created_by": "string",
          "parent_reference": {
            "url": "string",
            "kind": "string",
            "uuid": "string",
            "name": "string"
          },
          "sharing_status": "string",
          "disk_list": [
            {
              "index": 0,
              "storage_container_uuid": "string",
              "disk_size_mib": 0,
              "disk_size_bytes": 0,
              "uuid": "string"
            }
          ],
          "size_bytes": 0,
          "usage_type": "string",
          "load_balance_vm_attachments": true,
          "is_hidden": true,
          "size_mib": 0,
          "iscsi_target_prefix": "string"
        },
        "name": "string"
      },
      "spec": {
        "name": "string",
        "description": "string",
        "resources": {
          "flash_mode": "string",
          "load_balance_vm_attachments": true,
          "created_by": "string",
          "iscsi_target_prefix": "string",
          "parent_reference": {
            "url": "string",
            "kind": "string",
            "uuid": "string",
            "name": "string"
          },
          "sharing_status": "string",
          "attachment_list": [
            {
              "iscsi_initiator_network_id": "string",
              "client_secret": "string",
              "vm_reference": {
                "kind": "vm",
                "name": "string",
                "uuid": "string"
              },
              "iscsi_initiator_name": "string"
            }
          ],
          "usage_type": "string",
          "target_secret": "string",
          "is_hidden": true,
          "disk_list": [
            {
              "index": 16383,
              "data_source_reference": {
                "url": "string",
                "kind": "string",
                "uuid": "string",
                "name": "string"
              },
              "disk_size_mib": 0,
              "disk_size_bytes": 0,
              "storage_container_uuid": "string"
            }
          ]
        },
        "cluster_reference": {
          "kind": "cluster",
          "name": "string",
          "uuid": "string"
        }
      },
      "api_version": "3.1.0",
      "metadata": {
        "last_update_time": "2023-03-13T11:41:16.626Z",
        "use_categories_mapping": false,
        "kind": "volume_group",
        "uuid": "string",
        "project_reference": {
          "kind": "project",
          "name": "string",
          "uuid": "string"
        },
        "creation_time": "2023-03-13T11:41:16.626Z",
        "spec_version": 0,
        "spec_hash": "string",
        "categories_mapping": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "should_force_translate": true,
        "entity_version": "string",
        "owner_reference": {
          "kind": "user",
          "name": "string",
          "uuid": "string"
        },
        "categories": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "name": "string"
      }
    }
  ],
  "api_version": "3.1.0",
  "metadata": {
    "kind": "volume_group",
    "total_matches": 0,
    "sort_attribute": "string",
    "filter": "string",
    "length": 0,
    "sort_order": "string",
    "offset": 0
  }
}
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.volume_groups import VolumeGroup  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        volume_group_uuid=dict(type="str"),
    )

    return module_args


def get_volume_group(module, result):
    volume_group = VolumeGroup(module)
    volume_group_uuid = module.params.get("volume_group_uuid")
    resp = volume_group.read(volume_group_uuid)

    result["response"] = resp


def get_volume_groups(module, result):
    volume_group = VolumeGroup(module)

    resp = volume_group.read()

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("volume_group_uuid"):
        get_volume_group(module, result)
    else:
        get_volume_groups(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
