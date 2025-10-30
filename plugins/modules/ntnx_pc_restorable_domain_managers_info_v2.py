#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type
DOCUMENTATION = r"""
module: ntnx_pc_restorable_domain_managers_info_v2
short_description: Fetch restorable domain managers info
version_added: 2.1.0
description:
    - Fetch list of multiple restorable domain managers for a given restore source.
    - Please provide Prism Element IP address here in C(nutanix_host)
    - Lists all the domain managers backed up at the object store/cluster.
options:
    restore_source_ext_id:
        description:
            - External ID of the restore source.
        required: true
        type: str
    nutanix_host:
        description:
            - The Nutanix Prism Element IP address.
        required: true
        type: str
    nutanix_username:
        description:
            - The username to authenticate with the Nutanix Prism Element.
        required: true
        type: str
    nutanix_password:
        description:
            - The password to authenticate with the Nutanix Prism Element.
        required: true
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Get all restorable domain managers for a given restore source
  nutanix.ncp.ntnx_pc_restorable_domain_managers_info_v2:
    nutanix_host: <pe_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    restore_source_ext_id: "d4e44c2b-944c-48b0-8de1-b0adae3d54c6"
  register: result
"""

RETURN = r"""
response:
    description: List of restorable domain managers for a given restore source.
    type: list
    returned: always
    sample:
        [
            {
                "config": {
                    "bootstrap_config": null,
                    "build_info": null,
                    "credentials": null,
                    "name": "PC_10.44.76.25",
                    "resource_config": null,
                    "should_enable_lockdown_mode": null,
                    "size": null
                },
                "ext_id": "cfddac63-ffdb-4d9c-9a8c-54abf89ce234",
                "hosting_cluster_ext_id": null,
                "is_registered_with_hosting_cluster": null,
                "links": null,
                "network": {
                    "external_address": {
                        "ipv4": {
                            "prefix_length": null,
                            "value": "10.0.0.1"
                        },
                        "ipv6": null
                    },
                    "external_networks": null,
                    "fqdn": null,
                    "internal_networks": null,
                    "name_servers": null,
                    "ntp_servers": null
                },
                "node_ext_ids": null,
                "should_enable_high_availability": null,
                "tenant_id": null
            }
        ]

total_available_results:
    description: Total number of restorable domain managers available.
    returned: always
    type: int
    sample: 1

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str
    sample: false

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false

"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.prism.pc_api_client import (  # noqa: E402
    get_domain_manager_backup_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(restore_source_ext_id=dict(type="str", required=True))
    return module_args


def get_restorable_domain_managers(module, domain_manager_backups_api, result):
    restore_source_ext_id = module.params.get("restore_source_ext_id")
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating restorable domain managers info Spec", **result
        )
    try:
        resp = domain_manager_backups_api.list_restorable_domain_managers(
            restoreSourceExtId=restore_source_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching restorable domain managers info",
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
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    domain_manager_backups_api = get_domain_manager_backup_api_instance(module)
    get_restorable_domain_managers(module, domain_manager_backups_api, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
