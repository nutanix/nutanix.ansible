#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_resource_groups_v2
short_description: Create, update, and delete resource groups in Nutanix Prism Central using v4 APIs.
version_added: "2.1.0"
description:
    - Create, update, and delete resource groups in Nutanix Prism Central.
    - Resource groups define placement targets (clusters and storage containers)
      where resources within a project can be deployed.
    - This module uses the v4 multidomain API.
options:
    ext_id:
        description:
            - The external ID (UUID) of the resource group.
            - Required for update and delete operations.
        type: str
    name:
        description:
            - Name of the resource group.
            - Required for create operations.
            - Maximum 64 characters.
        type: str
    project_ext_id:
        description:
            - UUID of the project that owns this resource group.
        type: str
    placement_targets:
        description:
            - List of placement targets defining where resources can be deployed.
        type: list
        elements: dict
        suboptions:
            cluster_ext_id:
                description:
                    - UUID of the AOS cluster.
                type: str
            storage_containers:
                description:
                    - List of storage containers available for this cluster target.
                type: list
                elements: dict
                suboptions:
                    ext_id:
                        description:
                            - UUID of the storage container.
                        type: str
                    capabilities:
                        description:
                            - Capabilities and features of the storage container.
                            - Each item is a key-value pair.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description:
                                    - The key of the key-value pair.
                                type: str
                            value:
                                description:
                                    - The value associated with the key.
                                type: raw
            capabilities:
                description:
                    - Capabilities and features available at this placement target.
                    - Each item is a key-value pair.
                type: list
                elements: dict
                suboptions:
                    name:
                        description:
                            - The key of the key-value pair.
                        type: str
                    value:
                        description:
                            - The value associated with the key.
                        type: raw
    capabilities:
        description:
            - Capabilities and features for this resource group.
            - Each item is a key-value pair.
        type: list
        elements: dict
        suboptions:
            name:
                description:
                    - The key of the key-value pair.
                type: str
            value:
                description:
                    - The value associated with the key.
                type: raw
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Nutanix Ansible Team
"""

EXAMPLES = r"""
- name: Create a resource group
  nutanix.ncp.ntnx_resource_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    name: "my-resource-group"
    project_ext_id: "{{ project_ext_id }}"
    placement_targets:
      - cluster_ext_id: "{{ cluster_ext_id }}"
  register: result

- name: Update a resource group
  nutanix.ncp.ntnx_resource_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    wait: true
    ext_id: "{{ resource_group_ext_id }}"
    name: "my-resource-group-updated"
  register: result

- name: Delete a resource group
  nutanix.ncp.ntnx_resource_groups_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    wait: true
    ext_id: "{{ resource_group_ext_id }}"
  register: result
"""

RETURN = r"""
response:
    description:
        - The resource group response object.
        - Contains resource group details when C(wait) is true.
        - Contains task details when C(wait) is false.
    returned: always
    type: dict
    sample: {
        "name": "my-resource-group",
        "project_ext_id": "00000000-0000-0000-0000-000000000000",
        "ext_id": "00000000-0000-0000-0000-000000000001",
        "placement_targets": [
            {
                "cluster_ext_id": "00000000-0000-0000-0000-000000000002"
            }
        ]
    }
changed:
    description: Whether the state of the resource group was changed.
    returned: always
    type: bool
    sample: true
ext_id:
    description: The external ID of the resource group.
    returned: when available
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
task_ext_id:
    description: The external ID of the task created for the operation.
    returned: when a task is created
    type: str
    sample: "00000000-0000-0000-0000-000000000000"
skipped:
    description: Whether the operation was skipped due to no changes.
    returned: when idempotency check determines no update needed
    type: bool
    sample: true
msg:
    description: Additional message about the operation.
    returned: when applicable
    type: str
    sample: "Resource group with ext_id:xxx will be deleted."
"""

import traceback  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.multidomain.api_client import (  # noqa: E402
    get_etag,
    get_resource_groups_api_instance,
)
from ..module_utils.v4.multidomain.helpers import (  # noqa: E402
    get_resource_group,
)
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
    import ntnx_multidomain_py_client as multidomain_sdk  # noqa: E402
except ImportError:
    multidomain_sdk = None
    SDK_IMP_ERROR = traceback.format_exc()


def get_module_spec():
    kv_pair_spec = dict(
        name=dict(type="str"),
        value=dict(type="raw"),
    )

    storage_container_spec = dict(
        ext_id=dict(type="str"),
        capabilities=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            obj=multidomain_sdk.KVPair if multidomain_sdk else None,
        ),
    )

    placement_target_spec = dict(
        cluster_ext_id=dict(type="str"),
        storage_containers=dict(
            type="list",
            elements="dict",
            options=storage_container_spec,
            obj=multidomain_sdk.StorageContainerDetails
            if multidomain_sdk
            else None,
        ),
        capabilities=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            obj=multidomain_sdk.KVPair if multidomain_sdk else None,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        name=dict(type="str"),
        project_ext_id=dict(type="str"),
        placement_targets=dict(
            type="list",
            elements="dict",
            options=placement_target_spec,
            obj=multidomain_sdk.TargetDetails if multidomain_sdk else None,
        ),
        capabilities=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            obj=multidomain_sdk.KVPair if multidomain_sdk else None,
        ),
    )
    return module_args


def create_resource_group(module, result):
    api_instance = get_resource_groups_api_instance(module)
    sg = SpecGenerator(module)
    default_spec = multidomain_sdk.ResourceGroup()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create resource group spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_resource_group(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating resource group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(
            task_status.to_dict()
        )
        ext_id = get_entity_ext_id_from_task(
            task_status,
            rel=TASK_CONSTANTS.RelEntityType.RESOURCE_GROUP,
        )
        if ext_id:
            resp = get_resource_group(module, api_instance, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def update_resource_group(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    api_instance = get_resource_groups_api_instance(module)

    current_spec = get_resource_group(module, api_instance, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update resource group spec", **result
        )

    if check_resource_group_idempotency(
        current_spec.to_dict(), update_spec.to_dict()
    ):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(
            update_spec.to_dict()
        )
        return

    resp = None
    try:
        resp = api_instance.update_resource_group_by_id(
            extId=ext_id, body=update_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating resource group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_resource_group(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_resource_group(module, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    api_instance = get_resource_groups_api_instance(module)

    if module.check_mode:
        result["msg"] = (
            "Resource group with ext_id:{0} will be deleted.".format(ext_id)
        )
        return

    current_spec = get_resource_group(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for deleting resource group", **result
        )

    kwargs = {"if_match": etag}

    try:
        resp = api_instance.delete_resource_group_by_id(
            extId=ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting resource group",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_resource_group_idempotency(old_spec, update_spec):
    strip_internal_attributes(old_spec)
    strip_internal_attributes(update_spec)
    return old_spec == update_spec


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_multidomain_py_client"),
            exception=SDK_IMP_ERROR,
        )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "ext_id": None}
    state = module.params["state"]
    if state == "present":
        if module.params.get("ext_id"):
            update_resource_group(module, result)
        else:
            create_resource_group(module, result)
    else:
        delete_resource_group(module, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
