#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_groups_info_v2
short_description: Fetch information about Nutanix Prism Central Volume Groups.
version_added: "2.0.0"
description:
  - This module allows you to fetch information about VolumeGroup in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VolumeGroup.
  - If C(ext_id) is not provided, list multiple VolumeGroup optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Get a Volume Group) -
    Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin, Prism Viewer,
    Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(List all the Volume Groups) -
    Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin, Prism Viewer,
    Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  ext_id:
    description:
      - The external identifier of the Volume Group.
      - When provided, fetch a single Volume Group.
    type: str
    required: false
  expand:
    description:
      - A URL query parameter that allows clients to request related resources
        along with the Volume Group they retrieve.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Pradeepsingh Bhati (@bhati-pradeep)
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch information about all Volume Groups
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
  register: result

- name: Fetch information about a specific Volume Group
  nutanix.ncp.ntnx_volume_groups_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "530567f3-abda-4913-b5d0-0ab6758ec1653"
  register: result

- name: List Volume Groups filtered by name
  nutanix.ncp.ntnx_volume_groups_info_v2:
    filter: "startswith(name, 'ansible')"
  register: result

- name: List Volume Groups with limit
  nutanix.ncp.ntnx_volume_groups_info_v2:
    limit: 1
  register: result
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VolumeGroup info v4 API.
    - It can be a single VolumeGroup if external ID is provided.
    - List of multiple VolumeGroup if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample: {
    "attachment_type": null,
    "attachments": null,
    "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
    "created_by": null,
    "description": "Volume group 2",
    "disks": null,
    "enabled_authentications": null,
    "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
    "hydration_status": null,
    "is_hidden": null,
    "iscsi_features": {
      "enabled_authentications": "CHAP",
      "target_secret": null
    },
    "links": null,
    "name": "ansible-vgs-KjRMtTRxhrww2",
    "protocol": null,
    "sharing_status": "SHARED",
    "should_load_balance_vm_attachments": true,
    "storage_features": {
      "flash_mode": {
        "is_enabled": true
      }
    },
    "target_name": "vg1-792cd764-37b5-4da3-7ef1-ea3f618c1648",
    "target_prefix": null,
    "tenant_id": null,
    "usage_type": "USER"
  }
ext_id:
  description: Volume Group external identifier.
  type: str
  returned: When C(ext_id) is provided.
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b3b"
changed:
  description: Indicates whether the resource has changed.
  type: bool
  returned: always
  sample: false
failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching Volume Group info"
error:
  description: The error message if any.
  type: str
  returned: when error occurs
  sample: "Failed generating Volume Groups info Spec"
total_available_results:
  description:
    - The total number of available Volume Groups in Prism Central.
  type: int
  returned: when list operation is performed
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
from ..module_utils.v4.volumes.api_client import get_vg_api_instance  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        expand=dict(type="str"),
    )
    return module_args


def get_volume_group_by_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    kwargs = {}
    if module.params.get("expand"):
        kwargs["_expand"] = module.params.get("expand")
    try:
        resp = api_instance.get_volume_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Group info",
        )

    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def get_volume_groups(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Volume Groups info Spec", **result)

    if module.params.get("expand"):
        kwargs["_expand"] = module.params.get("expand")

    try:
        resp = api_instance.list_volume_groups(**kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Groups info",
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
    result = {"changed": False, "response": None, "failed": False}
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_volume_group_by_ext_id(module, api_instance, result)
    else:
        get_volume_groups(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
