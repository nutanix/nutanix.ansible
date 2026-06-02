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
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(List resource groups) -
      Required Roles: Backup Admin, Cluster Admin, Cluster Viewer, Consumer, CSI System, Developer,
      Disaster Recovery Admin, Disaster Recovery Viewer, File Server Security Admin,
      File Server Share Admin, Files Admin, Files Viewer, Flow Admin, Flow Policy Author, Flow Viewer,
      Internal Super Admin, Kubernetes Data Services System, Kubernetes Infrastructure Provision,
      License Admin, License Viewer, LocalAccountManager Admin, LocalAccountManager Viewer,
      Monitoring Admin, Monitoring Viewer, NCM Connector, Network Infra Admin, Objects Admin, Operator,
      Prism Admin, Prism Viewer, Project Admin, Project Manager, Security Dashboard Admin,
      Security Dashboard Viewer, Storage Admin, Storage Viewer, Super Admin, Tenant Admin,
      Tenant Consumer, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - >-
      B(Get resource group by external ID) -
      Required Roles: Backup Admin, Cluster Admin, Cluster Viewer, Consumer, CSI System, Developer,
      Disaster Recovery Admin, Disaster Recovery Viewer, File Server Security Admin,
      File Server Share Admin, Files Admin, Files Viewer, Flow Admin, Flow Policy Author, Flow Viewer,
      Internal Super Admin, Kubernetes Data Services System, Kubernetes Infrastructure Provision,
      License Admin, License Viewer, LocalAccountManager Admin, LocalAccountManager Viewer,
      Monitoring Admin, Monitoring Viewer, NCM Connector, Network Infra Admin, Objects Admin, Operator,
      Prism Admin, Prism Viewer, Project Admin, Project Manager, Security Dashboard Admin,
      Security Dashboard Viewer, Storage Admin, Storage Viewer, Super Admin, Tenant Admin,
      Tenant Consumer, Virtual Machine Admin, Virtual Machine Operator, Virtual Machine Viewer, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=multidomain)"
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
    ext_id: "384280b2-8f08-414a-b7b6-68a1b522001a"
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
        - List of multiple resource groups with optional filters if external ID is not provided.
    returned: always
    type: dict
    sample: [
            {
                "capabilities": null,
                "create_time": "2026-05-19T14:45:36.847543+00:00",
                "created_by": "00000000-0000-0000-0000-000000000000",
                "ext_id": "c8275149-4468-47e9-5adc-9d441157c94a",
                "last_update_time": "2026-05-19T14:45:36.847543+00:00",
                "last_updated_by": "00000000-0000-0000-0000-000000000000",
                "links": null,
                "name": "my-resource-group-1",
                "placement_targets": null,
                "project_ext_id": "532477b8-53eb-5ec4-8c1a-a458e70bc7e9",
                "tenant_id": null,
            },
            {
                "capabilities": null,
                "create_time": "2026-05-19T14:45:40.129823+00:00",
                "created_by": "00000000-0000-0000-0000-000000000000",
                "ext_id": "14669a45-1ee4-4b62-619e-2401c9a35621",
                "last_update_time": "2026-05-19T14:45:40.129823+00:00",
                "last_updated_by": "00000000-0000-0000-0000-000000000000",
                "links": null,
                "name": "my-resource-group-2",
                "placement_targets": [
                    {
                        "capabilities": null,
                        "cluster_ext_id": "000651ae-e050-d250-2d7a-5254001a3d38",
                        "storage_containers": [
                            {
                                "capabilities": null,
                                "ext_id": "5d4f7039-b1d4-437c-9b0e-c34a87e08583",
                            },
                        ],
                    },
                ],
                "project_ext_id": "4b53a755-0e1e-593c-9798-d179db2df309",
                "tenant_id": null,
            },
        ]

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
    sample: "Api Exception raised while fetching resource groups info"
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

import warnings  # noqa: E402

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
