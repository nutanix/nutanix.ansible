#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_ca_by_certificate_ids_info_v2
short_description: Fetch the Certificate Authority (CA) of Nutanix Object store certificates
version_added: 2.7.0
description:
    - This module allows you to fetch information about CaByCertificateId in Nutanix Prism Central.
    - It downloads the Certificate Authority (CA) associated with a specific Object store
      SSL certificate.
    - The Nutanix v4 Python SDK streams the CA response as C(application/octet-stream) and
      writes it to a file inside the configured C(download_directory); this module returns
      the SDK response along with the downloaded file path.
    - This module uses PC v4 APIs based SDKs.
notes:
    - >-
      This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
    - >-
      B(Download the certificate authority) -
      Required Roles: Objects Admin, Objects Editor, Objects Viewer, Prism Admin, Super Admin
    - "Ref: U(https://developers.nutanix.com/api-reference?namespace=objects)"
options:
    object_store_ext_id:
        description:
            - The external ID (UUID) of the Object store that owns the certificate.
        type: str
        required: true
    ext_id:
        description:
            - The external ID (UUID) of the certificate whose Certificate Authority (CA)
              is to be downloaded.
        type: str
        required: true
    read_timeout:
        description: Read timeout in milliseconds for API calls.
        type: int
        required: false
        default: 30000
extends_documentation_fragment:
    - nutanix.ncp.ntnx_credentials
    - nutanix.ncp.ntnx_logger
    - nutanix.ncp.ntnx_proxy_v2
author:
    - Abhinav Bansal (@abhinavbansal29)
    - George Ghawali (@george-ghawali)
"""

EXAMPLES = r"""
- name: Fetch the CA for an Object store certificate
  nutanix.ncp.ntnx_ca_by_certificate_ids_info_v2:
    object_store_ext_id: "cda893b8-2aee-34bf-817d-d2ee6026790b"
    ext_id: "b18822e9-b417-4834-6191-986010a4ee06"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
    description:
        - The response from the Nutanix PC CaByCertificateId info v4 API.
        - Contains the SDK response metadata and the path (under C(data)) to the file
          in which the SDK saved the streamed CA content.
    type: dict
    returned: always
    sample:
        {
            "data": "/tmp/ntnx_ca_info_tntisctw/ansible-object-2-certificate-authority-2026-07-21_2026-07-21T08:44:04.099.pem",
            "metadata": {
                "extra_info": null,
                "flags": [
                    {"name": "hasError", "value": false}
                ],
                "links": null,
                "messages": null,
                "total_available_results": null
            }
        }

ca_file_path:
    description:
        - The path returned by the SDK where the downloaded CA content was written.
    returned: when the SDK returns a downloaded file path
    type: str
    sample: "/tmp/ntnx_ca_info_tntisctw/ansible-object-2-certificate-authority-2026-07-21_2026-07-21T08:44:04.099.pem"

ext_id:
    description: External ID of the certificate whose CA was fetched.
    returned: always
    type: str
    sample: "e7855f76-fe69-455a-76b1-b3b3fddd67d2"

changed:
    description: This indicates whether the task resulted in any changes.
    returned: always
    type: bool
    sample: false

msg:
    description: Status/error message emitted by the module.
    returned: When there is an error
    type: str
    sample: "Api Exception raised while downloading CA by certificate ID"

error:
    description:
        - This field typically holds information about errors that occurred during the API call.
    returned: When an error occurs
    type: str

failed:
    description: This field indicates whether the task failed.
    returned: always
    type: bool
    sample: false
"""

import os  # noqa: E402
import tempfile  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.objects.api_client import get_objects_api_instance  # noqa: E402
from ..module_utils.v4.objects.helpers import get_ca_by_certificate_id  # noqa: E402
from ..module_utils.v4.utils import strip_internal_attributes  # noqa: E402

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        object_store_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=True),
    )
    return module_args


def _jsonify(value):
    """Recursively coerce SDK response values into JSON-serializable types.

    ``ntnx_objects_py_client`` streams the CA download to disk and returns
    a native ``pathlib.Path`` in ``resp.data``. That value flows into
    Ansible's ``exit_json`` unchanged and breaks ``_remove_values_conditions``
    (which only knows the primitive types). We walk the whole payload and
    convert any Path-like value into ``str``, leaving everything else
    untouched.
    """
    if isinstance(value, dict):
        return {k: _jsonify(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonify(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_jsonify(v) for v in value)
    if isinstance(value, (str, bool, int, float)) or value is None:
        return value
    if hasattr(value, "__fspath__"):
        return os.fspath(value)
    return value


def _serialize_response(resp):
    """Convert a v4 SDK response into a JSON-serializable dict.

    The ``get_ca_by_certificate_id`` API returns a response whose ``data``
    field is a ``pathlib.Path`` (or an SDK wrapper around one) pointing to
    the file the SDK streamed the CA into. ``to_dict()`` does not always
    stringify that Path, so we walk the payload and coerce every Path-like
    value into a string; SDK Path wrappers that serialize to a dict with a
    ``path`` key are also flattened to a plain string.
    """
    resp_dict = _jsonify(resp.to_dict())
    data = resp_dict.get("data")
    flattened = _flatten_path_dict(data)
    if flattened is not None:
        resp_dict["data"] = flattened
    return strip_internal_attributes(resp_dict)


def _flatten_path_dict(data):
    """Return a filesystem path string if ``data`` is an SDK Path dict."""
    if isinstance(data, dict) and "path" in data:
        path_value = data.get("path")
        if isinstance(path_value, str):
            return path_value
        if hasattr(path_value, "__fspath__"):
            return os.fspath(path_value)
    return None


def _pin_sdk_download_directory(api_instance):
    """Force the SDK's download directory to a per-invocation temp dir.

    ``ntnx_objects_py_client.Configuration`` defaults ``download_directory``
    to ``os.getcwd()`` at construction time. When Ansible runs the module
    from an ephemeral test/tempdir, that directory may not exist or may
    not be writable on subsequent invocations, so we pin it to a fresh
    ``tempfile.mkdtemp()`` we know we can create files in.
    """
    try:
        config = api_instance.api_client.configuration
    except AttributeError:
        return
    download_dir = tempfile.mkdtemp(prefix="ntnx_ca_info_")
    config.download_directory = download_dir


def _extract_downloaded_path(resp):
    """Return the filesystem path the SDK wrote the CA to, if any.

    ``get_ca_by_certificate_id`` may return the path as a native
    ``pathlib.Path``, as an SDK Path wrapper exposing a ``path`` attribute,
    or as a dict-of-str (once serialized via ``to_dict()``); we handle all
    three shapes so callers always get a plain string.
    """
    data = getattr(resp, "data", None)
    if data is None:
        return None
    if isinstance(data, str):
        return data
    if hasattr(data, "__fspath__"):
        return os.fspath(data)
    attr_path = getattr(data, "path", None)
    if attr_path is not None:
        if isinstance(attr_path, str):
            return attr_path
        if hasattr(attr_path, "__fspath__"):
            return os.fspath(attr_path)
    if isinstance(data, dict):
        return _flatten_path_dict(data)
    return None


def get_ca_by_certificate_id_info(module, result, api_instance):
    object_store_ext_id = module.params.get("object_store_ext_id")
    ext_id = module.params.get("ext_id")

    result["ext_id"] = ext_id

    _pin_sdk_download_directory(api_instance)
    resp = get_ca_by_certificate_id(module, api_instance, ext_id, object_store_ext_id)
    result["response"] = _serialize_response(resp)

    ca_file_path = _extract_downloaded_path(resp)
    if ca_file_path:
        result["ca_file_path"] = ca_file_path


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None}
    api_instance = get_objects_api_instance(module)
    get_ca_by_certificate_id_info(module, result, api_instance)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
