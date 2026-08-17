#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_disassociate_host_nic_from_nic_profile_v2
short_description: Disassociate a Host NIC from a NIC Profile in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module disassociates a physical Host NIC from a NIC Profile in Nutanix Prism Central.
  - The disassociate workflow reverses a prior associate operation, removing the SR-IOV /
    DP Offload / PCIe Passthrough capability configuration from the target host.
  - The API is asynchronous and returns a task reference; the module waits for the task
    to complete when I(wait=true) (default) and then returns the updated NIC Profile.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation. The required roles depend on the operation being performed.
  - >-
    B(Disassociate a Host NIC from a NIC Profile) -
    Required Roles: Network Infra Admin, Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=networking)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported for this action-type module; the action always
        performs a disassociation regardless of state.
    type: str
    choices:
      - present
    default: present
  ext_id:
    description:
      - The external ID (UUID) of the NIC Profile from which the Host NIC will be
        disassociated.
    type: str
    required: true
  host_nic_ext_id:
    description:
      - The external ID (UUID) of the Host NIC that should be disassociated from the
        NIC Profile referenced by I(ext_id).
      - The Host NIC must currently be associated with the target NIC Profile.
    type: str
    required: true
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
- name: Disassociate a Host NIC from a NIC Profile
  nutanix.ncp.ntnx_disassociate_host_nic_from_nic_profile_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "d1f6a2f0-1b1d-4b6b-8c1e-1a2b3c4d5e6f"
    host_nic_ext_id: "a4b5c6d7-e8f9-4a0b-8c1d-2e3f4a5b6c7d"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for disassociating a Host NIC from a NIC Profile.
    - If C(wait) is true, this contains the refreshed NIC Profile with the updated
      C(host_nic_references) list (the disassociated Host NIC will no longer appear
      in it).
    - If C(wait) is false, this contains the task reference returned by the API.
  returned: always
  type: dict
  sample:
    {
      "capability_config": {
          "config_type": "SR_IOV",
          "num_v_fs": 4
      },
      "description": "SR-IOV NIC profile for ansible tests",
      "ext_id": "d1f6a2f0-1b1d-4b6b-8c1e-1a2b3c4d5e6f",
      "host_nic_references": [],
      "links": null,
      "metadata": null,
      "name": "nic_profile_ansible",
      "nic_family": "MELLANOX_CONNECTX_6",
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
    - The external ID of the NIC Profile from which the Host NIC was disassociated.
  returned: always
  type: str
  sample: "d1f6a2f0-1b1d-4b6b-8c1e-1a2b3c4d5e6f"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution
  returned: when an error occurs
  type: str
  sample: "Failed to fetch NIC Profile before disassociating Host NIC"

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode
  type: str
  sample: "Api Exception raised while disassociating Host NIC from NIC Profile"
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.network.api_client import (  # noqa: E402
    get_etag,
    get_nic_profiles_api_instance,
)
from ..module_utils.v4.network.helpers import get_nic_profile  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_networking_py_client as networking_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as networking_sdk  # noqa: E402

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """Return the argument spec for the disassociate Host NIC action module.

    The Host NIC request body maps directly to the SDK ``HostNic`` struct which
    exposes a single mandatory attribute, ``host_nic_ext_id``. The NIC Profile
    ``ext_id`` is the URI path parameter and is required for the action to run.
    """
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        host_nic_ext_id=dict(type="str", required=True),
    )
    return module_args


def disassociate_host_nic_from_nic_profile(module, result, api_instance):
    """Disassociate a Host NIC from a NIC Profile.

    Follows the same task-plus-fetch pattern used by ``ntnx_virtual_switch_v2``:
        1. Validate that the required parameters are present.
        2. Build the SDK ``HostNic`` request body via ``SpecGenerator``.
        3. Fetch the target NIC Profile so we can send the ``If-Match`` header
           (etag) and validate the Host NIC is actually associated with it.
        4. Call the SDK's ``disassociate_host_nic_from_nic_profile`` action.
        5. When ``wait`` is true, poll the task, then re-fetch the NIC Profile
           so the caller sees the updated ``host_nic_references`` list.
    """
    validate_required_params(module, ["ext_id", "host_nic_ext_id"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    sg = SpecGenerator(module)
    default_spec = networking_sdk.HostNic()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating disassociate Host NIC from NIC Profile spec",
            **result,
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    nic_profile = get_nic_profile(module, api_instance, ext_id)
    etag = get_etag(data=nic_profile)
    if not etag:
        module.fail_json(
            msg="Failed to fetch etag for NIC Profile before disassociating Host NIC",
            **result,
        )
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.disassociate_host_nic_from_nic_profile(
            extId=ext_id, body=spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while disassociating Host NIC from NIC Profile",
        )
    task_ext_id = resp.data.ext_id
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())

    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        refreshed = get_nic_profile(module, api_instance, ext_id)
        result["response"] = strip_internal_attributes(refreshed.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_networking_py_client"),
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
    api_instance = get_nic_profiles_api_instance(module)
    disassociate_host_nic_from_nic_profile(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
