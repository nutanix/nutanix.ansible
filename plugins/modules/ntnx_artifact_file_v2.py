#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_artifact_file_v2
short_description: Create, upload and download report ArtifactFile in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module manages report artifact files (a.k.a. C(ArtifactFile)) in
    Nutanix Prism Central via the NCM Reports (opsmgmt) v4 API.
  - Report artifacts are graphic assets (for example, a company C(LOGO))
    that are referenced by the reporting engine when a report is rendered
    so administrators can brand exported reports.
  - This module allows you to
    - create the report artifact metadata (C(type), C(file_type)),
    - upload the binary file contents to an existing artifact, and
    - download the binary file contents of an existing artifact.
  - The opsmgmt v4 API does not expose an update or a delete operation for
    report artifacts, so C(state=absent) is not supported by this module.
  - Re-uploading against the same C(ext_id) effectively replaces the
    previously stored file contents for that artifact.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the Nutanix IAM privileges to manage report
    artifacts. Typical required roles are Prism Admin, Super Admin, or a
    custom role that carries the C(OpsMgmt:Upload_Report_Artifact) and
    C(OpsMgmt:View_Report_Artifact_File) operation permissions.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=opsmgmt)"
options:
  state:
    description:
      - If C(state) is set to C(present) and C(ext_id) is not provided the
        module creates a new report artifact. When C(file_path) is also
        supplied the file contents are uploaded to the newly created
        artifact as a single flow.
      - If C(state) is set to C(present) and C(ext_id) is provided the
        module operates on the existing artifact. Provide C(file_path) to
        upload / replace its binary contents, or C(download_path) to
        download the stored file to disk.
      - C(state=absent) is B(not supported) - the opsmgmt v4 API does not
        expose a delete endpoint for report artifacts. Attempting it will
        fail with a clear error message.
    type: str
    required: false
    choices:
      - present
      - absent
    default: present
  ext_id:
    description:
      - The external ID of the report artifact.
      - Required to upload contents to an existing artifact or to download
        its file.
    type: str
    required: false
  type:
    description:
      - Type of the report artifact.
      - Required when creating a new artifact (i.e. when C(ext_id) is not
        provided).
    type: str
    required: false
    choices:
      - LOGO
  file_type:
    description:
      - File extension / MIME shape of the report artifact.
      - Required when creating a new artifact (i.e. when C(ext_id) is not
        provided).
    type: str
    required: false
    choices:
      - PNG
      - JPEG
  file_path:
    description:
      - Absolute path (on the Ansible controller) of the local file whose
        contents should be uploaded to the report artifact.
      - When provided along with C(ext_id) the file is uploaded to the
        existing artifact.
      - When provided during create (no C(ext_id)) the file is uploaded
        immediately after the artifact metadata is created.
    type: path
    required: false
  download_path:
    description:
      - Absolute path (on the Ansible controller) where the artifact's
        binary file should be written when downloading.
      - Requires C(ext_id) to be set.
      - Mutually exclusive with C(file_path).
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
- name: Create a report artifact (LOGO metadata only)
  nutanix.ncp.ntnx_artifact_file_v2:
    state: present
    type: LOGO
    file_type: PNG
  register: create_result

- name: Create a report artifact and upload the logo file in one call
  nutanix.ncp.ntnx_artifact_file_v2:
    state: present
    type: LOGO
    file_type: PNG
    file_path: "/tmp/company_logo.png"
  register: create_and_upload

- name: Upload / replace the file of an existing report artifact
  nutanix.ncp.ntnx_artifact_file_v2:
    state: present
    ext_id: "7e3d1c17-4e49-4397-4b0f-00cd0debb46c"
    file_path: "/tmp/updated_company_logo.png"
  register: upload_result

- name: Download the binary file of an existing report artifact
  nutanix.ncp.ntnx_artifact_file_v2:
    state: present
    ext_id: "7e3d1c17-4e49-4397-4b0f-00cd0debb46c"
    download_path: "/tmp/downloaded_logo.png"
  register: download_result
"""

RETURN = r"""
response:
  description:
    - Response for creating, uploading or downloading a report artifact.
    - When the operation is create, the value is the created
      C(ReportArtifact) metadata (C(type), C(file_type), C(ext_id), ...).
    - When the operation is upload, the value is the SDK response object
      returned by the upload endpoint - typically a list of status
      messages plus response metadata.
    - When the operation is download, the value describes the download
      outcome including the C(download_path) on disk.
  returned: always
  type: dict
  sample:
    {
      "ext_id": "7e3d1c17-4e49-4397-4b0f-00cd0debb46c",
      "file_type": "PNG",
      "links": null,
      "tenant_id": null,
      "type": "LOGO"
    }

task_ext_id:
  description:
    - The external ID of the task, if any, for the operation.
    - The report artifact API is synchronous and does not return task
      references, so this is usually C(None) for this module.
  returned: always
  type: str
  sample: null

ext_id:
  description:
    - The external ID of the report artifact acted upon.
  returned: always
  type: str
  sample: "7e3d1c17-4e49-4397-4b0f-00cd0debb46c"

changed:
  description: This indicates whether the task resulted in any changes
  returned: always
  type: bool
  sample: true

skipped:
  description:
    - This indicates whether the task was skipped, for example when
      C(state=absent) is requested (not supported) or when there is
      nothing to do for the given parameters.
  returned: when applicable
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
  description:
    - This indicates the message describing what happened, for example
      the check-mode preview, an idempotent skip, or an error summary.
  returned: When there is an error, module is in check mode, or the
    operation was skipped
  type: str
  sample: "Api Exception raised while creating report artifact"
"""

import os  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402
from copy import deepcopy  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.content.api_client import (  # noqa: E402
    get_report_artifacts_api_instance,
)
from ..module_utils.v4.content.helpers import get_report_artifact  # noqa: E402
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

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        ext_id=dict(type="str"),
        type=dict(
            type="str",
            choices=["LOGO"],
            obj=getattr(ncm_operation_base_platform_sdk, "ArtifactType", None),
        ),
        file_type=dict(
            type="str",
            choices=["PNG", "JPEG"],
            obj=getattr(ncm_operation_base_platform_sdk, "ArtifactFileType", None),
        ),
        file_path=dict(type="path"),
        download_path=dict(type="path"),
    )
    return module_args


def _report_artifact_to_dict(artifact):
    """Return a JSON-safe dict for a ReportArtifact SDK object."""
    if artifact is None:
        return None
    if hasattr(artifact, "to_dict"):
        return strip_internal_attributes(artifact.to_dict())
    return strip_internal_attributes(deepcopy(artifact))


def _upload_file_to_artifact(module, api_instance, ext_id, file_path, result):
    """Upload the local ``file_path`` to the given report artifact ``ext_id``."""
    if not os.path.isfile(file_path):
        module.fail_json(
            msg="file_path '{0}' does not exist or is not a regular file".format(
                file_path
            ),
            **result,
        )
    try:
        resp = api_instance.upload_artifact_file(
            reportArtifactExtId=ext_id, path=file_path
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uploading report artifact file",
        )
    if hasattr(resp, "to_dict"):
        result["response"] = strip_internal_attributes(resp.to_dict())
    else:
        result["response"] = strip_internal_attributes(deepcopy(resp))
    result["changed"] = True
    return resp


def create_artifact_file(module, result, api_instance):
    """
    Create a new report artifact. When ``file_path`` is set, upload the
    file contents to the newly created artifact as a second step.
    """
    validate_required_params(module, ["type", "file_type"])

    file_path = module.params.get("file_path")
    if file_path and not os.path.isfile(file_path):
        module.fail_json(
            msg="file_path '{0}' does not exist or is not a regular file".format(
                file_path
            ),
            **result,
        )

    sg = SpecGenerator(module)
    default_spec = ncm_operation_base_platform_sdk.ReportArtifact()
    spec, err = sg.generate_spec(obj=default_spec)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating create report artifact spec", **result)

    if module.check_mode:
        result["response"] = strip_internal_attributes(spec.to_dict())
        result["msg"] = (
            "Report artifact would be created with the provided spec (check_mode)."
        )
        return

    try:
        resp = api_instance.create_report_artifact(body=spec)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while creating report artifact",
        )

    created = getattr(resp, "data", None)
    result["response"] = _report_artifact_to_dict(created)
    new_ext_id = getattr(created, "ext_id", None)
    if new_ext_id:
        result["ext_id"] = new_ext_id
    result["changed"] = True

    if file_path:
        if not new_ext_id:
            module.fail_json(
                msg=(
                    "Report artifact was created but no ext_id was returned by "
                    "the API; unable to upload the file contents."
                ),
                **result,
            )
        _upload_file_to_artifact(module, api_instance, new_ext_id, file_path, result)
        artifact = get_report_artifact(module, api_instance, new_ext_id)
        if artifact is not None:
            result["response"] = _report_artifact_to_dict(artifact)


def update_artifact_file(module, result, api_instance):
    """
    Operate on an existing report artifact.

    Because the opsmgmt v4 API does not expose an update endpoint for
    report artifacts, this branch dispatches to either an upload
    (when ``file_path`` is provided) or a download (when
    ``download_path`` is provided) - both of which act on an existing
    artifact identified by ``ext_id``.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    file_path = module.params.get("file_path")
    download_path = module.params.get("download_path")

    if not file_path and not download_path:
        result["skipped"] = True
        module.exit_json(
            msg=(
                "Nothing to do for report artifact ext_id={0}: provide "
                "'file_path' to upload contents or 'download_path' to "
                "download the file.".format(ext_id)
            ),
            **result,
        )

    if file_path and not os.path.isfile(file_path):
        module.fail_json(
            msg="file_path '{0}' does not exist or is not a regular file".format(
                file_path
            ),
            **result,
        )

    existing = get_report_artifact(module, api_instance, ext_id)
    if existing is None:
        module.fail_json(
            msg=(
                "Report artifact with ext_id '{0}' was not found on the "
                "Prism Central endpoint.".format(ext_id)
            ),
            **result,
        )

    if module.check_mode:
        preview = _report_artifact_to_dict(existing) or {}
        if file_path:
            preview["_pending_upload_from"] = file_path
            result["msg"] = (
                "Report artifact file for ext_id={0} would be uploaded "
                "from '{1}' (check_mode).".format(ext_id, file_path)
            )
        else:
            preview["_pending_download_to"] = download_path
            result["msg"] = (
                "Report artifact file for ext_id={0} would be downloaded "
                "to '{1}' (check_mode).".format(ext_id, download_path)
            )
        result["response"] = preview
        return

    if file_path:
        _upload_file_to_artifact(module, api_instance, ext_id, file_path, result)
        artifact = get_report_artifact(module, api_instance, ext_id)
        if artifact is not None:
            result["response"] = _report_artifact_to_dict(artifact)
        return

    _download_file_from_artifact(module, api_instance, ext_id, download_path, result)


def _download_file_from_artifact(module, api_instance, ext_id, download_path, result):
    """Download the artifact contents and persist them at ``download_path``."""
    try:
        resp = api_instance.download_artifact_file(reportArtifactExtId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading report artifact file",
        )

    data = getattr(resp, "data", None)
    persisted_path = _persist_downloaded_file(module, data, download_path, result)

    result["response"] = {
        "ext_id": ext_id,
        "download_path": persisted_path,
        "downloaded": True,
    }
    result["changed"] = True


def _persist_downloaded_file(module, data, download_path, result):
    """Copy the binary payload from the SDK download response to ``download_path``."""
    parent = os.path.dirname(os.path.abspath(download_path))
    if parent and not os.path.isdir(parent):
        try:
            os.makedirs(parent)
        except OSError as e:
            module.fail_json(
                msg="Failed to create directory '{0}' for download: {1}".format(
                    parent, str(e)
                ),
                **result,
            )

    try:
        if data is None:
            open(download_path, "wb").close()
        elif hasattr(data, "read"):
            with open(download_path, "wb") as fh:
                while True:
                    chunk = data.read(65536)
                    if not chunk:
                        break
                    fh.write(chunk)
        elif isinstance(data, (bytes, bytearray)):
            with open(download_path, "wb") as fh:
                fh.write(bytes(data))
        elif isinstance(data, str) and os.path.isfile(data):
            with open(data, "rb") as src, open(download_path, "wb") as dst:
                dst.write(src.read())
        else:
            with open(download_path, "wb") as fh:
                fh.write(str(data).encode("utf-8"))
    except OSError as e:
        module.fail_json(
            msg="Failed to persist downloaded artifact to '{0}': {1}".format(
                download_path, str(e)
            ),
            **result,
        )
    return download_path


def delete_artifact_file(module, result, api_instance):
    """
    Deletion of report artifacts is not exposed by the opsmgmt v4 API.

    We fail fast with a clear, actionable error so users understand that
    state=absent is not a supported operation for this entity today.
    """
    ext_id = module.params.get("ext_id")
    result["ext_id"] = ext_id
    result["skipped"] = True
    module.fail_json(
        msg=(
            "Deleting report artifacts (ArtifactFile) is not supported by "
            "the Nutanix opsmgmt v4 API. state=absent is therefore not "
            "supported by this module."
        ),
        **result,
    )


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("ext_id",)),
        ],
        mutually_exclusive=[
            ("file_path", "download_path"),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_opsmgmt_py_client"),
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

    api_instance = get_report_artifacts_api_instance(module)
    state = module.params.get("state")

    if state == "present":
        if module.params.get("ext_id"):
            update_artifact_file(module, result, api_instance)
        else:
            create_artifact_file(module, result, api_instance)
    else:
        delete_artifact_file(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
