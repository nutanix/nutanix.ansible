#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_containers_v2
short_description: Manage storage containers in Nutanix Prism Central
description:
    - This module allows you to create, update, and delete storage containers in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
version_added: 2.0.0
options:
  state:
    description:
        - Specify state
        - If C(state) is set to C(present) then module will create storage container.
        - if C(state) is set to C(present) and C(ext_id) is given, then module will update storage container.
        - If C(state) is set to C(absent) with C(ext_id), then module will delete storage container.
    choices:
        - present
        - absent
    type: str
    default: present
  wait:
      description: Wait for the operation to complete.
      type: bool
      required: false
      default: True
  owner_ext_id:
    description:
      - The external ID of the owner of the storage container.
    required: false
    type: str
  ext_id:
    description:
      - The external ID of the storage container.
    required: false
    type: str
  name:
    description:
      - The name of the storage container.
    required: false
    type: str
  cluster_ext_id:
    description:
      - The external ID of the cluster where the storage container belongs.
    required: false
    type: str
  logical_explicit_reserved_capacity_bytes:
    description:
      - The logical explicit reserved capacity of the storage container in bytes.
    required: false
    type: int
  logical_advertised_capacity_bytes:
    description:
      - The logical advertised capacity of the storage container in bytes.
    required: false
    type: int
  replication_factor:
    description:
      - The replication factor of the storage container.
    required: false
    type: int
  nfs_whitelist_address:
    description:
      - The NFS whitelist addresses of the storage container.
    required: false
    type: list
    elements: dict
    suboptions:
      ipv4:
        description:
          - The IPv4 address.
        required: false
        type: dict
        suboptions:
          value:
            description:
              - The value of the IPv4 address.
            required: true
            type: str
          prefix_length:
            description:
              - The prefix length of the IPv4 address.
            required: false
            type: int
      ipv6:
        description:
          - The IPv6 address.
        required: false
        type: dict
        suboptions:
          value:
            description:
              - The value of the IPv6 address.
            required: true
            type: str
          prefix_length:
            description:
              - The prefix length of the IPv6 address.
            required: false
            type: int
      fqdn:
        description:
          - The fully qualified domain name.
        required: false
        type: dict
        suboptions:
          value:
            description:
              - The value of the fully qualified domain name.
            required: true
            type: str
  erasure_code:
    description:
      - The erasure code setting.
    required: false
    type: str
    choices: ['NONE', 'OFF', 'ON']
  is_inline_ec_enabled:
    description:
      - Whether inline erasure coding is enabled.
    required: false
    type: bool
  has_higher_ec_fault_domain_preference:
    description:
      - Whether the storage container has higher erasure coding fault domain preference.
    required: false
    type: bool
  erasure_code_delay_secs:
    description:
      - The delay in seconds for erasure coding.
    required: false
    type: int
  cache_deduplication:
    description:
      - The cache deduplication setting.
    required: false
    type: str
    choices: ['NONE', 'OFF', 'ON']
  on_disk_dedup:
    description:
      - The on-disk deduplication setting.
    required: false
    type: str
    choices: ['NONE', 'OFF', 'POST_PROCESS']
  is_compression_enabled:
    description:
      - Whether compression is enabled.
    required: false
    type: bool
  compression_delay_secs:
    description:
      - The delay in seconds for compression.
    required: false
    type: int
  is_internal:
    description:
      - Whether the storage container is internal.
    required: false
    type: bool
  is_software_encryption_enabled:
    description:
      - Whether software encryption is enabled.
    required: false
    type: bool
  affinity_host_ext_id:
    description:
      - The external ID of the affinity host.
    required: false
    type: str
  ignore_small_files:
    description:
      - Whether to ignore small files during delete operation.
    required: false
    type: bool
extends_documentation_fragment:
      - nutanix.ncp.ntnx_credentials
      - nutanix.ncp.ntnx_operations_v2
author:
 - Alaa Bishtawi (@alaabishtawi)
 - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Create storage container with minimal spec
  nutanix.ncp.ntnx_storage_containers_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    name: storage_container_name
    cluster_ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2

- name: Create storage container
  nutanix.ncp.ntnx_storage_containers_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    name: storage_container_name
    cluster_ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
    owner_ext_id: 12345678-1234-1234-1324-123456789012
    logical_explicit_reserved_capacity_bytes: 20
    logical_implicit_reserved_capacity_bytes: 100
    logical_advertised_capacity_bytes: 1073741824000
    on_disk_dedup: "OFF"
    is_compression_enabled: true
    compression_delay_secs: 3600
    is_internal: false
    is_software_encryption_enabled: false
    is_encrypted: false
    is_nfs_whitelist_inherited: false
    is_inline_ec_enabled: false
    has_higher_ec_fault_domain_preference: true

- name: Update storage container
  nutanix.ncp.ntnx_storage_containers_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
    name: storage_container_name
    cluster_ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
    owner_ext_id: 12345678-1234-1234-1324-123456789012
    logical_explicit_reserved_capacity_bytes: 20

- name: Delete storage container
  nutanix.ncp.ntnx_storage_containers_v2:
    nutanix_host: <pc_ip>
    nutanix_username: <user>
    nutanix_password: <pass>
    ext_id: 00061de6-4a87-6b06-185b-ac1f6b6f97e2
    state: absent
"""

RETURN = r"""
response:
    description:
        - Response for the storage container operation.
        - Storage container details if C(wait) is true.
        - Task details if C(wait) is false.
    type: dict
    returned: always
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
        "ext_id": null,
        "has_higher_ec_fault_domain_preference": false,
        "is_compression_enabled": false,
        "is_encrypted": null,
        "is_inline_ec_enabled": false,
        "is_internal": false,
        "is_marked_for_removal": false,
        "is_nfs_whitelist_inherited": true,
        "is_software_encryption_enabled": false,
        "links": null,
        "logical_advertised_capacity_bytes": null,
        "logical_explicit_reserved_capacity_bytes": 0,
        "logical_implicit_reserved_capacity_bytes": 0,
        "max_capacity_bytes": 4291605771923,
        "name": "dIJXzxaJJkVFansible-ag1",
        "nfs_whitelist_address": null,
        "on_disk_dedup": "OFF",
        "owner_ext_id": "00000000-0000-0000-0000-000000000000",
        "replication_factor": null,
        "storage_pool_ext_id": "487c142e-6c41-4b10-9585-4feac6bd3c68",
        "tenant_id": null
      }
task_ext_id:
    description:
        - Task external ID.
    type: str
    returned: always
    sample: ZXJnb24=:d0fe946a-83b7-464d-bafb-4826282a75b1
ext_id:
    description:
        - External ID of the storage container.
    type: str
    returned: always
    sample: 4bc0962b-8fc1-4d04-b188-0a183c158e67
changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true
error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: always
  type: bool
  sample: false
skipped:
    description: This field indicates whether the task was skipped. For example during idempotency checks.
    returned: always
    type: bool
    sample: true
"""

import traceback  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.base_module import BaseModule  # noqa: E402
from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
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
)

SDK_IMP_ERROR = None
from ansible.module_utils.basic import missing_required_lib  # noqa: E402

try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()


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
        ipv4=dict(type="dict", options=ipv4_spec, required=False),
        ipv6=dict(type="dict", options=ipv6_spec, required=False),
        fqdn=dict(type="dict", options=fqdn_spec, required=False),
    )
    module_args = dict(
        owner_ext_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        cluster_ext_id=dict(type="str", required=False),
        logical_explicit_reserved_capacity_bytes=dict(type="int", required=False),
        logical_advertised_capacity_bytes=dict(type="int", required=False),
        replication_factor=dict(type="int", required=False),
        nfs_whitelist_address=dict(
            type="list",
            elements="dict",
            options=nfs_whitelist_address_spec,
            required=False,
        ),
        erasure_code=dict(type="str", choices=["NONE", "OFF", "ON"]),
        is_inline_ec_enabled=dict(type="bool", required=False),
        has_higher_ec_fault_domain_preference=dict(type="bool", required=False),
        erasure_code_delay_secs=dict(type="int", required=False),
        cache_deduplication=dict(type="str", choices=["NONE", "OFF", "ON"]),
        on_disk_dedup=dict(type="str", choices=["NONE", "OFF", "POST_PROCESS"]),
        is_compression_enabled=dict(type="bool", required=False),
        compression_delay_secs=dict(type="int", required=False),
        is_internal=dict(type="bool", required=False),
        is_software_encryption_enabled=dict(type="bool", required=False),
        affinity_host_ext_id=dict(type="str", required=False),
        ext_id=dict(type="str", required=False),
        ignore_small_files=dict(type="bool", required=False),
    )
    return module_args


def create_storage_container(module, storage_container_api, result):
    sg = SpecGenerator(module)
    default_spec = clustermgmt_sdk.StorageContainer()
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
    cluster_ext_id = module.params.get("cluster_ext_id")
    if not cluster_ext_id:
        return module.fail_json(
            "cluster_ext_id is required in case of creating storage container", **result
        )
    try:
        resp = storage_container_api.create_storage_container(
            body=spec, X_Cluster_Id=cluster_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while creating storage container",
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
            resp = get_storage_container(module, storage_container_api, ext_id)
            result["ext_id"] = ext_id
            result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def check_idempotency(old_spec, update_spec):
    if old_spec == update_spec:
        return True
    return False


def update_storage_container(module, storage_container_api, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current_spec = get_storage_container(module, storage_container_api, ext_id)

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))

    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update storage container spec", **result
        )
    # Setting external ID to None in update spec as 'container_ext_id' is being used instead
    if hasattr(current_spec, "ext_id"):
        update_spec.ext_id = None

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    resp = None
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            "unable to fetch etag for updating storage container", **result
        )

    kwargs = {"if_match": etag}
    try:
        resp = storage_container_api.update_storage_container_by_id(
            ext_id, update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while updating storage container",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_storage_container(module, storage_container_api, ext_id)
        result["ext_id"] = ext_id
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def delete_storage_container(module, storage_container_api, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = "Storage container with ext_id: {0} will be deleted.".format(
            ext_id
        )
        return

    ignore_small_files = module.params.get("ignore_small_files")
    try:
        resp = storage_container_api.delete_storage_container_by_id(
            extId=ext_id, ignore_small_files=ignore_small_files
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="API Exception while deleting storage container",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("name", "ext_id"), True),
            ("state", "present", ("cluster_ext_id",)),
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
        "error": None,
        "response": None,
        "ext_id": None,
    }
    state = module.params.get("state")
    storage_container_api = get_storage_containers_api_instance(module)
    if state == "present":
        if module.params.get("ext_id"):
            update_storage_container(module, storage_container_api, result)
        else:
            create_storage_container(module, storage_container_api, result)
    elif state == "absent":
        delete_storage_container(module, storage_container_api, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
