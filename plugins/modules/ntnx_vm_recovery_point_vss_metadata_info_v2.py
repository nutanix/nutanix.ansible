#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2027, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_vm_recovery_point_vss_metadata_info_v2
short_description: Download VSS metadata for a VM recovery point in Nutanix Prism Central
version_added: 2.7.0
description:
  - Download the Volume Shadow Copy Service (VSS) metadata associated with a specific
    VM recovery point.
  - The API returns the VSS metadata cabinet file (.cab) as an C(application/octet-stream)
    download and saves it to a local file.
  - The local downloaded file path is returned under C(response.path).
  - Backup agents can use this metadata during application-specific backup and restore operations.
  - Both the parent recovery point external ID and the VM recovery point external ID are required.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get VSS metadata by VM recovery point ID) -
    Required Roles: Disaster Recovery Admin, Prism Admin, Project Admin, Project Manager, Super Admin, Tenant Admin, Tenant Consumer
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=dataprotection)"
options:
  recovery_point_ext_id:
    description:
      - The external identifier that can be used to retrieve the recovery point using its URL.
    type: str
    required: true
  vm_recovery_point_ext_id:
    description:
      - The external identifier that can be used to identify a VM recovery point.
    type: str
    required: true
  dest:
    description:
      - Local destination file path where the downloaded VSS metadata (.cab) should be saved.
      - The parent directory is created if it does not already exist.
      - If not provided, the file is saved to the SDK default download location and that path is returned.
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
- name: Download VSS metadata for a VM recovery point
  nutanix.ncp.ntnx_vm_recovery_point_vss_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
  register: result

- name: Download VSS metadata to a specific destination path
  nutanix.ncp.ntnx_vm_recovery_point_vss_metadata_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    recovery_point_ext_id: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"
    vm_recovery_point_ext_id: "522670d7-e92d-45c5-9139-76ccff6813c2"
    dest: "/tmp/vm_rp_vss_metadata.cab"
  register: result
"""
RETURN = r"""
response:
  description: A dict containing the local path of the downloaded VSS metadata file.
  returned: always
  type: dict
  sample:
    {
        "path": "/tmp/vm_rp_vss_metadata.cab"
    }

changed:
  description: This indicates whether the task resulted in any changes.
  returned: always
  type: bool
  sample: false

ext_id:
  description:
    - External ID of the VM recovery point whose VSS metadata was downloaded.
  type: str
  returned: always
  sample: "522670d7-e92d-45c5-9139-76ccff6813c2"

recovery_point_ext_id:
  description:
    - External ID of the parent recovery point.
  type: str
  returned: always
  sample: "1ca2963d-77b6-453a-ae23-2c19e7a954a3"

error:
  description: Error details when the task fails.
  type: str
  returned: when an error occurs

msg:
  description: Message returned when an error occurs.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching VSS metadata for a VM recovery point using ext_ids"

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false
"""

import os  # noqa: E402
import shutil  # noqa: E402
import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.data_protection.api_client import (  # noqa: E402
    get_recovery_point_api_instance,
)
from ..module_utils.v4.data_protection.helpers import (  # noqa: E402
    get_vss_metadata_by_vm_recovery_point,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        recovery_point_ext_id=dict(type="str", required=True),
        vm_recovery_point_ext_id=dict(type="str", required=True),
        dest=dict(type="path"),
    )

    return module_args


def get_vss_metadata_using_vm_rp_ext_id(module, recovery_points, result):
    recovery_point_ext_id = module.params.get("recovery_point_ext_id")
    vm_recovery_point_ext_id = module.params.get("vm_recovery_point_ext_id")
    dest = module.params.get("dest")
    result["ext_id"] = vm_recovery_point_ext_id
    result["recovery_point_ext_id"] = recovery_point_ext_id

    if dest:
        dest_dir = os.path.dirname(os.path.abspath(dest))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        recovery_points.api_client.configuration.download_directory = dest_dir

    resp = get_vss_metadata_by_vm_recovery_point(
        module, recovery_points, recovery_point_ext_id, vm_recovery_point_ext_id
    )

    data = resp.data
    if isinstance(data, dict):
        downloaded_path = data.get("path")
    else:
        downloaded_path = getattr(data, "path", None)

    if not downloaded_path:
        module.fail_json(
            msg="Failed to determine the downloaded VSS metadata file path",
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
        supports_check_mode=False,
        skip_info_args=True,
    )
    remove_param_with_none_value(module.params)
    result = {"changed": False, "response": None, "failed": False}
    recovery_points = get_recovery_point_api_instance(module)
    get_vss_metadata_using_vm_rp_ext_id(module, recovery_points, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
