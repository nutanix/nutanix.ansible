#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_scan_migration_impact_role_v2
short_description: Scan migration impact for a role
version_added: "2.7.0"
description:
    - This module scans migration impact for a role identified by its external ID.
    - This module uses PC v4 APIs based SDKs
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Scan migration impact role) -
      Required Roles: Nutanix Central Admin, Prism Admin, Project Manager, Super Admin, Self-Service Admin (deprecated)
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=identity_and_access_management)"
options:
    ext_id:
        description:
            - The external ID of the role.
        type: str
        required: true
    state:
        description:
            - State of the module.
            - If C(state) is C(present), the module will scan migration impact for the role.
            - If C(state) is C(absent), the module will fail.
        type: str
        choices:
            - present
        default: present
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
- name: Scan migration impact for a role
  nutanix.ncp.ntnx_scan_migration_impact_role_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    ext_id: "00000000-0000-0000-0000-000000000001"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - Response for scanning migration impact for a role.
        - If C(wait) is true, it will contain the final task payload after completion.
        - If C(wait) is false, it will contain the initial task details.
    returned: always
    type: dict
    sample:
        {
            "data": [
                {
                    "arguments_map": null,
                    "code": "200",
                    "error_group": null,
                    "locale": "en_US",
                    "message": "NOT_IMPACTED",
                    "severity": null
                }
            ],
            "metadata": null
        }
changed:
    description: This indicates whether the task resulted in any changes
    returned: always
    type: bool
    sample: true
msg:
    description: This indicates the message if any message occurred
    returned: When there is an error
    type: str
    sample: "Api Exception raised while scanning migration impact for role"
error:
    description: This field typically holds information about if the task have errors that occurred during the task execution
    returned: when an error occurs
    type: str
failed:
    description: This field typically holds information about if the task have failed
    returned: always
    type: bool
    sample: false
task_ext_id:
    description: The external ID of the task
    returned: always
    type: str
    sample: "ZXJnb24=:0e040d14-5dcf-5302-8b48-d3c6cf115cd1"
ext_id:
    description: The external ID of the role
    returned: always
    type: str
    sample: "00000000-0000-0000-0000-000000000001"
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_role_api_instance,
)
from ..module_utils.v4.iam.helpers import get_role  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str", required=True),
        state=dict(type="str", default="present", choices=["present"]),
    )
    return module_args


def run_action(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["response"] = {
            "ext_id": ext_id,
            "msg": "Check mode: scan would be performed",
        }
        return

    # Fetch etag for If-Match header
    current_spec = get_role(module, api_instance, ext_id)
    etag = get_etag(data=current_spec)
    if not etag:
        module.fail_json(msg="Unable to fetch etag for scanning role", **result)
    kwargs = {"if_match": etag}

    resp = None
    try:
        resp = api_instance.scan_migration_impact_role(extId=ext_id, **kwargs)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while scanning migration impact for role",
        )

    try:
        resp_dict = strip_internal_attributes(resp.to_dict())
    except Exception:
        resp_dict = {}

    result["response"] = resp_dict

    try:
        if hasattr(resp, "data") and resp.data:
            data = resp.data
            if hasattr(data, "ext_id") and getattr(data, "ext_id"):
                result["task_ext_id"] = data.ext_id
            elif isinstance(resp_dict.get("data"), dict):
                inner = resp_dict.get("data")
                if inner and inner.get("ext_id"):
                    result["task_ext_id"] = inner.get("ext_id")
    except Exception:
        pass

    task_ext_id = result.get("task_ext_id")
    if task_ext_id and module.params.get("wait"):
        try:
            from ..module_utils.v4.prism.tasks import wait_for_completion  # noqa: E402

            task = wait_for_completion(module, task_ext_id)
            result["response"] = strip_internal_attributes(task.to_dict())
        except Exception:
            pass

    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )

    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None}

    api_instance = get_role_api_instance(module)
    run_action(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
