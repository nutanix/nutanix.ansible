#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Pradeepsingh Bhati
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: ntnx_volume_groups_categories_info_v2
short_description: Fetch list of attached categories to VG
description:
    - Fetch list of attached categories to VG
version_added: "2.0.0"
author:
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
- name: Fetch info of all categories attached to VG
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
        - list of categories attached to VG
    type: list
    returned: always
    sample:    [
            {
                "entity_type": "CATEGORY",
                "ext_id": "e4bda88f-e5da-5eb1-a031-2c0bb00d923d",
                "name": null,
                "uris": null
            },
            {
                "entity_type": "CATEGORY",
                "ext_id": "711936c6-7a6b-4b01-ab52-dc19b2e368db",
                "name": null,
                "uris": null
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
    sample: "Failed generating volume group associated categories info Spec"
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


def get_associated_categories(module, result):
    vgs = get_vg_api_instance(module)
    ext_id = module.params.get("ext_id")

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating volume group associated categories info Spec",
            **result,
        )

    try:
        resp = vgs.list_category_associations_by_volume_group_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching categories associated with volume group info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")
    if not result["response"]:
        result["response"] = []


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
    get_associated_categories(module, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
