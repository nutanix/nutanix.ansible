#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_external_iscsi_attachmentsinfo_v2
short_description: Fetch external iSCSI attachments of a Volume Group in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to fetch information about ExternalIscsiAttachmentsByVolumeGroupId in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific ExternalIscsiAttachmentsByVolumeGroupId.
  - If C(ext_id) is not provided, list multiple ExternalIscsiAttachmentsByVolumeGroupId optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(List external iSCSI attachments by Volume Group) -
    Required Roles: View_Volume_Group_iSCSI_Attachments or View_Volume_Group.
    When C(expand) is used, the caller must also possess View_External_iSCSI_Client.
  - The underlying B(list_external_iscsi_attachments_by_volume_group_id) v4 API is B(deprecated).
    Prefer M(nutanix.ncp.ntnx_volume_groups_info_v2) which returns attachments inline on the Volume Group resource.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  volume_group_ext_id:
    description:
      - The external ID of the Volume Group whose external iSCSI attachments should be listed.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of a specific external iSCSI attachment (iSCSI client).
      - When provided, only the matching attachment for the given C(volume_group_ext_id) is returned.
    type: str
    required: false
  expand:
    description:
      - OData C($expand) query parameter that allows clients to request related resources when a resource is retrieved.
      - Only the fields listed in the SDK are supported; consult the v4 API reference for allowed expand items.
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
- name: List all external iSCSI attachments for a Volume Group
  nutanix.ncp.ntnx_volume_group_external_iscsi_attachmentsinfo_v2:
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
  register: attachments

- name: Fetch a specific external iSCSI attachment by ext_id
  nutanix.ncp.ntnx_volume_group_external_iscsi_attachmentsinfo_v2:
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    ext_id: "aea43b5c-ae4d-4b60-934b-f8f581275dec"
  register: attachment

- name: List external iSCSI attachments with a limit and OData filter
  nutanix.ncp.ntnx_volume_group_external_iscsi_attachmentsinfo_v2:
    volume_group_ext_id: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"
    limit: 10
    filter: "startswith(iscsiInitiatorName, 'iqn')"
  register: filtered_attachments
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC ExternalIscsiAttachmentsByVolumeGroupId info v4 API.
    - It can be a single ExternalIscsiAttachmentsByVolumeGroupId if external ID is provided.
    - List of multiple ExternalIscsiAttachmentsByVolumeGroupId if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "attachment_site": "PRIMARY",
        "attached_targets": [],
        "client_secret": null,
        "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
        "enabled_authentications": "NONE",
        "ext_id": "aea43b5c-ae4d-4b60-934b-f8f581275dec",
        "iscsi_initiator_name": "iqn.1991-05.com.microsoft:ansible-client",
        "iscsi_initiator_network_id": null,
        "links": [
            {
                "href": "https://10.44.76.28:9440/api/volumes/v4.2/config/iscsi-clients/aea43b5c-ae4d-4b60-934b-f8f581275dec",
                "rel": "external_attachment"
            }
        ],
        "num_virtual_targets": 32,
        "tenant_id": null
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while listing external iSCSI attachments for Volume Group"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the external iSCSI attachment
  type: str
  returned: when external ID is provided
  sample: "aea43b5c-ae4d-4b60-934b-f8f581275dec"

volume_group_ext_id:
  description: External ID of the Volume Group being queried
  type: str
  returned: always
  sample: "0005b6b1-0b3b-4b3b-8b3b-0b3b4b3b4b35"

total_available_results:
  description: The total number of available external iSCSI attachments for the Volume Group.
  type: int
  returned: when all attachments are fetched (no ext_id given)
  sample: 3
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
from ..module_utils.v4.volumes.helpers import (  # noqa: E402
    get_external_iscsi_attachment_by_ext_id,
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


def get_external_iscsi_attachment(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    ext_id = module.params.get("ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id
    result["ext_id"] = ext_id

    entity = get_external_iscsi_attachment_by_ext_id(
        module, api_instance, volume_group_ext_id, ext_id
    )
    if entity is None:
        result["failed"] = True
        module.fail_json(
            msg=(
                "External iSCSI attachment with ext_id '{0}' was not found on "
                "Volume Group '{1}'."
            ).format(ext_id, volume_group_ext_id),
            **result,
        )

    result["response"] = strip_internal_attributes(entity.to_dict())


def get_external_iscsi_attachments(module, api_instance, result):
    volume_group_ext_id = module.params.get("volume_group_ext_id")
    result["volume_group_ext_id"] = volume_group_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params, extra_params=["expand"])
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating info spec for external iSCSI attachments", **result
        )

    try:
        resp = api_instance.list_external_iscsi_attachments_by_volume_group_id(
            volumeGroupExtId=volume_group_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while listing external iSCSI attachments "
                "for Volume Group {0}"
            ).format(volume_group_ext_id),
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
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "failed": False,
    }
    api_instance = get_vg_api_instance(module)
    if module.params.get("ext_id"):
        get_external_iscsi_attachment(module, api_instance, result)
    else:
        get_external_iscsi_attachments(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
