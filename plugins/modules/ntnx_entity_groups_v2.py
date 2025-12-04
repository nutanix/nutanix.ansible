#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_entity_groups_v2
short_description: Create, Update, Delete entity groups
version_added: 2.5.0
description:
    - An Entity Group is a logical group of entities supported by flow network security policies.
    - Once created, an Entity Group can be referenced in the network security policies.
    - Create, Update, Delete entity groups
    - This module uses PC v4 APIs based SDKs
options:
    ext_id:
        description:
            - External ID to update or delete specific entity group
        type: str
        required: false
    name:
        description:
            - A short identifier / name of an Entity Group.
        type: str
    description:
        description:
            - A user defined description for an Entity Group.
        type: str
    allowed_config:
        description:
            - Configuration of the allowed entities in the Entity Group.
        type: dict
        suboptions:
            entities:
                description:
                    - List of allowed entities in the Entity Group.
                    - An allowed entity is a collection of acceptable entites.
                type: list
                elements: dict
                suboptions:
                    select_by:
                        description:
                            - Select by field for the allowed entity.
                        type: str
                        choices: ["EXT_ID", "CATEGORY_EXT_ID", "LABELS", "NAME"]
                    type:
                        description:
                            - Type of allowed entity.
                        type: str
                        choices: ["VM", "SUBNET", "VPC", "KUBE_SERVICE", "KUBE_CLUSTER", "KUBE_PODS"]
                    reference_ext_ids:
                        description:
                            - List of reference external identifiers in an allowed entity.
                            - If the selection type is an external identifier, then it is necessary to specify the reference_ext_ids.
                        type: list
                        elements: str
                    kube_entities:
                        description:
                            - List of kube entities in an allowed entity.
                            - If the selection type is kube fields, then it is necessary to specify the kube_entities.
                        type: list
                        elements: str

extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - abhinavbansal29 (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create entity group
  nutanix.ncp.ntnx_entity_groups_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    name: "ansible-entity-group"
    description: "ansible-entity-group-desc"
    allowed_config:
      entities:
        - select_by: CATEGORY_EXT_ID
          type: VM
          reference_ext_ids:
            - "00062ffc-95ad-19e9-185b-ac1f6b6f97a3"
            - "00062ffc-95ad-19e9-185b-ac1f6b6f97a4"
  register: result
  ignore_errors: true

- name: Update entity group
  nutanix.ncp.ntnx_entity_groups_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: present
    ext_id: "b215708c-252f-400c-bc90-2f36242d3d3c"
    name: "ansible-entity-group-updated-name"
    description: "ansible-entity-group-updated-desc"
  register: result
  ignore_errors: true

- name: Delete entity group
  nutanix.ncp.ntnx_entity_groups_v2:
    ext_id: "b215708c-252f-400c-bc90-2f36242d3d3c"
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    validate_certs: false
    state: absent
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
      - Response for entity groups operations
      - Entity group details if C(wait) is True
      - Task details if C(wait) is False
  returned: always
  type: dict
  sample:
    {
        "allowed_config": {
            "entities": [
                {
                    "kube_entities": null,
                    "reference_ext_ids": [
                        "83c8be14-a656-4a53-6e2c-84d0e6b84182",
                        "6742b519-b958-4638-679c-c7b2d151c44a"
                    ],
                    "select_by": "CATEGORY_EXT_ID",
                    "type": "VM"
                }
            ]
        },
        "description": "mkWyftswwhuhansible-eg1_entity_group_desc",
        "ext_id": "b215708c-252f-400c-bc90-2f36242d3d3c",
        "links": null,
        "name": "mkWyftswwhuhansible-eg1_entity_group",
        "owner_ext_id": "00000000-0000-0000-0000-000000000000",
        "policy_ext_ids": null,
        "tenant_id": null
    }

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: str

failed:
    description: This field indicates if the task execution failed
    returned: always
    type: bool
    sample: false

msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or in check mode (in delete operation)
    type: str
    sample: "Failed generating create entity groups Spec"

ext_id:
  description: The entity group ext_id
  returned: always
  type: str
  sample: "63311404-8b2e-4dbf-9e33-7848cc88d330"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.flow.api_client import (  # noqa: E402
    get_entity_groups_api_instance,
    get_etag,
)
from ..module_utils.v4.flow.helpers import get_entity_group  # noqa: E402
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
    import ntnx_microseg_py_client as mic_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as mic_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    entities_sub_spec = dict(
        select_by=dict(
            type="str", choices=["EXT_ID", "CATEGORY_EXT_ID", "LABELS", "NAME"]
        ),
        type=dict(
            type="str",
            choices=[
                "VM",
                "SUBNET",
                "VPC",
                "KUBE_SERVICE",
                "KUBE_CLUSTER",
                "KUBE_PODS",
            ],
        ),
        reference_ext_ids=dict(type="list", elements="str"),
        kube_entities=dict(type="list", elements="str"),
    )
    allowed_config_spec = dict(
        entities=dict(
            type="list",
            elements="dict",
            options=entities_sub_spec,
            obj=mic_sdk.AllowedEntity,
        )
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        description=dict(type="str"),
        allowed_config=dict(
            type="dict",
            options=allowed_config_spec,
            obj=mic_sdk.AllowedConfig,
        ),
    )

    return module_args


def create_entity_group(module, entity_group, result):

    sg = SpecGenerator(module)
    default_spec = mic_sdk.EntityGroup()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create entity groups Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = entity_group.create_entity_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating entity group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.ENTITY_GROUP
        )
        if ext_id:
            resp = get_entity_group(module, entity_group, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_entity_groups_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    if old_spec != update_spec:
        return False

    return True


def update_entity_group(module, entity_group, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_entity_group(module, entity_group, ext_id)
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating entity_groups update spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    # check for idempotency
    if check_entity_groups_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.")

    resp = None
    try:
        resp = entity_group.update_entity_group_by_id(extId=ext_id, body=update_spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating entity_group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id, True)
        resp = get_entity_group(module, entity_group, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_entity_group(module, entity_group, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Entity group with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_entity_group(module, entity_group, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting entity group", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = entity_group.delete_entity_group_by_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting entity_group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_microseg_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "error": None,
        "response": None,
        "ext_id": None,
    }
    entity_group = get_entity_groups_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_entity_group(module, entity_group, result)
        else:
            create_entity_group(module, entity_group, result)
    else:
        delete_entity_group(module, entity_group, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
