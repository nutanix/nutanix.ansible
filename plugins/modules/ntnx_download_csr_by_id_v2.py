#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_download_csr_by_id_v2
short_description: Download a Certificate Signing Request (CSR) from a cluster in Nutanix Prism Central
version_added: 2.7.0
description:
  - This module downloads a Certificate Signing Request (CSR) file from a cluster in Nutanix Prism Central.
  - This is an action module that fetches the CSR file content for a given CSR external ID.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Download a Certificate Signing Request) -
    Required Roles: Prism Admin, Super Admin
  - This module talks to Prism Central (PC), not FCVM/Foundation.
  - The referenced cluster and Certificate Signing Request must exist before downloading the CSR file.
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=clustermgmt)"
options:
  cluster_ext_id:
    description:
      - The external ID of the cluster that owns the Certificate Signing Request.
    type: str
    required: true
  csr_ext_id:
    description:
      - The external ID of the Certificate Signing Request (CSR) to download.
    type: str
    required: true
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
- name: Download a Certificate Signing Request from a cluster
  nutanix.ncp.ntnx_download_csr_by_id_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    csr_ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for downloading a Certificate Signing Request from a cluster.
    - Contains the CSR file content (PEM-encoded) or the path to the downloaded file returned by the SDK.
  returned: always
  type: dict
  sample:
    "-----BEGIN CERTIFICATE REQUEST-----\nMIIC...==\n-----END CERTIFICATE REQUEST-----\n"

ext_id:
  description:
    - The external ID of the downloaded Certificate Signing Request.
  returned: always
  type: str
  sample: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"

changed:
  description: This indicates whether the action resulted in any changes.
  returned: always
  type: bool
  sample: false

error:
  description: This indicates the error message if any error occurred.
  returned: when an error occurs
  type: str

failed:
  description: This indicates whether the task failed.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the status/error message if any message occurred.
  returned: When there is an error or in check mode
  type: str
  sample: "Certificate Signing Request with ext_id: 7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0 will be downloaded."
"""

import os  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_module_v4 import BaseModuleV4  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_certificate_manager_api_instance,
)
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    validate_required_params,
)

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        csr_ext_id=dict(type="str", required=True),
    )
    return module_args


def _read_and_cleanup_file(path):
    """Read the content of a downloaded file and remove it from disk.

    The download CSR SDK call writes the CSR to a temporary file on disk. This
    helper reads its content back and removes the file so it does not pollute the
    working directory.
    """
    content = None
    try:
        with open(path, "r") as f:
            content = f.read()
    except Exception:
        try:
            with open(path, "rb") as f:
                content = f.read().decode("utf-8", errors="replace")
        except Exception:
            content = None
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
    return content


def _serialize_download_response(data):
    """Convert the SDK download response into a JSON-serializable value.

    The download CSR API returns the CSR file. Depending on the SDK version the
    returned data may be a dict containing a file path, a file path, bytes, or a
    string. This helper normalizes it into a string so it can be safely returned
    to the user.
    """
    if data is None:
        return None

    # The SDK may return the file as a dict with a "path" pointing to the file.
    if isinstance(data, dict):
        path = data.get("path")
        if path is not None:
            content = _read_and_cleanup_file(str(path))
            if content is not None:
                return content
        return data

    # Some SDK versions return a file path (str or Path) to the downloaded content.
    path_str = str(data)
    if os.path.isfile(path_str):
        content = _read_and_cleanup_file(path_str)
        if content is not None:
            return content

    if isinstance(data, bytes):
        try:
            return data.decode("utf-8")
        except Exception:
            return str(data)
    if hasattr(data, "to_dict"):
        return data.to_dict()
    return str(data)


def download_csr(module, result, api_instance):
    validate_required_params(module, ["cluster_ext_id", "csr_ext_id"])
    cluster_ext_id = module.params.get("cluster_ext_id")
    csr_ext_id = module.params.get("csr_ext_id")
    result["ext_id"] = csr_ext_id

    if module.check_mode:
        result["msg"] = (
            "Certificate Signing Request with ext_id: {0} will be downloaded.".format(
                csr_ext_id
            )
        )
        return

    resp = None
    try:
        resp = api_instance.download_csr_by_id(
            clusterExtId=cluster_ext_id, csrExtId=csr_ext_id
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while downloading CSR with ext_id: {0}".format(
                csr_ext_id
            ),
        )

    data = getattr(resp, "data", resp)
    result["response"] = _serialize_download_response(data)
    result["changed"] = False


def run_module():
    module = BaseModuleV4(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "ext_id": None,
    }
    api_instance = get_certificate_manager_api_instance(module)
    download_csr(module, result, api_instance)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
