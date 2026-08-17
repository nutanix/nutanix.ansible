#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_stores_by_cluster_id_v2
short_description: Manage NFS datastores (mount / unmount Storage Containers on ESXi) via Nutanix Prism Central
version_added: 2.7.0
description:
  - Manage the lifecycle of NFS datastores exposed to VMware ESXi hosts of a Nutanix cluster.
  - A datastore in a Nutanix ESXi cluster is a Storage Container that has been mounted as an NFS datastore on the ESXi hosts.
  - Setting C(state=present) mounts the given Storage Container as a datastore on the target ESXi node(s) — this "creates" the datastore.
  - Setting C(state=absent) unmounts the datastore from the target ESXi node(s) — this "deletes" the datastore.
  - Datastores are identified inside a cluster by the pair C(ext_id) (parent Storage Container ext_id)
    plus C(datastore_name); they do not have their own PC-managed external identifier.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Mount Storage Container on ESX datastore) -
    Required Roles: Prism Admin, Storage Admin, Super Admin
  - >-
    B(Unmount Storage Container from ESX datastore) -
    Required Roles: Prism Admin, Storage Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) the module mounts the Storage Container as an NFS datastore on the target ESXi node(s).
      - If C(state) is set to C(absent) the module unmounts the datastore from the target ESXi node(s).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  cluster_ext_id:
    description:
      - The external identifier of the cluster the datastore belongs to.
      - Used for the idempotency lookup — the module lists the cluster's datastores and
        skips the operation when a datastore of the same name is already in the expected state.
    type: str
    required: false
  ext_id:
    description:
      - The external identifier of the parent Storage Container that is (or should be) exposed as an NFS datastore.
      - Required for both mount (C(state=present)) and unmount (C(state=absent)) operations because the
        Nutanix v4 API scopes datastore mount / unmount actions by the Storage Container ext_id.
      - Datastores do not have their own PC-managed external identifier — this identifier maps
        to the parent Storage Container.
    type: str
    required: false
  datastore_name:
    description:
      - Name of the datastore as it will appear on the ESXi hosts.
      - Optional for mount (defaults to the Storage Container name when not supplied), required for unmount.
      - Maximum 255 characters.
    type: str
    required: false
  container_name:
    description:
      - Name of the Storage Container being mounted as a datastore. Must be unique within the cluster.
      - Required for mount (C(state=present)) operation.
      - Maximum 75 characters.
    type: str
    required: false
  node_ext_ids:
    description:
      - The UUIDs of the ESXi nodes where the NFS datastore should be created (mount) or removed (unmount).
      - When omitted on mount the API mounts the datastore on all eligible nodes of the cluster.
    type: list
    elements: str
    required: false
  is_read_only:
    description:
      - Indicates whether the host system will have read-only access to the NFS share.
      - Only applicable to the mount (C(state=present)) operation.
    type: bool
    required: false
  target_path:
    description:
      - The target path on which to mount the NFS datastore on the ESXi host.
      - Only applicable to the mount (C(state=present)) operation.
    type: str
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
- name: Mount a Storage Container as a datastore on ESXi hosts
  nutanix.ncp.ntnx_data_stores_by_cluster_id_v2:
    state: present
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "547c01c4-19c2-4293-8a9c-43441c18d0c7"
    datastore_name: "ansible_datastore"
    container_name: "ansible_container"
    node_ext_ids:
      - "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    is_read_only: false
    target_path: "/vmfs/volumes/ansible_datastore"
  register: mount_result
  ignore_errors: true

- name: Unmount the datastore from ESXi hosts
  nutanix.ncp.ntnx_data_stores_by_cluster_id_v2:
    state: absent
    cluster_ext_id: "00061de6-4a87-6b06-185b-ac1f6b6f97e2"
    ext_id: "547c01c4-19c2-4293-8a9c-43441c18d0c7"
    datastore_name: "ansible_datastore"
    node_ext_ids:
      - "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: unmount_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for the mount / unmount operation.
    - If the operation is mount / unmount and C(wait) is true, it will return the completed task details.
    - If C(wait) is false, it will return the task submission response.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_ids": ["00061de6-4a87-6b06-185b-ac1f6b6f97e2"],
      "completed_time": "2026-07-20T11:22:33.000000+00:00",
      "created_time": "2026-07-20T11:22:29.000000+00:00",
      "entities_affected": [
        {
          "ext_id": "547c01c4-19c2-4293-8a9c-43441c18d0c7",
          "rel": "clustermgmt:config:storage-container"
        }
      ],
      "error_messages": null,
      "ext_id": "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209",
      "is_cancelable": false,
      "last_updated_time": "2026-07-20T11:22:33.000000+00:00",
      "legacy_error_message": null,
      "operation": "MountStorageContainer",
      "operation_description": "Mount Storage Container on ESX datastore",
      "progress_percentage": 100,
      "started_time": "2026-07-20T11:22:29.000000+00:00",
      "status": "SUCCEEDED",
      "sub_steps": null,
      "sub_tasks": null,
      "warnings": null
    }

task_ext_id:
  description:
    - The external ID of the task that performed the mount / unmount action.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external identifier of the Storage Container that backs the datastore.
  returned: always
  type: str
  sample: "547c01c4-19c2-4293-8a9c-43441c18d0c7"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped due to idempotency (datastore already in the requested state).
  returned: when applicable
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
  description: This indicates a human-readable status message. Populated in error paths, idempotency skips, and check mode.
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Datastore with name 'ansible_datastore' is already mounted on cluster '00061de6-4a87-6b06-185b-ac1f6b6f97e2'. Skipping mount."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_storage_containers_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    find_data_store_by_name,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the argument spec for the datastore CRUD-style module.

    ``ext_id`` here refers to the parent Storage Container's external
    identifier because datastores in Nutanix are implemented as mounted
    Storage Containers and do not have their own PC-managed identifier.
    """
    module_args = dict(
        cluster_ext_id=dict(type="str", required=False),
        ext_id=dict(type="str", required=False),
        datastore_name=dict(type="str", required=False),
        container_name=dict(type="str", required=False),
        node_ext_ids=dict(type="list", elements="str", required=False),
        is_read_only=dict(type="bool", required=False),
        target_path=dict(type="str", required=False),
    )

    return module_args


def _idempotency_lookup(module, api_instance, cluster_ext_id, datastore_name):
    """Return the existing DataStore matching name in the cluster, or None.

    Idempotency for mount/unmount is derived by inspecting the cluster's
    current datastore list. We treat two datastores as identical when their
    ``datastore_name`` matches inside the same cluster — this is the only
    field the ESX layer uniquely keys on.
    """
    if not cluster_ext_id or not datastore_name:
        return None
    return find_data_store_by_name(module, api_instance, cluster_ext_id, datastore_name)


def create_data_stores_by_cluster_id(module, result, api_instance):
    """Mount a Storage Container as an ESX datastore ("create" the datastore)."""
    validate_required_params(module, ["ext_id", "container_name"])

    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    datastore_name = module.params.get("datastore_name") or module.params.get(
        "container_name"
    )
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.DataStoreMount()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating mount storage container (create datastore) spec",
            **result,
        )
    if not spec.datastore_name:
        spec.datastore_name = datastore_name

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    existing = _idempotency_lookup(module, api_instance, cluster_ext_id, datastore_name)
    if existing is not None:
        result["skipped"] = True
        result["response"] = strip_internal_attributes(existing.to_dict())
        result["msg"] = (
            "Datastore with name '{0}' is already mounted on cluster '{1}'. "
            "Skipping mount.".format(datastore_name, cluster_ext_id)
        )
        module.exit_json(**result)

    resp = None
    try:
        resp = api_instance.mount_storage_container(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while mounting storage container as datastore",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


def delete_data_stores_by_cluster_id(module, result, api_instance):
    """Unmount an ESX datastore ("delete" the datastore)."""
    validate_required_params(module, ["ext_id", "datastore_name"])

    ext_id = module.params.get("ext_id")
    cluster_ext_id = module.params.get("cluster_ext_id")
    datastore_name = module.params.get("datastore_name")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.DataStoreUnmount()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating unmount storage container (delete datastore) spec",
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "Datastore with name '{0}' backed by storage container ext_id "
            "'{1}' will be unmounted.".format(datastore_name, ext_id)
        )
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    existing = _idempotency_lookup(module, api_instance, cluster_ext_id, datastore_name)
    if cluster_ext_id and existing is None:
        result["skipped"] = True
        result["msg"] = (
            "Datastore with name '{0}' is not mounted on cluster '{1}'. "
            "Skipping unmount.".format(datastore_name, cluster_ext_id)
        )
        module.exit_json(**result)

    resp = None
    try:
        resp = api_instance.unmount_storage_container(extId=ext_id, body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unmounting datastore from ESX host",
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
            ("state", "present", ("ext_id",)),
            ("state", "absent", ("ext_id", "datastore_name")),
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
        create_data_stores_by_cluster_id(module, result, api_instance)
    else:
        delete_data_stores_by_cluster_id(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
