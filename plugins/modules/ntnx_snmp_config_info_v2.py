#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_snmp_config_info_v2
short_description: Fetch SNMP configuration of a Nutanix cluster
description:
  - This module fetches SNMP configuration of a Nutanix cluster.
  - Fetch SNMP config using the cluster external ID.
  - Returns SNMP status, users, traps, and transport details.
  - This module uses PC v4 APIs based SDKs.
version_added: "2.6.0"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster to fetch SNMP config from.
    type: str
    required: true
author:
  - George Ghawali (@george-ghawali)
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
"""

EXAMPLES = r"""
- name: Fetch SNMP config for a cluster
  nutanix.ncp.ntnx_snmp_config_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
  register: result
"""

RETURN = r"""
response:
  description:
    - The SNMP configuration of the cluster.
    - Includes status, users, traps, and transport details.
  type: dict
  returned: always
  sample:
    {
      "ext_id": null,
      "is_enabled": true,
      "links": null,
      "tenant_id": null,
      "transports": [
          {
              "port": 165,
              "protocol": "UDP6"
          }
      ],
      "traps": [
          {
              "address": {
                  "ipv4": {
                      "prefix_length": 32,
                      "value": "10.0.0.1"
                  },
                  "ipv6": null
              },
              "community_string": "public",
              "engine_id": null,
              "ext_id": "e4ef5d18-645f-4a35-a5be-93a3dab5db45",
              "links": null,
              "port": 162,
              "protocol": "UDP",
              "reciever_name": null,
              "should_inform": null,
              "tenant_id": null,
              "username": null,
              "version": "V2"
          }
      ],
      "users": [
          {
              "auth_key": null,
              "auth_type": "MD5",
              "ext_id": "84a60289-e6b6-4814-b882-7858f5485a24",
              "links": null,
              "priv_key": null,
              "priv_type": "DES",
              "tenant_id": null,
              "username": "snmp_user_all_ansible_test_EriQKlYVhfgw"
          }
      ]
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

error:
  description: Error message if something goes wrong.
  returned: always
  type: str
  sample: null

cluster_ext_id:
  description: The external ID of the cluster.
  returned: always
  type: str
  sample: "913fa076-d385-4dd8-b549-0e628e645569"
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_snmp_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_config  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    api_instance = get_snmp_api_instance(module)
    resp = get_snmp_config(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
