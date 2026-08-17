#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_data_store_v2
short_description: Mount and Unmount Data Stores for a Nutanix cluster
version_added: 2.7.0
description:
  - This module allows you to mount (add) and unmount (delete) a Data Store
    for a Nutanix cluster in Nutanix Prism Central.
  - A Data Store is the ESXi-side representation of a Nutanix Storage
    Container that has been mounted on ESXi hypervisor nodes. It provides
    ESXi hosts an NFS-backed datastore that is served by the Nutanix
    Controller VM (CVM) on each node.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    The required roles depend on the operation being performed.
  - >-
    B(Mount a Data Store on a cluster) -
    Required Roles: Prism Admin, Storage Admin, Super Admin
  - >-
    B(Unmount a Data Store from a cluster) -
    Required Roles: Prism Admin, Storage Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=storage)"
options:
  state:
    description:
      - Specifies the desired state of the Data Store on the cluster.
      - If C(state) is set to C(present) the module will mount the Data Store
        on the specified Storage Container / cluster.
      - If C(state) is set to C(absent) the module will unmount the Data
        Store from the specified Storage Container / cluster.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the Data Store.
      - Informational only, populated by the platform once a Data Store has
        been mounted; the mount/unmount SDK methods are keyed off the parent
        Storage Container ext_id and the C(datastore_name), not this value.
    type: str
    required: false
  container_ext_id:
    description:
      - The external ID of the Storage Container that backs the Data Store.
      - Required for all mount and unmount operations because the underlying
        v4 storage APIs are addressed via the Storage Container ext_id.
    type: str
    required: true
  cluster_ext_id:
    description:
      - The external ID of the cluster the Data Store is / will be mounted
        on. Used for idempotency checks and for surfacing a friendly
        response.
    type: str
    required: false
  datastore_name:
    description:
      - The name of the Data Store to mount or unmount.
      - Required for both mount and unmount operations.
    type: str
    required: false
  container_name:
    description:
      - Name of the underlying Storage Container.
      - Used only when creating (mounting) a Data Store.
    type: str
    required: false
  node_ext_ids:
    description:
      - List of node (ESXi host) external IDs on which the Data Store will
        be mounted / unmounted.
      - If not provided, the mount / unmount is applied to all applicable
        ESXi hosts in the cluster.
    type: list
    elements: str
    required: false
  read_only:
    description:
      - When true, mount the Data Store as read only.
      - Applies to the mount (create) operation only.
    type: bool
    required: false
  target_path:
    description:
      - Absolute filesystem path on each ESXi node where the Data Store
        should be mounted.
      - Applies to the mount (create) operation only.
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
- name: Mount a Data Store on all ESXi nodes of a cluster
  nutanix.ncp.ntnx_data_store_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    container_ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    datastore_name: "ansible_ds"
    container_name: "SelfServiceContainer"
    read_only: false
    target_path: "/vmfs/volumes/ansible_ds"
    node_ext_ids:
      - "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result

- name: Unmount a Data Store from selected ESXi nodes
  nutanix.ncp.ntnx_data_store_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    container_ext_id: "57516342-7d8e-470f-91b8-ae310737ff8c"
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    datastore_name: "ansible_ds"
    node_ext_ids:
      - "8300384a-56ee-4750-aeb8-3d1c42908bee"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for mounting or unmounting a Data Store.
    - When C(state=present) and C(wait=true), the response is the resolved
      Data Store object (as returned by the List Data Stores API).
    - When C(state=present) and C(wait=false), the response is the task
      details.
    - When C(state=absent), the response is the task details for the
      unmount operation.
  returned: always
  type: dict
  sample:
    {
      "capacity_bytes": null,
      "container_ext_id": "57516342-7d8e-470f-91b8-ae310737ff8c",
      "container_name": "SelfServiceContainer",
      "datastore_name": "ansible_ds",
      "ext_id": "1a68c1cd-8f38-4d64-8fd1-01d34e94b1a2",
      "free_space_bytes": null,
      "host_ext_id": "8300384a-56ee-4750-aeb8-3d1c42908bee",
      "host_ip_address": null,
      "links": null,
      "tenant_id": null,
      "vm_names": null
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the Data Store.
    - Populated when it can be resolved from the task or a follow-up list.
  returned: always
  type: str
  sample: "1a68c1cd-8f38-4d64-8fd1-01d34e94b1a2"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (e.g. idempotency).
  returned: when applicable
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "Data Store with name 'ansible_ds' is already mounted. Skipping mount."

error:
  description: This indicates the error message if any error occurred.
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        container_ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str"),
        datastore_name=dict(type="str"),
        container_name=dict(type="str"),
        node_ext_ids=dict(type="list", elements="str"),
        read_only=dict(type="bool"),
        target_path=dict(type="str"),
    )
    return module_args


def _resolve_data_store_ext_id(module, api_instance, container_ext_id, datastore_name):
    """
    Attempt to resolve the Data Store ext_id after a mount succeeds.

    ``get_data_stores`` requires a cluster ext_id. If the user supplied it we
    query directly; otherwise the ext_id cannot be resolved via the current
    SDK surface and ``None`` is returned.
    """
    cluster_ext_id = module.params.get("cluster_ext_id")
    if not cluster_ext_id:
        return None
    ds = find_data_store(
        module,
        api_instance,
        cluster_ext_id=cluster_ext_id,
        datastore_name=datastore_name,
        container_ext_id=container_ext_id,
    )
    return ds


def create_data_store_for_cluster(module, result, api_instance):
    """
    Mount (add) a Data Store instance to the cluster by invoking the
    AddDataStoreForCluster SDK method.
    """
    validate_required_params(module, ["container_ext_id", "datastore_name"])
    container_ext_id = module.params.get("container_ext_id")
    datastore_name = module.params.get("datastore_name")

    sg = SpecGenerator(module)
    default_spec = storage_sdk.DataStoreMount()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating mount Data Store spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    if module.params.get("cluster_ext_id"):
        existing = find_data_store(
            module,
            api_instance,
            cluster_ext_id=module.params.get("cluster_ext_id"),
            datastore_name=datastore_name,
            container_ext_id=container_ext_id,
        )
        if existing:
            result["skipped"] = True
            result["ext_id"] = getattr(existing, "ext_id", None)
            result["response"] = strip_internal_attributes(existing.to_dict())
            result["msg"] = (
                "Data Store with name '{0}' is already mounted on cluster '{1}'."
                " Skipping mount.".format(
                    datastore_name, module.params.get("cluster_ext_id")
                )
            )
            module.exit_json(**result)

    resp = None
    try:
        resp = api_instance.add_data_store_for_cluster(
            extId=container_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while mounting Data Store for cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
        ds = _resolve_data_store_ext_id(
            module, api_instance, container_ext_id, datastore_name
        )
        if ds is not None:
            result["ext_id"] = getattr(ds, "ext_id", None)
            result["response"] = strip_internal_attributes(ds.to_dict())
    result["changed"] = True


def delete_data_store_for_cluster(module, result, api_instance):
    """
    Unmount (delete) a Data Store instance from the cluster by invoking the
    DeleteDataStoreForCluster SDK method.
    """
    validate_required_params(module, ["container_ext_id", "datastore_name"])
    container_ext_id = module.params.get("container_ext_id")
    datastore_name = module.params.get("datastore_name")
    result["ext_id"] = module.params.get("ext_id")

    if module.check_mode:
        result["msg"] = (
            "Data Store with name '{0}' on container ext_id '{1}' will be unmounted.".format(
                datastore_name, container_ext_id
            )
        )
        return

    spec = storage_sdk.DataStoreUnmount()
    spec.datastore_name = datastore_name
    if module.params.get("node_ext_ids") is not None:
        spec.node_ext_ids = module.params.get("node_ext_ids")

    resp = None
    try:
        resp = api_instance.delete_data_store_for_cluster(
            extId=container_ext_id, body=spec
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while unmounting Data Store for cluster",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("datastore_name",)),
            ("state", "absent", ("datastore_name",)),
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
        "ext_id": module.params.get("ext_id"),
        "task_ext_id": None,
        "failed": False,
    }
    api_instance = get_storage_container_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        create_data_store_for_cluster(module, result, api_instance)
    else:
        delete_data_store_for_cluster(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
