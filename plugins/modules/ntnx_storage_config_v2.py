#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_storage_config_v2
short_description: Update the storage configuration of a Nutanix cluster in Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the storage configuration settings of a Nutanix cluster in Prism Central.
  - Storage configuration is a singleton resource per cluster, identified by the cluster external ID.
  - There is no create or delete operation for storage configuration; only update is supported.
  - The module fetches the current storage configuration and updates only the fields you specify.
  - The module is idempotent; if the desired configuration matches the current configuration, no change is made.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Update Storage Configuration) -
    Required Roles: Prism Admin, Storage Admin, Super Admin.
  - This module talks to Prism Central (PC), not to FCVM/Foundation.
  - The referenced cluster must exist and be registered with Prism Central before updating its storage configuration.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID (UUID) of the cluster whose storage configuration is to be updated.
      - Required for the update operation.
    type: str
    required: false
  resilient_capacity_warning_threshold_percentage:
    description:
      - The percentage threshold at which a resilient capacity warning is triggered.
      - Valid range is 0 to 100.
    type: int
    required: false
  is_rebuild_reservation_enabled:
    description:
      - Whether rebuild capacity reservation is enabled for the cluster.
    type: bool
    required: false
  is_rf1_enabled:
    description:
      - Whether replication factor 1 (RF1) storage containers are enabled for the cluster.
    type: bool
    required: false
  storage_over_provisioning_caution_threshold:
    description:
      - The storage over-provisioning caution threshold for the cluster.
    type: float
    required: false
  is_delayed_maintenance_resiliency_enabled:
    description:
      - Whether delayed maintenance resiliency is enabled for the cluster.
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
- name: Update storage configuration of a cluster
  nutanix.ncp.ntnx_storage_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "0006197f-3d06-ce49-1fc3-ac1f6b6029c1"
    resilient_capacity_warning_threshold_percentage: 75
    is_rebuild_reservation_enabled: true
    is_rf1_enabled: false
    storage_over_provisioning_caution_threshold: 3.0
    is_delayed_maintenance_resiliency_enabled: true
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating the storage configuration of the cluster.
    - If C(wait) is true, it returns the updated storage configuration details.
    - If C(wait) is false, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "is_delayed_maintenance_resiliency_enabled": true,
      "is_rebuild_reservation_enabled": false,
      "is_rf1_enabled": false,
      "resilient_capacity_warning_threshold_percentage": 75,
      "storage_over_provisioning_caution_threshold": 3.0
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:ac3dab28-ffc9-4eec-a08b-d70dd913180b"

ext_id:
  description:
    - The external ID of the cluster whose storage configuration was updated.
  returned: always
  type: str
  sample: "00065b6f-ec68-302b-185b-ac1f6b6f97e2"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped, for example during idempotency checks.
  returned: when the operation is skipped
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
  returned: When there is an error, module is idempotent, or in check mode.
  type: str
  sample: "Nothing to change."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_storage_config_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_storage_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as clustermgmt_sdk
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as clustermgmt_sdk

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=False),
        resilient_capacity_warning_threshold_percentage=dict(
            type="int", required=False
        ),
        is_rebuild_reservation_enabled=dict(type="bool", required=False),
        is_rf1_enabled=dict(type="bool", required=False),
        storage_over_provisioning_caution_threshold=dict(type="float", required=False),
        is_delayed_maintenance_resiliency_enabled=dict(type="bool", required=False),
    )
    return module_args


def check_idempotency(old_spec, update_spec):
    """Return True if the current and updated storage config specs are identical."""
    return old_spec == update_spec


def update_storage_config(module, api_instance, result):
    validate_required_params(module, ["cluster_ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    result["ext_id"] = cluster_ext_id

    current_resp = get_storage_config(module, api_instance, cluster_ext_id)
    current_spec = current_resp.data
    if not isinstance(current_spec, clustermgmt_sdk.StorageConfig):
        return module.fail_json(
            msg="Unexpected storage config response while updating storage config",
            **result,
        )

    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update storage config spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    etag = get_etag(data=current_resp)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating storage config", **result
        )

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_storage_config(
            clusterExtId=cluster_ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating storage config",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_storage_config(module, api_instance, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.data.to_dict())

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
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
    api_instance = get_storage_config_api_instance(module)
    update_storage_config(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
