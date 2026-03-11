#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_resource_groups_info_v2
short_description: Fetch resource group information using Nutanix v4 APIs.
version_added: "2.1.0"
description:
    - Fetch information about resource groups from Nutanix Prism Central.
    - Retrieve a single resource group by external ID or list all resource groups with optional filters.
    - This module uses the v4 multidomain API.
options:
    ext_id:
        description:
            - The external ID (UUID) of the resource group to retrieve.
            - Mutually exclusive with C(filter).
        type: str
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_info_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Nutanix Ansible Team
"""

EXAMPLES = r"""
- name: Get all resource groups
  nutanix.ncp.ntnx_resource_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Get resource group by ext_id
  nutanix.ncp.ntnx_resource_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "{{ resource_group_ext_id }}"
  register: result

- name: List resource groups with filter
  nutanix.ncp.ntnx_resource_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    filter: "name eq 'my-resource-group'"
  register: result
"""

RETURN = r"""
response:
    description:
        - The resource group response.
        - For a single resource group, this contains the resource group details.
        - For a list, this contains a list of resource group objects.
    returned: always
    type: dict or list
    sample: {
        "name": "my-resource-group",
        "project_ext_id": "00000000-0000-0000-0000-000000000000",
        "ext_id": "00000000-0000-0000-0000-000000000001",
        "placement_targets": [
            {
                "cluster_ext_id": "00000000-0000-0000-0000-000000000002"
            }
        ]
    }
changed:
    description: Whether the state changed. Always false for info modules.
    returned: always
    type: bool
    sample: false
ext_id:
    description: The external ID of the fetched resource group.
    returned: when a single resource group is fetched
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
total_available_results:
    description: Total number of available results when listing resource groups.
    returned: when listing resource groups
    type: int
    sample: 5
"""

import traceback  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_resource_groups_api_instance,
)
from ..module_utils.v4.multidomain.helpers import (  # noqa: E402
    get_resource_group,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_multidomain_py_client  # noqa: E402, F401
except ImportError:
    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_resource_group_by_ext_id(module, result):
    ext_id = module.params.get("ext_id")
    api_instance = get_resource_groups_api_instance(module)
    resp = get_resource_group(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_resource_groups(module, result):
    api_instance = get_resource_groups_api_instance(module)
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating list resource groups spec", **result
        )

    try:
        resp = api_instance.list_resource_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing resource groups",
        )

    resp = resp.to_dict()
    if resp.get("metadata"):
        result["total_available_results"] = resp["metadata"].get(
            "total_available_results"
        )
    result["response"] = (
        strip_internal_attributes(resp.get("data"))
        if resp.get("data")
        else []
    )


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_multidomain_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    if module.params.get("ext_id"):
        get_resource_group_by_ext_id(module, result)
    else:
        get_resource_groups(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
