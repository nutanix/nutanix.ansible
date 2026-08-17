#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_report_artifact_v2
short_description: Create, Update, Delete report artifacts in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module allows you to create and manage report artifacts in Nutanix Prism Central.
  - A ReportArtifact stores a binary asset (typically a LOGO in PNG/JPEG format) that is
    embedded in generated NCM/Intelligent Operations reports.
  - Creation is a two-step workflow, only the metadata (I(type), I(file_type)) is required
    up front; the binary can then be uploaded by providing I(file_path).
  - When updating an existing artifact (I(ext_id) set) this module re-uploads the binary
    file, since the underlying opsmgmt v4 API does not support metadata mutation.
  - The opsmgmt v4 API does not currently expose a delete endpoint; C(state=absent)
    is therefore reported as skipped with a descriptive message.
  - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user
      performing the operation. The required roles depend on the operation being performed.
    - >-
      B(Create a Report Artifact) -
      Required Roles: Prism Admin, Super Admin, NCM Admin, Intelligent Ops Admin, Project Admin
    - >-
      B(Upload a Report Artifact binary) -
      Required Roles: Prism Admin, Super Admin, NCM Admin, Intelligent Ops Admin, Project Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided the operation is
        create report artifact (optionally followed by an upload of I(file_path)).
      - If C(state) is set to C(present) and C(ext_id) is provided the operation is
        upload/replace the artifact binary for the existing metadata (I(file_path) is
        required in that case).
      - If C(state) is set to C(absent) and C(ext_id) is provided the module reports
        a skipped operation because the opsmgmt v4 ReportArtifact API does not expose a
        delete endpoint.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of an existing report artifact.
      - Required for update and delete-style operations.
    type: str
    required: false
  type:
    description:
      - Type of the report artifact.
      - Required for create operation.
    type: str
    required: false
    choices:
      - LOGO
  file_type:
    description:
      - File extension / MIME family of the report artifact binary.
      - Required for create operation.
    type: str
    required: false
    choices:
      - PNG
      - JPEG
  file_path:
    description:
      - Local filesystem path to the binary file (PNG/JPEG) that must be uploaded to
        the report artifact.
      - When provided together with a create operation the module will first create
        the artifact metadata and then upload the binary.
      - Required when I(ext_id) is provided and I(state) is C(present) — in that case
        this module re-uploads the binary for the existing artifact.
    type: path
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
- name: Create report artifact metadata only
  nutanix.ncp.ntnx_report_artifact_v2:
    state: present
    type: LOGO
    file_type: PNG
  register: result

- name: Create report artifact and upload binary in one step
  nutanix.ncp.ntnx_report_artifact_v2:
    state: present
    type: LOGO
    file_type: PNG
    file_path: /tmp/report_logo.png
  register: result

- name: Upload a new binary for an existing report artifact (update flow)
  nutanix.ncp.ntnx_report_artifact_v2:
    state: present
    ext_id: "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11"
    file_path: /tmp/updated_report_logo.png
  register: result

- name: Delete report artifact (reports skipped — API does not support delete)
  nutanix.ncp.ntnx_report_artifact_v2:
    state: absent
    ext_id: "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11"
  register: result
"""

RETURN = r"""
response:
  description:
    - Response for creating or uploading a report artifact.
    - For create it is the ReportArtifact entity returned by the API (including the
      newly assigned C(ext_id)).
    - For a create-plus-upload flow, this is the ReportArtifact enriched with the
      response from the upload action.
    - For an update flow (upload only) it is the response of the upload action.
    - For a delete-style call (C(state=absent)) it echoes the informational message.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11",
      "file_type": "PNG",
      "links": null,
      "tenant_id": null,
      "type": "LOGO"
    }

task_ext_id:
  description:
    - The external ID of the task.
    - The opsmgmt ReportArtifact API is synchronous and does not return a task
      reference — this field is therefore always C(null) for this module.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the report artifact.
  returned: always
  type: str
  sample: "e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped (idempotency or an operation the
      API does not support, e.g. delete).
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
  sample: "ReportArtifact with ext_id:'e4f3a1c2-1a29-4a4b-8f2e-4b5f2f9c0f11' cannot be deleted. Delete is not supported by the opsmgmt v4 ReportArtifact API."
"""

import os  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.opsmgmt.api_client import (  # noqa: E402
    get_report_artifacts_api_instance,
)
from ..module_utils.v4.opsmgmt.helpers import (  # noqa: E402
    get_report_artifact_by_ext_id,
)
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_opsmgmt_py_client as ncm_operation_base_platform_sdk  # noqa: E402
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: E402
        mock_sdk as ncm_operation_base_platform_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    """
    Argument spec for :module:`ntnx_report_artifact_v2`.

    Every field mirrors the ``ReportArtifact`` model in the opsmgmt v4 SDK:

    * ``type`` and ``file_type`` are enums — ``choices=`` restricts them to
      the values the SDK's :class:`ArtifactType` / :class:`ArtifactFileType`
      accept (``LOGO`` / ``PNG`` / ``JPEG``). They are marked optional
      here because they are only required for create; per-operation
      validation is performed inside :func:`create_ReportArtifact` /
      :func:`update_ReportArtifact` via ``validate_required_params``.
    * ``file_path`` accepts a local filesystem path pointing to the binary
      to upload; it is optional on create (metadata-only artifact) and
      required on update (there is no metadata-only update API).
    """
    module_args = dict(
        ext_id=dict(type="str"),
        type=dict(
            type="str",
            choices=["LOGO"],
            obj=ncm_operation_base_platform_sdk.ArtifactType,
        ),
        file_type=dict(
            type="str",
            choices=["PNG", "JPEG"],
            obj=ncm_operation_base_platform_sdk.ArtifactFileType,
        ),
        file_path=dict(type="path"),
    )
    return module_args


def _upload_artifact_file(module, api_instance, ext_id, file_path):
    """
    Upload the local binary at ``file_path`` to the report artifact
    identified by ``ext_id``.

    Args:
        module (AnsibleModule): the calling module — used to route SDK
            errors through :func:`raise_api_exception`.
        api_instance (ReportArtifactsApi): SDK client instance.
        ext_id (str): the artifact's ``extId``.
        file_path (str): local filesystem path to the binary. Must exist
            and be a file — the caller is expected to have validated
            this. The SDK will still raise ``ValueError`` if not.

    Returns:
        dict: the upload API response converted with ``to_dict`` and
        stripped of v4 internal attributes.
    """
    try:
        resp = api_instance.upload_artifact_file(
            reportArtifactExtId=ext_id, path=Path(file_path)
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uploading report artifact binary",
        )
        return None
    return strip_internal_attributes(resp.to_dict())


def create_ReportArtifact(module, result, api_instance):  # noqa: N802
    """
    Handle the ``state=present`` + no ``ext_id`` code path.

    Steps:
        1. Validate that both ``type`` and ``file_type`` are provided.
        2. Build a :class:`ReportArtifact` spec via :class:`SpecGenerator`.
        3. Short-circuit in ``check_mode`` returning the built spec.
        4. Call the SDK ``create_report_artifact`` and record the assigned
           ``ext_id`` in the result.
        5. If ``file_path`` is provided, immediately upload the binary
           against the freshly created artifact.
    """
    validate_required_params(module, ["type", "file_type"])
    sg = SpecGenerator(module)
    default_spec = ncm_operation_base_platform_sdk.ReportArtifact()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create report artifact spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        return

    resp = None
    try:
        resp = api_instance.create_report_artifact(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating report artifact",
        )

    artifact = resp.data
    result["response"] = strip_internal_attributes(artifact.to_dict())
    ext_id = getattr(artifact, "ext_id", None)
    if not ext_id:
        raise_api_exception(
            module=module,
            exception=Exception(
                "Failed to get ext_id from create response for ReportArtifact"
            ),
            msg="Failed to get ext_id from create response for ReportArtifact",
        )
    result["ext_id"] = ext_id
    result["changed"] = True

    file_path = module.params.get("file_path")
    if file_path:
        upload_resp = _upload_artifact_file(module, api_instance, ext_id, file_path)
        result["response"] = {
            "artifact": result["response"],
            "upload": upload_resp,
        }


def update_ReportArtifact(module, result, api_instance):  # noqa: N802
    """
    Handle the ``state=present`` + ``ext_id`` code path.

    The opsmgmt v4 ReportArtifact API has no metadata-mutation endpoint,
    so "update" is redefined as "replace the binary attached to an
    existing artifact via the upload action". Consequently:

    * ``file_path`` is required in this branch.
    * If the artifact matching ``ext_id`` cannot be found we fail with a
      descriptive error.
    * ``check_mode`` short-circuits without touching the cluster.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["file_path"])

    old = get_report_artifact_by_ext_id(module, api_instance, ext_id)
    if old is None:
        module.fail_json(
            msg="ReportArtifact with ext_id:'{0}' not found. Cannot update.".format(
                ext_id
            ),
            **result,
        )

    result["response"] = strip_internal_attributes(old.to_dict())

    if module.check_mode:
        result["msg"] = (
            "ReportArtifact with ext_id:'{0}' will be updated by uploading '{1}'.".format(
                ext_id, module.params.get("file_path")
            )
        )
        return

    upload_resp = _upload_artifact_file(
        module, api_instance, ext_id, module.params.get("file_path")
    )
    result["response"] = {
        "artifact": strip_internal_attributes(old.to_dict()),
        "upload": upload_resp,
    }
    result["changed"] = True


def delete_ReportArtifact(module, result, api_instance):  # noqa: N802
    """
    Handle the ``state=absent`` code path.

    The opsmgmt v4 ``ReportArtifactsApi`` does not expose a delete
    endpoint (see the SDK class docstring). Rather than fail hard — which
    would break playbooks that naturally rely on "state: absent" for
    cleanup — we mark the operation as skipped and surface a clear
    message so users understand why nothing happened on the cluster.

    ``api_instance`` is accepted for a consistent signature with the
    create / update handlers, even though it is not used here.
    """
    del api_instance
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id

    msg = (
        "ReportArtifact with ext_id:'{0}' cannot be deleted. "
        "Delete is not supported by the opsmgmt v4 ReportArtifact API.".format(ext_id)
    )
    result["skipped"] = True
    result["msg"] = msg
    result["response"] = {"message": msg}


def run_module():
    """
    Wire up the argument spec, create the API instance, and dispatch to
    the ``state`` handler.

    Uses ``required_if`` so Ansible fails fast when the caller forgets
    ``ext_id`` on ``state=absent`` or forgets either the type/file_type
    pair (create) or ``ext_id`` (update) on ``state=present``.
    """
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
            ("state", "present", ("ext_id", "type"), True),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_opsmgmt_py_client"),
            exception=SDK_IMP_ERROR,
        )

    remove_param_with_none_value(module.params)

    file_path = module.params.get("file_path")
    if file_path and not os.path.isfile(file_path):
        module.fail_json(
            msg="file_path '{0}' does not point to an existing file.".format(file_path)
        )

    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "ext_id": None,
        "task_ext_id": None,
        "skipped": False,
    }
    api_instance = get_report_artifacts_api_instance(module)
    state = module.params.get("state")
    if state == "present":
        if module.params.get("ext_id"):
            update_ReportArtifact(module, result, api_instance)
        else:
            create_ReportArtifact(module, result, api_instance)
    else:
        delete_ReportArtifact(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
