#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_snmp_trap_info_v2
short_description: Fetch information about a specific SNMP trap
description:
  - This module fetches information about a Nutanix SNMP trap.
  - Fetch specific SNMP trap using external ID and cluster external ID.
  - This module uses PC v4 APIs based SDKs.
version_added: "2.6.0"
options:
  ext_id:
    description:
      - The external ID of the SNMP trap.
    type: str
    required: true
  cluster_ext_id:
    description:
      - The external ID of the parent cluster.
    type: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get details of a specific SNMP trap
  nutanix.ncp.ntnx_snmp_trap_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "{{ cluster_ext_id }}"
    ext_id: "a3265671-de53-41be-af9b-f06241b95356"
  register: result
"""

RETURN = r"""
response:
  description:
    - The response for fetching the SNMP trap.
  type: dict
  returned: always
  sample:
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
from ..module_utils.v4.clusters_mgmt.helpers import get_snmp_trap  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str", required=True),
    )
    return module_args


def get_snmp_trap_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id

    resp = get_snmp_trap(
        module=module,
        api_instance=api_instance,
        ext_id=ext_id,
        cluster_ext_id=cluster_ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_snmp_api_instance(module)
    get_snmp_trap_using_ext_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
