#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_config_info_v2
short_description: Get PC Configuration info
version_added: 2.1.0
description:
    - Fetch specific PC Configuration info using external ID
    - Fetch list of PC Configuration info if external ID is not provided with optional filters. Length of list is 1.
options:
    ext_id:
        description:
            - External ID of PC which is not the external ID of PCVM.
            - To fetch specific PC Configuration info.
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get PC config without external ID
  nutanix.ncp.ntnx_pc_config_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
  register: result

- name: Fetch PC details using external ID
  nutanix.ncp.ntnx_pc_config_info_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for fetching PC Configuration info
        - PC Configuration info if external ID is provided
        - One PC Configuration info if external ID is not provided as length of array is 1
    type: dict
    returned: always
    sample:
        {
            "config": {
                "bootstrap_config": {
                    "cloud_init_config": null,
                    "environment_info": {
                        "provider_type": "NTNX",
                        "provisioning_type": "NTNX",
                        "type": "ONPREM"
                    }
                },
                "build_info": {
                    "version": "pc.2024.3"
                },
                "credentials": null,
                "name": "PC_10.44.76.25",
                "resource_config": {
                    "container_ext_ids": [
                        "6171a26e-7d08-4f10-b6fa-9304b333f6b6"
                    ],
                    "data_disk_size_bytes": 536870912000,
                    "memory_size_bytes": 37580963840,
                    "num_vcpus": 10
                },
                "should_enable_lockdown_mode": null,
                "size": "SMALL"
            },
            "ext_id": "cfddac63-ffdb-4d9c-9a8c-54abf89ce234",
            "hosting_cluster_ext_id": "00062cd6-e034-fd28-185b-ac1f6b6f97e2",
            "is_registered_with_hosting_cluster": true,
            "links": null,
            "network": {
                "external_address": {
                    "ipv4": {
                        "prefix_length": null,
                        "value": "10.44.76.25"
                    },
                    "ipv6": null
                },
                "external_networks": [
                    {
                        "default_gateway": {
                            "fqdn": null,
                            "ipv4": {
                                "prefix_length": null,
                                "value": "10.44.76.1"
                            },
                            "ipv6": null
                        },
                        "ip_ranges": [
                            {
                                "begin": {
                                    "ipv4": {
                                        "prefix_length": null,
                                        "value": "10.44.76.24"
                                    },
                                    "ipv6": null
                                },
                                "end": {
                                    "ipv4": {
                                        "prefix_length": null,
                                        "value": "10.44.76.24"
                                    },
                                    "ipv6": null
                                }
                            }
                        ],
                        "network_ext_id": "afc34756-bb5e-4df9-a2ec-c82ad628c4ae",
                        "subnet_mask": {
                            "fqdn": null,
                            "ipv4": {
                                "prefix_length": null,
                                "value": "255.255.252.0"
                            },
                            "ipv6": null
                        }
                    }
                ],
                "fqdn": null,
                "internal_networks": null,
                "name_servers": [
                    {
                        "fqdn": null,
                        "ipv4": {
                            "prefix_length": null,
                            "value": "10.40.64.15"
                        },
                        "ipv6": null
                    },
                    {
                        "fqdn": null,
                        "ipv4": {
                            "prefix_length": null,
                            "value": "10.40.64.16"
                        },
                        "ipv6": null
                    }
                ],
                "ntp_servers": [
                    {
                        "fqdn": {
                            "value": "0.example.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    },
                    {
                        "fqdn": {
                            "value": "3.example.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    },
                    {
                        "fqdn": {
                            "value": "2.example.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    },
                    {
                        "fqdn": {
                            "value": "1.example.org"
                        },
                        "ipv4": null,
                        "ipv6": null
                    }
                ]
            },
            "node_ext_ids": [
                "e5cc110f-3a4a-4a88-8c89-71aa101adb03"
            ],
            "should_enable_high_availability": false,
            "tenant_id": null
        }

ext_id:
    description: External ID of the PC
    type: str
    returned: always
    sample: "cda893b8-2aee-34bf-817d-d2ee6026790b"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching PC Configuration info"

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
total_available_results:
    description:
        - The total number of available PCs
        - This will always be 1.
    type: int
    returned: when all pc configurations are fetched
    sample: 1
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.helpers import get_pc_config  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_api_instance,
)
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


def get_pc_config_with_ext_id(module, domain_manager_api, result):
    ext_id = module.params.get("ext_id")
    resp = get_pc_config(module, domain_manager_api, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_pc_configs(module, domain_manager_api, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating PC Configuration info Spec", **result)
    try:
        resp = domain_manager_api.list_domain_managers(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching PC Configuration info",
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
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    domain_manager_api = get_domain_manager_api_instance(module)
    if module.params.get("ext_id"):
        get_pc_config_with_ext_id(module, domain_manager_api, result)
    else:
        get_pc_configs(module, domain_manager_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
