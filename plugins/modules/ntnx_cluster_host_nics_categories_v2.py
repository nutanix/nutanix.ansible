#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_host_nics_categories_v2
short_description: Associate or disassociate categories with a host NIC
version_added: "2.7.0"
description:
    - This module allows you to associate or disassociate categories with a host NIC in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Associate Host Nic Categories) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - >-
      B(Disassociate Host Nic Categories) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - The state of the category association.
      - If C(present), the module will associate the provided categories with the host NIC.
      - If C(absent), the module will disassociate the provided categories from the host NIC.
    type: str
    choices: [present, absent]
    default: present
  cluster_ext_id:
    description:
      - Indicates the UUID of a cluster.
    type: str
    required: true
  host_ext_id:
    description:
      - Indicates the UUID of a host.
    type: str
    required: true
  ext_id:
    description:
      - Indicates the UUID of a host NIC.
    type: str
    required: true
  categories:
    description:
      - List of extIds of the categories to be updated for the entity.
    type: list
    elements: str
    required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Associate categories with host NIC
  nutanix.ncp.ntnx_cluster_host_nics_categories_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
    categories:
      - "f7c8a907-b7ec-409d-b626-3b69ac3a0e4e"
    state: present
  register: result
  ignore_errors: true

- name: Disassociate categories from host NIC
  nutanix.ncp.ntnx_cluster_host_nics_categories_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    host_ext_id: "af49a0bb-b3d7-41c0-b9c2-f4ca0e8763e9"
    ext_id: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
    categories:
      - "f7c8a907-b7ec-409d-b626-3b69ac3a0e4e"
    state: absent
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for associating or disassociating categories with a host NIC.
    - If C(wait) is true, it will contain the final task payload after completion.
    - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
        "cluster_ext_ids": [
            "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
        ],
        "completed_time": "2026-07-20T12:20:41.524581+00:00",
        "created_time": "2026-07-20T12:19:47.167906+00:00",
        "entities_affected": [
            {
                "ext_id": "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821",
                "rel": "clustermgmt:config:host-nic"
            }
        ],
        "error_messages": null,
        "ext_id": "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1",
        "is_cancelable": false,
        "last_updated_time": "2026-07-20T12:20:41.524581+00:00",
        "legacy_error_message": null,
        "operation": "AssociateCategoriesToHostNic",
        "operation_description": "Associate categories to host NIC",
        "owned_by": {
            "ext_id": "00000000-0000-0000-0000-000000000000",
            "name": "admin"
        },
        "parent_task": null,
        "progress_percentage": 100,
        "started_time": "2026-07-20T12:19:47.185754+00:00",
        "status": "SUCCEEDED",
        "sub_steps": null,
        "sub_tasks": null,
        "warnings": null
    }
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
msg:
  description: This indicates the message if any message occurred
  returned: When there is an error
  type: str
  sample: "Api Exception raised while associating categories to host NIC"
error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str
failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false
task_ext_id:
  description: The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
ext_id:
  description: The external ID of the host NIC.
  returned: always
  type: str
  sample: "d6e2eec2-8d68-4b9c-a3f5-cfc9f9b7a821"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_clusters_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as cluster_management_sdk  # noqa: E402  # fmt: skip

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        host_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
        categories=dict(type="list", elements="str", required=True),
    )
    return module_args


def associate_categories(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for associate categories", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.associate_categories_to_host_nic(
            clusterExtId=cluster_ext_id, hostExtId=host_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while associating categories to host NIC",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def disassociate_categories(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("host_ext_id")
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.CategoryEntityReferences()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for disassociate categories", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.disassociate_categories_from_host_nic(
            clusterExtId=cluster_ext_id, hostExtId=host_ext_id, extId=ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating categories from host NIC",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}
    state = module.params.get("state")
    api_instance = get_clusters_api_instance(module)
    if state == "present":
        associate_categories(module, result, api_instance)
    else:
        disassociate_categories(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
