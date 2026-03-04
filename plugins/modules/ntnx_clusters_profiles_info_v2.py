#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_profiles_info_v2
short_description: Retrieve information about Nutanix cluster profiles from PC
version_added: 2.4.0
description:
    - This module retrieves information about Nutanix cluster profiles from PC.
    - Fetch particular cluster profile info using external ID
    - Fetch multiple cluster profiles info with/without using filters, limit, etc.
    - This module uses PC v4 APIs based SDKs
options:
  ext_id:
    description:
      - The external ID of the cluster profile.
      - If not provided, multiple cluster profiles info will be fetched.
    type: str
    required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger
      - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: fetch cluster profile info using external ID
  nutanix.ncp.ntnx_clusters_profiles_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
  register: result

- name: fetch all cluster profiles info
  nutanix.ncp.ntnx_clusters_profiles_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: fetch all clusters info with filter
  nutanix.ncp.ntnx_clusters_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    filter: "name eq 'cluster_profile_1'"
  register: result

- name: Fetch all cluster profiles info with limit
  nutanix.ncp.ntnx_clusters_profiles_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    limit: 1
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching cluster profile info.
        - Returns specific cluster profile info if ext_id is provided
        - Returns list of multiple cluster profiles info if ext_id is not provided
    type: dict
    returned: always
    sample:
        {
            "allowed_overrides": [
                "NTP_SERVER_CONFIG"
            ],
            "cluster_count": 0,
            "clusters": null,
            "create_time": "2025-11-05T13:21:04.998917+00:00",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "description": "Cluster profile description 2",
            "drifted_cluster_count": 0,
            "ext_id": "e5a0f246-0880-44f2-7b51-0aad170ac45e",
            "last_update_time": "2025-11-05T13:21:04.998917+00:00",
            "last_updated_by": "00000000-0000-0000-0000-000000000000",
            "links": null,
            "name": "cluster_profile_1_2",
            "name_server_ip_list": [
                {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "240.29.254.180"
                    },
                    "ipv6": null
                }
            ],
            "nfs_subnet_whitelist": [
                "10.110.106.45/255.255.255.255"
            ],
            "ntp_server_ip_list": [
                {
                    "fqdn": null,
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "240.29.254.180"
                    },
                    "ipv6": null
                }
            ],
            "pulse_status": {
                "is_enabled": false,
                "pii_scrubbing_level": "DEFAULT"
            },
            "rsyslog_server_list": [
                {
                    "ext_id": null,
                    "ip_address": {
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "240.29.254.180"
                        },
                        "ipv6": null
                    },
                    "links": null,
                    "modules": [
                        {
                            "log_severity_level": "EMERGENCY",
                            "name": "CASSANDRA",
                            "should_log_monitor_files": true
                        },
                        {
                            "log_severity_level": "ERROR",
                            "name": "CURATOR",
                            "should_log_monitor_files": false
                        }
                    ],
                    "network_protocol": "UDP",
                    "port": 29,
                    "server_name": "testServer1",
                    "tenant_id": null
                }
            ],
            "smtp_server": {
                "email_address": "email@example.com",
                "server": {
                    "ip_address": {
                        "fqdn": null,
                        "ipv4": {
                            "prefix_length": 32,
                            "value": "240.29.254.180"
                        },
                        "ipv6": null
                    },
                    "password": null,
                    "port": 465,
                    "username": "smtp-user"
                },
                "type": "SSL"
            },
            "snmp_config": {
                "ext_id": null,
                "is_enabled": false,
                "links": null,
                "tenant_id": null,
                "transports": [
                    {
                        "port": 21,
                        "protocol": "UDP"
                    }
                ],
                "traps": [
                    {
                        "address": {
                            "ipv4": {
                                "prefix_length": 32,
                                "value": "240.29.254.180"
                            },
                            "ipv6": null
                        },
                        "community_string": "snmp-server community public RO 192.168.1.0 255.255.255.0",
                        "engine_id": "0x1234567890abcdef12",
                        "ext_id": null,
                        "links": null,
                        "port": 59,
                        "protocol": "UDP",
                        "reciever_name": "trap-receiver",
                        "should_inform": false,
                        "tenant_id": null,
                        "username": "trapuser",
                        "version": "V2"
                    }
                ],
                "users": [
                    {
                        "auth_key": null,
                        "auth_type": "MD5",
                        "ext_id": null,
                        "links": null,
                        "priv_key": null,
                        "priv_type": "DES",
                        "tenant_id": null,
                        "username": "snmpuser1"
                    }
                ]
            },
            "tenant_id": null
        }
changed:
    description:
        - Indicates if any changes were made during the operation.
    type: bool
    returned: always
    sample: true
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching cluster profiles info"
ext_id:
    description:
        - The external ID of the cluster profile if given in input.
    type: str
    returned: always
    sample: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
total_available_results:
    description:
        - The total number of available cluster profiles in PC.
    type: int
    returned: when all cluster profiles are fetched
    sample: 100
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_cluster_profiles_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_cluster_profile  # noqa: E402
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


def get_cluster_profile_by_ext_id(module, cluster_profiles, result):
    ext_id = module.params.get("ext_id")
    resp = get_cluster_profile(module, cluster_profiles, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_cluster_profiles(module, cluster_profiles, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(module.params)
    if err:
        module.fail_json(
            "Failed creating query parameters for fetching cluster profiles info"
        )
    resp = None
    try:
        resp = cluster_profiles.list_cluster_profiles(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching cluster profiles info",
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata").get("total_available_results")
    result["total_available_results"] = total_available_results
    resp = resp.get("data")

    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        support_proxy=True,
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=False,
        mutually_exclusive=[("ext_id", "filter")],
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    cluster_profiles = get_cluster_profiles_api_instance(module)
    if module.params.get("ext_id"):
        get_cluster_profile_by_ext_id(module, cluster_profiles, result)
    else:
        get_cluster_profiles(module, cluster_profiles, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
