#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_external_attachments_info_v2
short_description: Fetch iSCSI external attachments info for a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ExternalAttachment in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ExternalAttachment.
  - If C(ext_id) is not provided, list multiple ExternalAttachment optionally filtered / paginated.
  - This module uses the PC v4 storage APIs (ntnx_storage_py_client).
options:
  volume_group_ext_id:
    description:
      - The external ID of the parent Volume Group.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific iSCSI external attachment on the Volume Group.
      - If provided, only the matching attachment is returned.
    type: str
    required: false
  expand:
    description:
      - OData ``$expand`` value passed to the SDK's C(_expand) parameter.
      - Allows related resources to be included in the response.
      - Supported expansion key(s) - C(cluster).
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
- name: Get iSCSI external attachment on a Volume Group using ext_id
  nutanix.ncp.ntnx_volume_group_external_attachments_info_v2:
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
  register: attachment_info

- name: List all iSCSI external attachments on a Volume Group
  nutanix.ncp.ntnx_volume_group_external_attachments_info_v2:
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
  register: attachments_list

- name: List iSCSI external attachments with filter
  nutanix.ncp.ntnx_volume_group_external_attachments_info_v2:
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
    filter: "startswith(clusterReference, '00061663')"

- name: List iSCSI external attachments with limit
  nutanix.ncp.ntnx_volume_group_external_attachments_info_v2:
    volume_group_ext_id: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"
    limit: 5
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ExternalAttachment info v4 API.
    - It can be a single ExternalAttachment if external ID is provided.
    - List of multiple ExternalAttachment if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "attachment_site": "PRIMARY",
        "client_secret": null,
        "cluster_name": null,
        "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
        "created_time": null,
        "enabled_authentications": "NONE",
        "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
        "iscsi_initiator_name": "iqn.1991-05.com.microsoft:ansible-host-01",
        "iscsi_initiator_network_id": null,
        "iscsi_target_names": null,
        "links": null,
        "target_params": [
          {
            "num_virtual_targets": 32
          }
        ],
        "tenant_id": null
      }
    ]

changed:
  description: Indicates whether the module made any changes on the cluster. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: Status or error message.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching external attachments for Volume Group"

error:
  description: Error message returned by the API (if any).
  returned: When an error occurs
  type: str

failed:
  description: Indicates whether the task failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the iSCSI external attachment (only on get-by-ID).
  returned: when external ID is provided
  type: str
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

volume_group_ext_id:
  description: External ID of the parent Volume Group.
  returned: always
  type: str
  sample: "00061663-9fa0-28ca-185b-ac1f6b6f97e2"

total_available_results:
  description: The total number of external attachments available for the Volume Group.
  returned: when all external attachments are listed
  type: int
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import get_vg_api_instance  # noqa: E402
from ..module_utils.v4.storage.helpers import (  # noqa: E402
    get_external_attachment_by_ext_id,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        volume_group_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
        expand=dict(type="str", required=False),
    )
    return module_args


def get_external_attachment_using_ext_id(module, api_instance, result):
    """Fetch a single external attachment by ext_id from the given Volume Group."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")

    attachment = get_external_attachment_by_ext_id(
        module, api_instance, volume_group_ext_id, ext_id
    )
    if attachment is None:
        module.fail_json(
            msg=(
                "External attachment with ext_id '{0}' was not found on Volume Group "
                "'{1}'.".format(ext_id, volume_group_ext_id)
            ),
            **result,
        )
    result["ext_id"] = ext_id
    result["volume_group_ext_id"] = volume_group_ext_id
    result["response"] = strip_internal_attributes(attachment.to_dict())


def list_external_attachments(module, api_instance, result):
    """List external attachments on the given Volume Group with optional OData params."""
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating external attachments info spec", **result
        )

    try:
        resp = api_instance.get_external_attachments(
            extId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching external attachments for Volume Group",
        )

    total_available_results = getattr(resp.metadata, "total_available_results", None)
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
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "volume_group_ext_id": None,
    }
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_external_attachment_using_ext_id(module, api_instance, result)
    else:
        list_external_attachments(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
