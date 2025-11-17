#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_templates_versions_info_v2
short_description: Fetches information about Nutanix template versions.
version_added: 2.0.0
description:
    - This module fetches information about Nutanix template versions.
    - It can retrieve information about a specific template version or all template versions.
    - This module uses PC v4 APIs based SDKs
options:
    template_ext_id:
        description:
            - The external ID of the template.
        type: str
        required: true
    ext_id:
        description:
            - The external ID of the template version.
        type: str
        required: false
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
      - nutanix.ncp.ntnx_logger_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""

EXAMPLES = r"""
- name: Retrieve the Template Version details for the given Template Version identifier.
  nutanix.ncp.ntnx_templates_versions_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ version_ext_id }}"
    template_ext_id: "{{ template_ext_id }}"
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC template version v4 API.
    - Type can be list or dict; a response could be a list of templates version or a template version.
      By default, the response will be a list. and dict if the ext_id is supplied in order to retrieve the template version specifically
  type: dict
  returned: always
  sample:
        {
                    "create_time": "2024-05-16T04:41:24.102680+00:00",
                    "created_by": {
                        "additional_attributes": null,
                        "buckets_access_keys": null,
                        "created_by": null,
                        "created_time": null,
                        "display_name": null,
                        "email_id": null,
                        "ext_id": "00000000-0000-0000-0000-000000000000",
                        "first_name": null,
                        "idp_id": null,
                        "is_force_reset_password_enabled": null,
                        "last_login_time": null,
                        "last_name": null,
                        "last_updated_time": null,
                        "links": null,
                        "locale": null,
                        "middle_initial": null,
                        "password": null,
                        "region": null,
                        "status": null,
                        "tenant_id": null,
                        "user_type": null,
                        "username": "admin"
                    },
                    "ext_id": "3a6a4105-0e90-4114-a9b6-53bb7203c357",
                    "is_active_version": true,
                    "is_gc_override_enabled": true,
                    "links": null,
                    "tenant_id": null,
                    "version_description": "ansible_template_version_description New",
                    "version_name": "SNfCOFKPcllbansible-agversion2",
                    "version_source": null,
                    "version_source_discriminator": null,
                    "vm_spec": {
                        "apc_config": null,
                        "availability_zone": null,
                        "bios_uuid": null,
                        "boot_config": {
                            "boot_device": null,
                            "boot_order": [
                                "CDROM",
                                "DISK",
                                "NETWORK"
                            ]
                        },
                        "categories": [
                            {
                                "ext_id": "eb8b4155-b3d1-5772-8d2f-d566d43d8e46"
                            }
                        ],
                        "cd_roms": null,
                        "cluster": {
                            "ext_id": "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
                        },
                        "create_time": null,
                        "description": null,
                        "disks": null,
                        "enabled_cpu_features": null,
                        "ext_id": null,
                        "generation_uuid": null,
                        "gpus": null,
                        "guest_customization": null,
                        "guest_tools": null,
                        "hardware_clock_timezone": "UTC",
                        "host": null,
                        "is_agent_vm": false,
                        "is_branding_enabled": true,
                        "is_cpu_passthrough_enabled": false,
                        "is_cross_cluster_migration_in_progress": null,
                        "is_gpu_console_enabled": false,
                        "is_live_migrate_capable": null,
                        "is_memory_overcommit_enabled": false,
                        "is_vcpu_hard_pinning_enabled": false,
                        "is_vga_console_enabled": true,
                        "links": null,
                        "machine_type": "PC",
                        "memory_size_bytes": 4294967296,
                        "name": "new_vm_name",
                        "nics": null,
                        "num_cores_per_socket": 4,
                        "num_numa_nodes": 0,
                        "num_sockets": 4,
                        "num_threads_per_core": 4,
                        "ownership_info": null,
                        "power_state": "ON",
                        "protection_policy_state": null,
                        "protection_type": null,
                        "serial_ports": null,
                        "source": null,
                        "storage_config": null,
                        "tenant_id": null,
                        "update_time": null,
                        "vtpm_config": {
                            "is_vtpm_enabled": false,
                            "version": null
                        }
                    }
                    }
error:
  description: The error message if an error occurs.
  type: str
  returned: when an error occurs
ext_id:
    description:
        - The external ID of the template version when is fetched.
    type: str
    returned: always
    sample: "00000-00000-000000-000000"
total_available_results:
    description:
        - The total number of available template versions in PC.
    type: int
    returned: when all template versions are fetched
    sample: 125
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_templates_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        template_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str"),
    )

    return module_args


def get_template_version(module, result):
    templates = get_templates_api_instance(module)
    template_ext_id = module.params.get("template_ext_id")
    ext_id = module.params.get("ext_id")

    try:
        resp = templates.get_template_version_by_id(template_ext_id, ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching template version info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_template_versions(module, result):
    templates = get_templates_api_instance(module)
    template_ext_id = module.params.get("template_ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating template versions info Spec", **result)

    try:
        resp = templates.list_template_versions(template_ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching template versions info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results

    if not getattr(resp, "data", None):
        result["response"] = []
        return
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    if module.params.get("ext_id"):
        get_template_version(module, result)
    else:
        get_template_versions(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
