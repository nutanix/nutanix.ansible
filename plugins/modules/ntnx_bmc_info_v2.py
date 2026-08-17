#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_bmc_info_v2
short_description: Update BMC (Baseboard Management Controller) info of a host in Nutanix Prism Central
version_added: 2.5.0
description:
  - This module allows you to update the out-of-band Baseboard Management Controller (BMC) info
    (IP address and basic-auth credentials) of a host that belongs to a cluster registered with
    Nutanix Prism Central.
  - BMC info is a sub-resource of a host in a cluster; the v4.2 clustermgmt APIs only expose
    Get and Update operations on this resource, so this module only supports the update flow.
  - The C(status) attribute of BMC info is server-populated (V(VALID)/V(INVALID)/V(UNAVAILABLE))
    and is treated as read-only by this module.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update BMC info of a host) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  state:
    description:
      - Only V(present) is supported for BMC info because the underlying v4 API does not
        expose create or delete operations. When set to V(absent) the module fails with a
        clear error message.
    type: str
    choices:
      - present
      - absent
    default: present
    required: false
  ext_id:
    description:
      - The external ID of the host whose BMC info should be updated.
    type: str
    required: true
  cluster_ext_id:
    description:
      - The external ID of the cluster that owns the host.
    type: str
    required: true
  ip_address:
    description:
      - IP address of the BMC. Provide exactly one of C(ipv4) or C(ipv6).
    type: dict
    required: false
    suboptions:
      ipv4:
        description:
          - IPv4 address of the BMC.
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
              - Prefix length of the IPv4 address.
            type: int
            required: false
            default: 32
      ipv6:
        description:
          - IPv6 address of the BMC.
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
              - Prefix length of the IPv6 address.
            type: int
            required: false
            default: 128
  credential:
    description:
      - Basic authentication credential (username / password) used by Prism / LCM to
        talk to the BMC over its OOB channel.
    type: dict
    required: false
    suboptions:
      username:
        description:
          - Username configured on the BMC.
        type: str
        required: true
      password:
        description:
          - Password configured on the BMC. Handled as a secret and never logged.
        type: str
        required: true
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_operations_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Abhinav Bansal (@abhinavbansal29)
"""

EXAMPLES = r"""
- name: Update BMC IP address and credential of a host
  nutanix.ncp.ntnx_bmc_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    ip_address:
      ipv4:
        value: "10.44.60.10"
        prefix_length: 24
    credential:
      username: "ADMIN"
      password: "SuperSecret.123"

- name: Rotate only the BMC credential (keep existing IP)
  nutanix.ncp.ntnx_bmc_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"
    ext_id: "8300384a-56ee-4750-aeb8-3d1c42908bee"
    credential:
      username: "ADMIN"
      password: "RotatedSecret.456"
"""

RETURN = r"""
response:
  description:
    - Response of the BMC info update operation.
    - If C(wait) is true, the response contains the refreshed BMC info entity after the task completes.
    - If C(wait) is false, the response contains the task details.
  returned: always
  type: dict
  sample:
    {
        "credential": {
            "password": null,
            "username": "ADMIN"
        },
        "ip_address": {
            "ipv4": {
                "prefix_length": 32,
                "value": "10.44.60.10"
            },
            "ipv6": null
        },
        "status": "VALID"
    }

task_ext_id:
  description:
    - The external ID of the task created by the update operation.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the host whose BMC info was updated.
  returned: always
  type: str
  sample: "8300384a-56ee-4750-aeb8-3d1c42908bee"

cluster_ext_id:
  description:
    - The external ID of the cluster that owns the host.
  returned: always
  type: str
  sample: "bde7fc02-fe9c-4ce3-9212-2ca4e4b4d258"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the operation was skipped due to idempotency.
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
  description: This indicates the message when there is an error, on idempotency, or when state=absent is requested.
  returned: When there is an error, module is idempotent or state=absent is requested
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
    get_bmc_api_instance,
    get_etag,
)
from ..module_utils.v4.clusters_mgmt.helpers import get_bmc_info  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_clustermgmt_py_client as cluster_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as cluster_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    ipv4_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=32),
    )

    ipv6_address_spec = dict(
        value=dict(type="str", required=True),
        prefix_length=dict(type="int", required=False, default=128),
    )

    ip_address_spec = dict(
        ipv4=dict(
            type="dict",
            options=ipv4_address_spec,
            obj=cluster_management_sdk.IPv4Address,
            required=False,
        ),
        ipv6=dict(
            type="dict",
            options=ipv6_address_spec,
            obj=cluster_management_sdk.IPv6Address,
            required=False,
        ),
    )

    credential_spec = dict(
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    module_args = dict(
        ext_id=dict(type="str", required=True),
        cluster_ext_id=dict(type="str", required=True),
        ip_address=dict(
            type="dict",
            options=ip_address_spec,
            obj=cluster_management_sdk.IPAddress,
            required=False,
            mutually_exclusive=[("ipv4", "ipv6")],
        ),
        credential=dict(
            type="dict",
            options=credential_spec,
            obj=cluster_management_sdk.BasicAuth,
            required=False,
        ),
    )
    return module_args


def _check_for_idempotency(old_spec_dict, update_spec_dict):
    """Return True if the update payload matches the current BMC info spec."""
    old = strip_internal_attributes(deepcopy(old_spec_dict))
    new = strip_internal_attributes(deepcopy(update_spec_dict))
    # `status` is server-populated (VALID/INVALID/UNAVAILABLE) — ignore in diff.
    old.pop("status", None)
    new.pop("status", None)
    # BMC never echoes the password back, so an update that only re-sets the
    # password must never be reported as no-op.
    old_cred = old.get("credential") or {}
    new_cred = new.get("credential") or {}
    if new_cred.get("password") is not None:
        return False
    if old_cred.get("username") != new_cred.get("username"):
        return False
    return old.get("ip_address") == new.get("ip_address")


def update_BmcInfo(module, result, api_instance):
    cluster_ext_id = module.params.get("cluster_ext_id")
    host_ext_id = module.params.get("ext_id")
    result["cluster_ext_id"] = cluster_ext_id
    result["ext_id"] = host_ext_id

    # Build a preview spec from user params on top of a fresh default so that
    # check_mode does NOT depend on the live BMC endpoint (which is documented
    # to return 503 on small PCs). This mirrors ntnx_ssl_certificates_v2.
    sg = SpecGenerator(module)
    default_spec = cluster_management_sdk.BmcInfo()
    preview_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update BMC info spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(preview_spec.to_dict())
        return

    current_spec = get_bmc_info(module, api_instance, cluster_ext_id, host_ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating BMC info", **result
        )

    update_spec, err = sg.generate_spec(obj=deepcopy(current_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating update BMC info spec", **result)

    if _check_for_idempotency(current_spec.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_spec.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag}
    resp = None
    try:
        resp = api_instance.update_bmc_info(
            clusterExtId=cluster_ext_id,
            extId=host_ext_id,
            body=update_spec,
            **kwargs,
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating BMC info",
        )

    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_bmc_info(module, api_instance, cluster_ext_id, host_ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
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
        "cluster_ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    state = module.params.get("state")
    if state == "absent":
        module.fail_json(
            msg=(
                "state=absent is not supported for BMC info — the v4 API "
                "only exposes get and update operations on this resource."
            ),
            **result,
        )

    api_instance = get_bmc_api_instance(module)
    update_BmcInfo(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
