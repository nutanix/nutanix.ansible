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
    - This module uses PC v4 APIs based SDKs
options:
    state:
        description:
            - State of the Nutanix object store, whether to create, update or delete.
            - If C(state) is present, it will create or update the object store.
            - If C(state) is set to C(present) and ext_id is not provided then it will create a new object store.
            - If C(state) is set to C(present) and ext_id is provided then it will update the object store.
            - If C(state) is absent, and ext_id is provided then it will delete the object store.
            - Update object store is only supported for object stores in C(OBJECT_STORE_DEPLOYMENT_FAILED) state.
            - If the object store is in C(OBJECT_STORE_DEPLOYMENT_FAILED) state, it can be updated to redeploy the object store.
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
            - The DNS domain/subdomain the Object store belongs to.
            - All the Object stores under one Prism Central must have the same domain name.
            - The domain name must consist of at least 2 parts separated by a '.'.
            - Each part can contain upper and lower case letters, digits, hyphens, or underscores.
            - Each part can be up to 63 characters long.
            - The domain must begin and end with an alphanumeric character. For example - 'objects-0.pc_nutanix.com'.
        type: str
        required: false
    region:
        description:
            - The region in which the Object store is deployed.
        type: str
        required: false
    num_worker_nodes:
        description:
            - The number of worker nodes (VMs) to be created for the Object store.
            - Each worker node requires 10 vCPUs and 32 GiB of memory.
        type: int
        required: false
    cluster_ext_id:
        description:
            - External ID of the cluster where the object store will be deployed.
        type: str
        required: false
    storage_network_reference:
        description:
            - Reference to the Storage Network of the Object store.
            - This is the subnet UUID for an AHV cluster or the IPAM name for an ESXi cluster.
            - Used for internal service calls.
        type: str
        required: false
    storage_network_vip:
        description:
            - A unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
        type: dict
        required: false
        suboptions:
            ipv4:
                description:
                    - A unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv4 address value of the host.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - A unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv6 address value of the host.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv6 address.
                        type: int
                        default: 128
    storage_network_dns_ip:
        description:
            - A unique address that identifies a device on the internet or a local network in IPv4 or IPv6 format.
        type: dict
        required: false
        suboptions:
            ipv4:
                description:
                    - A unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv4 address value of the host.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - A unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv6 address value of the host.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv6 address.
                        type: int
                        default: 128
    public_network_reference:
        description:
            - Public network reference of the Object store.
            - This is the subnet UUID for an AHV cluster or the IPAM name for an ESXi cluster.
            - Used to allow access from external clients.
        type: str
        required: false
    public_network_ips:
        description:
            - A list of static IP addresses used as public IPs to access the Object store.
        type: list
        elements: dict
        required: false
        suboptions:
            ipv4:
                description:
                    - A unique address that identifies a device on the internet or a local network in IPv4 format.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv4 address value of the host.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv4 address.
                        type: int
                        default: 32
            ipv6:
                description:
                    - A unique address that identifies a device on the internet or a local network in IPv6 format.
                type: dict
                required: false
                suboptions:
                    value:
                        description:
                            - IPv6 address value of the host.
                        type: str
                        required: true
                    prefix_length:
                        description:
                            - Prefix length of the IPv6 address.
                        type: int
                        default: 128
    total_capacity_gi_b:
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
- name: Create Object Store
  nutanix.ncp.ntnx_object_stores_v2:
    name: "ansible-object"
    cluster_ext_id: "000633ea-e256-b6a1-185b-ac1f6b6f97e2"
    description: "object store test"
    domain: "domain.example.nutanix.com"
    num_worker_nodes: "1"
    storage_network_reference: "313c37c1-6f1d-4520-9245-528e3162af5c"
    storage_network_vip:
      ipv4:
        value: "10.10.10.124"
    storage_network_dns_ip:
      ipv4:
        value: "10.10.10.125"
    public_network_reference: "313c37c1-6f1d-4520-9245-528e3162af5c"
    public_network_ips:
      - ipv4:
          value: "10.10.10.126"
    total_capacity_gi_b: "21474836480"
  register: result
  ignore_errors: true

- name: Update Object Store if the deployment failed
  nutanix.ncp.ntnx_object_stores_v2:
    name: "ansible-object"
    ext_id: "6dd6df38-5d5c-40a8-561f-10862416c1c0"
    cluster_ext_id: "000633ea-e256-b6a1-185b-ac1f6b6f97e2"
    description: "object store test"
    domain: "domain.example.nutanix.com"
    num_worker_nodes: "1"
    storage_network_reference: "313c37c1-6f1d-4520-9245-528e3162af5c"
    storage_network_vip:
      ipv4:
        value: "10.10.10.124"
    storage_network_dns_ip:
      ipv4:
        value: "10.10.10.125"
    public_network_reference: "313c37c1-6f1d-4520-9245-528e3162af5c"
    public_network_ips:
      - ipv4:
          value: "10.10.10.126"
    total_capacity_gi_b: "21474836480"
  register: result
  ignore_errors: true

- name: Delete object store
  nutanix.ncp.ntnx_object_stores_v2:
    ext_id: "6dd6df38-5d5c-40a8-561f-10862416c1c0"
    state: absent
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for creating, updating or deleting object store
        - Object store details if created or updated
        - Task details if deleted
    type: dict
    returned: always
    sample:
        {
            "certificate_ext_ids": [
                "1f2e1e77-890b-4e0d-4ab4-5c0904a16320"
            ],
            "cluster_ext_id": "000633ea-e256-b6a1-185b-ac1f6b6f97e2",
            "creation_time": "2025-05-04T11:30:10+00:00",
            "deployment_version": "5.1.1.1",
            "description": "object store test",
            "domain": "example.nutanix.com",
            "ext_id": "62f80159-be3b-49aa-4701-9e1e32b9c828",
            "last_update_time": "2025-05-04T11:30:10+00:00",
            "links": null,
            "metadata": null,
            "name": "ansible-object",
            "num_worker_nodes": 1,
            "public_network_ips": [
                {
                    "ipv4": {
                        "prefix_length": 32,
                        "value": "10.10.10.123"
                    },
                    "ipv6": null
                }
            ],
            "public_network_reference": "313c37c1-6f1d-4520-9245-528e3162af5c",
            "region": null,
            "state": "OBJECT_STORE_AVAILABLE",
            "storage_network_dns_ip": {
                "ipv4": {
                    "prefix_length": 32,
                    "value": "10.10.10.125"
                },
                "ipv6": null
            },
            "storage_network_reference": "313c37c1-6f1d-4520-9245-528e3162af5c",
            "storage_network_vip": {
                "ipv4": {
                    "prefix_length": 32,
                    "value": "10.10.10.124"
                },
                "ipv6": null
            },
            "tenant_id": null,
            "total_capacity_gi_b": 21474836480
        }

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
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.objects.api_client import (  # noqa: E402
    get_etag,
    get_objects_api_instance,
)
from ..module_utils.v4.objects.helpers import get_object_store  # noqa: E402
from ..module_utils.v4.objects.spec.objects import (  # noqa: E402
    ObjectsSpecs as objects_specs,
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
    del module.params["state"]
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
        resp = object_stores_api.create_objectstore(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception raised while creating object store",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.OBJECTS
        )
        object_stores_api = get_objects_api_instance(module)
        if ext_id:
            resp = get_object_store(module, object_stores_api, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def update_object_store(module, object_stores_api, result):
    """
    This method will update object store.
    Args:
        module (object): Ansible module object
        object_stores_api (object): ObjectStoresApi instance
        result (dict): Result object
    """
    ext_id = module.params.get("ext_id")
    del module.params["state"]

    current_spec = get_object_store(module, object_stores_api, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for Updating Object Store", **result
        )
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating object store update Spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return
    kwargs = {"if_match": etag_value}

    resp = None
    try:
        resp = object_stores_api.update_objectstore_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception raised while updating object store",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        object_stores_api = get_objects_api_instance(module)
        resp = get_object_store(module, object_stores_api, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
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

    if module.check_mode:
        result["msg"] = "Object store with ext_id:{0} will be deleted.".format(ext_id)
        return

    current_spec = get_object_store(module, object_stores_api, ext_id)

    etag_value = get_etag(data=current_spec)
    if not etag_value:
        return module.fail_json(
            "Unable to fetch etag for deleting Object Store", **result
        )
    kwargs = {"if_match": etag_value}

    resp = None
    try:
        resp = object_stores_api.delete_objectstore_by_id(extId=ext_id, **kwargs)
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
            ("state", "present", ["name"]),
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
