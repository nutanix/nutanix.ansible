#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_config_v2
short_description: Update LCM Configuration
description:
    - This module updates LCM configurations.
version_added: 2.1.0
author:
    - Abhinav Bansal (@abhinavbansal29)
options:
    state:
        description:
            - State of the module.
            - If state is present, the module will update the LCM configuration.
            - If state is not present, the module will fail.
        type: str
        choices:
            - present
        default: present
    cluster_ext_id:
        description:
            - The external ID of the cluster.
            - It is used to update the LCM configuration on a particular cluster, it updates Prism Central's LCM configuration if nothing passed.
            - If we give PE cluster's external ID, it will update PE cluster's LCM configuration.
            - We can get the external ID of the cluster using ntnx_clusters_info_v2 module.
        type: str
        required: false
    url:
        description:
            - URL of the LCM repository.
        type: str
        required: false
    is_auto_inventory_enabled:
        description:
            - Whether auto inventory is enabled.
        type: bool
        required: false
    auto_inventory_schedule:
        description:
            - The scheduled time in "%H:%M" 24-hour format of the next inventory execution.
            - Used when auto_inventory_enabled is set to True.
            - The default schedule time is 03:00(AM).
        type: str
        required: false
    connectivity_type:
        description:
            - This field indicates whether LCM framework on the cluster is running in connected-site mode or darksite mode.
        type: str
        choices: ["CONNECTED_SITE", "DARKSITE_DIRECT_UPLOAD", "DARKSITE_WEB_SERVER"]
        required: false
    is_https_enabled:
        description:
            - Indicates if the LCM URL has HTTPS enabled.
        type: bool
        required: false
        default: false
    has_module_auto_upgrade_enabled:
        description:
            - Indicates if LCM is enabled to auto-upgrade products.
        type: bool
        required: false
        default: false
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
"""

EXAMPLES = r"""
- name: Update config of LCM
  nutanix.ncp.ntnx_lcm_config_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    is_auto_inventory_enabled: true
    is_https_enabled: true
    has_module_auto_upgrade_enabled: false
    url: "http://example.com"
  register: lcm_config_update
"""

RETURN = r"""
response:
    description: The response from the LCM config API
    type: dict
    returned: always
    sample:
        {
            "auto_inventory_schedule": "03:00",
            "connectivity_type": "CONNECTED_SITE",
            "deprecated_software_entities": [
                "Firmware",
                "Foundation",
                "NCC"
            ],
            "display_version": "3.1.0.4301",
            "ext_id": null,
            "has_module_auto_upgrade_enabled": true,
            "is_auto_inventory_enabled": true,
            "is_framework_bundle_uploaded": false,
            "is_https_enabled": false,
            "links": null,
            "supported_software_entities": [
                "AOS base software",
                "Prism Central"
            ],
            "tenant_id": null,
            "url": "http://example.com",
            "version": "3.1.56788"
        }
changed:
    description: Whether the module made any changes
    type: bool
    returned: always
    sample: false
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    type: str
    returned: When an error occurs
    sample: "Failed creating query parameters for updating lcm config"
skipped:
    description: Indicates if the operation was skipped.
    type: bool
    returned: When the operation was skipped
    sample: false
"""


import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_config_api_instance,
    get_etag,
)
from ..module_utils.v4.lcm.helpers import get_lcm_config  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_users_empty_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str"),
        url=dict(type="str"),
        is_auto_inventory_enabled=dict(type="bool"),
        auto_inventory_schedule=dict(type="str"),
        connectivity_type=dict(
            type="str",
            choices=["CONNECTED_SITE", "DARKSITE_DIRECT_UPLOAD", "DARKSITE_WEB_SERVER"],
        ),
        is_https_enabled=dict(type="bool", default=False),
        has_module_auto_upgrade_enabled=dict(type="bool", default=False),
    )
    return module_args


def check_lcm_config_idempotency(old_spec, update_spec):
    return old_spec == update_spec


def update_lcm_config(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    current_spec = get_lcm_config(module, api_instance, cluster_ext_id)
    etag_value = get_etag(current_spec)
    if not etag_value:
        module.fail_json(msg="Failed to get etag value from the current lcm config")

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed creating query parameters for updating lcm config", **result
        )
    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_lcm_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    try:
        resp = api_instance.update_config(
            X_Cluster_Id=cluster_ext_id, body=update_spec, if_match=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating lcm config",
        )
    resp = get_lcm_config(module, api_instance, cluster_ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
    }
    api_instance = get_config_api_instance(module)
    update_lcm_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
