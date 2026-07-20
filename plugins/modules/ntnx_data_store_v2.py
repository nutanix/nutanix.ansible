#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_store_v2
short_description: Mount and Unmount Data Stores in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to mount (create) and unmount (delete) NFS Data Stores in Nutanix Prism Central.
  - A Data Store is the hypervisor-facing representation of a Storage Container.
  - Mounting a Data Store exposes a Storage Container to the specified hypervisor hosts (ESXi/AHV) as an NFS datastore.
  - The Storage Container ext_id is used as the URL parameter for both mount and unmount operations.
  - Update operation is not supported by the underlying v4 API. Use state C(absent) followed by state C(present) to change the mount configuration.
  - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Mount a Data Store) -
      Required Roles: Prism Admin, Storage Admin, Super Admin
    - >-
      B(Unmount a Data Store) -
      Required Roles: Prism Admin, Storage Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - If C(state) is set to C(present), the operation will be mount the Data Store on the specified nodes.
      - If C(state) is set to C(absent), the operation will unmount the Data Store from the specified nodes.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Storage Container to mount as a Data Store.
      - Required for both mount and unmount operations.
      - The underlying v4 API uses this value as the URL path parameter for both /$actions/mount and /$actions/unmount.
    type: str
    required: false
  cluster_ext_id:
    description:
      - The external ID of the Prism Element cluster that owns the Storage Container.
      - Required for idempotency checks (looking up existing Data Stores on the cluster before mount).
    type: str
    required: false
  datastore_name:
    description:
      - Name of the Data Store as it will appear on the hypervisor hosts.
      - Required for the mount operation. Must be unique per cluster.
    type: str
    required: false
  container_name:
    description:
      - Name of the underlying Storage Container to mount.
      - The name of a Storage Container is unique per cluster.
      - Required for the mount operation.
    type: str
    required: false
  node_ext_ids:
    description:
      - List of node (host) external IDs on which the NFS Data Store must be mounted or unmounted.
      - Required for both mount and unmount operations.
    type: list
    elements: str
    required: false
  read_only:
    description:
      - Indicates whether the host system has only read-only access to the NFS share.
      - Applies to the mount operation only.
    type: bool
    required: false
  target_path:
    description:
      - The target path on which to mount the NFS Data Store on the hypervisor hosts.
      - Applies to the mount operation only.
    type: str
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
- name: Mount a Data Store on selected nodes
  nutanix.ncp.ntnx_data_store_v2:
    state: present
    ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    datastore_name: "ansible_ds"
    container_name: "ansible_storage_container"
    node_ext_ids:
      - "f28e7475-f835-42ef-ac35-ecbc48d5421e"
    read_only: false
    target_path: "/vmfs/volumes/ansible_ds"
  register: result
  ignore_errors: true

- name: Unmount a Data Store from selected nodes
  nutanix.ncp.ntnx_data_store_v2:
    state: absent
    ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    datastore_name: "ansible_ds"
    node_ext_ids:
      - "f28e7475-f835-42ef-ac35-ecbc48d5421e"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for mounting or unmounting a Data Store.
    - If the operation is create and C(wait) is true, it will return the Data Store details (as reported by the list API).
    - If C(wait) is false, it will return the task details.
    - If the operation is delete, it will return the task details.
  returned: always
  type: dict
  sample:
    {
      "capacity_bytes": 4291605771923,
      "container_ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
      "container_name": "ansible_storage_container",
      "datastore_name": "ansible_ds",
      "ext_id": "b4bb1a51-1a5d-4a2c-9c8b-63c96c74ffe6",
      "free_space_bytes": 4290000000000,
      "host_ext_id": "f28e7475-f835-42ef-ac35-ecbc48d5421e",
      "host_ip_address": "10.44.76.55",
      "vm_names": []
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The Storage Container ext_id used for the mount/unmount action.
  returned: always
  type: str
  sample: "57516342-7d8e-470f-91b8-ae310737ff8c"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - Indicates that the operation was skipped (e.g. idempotency — the Data Store
      already exists on the cluster for the specified container).
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
  description: Status/error message.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Data Store with name 'ansible_ds' already exists on cluster '<cluster_ext_id>'. Skipping creation."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.storage.api_client import (  # noqa: E402
    get_storage_container_api_instance,
)
from ..module_utils.v4.storage.helpers import find_data_store  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_storage_py_client as storage_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as storage_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        datastore_name=dict(type="str"),
        container_name=dict(type="str"),
        node_ext_ids=dict(type="list", elements="str"),
        read_only=dict(type="bool"),
        target_path=dict(type="str"),
    )
    return module_args


def _find_existing_data_store(module, api_instance):
    """
    Idempotency helper: look up any existing DataStore on the target cluster
    that already maps to this Storage Container (by container_ext_id) or has
    the same datastore_name. Returns the matching DataStore dict or None.
    """
    cluster_ext_id = module.params.get("cluster_ext_id")
    container_ext_id = module.params.get("ext_id")
    datastore_name = module.params.get("datastore_name")

    if not cluster_ext_id:
        return None

    return find_data_store(
        module=module,
        api_instance=api_instance,
        cluster_ext_id=cluster_ext_id,
        container_ext_id=container_ext_id,
        datastore_name=datastore_name,
        strict=False,
    )


def create_data_store(module, result, api_instance):
    validate_required_params(
        module,
        [
            "ext_id",
            "cluster_ext_id",
            "datastore_name",
            "container_name",
            "node_ext_ids",
        ],
    )

    container_ext_id = module.params.get("ext_id")
    result["ext_id"] = container_ext_id

    sg = SpecGenerator(module)
    default_spec = storage_sdk.DataStoreMount()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating mount Data Store spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    existing = _find_existing_data_store(module, api_instance)
    if existing:
        result["response"] = strip_internal_attributes(existing)
        result["skipped"] = True
        module.exit_json(
            msg=(
                "Data Store with name '{0}' already exists on cluster '{1}'. "
                "Skipping creation."
            ).format(
                module.params.get("datastore_name"),
                module.params.get("cluster_ext_id"),
            ),
            **result,
        )

    resp = None
    try:
        resp = api_instance.add_data_store_for_cluster(
            extId=container_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while mounting Data Store",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_status.to_dict())
        existing = _find_existing_data_store(module, api_instance)
        if existing:
            result["response"] = strip_internal_attributes(existing)
            if existing.get("ext_id"):
                result["ext_id"] = existing.get("ext_id")

    result["changed"] = True


def delete_data_store(module, result, api_instance):
    validate_required_params(module, ["ext_id", "datastore_name", "node_ext_ids"])

    container_ext_id = module.params.get("ext_id")
    result["ext_id"] = container_ext_id

    if module.check_mode:
        result["msg"] = (
            "Data Store '{0}' backed by Storage Container ext_id:{1} will be unmounted "
            "from nodes: {2}."
        ).format(
            module.params.get("datastore_name"),
            container_ext_id,
            module.params.get("node_ext_ids"),
        )
        return

    unmount_spec = storage_sdk.DataStoreUnmount(
        datastore_name=module.params.get("datastore_name"),
        node_ext_ids=module.params.get("node_ext_ids"),
    )

    resp = None
    try:
        resp = api_instance.delete_data_store_for_cluster(
            extId=container_ext_id, body=unmount_spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unmounting Data Store",
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
            ("state", "present", ("ext_id",)),
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
        create_data_store(module, result, api_instance)
    else:
        delete_data_store(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
