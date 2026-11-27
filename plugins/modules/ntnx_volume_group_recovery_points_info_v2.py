#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_volume_group_recovery_points_info_v2
short_description: Fetch volume group recovery points info from Nutanix Prism Central
version_added: "2.7.0"
description:
  - This module allows you to fetch information about volume group recovery points in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific volume group recovery point.
  - If C(ext_id) is not provided, list multiple volume group recovery points optionally filtered or paginated.
  - This module uses PC v4 APIs based SDKs
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get a Volume Group Recovery Point) -
    Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - >-
    B(List Volume Group Recovery Points) -
    Required Roles: Backup Admin, CSI System, Disaster Recovery Admin, Disaster Recovery Viewer, Kubernetes Data Services System, Prism Admin, Prism Viewer, Project Manager, Storage Admin, Storage Viewer, Super Admin, Self-Service Admin (deprecated)
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=volumes)"
options:
  ext_id:
    description:
      - The External ID of the volume group recovery point.
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
- name: Get volume group recovery point by external ID
  nutanix.ncp.ntnx_volume_group_recovery_points_info_v2:
    ext_id: "b387359d-fa5c-4d58-9eb2-3af1a4976319"
  register: result
  ignore_errors: true

- name: List all volume group recovery points
  nutanix.ncp.ntnx_volume_group_recovery_points_info_v2:
  register: result
  ignore_errors: true

- name: List volume group recovery points with filter
  nutanix.ncp.ntnx_volume_group_recovery_points_info_v2:
    filter: "volumeGroupName eq 'vg1'"
  register: result
  ignore_errors: true

- name: List volume group recovery points with limit
  nutanix.ncp.ntnx_volume_group_recovery_points_info_v2:
    limit: 1
  register: result
  ignore_errors: true

- name: List all volume group recovery points with fetch_all
  nutanix.ncp.ntnx_volume_group_recovery_points_info_v2:
    fetch_all: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix volume group recovery points info v4 API (host is Prism Central).
    - It can be a single volume group recovery point if External ID is provided.
    - List of multiple volume group recovery points if External ID is not provided with optional filter, limit, or fetch_all.
  returned: always
  type: dict
  sample:
    {
      "consistency_group_ext_id": null,
      "creation_time": "2024-08-22T03:23:36.701254+00:00",
      "disk_recovery_points": [
        {
          "disk_ext_id": "839feff9-bac0-4a70-9523-82ea9e431517",
          "disk_recovery_point_ext_id": "21d467f0-ccef-4733-91cc-f04db58a92eb"
        }
      ],
      "expiration_time": "2092-09-09T06:37:42+00:00",
      "ext_id": "b387359d-fa5c-4d58-9eb2-3af1a4976319",
      "links": null,
      "location_agnostic_id": "e5e1a71b-4911-480d-a4d4-3a175797c401",
      "location_references": [
        {
          "location_ext_id": "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
        }
      ],
      "name": "test_vg_rp",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "recovery_point_type": "CRASH_CONSISTENT",
      "status": "COMPLETE",
      "tenant_id": null,
      "volume_group_ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
      "volume_group_name": "ansible-vg-test",
      "volume_group": {
        "cluster_reference": "00061663-9fa0-28ca-185b-ac1f6b6f97e2",
        "description": "Volume group",
        "ext_id": "792cd764-37b5-4da3-7ef1-ea3f618c1648",
        "name": "ansible-vg-test",
        "sharing_status": "SHARED"
      }
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching volume group recovery points info"

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
  description: External ID of the volume group recovery point.
  type: str
  returned: when external ID is provided
  sample: "b387359d-fa5c-4d58-9eb2-3af1a4976319"

total_available_results:
  description: The total number of available volume group recovery points on Prism Central.
  type: int
  returned: when volume group recovery points are listed
  sample: 5
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    list_entities,
    raise_api_exception,
    strip_internal_attributes,
)
from ..module_utils.v4.volumes.api_client import (  # noqa: E402
    get_volume_group_recovery_points_api_instance,
)
from ..module_utils.v4.volumes.helpers import (  # noqa: E402
    get_volume_group_recovery_point,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    return module_args


def get_volume_group_recovery_point_using_ext_id(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    resp = get_volume_group_recovery_point(module, api_instance, ext_id)
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def get_volume_group_recovery_points(module, api_instance, result):
    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating volume group recovery points info spec",
            **result,
        )

    try:
        resp = list_entities(
            api_instance.list_volume_group_recovery_points,
            kwargs=kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg=(
                "Api Exception raised while fetching "
                "volume group recovery points info"
            ),
        )

    resp = strip_internal_attributes(resp.to_dict())
    total_available_results = resp.get("metadata", {}).get("total_available_results")
    result["total_available_results"] = total_available_results
    data = resp.get("data") or []
    result["response"] = data


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
    api_instance = get_volume_group_recovery_points_api_instance(module)
    if module.params.get("ext_id"):
        get_volume_group_recovery_point_using_ext_id(module, api_instance, result)
    else:
        get_volume_group_recovery_points(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
