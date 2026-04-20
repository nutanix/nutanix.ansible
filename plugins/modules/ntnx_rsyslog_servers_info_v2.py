#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_rsyslog_servers_info_v2
short_description: Fetch RSYSLOG server configuration info from a Nutanix cluster
version_added: 2.6.0
description:
  - This module allows you to fetch RSYSLOG server configurations from a Nutanix cluster.
  - If C(ext_id) is provided, fetches a particular RSYSLOG server using its external ID.
  - If C(ext_id) is not provided, fetches all RSYSLOG servers for the given cluster.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Get RSYSLOG server by ext_id) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager,
      Security Dashboard Admin, Security Dashboard Viewer, Super Admin, Self-Service Admin (deprecated),
    - >-
      B(List RSYSLOG servers) -
      Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Project Manager,
      Security Dashboard Admin, Security Dashboard Viewer, Super Admin, Self-Service Admin (deprecated),
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster from which to fetch RSYSLOG server configurations.
      - Required for all operations.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the RSYSLOG server.
      - If provided, fetches a specific RSYSLOG server by its external ID.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get RSYSLOG server using ext_id
  nutanix.ncp.ntnx_rsyslog_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: List all RSYSLOG servers for a cluster
  nutanix.ncp.ntnx_rsyslog_servers_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for fetching RSYSLOG server info.
    - Specific RSYSLOG server info if External ID is provided.
    - List of RSYSLOG servers if External ID is not provided.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0",
      "server_name": "rsyslog_server_1",
      "ip_address": {
          "ipv4": {
              "value": "192.168.1.100",
              "prefix_length": 32
          },
          "ipv6": null
      },
      "port": 514,
      "network_protocol": "UDP",
      "modules": [
          {
              "name": "PRISM",
              "log_severity_level": "INFO",
              "should_log_monitor_files": false
          }
      ],
      "links": null,
      "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: when there is an error
  type: str
  sample: "Api Exception raised while fetching RSYSLOG servers info"

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the RSYSLOG server.
  type: str
  returned: when external ID is provided
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

total_available_results:
  description: The total number of available RSYSLOG servers for the cluster.
  type: int
  returned: when all RSYSLOG servers are fetched
  sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_rsyslog_server  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_rsyslog_server_using_ext_id(module, api_instance, cluster_ext_id, result):
    ext_id = module.params.get("ext_id")
    resp = get_rsyslog_server(module, api_instance, cluster_ext_id, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_rsyslog_servers(module, api_instance, cluster_ext_id, result):
    try:
        resp = api_instance.list_rsyslog_servers_by_cluster_id(
            clusterExtId=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching RSYSLOG servers info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "error": None}
    api_instance = get_clusters_api_instance(module)
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    if module.params.get("ext_id"):
        get_rsyslog_server_using_ext_id(module, api_instance, cluster_ext_id, result)
    else:
        get_rsyslog_servers(module, api_instance, cluster_ext_id, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
