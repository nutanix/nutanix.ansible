#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: ntnx_volume_groups_info_v2
short_description: Fetch information about Nutanix PC Volume groups.
description:
  - This module fetches information about Nutanix PC Volume groups.
  - The module can fetch information about all Volume groups or a specific Volume group.
  - This module uses PC v4 APIs based SDKs
version_added: "2.0.0"
author:
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of the Volume Group.
        type: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch information about all VGs
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false

- name: Fetch information about a specific VG
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653

- name: Fetch information about a specific VG
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: 530567f3-abda-4913-b5d0-0ab6758ec1653
"""

RETURN = r"""
response:
    description:
        - Volume group details if C(ext_id) is provided.
        - List of Volume groups if C(ext_id) is not provided.
    type: dict
    returned: always
    sample: {
            "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
            "created_by": null,
            "created_time": null,
            "description": "Volume group 2",
            "enabled_authentications": null,
            "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
            "is_hidden": null,
            "iscsi_features": {
                "enabled_authentications": "CHAP",
                "iscsi_target_name": null,
                "target_secret": null
            },
            "iscsi_target_name": null,
            "iscsi_target_prefix": null,
            "links": null,
            "load_balance_vm_attachments": null,
            "name": "ansible-vgs-KjRMtTRxhrww2",
            "sharing_status": "SHARED",
            "should_load_balance_vm_attachments": true,
            "storage_features": {
                "flash_mode": {
                    "is_enabled": true
                }
            },
            "target_name": "vg1-792cd764-37b5-4da3-7ef1-ea3f618c1648",
            "target_prefix": null,
            "target_secret": null,
            "tenant_id": null,
        }
ext_id:
    description: Volume group external ID.
    type: str
    returned: When C(ext_id) is provided.
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Failed generating volume groups info Spec"
changed:
    description: Indicates whether the resource has changed.
    type: bool
    returned: always
    sample: true
"""

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_vg(module, result):
    vgs = get_vg_api_instance(module)
    ext_id = module.params.get("ext_id")

    try:
        resp = vgs.get_volume_group_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume group info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_vgs(module, result):
    vgs = get_vg_api_instance(module)

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating volume groups info Spec", **result)

    try:
        resp = vgs.list_volume_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching volume groups info",
        )

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
    if module.params.get("ext_id"):
        get_vg(module, result)
    else:
        get_vgs(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
