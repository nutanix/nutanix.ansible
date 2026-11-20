#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iam_system_config_v2
short_description: Update system configurations in Nutanix Prism Central
version_added: "2.7.0"
description:
    - Update system configurations in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update system configuration) -
      Required Roles: Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the system configuration.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    name_value_pair:
        description:
            - Name Value Pair of the system configuration.
        type: list
        elements: dict
        required: true
        suboptions:
            name:
                description:
                    - The key of the key-value pair.
                type: str
                required: true
            value:
                description:
                    - The value associated with the key for this key-value pair.
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
- name: Update system configuration
  nutanix.ncp.ntnx_iam_system_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    name_value_pair:
      - name: "sample_config_key"
        value: "sample_config_value"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for updating system configuration.
        - Returns the updated system configuration details.
    returned: always
    type: dict
    sample:
        {
            "last_updated_time": "2026-07-21T06:36:56.065999+00:00",
            "name_value_pair": [
                {
                    "name": "sample_config_key",
                    "value": "sample_config_value"
                }
            ]
        }
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
skipped:
    description: This indicates whether the task was skipped
    returned: when module is idempotent
    type: bool
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or module is idempotent
    type: str
    sample: "Nothing to change."
error:
    description: This indicates the error message if any error occurred
    returned: When an error occurs
    type: str
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_system_config_api_instance,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_iam_py_client as identity_and_access_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as identity_and_access_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    kv_pair_spec = dict(
        name=dict(type="str", required=True),
        value=dict(type="str", required=False),
    )

    module_args = dict(
        state=dict(type="str", choices=["present"], default="present"),
        name_value_pair=dict(
            type="list",
            elements="dict",
            options=kv_pair_spec,
            obj=identity_and_access_management_sdk.KVPair,
            required=True,
        ),
    )
    return module_args


def check_system_config_idempotency(current_spec, update_spec):
    """
    Check idempotency for system config update.
    Compares name_value_pair lists.
    """
    current = strip_internal_attributes(current_spec.to_dict())
    update = strip_internal_attributes(update_spec.to_dict())
    # Compare name_value_pair ignoring order if needed
    curr_pairs = sorted(
        current.get("name_value_pair") or [], key=lambda x: x.get("name", "")
    )
    upd_pairs = sorted(
        update.get("name_value_pair") or [], key=lambda x: x.get("name", "")
    )
    if curr_pairs != upd_pairs:
        return False
    # Also check that update spec doesn't have extra changes
    # last_updated_time is read-only and should be ignored
    # Already stripped via strip_internal_attributes but ensure
    return True


def update_system_config(module, result, api_instance):
    # Fetch current system config to get etag and baseline spec
    # This endpoint is accessible over mTLS only; handle fetch failure gracefully
    # for check_mode and for live update fallback.
    current_spec = None
    etag = None
    try:
        # Direct API call to avoid helper's fail_json on mTLS error
        current_spec = api_instance.get_system_config().data
        etag = get_etag(data=current_spec)
    except Exception:
        # Fallback: create empty spec as base when fetch fails (e.g., mTLS restriction)
        # SpecGenerator will populate from module params.
        # In check_mode we still need to return a valid response.
        current_spec = None

    sg = SpecGenerator(module)
    if current_spec is not None:
        base_spec = deepcopy(current_spec)
    else:
        base_spec = identity_and_access_management_sdk.SystemConfig()
    update_spec, err = sg.generate_spec(obj=base_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating system configuration update spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if current_spec is not None and check_system_config_idempotency(
        current_spec, update_spec
    ):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_spec.to_dict())
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {}
    if etag:
        kwargs["if_match"] = etag

    resp = None
    try:
        resp = api_instance.update_system_config(body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating system configuration",
        )

    result["response"] = strip_internal_attributes(resp.data.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}

    api_instance = get_system_config_api_instance(module)
    update_system_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
