#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_all_storage_container_v2
short_description: Create, Update, Delete storage containers in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to create, update, and delete storage containers in Nutanix Prism Central via the storage namespace v4 APIs.
  - This module uses PC v4 APIs based SDKs (ntnx_storage_py_client).
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
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will be create storage container.
      - If C(state) is set to C(present) and C(ext_id) is provided then the operation will be update storage container.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the operation will be delete storage container.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the storage container.
      - Required for update and delete operations.
    type: str
    required: false
  name:
    description:
      - The name of the storage container.
      - Required for create operation.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the cluster on which the storage container is hosted.
      - Required for create operation.
    type: str
    required: false
  owner_ext_id:
    description:
      - The external ID of the owner of the storage container.
    type: str
    required: false
  storage_pool_ext_id:
    description:
      - The external ID of the storage pool of the storage container.
    type: str
    required: false
  max_capacity_bytes:
    description:
      - The maximum capacity of the storage container in bytes (read-only for create).
    type: int
    required: false
  explicit_reserved_capacity_bytes:
    description:
      - The explicit reserved capacity of the storage container in bytes.
    type: int
    required: false
  advertised_capacity_bytes:
    description:
      - The advertised capacity of the storage container in bytes.
    type: int
    required: false
  replication_factor:
    description:
      - The replication factor of the storage container.
    type: int
    required: false
  oplog_replication_factor:
    description:
      - The replication factor of the OpLog for the storage container.
    type: int
    required: false
  nfs_whitelist_address:
    description:
      - The NFS whitelist addresses of the storage container.
    type: list
    elements: dict
    required: false
    suboptions:
      ipv4:
        description:
          - The IPv4 address specification.
        required: false
        type: dict
        suboptions:
          value:
            description: The value of the IPv4 address.
            type: str
            required: true
          prefix_length:
            description: The prefix length of the IPv4 address.
            type: int
            required: false
      ipv6:
        description:
          - The IPv6 address specification.
        required: false
        type: dict
        suboptions:
          value:
            description: The value of the IPv6 address.
            type: str
            required: true
          prefix_length:
            description: The prefix length of the IPv6 address.
            type: int
            required: false
      fqdn:
        description:
          - The fully qualified domain name specification.
        required: false
        type: dict
        suboptions:
          value:
            description: The FQDN value.
            type: str
            required: true
  is_nfs_whitelist_inherited:
    description:
      - Whether the NFS whitelist is inherited from the global settings.
    type: bool
    required: false
  random_io_preference:
    description:
      - The random IO tier preference order for the storage container.
    type: list
    elements: str
    required: false
  seq_io_preference:
    description:
      - The sequential IO tier preference order for the storage container.
    type: list
    elements: str
    required: false
  ilm_down_migrate_times_secs:
    description:
      - The ILM down-migrate times in seconds for each tier for the storage container.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description: Tier name key.
        type: str
        required: true
      value:
        description: Down-migrate time in seconds for the tier.
        type: str
        required: false
  erasure_code:
    description:
      - The erasure code setting for the storage container.
    type: str
    choices:
      - NONE
      - "OFF"
      - "ON"
    required: false
  is_inline_ec_enabled:
    description:
      - Whether inline erasure coding is enabled for the storage container.
    type: bool
    required: false
  has_higher_ec_fault_domain_preference:
    description:
      - Whether the storage container prefers a higher fault domain for erasure coding.
    type: bool
    required: false
  erasure_code_delay_secs:
    description:
      - The delay in seconds before erasure coding is applied.
    type: int
    required: false
  cache_deduplication:
    description:
      - The cache deduplication setting for the storage container.
    type: str
    choices:
      - NONE
      - "OFF"
      - "ON"
    required: false
  on_disk_dedup:
    description:
      - The on-disk deduplication setting for the storage container.
    type: str
    choices:
      - NONE
      - "OFF"
      - POST_PROCESS
    required: false
  is_compression_enabled:
    description:
      - Whether compression is enabled for the storage container.
    type: bool
    required: false
  compression_delay_secs:
    description:
      - The delay in seconds before compression is applied.
    type: int
    required: false
  is_internal:
    description:
      - Whether the storage container is internal.
    type: bool
    required: false
  is_software_encryption_enabled:
    description:
      - Whether software encryption is enabled for the storage container.
    type: bool
    required: false
  affinity_host_ext_id:
    description:
      - The external ID of the affinity host for the storage container.
    type: str
    required: false
  ignore_small_files:
    description:
      - When deleting, whether to ignore small files that may prevent deletion.
    type: bool
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Create storage container with all attributes
  nutanix.ncp.ntnx_all_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name: "ansible_all_sc_full"
    cluster_ext_id: "0006555e-4e63-4a5e-185b-ac1f6b6f97e2"
    advertised_capacity_bytes: 1073741824000
    explicit_reserved_capacity_bytes: 0
    replication_factor: 2
    is_nfs_whitelist_inherited: true
    erasure_code: "OFF"
    is_inline_ec_enabled: false
    has_higher_ec_fault_domain_preference: false
    cache_deduplication: "OFF"
    on_disk_dedup: "OFF"
    is_compression_enabled: true
    compression_delay_secs: 3600
    is_internal: false
    is_software_encryption_enabled: false
  register: create_result

- name: Update storage container
  nutanix.ncp.ntnx_all_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
    name: "ansible_all_sc_full_updated"
    advertised_capacity_bytes: 2147483648000
    is_compression_enabled: false
  register: update_result

- name: Delete storage container
  nutanix.ncp.ntnx_all_storage_container_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
  register: delete_result
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting storage container.
    - If the operation is create or update and C(wait) is true, it will return the storage container details.
    - If the operation is create or update and C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "advertised_capacity_bytes": 1073741824000,
      "affinity_host_ext_id": null,
      "cache_deduplication": "OFF",
      "cluster_ext_id": "0006555e-4e63-4a5e-185b-ac1f6b6f97e2",
      "cluster_name": "auto_cluster_prod_36acf9b012ca",
      "compression_delay_secs": 3600,
      "container_ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
      "erasure_code": "OFF",
      "ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
      "has_higher_ec_fault_domain_preference": false,
      "is_compression_enabled": true,
      "is_inline_ec_enabled": false,
      "is_internal": false,
      "is_marked_for_removal": false,
      "is_nfs_whitelist_inherited": true,
      "is_software_encryption_enabled": false,
      "max_capacity_bytes": 4404802450302,
      "name": "ansible_all_sc_full",
      "on_disk_dedup": "OFF",
      "owner_ext_id": "00000000-0000-0000-0000-000000000000",
      "replication_factor": 2,
      "storage_pool_ext_id": "df233a93-0480-4f15-a500-1269696fc4b2"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the storage container.
  returned: always
  type: str
  sample: "57516342-7d8e-470f-91b8-ae310737ff8c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. idempotency).
  returned: When applicable
  type: bool
  sample: false

error:
  description: This indicates the error details if any error occurred.
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


READ_ONLY_FIELDS = [
    "container_ext_id",
    "storage_pool_ext_id",
    "is_marked_for_removal",
    "max_capacity_bytes",
    "implicit_reserved_capacity_bytes",
    "is_encrypted",
    "cluster_name",
    "ext_id",
    "links",
    "tenant_id",
    "mapped_remote_containers",
]


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
            obj=storage_sdk.IPv4Address,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_spec,
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
        value=dict(type="str", required=False),
    )

    module_args = dict(
        ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=False),
        owner_ext_id=dict(type="str", required=False),
        storage_pool_ext_id=dict(type="str", required=False),
        max_capacity_bytes=dict(type="int", required=False),
        explicit_reserved_capacity_bytes=dict(type="int", required=False),
        advertised_capacity_bytes=dict(type="int", required=False),
        replication_factor=dict(type="int", required=False),
        oplog_replication_factor=dict(type="int", required=False),
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
            obj=storage_sdk.ErasureCodeStatus,
        ),
        is_inline_ec_enabled=dict(type="bool", required=False),
        has_higher_ec_fault_domain_preference=dict(type="bool", required=False),
        erasure_code_delay_secs=dict(type="int", required=False),
        cache_deduplication=dict(
            type="str",
            choices=["NONE", "OFF", "ON"],
            obj=storage_sdk.CacheDeduplication,
        ),
        on_disk_dedup=dict(
            type="str",
            choices=["NONE", "OFF", "POST_PROCESS"],
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


def create_AllStorageContainer(module, result, api_instance):
    validate_required_params(module, ["name", "cluster_ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")

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
            resp = get_storage_container(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(resp.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for AllStorageContainer"
                ),
                msg="Failed to get entity ext_id from task for AllStorageContainer",
            )
    result["changed"] = True


def check_for_idempotency(old_spec, update_spec):
    """Return True when the update spec introduces no changes.

    We only compare attributes that both sides expose so that server-populated
    read-only fields (e.g. ``max_capacity_bytes``) do not spuriously mark the
    operation as changed. Fields whose new value is ``None`` are treated as
    "unset" and skipped — the SDK does not send ``null`` in the update body
    for those.
    """
    old_dict = strip_internal_attributes(old_spec.to_dict())
    new_dict = strip_internal_attributes(update_spec.to_dict())
    for key in READ_ONLY_FIELDS:
        old_dict.pop(key, None)
        new_dict.pop(key, None)
    for key, new_val in list(new_dict.items()):
        if new_val is None:
            old_dict.pop(key, None)
            new_dict.pop(key, None)
    return old_dict == new_dict


def update_AllStorageContainer(module, result, api_instance):
    validate_required_params(module, ["ext_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    old_spec = get_storage_container(module, api_instance, ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating storage container", **result
        )
    kwargs = {"if_match": etag}

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update storage container spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec, update_spec):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(old_spec.to_dict())
        module.exit_json(
            msg="Nothing to change. Storage container with ext_id: {0} is already in the desired state.".format(
                ext_id
            ),
            **result,
        )

    strip_read_only_fields(update_spec, fields=READ_ONLY_FIELDS)

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
        resp = get_storage_container(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def delete_AllStorageContainer(module, result, api_instance):
    validate_required_params(module, ["ext_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Storage container with ext_id: {0} will be deleted.".format(
            ext_id
        )
        return

    ignore_small_files = module.params.get("ignore_small_files")
    resp = None
    delete_kwargs = {"extId": ext_id}
    if ignore_small_files is not None:
        # Pass boolean as a lowercase-string so the SDK serialises it into
        # ``?ignoreSmallFiles=true|false`` — servers reject the Python
        # ``True``/``False`` literal.
        delete_kwargs["ignoreSmallFiles"] = "true" if ignore_small_files else "false"
    try:
        resp = api_instance.delete_storage_container_by_ext_id(**delete_kwargs)
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
        task_status = wait_for_completion(module, task_ext_id, True)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("name", "ext_id"), True),
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
        "error": None,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_storage_container_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_AllStorageContainer(module, result, api_instance)
        else:
            create_AllStorageContainer(module, result, api_instance)
    else:
        delete_AllStorageContainer(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
