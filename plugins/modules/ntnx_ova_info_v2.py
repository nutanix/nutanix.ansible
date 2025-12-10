#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_ova_info_v2
short_description: Fetch information about ova(s)
description:
    - This module fetches information about Nutanix OVA(s)
    - Fetch specific OVA using external ID
    - Fetch list of multiple OVAs if external ID is not provided with optional filter
    - This module uses PC v4 APIs based SDKs
version_added: "2.3.0"
options:
    ext_id:
        description:
            - The external ID of the OVA.
        type: str
        required: false
author:
    - Abhinav Bansal (@abhinavbansal29)
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: List all Ovas
  nutanix.ncp.ntnx_ova_info_v2:
  register: result

- name: List Ovas with filter
  nutanix.ncp.ntnx_ova_info_v2:
    filter: "name eq 'test_ova'"
  register: result

- name: List Ovas with limit
  nutanix.ncp.ntnx_ova_info_v2:
    limit: 1
  register: result

- name: Get details of a specific Ova
  nutanix.ncp.ntnx_ova_info_v2:
    ext_id: "12345678-1234-1234-1234-123456789012"
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC OVA info v4 API.
        - It can be a single OVA if external ID is provided.
        - List of multiple OVAs if external ID is not provided.
    type: dict
    returned: always
    sample:
        [
            {
                "checksum": {
                    "hex_digest": "6c55d188e23983046a94f31f3d8b40d53d1db66f0d3676c77460e862dc577926"
                },
                "cluster_location_ext_ids": null,
                "create_time": "2025-07-21T05:53:39.814198+00:00",
                "created_by": {
                    "additional_attributes": null,
                    "buckets_access_keys": null,
                    "created_by": null,
                    "created_time": null,
                    "creation_type": null,
                    "description": null,
                    "display_name": null,
                    "email_id": null,
                    "ext_id": "30303030-3030-3030-2d30-3030302d3030",
                    "first_name": null,
                    "idp_id": null,
                    "is_force_reset_password_enabled": null,
                    "last_login_time": null,
                    "last_name": null,
                    "last_updated_by": null,
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
                "disk_format": "QCOW2",
                "ext_id": "ddab0ab3-daf1-4253-bb0e-0b51cec16205",
                "last_update_time": "2025-07-21T09:52:22.983006+00:00",
                "links": null,
                "name": "test_ova_123_update",
                "parent_vm": "test_ansi_ova_vm",
                "size_bytes": 10240,
                "source": null,
                "tenant_id": null,
                "vm_config": null
            }
        ]
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while fetching ovas info"
error:
    description: Error message if something goes wrong.
    type: str
    returned: always
ext_id:
    description: The external ID of the OVA that was fetched.
    type: str
    returned: when fetching a specific OVA
    sample: "12345678-1234-1234-1234-123456789012"
total_available_results:
    description: The total number of available OVAs in PC.
    type: int
    returned: when all OVAs are fetched
    sample: 125
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.vmm.api_client import get_ova_api_instance  # noqa: E402
from ..module_utils.v4.vmm.helpers import get_ova  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_ova_using_ext_id(module, ova, result):
    ext_id = module.params.get("ext_id")

    resp = get_ova(
        module=module,
        api_instance=ova,
        ext_id=ext_id,
    )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_ovas(module, ova, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating ovas info Spec", **result)

    try:
        resp = ova.list_ovas(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching ovas info",
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
    result = {"changed": False, "error": None, "response": None}
    ova = get_ova_api_instance(module)
    if module.params.get("ext_id"):
        get_ova_using_ext_id(module, ova, result)
    else:
        get_ovas(module, ova, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
