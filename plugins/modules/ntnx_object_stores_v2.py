#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: ntnx_object_stores_v2
short_description: Create, Update and Delete a Nutanix object store
version_added: 2.2.0
description:
    - Create, Update and Delete a Nutanix object store.
options:
    state:
        description:
            - State of the Nutanix object store, whether to create, update or delete.
            - If C(state) is present, it will create or update the object store.
            - If C(state) is set to C(present) and ext_id is not provided then it will create a new object store.
            - If C(state) is set to C(present) and ext_id is provided then it will update the object store.
            - If C(state) is absent, and ext_id is provided then it will delete the object store.
        choices: ['present', 'absent']
        type: str
        default: present
    ext_id:
        description:
            - External ID of the object store.
            - Used to update or delete the object store.
        type: str
        required: false
    name:
        description:
            - Name of the object store.
        type: str
        required: true
    metadata:
        description:
            - Metadata of the object store.
        type: dict
        required: false
        suboptions:
            owner_reference_id:
                description:
                    - Owner reference ID of the object store.
                type: str
                required: false
            owner_user_name:
                description:
                    - Owner user name of the object store.
                type: str
                required: false
            project_reference_id:
                description:
                    - Project reference ID of the object store.
                type: str
                required: false
            project_name:
                description:
                    - Project name of the object store.
                type: str
                required: false
            category_ids:
                description:
                    - Category IDs of the object store.
                type: list
                elements: str
                required: false
    description:
        description:
            - Description of the object store.
        type: str
        required: false
    deployment_version:
        description:
            - Deployment version of the object store.
        type: str
        required: false
    domain:
        description:
            - Domain of the object store.
        type: str
        required: false
    region:
        description:
            - Region of the object store.
        type: str
        required: false
    num_worker_nodes:
        description:
            - Number of worker nodes in the object store.
        type: int
        required: false
    cluster_ext_id:
        description:
            - External ID of the cluster where the object store will be deployed.
        type: str
        required: false
    storage_network_reference:
        description:
            - Reference ID of the storage network for the object store.
        type: str
        required: false
    storage_network_vip:
        description:
            - Storage network VIP of the object store.
        type: dict
        required: false
        suboptions:
            ipv4:
                description:
                    - IPv4 address of the storage network VIP.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv4 address value.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - IPv6 address of the storage network VIP.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv6 address value.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv6 address.
                        type: int
                        default: 128
    storage_network_dns_ip:
        description:
            - Storage network DNS IP of the object store.
        type: dict
        required: false
        suboptions:
            ipv4:
                description:
                    - IPv4 address of the storage network DNS IP.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv4 address value.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - IPv6 address of the storage network DNS IP.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv6 address value.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv6 address.
                        type: int
                        default: 128
    public_network_reference:
        description:
            - Reference ID of the public network for the object store.
        type: str
        required: false
    public_network_ips:
        description:
            - Public network IPs of the object store.
        type: list
        elements: dict
        required: false
        suboptions:
            ipv4:
                description:
                    - IPv4 address of the public network IP.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv4 address value.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - IPv6 address of the public network IP.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv6 address value.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv6 address.
                        type: int
                        default: 128
    total_capacity_gib:
        description:
            - Total capacity in GiB of the object store.
        type: int
        required: false
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        required: false

extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_operations_v2
author:
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
"""

RETURN = r"""
response:
    description: Task status for the object store operation
    type: dict
    returned: always
    sample:

task_ext_id:
    description: Task ID for the object store operation.
    type: str
    returned: always
    sample: "ZXJnb24=:5f63a855-6b6e-4aca-4efb-159a35ce0e52"

ext_id:
    description: External ID of the object store
    type: str
    returned: always
    sample: "00062c47-ac15-ee40-185b-ac1f6b6f97e2"

changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true

error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: When an error occurs
    type: str

failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.objects.helpers import get_object_store  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_objects_api_instance,
    get_etag,
)
from ..module_utils.v4.objects.spec.objects import (
    ObjectsSpecs as objects_specs,
)  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_objects_py_client as objects_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as objects_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
    )
    module_args.update(objects_specs.get_object_store_spec())
    return module_args


def create_object_store(module, object_stores_api, result):
    """
    This method will create object store.
    Args:
        module (object): Ansible module object
        object_stores_api (object): ObjectStoresApi instance
        result (dict): Result object
    """
    sg = SpecGenerator(module)
    default_spec = objects_sdk.ObjectStore()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating object store create Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    try:
        resp = object_stores_api.create_object_store(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to create object store",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def check_idempotency(current_spec, update_spec):
    if current_spec != update_spec:
        return False
    return True


def update_object_store(module, object_stores_api, result):
    """
    This method will update object store.
    Args:
        module (object): Ansible module object
        object_stores_api (object): ObjectStoresApi instance
        result (dict): Result object
    """
    ext_id = module.params.get("ext_id")
    sg = SpecGenerator(module)
    default_spec = objects_sdk.ObjectStore()
    spec, err = sg.generate_spec(obj=default_spec)

    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update object store spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    current_spec = get_object_store(module, object_stores_api, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for Updating Object Store", **result
        )

    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating object store update Spec", **result)

    skip_idempotency = False
    if module.params.get("location", {}).get("cluster_location") or module.params.get(
        "location", {}
    ).get("object_store_location", {}).get("provider_config", {}).get("credentials"):
        skip_idempotency = True

    if not skip_idempotency:
        if check_idempotency(current_spec, update_spec):
            result["skipped"] = True
            module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    resp = None
    try:
        resp = object_stores_api.update_object_store_by_id(
            extId=ext_id, body=update_spec, ifMatch=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Failed to update object store",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_object_store(module, object_stores_api, result):
    """
    This method will delete object store.
    Args:
        module (object): Ansible module object
        object_stores_api (object): ObjectStoresApi instance
        result (dict): Result object
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_object_store(module, object_stores_api, ext_id)

    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for deleting Object Store", **result
        )

    resp = None
    try:
        resp = object_stores_api.delete_object_store_by_id(
            extId=ext_id, ifMatch=etag_value
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting object store",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ["ext_id"]),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_objects_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    state = module.params.get("state")
    object_stores_api = get_objects_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_object_store(module, object_stores_api, result)
        else:
            create_object_store(module, object_stores_api, result)
    else:
        delete_object_store(module, object_stores_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
