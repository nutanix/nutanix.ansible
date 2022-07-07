#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_clusters_info
short_description: cluster info module
version_added: 1.3.0
description: 'Get cluster info'
options:
      kind:
        description:
          - The kind name
        type: str
        default: cluster
      cluster_uuid:
        description:
            - cluster UUID
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
  - name: List clusters using priority filter criteria
    ntnx_clusters_info:
      nutanix_host: "{{ ip }}"
      nutanix_username: "{{ username }}"
      nutanix_password: "{{ password }}"
      validate_certs: False
      filter: TODO
      kind: cluster
    register: result

  - name: List clusters using length, offset, sort order and priority sort attribute
    ntnx_clusters_info:
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
  description: Metadata for clusters list output
  returned: always
  type: dict
  sample: {
    "metadata": {
            "kind": "cluster",
            "length": 6,
            "offset": 0,
            "sort_attribute": "priority",
            "sort_order": "ASCENDING",
            "total_matches": 6
        }
        }
entities:
  description: cluster intent response
  returned: always
  type: list
  sample: {
    "entities": [ {
            "metadata": {
                "categories": {},
                "categories_mapping": {},
                "creation_time": "",
                "kind": "cluster",
                "last_update_time": "",
                "spec_hash": "",
                "spec_version": "",
                "uuid": ""
            },
            "spec": {
                "name": "Unnamed",
                "resources": {
                    "config": {
                        "domain_awareness_level": "",
                        "enabled_feature_list": [
                            "PASSWORD_REMOTE_LOGIN_ENABLED",
                            "SHADOW_CLONES_ENABLED"
                        ],
                        "encryption_status": "NOT_SUPPORTED",
                        "operation_mode": "NORMAL",
                        "redundancy_factor": 2,
                        "software_map": {
                            "NCC": {
                                "software_type": "NCC",
                                "status": "INSTALLED",
                                "version": ""
                            },
                            "NOS": {
                                "software_type": "NOS",
                                "status": "INSTALLED",
                                "version": ""
                            }
                        },
                        "supported_information_verbosity": "BASIC_PLUS_CORE_DUMP",
                        "timezone": "Atlantic/Reykjavik"
                    },
                    "network": {
                        "external_ip": "",
                        "external_subnet": "",
                        "internal_subnet": "",
                        "name_server_ip_list": [
                            "",
                        ],
                        "ntp_server_ip_list": [
                            "",
                        ]
                    }
                }
            },
            "status": {
                "name": "Unnamed",
                "resources": {
                    "config": {
                        "build": {
                            "build_type": "release",
                            "commit_date": "",
                            "commit_id": "",
                            "full_version": "",
                            "short_commit_id": "",
                            "version": ""
                        },
                        "cluster_arch": "",
                        "domain_awareness_level": "NODE",
                        "enabled_feature_list": [
                            "PASSWORD_REMOTE_LOGIN_ENABLED",
                            "SHADOW_CLONES_ENABLED"
                        ],
                        "encryption_status": "NOT_SUPPORTED",
                        "is_available": true,
                        "operation_mode": "NORMAL",
                        "redundancy_factor": 2,
                        "service_list": [
                            "PRISM_CENTRAL"
                        ],
                        "software_map": {
                            "NCC": {
                                "software_type": "NCC",
                                "status": "INSTALLED",
                                "version": ""
                            },
                            "NOS": {
                                "software_type": "NOS",
                                "status": "INSTALLED",
                                "version": ""
                            }
                        },
                        "supported_information_verbosity": "BASIC_PLUS_CORE_DUMP",
                        "timezone": "Atlantic/Reykjavik"
                    },
                    "network": {
                        "external_ip": "",
                        "external_subnet": "",
                        "internal_subnet": "",
                        "name_server_ip_list": [
                            ""
                        ],
                        "ntp_server_ip_list": [
                            "",
                        ]
                    },
                    "runtime_status_list": [
                        "SSP_CONFIG_OWNER"
                    ]
                },
                "state": "COMPLETE"
            }
        }
        ],
        }
"""

from ..module_utils.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.prism.clusters import Cluster  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402


def get_module_spec():

    module_args = dict(
        cluster_uuid=dict(type="str"),
        kind=dict(type="str", default="cluster"),
        sort_order=dict(type="str"),
        sort_attribute=dict(type="str"),
    )

    return module_args


def get_cluster(module, result):
    cluster = Cluster(module)
    cluster_uuid = module.params.get("cluster_uuid")
    resp = cluster.read(cluster_uuid)

    result["response"] = resp


def get_clusters(module, result):
    cluster = Cluster(module)
    spec, error = cluster.get_info_spec()

    resp = cluster.list(spec)

    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        required_together=[("sort_order", "sort_attribute")],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("cluster_uuid"):
        get_cluster(module, result)
    else:
        get_clusters(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
