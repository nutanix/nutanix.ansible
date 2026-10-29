#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_foundation_central_config_v2
short_description: Update Foundation Central configuration
version_added: "2.7.0"
description:
    - Updates the configuration settings of the Foundation Central service.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update Foundation Central configuration) -
      Required Roles: Cluster Admin, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the Foundation Central configuration.
        type: str
        choices:
            - present
        default: present
    aos_download_timeout_minutes:
        description:
            - Timeout in minutes for AOS download.
        type: int
        required: false
    ahv_installation_timeout_minutes:
        description:
            - Timeout in minutes for AHV installation.
        type: int
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
- name: Update Foundation Central configuration
  nutanix.ncp.ntnx_foundation_central_config_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    aos_download_timeout_minutes: 90
    ahv_installation_timeout_minutes: 60
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating Foundation Central configuration.
        - Configuration details after the update operation.
    type: dict
    returned: always
    sample:
        {
            "ahv_installation_timeout_minutes": 60,
            "aos_download_timeout_minutes": 90,
            "commit_id": "f3fdb87d",
            "tls_certificate_fingerprint": "0a96886f32a7a03b0f729ecee1d217575c7a6f5f6e544ab1485b982b2323223b",
            "version": "2.2"
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
skipped:
    description: This indicates whether the task was skipped
    type: bool
    returned: When the operation was skipped
    sample: true
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:1a1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e5e"
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error or module is idempotent
    type: str
    sample: "Nothing to change."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
"""

import copy  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_etag,
    get_foundation_central_config_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_foundation_central_config  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_users_empty_attributes,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client  # noqa: E402, F401  # pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402, F401  # pylint: disable=unused-import
        mock_sdk as ntnx_lifecycle_py_client,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

WRITABLE_FIELDS = (
    "aos_download_timeout_minutes",
    "ahv_installation_timeout_minutes",
)


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        aos_download_timeout_minutes=dict(type="int"),
        ahv_installation_timeout_minutes=dict(type="int"),
    )
    return module_args


def check_foundation_central_config_idempotency(current_spec, update_spec):
    for field in WRITABLE_FIELDS:
        if getattr(current_spec, field, None) != getattr(update_spec, field, None):
            return False
    return True


def update_foundation_central_config(module, result, api_instance):
    current_spec = get_foundation_central_config(module, api_instance)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Failed to get etag value from the current Foundation Central config",
            **result,
        )

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating Foundation Central config",
            **result,
        )

    if check_foundation_central_config_idempotency(current_spec, update_spec):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current_spec.to_dict())
        if module.check_mode:
            return
        module.exit_json(msg="Nothing to change.", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    kwargs = {"if_match": etag_value}
    resp = None
    try:
        resp = api_instance.update_foundation_central_config(body=update_spec, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating Foundation Central config",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)

    updated_config = get_foundation_central_config(module, api_instance)
    result["response"] = strip_internal_attributes(updated_config.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
    }
    api_instance = get_foundation_central_config_api_instance(module)
    update_foundation_central_config(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
