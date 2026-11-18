#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_configs_visibility_v2
short_description: Update the security configurations visibility setting
version_added: "2.7.0"
description:
    - Update the list of security configurations settings being displayed on the Prism Central dashboard.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update Security Config Visibility Setting) -
      Required Roles: Prism Admin, Security Dashboard Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the security configurations visibility setting.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    is_secure_boot_visible:
        description:
            - Represents the visibility of host secure boot state.
        type: bool
        required: false
    is_network_segmentation_visible:
        description:
            - Represents the visibility of network segmentation state.
        type: bool
        required: false
    is_cluster_lockdown_visible:
        description:
            - Represents the visibility of cluster lockdown state.
        type: bool
        required: false
    is_log_forwarding_visible:
        description:
            - Represents the visibility of log forwarding state.
        type: bool
        required: false
    is_consent_banner_visible:
        description:
            - Represents the visibility of banner state.
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
- name: Update security configurations visibility setting
  nutanix.ncp.ntnx_security_configs_visibility_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    is_secure_boot_visible: true
    is_network_segmentation_visible: true
    is_cluster_lockdown_visible: true
    is_log_forwarding_visible: false
    is_consent_banner_visible: false
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating the security configurations visibility setting.
        - Contains the visibility setting details after the update.
    type: dict
    returned: always
    sample:
        {
            "is_cluster_lockdown_visible": true,
            "is_consent_banner_visible": false,
            "is_log_forwarding_visible": false,
            "is_network_segmentation_visible": true,
            "is_secure_boot_visible": true,
            "is_security_profile_visible": false
        }
changed:
    description: This indicates whether the task resulted in any changes
    type: bool
    returned: always
    sample: true
skipped:
    description: This indicates whether the task was skipped
    type: bool
    returned: when module is idempotent
    sample: false
failed:
    description: This indicates whether the task failed
    type: bool
    returned: always
    sample: false
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error, module is idempotent or check mode
    type: str
    sample: "Nothing to change."
error:
    description: This indicates the error message if any error occurred
    type: str
    returned: When an error occurs
"""

from copy import deepcopy  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_etag,
    get_security_configs_visibility_api_instance,
)
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_security_configs_visibility_setting,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_read_only_fields,
    strip_users_empty_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

READ_ONLY_ATTRIBUTES = ("is_security_profile_visible",)


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        is_secure_boot_visible=dict(type="bool"),
        is_network_segmentation_visible=dict(type="bool"),
        is_cluster_lockdown_visible=dict(type="bool"),
        is_log_forwarding_visible=dict(type="bool"),
        is_consent_banner_visible=dict(type="bool"),
    )
    return module_args


def check_visibility_idempotency(old_spec, update_spec):
    old_dict = strip_internal_attributes(old_spec.to_dict())
    update_dict = strip_internal_attributes(update_spec.to_dict())
    for field in READ_ONLY_ATTRIBUTES:
        old_dict.pop(field, None)
        update_dict.pop(field, None)
    return old_dict == update_dict


def update_security_configs_visibility(module, result, api_instance):
    current_spec = get_security_configs_visibility_setting(module, api_instance)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Failed to get etag value from the current security configs visibility setting",
            **result,
        )

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    default_spec = deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating security configs visibility setting",
            **result,
        )

    strip_read_only_fields(update_spec, fields=READ_ONLY_ATTRIBUTES)

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        result["msg"] = "Security configs visibility setting will be updated."
        return

    if check_visibility_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag_value}
    try:
        api_instance.update_security_configs_visibility_setting(
            body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating security configs visibility setting",
        )

    updated = get_security_configs_visibility_setting(module, api_instance)
    result["response"] = strip_internal_attributes(updated.to_dict())
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "failed": False,
        "response": None,
    }
    api_instance = get_security_configs_visibility_api_instance(module)
    update_security_configs_visibility(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
