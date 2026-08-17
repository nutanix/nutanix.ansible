#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_container_v2
short_description: Create, Update, Delete Storage Containers in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, update, and delete Storage Containers in Nutanix Prism Central.
  - Uses the v4 Nutanix Storage namespace SDK (C(ntnx_storage_py_client)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create a Storage Container) -
      Required Roles: Prism Admin, Project Manager, Storage Admin, Super Admin
    - >-
      B(Update a Storage Container) -
      Required Roles: Backup Admin, Prism Admin, Project Manager, Storage Admin, Super Admin
    - >-
      B(Delete a Storage Container) -
      Required Roles: Prism Admin, Project Manager, Storage Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided, the module creates a new Storage Container.
      - If C(state) is set to C(present) and C(ext_id) is provided, the module updates the Storage Container.
      - If C(state) is set to C(absent) and C(ext_id) is provided, the module deletes the Storage Container.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Storage Container.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - Name of the Storage Container.
      - The name must be unique per cluster.
      - Required for create operation.
    type: str
    required: false
  cluster_ext_id:
    description:
      - External ID of the Prism Element cluster that hosts the Storage Container.
      - Required for create operation. The value is forwarded to the API through
        the C(X-Cluster-Id) header.
    type: str
    required: false
  owner_ext_id:
    description:
      - External ID of the user who owns the Storage Container.
    type: str
    required: false
  replication_factor:
    description:
      - Replication factor of the Storage Container.
      - Common values are C(2) (RF2) and C(3) (RF3).
    type: int
    required: false
  oplog_replication_factor:
    description:
      - Oplog replication factor of the Storage Container.
    type: int
    required: false
  advertised_capacity_bytes:
    description:
      - Maximum advertised capacity of the Storage Container in bytes.
    type: int
    required: false
  explicit_reserved_capacity_bytes:
    description:
      - Total reserved size (in bytes) of the Storage Container as set by an
        administrator. This value accounts for the container's replication factor.
    type: int
    required: false
  nfs_whitelist_address:
    description:
      - List of NFS addresses (IPv4/IPv6/FQDN) that should be whitelisted for the
        Storage Container.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 whitelist address.
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
              - Prefix length of the IPv4 subnet.
            type: int
            required: false
      ipv6:
        description:
          - IPv6 whitelist address.
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
              - Prefix length of the IPv6 subnet.
            type: int
            required: false
      fqdn:
        description:
          - Fully qualified domain name.
        type: dict
        required: false
        suboptions:
          value:
            description:
              - FQDN value.
            type: str
            required: true
  is_nfs_whitelist_inherited:
    description:
      - Indicates whether the NFS whitelist is inherited from the global cluster
        configuration.
    type: bool
    required: false
  random_io_preference:
    description:
      - Ordered list of random IO preference storage tiers (e.g. C(SSD-SATA)).
    type: list
    elements: str
    required: false
  seq_io_preference:
    description:
      - Ordered list of sequential IO preference storage tiers (e.g. C(SSD-SATA)).
    type: list
    elements: str
    required: false
  ilm_down_migrate_times_secs:
    description:
      - ILM down-migrate time (in seconds) per random-IO-preference tier. Each
        entry's C(name) identifies the tier and C(value) is the down-migration
        delay in seconds.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - Name of the random-IO-preference tier (e.g. C(SSD-SATA)).
        type: str
        required: true
      value:
        description:
          - Down-migration delay in seconds for the tier.
        type: int
        required: true
  erasure_code:
    description:
      - Erasure Code setting for the Storage Container.
    type: str
    required: false
    choices:
      - NONE
      - "OFF"
      - "ON"
  is_inline_ec_enabled:
    description:
      - Whether data written to the container should be inline-erasure-coded.
      - Only honored when C(erasure_code) is C(ON).
    type: bool
    required: false
  has_higher_ec_fault_domain_preference:
    description:
      - Whether to prefer a higher Erasure Code fault domain.
    type: bool
    required: false
  erasure_code_delay_secs:
    description:
      - Delay (in seconds) before performing Erasure Coding on new data.
    type: int
    required: false
  cache_deduplication:
    description:
      - Cache deduplication setting for the Storage Container.
    type: str
    required: false
    choices:
      - NONE
      - "OFF"
      - "ON"
  on_disk_dedup:
    description:
      - On-disk deduplication setting for the Storage Container.
    type: str
    required: false
    choices:
      - NONE
      - "OFF"
      - POST_PROCESS
  is_compression_enabled:
    description:
      - Whether compression is enabled for the Storage Container.
    type: bool
    required: false
  compression_delay_secs:
    description:
      - Compression delay in seconds. C(0) means inline compression.
    type: int
    required: false
  is_internal:
    description:
      - Indicates whether the container is internal (Nutanix managed).
    type: bool
    required: false
  is_software_encryption_enabled:
    description:
      - Indicates whether software encryption is enabled for the container.
    type: bool
    required: false
  affinity_host_ext_id:
    description:
      - Affinity host external ID for RF1 Storage Containers.
    type: str
    required: false
  ignore_small_files:
    description:
      - Whether to ignore small files during the delete operation.
      - Applies only to the delete operation.
    type: bool
    required: false
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
- name: Create a Storage Container with only required fields
  nutanix.ncp.ntnx_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "sc_ansible_min"
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
  register: result
  ignore_errors: true

- name: Create a Storage Container with all supported attributes
  nutanix.ncp.ntnx_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "sc_ansible_full"
    cluster_ext_id: "0006361b-6855-3644-7458-2268f8ffb2bd"
    owner_ext_id: "00000000-0000-0000-0000-000000000000"
    replication_factor: 2
    advertised_capacity_bytes: 1073741824000
    explicit_reserved_capacity_bytes: 0
    is_nfs_whitelist_inherited: false
    nfs_whitelist_address:
      - ipv4:
          value: "192.168.10.10"
    erasure_code: "OFF"
    is_inline_ec_enabled: false
    has_higher_ec_fault_domain_preference: false
    erasure_code_delay_secs: 0
    cache_deduplication: "OFF"
    on_disk_dedup: "OFF"
    is_compression_enabled: true
    compression_delay_secs: 0
    is_internal: false
    is_software_encryption_enabled: false
  register: result
  ignore_errors: true

- name: Update the Storage Container
  nutanix.ncp.ntnx_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6"
    name: "sc_ansible_full_updated"
    advertised_capacity_bytes: 2147483648000
    explicit_reserved_capacity_bytes: 10737418240
    nfs_whitelist_address:
      - ipv4:
          value: "192.168.10.11"
      - ipv4:
          value: "192.168.10.12"
    is_compression_enabled: true
    compression_delay_secs: 3600
  register: result
  ignore_errors: true

- name: Delete the Storage Container
  nutanix.ncp.ntnx_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6"
    ignore_small_files: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting a Storage Container.
    - If the operation is create or update and C(wait) is true, this contains
      the resulting Storage Container details.
    - If the operation is create or update and C(wait) is false, this contains
      the task reference details.
    - For delete operations, this contains the completed task details.
  returned: always
  type: dict
  sample:
    {
      "advertised_capacity_bytes": 1073741824000,
      "affinity_host_ext_id": null,
      "cache_deduplication": "OFF",
      "cluster_ext_id": "0006361b-6855-3644-7458-2268f8ffb2bd",
      "cluster_name": "auto-cluster-prod",
      "compression_delay_secs": 0,
      "container_ext_id": "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6",
      "erasure_code": "OFF",
      "erasure_code_delay_secs": null,
      "explicit_reserved_capacity_bytes": 0,
      "ext_id": "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6",
      "has_higher_ec_fault_domain_preference": false,
      "is_compression_enabled": true,
      "is_encrypted": null,
      "is_inline_ec_enabled": false,
      "is_internal": false,
      "is_marked_for_removal": false,
      "is_nfs_whitelist_inherited": true,
      "is_software_encryption_enabled": false,
      "links": null,
      "mapped_remote_containers": null,
      "max_capacity_bytes": 4291605771923,
      "name": "sc_ansible_full",
      "nfs_whitelist_address": null,
      "on_disk_dedup": "OFF",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "replication_factor": 2,
      "storage_pool_ext_id": "487c142e-6c41-4b10-9585-4feac6bd3c68",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the underlying async task.
  returned: always
  type: str
  sample: "ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1"

ext_id:
  description:
    - The external ID of the Storage Container.
  returned: always
  type: str
  sample: "8b12c1a3-2c8a-4a55-9f5e-3b3a04a4b1e6"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. idempotency).
  returned: always
  type: bool
  sample: false

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
  description: Status or error message set on specific code paths.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Api Exception raised while creating storage container"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_etag,
    get_storage_container_api_instance,
)
from ..module_utils.v4.storage.helpers import get_storage_container  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


# Server-populated fields we must strip from update bodies (they are read-only).
_READ_ONLY_UPDATE_FIELDS = (
    "container_ext_id",
    "storage_pool_ext_id",
    "cluster_name",
    "is_marked_for_removal",
    "max_capacity_bytes",
    "implicit_reserved_capacity_bytes",
    "mapped_remote_containers",
    "vstore_name_list",
    "is_encrypted",
    "ext_id",
    "links",
    "tenant_id",
)


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False),
    )

    fqdn_spec = dict(
        value=dict(type="str", required=True),
    )

    nfs_whitelist_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            required=False,
            obj=storage_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            required=False,
            obj=storage_sdk.IPv6Address,
        ),
        fqdn=dict(
            type="dict",
            options=fqdn_spec,
            required=False,
            obj=storage_sdk.FQDN,
        ),
    )

    kv_pair_spec = dict(
        name=dict(type="str", required=True),
        value=dict(type="int", required=True),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=False),
        owner_ext_id=dict(type="str", required=False),
        replication_factor=dict(type="int", required=False),
        oplog_replication_factor=dict(type="int", required=False),
        advertised_capacity_bytes=dict(type="int", required=False),
        explicit_reserved_capacity_bytes=dict(type="int", required=False),
        nfs_whitelist_address=dict(
            type="list",
            elements="dict",
            options=nfs_whitelist_address_spec,
            required=False,
            obj=storage_sdk.IPAddressOrFQDN,
        ),
        is_nfs_whitelist_inherited=dict(type="bool", required=False),
        random_io_preference=dict(type="list", elements="str", required=False),
        seq_io_preference=dict(type="list", elements="str", required=False),
        ilm_down_migrate_times_secs=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            required=False,
            obj=storage_sdk.KVPair,
        ),
        erasure_code=dict(
            type="str",
            choices=["NONE", "OFF", "ON"],
            required=False,
            obj=storage_sdk.ErasureCodeStatus,
        ),
        is_inline_ec_enabled=dict(type="bool", required=False),
        has_higher_ec_fault_domain_preference=dict(type="bool", required=False),
        erasure_code_delay_secs=dict(type="int", required=False),
        cache_deduplication=dict(
            type="str",
            choices=["NONE", "OFF", "ON"],
            required=False,
            obj=storage_sdk.CacheDeduplication,
        ),
        on_disk_dedup=dict(
            type="str",
            choices=["NONE", "OFF", "POST_PROCESS"],
            required=False,
            obj=storage_sdk.OnDiskDedup,
        ),
        is_compression_enabled=dict(type="bool", required=False),
        compression_delay_secs=dict(type="int", required=False),
        is_internal=dict(type="bool", required=False),
        is_software_encryption_enabled=dict(type="bool", required=False),
        affinity_host_ext_id=dict(type="str", required=False),
        ignore_small_files=dict(type="bool", required=False),
    )
    return module_args


def create_storage_container(module, result, api_instance):
    validate_required_params(module, ["name", "cluster_ext_id"])

    sg = SpecGenerator(module)
    default_spec = storage_sdk.StorageContainer()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create storage container spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    cluster_ext_id = module.params.get("cluster_ext_id")
    resp = None
    try:
        resp = api_instance.add_storage_container_for_cluster(
            body=spec, X_Cluster_Id=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating storage container",
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
            new_sc = get_storage_container(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(new_sc.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for Storage Container"
                ),
                msg="Failed to get entity ext_id from task for Storage Container",
            )
    result["changed"] = True


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    # Drop attributes that either differ across API responses or are never
    # accepted on the update body.
    volatile_keys = (
        "container_ext_id",
        "storage_pool_ext_id",
        "cluster_name",
        "is_marked_for_removal",
        "max_capacity_bytes",
        "implicit_reserved_capacity_bytes",
        "mapped_remote_containers",
        "vstore_name_list",
        "is_encrypted",
        "ext_id",
        "links",
        "tenant_id",
    )
    for k in volatile_keys:
        old.pop(k, None)
        new.pop(k, None)
    return old == new


def update_storage_container(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_storage_container(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating storage container", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update storage container spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(update_spec, _READ_ONLY_UPDATE_FIELDS)

    resp = None
    try:
        resp = api_instance.update_storage_container(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating storage container",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated = get_storage_container(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(updated.to_dict())
    result["changed"] = True


def delete_storage_container(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Storage container with ext_id:{0} will be deleted.".format(
            ext_id
        )
        return

    ignore_small_files = module.params.get("ignore_small_files")
    kwargs = {}
    if ignore_small_files is not None:
        kwargs["ignoreSmallFiles"] = ignore_small_files

    resp = None
    try:
        resp = api_instance.delete_storage_container_by_ext_id(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting storage container",
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
            msg=missing_required_lib("ntnx_storage_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
    }
    api_instance = get_storage_container_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_storage_container(module, result, api_instance)
        else:
            create_storage_container(module, result, api_instance)
    else:
        delete_storage_container(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
