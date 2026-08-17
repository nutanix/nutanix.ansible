#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Nutanix
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntnx_files_infected_files_info_v2
short_description: Fetch info about infected files on Nutanix Files file servers
version_added: 2.5.0
description:
  - This module allows you to fetch information about InfectedFile in Nutanix Prism Central.
  - If C(ext_id) is provided, fetch details of the specific InfectedFile.
  - If C(ext_id) is not provided, list multiple InfectedFile optionally filtered / paginated.
  - This module uses PC v4 APIs based SDKs.
notes:
  - >-
    This module requires the following Nutanix IAM roles to be assigned to the user performing the operation.
  - >-
    B(Get an infected file by ext_id) -
    Required Roles: Consumer, Developer, Prism Admin, Prism Viewer, Super Admin
  - >-
    B(List infected files) -
    Required Roles: Consumer, Developer, Prism Admin, Prism Viewer, Super Admin
  - "Ref: U(https://developers.nutanix.com/api-reference?namespace=files)"
options:
  file_server_ext_id:
    description:
      - The external ID of the parent Nutanix Files file server.
    type: str
    required: true
  ext_id:
    description:
      - The external ID of the infected file.
      - When provided, a single infected file is fetched.
      - When omitted, a list of infected files under the file server is returned.
    type: str
    required: false
extends_documentation_fragment:
  - nutanix.ncp.ntnx_credentials
  - nutanix.ncp.ntnx_info_v2
  - nutanix.ncp.ntnx_logger
  - nutanix.ncp.ntnx_proxy_v2
author:
  - Nutanix (@nutanix)
"""

EXAMPLES = r"""
- name: Get infected file by ext_id
  nutanix.ncp.ntnx_files_infected_files_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    ext_id: "b7a4c8e6-1234-5678-9abc-def012345678"
  register: single_infected

- name: List all infected files under a file server
  nutanix.ncp.ntnx_files_infected_files_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
  register: all_infected

- name: List infected files with an OData filter (quarantined only)
  nutanix.ncp.ntnx_files_infected_files_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    filter: "isQuarantined eq true"
  register: quarantined

- name: List infected files with a limit
  nutanix.ncp.ntnx_files_infected_files_info_v2:
    nutanix_host: "{{ ip }}"
    nutanix_username: "{{ username }}"
    nutanix_password: "{{ password }}"
    validate_certs: false
    file_server_ext_id: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"
    limit: 5
  register: limited
"""

RETURN = r"""
response:
  description:
    - The response from the Nutanix PC InfectedFile info v4 API.
    - It can be a single InfectedFile if external ID is provided.
    - List of multiple InfectedFile if external ID is not provided with optional filter or limit.
  returned: always
  type: dict
  sample:
    [
      {
        "ext_id": "b7a4c8e6-1234-5678-9abc-def012345678",
        "is_quarantined": true,
        "links": null,
        "mount_target_ext_id": "aa11bb22-cc33-dd44-ee55-ff6677889900",
        "partner_server": "icap-01.example.com",
        "path": "/share/malware/eicar.txt",
        "scan_time": "2026-07-21T05:12:33.123456+00:00",
        "tenant_id": null,
        "threat_description": "EICAR-Test-File"
      }
    ]

changed:
  description: This indicates whether the task resulted in any changes. Always false for info modules.
  returned: always
  type: bool
  sample: false

msg:
  description: This indicates the message if any message occurred.
  returned: When there is an error
  type: str
  sample: "Api Exception raised while fetching infected files info"

error:
  description: This field typically holds information about if the task have errors that occurred during the task execution.
  type: str
  returned: when an error occurs

failed:
  description: This field typically holds information about if the task have failed.
  returned: always
  type: bool
  sample: false

ext_id:
  description: External ID of the infected file.
  type: str
  returned: when external ID is provided
  sample: "b7a4c8e6-1234-5678-9abc-def012345678"

file_server_ext_id:
  description: External ID of the parent file server.
  type: str
  returned: always
  sample: "d1e6f2fa-5c8a-4d2f-9a3b-1a2b3c4d5e6f"

total_available_results:
  description: The total number of available infected files under the file server.
  type: int
  returned: when the list operation is used
  sample: 3
"""

import warnings  # noqa: E402

from ..module_utils.utils import remove_param_with_none_value  # noqa: E402
from ..module_utils.v4.base_info_module import BaseInfoModule  # noqa: E402
from ..module_utils.v4.files.api_client import (  # noqa: E402
    get_infected_files_api_instance,
)
from ..module_utils.v4.files.helpers import get_infected_file  # noqa: E402
from ..module_utils.v4.spec_generator import SpecGenerator  # noqa: E402
from ..module_utils.v4.utils import (  # noqa: E402
    raise_api_exception,
    strip_internal_attributes,
)

warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")


def get_module_spec():

    module_args = dict(
        file_server_ext_id=dict(type="str", required=True),
        ext_id=dict(type="str", required=False),
    )
    return module_args


def get_infected_file_using_ext_id(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    ext_id = module.params.get("ext_id")
    resp = get_infected_file(module, api_instance, file_server_ext_id, ext_id)
    result["file_server_ext_id"] = file_server_ext_id
    result["ext_id"] = ext_id
    result["response"] = strip_internal_attributes(resp.to_dict())


def list_infected_files(module, api_instance, result):
    file_server_ext_id = module.params.get("file_server_ext_id")
    result["file_server_ext_id"] = file_server_ext_id

    sg = SpecGenerator(module)
    kwargs, err = sg.get_info_spec(attr=module.params)
    if err:
        result["error"] = err
        module.fail_json(msg="Failed generating infected files info spec", **result)

    try:
        resp = api_instance.list_infected_files(
            fileServerExtId=file_server_ext_id, **kwargs
        )
    except Exception as e:
        raise_api_exception(
            module=module,
            exception=e,
            msg="Api Exception raised while fetching infected files info",
        )

    total_available_results = resp.metadata.total_available_results
    result["total_available_results"] = total_available_results
    resp = strip_internal_attributes(resp.to_dict()).get("data")
    if not resp:
        resp = []
    result["response"] = resp


def run_module():
    module = BaseInfoModule(
        argument_spec=get_module_spec(),
        supports_check_mode=False,
        mutually_exclusive=[
            ("ext_id", "filter"),
            ("ext_id", "limit"),
            ("ext_id", "page"),
            ("ext_id", "orderby"),
            ("ext_id", "select"),
        ],
    )
    remove_param_with_none_value(module.params)
    result = {
        "changed": False,
        "response": None,
        "failed": False,
        "file_server_ext_id": None,
    }
    api_instance = get_infected_files_api_instance(module)
    if module.params.get("ext_id"):
        get_infected_file_using_ext_id(module, api_instance, result)
    else:
        list_infected_files(module, api_instance, result)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
