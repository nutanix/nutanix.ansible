#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_cluster_ssh_access_control_v2
short_description: Update external SSH access control for a cluster
version_added: "2.7.0"
description:
  - This module allows you to update the external SSH access control
    settings of a cluster in Nutanix Prism Central.
  - External SSH access control is a singleton resource per cluster,
    identified by the cluster external ID.
  - There is no create or delete operation for this resource; only
    update is supported.
  - This module uses PC v4 APIs based SDKs.
notes:
  - This module talks to Prism Central (PC).
  - >-
    This module requires the following Nutanix IAM roles to be assigned
    to the user performing the operation.
  - >-
    B(Update External SSH Access Control) -
    Required Roles: Cluster Admin, Prism Admin, Super Admin
  - The cluster referenced by C(cluster_ext_id) must exist before
    updating SSH access control.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - Specify state.
      - If C(state) is set to C(present), the module will update the
        external SSH access control.
      - C(absent) is not supported because SSH access control cannot be
        deleted.
    type: str
    choices:
      - present
    default: present
  cluster_ext_id:
    description:
      - The external ID of the cluster to update SSH access control for.
    type: str
    required: true
  is_ssh_enabled:
    description:
      - Indicates whether SSH is currently enabled on the cluster.
    type: bool
    required: false
  is_password_login_enabled:
    description:
      - Indicates whether password-based SSH login is enabled on the
        cluster.
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
- name: Update external SSH access control - enable SSH
  nutanix.ncp.ntnx_cluster_ssh_access_control_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
    is_ssh_enabled: true
    is_password_login_enabled: false
  register: result
  ignore_errors: true

- name: Update external SSH access control - disable SSH
  nutanix.ncp.ntnx_cluster_ssh_access_control_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00062db3-c8a6-4b3d-8b9a-7f4d9b2c1a55"
    is_ssh_enabled: false
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for updating external SSH access control for a cluster.
    - If C(wait) is true, it will contain the SSH access control details after completion.
    - If C(wait) is false, it will contain the initial task details.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "00065ffe-0266-379f-0000-000000028f57",
      "is_password_login_enabled": true,
      "is_ssh_enabled": true,
      "links": [],
      "ssh_access_inconsistency_details": [],
      "tenant_id": "00065ffe-0266-379f-0000-000000028f57"
    }

task_ext_id:
  description:
    - The external ID of the task.
  returned: always
  type: str
  sample: "ZXJnb24=:bdd07ab4-889b-4617-723f-ccedfb0416ad"

ext_id:
  description:
    - The external ID of the cluster whose SSH access control was
      updated.
  returned: always
  type: str
  sample: "00065ffe-0266-379f-0000-000000028f57"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped due to idempotency.
  returned: when module is idempotent
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any occurred.
  returned: When there is an error or when module is idempotent
  type: str
  sample: "Nothing to change."
"""

import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_etag,
    get_ssh_control_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import (  # noqa: E402
    get_external_ssh_access_control,
)
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


_EXTERNAL_SSH_ACCESS_CONTROL_READ_ONLY_FIELDS = (
    "ext_id",
    "links",
    "tenant_id",
    "ssh_access_inconsistency_details",
)


def get_module_spec():

    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        cluster_ext_id=dict(type="str", required=True),
        is_ssh_enabled=dict(type="bool", required=False),
        is_password_login_enabled=dict(type="bool", required=False),
    )
    return module_args


def check_for_idempotency(old_spec_dict, update_spec_dict):
    old_spec_dict = strip_internal_attributes(old_spec_dict)
    update_spec_dict = strip_internal_attributes(update_spec_dict)
    for key in _EXTERNAL_SSH_ACCESS_CONTROL_READ_ONLY_FIELDS:
        old_spec_dict.pop(key, None)
        update_spec_dict.pop(key, None)
    return old_spec_dict == update_spec_dict


def update_external_ssh_access_control(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")

    result["cluster_ext_id"] = cluster_ext_id
    old_spec = get_external_ssh_access_control(module, api_instance, cluster_ext_id)
    etag = get_etag(data=old_spec)
    if not etag:
        return module.fail_json(
            "Unable to fetch etag for updating external SSH access control", **result
        )
    kwargs = {"if_match": etag}
    sg = SpecGenerator(module)
    update_spec, err = sg.generate_spec(obj=deepcopy(old_spec))
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating update external SSH access control spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if check_for_idempotency(old_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    strip_read_only_fields(
        update_spec, fields=_EXTERNAL_SSH_ACCESS_CONTROL_READ_ONLY_FIELDS
    )
    resp = None
    try:
        resp = api_instance.update_external_ssh_access_control(
            clusterExtId=cluster_ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating external SSH access control",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        resp = get_external_ssh_access_control(module, api_instance, cluster_ext_id)
        result["response"] = strip_internal_attributes(resp.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_ssh_control_api_instance(module)
    update_external_ssh_access_control(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
