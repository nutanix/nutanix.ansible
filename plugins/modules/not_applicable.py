#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: not_applicable
short_description: Fetch information about Nutanix Prism Central Volume Groups (companion to ntnx_revert_volume_group_v2)
version_added: 2.6.0
description:
  - This module allows you to fetch information about VolumeGroup in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific VolumeGroup.
  - If C(ext_id) is not provided, list multiple VolumeGroup optionally filtered / paginated.
  - This module is the info companion generated alongside the
    C(ntnx_revert_volume_group_v2) action module. Since the Revert Volume Group
    action itself is not a listable/queryable entity, this module lists / gets
    the underlying VolumeGroup so that callers can look up the ext_id used by
    the revert action.
  - This module uses PC v4 APIs based SDKs.
notes:
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  ext_id:
    description:
      - The external identifier of the Volume Group to fetch.
      - When omitted the module lists Volume Groups instead of fetching one.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: List all Volume Groups (used to look up an ext_id for the revert action)
  nutanix.ncp.not_applicable:
  register: vgs

- name: Fetch a specific Volume Group by ext_id
  nutanix.ncp.not_applicable:
    ext_id: "530567f3-abda-4913-b5d0-0ab6758ec165"
  register: vg

- name: List Volume Groups whose name starts with a prefix
  nutanix.ncp.not_applicable:
    filter: "startswith(name, 'ansible-')"
  register: vgs

- name: List at most 10 Volume Groups
  nutanix.ncp.not_applicable:
    limit: 10
  register: vgs
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC VolumeGroup info v4 API.
    - It can be a single VolumeGroup if external ID is provided.
    - List of multiple VolumeGroup if external ID is not provided with optional
      filter or limit.
  returned: always
  type: dict
  sample: {
      "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
      "created_by": null,
      "created_time": null,
      "description": "Volume group",
      "enabled_authentications": null,
      "ext_id": "530567f3-abda-4913-b5d0-0ab6758ec165",
      "is_hidden": null,
      "iscsi_features": null,
      "iscsi_target_name": null,
      "iscsi_target_prefix": null,
      "links": null,
      "load_balance_vm_attachments": null,
      "name": "ansible-vgs-example",
      "sharing_status": null,
      "should_load_balance_vm_attachments": false,
      "storage_features": null,
      "target_name": null,
      "target_prefix": null,
      "target_secret": null,
      "tenant_id": null
  }

ext_id:
  description:
    - The external ID of the Volume Group.
    - Only returned when C(ext_id) is provided as an input.
  returned: when C(ext_id) is provided
  type: str
  sample: "530567f3-abda-4913-b5d0-0ab6758ec165"

total_available_results:
  description:
    - The total number of available VolumeGroup entries in Prism Central.
  returned: when listing without C(ext_id)
  type: int
  sample: 12

changed:
  description:
    - This indicates whether the task resulted in any changes.
    - Always false for info modules.
  returned: always
  type: bool
  sample: false

error:
  description:
    - The error message if any error occurred.
  returned: when an error occurs
  type: str
  sample: "Api Exception raised while fetching Volume Group info"

failed:
  description:
    - This indicates whether the task failed.
  returned: when the task fails
  type: bool
  sample: false

msg:
  description:
    - Status or informational message on error.
  returned: when an error occurs
  type: str
  sample: "Api Exception raised while fetching Volume Group info"
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

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_volume_group(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    try:
        resp = api_instance.get_volume_group_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching Volume Group info",
        )
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict()).get("data")


def list_volume_groups(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating Volume Groups info Spec", **result)
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
    result = {"changed": False, "error": None, "response": None}
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_volume_group(module, api_instance, result)
    else:
        list_volume_groups(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
