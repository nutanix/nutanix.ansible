#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_lcm_upgrade_selection_v2
short_description: Create, Export or Delete an LCM Upgrade Selection in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create, export and delete an LCM Upgrade Selection in Nutanix Prism Central.
  - An LCM Upgrade Selection is used by the Dark Site Upgrade Orchestrator (DUO) to lock a set of
    selected LCM upgrade targets (entity_uuid + to_version) for a cluster and to generate the
    darksite download_helper.zip helper bundle for offline binary download.
  - An LCM Upgrade Selection is immutable after creation - the underlying API deliberately
    does not expose a PUT/update endpoint. When C(ext_id) is provided together with
    C(state=present), this module will trigger the export action (download_helper.zip)
    on the existing selection if C(export) is C(true); otherwise the module reports
    C(skipped=true) because there is nothing to update.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
      The required roles depend on the operation being performed.
    - >-
      B(Create an LCM Upgrade Selection) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Export an LCM Upgrade Selection) -
      Required Roles: Prism Admin, Super Admin
    - >-
      B(Delete an LCM Upgrade Selection) -
      Required Roles: Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=lifecycle)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided then the operation will create an LCM upgrade selection.
      - If C(state) is set to C(present) and C(ext_id) is provided with C(export=true)
        then the export action will run on the existing selection.
      - If C(state) is set to C(present) and C(ext_id) is provided without C(export=true)
        then the module reports skipped (the selection is immutable).
      - If C(state) is set to C(absent) then the operation will delete the LCM upgrade selection identified by C(ext_id).
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the LCM Upgrade Selection.
      - Required for delete and export operations.
    type: str
    required: false
  cluster_ext_id:
    description:
      - External ID of the cluster on which the LCM Upgrade Selection is scoped.
      - This is a read-only attribute on the entity itself; the value returned in
        the response reflects the cluster the selection is bound to.
    type: str
    required: false
  selected_upgrades:
    description:
      - List of upgrade selections. Each element identifies an LCM entity and the
        version it should be upgraded to.
      - Required for create operation.
    type: list
    elements: dict
    required: false
    suboptions:
      entity_uuid:
        description:
          - UUID of the LCM entity being upgraded.
        type: str
        required: true
      to_version:
        description:
          - Target version of the LCM entity.
        type: str
        required: true
  export:
    description:
      - When C(true) and C(ext_id) is provided together with C(state=present),
        the module invokes the export action which produces the darksite
        C(download_helper.zip) helper bundle for the specified upgrade selection.
      - When omitted or C(false) with C(ext_id) and C(state=present), the module
        reports C(skipped=true) since LCM Upgrade Selections are immutable.
    type: bool
    required: false
    default: false
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
- name: Create an LCM upgrade selection
  nutanix.ncp.ntnx_lcm_upgrade_selection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    selected_upgrades:
      - entity_uuid: "15570c98-beaf-4633-afd2-b6a306ff1001"
        to_version: "5.0.0"
  register: result
  ignore_errors: true

- name: Export an LCM upgrade selection (download helper zip)
  nutanix.ncp.ntnx_lcm_upgrade_selection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: present
    ext_id: "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a"
    export: true
  register: result
  ignore_errors: true

- name: Delete an LCM upgrade selection
  nutanix.ncp.ntnx_lcm_upgrade_selection_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    state: absent
    ext_id: "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for creating, exporting or deleting an LCM upgrade selection.
    - If the operation is create and C(wait) is C(true), it returns the LCM upgrade selection details.
    - If the operation is create and C(wait) is C(false), it returns the task details.
    - If the operation is export, it returns the task details (the actual helper zip is streamed by the server).
    - If the operation is delete, it returns the task details.
  returned: always
  type: dict
  sample:
    {
      "cluster_ext_id": "00062e00-87eb-ef15-0000-00000000b71a",
      "ext_id": "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a",
      "links": null,
      "selected_upgrades": [
        {
          "entity_uuid": "15570c98-beaf-4633-afd2-b6a306ff1001",
          "to_version": "5.0.0"
        }
      ],
      "status": "UPGRADE_READY",
      "tenant_id": null
    }

task_ext_id:
  description:
    - The external ID of the task associated with the operation, when the API returns a task reference.
  returned: always
  type: str
  sample: "ZXJnb24=:90458bc7-a12b-4616-ac66-562fdb00c209"

ext_id:
  description:
    - The external ID of the LCM upgrade selection.
  returned: always
  type: str
  sample: "b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a"

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped.
    - Set to C(true) when C(state=present) with C(ext_id) and C(export=false),
      because LCM upgrade selections are immutable.
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
  returned: When there is an error, module is idempotent, or check mode (in delete/export operation)
  type: str
  sample: >-
    LCM upgrade selection with ext_id: b7dbcf46-8ba3-4dcd-a7c3-4b09b0f7a11a is
    immutable. Nothing to update; pass export=true to export the download helper.
"""

import traceback  # noqa: E402
import warnings  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.constants import Tasks as TASK_CONSTANTS  # noqa: E402
from ..module_utils.v4.lcm.api_client import (  # noqa: E402
    get_upgrade_selections_api_instance,
)
from ..module_utils.v4.lcm.helpers import get_upgrade_selection  # noqa: E402
from ..module_utils.v4.prism.tasks import (  # noqa: E402
    get_entity_ext_id_from_task,
    wait_for_completion,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_lifecycle_py_client as life_cycle_management_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as life_cycle_management_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    entity_update_spec = dict(
        entity_uuid=dict(type="str", required=True),
        to_version=dict(type="str", required=True),
    )

    module_args = dict(
        ext_id=dict(type="str"),
        cluster_ext_id=dict(type="str"),
        selected_upgrades=dict(
            type="list",
            elements="dict",
            options=entity_update_spec,
            obj=life_cycle_management_sdk.EntityUpdateSpec,
        ),
        export=dict(type="bool", default=False),
    )
    return module_args


def create_upgrade_selection(module, api_instance, result):
    validate_required_params(module, ["selected_upgrades"])
    sg = SpecGenerator(module)
    default_spec = life_cycle_management_sdk.UpgradeSelection()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(
            msg="Failed generating create LCM upgrade selection spec", **result
        )

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_upgrade_selection(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating LCM upgrade selection",
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
        ext_id = get_entity_ext_id_from_task(
            task_resp, rel=TASK_CONSTANTS.RelEntityType.UPGRADE_SELECTION
        )
        if ext_id:
            result["ext_id"] = ext_id
            entity = get_upgrade_selection(module, api_instance, ext_id)
            result["response"] = strip_internal_attributes(entity.to_dict())
        else:
            raise_api_exception(
                module=module,
                exception=Exception(
                    "Failed to get entity ext_id from task for LCM Upgrade Selection"
                ),
                msg="Failed to get entity ext_id from task for LCM Upgrade Selection",
            )
    result["changed"] = True


def update_upgrade_selection(module, api_instance, result):
    """
    LCM Upgrade Selections are immutable - the SDK/API deliberately does not
    expose a PUT/update endpoint. When ext_id is provided together with
    state=present, we either trigger the export action (when export=true) or
    report a skipped/idempotent no-op with a descriptive message.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.params.get("export"):
        export_upgrade_selection(module, api_instance, result)
        return

    entity = get_upgrade_selection(module, api_instance, ext_id)
    result["response"] = strip_internal_attributes(entity.to_dict())
    result["skipped"] = True
    result["changed"] = False
    module.exit_json(
        msg=(
            "LCM upgrade selection with ext_id: {0} is immutable. Nothing to "
            "update; pass export=true to export the download helper."
        ).format(ext_id),
        **result,
    )


def export_upgrade_selection(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "LCM upgrade selection with ext_id: {0} will be exported "
            "(download_helper.zip)."
        ).format(ext_id)
        return

    resp = None
    try:
        resp = api_instance.export_upgrade_selection(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while exporting LCM upgrade selection with ext_id: {0}".format(
                ext_id
            ),
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_resp = wait_for_completion(module, task_ext_id)
        result["response"] = strip_internal_attributes(task_resp.to_dict())
    result["changed"] = True


def delete_upgrade_selection(module, api_instance, result):
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "LCM upgrade selection with ext_id: {0} will be deleted.".format(ext_id)
        )
        return

    resp = None
    try:
        resp = api_instance.delete_upgrade_selection_by_id(extId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while deleting LCM upgrade selection with ext_id: {0}".format(
                ext_id
            ),
        )

    task_ext_id = getattr(resp.data, "ext_id", None)
    result["task_ext_id"] = task_ext_id
    if resp.data is not None:
        result["response"] = strip_internal_attributes(resp.data.to_dict())
    if task_ext_id and module.params.get("wait"):
        task_status = wait_for_completion(module, task_ext_id, raise_error=False)
        result["response"] = strip_internal_attributes(task_status.to_dict())
    result["changed"] = True


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
            msg=missing_required_lib("ntnx_lifecycle_py_client"),
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
    api_instance = get_upgrade_selections_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_upgrade_selection(module, api_instance, result)
        else:
            create_upgrade_selection(module, api_instance, result)
    else:
        delete_upgrade_selection(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
