#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
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
  - The CSR is returned as an C(application/octet-stream) download and saved to a local file.
  - The local downloaded file path is returned under C(response.path).
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Download Cluster Certificate Signing Request) -
    Required Roles: Cluster Admin, Cluster Viewer, Prism Admin, Prism Viewer, Super Admin
  - This module talks to B(Prism Central) (PC). It does not target FCVM/Foundation.
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
  dest:
    description:
      - Local destination file path where the downloaded CSR should be saved.
      - The parent directory is created if it does not already exist.
      - If not provided, the CSR is saved to the SDK default download location and that path is returned.
    type: path
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
- name: Download a Certificate Signing Request from a cluster
  nutanix.ncp.ntnx_download_csr_by_id_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    csr_ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
  register: result
  ignore_errors: true

- name: Download a Certificate Signing Request to a specific destination path
  nutanix.ncp.ntnx_download_csr_by_id_v2:
    cluster_ext_id: "00061fa4-ef93-7dd8-185b-ac1f6b6f97e2"
    csr_ext_id: "7c6bc5f3-c18c-4702-4c2d-b769fd5f94b0"
    dest: "/tmp/ansible_csr.pem"
  register: result
  ignore_errors: true
"""

RETURN = r"""
response:
  description:
    - Response for downloading a Certificate Signing Request from a cluster.
    - Contains the local path of the downloaded CSR file.
  returned: always
  type: dict
  sample:
    {
      "path": "/tmp/ansible_csr.pem"
    }

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
import shutil  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.clusters_mgmt.api_client import (  # noqa: E402
    get_certificate_manager_api_instance,
)
from ..module_utils.v4.clusters_mgmt.helpers import download_csr  # noqa: E402

# Suppress the InsecureRequestWarning
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():
    module_args = dict(
        cluster_ext_id=dict(type="str", required=True),
        csr_ext_id=dict(type="str", required=True),
        dest=dict(type="path"),
    )
    return module_args


def download_csr_by_id(module, api_instance, result):
    cluster_ext_id = module.params.get("cluster_ext_id")
    csr_ext_id = module.params.get("csr_ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = csr_ext_id

    if module.check_mode:
        if dest:
            result["msg"] = (
                "Certificate Signing Request with ext_id: {0} "
                "will be downloaded to destination path: {1}".format(csr_ext_id, dest)
            )
            result["response"] = {"path": dest}
        else:
            result["msg"] = (
                "Certificate Signing Request with ext_id: {0} will be downloaded.".format(
                    csr_ext_id
                )
            )
        return

    if dest:
        dest_dir = os.path.dirname(os.path.abspath(dest))
        if dest_dir and not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        api_instance.api_client.configuration.download_directory = dest_dir

    resp = download_csr(module, api_instance, cluster_ext_id, csr_ext_id)

    data = resp.data
    if isinstance(data, dict):
        downloaded_path = data.get("path")
    else:
        downloaded_path = getattr(data, "path", None)

    if not downloaded_path:
        module.fail_json(
            msg="Failed to determine the downloaded Certificate Signing Request file path",
            **result,
        )

    downloaded_path = str(downloaded_path)
    if dest and os.path.abspath(downloaded_path) != os.path.abspath(dest):
        shutil.move(downloaded_path, dest)
        downloaded_path = dest

    result["response"] = {"path": downloaded_path}


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=True,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "failed": False, "response": None, "ext_id": None}
    api_instance = get_certificate_manager_api_instance(module)
    download_csr_by_id(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
