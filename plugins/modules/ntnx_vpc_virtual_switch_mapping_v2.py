#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vpc_virtual_switch_mapping_v2
short_description: Set VPC for virtual switch mappings traffic config
version_added: 2.6.0
description:
  - Configures and updates VPC to Virtual Switch mappings for specific clusters.
  - It allows targeted updates by applying configurations only to the clusters explicitly provided in the payload.
  - One or more mappings can be submitted in a single invocation (up to 200 items per the API).
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Set VPC for virtual switch mappings traffic config) -
      Required Roles: Prism Admin, Super Admin, VPC Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - State of the VPC virtual switch mapping.
      - Only present is supported.
    type: str
    required: false
    default: present
    choices:
      - present
  virtual_switch_mappings:
    description:
      - List of VPC virtual switch mappings to apply in a single call.
    type: list
    elements: dict
    required: true
    suboptions:
      virtual_switch_uuid:
        description: UUID of the virtual switch.
        type: str
        required: true
      cluster_uuids:
        description: UUIDs of the clusters.
        type: list
        elements: str
      is_all_traffic_permitted:
        description:
          - Whether to permit all traffic through virtual switch or only the ICMP and statistics collection requests.
        type: bool
      metadata:
        description: Metadata associated with this resource.
        type: dict
        suboptions:
          owner_reference_id:
            description: A globally unique identifier that represents the owner of this resource.
            type: str
          owner_user_name:
            description: The userName of the owner of this resource.
            type: str
          project_reference_id:
            description: A globally unique identifier that represents the project this resource belongs to.
            type: str
          project_name:
            description: The name of the project this resource belongs to.
            type: str
          category_ids:
            description: A list of globally unique identifiers that represent all the categories the resource is associated with.
            type: list
            elements: str
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
- name: Set VPC virtual switch mappings
  nutanix.ncp.ntnx_vpc_virtual_switch_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    virtual_switch_mappings:
      - virtual_switch_uuid: "ae3db57a-49ef-471b-8480-b6f03b577af6"
        cluster_uuids:
          - "d5534b54-4b54-4b54-4b54-d5534b544b54"
          - "d5534b54-4b54-4b54-4b54-d5534b544b55"
        is_all_traffic_permitted: true
      - virtual_switch_uuid: "ae3db57a-49ef-471b-8480-b6f03b577af6"
        cluster_uuids:
          - "d5534b54-4b54-4b54-4b54-d5534b544b54"
        is_all_traffic_permitted: false
        metadata:
          owner_reference_id: "123e4567-e89b-12d3-a456-426614174000"
          owner_user_name: "admin"
          project_reference_id: "123e4567-e89b-12d3-a456-426614174000"
          project_name: "project_name"
          category_ids:
            - "123e4567-e89b-12d3-a456-426614174000"
            - "123e4567-e89b-12d3-a456-426614174001"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for setting VPC virtual switch mappings.
    - It contains task details for the set operation.
  returned: always
  type: dict

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error or check mode.
  type: str

error:
  description: This field typically holds information about errors that occurred during the task execution.
  returned: When an error occurs.
  type: str

task_ext_id:
  description: The external ID of the task created by the set operation.
  returned: when available
  type: str

failed:
  description: This field typically holds information about if the task has failed.
  returned: always
  type: bool
  sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_vpc_virtual_switch_mappings_api_instance,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as net_sdk  # noqa: E402
except ImportError:
    from ..module_utils.v4.sdk_mock import mock_sdk as net_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_mapping_spec():
    metadata_spec = dict(
        owner_reference_id=dict(type="str"),
        owner_user_name=dict(type="str"),
        project_reference_id=dict(type="str"),
        project_name=dict(type="str"),
        category_ids=dict(type="list", elements="str"),
    )

    return dict(
        virtual_switch_uuid=dict(type="str", required=True),
        cluster_uuids=dict(type="list", elements="str"),
        is_all_traffic_permitted=dict(type="bool"),
        metadata=dict(type="dict", options=metadata_spec, obj=net_sdk.Metadata),
    )


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        virtual_switch_mappings=dict(
            type="list",
            elements="dict",
            required=True,
            options=get_mapping_spec(),
            obj=net_sdk.VpcVirtualSwitchMapping,
        ),
    )

    return module_args


def set_vpc_virtual_switch_mappings(module, api_instance, result):
    sg = SpecGenerator(module)
    mapping_args = get_mapping_spec()

    body = []
    for item in module.params["virtual_switch_mappings"]:
        default_spec = net_sdk.VpcVirtualSwitchMapping()
        spec, err = sg.generate_spec(
            obj=default_spec, attr=item, module_args=mapping_args
        )
        if err:
            result["error"] = err
            module.fail_json(
                msg="Failed generating VPC virtual switch mapping Spec", **result
            )
        body.append(spec)

    if module.check_mode:
        result["response"] = [strip_internal_attributes(s.to_dict()) for s in body]
        return

    resp = None
    try:
        resp = api_instance.create_vpc_virtual_switch_mapping(body=body)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while setting VPC virtual switch mappings",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
        "task_ext_id": None,
    }
    api_instance = get_vpc_virtual_switch_mappings_api_instance(module)
    set_vpc_virtual_switch_mappings(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
