#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_resource_groups_info_v2
short_description: Fetch resource group information using Nutanix v4 APIs
version_added: "2.6.0"
description:
    - Fetch information about resource groups from Nutanix Prism Central.
    - Retrieve a single resource group by external ID or list all resource groups with optional filters.
    - This module uses PC v4 APIs based SDKs.
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
    - Abhinav Bansal (@abhinavbansal29)
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

- name: List resource groups with limit
  nutanix.ncp.ntnx_resource_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    limit: 5
  register: result
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC Resource Groups info v4 API.
        - It can be a single resource group if external ID is provided.
        - List of multiple resource groups if external ID is not provided.
    returned: always
    type: dict
    sample: "<Need to add sample>"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

ext_id:
    description: The external ID of the resource group.
    returned: When single entity is fetched
    type: str
    sample: "00000000-0000-0000-0000-000000000000"

total_available_results:
    description: Total number of available results when listing resource groups.
    returned: When listing resource groups
    type: int
    sample: 5

msg:
    description: Additional message about the operation.
    returned: When there is an error
    type: str

error:
    description: This field holds information about errors that occurred during the task execution.
    returned: When an error occurs
    type: str

failed:
    description: This indicates whether the task failed.
    returned: When something fails
    type: bool
    sample: true
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_resource_groups_api_instance,
)
from ..module_utils.v4.multidomain.helpers import get_resource_group  # noqa: E402
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


def get_resource_group_by_ext_id(module, resource_groups, result):
    """
    Fetch a single resource group by its external ID.
    Args:
        module: Ansible module object
        resource_groups: ResourceGroupsApi instance
        result: Result dict to populate
    """
    ext_id = module.params.get("ext_id")
    resp = get_resource_group(module, resource_groups, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_resource_groups_list(module, resource_groups, result):
    """
    List resource groups with optional filters and pagination.
    Args:
        module: Ansible module object
        resource_groups: ResourceGroupsApi instance
        result: Result dict to populate
    """
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating list resource groups spec", **result)

    try:
        resp = resource_groups.list_resource_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while listing resource groups",
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

    resource_groups = get_resource_groups_api_instance(module)

    if module.params.get("ext_id"):
        get_resource_group_by_ext_id(module, resource_groups, result)
    else:
        get_resource_groups_list(module, resource_groups, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
