#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_user_mapping_v2
short_description: Download or upload Nutanix Files user mappings for a file server
version_added: 2.7.0
description:
  - This module allows you to manage the file-server-wide user mappings
    configuration for a Nutanix Files server in Prism Central.
  - User mappings translate SMB (Active Directory) user or group identities
    into NFS (POSIX) identities (and the other way around) so that files
    accessed through different protocols retain consistent ownership.
  - Two operations are supported. C(download) fetches the current mapping table
    from the file server as a CSV file. C(upload) replaces the mapping table
    of the file server with the contents of a local CSV file.
  - The upload is a wholesale replacement of the existing mapping table.
    The typical workflow is C(download), edit the CSV locally, then C(upload).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the
    user performing the operation.
  - >-
    B(Download user mappings) -
    Required Roles: Prism Admin, Prism Viewer, Super Admin
  - >-
    B(Upload user mappings) -
    Required Roles: Prism Admin, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  state:
    description:
      - State of the module.
      - Only C(present) is supported since this module performs an action on
        an existing file server rather than creating or deleting an entity.
    type: str
    choices:
      - present
    default: present
  file_server_ext_id:
    description:
      - The external identifier of the file server whose user mappings should
        be downloaded or uploaded.
    type: str
    required: true
  operation:
    description:
      - Operation to perform on the file server user mappings.
      - Set to C(download) to fetch the current user mappings CSV from the
        file server.
      - Set to C(upload) to replace the user mappings on the file server with
        the CSV file at C(source_path).
    type: str
    choices:
      - download
      - upload
    required: true
  source_path:
    description:
      - Local filesystem path to the user mappings CSV file to upload.
      - Required when C(operation) is C(upload).
      - The file must be readable by the Ansible control node executing this
        module. The CSV is interpreted positionally by four columns
        C(smbName), C(nfsId), C(userOrGroup) and C(mappingType).
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
- name: Download user mappings from a file server
  nutanix.ncp.ntnx_user_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "6f6cbb1c-3f6f-46bf-9c9a-9c1234567890"
    operation: download
  register: download_result
  ignore_errors: true

- name: Upload user mappings CSV to a file server
  nutanix.ncp.ntnx_user_mapping_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "6f6cbb1c-3f6f-46bf-9c9a-9c1234567890"
    operation: upload
    source_path: "/tmp/user_mappings.csv"
  register: upload_result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response of the download or upload user mappings operation.
    - For C(operation=download) the response is a dict containing the local
      path to the downloaded user mappings CSV file.
    - For C(operation=upload) the response contains the SDK response data
      returned by the file server, typically a list of informational messages
      describing the effect of the upload.
  returned: always
  type: dict
  sample:
    {
      "path": "/tmp/user_mappings.csv"
    }

changed:
  description: Indicates whether the module made any change on the target file server.
  returned: always
  type: bool
  sample: true

ext_id:
  description:
    - External ID of the file server on which the user mappings operation was performed.
  returned: always
  type: str
  sample: "6f6cbb1c-3f6f-46bf-9c9a-9c1234567890"

task_ext_id:
  description:
    - External ID of the task that performed the operation on the file server.
    - These SDK endpoints execute synchronously and do not always return a
      dedicated task identifier, in which case this field remains C(null).
  returned: always
  type: str
  sample: null

msg:
  description: Status or error message.
  returned: When there is an error, an operation is skipped in check mode, or additional info is available
  type: str
  sample: "User mappings for file server with ext_id:6f6cbb1c-3f6f-46bf-9c9a-9c1234567890 will be downloaded."

error:
  description:
    - Error details when an API or validation failure occurs.
  returned: When an error occurs
  type: str
  sample: null

failed:
  description: Whether the module execution failed.
  returned: always
  type: bool
  sample: false
"""

import os  # noqa: E402
import traceback  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

from ansible.module_utils.basic import missing_required_lib  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_user_mappings_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
    validate_required_params,
)

SDK_IMP_ERROR = None
try:
    import ntnx_files_py_client as files_sdk  # noqa: F401,E402  # pylint: disable=unused-import
except ImportError:

    from ..module_utils.v4.sdk_mock import (  # noqa: F401,E402  # pylint: disable=unused-import
        mock_sdk as files_sdk,
    )

    SDK_IMP_ERROR = traceback.format_exc()

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        state=dict(type="str", default="present", choices=["present"]),
        file_server_ext_id=dict(type="str", required=True),
        operation=dict(
            type="str",
            required=True,
            choices=["download", "upload"],
        ),
        source_path=dict(type="path", required=False),
    )
    return module_args


def _extract_download_path(resp):
    """
    Best-effort extraction of the downloaded CSV file path from a
    DownloadUserMappings SDK response.

    The SDK returns a wrapper whose ``data`` attribute is a
    ``pathlib.Path`` on success. We accept anything path-like and
    fall back to a serialized ``dict`` form for older or mocked SDKs.
    """
    data = getattr(resp, "data", None)
    if data is None:
        return None
    if isinstance(data, Path):
        return str(data)
    if isinstance(data, str):
        return data
    for attr in ("path", "value"):
        val = getattr(data, attr, None)
        if val:
            return str(val)
    to_dict = getattr(data, "to_dict", None)
    if callable(to_dict):
        as_dict = to_dict() or {}
        if isinstance(as_dict, dict):
            for key in ("path", "value"):
                if as_dict.get(key):
                    return str(as_dict[key])
    return None


def download_user_mappings(module, api_instance, result):
    ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id

    if module.check_mode:
        result["msg"] = (
            "User mappings for file server with ext_id:{0} will be downloaded.".format(
                ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.download_user_mappings(fileServerExtId=ext_id)
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading user mappings for file server ext_id:{0}".format(
                ext_id
            ),
        )

    path = _extract_download_path(resp)
    if not path:
        module.fail_json(
            msg="Failed to determine downloaded user mappings path for file server ext_id:{0}".format(
                ext_id
            ),
            **result,
        )
    result["response"] = {"path": path}
    result["changed"] = True


def upload_user_mappings(module, api_instance, result):
    ext_id = module.params.get("file_server_ext_id")
    result["ext_id"] = ext_id
    validate_required_params(module, ["source_path"])

    source_path = module.params.get("source_path")
    if not os.path.isfile(source_path):
        module.fail_json(
            msg="source_path '{0}' does not exist or is not a regular file.".format(
                source_path
            ),
            **result,
        )

    if module.check_mode:
        result["msg"] = (
            "User mappings from '{0}' will be uploaded to file server with ext_id:{1}.".format(
                source_path, ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.upload_user_mappings(
            fileServerExtId=ext_id, path=Path(source_path)
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while uploading user mappings for file server ext_id:{0}".format(
                ext_id
            ),
        )

    if hasattr(resp, "to_dict"):
        result["response"] = strip_internal_attributes(resp.to_dict())
    else:
        result["response"] = resp
    result["changed"] = True


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        required_if=[
            ("operation", "upload", ("source_path",)),
        ],
    )
    if SDK_IMP_ERROR:
        module.fail_json(
            msg=missing_required_lib("ntnx_files_py_client"), exception=SDK_IMP_ERROR
        )

    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
        "task_ext_id": None,
    }
    api_instance = get_user_mappings_api_instance(module)
    operation = module.params.get("operation")
    if operation == "download":
        download_user_mappings(module, api_instance, result)
    else:
        upload_user_mappings(module, api_instance, result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
