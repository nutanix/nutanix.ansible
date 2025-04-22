#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Prem Karat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_vms_info_v2
short_description: Fetch VG attached VMs info
description:
    - Fetch all VMs info attached to VM
version_added: "2.0.0"
author:
 - Prem Karat (@premkarat)
 - Pradeepsingh Bhati (@bhati-pradeep)
options:
    ext_id:
        description:
            - The external ID of VG
        type: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
"""

EXAMPLES = r"""
- name: Fetch particular VM attached to VG using filters
  ntnx_volume_groups_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    filter: extId eq '{{ vm1_uuid }}'
    ext_id: "{{ vg1_uuid }}"
  register: result

- name: Fetch all VMs attached to VG
  ntnx_volume_groups_vms_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    state: "present"
    ext_id: 0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35
  register: result
"""

RETURN = r"""
response:
    description:
        - list of VMs attached to VG
    type: list
    returned: always
    sample:   [
            {
                "created_time": null,
                "ext_id": "7b959066-86f4-43e5-4c8b-d870876674da",
                "index": null,
                "links": null,
                "tenant_id": null
            }
        ]
ext_id:
    description: volume group external ID
    type: str
    returned: always
    sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
error:
    description: The error message if any.
    type: str
    returned: when error occurs
    sample: "Api Exception raised while fetching VMs attached to given Volume Group"
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
        ext_id=dict(type="str", required=True),
    )
    return module_args


def get_vg_vms(module, result):
    vgs = get_vg_api_instance(module)
    volume_group_ext_id = module.params.get("ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating info Spec", **result)

    try:
        resp = vgs.list_vm_attachments_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching VMs attached to given Volume Group",
        )

    result["ext_id"] = volume_group_ext_id
    vms = strip_internal_attributes(resp.to_dict()).get("data")
    if not vms:
        vms = []
    result["response"] = vms


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "error": None, "response": None}
    get_vg_vms(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
