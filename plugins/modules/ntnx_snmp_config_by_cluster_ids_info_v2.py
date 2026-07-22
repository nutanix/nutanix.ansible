#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_snmp_config_by_cluster_ids_info_v2
short_description: Fetch SNMP configuration of a Nutanix cluster in Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about SnmpConfigByClusterId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of a specific SNMP user or SNMP trap on the cluster
    (choose using C(resource_type)).
  - If C(ext_id) is not provided, fetch the full SNMP configuration of the cluster
    (status, users, transports, traps).
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get SNMP configuration / SNMP user / SNMP trap) -
      Required Roles: Cluster Admin, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose SNMP configuration is fetched.
    type: str
    required: true
  resource_type:
    description:
      - Selects which SNMP resource to fetch when C(ext_id) is provided.
      - C(user) fetches an SNMP user by ID.
      - C(trap) fetches an SNMP trap by ID.
      - C(config) fetches the complete SNMP configuration (default when no C(ext_id)).
    type: str
    required: false
    choices:
      - config
      - user
      - trap
    default: config
  ext_id:
    description:
      - The external ID (UUID) of the SNMP user or SNMP trap to fetch.
      - When provided, C(resource_type) must be C(user) or C(trap).
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Fetch complete SNMP configuration of a cluster
  nutanix.ncp.ntnx_snmp_config_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: Fetch a specific SNMP user by ext_id
  nutanix.ncp.ntnx_snmp_config_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: user
    ext_id: "aaaaaaaa-1111-2222-3333-444444444444"
  register: result
  ignore_errors: true

- name: Fetch a specific SNMP trap by ext_id
  nutanix.ncp.ntnx_snmp_config_by_cluster_ids_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    resource_type: trap
    ext_id: "bbbbbbbb-1111-2222-3333-444444444444"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC SnmpConfigByClusterId info v4 API.
    - It can be a single SnmpUser or SnmpTrap if C(ext_id) is provided.
    - Full SnmpConfig for the cluster (containing status, users, transports, traps)
      if C(ext_id) is not provided.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "00061de6-4a87-6b06-185b-ac1f6b6f97e2",
      "is_enabled": true,
      "links": null,
      "tenant_id": null,
      "traps": [],
      "transports": [
          {
              "port": 161,
              "protocol": "UDP"
          }
      ],
      "users": []
    }

cluster_ext_id:
  description:
    - The external ID of the cluster whose SNMP configuration was fetched.
  returned: always
  type: str
  sample: "0006361b-6855-3644-7458-2268f8ffb2bd"

ext_id:
  description:
    - External ID of the fetched SNMP user or SNMP trap.
  type: str
  returned: when C(ext_id) is provided
  sample: "aaaaaaaa-1111-2222-3333-444444444444"

changed:
  description: Whether the module made any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching SNMP config using cluster ext_id"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: When an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_snmp_config,
    get_snmp_trap,
    get_snmp_user,
)
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

# Silence the unused-import warning while keeping the SDK reference available
# for the ``sdk_mock`` fallback semantics matching sibling modules.
_ = cluster_management_sdk


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        resource_type=dict(
            type="str",
            required=False,
            choices=["config", "user", "trap"],
            default="config",
        ),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_snmp_user_by_ext_id(module, clusters, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_snmp_user(module, clusters, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_snmp_trap_by_ext_id(module, clusters, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_snmp_trap(module, clusters, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_snmp_config_by_cluster_ext_id(module, clusters, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = get_snmp_config(module, clusters, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_if=[
            ("resource_type", "user", ("ext_id",)),
            ("resource_type", "trap", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "cluster_ext_id": module.params.get("cluster_ext_id"),
    }
    clusters = get_clusters_api_instance(module)
    resource_type = module.params.get("resource_type") or "config"
    ext_id = module.params.get("ext_id")
    if ext_id and resource_type == "user":
        get_snmp_user_by_ext_id(module, clusters, result)
    elif ext_id and resource_type == "trap":
        get_snmp_trap_by_ext_id(module, clusters, result)
    else:
        get_snmp_config_by_cluster_ext_id(module, clusters, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
