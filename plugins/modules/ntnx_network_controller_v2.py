#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_network_controller_v2
short_description: Create, Update, Delete network controllers in Nutanix Prism Central
version_added: 2.6.0
description:
  - This module allows you to create, update, and delete network controllers in Nutanix Prism Central.
  - Creating a network controller enables Flow Virtual Networking on the registered clusters.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Network Controller) -
      Required Roles: Super Admin
    - >-
      B(Update a Network Controller) -
      Required Roles: Super Admin
    - >-
      B(Delete a Network Controller) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and ext_id is not provided then the operation will be create network controller.
      - If C(state) is set to C(present) and ext_id is provided then the operation will be update network controller.
      - If C(state) is set to C(absent) and ext_id is provided then the operation will be delete network controller.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the network controller.
      - Required for update and delete operations.
    type: str
    required: false
  cloud_substrate:
    description:
      - The cloud substrate on which the network controller is deployed.
    type: str
    choices:
      - AZURE
      - AWS
      - GCP
    required: false
  default_vlan_stack:
    description:
      - Default VLAN stack(Legacy or Advanced) to instatiate VLAN-backed subnets on if advanced networking is enabled.
    type: str
    choices:
      - ADVANCED
      - LEGACY
    required: false
  vpc_global_config:
    description:
      - Global settings for all VPCs within the network controller.
    type: dict
    required: false
    suboptions:
      is_overlapping_erps_enabled:
        description:
          - Option to enable or disable overlapping ERPs (External Routable Prefixes) across VPCs.
        type: bool
        required: false
        default: false
  metadata:
    description:
      - Metadata associated with this resource.
    type: dict
    required: false
    suboptions:
      owner_reference_id:
        description:
          - A globally unique identifier that represents the owner of this resource.
        type: str
        required: false
      owner_user_name:
        description:
          - The userName of the owner of this resource.
        type: str
        required: false
      project_reference_id:
        description:
          - A globally unique identifier that represents the project this resource belongs to.
        type: str
        required: false
      project_name:
        description:
          - The name of the project this resource belongs to.
        type: str
        required: false
      category_ids:
        description:
          - A list of globally unique identifiers that represent all the categories the resource is associated with.
        type: list
        elements: str
        required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create network controller
  nutanix.ncp.ntnx_network_controller_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    default_vlan_stack: "ADVANCED"
    vpc_global_config:
      is_overlapping_erps_enabled: false
  register: result
  ignore_errors: true

- name: Update network controller
  nutanix.ncp.ntnx_network_controller_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    vpc_global_config:
      is_overlapping_erps_enabled: true
  register: result
  ignore_errors: true

- name: Delete network controller
  nutanix.ncp.ntnx_network_controller_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting network controller
    - If the operation is create or update and C(wait) is true, it will return the network controller details
    - If the operation is create or update and C(wait) is false, it will return the task details
    - If the operation is delete, it will return the task details
  returned: always
  type: dict
  sample:
    {
      "cloud_substrate": null,
      "controller_health": null,
      "controller_status": "UP",
      "controller_version": "6.5",
      "default_vlan_stack": "ADVANCED",
      "ext_id": "2e40ff57-20aa-4d2b-b179-298db969c20d",
      "links": null,
      "metadata": null,
      "minimum_ahv_version": null,
      "minimum_nos_version": null,
      "project_ext_id": null,
      "tenant_id": null,
      "vpc_global_config": {
          "is_overlapping_erps_enabled": false
      }
    }

task_ext_id:
  description:
    - The external id of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external id of the network controller.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_network_controllers_api_instance,
)
from ..module_utils.v4.network.helpers import get_network_controller  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    vpc_global_config_spec = dict(
        is_overlapping_erps_enabled=dict(type="bool", required=False, default=False),
    )

    metadata_spec = dict(
        owner_reference_id=dict(type="str", required=False),
        owner_user_name=dict(type="str", required=False),
        project_reference_id=dict(type="str", required=False),
        project_name=dict(type="str", required=False),
        category_ids=dict(type="list", elements="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        cloud_substrate=dict(
            type="str",
            choices=["AZURE", "AWS", "GCP"],
            obj=networking_sdk.CloudSubstrate,
        ),
        default_vlan_stack=dict(
            type="str",
            choices=["ADVANCED", "LEGACY"],
            obj=networking_sdk.DefaultVlanStack,
        ),
        vpc_global_config=dict(
            type="dict",
            options=vpc_global_config_spec,
            obj=networking_sdk.VpcGlobalConfig,
        ),
        metadata=dict(
            type="dict",
            options=metadata_spec,
            obj=networking_sdk.Metadata,
        ),
    )
    return module_args


def create_network_controller(module, network_controllers, result):
    sg = SpecGenerator(module)
    default_spec = networking_sdk.NetworkController()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create network controller spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = network_controllers.create_network_controller(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating network controller",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            resp, rel=TASK_CONSTANTS.RelEntityType.NETWORK_CONTROLLER
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_network_controller(module, network_controllers, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Network Controller"
                ),
                msg="Failed to get entity ext_id from task for Network Controller",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    for spec_dict in (old_spec_dict, update_spec_dict):
        metadata = spec_dict.get("metadata") or {}
        category_ids = metadata.get("category_ids")
        if category_ids:
            metadata["category_ids"] = sorted(category_ids)
    return old_spec_dict == update_spec_dict


def update_network_controller(module, network_controllers, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_network_controller(module, network_controllers, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating network controller", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update network controller spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = None
    try:
        resp = network_controllers.update_network_controller_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating network controller",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_network_controller(module, network_controllers, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_network_controller(module, network_controllers, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Network controller with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = network_controllers.delete_network_controller_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting network controller",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    network_controllers = get_network_controllers_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_network_controller(module, network_controllers, result)
        else:
            create_network_controller(module, network_controllers, result)
    elif state == "absent":
        delete_network_controller(module, network_controllers, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
