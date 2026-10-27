#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_container_esxi_v2
short_description: Create, Update, Delete Storage Containers in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Storage Containers in Nutanix Prism Central.
  - A Storage Container is a logical subset of available storage within a Nutanix Storage Pool
    where storage-efficiency features (compression, deduplication, erasure coding) and policies
    (Replication Factor, encryption) are applied.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Storage Container) -
      Required Roles: Prism Admin, Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Update a Storage Container) -
      Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
    - >-
      B(Delete a Storage Container) -
      Required Roles: Prism Admin, Project Manager, Storage Admin, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will
        be create Storage Container.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be
        update Storage Container.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be
        delete Storage Container.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external identifier of the Storage Container.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the Storage Container. Must be unique on every cluster. Maximum length is 75
        characters.
      - Required for create operation. On update, if omitted, the existing name from the
        current Storage Container is retained in the request body.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external identifier of the Prism Element cluster on which the Storage Container is
        (or will be) hosted.
      - Required for create operation. Passed as the C(X-Cluster-Id) header to route the
        request to the correct PE. Not a writable body field (C(clusterExtId) is read-only
        on the Storage Container model).
    type: str
    required: false
  owner_ext_id:
    description:
      - The external identifier of the owner of the Storage Container.
    type: str
    required: false
  logical_explicit_reserved_capacity_bytes:
    description:
      - Total reserved size (in bytes) of the Storage Container (set by Admin). This also
        includes the replication factor of the Storage Container. The actual reserved capacity
        is the maximum of explicit and implicit reserved capacity.
    type: int
    required: false
  logical_advertised_capacity_bytes:
    description:
      - Maximum capacity of the Storage Container as defined by the user, in bytes.
    type: int
    required: false
  replication_factor:
    description:
      - Replication factor of the Storage Container. Typically C(2) or C(3).
      - RF-1 containers generally require C(affinity_host_ext_id).
    type: int
    required: false
  nfs_whitelist_address:
    description:
      - List of NFS addresses that need to be whitelisted for this Storage Container.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address.
        type: dict
        required: false
        suboptions:
          value:
            description: The IPv4 address value.
            type: str
            required: true
          prefix_length:
            description: The prefix length of the network to which this address belongs.
            type: int
            required: false
      ipv6:
        description:
          - IPv6 address.
        type: dict
        required: false
        suboptions:
          value:
            description: The IPv6 address value.
            type: str
            required: true
          prefix_length:
            description: The prefix length of the network to which this address belongs.
            type: int
            required: false
      fqdn:
        description:
          - Fully qualified domain name.
        type: dict
        required: false
        suboptions:
          value:
            description: The fully qualified domain name value.
            type: str
            required: true
  erasure_code:
    description:
      - Erasure Coding status for the Storage Container.
    type: str
    required: false
    choices:
      - NONE
      - "OFF"
      - "ON"
  is_inline_ec_enabled:
    description:
      - Indicates whether data written to this Storage Container should be inline
        erasure-coded. Only considered when Erasure Coding is enabled.
    type: bool
    required: false
  has_higher_ec_fault_domain_preference:
    description:
      - Indicates whether to prefer a higher Erasure Code fault domain.
    type: bool
    required: false
  erasure_code_delay_secs:
    description:
      - Delay in seconds before performing Erasure Coding for the Storage Container.
    type: int
    required: false
  cache_deduplication:
    description:
      - Cache deduplication status for the Storage Container.
    type: str
    required: false
    choices:
      - NONE
      - "OFF"
      - "ON"
  on_disk_dedup:
    description:
      - On-disk deduplication status for the Storage Container.
    type: str
    required: false
    choices:
      - NONE
      - "OFF"
      - POST_PROCESS
  is_compression_enabled:
    description:
      - Indicates whether compression is enabled for the Storage Container.
    type: bool
    required: false
  compression_delay_secs:
    description:
      - The compression delay in seconds.
    type: int
    required: false
  is_internal:
    description:
      - Indicates whether the Storage Container is internal and is managed by Nutanix.
      - Internal containers (e.g. C(NutanixManagementShare)) are not expected to be created by
        end users.
    type: bool
    required: false
  is_software_encryption_enabled:
    description:
      - Indicates whether the Storage Container instance has software encryption enabled.
    type: bool
    required: false
  affinity_host_ext_id:
    description:
      - Affinity host external identifier for an RF-1 Storage Container.
    type: str
    required: false
  is_shared:
    description:
      - Indicates whether the Storage Container is shared. When shared, all Prism Element
        clusters registered under the same Prism Central can access and utilize its storage.
      - Once set during create, this field is immutable except for SelfServiceContainer, where
        only a change from C(false) to C(true) is allowed.
    type: bool
    required: false
  ignore_small_files:
    description:
      - When deleting a Storage Container, if this is set to C(true) small files that may still
        be in the container will be ignored and the delete will proceed.
      - Applies only to the delete operation.
      - Corresponds to the C(ignoreSmallFiles) query parameter on the delete API
        (API default is C(true) when omitted).
    type: bool
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - George Ghawali (@george-ghawali)
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create Storage Container with minimal spec
  nutanix.ncp.ntnx_storage_container_esxi_v2:
    state: present
    name: "storage_container_ansible"
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: Create Storage Container with full spec
  nutanix.ncp.ntnx_storage_container_esxi_v2:
    state: present
    name: "storage_container_ansible_full"
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    owner_ext_id: "00000000-0000-0000-0000-000000000000"
    logical_explicit_reserved_capacity_bytes: 0
    logical_advertised_capacity_bytes: 107374182400
    replication_factor: 2
    nfs_whitelist_address:
      - ipv4:
          value: "192.168.1.1"
    erasure_code: "OFF"
    is_inline_ec_enabled: false
    has_higher_ec_fault_domain_preference: true
    erasure_code_delay_secs: 0
    cache_deduplication: "OFF"
    on_disk_dedup: "OFF"
    is_compression_enabled: true
    compression_delay_secs: 0
    is_internal: false
    is_software_encryption_enabled: false
    is_shared: true
  register: result
  ignore_errors: true

- name: Update Storage Container
  nutanix.ncp.ntnx_storage_container_esxi_v2:
    state: present
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    name: "storage_container_ansible_updated"
    logical_explicit_reserved_capacity_bytes: 25
    logical_advertised_capacity_bytes: 2147483648000
    nfs_whitelist_address:
      - ipv4:
          value: "192.168.13.2"
  register: result
  ignore_errors: true

- name: Delete Storage Container
  nutanix.ncp.ntnx_storage_container_esxi_v2:
    state: absent
    ext_id: "2e40ff57-20aa-4d2b-b179-298db969c20d"
    ignore_small_files: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a Storage Container.
    - If the operation is create or update and C(wait) is true, it will return the Storage
      Container details.
    - If the operation is create or update and C(wait) is false, it will return the task
      details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "affinity_host_ext_id": null,
      "cache_deduplication": "OFF",
      "cluster_ext_id": "0006197f-3d06-ce49-1fc3-ac1f6b6029c1",
      "cluster_name": "auto-cluster-prod-f30accd2eec1",
      "compression_delay_secs": 0,
      "container_ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
      "erasure_code": "OFF",
      "erasure_code_delay_secs": null,
      "ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
      "has_higher_ec_fault_domain_preference": false,
      "is_compression_enabled": false,
      "is_encrypted": null,
      "is_inline_ec_enabled": false,
      "is_internal": false,
      "is_marked_for_removal": false,
      "is_nfs_whitelist_inherited": true,
      "is_shared": true,
      "is_software_encryption_enabled": false,
      "links": null,
      "logical_advertised_capacity_bytes": null,
      "logical_explicit_reserved_capacity_bytes": 0,
      "logical_implicit_reserved_capacity_bytes": 0,
      "max_capacity_bytes": 4291605771923,
      "name": "storage_container_ansible",
      "nfs_whitelist_address": null,
      "on_disk_dedup": "OFF",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "replication_factor": 2,
      "storage_pool_ext_id": "487c142e-6c41-4b10-9585-4feac6bd3c68",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the Storage Container.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped, for example during idempotency checks.
  returned: when applicable
  type: bool
  sample: true

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating Storage Container"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_storage_containers_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_storage_container  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


# Fields that are populated by the server and MUST NOT be sent back on update
# to avoid schema/validation errors on the API side.
_READ_ONLY_FIELDS = (
    "container_ext_id",
    "storage_pool_ext_id",
    "max_capacity_bytes",
    "logical_implicit_reserved_capacity_bytes",
    "cluster_ext_id",
    "cluster_name",
    "is_marked_for_removal",
    "external_storage_ext_id",
    "is_encrypted",
    "is_nfs_whitelist_inherited",
    "links",
    "tenant_id",
    "ext_id",
)


def get_module_spec():

    ipv4_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    ipv6_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )
    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )
    nfs_whitelist_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_spec,
            required=False,
            obj=clustermgmt_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
            required=False,
            obj=clustermgmt_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=clustermgmt_sdk.FQDN,
        ),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=False),
        owner_ext_id=dict(type="str", required=False),
        logical_explicit_reserved_capacity_bytes=dict(type="int", required=False),
        logical_advertised_capacity_bytes=dict(type="int", required=False),
        replication_factor=dict(type="int", required=False),
        nfs_whitelist_address=dict(
            type="list",
            elements="dict",
            options=nfs_whitelist_address_spec,
            required=False,
            obj=clustermgmt_sdk.IPAddressOrFQDN,
        ),
        erasure_code=dict(
            type="str",
            choices=["NONE", "OFF", "ON"],
            required=False,
            obj=clustermgmt_sdk.ErasureCodeStatus,
        ),
        is_inline_ec_enabled=dict(type="bool", required=False),
        has_higher_ec_fault_domain_preference=dict(type="bool", required=False),
        erasure_code_delay_secs=dict(type="int", required=False),
        cache_deduplication=dict(
            type="str",
            choices=["NONE", "OFF", "ON"],
            required=False,
            obj=clustermgmt_sdk.CacheDeduplication,
        ),
        on_disk_dedup=dict(
            type="str",
            choices=["NONE", "OFF", "POST_PROCESS"],
            required=False,
            obj=clustermgmt_sdk.OnDiskDedup,
        ),
        is_compression_enabled=dict(type="bool", required=False),
        compression_delay_secs=dict(type="int", required=False),
        is_internal=dict(type="bool", required=False),
        is_software_encryption_enabled=dict(type="bool", required=False),
        affinity_host_ext_id=dict(type="str", required=False),
        is_shared=dict(type="bool", required=False),
        ignore_small_files=dict(type="bool", required=False),
    )
    return module_args


def check_idempotency(old_spec, update_spec):
    """Return True if the update spec matches the current spec (nothing to change)."""
    return old_spec == update_spec


def create_storage_container(module, api_instance, result):
    validate_required_params(module, ["name", "cluster_ext_id"])

    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.StorageContainer()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create Storage Container spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    cluster_ext_id = module.params.get("cluster_ext_id")

    resp = None
    try:
        resp = api_instance.create_storage_container(
            body=spec, X_Cluster_Id=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating Storage Container",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_status, rel=TASK_CONSTANTS.RelEntityType.STORAGE_CONTAINER
        )
        if ext_id:
            result["ext_id"] = ext_id
            resp = get_storage_container(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Storage Container"
                ),
                msg="Failed to get entity ext_id from task for Storage Container",
            )

    result["changed"] = True


def update_storage_container(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_storage_container(module, api_instance, ext_id)

    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating Storage Container", **result
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update Storage Container spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    # Clear GET-populated fields the update API rejects.
    strip_read_only_fields(update_spec, fields=_READ_ONLY_FIELDS)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_storage_container_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Storage Container",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_storage_container(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_storage_container(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Storage Container with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    ignore_small_files = module.params.get("ignore_small_files")

    resp = None
    try:
        resp = api_instance.delete_storage_container_by_id(
            extId=ext_id, ignoreSmallFiles=ignore_small_files
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting Storage Container",
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
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_clustermgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
    }

    api_instance = get_storage_containers_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_storage_container(module, api_instance, result)
        else:
            create_storage_container(module, api_instance, result)
    else:
        delete_storage_container(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
