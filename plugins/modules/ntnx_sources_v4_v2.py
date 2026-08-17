#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_sources_v4_v2
short_description: Manage aiops SourcesV4 in Nutanix Prism Central
version_added: 2.7.0
description:
  - Provides a Create/Update/Delete-style interface for aiops SourcesV4
    entities in Nutanix Prism Central.
  - >-
    IMPORTANT — the aiops v4 SDK (C(ntnx_aiops_py_client), C(StatsApi))
    exposes SourcesV4 as a read-only singleton catalog
    (C(GET /api/aiops/v4.2.b1/config/sources)) with NO
    Create/Update/Delete server endpoints. When invoked, this module reports
    that limitation and points callers to M(nutanix.ncp.ntnx_sources_info_v2)
    for the supported read operation.
  - This module uses PC v4 APIs based SDKs (namespace C(aiops)).
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(List aiops SourcesV4) -
      Required Roles: Consumer, Developer, Operator, Prism Admin, Prism Viewer, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=aiops)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the
        operation is I(create) SourcesV4 — currently unsupported by the aiops
        SDK, and the module will fail with a clear error.
      - If C(state) is set to C(present) and C(ext_id) is provided then the
        operation is I(update) SourcesV4 — currently unsupported by the aiops
        SDK, and the module will fail with a clear error.
      - If C(state) is set to C(absent) and C(ext_id) is provided then the
        operation is I(delete) SourcesV4 — currently unsupported by the aiops
        SDK, and the module will fail with a clear error.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the aiops SourcesV4.
      - Required for update and delete operations.
    type: str
    required: false
  source_name:
    description:
      - Human-readable name of the aiops source (e.g. C(nutanix)).
      - The SDK exposes this as a read-only attribute on the C(Source) model.
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
- name: Attempt to create an aiops SourcesV4 (unsupported by SDK — will fail)
  nutanix.ncp.ntnx_sources_v4_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    source_name: "custom_source"
  register: result
  ignore_errors: true

- name: Attempt to update an aiops SourcesV4 (unsupported by SDK — will fail)
  nutanix.ncp.ntnx_sources_v4_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "d2c1a3a4-0000-0000-0000-000000000001"
    source_name: "custom_source_renamed"
  register: result
  ignore_errors: true

- name: Attempt to delete an aiops SourcesV4 (unsupported by SDK — will fail)
  nutanix.ncp.ntnx_sources_v4_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "d2c1a3a4-0000-0000-0000-000000000001"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, updating, or deleting aiops SourcesV4.
    - Because the aiops SDK exposes SourcesV4 as a read-only catalog, this
      module cannot mutate the resource. When an existing C(ext_id) is
      supplied and C(state=present), the current Source object is returned
      unchanged; otherwise the module fails.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "db293e8a-5770-c3c7-4213-85dbbc1d3679",
      "links": null,
      "source_name": "nutanix",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task.
    - Not populated because the aiops SDK does not support async
      create/update/delete for SourcesV4.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the aiops SourcesV4.
  returned: always
  type: str
  sample: "db293e8a-5770-c3c7-4213-85dbbc1d3679"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: false

skipped:
  description:
    - This indicates whether the task was skipped.
    - Set to C(true) when the requested update matches the existing
      immutable source (idempotent no-op).
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred
  returned: When an error occurs
  type: str

failed:
  description: This indicates whether the task failed
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred
  returned: When there is an error, module is idempotent or check mode (in delete operation)
  type: str
  sample: "SourcesV4 create is not supported by the aiops v4 SDK — the sources catalog is read-only. Use ntnx_sources_info_v2 to list existing sources."
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.aiops.api_client import get_stats_api_instance  # noqa: E402
from ..module_utils.v4.aiops.helpers import get_source_by_ext_id  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_aiops_py_client as aiops_sdk  # noqa: F401,E402
except ImportError:

    from ..module_utils.v4.sdk_mock import mock_sdk as aiops_sdk  # noqa: F401,E402

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")

_UNSUPPORTED_MSG_FMT = (
    "SourcesV4 {op} is not supported by the aiops v4 SDK — the sources "
    "catalog is read-only. Use ntnx_sources_info_v2 to list existing sources."
)


def get_module_spec():
    module_args = dict(
        ext_id=dict(type="str"),
        source_name=dict(type="str"),
    )
    return module_args


def _source_exists(module, api_instance, ext_id):
    try:
        return get_source_by_ext_id(module, api_instance, ext_id) is not None
    except Exception:
        return False


def create_SourcesV4(module, result, api_instance):
    validate_required_params(module, ["source_name"])
    msg = _UNSUPPORTED_MSG_FMT.format(op="create")
    result["failed"] = True
    result["msg"] = msg
    module.fail_json(**result)


def update_SourcesV4(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    current = get_source_by_ext_id(module, api_instance, ext_id)
    current_dict = strip_internal_attributes(current.to_dict())
    result["response"] = current_dict

    requested_name = module.params.get("source_name")
    if requested_name is None or requested_name == current_dict.get("source_name"):
        result["skipped"] = True
        result["msg"] = (
            "SourcesV4 with ext_id '{0}' is immutable and matches the "
            "requested state. Nothing to change.".format(ext_id)
        )
        return

    if module.check_mode:
        result["msg"] = (
            "Check mode: SourcesV4 with ext_id '{0}' cannot be updated because "
            "the aiops v4 SDK exposes the sources catalog as read-only.".format(ext_id)
        )
        return

    msg = _UNSUPPORTED_MSG_FMT.format(op="update")
    result["failed"] = True
    result["msg"] = msg
    module.fail_json(**result)


def delete_SourcesV4(module, result, api_instance):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "Check mode: SourcesV4 with ext_id '{0}' cannot be deleted because "
            "the aiops v4 SDK exposes the sources catalog as read-only.".format(ext_id)
        )
        return

    # Verify the source exists before reporting the unsupported-delete error.
    # If the ext_id is bogus the helper will emit a descriptive "not found"
    # message and fail_json for us; if it exists we surface the SDK-limitation
    # message so callers understand the delete failure is not transient.
    get_source_by_ext_id(module, api_instance, ext_id)

    msg = _UNSUPPORTED_MSG_FMT.format(op="delete")
    result["failed"] = True
    result["msg"] = msg
    module.fail_json(**result)


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_aiops_py_client"),
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
    api_instance = get_stats_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_SourcesV4(module, result, api_instance)
        else:
            create_SourcesV4(module, result, api_instance)
    else:
        delete_SourcesV4(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
