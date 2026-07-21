#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_network_controller_v2
short_description: Create, Update, Delete network controller in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update and delete a network controller in Nutanix Prism Central.
  - The network controller is the central Flow Virtual Networking (FVN) orchestration engine
    responsible for advanced networking (VPCs, overlay subnets, floating IPs, NAT gateways).
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Create/Update/Delete a Network Controller) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create network controller.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update network controller.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete network controller.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the network controller.
      - Required for update and delete operations.
    type: str
    required: false
  cloud_substrate:
    description:
      - Underlying cloud substrate on which the network controller is deployed.
      - Applicable for Nutanix Cloud Clusters (NC2) deployments.
    type: str
    required: false
    choices:
      - AWS
      - AZURE
      - GCP
  default_vlan_stack:
    description:
      - The default networking stack used when creating new VLAN backed subnets.
      - C(ADVANCED) enables the OVN based advanced networking stack (required for Flow Virtual Networking features).
      - C(LEGACY) uses the traditional Acropolis networking stack.
    type: str
    required: false
    choices:
      - ADVANCED
      - LEGACY
  vpc_global_config:
    description:
      - Global settings applied to all VPCs managed by this network controller.
    type: dict
    required: false
    suboptions:
      is_overlapping_erps_enabled:
        description:
          - Option to enable or disable overlapping ERPs (External Routable Prefixes) across VPCs.
          - Defaults to false when not set on the server side.
        type: bool
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
    state: present
    default_vlan_stack: ADVANCED
    vpc_global_config:
      is_overlapping_erps_enabled: false
  register: result
  ignore_errors: true

- name: Update network controller
  nutanix.ncp.ntnx_network_controller_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    default_vlan_stack: ADVANCED
    vpc_global_config:
      is_overlapping_erps_enabled: true
  register: result
  ignore_errors: true

- name: Delete network controller
  nutanix.ncp.ntnx_network_controller_v2:
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
      "controller_status": "UP",
      "controller_version": "7.6.0",
      "default_vlan_stack": "LEGACY",
      "ext_id": "98fac596-6e4f-407e-bfbb-89681ca72415",
      "links": null,
      "metadata": null,
      "minimum_ahv_version": "11.2",
      "minimum_nos_version": "7.0",
      "tenant_id": null,
      "vpc_global_config": {
          "is_overlapping_erps_enabled": false
      }
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the network controller.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency or check mode
  returned: When the operation is skipped
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
  sample: "Api Exception raised while creating network controller"
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
    strip_read_only_fields,
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
        is_overlapping_erps_enabled=dict(type="bool", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        cloud_substrate=dict(
            type="str",
            choices=["AWS", "AZURE", "GCP"],
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
    )
    return module_args


READ_ONLY_FIELDS = (
    "controller_status",
    "controller_version",
    "minimum_ahv_version",
    "minimum_nos_version",
    "metadata",
    "links",
    "tenant_id",
)


def _fetch_and_return_controller(module, api_instance, ext_id, result):
    resp = get_network_controller(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(resp.to_dict())


def create_NetworkController(module, result, api_instance):
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
        resp = api_instance.create_network_controller(body=spec)
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
            _fetch_and_return_controller(module, api_instance, ext_id, result)
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
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    for field in READ_ONLY_FIELDS:
        old.pop(field, None)
        new.pop(field, None)
    return old == new


def update_NetworkController(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_network_controller(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating network controller", **result
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
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

    resp = None
    try:
        resp = api_instance.update_network_controller_by_id(
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
        _fetch_and_return_controller(module, api_instance, ext_id, result)
    result["changed"] = True


def delete_NetworkController(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Network controller with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    resp = None
    try:
        resp = api_instance.delete_network_controller_by_id(extId=ext_id)
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
    api_instance = get_network_controllers_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_NetworkController(module, result, api_instance)
        else:
            create_NetworkController(module, result, api_instance)
    else:
        delete_NetworkController(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
