#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_templates_info_v2
short_description: template info module
version_added: 2.0.0
description:
    - Get templates info
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - template UUID
        type: str
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_info_v2
author:
 - Gevorg Khachatryan (@Gevorg-Khachatryan-97)
 - Alaa Bishtawi (@alaa-bish)
"""
EXAMPLES = r"""
- name: Fetch template info using ext id
  nutanix.ncp.ntnx_templates_info_v2:
    ext_id: "{{ template1_ext_id }}"
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: List all templates
  nutanix.ncp.ntnx_templates_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
"""
RETURN = r"""
response:
  description:
    - it contains template information
    - Type can be list or dict; a response could be a list of templates or a template itself.
      By default, the response will be a list. and dict if the ext_id is supplied in order to retrieve the template specifically
  type: dict
  returned: always
  sample:
    {
                "create_time": "2024-05-16T04:41:12.501912+00:00",
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
                "ext_id": "a13033a1-dbca-4712-aa33-54ab0ee86a94",
                "guest_update_status": null,
                "links": null,
                "template_description": "ansible test",
                "template_name": "SNfCOFKPcllbansible-agtemplate",
                "template_version_spec": {
                    "create_time": "2024-05-16T04:41:12.458682+00:00",
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
                    "ext_id": "8cbc63a1-1219-4e75-b728-9086d3f7d13e",
                    "is_active_version": true,
                    "is_gc_override_enabled": true,
                    "links": null,
                    "tenant_id": null,
                    "version_description": "Created from VM: MinReqVMalaa2",
                    "version_name": "Initial Version",
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
                        "name": "MinReqVMalaa2",
                        "nics": null,
                        "num_cores_per_socket": 1,
                        "num_numa_nodes": 0,
                        "num_sockets": 1,
                        "num_threads_per_core": 1,
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
                },
                "tenant_id": null,
                "update_time": "2024-05-16T04:41:12.501912+00:00",
                "updated_by": {
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
        ext_id=dict(type="str"),
    )

    return module_args


def get_template(module, result):
    templates = get_templates_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = templates.get_template_by_id(ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching template info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_templates(module, result):
    templates = get_templates_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating templates info Spec", **result)

    try:
        resp = templates.list_templates(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching templates info",
        )
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
    result = {"changed": False, "response": None}
    if module.params.get("ext_id"):
        get_template(module, result)
    else:
        get_templates(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
