#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_security_profiles_v2
short_description: Update the security profile for a cluster
version_added: "2.7.0"
description:
    - Update the security profile for a cluster in Nutanix Prism Central.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Update Security Profile) -
      Required Roles: Prism Admin, Security Dashboard Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=security)"
options:
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will update the security profile.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
    ext_id:
        description:
            - External ID of the security profile.
            - Required for update.
        type: str
        required: true
    type:
        description:
            - Possible values for security profile types.
        type: str
        choices:
            - STANDARD
            - ELEVATED
            - STRICT
            - NOT_SET
            - NOT_SUPPORTED
        required: false
    wait:
        description:
            - Wait for the task to complete.
        type: bool
        default: true
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
- name: Update security profile type
  nutanix.ncp.ntnx_security_profiles_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "64eae63e-d671-483f-a8bf-e55e426a7168"
    type: STANDARD
  register: result
"""

RETURN = r"""
response:
    description:
        - Response for updating the security profile.
        - If C(wait) is true, it will contain the security profile details.
        - If C(wait) is false, it will contain the task details.
    type: dict
    returned: always
    sample:
        {
            "cluster_ext_id": "64eae63e-d671-483f-a8bf-e55e426a7168",
            "ext_id": "64eae63e-d671-483f-a8bf-e55e426a7168",
            "failure_details": null,
            "links": null,
            "tenant_id": null,
            "type": "STANDARD"
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
ext_id:
    description: The external ID of the security profile.
    type: str
    returned: always
    sample: "64eae63e-d671-483f-a8bf-e55e426a7168"
task_ext_id:
    description: The external ID of the task.
    type: str
    returned: always
    sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"
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

import copy  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402
from ..module_utils.v4.security.api_client import (  # noqa: E402
    get_etag,
    get_security_profiles_api_instance,
)
from ..module_utils.v4.security.helpers import (  # noqa: E402
    get_security_profile_by_ext_id,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    strip_users_empty_attributes,
    validate_required_params,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        ext_id=dict(type="str", required=True),
        type=dict(
            type="str",
            choices=["STANDARD", "ELEVATED", "STRICT", "NOT_SET", "NOT_SUPPORTED"],
        ),
    )
    return module_args


def _normalize_value(value):
    if value is None:
        return None
    if hasattr(value, "value"):
        return value.value
    return value


def check_security_profile_idempotency(current_spec, update_spec):
    return _normalize_value(getattr(current_spec, "type", None)) == _normalize_value(
        getattr(update_spec, "type", None)
    )


def update_security_profile(module, result, api_instance):
    validate_required_params(module, ["type"])
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    current_spec = get_security_profile_by_ext_id(module, api_instance, ext_id)
    etag_value = get_etag(data=current_spec)
    if not etag_value:
        module.fail_json(
            msg="Unable to fetch etag for updating security profile", **result
        )

    strip_users_empty_attributes(current_spec)

    sg = SpecGenerator(module)
    default_spec = copy.deepcopy(current_spec)
    update_spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating spec for updating security profile", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        result["msg"] = "Security profile will be updated."
        return

    if check_security_profile_idempotency(current_spec, update_spec):
        result["skipped"] = True
        module.exit_json(msg="Nothing to change.", **result)

    kwargs = {"if_match": etag_value}
    resp = None
    try:
        resp = api_instance.update_security_profile_by_id(
            extId=ext_id, body=update_spec, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating security profile",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        wait_for_completion(module, task_ext_id)
        updated = get_security_profile_by_ext_id(module, api_instance, ext_id)
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
    api_instance = get_security_profiles_api_instance(module)
    update_security_profile(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
