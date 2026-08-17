#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_iam_welcome_banner_v2
short_description: Manage the IAM Welcome Banner in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to update the IAM welcome banner in Nutanix Prism Central.
  - The welcome banner is a singleton resource that is displayed on the Prism Central
    login page before any authentication mechanism runs. It has no external ID.
  - When C(state=present) the module updates the banner content and enablement flag
    using the v4 PUT API (with C(If-Match) optimistic concurrency).
  - When C(state=absent) the module resets the banner to its factory defaults
    (disabled with the default content), which effectively hides the banner from
    the login page.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user
    performing the operation.
  - >-
    B(Update the Welcome Banner) - Required Roles: Super Admin, Prism Admin.
  - >-
    B(Reset the Welcome Banner) - Required Roles: Super Admin, Prism Admin.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=iam)"
options:
  state:
    description:
      - If C(state) is set to C(present) the welcome banner will be updated with
        the supplied C(content)/C(is_enabled) values.
      - If C(state) is set to C(absent) the welcome banner will be reset to its
        default state (C(is_enabled=false), default placeholder content).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - Placeholder external ID for the welcome banner.
      - The welcome banner is a singleton resource in Prism Central and does not
        have a real external ID; this option is accepted for consistency with the
        other CRUD-style v4 modules and is otherwise ignored.
    type: str
    required: false
  content:
    description:
      - Content of the welcome banner. Supports plain text and a subset of HTML
        (paragraphs, line breaks, custom coloring, and localized text).
      - Required when C(state=present).
    type: str
    required: false
  is_enabled:
    description:
      - Whether the welcome banner is displayed on the Prism Central login page.
      - When C(true) the banner is shown before the login connectors (Local,
        LDAP, SAML, CAC) and the user must click B(Accept) to proceed.
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
- name: Update the welcome banner
  nutanix.ncp.ntnx_iam_welcome_banner_v2:
    state: present
    content: "Authorized personnel only. All activity is monitored and recorded."
    is_enabled: true
  register: result

- name: Disable the welcome banner but keep the content
  nutanix.ncp.ntnx_iam_welcome_banner_v2:
    state: present
    content: "Authorized personnel only. All activity is monitored and recorded."
    is_enabled: false
  register: result

- name: Reset the welcome banner to defaults (disabled + placeholder content)
  nutanix.ncp.ntnx_iam_welcome_banner_v2:
    state: absent
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for updating or resetting the welcome banner.
    - Returns the full welcome banner details (content, is_enabled, created_time,
      last_updated_time) after the operation completes.
  returned: always
  type: dict
  sample:
    {
      "content": "Authorized personnel only. All activity is monitored and recorded.",
      "created_time": "2026-06-29T07:18:36.280134+00:00",
      "is_enabled": true,
      "last_updated_time": "2026-07-21T06:36:56.065999+00:00",
      "links": null,
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
    - The welcome banner PUT API is synchronous and does not return a task, so this
      field is always C(null) for this module. It is kept for API consistency with
      other v4 CRUD modules.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the welcome banner.
    - The welcome banner is a singleton resource and has no real external ID; this
      field is always C(null).
  returned: always
  type: str
  sample: null

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description: This indicates whether the task was skipped (idempotent no-op).
  returned: always
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
  description: This indicates the message if any message occurred.
  returned: When there is an error, the module is idempotent, or check mode is used.
  type: str
  sample: "Welcome banner is already in the desired state. Skipping update."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.iam.api_client import (  # noqa: E402
    get_etag,
    get_welcome_banner_api_instance,
)
from ..module_utils.v4.iam.helpers import get_welcome_banner  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
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

DEFAULT_BANNER_CONTENT = "Write HTML code here"
READ_ONLY_FIELDS = ("created_time", "last_updated_time")


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        content=dict(type="str"),
        is_enabled=dict(type="bool"),
    )
    return module_args


def _fetch_current_banner(module, api_instance):
    """Fetch the current welcome banner and its etag from Prism Central."""
    current = get_welcome_banner(module, api_instance)
    etag = get_etag(data=current)
    return current, etag


def _is_no_op(current_dict, desired_dict):
    """Return True when the desired banner already matches the current banner."""
    current_dict = strip_internal_attributes(deepcopy(current_dict))
    desired_dict = strip_internal_attributes(deepcopy(desired_dict))
    for field in READ_ONLY_FIELDS:
        current_dict.pop(field, None)
        desired_dict.pop(field, None)
    return current_dict == desired_dict


def create_welcome_banner(module, result, api_instance):
    """
    The welcome banner is a singleton resource — it is always present in Prism
    Central. "Create" for this entity is therefore the same operation as
    "update": push the desired content/is_enabled via PUT.
    """
    update_welcome_banner(module, result, api_instance)


def update_welcome_banner(module, result, api_instance):
    validate_required_params(module, ["content"])

    current, etag = _fetch_current_banner(module, api_instance)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for updating the welcome banner", **result
        )

    sg = SpecGenerator(module)
    default_spec = identity_and_access_management_sdk.WelcomeBanner()
    update_spec, err = sg.generate_spec(obj=deepcopy(default_spec))
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating welcome banner update spec", **result)

    # `created_time` and `last_updated_time` are server-managed; a fresh spec
    # created via the SDK model does not carry them, so no explicit stripping
    # is required (the SDK property has no deleter).

    if module.check_mode:
        result["response"] = strip_internal_attributes(update_spec.to_dict())
        return

    if _is_no_op(current.to_dict(), update_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current.to_dict())
        result["msg"] = (
            "Welcome banner is already in the desired state. Skipping update."
        )
        return

    try:
        resp = api_instance.update_welcome_banner(body=update_spec, if_match=etag)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while updating the welcome banner",
        )

    if resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        fresh = get_welcome_banner(module, api_instance)
        result["response"] = strip_internal_attributes(fresh.to_dict())
    result["changed"] = True


def delete_welcome_banner(module, result, api_instance):
    """
    A welcome banner cannot be removed from Prism Central (it is a singleton).
    "Delete" for this module is therefore implemented as a reset: push a PUT
    that disables the banner and restores the factory default placeholder
    content. This is the closest analogue to a DELETE for an update-only
    singleton resource.
    """
    current, etag = _fetch_current_banner(module, api_instance)
    if not etag:
        return module.fail_json(
            msg="Unable to fetch etag for resetting the welcome banner", **result
        )

    reset_spec = identity_and_access_management_sdk.WelcomeBanner()
    reset_spec.content = DEFAULT_BANNER_CONTENT
    reset_spec.is_enabled = False

    if module.check_mode:
        result["response"] = strip_internal_attributes(reset_spec.to_dict())
        result["msg"] = "Welcome banner will be reset to default state."
        return

    if _is_no_op(current.to_dict(), reset_spec.to_dict()):
        result["skipped"] = True
        result["response"] = strip_internal_attributes(current.to_dict())
        result["msg"] = (
            "Welcome banner is already in the default state. Skipping reset."
        )
        return

    try:
        resp = api_instance.update_welcome_banner(body=reset_spec, if_match=etag)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while resetting the welcome banner",
        )

    if resp.data:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    else:
        fresh = get_welcome_banner(module, api_instance)
        result["response"] = strip_internal_attributes(fresh.to_dict())
    result["changed"] = True
    result["msg"] = "Welcome banner has been reset to the default state."


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("content",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_iam_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }

    api_instance = get_welcome_banner_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_welcome_banner(module, result, api_instance)
        else:
            create_welcome_banner(module, result, api_instance)
    else:
        delete_welcome_banner(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
